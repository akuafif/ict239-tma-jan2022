# ICT239 Jan 2022 TMA Question 1 
I have written 2 bash scripts (setup.sh & start.sh) to automate the creation of venv for q1.

There is no MongoDB instance in q1.

All data are stored and accessed with CSV files in the asset folder

## Setting up the enviroment
Run the `setup.sh` file.

## To run the flask app
Run the `start.sh` file.

Please register with `admin@abc.com` for admin access.



-------------------
## Question 1 HTML/CSS/JS/AJAX, Jinja, and Flask programming 
### CSV Files as data storage
- assets/users.csv
- assets/booking.csv
- assets/js/staycation.csv (__Location locked by TMA Q1 requirement__)
### HTML:
- _render_field.html, Jinga marco
- base.html, base layout
- login.html, login page
- register.html, register page
- viewallpackages.html, view all packages page and home page for all accounts
- booking.html, to view and book a package

### CSS:
- custom.css
- dtsel.css, datepicker css

### JS/AJAX
- booking.js, for booking.html (AJAX)
- dtsel.js, datepicker js library
- moment.js, date format js library

### FLASK programming:
- blueprint/auth.py, routes for authentication related 
- models/package.py, routes for package related

### models:
- models/user.py, User model class without MongoDB
- models/staycation.py, staycation model class

### Jinga:
- All HTML templates
- templates/register.html (wtform)
- templates/login.html (wtform)

### Cookies
- Remember Me upon login/register (models.auth) (blueprints/auth.py)
- COOKIE_TIME_OUT (__init__.py) 



#########################
# Code are written in:
- Debian 11 Bulleye (Proxmox LXC) 
- vscode-server https://github.com/coder/code-server