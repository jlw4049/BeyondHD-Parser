import requests
import bs4
import re
from typing import TextIO
from bhdstudio_nfo_parse import parse_bhdstudio_nfo


class BeyondHDCookieError(Exception):
    pass


class BeyondHDScrape:
    def __init__(self,
                 url: str,
                 cookie_key: str = None,
                 cookie_value: str = None,
                 timeout: int = 60):

        self.url = url
        self.cookie_key = cookie_key
        self.cookie_value = cookie_value
        self.timeout = timeout
        self.bhd_session = None

        self.media_info = None
        self.nfo = None

        if not self.cookie_key or not self.cookie_value:
            raise BeyondHDCookieError("You must provide the cookie value and key")
        else:
            self._start_session()

    def _start_session(self):
        session = requests.session()
        session_results = session.get(url=self.url,
                                           cookies={self.cookie_key: self.cookie_value},
                                           timeout=self.timeout)
        self.bhd_session = bs4.BeautifulSoup(session_results.text, "html.parser")

    def parse_media_info(self):
        get_mediainfo = re.search(r"(?s)<code>General(.+)</code></pre>", str(self.bhd_session), re.MULTILINE)
        if get_mediainfo:
            self.media_info = get_mediainfo.group(1)
        else:
            return None

    def parse_nfo(self,
                  bhdstudio: bool = False):
        # print(self.bhd_session)
        get_nfo = re.search(r'(?s)id="nfo".*>(.+)</textarea>', str(self.bhd_session), re.MULTILINE)
        # print(get_nfo.group(1))
        if get_nfo:
            if bhdstudio:
                self.nfo = {"bhdstudio_nfo_parsed": parse_bhdstudio_nfo(get_nfo)}
            else:
                self.nfo = get_nfo.group(1)
        else:
            self.nfo = None


if __name__ == '__main__':
    import keys
    test = BeyondHDScrape(
        url="https://beyond-hd.me/torrents/stan-ollie-2018-bluray-1080p-dd51-x264-bhdstudio.232368",
        cookie_key=keys.cookie_key,
        cookie_value=keys.cookie_value)
    test.parse_media_info()
    test.parse_nfo(bhdstudio=True)
    print(test.nfo)
