from bs4 import BeautifulSoup
import re

def get_event_properties(html):
    link = html.findAll("a", href=re.compile('page'))
    print(link[:-1])
