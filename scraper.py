from bs4 import BeautifulSoup
from models import Day, Event
import re
import requests

def get_page_html(url):
    print("Fetching page HTML from: " + url)
    response = requests.get(url)
    html = BeautifulSoup(response.content, 'html.parser')
    return html

def get_events(html):
    url = "http://events.ucf.edu/this-week/?page="
    event_lists = []
    events = []

    # Get how many pages there are, not including the "next arrow"
    # via pagination at the bottom of the events page.
    links = html.findAll("a", href=re.compile('page'))[:-1]

    # For each individual page of events per week ...
    for index in range(0, len(links)):
        page = get_page_html(url + str(index+1))
        event_week = page.find(id="calendar-events-week")
        event_lists += event_week.findAll("ul", class_="event-list")

    # For each event list, get the events.
    for event_list in event_lists:
        events += event_list.findAll("li", class_="event")
    
    return events

        

# Initialize an array that holds Day objects
def create_day_list(self):
    day_names = ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]
    day_list = []

    for i in range(7):
        day = Day(names[i], [])
        day_list.append(day)

    return day_list

if __name__ == "__main__":
    
    events_url = "http://events.ucf.edu/this-week/"
    html = get_page_html(events_url)

    events = get_events(html)
    print(events)