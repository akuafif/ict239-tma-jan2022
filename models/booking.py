from app import db
from models.user import User
from models.hotel import Hotel

class Booking(db.Document):
    meta = {'collection': 'booking'}
    check_in_date = db.DateTimeField()
    customer = db.ReferenceField(User)
    hotel_name = db.ReferenceField(Hotel)