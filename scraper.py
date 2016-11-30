import re
import requests
import dateutil.parser
import json
from datetime import datetime
from bs4 import BeautifulSoup
from Event import Event


def fetch_page_html(url):
    print("Fetching page HTML from: " + url)
    response = requests.get(url, timeout=8)
    html = BeautifulSoup(response.content, 'html.parser')
    return html


def get_events(html):
    url = "http://events.ucf.edu/this-week/?page="
    event_lists = []
    events = []

    # Get how many pages there are, not including the "next arrow"
    # via pagination at the bottom of the events page via regex.
    links = html.findAll("a", href=re.compile('page'))[:-1]

    # For each individual page of events per week ...
    for index in range(0, len(links)):
        page = fetch_page_html(url + str(index+1))

        print('Fetching events from week page ' + str(index+1) + ' ...')

        event_week = page.find(id="calendar-events-week")
        event_lists += event_week.findAll("ul", class_="event-list")

    # For each event list, get the events.
    for event_list in event_lists:
        events += event_list.findAll("li", class_="event")

    return events


def format_datetime(unformated_datetime):
    day_names = [
        "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday",
        "Friday", "Saturday"
    ]

    month_names = [
        'January', 'February', 'March', 'April', 'May', 'June', 'July',
        'August', 'September', 'October', 'November', 'December'
    ]

    # Clean up formatting.
    formatted_datetime = unformated_datetime.replace('-', ' ')
    formatted_datetime = formatted_datetime.replace('T', ' ')
    formatted_datetime = formatted_datetime.split(' ')[:-1]

    year = formatted_datetime[0]
    month = month_names[int(formatted_datetime[1]) - 1]
    day = formatted_datetime[2]
    time = formatted_datetime[3].replace(':', '').replace('.999999', '')[:-2]

    date_string = day + month + year + ' ' + time

    # Convert to datetime object.
    date_obj = datetime.strptime(date_string, '%d%B%Y %H%M')

    # Use datetime obj to get the weekday according to date.
    weekday = day_names[date_obj.weekday()]

    return [weekday, month, day, year, time]


def init_event_objects(events):
    print('Creating event objects ...')

    event_objects = []

    for event in events:
        # Retrieve properties that make up an event.
        title = event.h3.a.text
        start_time = event.find('time', class_='dtstart')['datetime']
        end_time = event.find('time', class_='dtend')['datetime']
        location = event.find('span', class_='location').text
        description = event.p.text
        url = 'http://events.ucf.edu' + event.a['href']

        # Create an event object with the event properties.
        event_objects.append(
            Event(
                title,
                format_datetime(start_time),
                format_datetime(end_time),
                location,
                description,
                url
            )
         )

    return event_objects


if __name__ == "__main__":

    events_url = "http://events.ucf.edu/this-week/"
    html = fetch_page_html(events_url)

    events = get_events(html)
    event_objects = init_event_objects(events)

    # Convert list of objs to dicts and dump to JSON.
    event_json = json.dumps(
        [obj.__dict__ for obj in event_objects],
        indent=4,
        sort_keys=False,
    )

    print(event_json)
