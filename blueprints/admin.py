from flask import Blueprint, request, redirect, render_template, url_for, jsonify
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash

# file upload operation related imports
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
import pandas as pd
from models.user import User
from models.staycation import Staycation
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
    if current_user.email == 'admin@abc.com':
        return render_template('upload.html')
    return redirect(url_for('auth.login')) 

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
                pa = Staycation(hotel_name=hotel_name,
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
                hotel_obj = Staycation.objects(hotel_name=hotel_name).first()
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
    # Generate a date object 
    d,m,y = str(data['fromdate']).split('-')
    fromDate = datetime(year=int(y),month=int(m),day=int(d))
    d,m,y = str(data['todate']).split('-')
    toDate = datetime(year=int(y),month=int(m),day=int(d))
    gap = toDate - fromDate

    isViewAll = bool(data['viewall'])

    # Create containers to pass to chart js
    date_labels = [] # x-axis
    hotel_label = [] # legend
    income_label = {} # legend x-axis
    income_dict = {} # legend y-axis
    if isViewAll:
        date_list = [fromDate + timedelta(days=x) for x in range(gap.days+1)]
        date_labels = [d.strftime("%Y-%m-%d") for d in date_list]
        for hotel in Staycation.objects: 
            hotel_label.append(hotel.hotel_name)
            income_dict[hotel.hotel_name] = [0 for d in date_list] # put 0 as default value
            income_label[hotel.hotel_name] = [fromDate + timedelta(days=x) for x in range(gap.days+1)]
            

    for h in Staycation.objects:
        # Sort the bookings by date
        for book in Booking.objects(hotel_name=h.id).order_by('check_in_date'):
            if toDate >= book.check_in_date >= fromDate: 
                date_str = book.check_in_date.strftime("%Y-%m-%d")
                if isViewAll:
                    date_index = date_list.index(book.check_in_date)
                    income_dict[h.hotel_name][date_index] += h.unit_cost   
                else:
                    if not h.hotel_name in hotel_label:
                        hotel_label.append(h.hotel_name)
                        income_label[h.hotel_name] = []
                        income_dict[h.hotel_name] = []
                    if date_str not in date_labels:
                        date_labels.append(date_str)
                    if date_str not in income_label[h.hotel_name]:
                        income_label[h.hotel_name].append(date_str)
                        income_dict[h.hotel_name].append(h.unit_cost)
                    else:
                        # add the income to existing date
                        index = income_label[h.hotel_name].index(date_str)
                        income_dict[h.hotel_name][index] += h.unit_cost
    date_labels.sort()
    return hotel_label, date_labels, income_dict, income_label, gap
    
@admin.route('/get_chart_data', methods=['GET', 'POST'])
@login_required    
def get_chart_data():
    if current_user.email != 'admin@abc.com':
        return jsonify({'status' : 'ERROR', 
                        'message' : ['Not Allowed! User is not admin!']})

    # Generate the required variables for chart js
    data = request.get_json()
    hotel_label, date_labels, income_dict, income_label, gap = generateIncomeInRange(data)
    return jsonify({'status' : 'OK',
                    'message': f'{data}',
                    'hotel_label' : hotel_label,
                    'date_labels' : date_labels,
                    'income_dict' : income_dict,
                    'income_label': income_label,
                    'daysrange' : gap.days+1})