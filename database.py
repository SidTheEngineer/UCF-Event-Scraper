import json
from pymongo import MongoClient


# Config file where db info is contained. Open the
# file and conver the JSON to a Python object.
config = json.loads(open('config.json').read())

client = MongoClient(config['mlabUrl'])
db = client['campus-events']
events = db.events


def save_event(event):
    pass

test_event = {
    "title": "test title",
    "start": "test start time",
    "end": "test end time",
    "location": "test location",
    "description": "test description",
    "url": "test url"
}

event_id = events.insert_one(test_event).inserted_id
print(event_id)
