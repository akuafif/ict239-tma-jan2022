from flask import Blueprint, request, render_template, jsonify
from flask_login import login_required, current_user
from datetime import datetime, timedelta
from models.staycation import Staycation
from models.user import User
import csv

package = Blueprint('package', __name__)

# for question 1 c (ii)
def load_staycation_csv(): 
    with open('assets/js/staycation.csv', mode ='r')as file:
        tDict = {}
        csvFile = csv.reader(file)
        next(csvFile) # skip header
        for lines in csvFile:
            # hotel_name,duration,unit_cost,image_url,description
            tDict[lines[0]] = {'hotel_name': lines[0],
                                'duration': lines[1],
                                'unit_cost': lines[2],
                                'image_url': lines[3],
                                'description' : lines[4]} 
    return tDict

def load_booking_csv():
    with open('assets/booking.csv', mode ='r')as file:
        tList = []
        csvFile = csv.reader(file)
        next(csvFile) # skip header
        for lines in csvFile:
            # check_in_date,customer,hotel_name
            if lines[1] == current_user.email:
                tList.append([lines[0], lines[1], lines[2]])
    return tList

def save_booking_csv(data):
    with open('assets/booking.csv', 'a+', newline='') as file:
        spamwriter = csv.writer(file)
        spamwriter.writerow(data)

@package.route('/products')
@login_required
def viewallpackages():
    # Home page of all authenticated users
    # To load assets/js/staycation.js as required from q1c (ii)
    hotel_list = []
    for k,v in load_staycation_csv().items():
        hotel_list.append(Staycation(hotel_name=v.get('hotel_name'),
                                duration=v.get('duration'),
                                unit_cost=v.get('unit_cost'),
                                image_url=v.get('image_url'),
                                description=v.get('description')))
    return render_template('viewallpackages.html', 
                            hotel_list=hotel_list)

@package.route('/view', methods=['GET'])
@login_required
def viewpackage():
    # retrive the hotel name from url query string
    hotel_name = request.args.get("hotel")
    selected_hotel = load_staycation_csv().get(hotel_name, None)

    if selected_hotel is None:
        return render_template('booking.html',
                            hotel_name="Invalid Hotel",
                            description="Invalid Hotel",
                            image_url="https://fscene8.me/content/images/size/w1000/2022/04/question-mark-1019820_1280-1-.jpg")
    return render_template('booking.html', 
                            hotel_name=selected_hotel.get('hotel_name'),
                            description=selected_hotel.get('description'),
                            image_url=selected_hotel.get('image_url'))

@package.route('/addbooking', methods=['POST'])
@login_required
def addbooking():
    # Q1 uses csv file to store the booking
    data = request.get_json()
    hotel_name = data['hotel_name']
    
    # date format to followng the csv format from tma asset
    d,m,y = str(data['checkindate']).split('-')
    csv_date_format = f'{y}-{m}-{d}'
    new_book = [csv_date_format, current_user.email, str(hotel_name)]
    
    if new_book in load_booking_csv():
        return jsonify({'status' : 'ERROR',
                        'message': f'ERROR: You already have an existing booking at "{hotel_name}" on {data["checkindate"]}, under the name of {current_user.name}.'})

    save_booking_csv(new_book)
    return jsonify({'status' : 'OK',
                    'message': f'Booking at "{hotel_name}" on {data["checkindate"]} for {current_user.name} was made.'})