import requests


class ApiKeyError(Exception):
    """Custom exception for ApiKeyError"""

    pass


class BhdApiError(Exception):
    """All generic BHD errors"""

    pass


class BeyondHDAPI:
    def __init__(self, api_key: str):
        """
        Search BeyondHD for torrents and return 100 results at a time.

        :param api_key: API key from BeyondHD.
        """

        # variables
        self.api_key = api_key
        self.title = None
        self.release_group = None
        self.page = None
        self.resolution = None
        self.search_timeout = None
        self.run_check = None
        self.payload = None
        self.success = None

    def search(
        self,
        title: str,
        release_group: str = None,
        page: int = 0,
        resolution: str = None,
        search_timeout: int = 60,
    ):
        """
        Searches BeyondHD via the search API

        :param title: Title of the movie to check.
        :param release_group: Release group in the format of BHDStudio, FraMeSToR, SacReD, is case sensitive.
        :param page: This returns 100 results by default, if for some reason there is more send a page number.
        :param resolution: Filters results by resolution, 720p... If left as None then it will return all results.
        :param search_timeout: Default is 60, can adjust this in seconds
        """

        # update variables
        self.title = title
        self.release_group = release_group
        self.page = page
        self.resolution = resolution
        self.search_timeout = search_timeout

        # base payload
        self.payload = {
            "action": "search",
            "search": title,
        }

        # if a page is specified add it to the payload
        if self.page >= 1:
            self.payload.update({"page": int(page)})

        # if a group is specified add it to the payload
        if self.release_group:
            self.payload.update({"groups": self.release_group})

        try:
            self.run_check = requests.post(
                "https://beyond-hd.me/api/torrents/" + self.api_key,
                params=self.payload,
                timeout=self.search_timeout,
            )

            # if post returns a False when connecting
            if not self.run_check.ok:
                raise ApiKeyError(
                    "BeyondHD connection failed, likely due to API key error"
                )

            # if post returns True when connecting
            elif self.run_check.ok:
                # if post is successful get the torrents
                if self.run_check.json()["success"]:
                    self.success = True

                # if post is not successful
                else:
                    # if site returns invalid api key
                    if (
                        "invalid api key:"
                        in str(self.run_check.json()["status_message"]).lower()
                    ):
                        raise ApiKeyError("Invalid API Key")
                    # for all other errors directly post the status message from the site
                    else:
                        raise ApiKeyError(str(self.run_check.json()["status_message"]))

        # if there is some sort of connection error
        except requests.exceptions.ConnectionError:
            raise ConnectionError(
                "There was a connection error when attempting to connect to beyond-hd"
            )

    def get_results(self):
        """
        Used to get the results of the search

        :return: List with a dictionary in it of the first 100 results.
        """
        # release dict
        release_dict = {}

        # if all 3 checks are successful, return all results in a list.
        if (
            self.run_check.ok
            and self.run_check.json()["status_code"]
            and self.run_check.json()["success"]
        ):
            for x in self.run_check.json()["results"]:
                if self.resolution:
                    if self.resolution in str(x):
                        release_dict.update({x["name"]: x})
                elif not self.resolution:
                    release_dict.update({x["name"]: x})

        return release_dict


if __name__ == "__main__":
    import keys
    try:
        search_beyondhd = BeyondHDAPI(api_key=keys.api_key)
        search_beyondhd.search(title="Gone In 60 Seconds")

        if search_beyondhd.success:
            print("Do something with results:\n" + str(search_beyondhd.get_results()))
        elif not search_beyondhd.success:
            print("No results")

    except ConnectionError:
        print("Connection Error!")

    except ApiKeyError:
        print("Invalid API Key")

    except BhdApiError as bhd_error:
        print(str(bhd_error))
