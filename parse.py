from bs4 import BeautifulSoup
import re

def get_event_properties(html):
    links = html.findAll("a", href=re.compile('page'))
    
