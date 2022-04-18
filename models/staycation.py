from app import db

class Staycation(db.Document):
    meta = {'collection': 'staycation'}
    hotel_name = db.StringField()
    duration = db.IntField()
    unit_cost = db.IntField()
    image_url = db.URLField()
    description = db.StringField()
    