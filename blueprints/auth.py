from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from flask import Blueprint, request, redirect, render_template, url_for, make_response
from form import RegForm
from models.user import User
from app import COOKIE_TIME_OUT

auth = Blueprint('auth', __name__)

# Using xor encryption for password cookie
XOR_KEY = '1@3_FGSGA9gsg88SS02b8gsgs83RNS8gsgk9'
def sxor(pwd): 
    key = ''.join(XOR_KEY[i] for i in range(len(pwd)+1))   
    return ''.join(chr(ord(a) ^ ord(b)) for a,b in zip(pwd,key))
    
@auth.route('/login', methods=['GET', 'POST'])   
@auth.route('/')
def login():
    # Root of the webpage
    # if log in, redirect to viewallpackages page
    if current_user.is_authenticated:
         return redirect(url_for('package.viewallpackages'))

    form = RegForm()
    email = ""
    pwd = ""
    rem = ""
    if request.method == 'POST':
        if form.validate():
            check_user = User.get(form.email.data)
            if check_user:
                if form.password.data == check_user.password:
                    resp = make_response(redirect(url_for('package.viewallpackages')))

                    # Save details to cookies
                    if request.form.get('checkbox') is not None:
                        resp.set_cookie('email', form.email.data, max_age=COOKIE_TIME_OUT)
                        resp.set_cookie('pwd',  sxor(form.password.data), max_age=COOKIE_TIME_OUT) 
                        resp.set_cookie('rem',  "checked", max_age=COOKIE_TIME_OUT)
                    else: 
                        resp.delete_cookie('email')
                        resp.delete_cookie('pwd')
                        resp.delete_cookie('rem')
                    login_user(check_user)
                    return resp
                else:
                    form.password.errors.append("User Password Not Correct")
            else:
                form.email.errors.append("No Such User")
    else:
        # Check if remember me check box is set
        if 'email' in request.cookies:
            email = request.cookies.get('email')
            pwd = sxor(request.cookies.get('pwd'))
            rem = request.cookies.get('rem')
    return render_template('login.html', form=form, email=email, pwd=pwd, rem=rem)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegForm()
    if request.method == 'POST':
        if form.validate():
            existing_user = User.get(form.email.data)
            if existing_user is None:
                # no hashing is done because saving to users.csv
                new_user = User(email=form.email.data,password=form.password.data,name=form.name.data)
                new_user.save()

                resp = make_response(redirect(url_for('package.viewallpackages')))
                # Save details to cookies
                if request.form.get('checkbox') is not None:
                    resp.set_cookie('email', new_user.email, max_age=COOKIE_TIME_OUT)
                    resp.set_cookie('pwd',  sxor(form.password.data), max_age=COOKIE_TIME_OUT)
                    resp.set_cookie('rem',  "checked", max_age=COOKIE_TIME_OUT)
                else: 
                    resp.delete_cookie('email')
                    resp.delete_cookie('pwd')
                    resp.delete_cookie('rem')
                login_user(new_user)
                return resp
            else:
                form.email.errors.append("User already existed")
    return render_template('register.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login')) 
