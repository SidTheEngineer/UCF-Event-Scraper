from bs4 import BeautifulSoup
import requests

class Page(object):
    def __init__(self, url):
        self.url = url
        self.html = self.getPageHtml()
    
    # Get the 'soup' object of the page via BS4.
    def getPageHtml(self):
        response = requests.get(self.url)
        html = BeautifulSoup(response.content, 'html.parser')
        return html

    def printTitles(self, html):
        pass
        
class Day(object):
    def __init__(self, name, events):
        self.name = name
        self.events = events

class Event(object):
    def __init__(self, title, time, location, description):
        self.title = title
        self.time = time
        self.location = location
        self.description = description

# Main function.
if __name__ == "__main__":
    
    events_url = "http://events.ucf.edu/this-week/"
    events_page = Page(events_url)

    print(events_page.html.prettify())

    #for event in html.findAll("li", class_="event"):
        
        # Get the title 
        #print(event.a.contents[0].string)