from flask import Blueprint, request, render_template
from flask_login import login_required, current_user
from models.hotel import Hotel
from models.user import User
package = Blueprint('package', __name__)

@package.route('/products')
@login_required
def viewallpackages():
    # Home page of all authenticated users
    return render_template('viewallpackages.html', hotel_list = Hotel.objects)

from datetime import datetime, timedelta
from models.booking import Booking
@package.route('/view', methods=['GET'])
@login_required
def viewpackage():
    # retrive the hotel name from url query string
    
    hotel_name = request.args.get("hotel")
    selected_hotel = Hotel.objects(hotel_name=hotel_name).first()
    existing_user = User.objects(email=current_user.email).first()
    if selected_hotel is None:
        selected_hotel = Hotel(hotel_name="Invalid Hotel",
                               description="Invalid Hotel",
                               image_url="https://fscene8.me/content/images/size/w1000/2022/04/question-mark-1019820_1280-1-.jpg")
    return render_template('viewpackage.html', 
                            hotel_name=hotel_name, 
                            image_url=selected_hotel.image_url, 
                            description=selected_hotel.description)

from flask import jsonify
@package.route('/addbooking', methods=['POST'])
@login_required
def addbooking():
    data = request.get_json()
    hotel_name = data['hotel_name']

    d,m,y = str(data['checkindate']).split('-')
    checkindate = datetime(year=int(y),month=int(m),day=int(d))
    selected_hotel = Hotel.objects(hotel_name=hotel_name).first()

    if selected_hotel is None:
        return jsonify({'status' : 'ERROR',
                        'message': f'ERROR: Cannot find "{hotel_name}"'})
    elif Booking.objects(hotel_name=selected_hotel.id, customer=current_user.id, check_in_date=checkindate).first() is None:
        Booking(check_in_date=checkindate,customer=current_user.id,hotel_name=selected_hotel.id).save()
        return jsonify({'status' : 'OK',
                        'message': f'Booking at "{hotel_name}" on {checkindate.strftime("%d-%m-%Y")} for {current_user.name} was made.'})
    else:
        return jsonify({'status' : 'ERROR',
                        'message': f'ERROR: You already have an existing booking at "{hotel_name}" on {checkindate.strftime("%d-%m-%Y")}, under the name of {current_user.name}.'})