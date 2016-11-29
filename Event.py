class Event(object):
    def __init__(self, title, start, end, location, description, url):
        self.title = title
        self.start = start
        self.end = end
        self.location = location
        self.description = description
        self.url = url

    def __str__(self):
        return self.title + ' ' + str(self.start)
