"""
rtcm3_handler.py

RTCM Protocol handler - handles all incoming RTCM messages.

Parses individual RTCM3 sentences (using pyrtcm library).

Created on 10 Apr 2022

:author: semuadmin
:copyright: 2020 SEMU Consulting
:license: BSD 3-Clause
"""

import logging


class RTCM3Handler:
    """
    RTCM3 handler class.
    """

    def __init__(self, app):
        """
        Constructor.

        :param Frame app: reference to main tkinter application
        """

        self.__app = app  # Reference to main application class
        self.__master = self.__app.appmaster  # Reference to root class (Tk)
        self.logger = logging.getLogger(__name__)

        self._raw_data = None
        self._parsed_data = None

    def process_data(self, raw_data: bytes, parsed_data: object):
        """
        Process relevant RTCM message types

        :param bytes raw_data: raw_data
        :param RTCMMessage parsed_data: parsed data
        """
        # pylint: disable=no-member

        try:
            if raw_data is None:
                return

            # if parsed_data.identity == "1005":
            #     self._process_1005(parsed_data)
            # etc...

        except ValueError:
            # self.__app.set_status(RTCMVALERROR.format(err), "red")
            pass
