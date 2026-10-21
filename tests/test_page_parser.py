from page_analyzer.page_parser import MAX_FIELD_LENGTH, parse_page

FULL_PAGE = """
<html>
  <head>
    <title> Awesome page </title>
    <meta name="description" content="Statements of great people">
  </head>
  <body><h1>Do not expect a miracle</h1></body>
</html>
"""


def test_parse_page_extracts_seo_tags():
    assert parse_page(FULL_PAGE) == {
        "h1": "Do not expect a miracle",
        "title": "Awesome page",
        "description": "Statements of great people",
    }


def test_parse_page_without_tags_gives_empty_values():
    assert parse_page("<html><body><p>text</p></body></html>") == {
        "h1": "",
        "title": "",
        "description": "",
    }


def test_parse_page_cuts_long_values():
    long_text = "a" * (MAX_FIELD_LENGTH + 50)
    page = f"<title>{long_text}</title><h1>{long_text}</h1>"

    seo = parse_page(page)

    assert len(seo["title"]) == MAX_FIELD_LENGTH
    assert len(seo["h1"]) == MAX_FIELD_LENGTH
