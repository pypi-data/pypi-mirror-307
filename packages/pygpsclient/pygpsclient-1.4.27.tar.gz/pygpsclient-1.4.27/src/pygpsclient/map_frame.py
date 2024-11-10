"""
map_frame.py

Mapview frame class for PyGPSClient application.

This handles a frame containing a location map which can be either:

 - one or more fixed offline maps based on user-provided georeferenced
   images e.g. geoTIFF (defaults to Mercator world image).
 - dynamic online map or satellite image accessed via a MapQuest API.

NOTE: The free MapQuest API key is subject to a limit of 15,000
transactions / month, or roughly 500 / day, so the map updates are only
run periodically (once a minute). This utility is NOT intended to be used for
real time navigation.

Created on 13 Sep 2020

:author: semuadmin
:copyright: 2020 SEMU Consulting
:license: BSD 3-Clause
"""

from http.client import responses
from io import BytesIO
from os import getenv
from time import time
from tkinter import CENTER, NW, Canvas, E, Frame, N, S, W, font

from PIL import Image, ImageTk, UnidentifiedImageError
from requests import ConnectionError as ConnError
from requests import ConnectTimeout, RequestException, get

from pygpsclient.globals import BGCOL, ICON_POS, IMG_WORLD, IMG_WORLD_CALIB, WIDGETU2
from pygpsclient.mapquest import (
    MAP_UPDATE_INTERVAL,
    MAPQTIMEOUT,
    MAPURL,
    MARKERURL,
    MAX_ZOOM,
    MIN_UPDATE_INTERVAL,
    MIN_ZOOM,
)
from pygpsclient.strings import (
    MAPCONFIGERR,
    MAPOPENERR,
    NOCONN,
    NOWEBMAPCONN,
    NOWEBMAPFIX,
    NOWEBMAPHTTP,
    NOWEBMAPKEY,
    OUTOFBOUNDS,
)

ZOOMCOL = "red"
ZOOMEND = "lightgray"
WORLD = "world"
CUSTOM = "custom"
MAP = "map"
SAT = "sat"


class MapviewFrame(Frame):
    """
    Map frame class.
    """

    def __init__(self, app, *args, **kwargs):
        """
        Constructor.

        :param Frame app: reference to main tkinter application
        :param args: optional args to pass to Frame parent class
        :param kwargs: optional kwargs to pass to Frame parent class
        """

        self.__app = app  # Reference to main application class
        self.__master = self.__app.appmaster  # Reference to root class (Tk)

        Frame.__init__(self, self.__master, *args, **kwargs)

        def_w, def_h = WIDGETU2
        self.width = kwargs.get("width", def_w)
        self.height = kwargs.get("height", def_h)
        self._img = None
        self._marker = None
        self._last_map_update = 0
        self._resize_font = font.Font(size=min(int(self.height / 5), 30))
        self._resize_font_height = self._resize_font.metrics("linespace")
        self._resize_font_width = self._resize_font.measure("+")
        self._zoom = int((MAX_ZOOM - MIN_ZOOM) / 2)
        self._lastmaptype = ""
        self._lastmappath = ""
        self._mapimage = None
        self._body()
        self._attach_events()

    def _body(self):
        """
        Set up frame and widgets.
        """

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self._can_mapview = Canvas(self, width=self.width, height=self.height, bg=BGCOL)
        self._can_mapview.grid(column=0, row=0, sticky=(N, S, E, W))

    def _attach_events(self):
        """
        Bind events to frame.
        """

        self.bind("<Configure>", self._on_resize)
        self._can_mapview.bind("<Double-Button-1>", self.on_refresh)  # double-click
        self._can_mapview.bind("<Button-1>", self.on_zoom)  # left-click
        self._can_mapview.bind("<Button-2>", self.on_zoom)  # right click Posix
        self._can_mapview.bind("<Button-3>", self.on_zoom)  # right-click Windows

    def init_frame(self):
        """
        Initialise map.
        """

        self._zoom = self.__app.frm_settings.config.get("mapzoom", 10)

    def on_refresh(self, event):  # pylint: disable=unused-argument
        """
        Trigger refresh of web map.

        :param event: event
        """

        self._last_map_update = 0

    def on_zoom(self, event):  # pylint: disable=unused-argument
        """
        Trigger zoom in or out.

        Left click (event.num = 1) increments zoom by 1.
        Right click (event.num = 2/3) increments zoom to maximum extent.

        :param event: event
        """

        refresh = False
        w, h = self.width, self.height
        fw, fh = self._resize_font_width, self._resize_font_height
        # zoom out (-) if not already at min
        zinc = 0
        if w > event.x > w - 2 - fw and h > event.y > h - fh:
            if self._zoom > MIN_ZOOM:
                zinc = -1 if event.num == 1 else MIN_ZOOM - self._zoom
                refresh = True
        # zoom in (+) if not already at max
        elif w > event.x > w - 2 - fw and h - fh > event.y > h - fh * 2:
            if self._zoom < MAX_ZOOM:
                zinc = 1 if event.num == 1 else MAX_ZOOM - self._zoom
                refresh = True

        if refresh:
            self._zoom += zinc
            self.__app.frm_settings.mapzoom.set(self._zoom)
            self.on_refresh(event)

    def update_frame(self):
        """
        Draw map and mark current known position and horizontal accuracy (where available).
        """

        lat = self.__app.gnss_status.lat
        lon = self.__app.gnss_status.lon
        hacc = self.__app.gnss_status.hacc

        # if no valid position, display warning message
        # fix = kwargs.get("fix", 0)
        if (
            lat in (None, "")
            or lon in (None, "")
            or (lat == 0 and lon == 0)
            # or fix in (0, 5)  # no fix or time only
        ):
            self.reset_map_refresh()
            self._disp_error(NOWEBMAPFIX)
            return

        maptype = self.__app.frm_settings.config.get("maptype_s", WORLD)
        if maptype in (WORLD, CUSTOM):
            self._draw_offline_map(lat, lon, maptype)
        else:
            self._draw_online_map(lat, lon, maptype, hacc)

    def _draw_offline_map(
        self,
        lat: float,
        lon: float,
        maptype: str = WORLD,
    ):
        """
        Draw fixed offline map using optional user-provided georeferenced
        image path(s) and calibration bounding box(es).

        Defaults to Mercator world image with bounding box [90, -180, -90, 180]
        if location is not within bounds of any custom map.

        :param float lat: latitude
        :param float lon: longitude
        :param str maptype: "world" or "custom"
        """
        # pylint: disable=no-member

        w, h = self.width, self.height
        self._lastmaptype = maptype
        bounds = IMG_WORLD_CALIB
        err = ""

        if maptype == CUSTOM:
            err = OUTOFBOUNDS
            # usermaps = self.__app.frm_settings.config.get("usermaps_l", [])
            usermaps = self.__app.saved_config.get("usermaps_l", [])
            for mp in usermaps:
                try:
                    mpath, bounds = mp
                    if (bounds[0] > lat > bounds[2]) and (bounds[1] < lon < bounds[3]):
                        if self._lastmappath != mpath:
                            self._mapimage = Image.open(mpath)
                            self._lastmappath = mpath
                        err = ""
                        break
                except (ValueError, IndexError):
                    err = MAPCONFIGERR
                    break
                except (FileNotFoundError, UnidentifiedImageError):
                    err = MAPOPENERR.format(mpath.split("/")[-1])
                    break

        if maptype == WORLD or err != "":
            if self._lastmappath != IMG_WORLD:
                self._mapimage = Image.open(IMG_WORLD)
                self._lastmappath = IMG_WORLD
            bounds = IMG_WORLD_CALIB

        self._can_mapview.delete("all")
        self._img = ImageTk.PhotoImage(self._mapimage.resize((w, h)))
        self._can_mapview.create_image(0, 0, image=self._img, anchor=NW)
        plon = w / (bounds[3] - bounds[1])  # x pixels per degree lon
        plat = h / (bounds[0] - bounds[2])  # y pixels per degree lat
        x = (lon - bounds[1]) * plon
        y = (bounds[0] - lat) * plat
        self._marker = ImageTk.PhotoImage(Image.open(ICON_POS))
        self._can_mapview.create_image(x, y, image=self._marker, anchor=CENTER)
        if err != "":
            self._can_mapview.create_text(w / 2, h / 2, text=err, fill="orange")

    def _draw_online_map(
        self, lat: float, lon: float, maptype: str = MAP, hacc: float = 0
    ):
        """
        Draw scalable web map or satellite image via online MapQuest API.

        :param float lat: latitude
        :param float lon: longitude
        :param str maptype: "map" or "sat"
        :param float hacc: horizontal accuracy
        """

        sc = NOCONN
        msg = ""
        hacc = hacc if isinstance(hacc, (float, int)) else 0

        if maptype != self._lastmaptype:
            self._lastmaptype = maptype
            self.reset_map_refresh()

        mqapikey = self.__app.frm_settings.config.get(
            "mqapikey_s", getenv("MQAPIKEY", "")
        )
        if mqapikey == "":
            self._disp_error(NOWEBMAPKEY)
            return
        map_update_interval = max(
            self.__app.frm_settings.config.get(
                "mapupdateinterval_n",
                self.__app.frm_settings.config.get(
                    "mapupdateinterval", MAP_UPDATE_INTERVAL
                ),
            ),
            MIN_UPDATE_INTERVAL,
        )

        now = time()
        if now - self._last_map_update < map_update_interval:
            self._draw_countdown(
                (-360 / map_update_interval) * (now - self._last_map_update)
            )
            return
        self._last_map_update = now

        url = self._format_url(mqapikey, maptype, lat, lon, hacc)

        try:
            response = get(url, timeout=MAPQTIMEOUT)
            sc = responses[response.status_code]  # get descriptive HTTP status
            response.raise_for_status()  # raise Exception on HTTP error
            if sc == "OK":
                img_data = response.content
                self._img = ImageTk.PhotoImage(Image.open(BytesIO(img_data)))
                self._can_mapview.delete("all")
                self._can_mapview.create_image(0, 0, image=self._img, anchor=NW)
                self._draw_zoom()
                self._can_mapview.update_idletasks()
                return
        except (ConnError, ConnectTimeout):
            msg = NOWEBMAPCONN
        except RequestException:
            msg = NOWEBMAPHTTP.format(sc)

        self._disp_error(msg)

    def _draw_countdown(self, wait):
        """
        Draw clock icon indicating time until next scheduled map refresh.

        :param int wait: wait time in seconds
        """

        self._can_mapview.create_oval((5, 5, 20, 20), fill="#616161", outline="")
        self._can_mapview.create_arc(
            (5, 5, 20, 20), start=90, extent=wait, fill="#ffffff", outline=""
        )

    def _draw_zoom(self):
        """
        Draw +/- zoom icons.
        """

        w, h = self.width, self.height
        fw, fh = self._resize_font_width, self._resize_font_height
        self._can_mapview.create_text(
            w - 2 - fw / 2,
            h - 2 - fh,
            text="+",
            font=self._resize_font,
            fill=ZOOMCOL if self._zoom < MAX_ZOOM else ZOOMEND,
            anchor="s",
        )
        self._can_mapview.create_text(
            w - 2 - fw / 2,
            h - 2 - fh / 1.2,
            text=self._zoom,
            fill=ZOOMCOL,
            font=font.Font(size=8),
            # anchor="e",
        )
        self._can_mapview.create_text(
            w - 2 - fw / 2,
            h - 2,
            text="−",
            font=self._resize_font,
            fill=ZOOMCOL if self._zoom > MIN_ZOOM else ZOOMEND,
            anchor="s",
        )

    def _format_url(
        self, mqapikey: str, maptype: str, lat: float, lon: float, hacc: float
    ):
        """
        Formats URL for web map download.

        :param str mqapikey: MapQuest API key
        :param str maptype: "map" or "sat"
        :param float lat: latitude
        :param float lon: longitude
        :param float hacc: horizontal accuracy
        :return: formatted MapQuest URL
        :rtype: str
        """

        w, h = self.width, self.height
        radius = str(hacc / 1000)  # km
        zoom = self._zoom
        # seems to be bug in MapQuest API which causes error
        # if scalebar displayed at maximum zoom
        scalebar = "true" if zoom < 20 else "false"

        return MAPURL.format(
            mqapikey,
            lat,
            lon,
            MARKERURL,
            zoom,
            w,
            h,
            radius,
            lat,
            lon,
            scalebar,
            maptype,
        )

    def _disp_error(self, msg):
        """
        Display error message in webmap widget.

        :param str msg: error message
        """

        w, h = self.width, self.height
        resize_font = font.Font(size=min(int(w / 20), 14))

        self._can_mapview.delete("all")
        self._can_mapview.create_text(
            w / 2,
            h / 2,
            text=msg,
            fill="orange",
            font=resize_font,
            anchor="s",
        )

    def reset_map_refresh(self):
        """
        Reset map refresh counter to zero
        """

        self._last_map_update = 0

    def _on_resize(self, event):  # pylint: disable=unused-argument
        """
        Resize frame

        :param event event: resize event
        """

        self.width, self.height = self.get_size()
        self._resize_font = font.Font(size=min(int(self.height / 5), 30))
        self._resize_font_height = self._resize_font.metrics("linespace")
        self._resize_font_width = self._resize_font.measure("+")

    def get_size(self):
        """
        Get current canvas size.

        :return: window size (width, height)
        :rtype: tuple
        """

        self.update_idletasks()  # Make sure we know about any resizing
        width = self._can_mapview.winfo_width()
        height = self._can_mapview.winfo_height()
        return (width, height)
