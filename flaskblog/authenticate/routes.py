from flaskblog.authenticate.forms import UpdateAccountForm, RequestResetForm, ResetPasswordForm
from flask import render_template, request, flash,url_for, redirect, Blueprint
from flaskblog.utils import save_picture, send_reset_password_request
from flask_login import login_required, current_user
from flaskblog.models import User
from flaskblog import db, bcrypt

authentication = Blueprint('authentication', __name__)

@authentication.route('/account',  methods=['GET', 'POST'])
@login_required
def account():
    form =  UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            profile_pic=  save_picture(form.picture.data)
            current_user.image_file = profile_pic
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash(f"Your account is successfully updated!", 'success')
        return redirect(url_for('authentication.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='account', image_file=image_file, form=form)

@authentication.route('/request_reset_password', methods=['GET', 'POST'])
def request_reset_password():
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_password_request(user)
        flash(f'An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title="Reset Request", form=form)

@authentication.route('/password_reset/<string:token>', methods=['GET', 'POST'])
def reset_password(token):
    user = User.verify_reset_token(token)
    if user is None:
        flash(f'That is an invalid or expired token', 'warning')
        return redirect(url_for('authentication.request_reset_password'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password 
        db.session.commit()
        flash(f'Your password has been updated! you are now able to login', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_password.html', title="Reset Password", form=form)