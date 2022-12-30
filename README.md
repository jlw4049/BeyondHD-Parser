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

## Example of how scrape BeyondHD

```python
from beyondhd_parser.parsers.beyondhd_details import BeyondHDScrape

scrape_bhd = BeyondHDScrape(
    url="URL"
)
scrape_bhd.parse_media_info()
scrape_bhd.parse_nfo()
print(scrape_bhd.nfo)
print(scrape_bhd.media_info)

```

