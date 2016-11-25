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