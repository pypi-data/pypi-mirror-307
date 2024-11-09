import unittest
from scrapper_boilerplate import load_dynamic_page


def test_load_dynamic_page():
    code = load_dynamic_page("https://github.com/mx-jeff/scrapper-boilerplate")
    assert code

def test_load_dynamic_page_with_scroll():
    code = load_dynamic_page("https://github.com/mx-jeff/scrapper-boilerplate", scroll=True)
    assert code

def test_load_dynamic_page_with_no_headless():
    code = load_dynamic_page("https://github.com/mx-jeff/scrapper-boilerplate", headless=False)
    assert code

def test_load_dynamic_page_with_no_headless_and_scroll_enabled():
    code = load_dynamic_page("https://github.com/mx-jeff/scrapper-boilerplate", headless=False, scroll=True)
    assert code
