
"""
Disclaimer:
I know I could just use one of the many MD parsers available. But I wanted to write my own, just for the sake of
creating something on my own.
"""


def convert_to_html(markdown_text):
    """
    
    :param markdown_text:
    :return:
    """
    return "\n".join([_parse_line(line) for line in markdown_text.split('\n')])


def _parse_line(line):
    # Headers
    if line[:6] == "######":
        return "<h6>{}</h6>".format(line[6:])
    elif line[:5] == "#####":
        return "<h5>{}</h5>".format(line[5:])
    elif line[:4] == "####":
        return "<h4>{}</h4>".format(line[4:])
    elif line[:3] == "###":
        return "<h3>{}</h3>".format(line[3:])
    elif line[:2] == "##":
        return "<h2>{}</h2>".format(line[2:])
    elif line[:1] == "#":
        return "<h1>{}</h1>".format(line[1:])
    else:
        return line
