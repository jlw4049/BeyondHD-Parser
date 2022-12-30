# BeyondHD-Parser

This package includes a way to utilize BeyondHD's search API as well as parse URL's for MediaInfo/NFO

## Install

`pip install BeyondHD-Parser`

## Uninstall

`pip uninstall BeyondHD-Parser`

## Example of how to use search API

```python
from beyondhd_parser.parsers.beyondhd_search import BeyondHDAPI, BhdApiError, ApiKeyError

# basic ##########################
search_beyondhd = BeyondHDAPI(api_key="NEED KEY")
search_beyondhd.search(title="Gone In 60 Seconds")

if search_beyondhd.success:
    print("Do something with results:\n" + str(search_beyondhd.get_results()))
elif not search_beyondhd.success:
    print("No results")

    
# full work flow with error handling ##################
try:
    search_beyondhd = BeyondHDAPI(api_key="NEED KEY")
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
```

## BeyondHDApi's .search() parameters
BeyondHDApi() only accepts URL, the .search() method is where all the magic happens

`title` Required, title to search for in the format of *The Matrix 1999*

`release_group` Optional, specify groups *BHDStudio, FraMeSToR, SacReD*

`page` Optional, allows you to select which page *int e.g. 0, 1, 2*

`resolution` Optional, can filter resolutions *720p, 1080p, etc*

`search_timeout` You can adjust the timeout time, default is 60 (seconds)

## Example of how scrape BeyondHD

```python
from beyondhd_parser.beyondhd_details import BeyondHDScrape

scrape_bhd = BeyondHDScrape(
    url="URL"
)
scrape_bhd.parse_media_info()
scrape_bhd.parse_nfo()
print(scrape_bhd.nfo)
print(scrape_bhd.media_info)

```
## BeyondHDScrape() parameters
`url` Required, url to the torrent to parse

`cookie_key` Optional, but if you do not provide the key/value you must have logged in prior in a supported browser

`cookie_value` Optional, but if you do not provide the key/value you must have logged in prior in a supported browser

`auto_cookie_detection` Default is True, manual cookie input does override this. If you've logged into BeyondHD in any of the supported browsers, this will automatically inject your cookie.\
*chrome, chromium, opera, brave, edge, vivaldi, firefox and safari*

`timeout` You can adjust the timeout time, default is 60 (seconds)

## BeyondHDScrape's .parse_nfo() parameters
`bhdstudio` True or False, default is False. You can parse BHDStudio NFO's into a python dictionary

`text_only` True or False, default is False. You can strip away anything that isn't text in the NFO output
