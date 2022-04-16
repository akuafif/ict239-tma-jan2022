from flask import Blueprint, request, redirect, render_template, url_for, flash, render_template, jsonify
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash

# file upload operation related imports
import os
from werkzeug.utils import secure_filename
import pandas as pd
from models.user import User
from models.hotel import Hotel
from models.booking import Booking
from datetime import datetime, timedelta

admin = Blueprint('admin', __name__)

ALLOWED_EXTENSIONS = set(['csv'])
def allowed_file(filename):
    """ whitelists file extensions for security reasons """
    return '.' in filename and filename.split('.')[-1].lower()  in ALLOWED_EXTENSIONS

@admin.route('/upload', methods=['GET'])
@login_required
def upload():
    # 1. check if current user is admin
    # 2. if POST, ajax will check file and data type
    # 3. open file with pd, check if headers is valid for the datatype
    #    return error if wrong header for datatype. This requires pandas.
    # 4. for loop the pd object and save each row to db
    if current_user.email == 'admin@abc.com':
        return render_template('upload.html')
    return redirect(url_for('auth.login')) 

from flask import jsonify
from werkzeug.datastructures import FileStorage
@admin.route('/up_user', methods=['POST'])
@login_required
def up_user():
    if current_user.email != 'admin@abc.com':
        return jsonify({'status' : 'ERROR', 
                        'message' : ['Not Allowed! User is not admin!']})
    
    upload_result = []
    f = request.files['file']
    headers = ['email','password','name'] 
    upload_result.append(f'ERROR: File contains invalid user.csv header format')
    status = 'ERROR'
    if allowed_file(secure_filename(f.filename)):
        fdata = pd.read_csv(f)
        if list(fdata.columns) == headers:
            for index, row in fdata.iterrows():
                email , password, name = list(row)
                existing_user = User.objects(email=email).first()
                if existing_user is None:
                    hashpass = generate_password_hash(str(password), method='sha256')
                    User(email=email, 
                        password=hashpass, 
                        name=name).save()
                    upload_result.append(f'{name} [{email}] >> Added Successfully')
                else:
                    upload_result.append(f'{name} [{email}] >> Failed, existing email!')
            status = 'OK'
            upload_result.pop(0) # remove error msg at index 0
    return jsonify({'status' :status, 
                    'datatype' : 'user',
                    'filename': f'{f.filename}',
                    'message' : upload_result})

@admin.route('/up_staycation', methods=['POST'])
@login_required
def up_staycation():
    if current_user.email != 'admin@abc.com':
        return jsonify({'status' : 'ERROR', 
                        'message' : ['Not Allowed! User is not admin!']})

    upload_result = []
    f = request.files['file']
    headers = ['hotel_name','duration','unit_cost','image_url','description']
    upload_result.append(f'ERROR: File contains invalid staycation.csv header format')
    status = 'ERROR'
    if allowed_file(secure_filename(f.filename)):
        fdata = pd.read_csv(f)
        if list(fdata.columns) == headers:
            for index, row in fdata.iterrows():
                hotel_name,duration,unit_cost,image_url,description = list(row)
                pa = Hotel(hotel_name=hotel_name,
                        duration=duration,
                        unit_cost=unit_cost,
                        image_url=image_url,
                        description=description).save()
                upload_result.append(f'{hotel_name} >> Added Succssfully')
            status = 'OK'
            upload_result.pop(0) # remove error msg at index 0
    return jsonify({'status' :status, 
                    'datatype' : 'staycation',
                    'filename': f'{f.filename}',
                    'message' : upload_result})


@admin.route('/up_booking', methods=['POST'])
@login_required
def up_booking():
    if current_user.email != 'admin@abc.com':
        return jsonify({'status' : 'ERROR', 
                        'message' : ['Not Allowed! User is not admin!']})
                    
    upload_result = []
    f = request.files['file']
    headers = ['check_in_date','customer','hotel_name']
    upload_result.append(f'ERROR: File contains invalid booking.csv header format')
    status = 'ERROR'
    if allowed_file(secure_filename(f.filename)):
        fdata = pd.read_csv(f)
        if list(fdata.columns) == headers:
            for index, row in fdata.iterrows():
                check_in_date,customer,hotel_name = list(row)
                user_obj = User.objects(email=customer).first()
                hotel_obj = Hotel.objects(hotel_name=hotel_name).first()
                if user_obj and hotel_obj:
                    Booking(check_in_date=check_in_date,
                            customer=user_obj,
                            hotel_name=hotel_obj).save()
                    upload_result.append(f'{check_in_date} - {customer} - {hotel_name} >> Added Successfully!')
                else:
                    upload_result.append(f'{check_in_date} - {customer} - {hotel_name} >> Failed! Missing reference for user and staycation!')
            status = 'OK'
            upload_result.pop(0) # remove error msg at index 0
    return jsonify({'status' :status, 
                    'datatype' : 'booking',
                    'filename': f'{f.filename}',
                    'message' : upload_result})

@admin.route('/trend_chart', methods=['GET'])
@login_required
def chart():
    if current_user.email == 'admin@abc.com':
        return render_template('dashboard.html')
    return redirect(url_for('auth.login')) 
   
def generateIncomeInRange(data):
    # To geneate a dictionary for the dataset
    # format -> { hotel_name: [fromDate, ... , toDate] }
    # value  -> {"Shangri-La Singapore" : [300, ... , 0] }
    
    # Generate a date list to get the length of the x-axis
    d,m,y = str(data['fromdate']).split('-')
    fromDate = datetime(year=int(y),month=int(m),day=int(d))
    d,m,y = str(data['todate']).split('-')
    toDate = datetime(year=int(y),month=int(m),day=int(d))
    gap = toDate - fromDate
    date_list = [fromDate + timedelta(days=x) for x in range(gap.days+1)]

    # x-axis
    # change to yyyy-mm-dd string for dates labels on x-axis, as per TMA figure example
    date_labels = [d.strftime("%Y-%m-%d") for d in date_list]

    # Generate Legends label
    hotel_label = []
    for hotel in Hotel.objects:
        hotel_label.append(hotel.hotel_name)

    # Create a dictionary (dataset)
    income_dict = {}
    for h in hotel_label:
        # put 0 as default value
        income_dict[h] = [0 for d in date_list]

    for hotel in hotel_label:
        h = Hotel.objects(hotel_name=hotel).first()
        for book in Booking.objects(hotel_name=h.id):
            if toDate >= book.check_in_date >= fromDate: 
                date_index = date_list.index(book.check_in_date)
                income_dict[hotel][date_index] += h.unit_cost 
    return hotel_label, date_labels, income_dict, gap
    
@admin.route('/get_chart_data', methods=['GET', 'POST'])
@login_required    
def get_chart_data():
    if current_user.email != 'admin@abc.com':
        return jsonify({'status' : 'ERROR', 
                        'message' : ['Not Allowed! User is not admin!']})

    data = request.get_json()

    # Generate the required variables for chart js
    hotel_label, date_labels, income_dict, gap = generateIncomeInRange(data)

    return jsonify({'status' : 'OK',
                    'message': f'{data}',
                    'hotel_label' : hotel_label,
                    'date_labels' : date_labels,
                    'income_dict' : income_dict,
                    'daysrange' : gap.days+1})