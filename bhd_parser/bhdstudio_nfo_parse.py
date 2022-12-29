import re


def parse_bhdstudio_nfo(get_nfo: re):
    """
    Parse NFO details to a dictionary.

    :param get_nfo: Regex of BeyondHD specific NFO from site.
    :return: Dictionary all the parsed information.
    """
    # empty dictionary
    bhdstudio_dict = {}

    # convert line breaks to newlines
    parse_nfo = str(get_nfo.group(1)).replace("<br/>", "\n").replace("\r", "")

    # get source
    get_source = re.search(r"Source\s+:\s(.+)\n", parse_nfo)
    if get_source:
        bhdstudio_dict.update(
            {"source": get_source.group(1).replace("(Thanks!)", "").rstrip()}
        )

    # get chapters
    get_chapters = re.search(r"Chapters\s+:\s(.+)\n", parse_nfo)
    if get_chapters:
        bhdstudio_dict.update({"chapters": get_chapters.group(1)})

    # get file size
    get_file_size = re.search(r"File\sSize\s+:\s(.+)\n", parse_nfo)
    if get_file_size:
        bhdstudio_dict.update({"file_size": get_file_size.group(1)})

    # get duration
    get_duration = re.search(r"Duration\s+:\s(.+)\n", parse_nfo)
    if get_duration:
        bhdstudio_dict.update({"duration": get_duration.group(1)})

    # get video
    get_video_info = re.search(r"Video\s+:\s(.+)\n", parse_nfo)
    if get_video_info:
        bhdstudio_dict.update({"video_info": get_video_info.group(1)})

    # get resolution
    get_resolution = re.search(r"Resolution\s+:\s(.+)\n", parse_nfo)
    if get_resolution:
        bhdstudio_dict.update({"resolution": get_resolution.group(1)})

    # get audio
    get_audio = re.search(r"Audio\s+:\s(.+)\n", parse_nfo)
    if get_audio:
        bhdstudio_dict.update({"audio_info": get_audio.group(1)})

    # get encoded_by
    get_encoded_by = re.search(r'Encoder\s+:\s.+">(.+)</.+\n', parse_nfo)
    if get_encoded_by:
        bhdstudio_dict.update({"encoder": get_encoded_by.group(1)})

    # get release notes
    release_notes = re.search(
        r'(?s)RELEASE NOTES</span>\n\n(.+)\n\n<span style="color: #f5c70a">SCREENSHOTS',
        parse_nfo,
        re.MULTILINE,
    )
    if release_notes:
        bhdstudio_dict.update({"release_notes": release_notes.group(1)})

    # get all images
    images = re.findall(r'="(http.+?)"', parse_nfo)
    if images:
        bhdstudio_dict.update(
            {
                "medium_linked_images": [x for x in images if "md" in x],
                "full_resolution_images": [x for x in images if "md" not in x],
            }
        )

    return bhdstudio_dict
