from app import db

class Hotel(db.Document):
    meta = {'collection': 'hotel'}
    hotel_name = db.StringField()
    duration = db.IntField()
    unit_cost = db.IntField()
    image_url = db.URLField()
    description = db.StringField()
    