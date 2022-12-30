import argparse
import sys

from bhd_parser.beyondhd_details import BeyondHDScrape


def get_args():
    parser = argparse.ArgumentParser()

    # search args
    parser.add_argument("-u", "--url", help="BeyondHD URL", required=True)

    parser.add_argument(
        "-k",
        "--cookie_key",
        default=None,
        help="Cookie value",
    )

    parser.add_argument(
        "-v",
        "--cookie_value",
        default=None,
        help="Cookie value",
    )

    parser.add_argument(
        "-a",
        "--auto_cookie_detection",
        default=True,
        choices=(True, False),
        help="Automatic cookie detection, you must login to BeyondHD first in "
        "chrome, chromium, opera, brave, edge, vivaldi, firefox or safari",
    )

    parser.add_argument(
        "-f",
        "--format",
        default="both",
        choices=("nfo", "media_info", "both"),
        help="Format to return results in",
    )

    parser.add_argument(
        "-t",
        "--text_only",
        default="n",
        choices=("y", "n"),
        help="Return results in text only mode",
    )

    parser.add_argument(
        "-x",
        "--time_out",
        default=60,
        help="Time out in seconds, default is 60",
    )

    # parse args
    return vars(parser.parse_args())


def _format_search_results(info, results_format: str = "dict"):
    if results_format == "dict":
        print(info)
    elif results_format == "list":
        new_list = []
        for x in list(info.keys()):
            new_list.append((x, info[x]["url"]))
        print(new_list)
    elif results_format == "string":
        for x in list(info.keys()):
            print(x)
    elif results_format == "string_w_link":
        first_new_line = ""
        for x in list(info.keys()):
            print(first_new_line + str(x) + "\nlink: " + str(info[x]["url"]))
            first_new_line = "\n"


if __name__ == "__main__":
    # keep prompt over if double-clicked or script is utilized with no args
    try:
        sys.argv[1]
    except IndexError:
        print("This is a command line program. Run this from a terminal.")
        print("You can use '-h' to get parameter arguments")
        input()
        exit()

    # parse arguments
    parse_args = get_args()

    search_args = {"url": parse_args["url"]}

    if parse_args["cookie_key"]:
        search_args.update({"cookie_key": parse_args["cookie_key"]})

    if parse_args["cookie_value"]:
        search_args.update({"cookie_value": parse_args["cookie_value"]})

    if parse_args["auto_cookie_detection"]:
        search_args.update(
            {"auto_cookie_detection": parse_args["auto_cookie_detection"]}
        )

    if parse_args["time_out"]:
        search_args.update({"timeout": parse_args["time_out"]})

    search_torrent = BeyondHDScrape(**search_args)
    search_torrent.parse_media_info()

    if parse_args["text_only"] == "y":
        search_torrent.parse_nfo(text_only=True)
    else:
        search_torrent.parse_nfo(text_only=False)

    if parse_args["format"] == "both":
        print(search_torrent.media_info + "\n\n" + search_torrent.nfo)
    elif parse_args["format"] == "nfo":
        print(search_torrent.nfo)
    elif parse_args["format"] == "media_info":
        print(search_torrent.media_info)
