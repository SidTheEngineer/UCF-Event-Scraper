from bs4 import BeautifulSoup
from models import Day, Event
from datetime import datetime
import re
import requests
import dateutil.parser

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

def format_datetime(unformated_datetime):
    day_names = ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]
    month_names = [
        'January',
        'February',
        'March',
        'April',
        'May',
        'June',
        'July',
        'August',
        'September',
        'October',
        'November',
        'December'
    ]

    formatted_datetime = unformated_datetime.replace('-', ' ').replace('T', ' ').split(' ')[:-1]

    year = formatted_datetime[0]
    month = month_names[int(formatted_datetime[1]) - 1]
    day = formatted_datetime[2]
    time = formatted_datetime[3]

    date_string = day + month + year + ' ' + time
    print(datetime.strptime(date_string, '%d%B%Y %H:%M:%S'))
    print(datetime.strptime(date_string, '%d%B%Y %H:%M:%S').weekday())

if __name__ == "__main__":

    events_url = "http://events.ucf.edu/this-week/"
    html = get_page_html(events_url)

    events = get_events(html)
    for event in events:
        start_time = event.find('time', class_='dtstart')['datetime']
        end_time = event.find('time', class_='dtend')['datetime']

        # Convert from ISO style format to an easier to deal with format.
        # Done explicitly because dateutil parser threw uknown type error.
        #start_time = start_time.replace('-', ' ').replace('T', ' ').split(' ')[:-1]
        #end_time = end_time.replace('-', ' ').replace('T', ' ').split(' ')[:-1]

        format_datetime(start_time)
