from datetime import datetime

from flask import Blueprint, render_template, request, redirect, url_for, flash, get_flashed_messages
from flask_login import login_user, login_required, logout_user, current_user, UserMixin
from flask_sqlalchemy import SQLAlchemy

from dbConn import getUser


db = SQLAlchemy()

auth = Blueprint('auth', __name__)

class User(UserMixin):
    def __init__(self, username, password, id, fname, lname, position):
        self.username = username
        self.password = password
        self.id = id
        self.fname = fname
        self.lname = lname
        self.position = position


@auth.route('/login', methods=['GET', 'POST'])
def login():
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        e_login_result, e_password_result, e_id_result, e_fname_result, e_lname_result, e_position_result = getUser(username)
        if e_login_result is None or e_password_result != password:
            error = 'Invalid username or password. Please try again.'
            flash(error, category='error')
        else:
            user = User(e_login_result, e_password_result, e_id_result, e_fname_result, e_lname_result, e_position_result)
            login_user(user)
            return redirect('/')
    messages = get_flashed_messages(with_categories=True)
    print(messages)
    return render_template('login.html', error=error, current_time=current_time)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
