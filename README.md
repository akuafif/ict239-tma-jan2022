# ICT239 TMA Jan 2022 Question 2
I have written 2 bash scripts (`setup.sh` & `start.sh`) to automate the creation of venv for q2.

# Setting up the enviroment
Run the `setup.sh` file.

# To run the flask app
Run `start.sh` file.

Please register with `admin@abc.com` for admin access.


# Question 2 Notable Locations

## AJAX
- File upload (assets/js/upload.js)
- Dashboard (assets/js/dashboard.js)
- Booking (assets/js/booking.js)

## Python returning JSON for AJAX
- File upload feature (models.admin) (blueprints/admin.py)
- Dashboard feature (models.admin) (blueprints/admin.py)
- Booking feature (models.package) (blueprints/package.py)

# Models
- user.py, to access user collection
- staycation.py, to access staycation collection
- booking.py, to access booking collection

## Chart.js 
- dashboard.html (templates.dashboard.html)

## Jinga usage
- All HTML templates

## Jinga Marco flaskform (_render_field.html)
- register.html 
- login.html

## Cookies
- Remember Me upon login/register (models.auth) (blueprints/auth.py)
- COOKIE_TIME_OUT (`__init__.py`) 



# Software Used
- Debian 11 Bulleye (Proxmox LXC) 
- vscode-server https://github.com/coder/code-server
- MongoDB v5.0.6