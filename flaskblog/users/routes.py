from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, logout_user
from flaskblog import db, bcrypt
from flaskblog.models import User
from flaskblog.users.forms import RegistrationForm, LoginForm

users = Blueprint('users', __name__)


@users.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user =  User(username=form.username.data, email= form.email.data, password = hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created! you are now able to login', 'success')
        return redirect(url_for('users.login'))
    else:
        return render_template('register.html', title='Register', form=form)

@users.route('/login', methods=['GET', 'POST'])
def login():
    form =  LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        print('user--->', user.password)
        print(form.email.data)
        print(form.password.data)
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            print('yes')
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash(f'login success!', 'success')
            return  redirect(next_page) if next_page else redirect(url_for('mains.home'))
        else:
            flash(f'Failed to login!', 'danger')
    return render_template('login.html', title='Login', form=form)
    
@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('mains.home'))