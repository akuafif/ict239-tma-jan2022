# This is question 1 TMA
I have written 2 bash scripts (setup.sh & start.sh) to automate the creation of venv for q1.

There is no MongoDB instance in q1.
All data are stored and accessed with CSV files in the asset folder

## Setting up the enviroment
Please run the setup.sh

## To run the flask app
run start.sh

Please register with "admin@abc.com" for admin access.




###############################
## Q1 description
html templates:
- _render_field.html, Jinga marco
- base.html, base layout
- login.html, login page
- register.html, register page
- viewallpackages.html, view all packages page and home page for all accounts
- booking.html, to view and book a package

blueprints folder:
- auth.py, routes for authentication related 
- package.py, routes for package related

models folder:
- user.py, User model class without MongoDB
- staycation.py, staycation model class

MongoDB:
- Only User collection in MongoDB is used

js assets:
- booking,js, AJAX call for booking, to be used with booking.html
- dtsel.js, datepicker js library
- moment.js, date format js library

## Jinga usage
- All HTML templates

## Jinga Marco flask form (_render_field.html)
- register.html 
- login.html

## Cookies
- Remember Me upon login/register (models.auth) (blueprints/auth.py)
- COOKIE_TIME_OUT (__init__.py) 



######################
# Code are written in:
- Debian 11 Bulleye (Proxmox LXC) 
- vscode-server https://github.com/coder/code-server