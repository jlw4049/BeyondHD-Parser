import re
from html import unescape

import browser_cookie3
import bs4
import requests

from bhdstudio_nfo_parse import parse_bhdstudio_nfo


class BeyondHDCookieError(Exception):
    pass


class BeyondHDScrape:
    def __init__(
        self,
        url: str,
        cookie_key: str = None,
        cookie_value: str = None,
        auto_cookie_detection: bool = True,
        timeout: int = 60,
    ):
        """
        Used to scrape BeyondHD for torrent information

        :param url: URL to torrent.
        :param cookie_key: Beyond-hd.me cookie key (starts with remember_).
        :param cookie_value: Beyond-hd.me cookie value (value after remember_... key).
        :param auto_cookie_detection: Will utilize browser_cookie3 to automatically detect beyond-hd cookies from
        chrome, chromium, opera, brave, edge, vivaldi, firefox and safari browsers. If the user leaves this equal to
        True, but also provides a cookie_key/value then we will not attempt to automatically load the cookies.
        :param timeout: Set requests timeout, default is 60 seconds.
        """

        # variables
        self.url = url
        self.cookie_key = cookie_key
        self.cookie_value = cookie_value
        self.auto_cookie_detection = auto_cookie_detection
        self.cookie_jar = None
        self.timeout = timeout
        self.bhd_session = None
        self.media_info = None
        self.nfo = None

        # get cookies ready
        self._handle_cookies()
        if self.cookie_jar:
            self._start_session()
        else:
            raise BeyondHDCookieError(
                "Missing cookies, login into BeyondHD with any supported browsers or "
                "provide cookie_key/value"
            )

    def _handle_cookies(self):
        """
        This handles our cookie input.
        If auto_cookie_detection=True then we will attempt to automatically load cookies.
        If the user defines cookie_key AND cookie_value then we will ignore auto_cookie_detection=True.
        Then we will update self.cookie_jar variable with which ever cookies.
        """
        if not self.auto_cookie_detection:
            if not self.cookie_key or not self.cookie_value:
                raise BeyondHDCookieError(
                    "You must provide the cookie value and key or re-enable"
                    "'auto_cookie_detection=True'"
                )
            else:
                self.cookie_jar = {self.cookie_key: self.cookie_value}

        elif self.auto_cookie_detection:
            if self.cookie_key and self.cookie_value:
                self.cookie_jar = {self.cookie_key: self.cookie_value}
            else:
                self.cookie_jar = browser_cookie3.load(domain_name="beyond-hd")

    def _start_session(self):
        """Utilizes requests to parse the input url while converting the output with BeautifulSoup"""
        session = requests.session()
        try:
            session_results = session.get(
                url=self.url,
                cookies=self.cookie_jar,
                timeout=self.timeout,
            )
            self.bhd_session = bs4.BeautifulSoup(session_results.text, "html.parser")
        except requests.exceptions.ConnectionError:
            raise ConnectionError(
                "There was a connection error when attempting to connect to beyond-hd"
            )

    def parse_media_info(self):
        """Parses URL for MediaInfo"""
        get_mediainfo = re.search(
            r"(?s)<code>General(.+)</code></pre>", str(self.bhd_session), re.MULTILINE
        )
        if get_mediainfo:
            self.media_info = unescape(get_mediainfo.group(1).lstrip().rstrip())
        else:
            return None

    def parse_nfo(self, bhdstudio: bool = False, text_only: bool = False):
        """
        Parse NFO

        :param bhdstudio: If set to True and bhdstudio is in URL, return a dictionary for BHDStudio.
        :param text_only: If set to True, then only return all the text from the NFO.
        """
        get_nfo = re.search(r"(?s)forced-nfo(.+?)</tbody>", str(self.bhd_session))
        if get_nfo:
            if bhdstudio and "bhdstudio" in str(self.url).lower():
                self.nfo = {"bhdstudio_nfo_parsed": parse_bhdstudio_nfo(get_nfo)}
            else:
                if text_only:
                    self.nfo = bs4.BeautifulSoup(
                        get_nfo.group(1).replace("<br/>", "\n"), "html.parser"
                    ).text
                else:
                    self.nfo = unescape(get_nfo.group(1).replace("<br/>", "\n"))
        else:
            self.nfo = None


if __name__ == "__main__":
    test = BeyondHDScrape(
        url="https://beyond-hd.me/torrents/metropolis-2001-proper-bluray-1080p-dts-hd-ma-51-avc-remux-framestor.232582"
    )
    test.parse_media_info()
    test.parse_nfo(bhdstudio=True, text_only=True)
    print(test.nfo)
    # print(test.media_info)
