from flask import Blueprint, request, render_template, jsonify
from flask_login import login_required, current_user
from datetime import datetime, timedelta
from models.hotel import Hotel
from models.user import User

package = Blueprint('package', __name__)

# for question 1 c (ii)
import pandas as pd

@package.route('/products')
@login_required
def viewallpackages():
    # Home page of all authenticated users
    # To load assets/js/staycation.js as required from q1c (ii)
    hotel_list = []
    hotel_csv = pd.read_csv('assets/js/staycation.csv')
    for index, row in hotel_csv.iterrows():
        hotel_name,duration,unit_cost,image_url,description = list(row)
        hotel_list.append(Hotel(hotel_name=hotel_name,
                                duration=duration,
                                unit_cost=unit_cost,
                                image_url=image_url,
                                description=description))
    return render_template('viewallpackages.html', 
                            hotel_list=hotel_list)

@package.route('/view', methods=['GET'])
@login_required
def viewpackage():
    # retrive the hotel name from url query string
    hotel_name = request.args.get("hotel")
    hotel_csv = pd.read_csv('assets/js/staycation.csv')
    selected_hotel = hotel_csv[hotel_csv['hotel_name'] == hotel_name]

    if selected_hotel.empty:
        return render_template('viewpackage.html',
                            hotel_name="Invalid Hotel",
                            description="Invalid Hotel",
                            image_url="https://fscene8.me/content/images/size/w1000/2022/04/question-mark-1019820_1280-1-.jpg")
    return render_template('viewpackage.html', 
                            hotel_name=selected_hotel.iloc[0][0],
                            description=selected_hotel.iloc[0][4],
                            image_url=selected_hotel.iloc[0][3])

@package.route('/addbooking', methods=['POST'])
@login_required
def addbooking():
    # To be implemented in Q2
    return jsonify({'status' : 'ERROR',
                    'message': f'Booking Model not yet avaliable in Q1. It will be implemented in Q2'})