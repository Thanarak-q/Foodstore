# from app.controllers import ctable_mange
from app.controllers import table_manage
from app.controllers import menu_manage
from app.controllers import employee_manage
<<<<<<< HEAD
from app.controllers import dasboard
=======
from app.controllers import order_manage

from app.controllers.Dashboard import Revenue
>>>>>>> 5b448d3e4d03ed1e16f2ee8c89a50513d7036e3a

from flask import (jsonify, render_template,
                   request, url_for, flash, redirect)
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.urls import url_parse
from app import app