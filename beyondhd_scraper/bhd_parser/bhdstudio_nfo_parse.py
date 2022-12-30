import re
from html import unescape


def parse_bhdstudio_nfo(get_nfo: re):
    """
    Parse NFO details to a dictionary.

    :param get_nfo: Regex of BeyondHD specific NFO from site.
    :return: Dictionary all the parsed information.
    """
    # empty dictionary
    bhdstudio_dict = {}

    # convert line breaks to newlines
    parse_nfo = unescape(str(get_nfo.group(1)).replace("<br/>", "\n"))

    # get source
    get_source = re.search(r"Source\s+:\s(.+)\n", parse_nfo)
    if get_source:
        bhdstudio_dict.update(
            {"source": get_source.group(1).replace("(Thanks!)", "").rstrip()}
        )

    # get chapters
    get_chapters = re.search(r"Chapters\s+:\s(.+)\n", parse_nfo)
    if get_chapters:
        bhdstudio_dict.update({"chapters": get_chapters.group(1).rstrip()})

    # get file size
    get_file_size = re.search(r"File\sSize\s+:\s(.+)\n", parse_nfo)
    if get_file_size:
        bhdstudio_dict.update({"file_size": get_file_size.group(1).rstrip()})

    # get duration
    get_duration = re.search(r"Duration\s+:\s(.+)\n", parse_nfo)
    if get_duration:
        bhdstudio_dict.update({"duration": get_duration.group(1).rstrip()})

    # get video
    get_video_info = re.search(r"Video\s+:\s(.+)\n", parse_nfo)
    if get_video_info:
        bhdstudio_dict.update({"video_info": get_video_info.group(1).rstrip()})

    # get resolution
    get_resolution = re.search(r"Resolution\s+:\s(.+)\n", parse_nfo)
    if get_resolution:
        bhdstudio_dict.update({"resolution": get_resolution.group(1).rstrip()})

    # get audio
    get_audio = re.search(r"Audio\s+:\s(.+)\n", parse_nfo)
    if get_audio:
        bhdstudio_dict.update({"audio_info": get_audio.group(1).rstrip()})

    # get encoded_by
    get_encoded_by = re.search(r'Encoder\s+:\s.+">(.+)</.+\n', parse_nfo)
    if get_encoded_by:
        bhdstudio_dict.update({"encoder": get_encoded_by.group(1).rstrip()})

    # get release notes
    release_notes = re.search(
        r'(?s)RELEASE NOTES</span>\n\n(.+)\n\n<span style="color: #f5c70a">SCREENSHOTS',
        parse_nfo,
        re.MULTILINE,
    )
    if release_notes:
        bhdstudio_dict.update({"release_notes": release_notes.group(1).rstrip()})

    # get only the image section
    image_section = re.search(
        r"(?s)ENCODE.*\[/color](.*)\[/center].*GREETZ", parse_nfo, flags=re.MULTILINE
    )

    # if images are detected
    if image_section:

        # find full resolution images and update the dictionary
        full_res_images = re.findall(
            r"url=(http.+?)]\[img]", str(image_section.group(1)), flags=re.MULTILINE
        )
        if full_res_images:
            bhdstudio_dict.update(
                {
                    "full_resolution_images": [
                        x for x in full_res_images if "md" not in x
                    ],
                }
            )

        # find medium linked images and update the dictionary
        medium_linked_images = re.findall(
            r"\[img](http.+?)\[/img]\[/url]",
            str(image_section.group(1)),
            flags=re.MULTILINE,
        )
        if medium_linked_images:
            bhdstudio_dict.update(
                {"medium_linked_images": [x for x in medium_linked_images if "md" in x]}
            )

    return bhdstudio_dict
