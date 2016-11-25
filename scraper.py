from bs4 import BeautifulSoup
from models import Day, Event
import re
import requests

def get_page_html(url):
    print("Fetching page HTML ...")
    response = requests.get(url)
    html = BeautifulSoup(response.content, 'html.parser')
    return html

def get_event_lists(html):
    url = "http://events.ucf.edu/this-week/?page="
    day_list = []

    # Get how many pages there are, not including the "next arrow"
    # via pagination at the bottom of the events page.
    links = html.findAll("a", href=re.compile('page'))[:-1]

    # Start after getting events from the 1st page.
    for index in range(0, len(links)):
        page = get_page_html(url + str(index))

        # Do this by span day-heading instead to avoid duplicate days.
        # Each list will be the next sibling of a span day-heading.
        day_event_lists = page.findAll("ul", class_="event-list")

        for event_list in day_event_lists:
            day_list.append(event_list)

    for i, dl in enumerate(day_list):
        print(i)

    
    
# Initialize an array that holds Day objects
def create_day_list(self):
    names = ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]
    day_list = []

    for i in range(7):
        day = Day(names[i], [])
        day_list.append(day)

    return day_list

if __name__ == "__main__":
    
    events_url = "http://events.ucf.edu/this-week/"
    html = get_page_html(events_url)

    get_event_lists(html)