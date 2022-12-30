import argparse
import sys

from bhd_parser.beyondhd_search import BeyondHDAPI


def get_args():
    parser = argparse.ArgumentParser()

    # search args
    parser.add_argument(
        "-a",
        "--api_key",
        help="BeyondHD API Key",
    )

    parser.add_argument(
        "-t",
        "--title",
        help="Movie/Tv Show - e.g. The Matrix 1999",
    )

    parser.add_argument(
        "-g",
        "--filter_group",
        default=None,
        help="Release group in the format of 'BHDStudio', 'FraMeSToR'",
    )

    parser.add_argument(
        "-r",
        "--resolution",
        default=None,
        help="Filter by resolution in the format of '720p', '1080p'",
    )

    parser.add_argument(
        "-x",
        "--time_out",
        default=60,
        help="Time out in seconds, default is 60",
    )

    parser.add_argument(
        "-f",
        "--format",
        default="dict",
        choices=("dict", "list", "string", "string_w_link"),
        help="Format to return results in",
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


def _search_error(x):
    print(x + "\nYou must pass API key with '-a' and title with '-t'")
    input()
    exit()


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

    # handle args
    if not parse_args["api_key"]:
        _search_error("Missing API Key")
    if not parse_args["title"]:
        _search_error("Missing title")

    # start BeyondHDAPI instance
    search_torrent = BeyondHDAPI(api_key=parse_args["api_key"])

    # create args
    search_args = {"title": parse_args["title"]}
    if parse_args["filter_group"]:
        search_args.update({"release_group": parse_args["filter_group"]})

    if parse_args["resolution"]:
        search_args.update({"resolution": parse_args["resolution"]})

    if parse_args["time_out"]:
        search_args.update({"search_timeout": parse_args["time_out"]})

    # search
    search_torrent.search(**search_args)

    # handle output
    if search_torrent.success:
        format_search_args = {"info": search_torrent.get_results()}
        if parse_args["format"]:
            format_search_args.update({"results_format": parse_args["format"]})
        _format_search_results(**format_search_args)
