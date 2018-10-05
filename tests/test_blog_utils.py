from blog_utils.md_parser import convert_to_html


def test_h1():
    assert convert_to_html("# Title level one") == "<h1> Title level one</h1>"
