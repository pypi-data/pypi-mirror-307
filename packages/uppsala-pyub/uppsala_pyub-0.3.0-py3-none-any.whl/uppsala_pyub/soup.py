from bs4 import BeautifulSoup as bs
from requests_html import HTMLSession




def make_soup(url):
    """
    Makes a bs4 soup object from the url

    Args:
        url:
    """
    s = HTMLSession()
    r = s.get(url)
    r.html.render()
    r = r.html
    return bs(r.__dict__.get('_html'), 'html.parser')
