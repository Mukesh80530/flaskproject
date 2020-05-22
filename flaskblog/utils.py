import os
import secrets
from PIL import Image
from flaskblog import mail
from flask_mail import Message 
from flask import url_for, current_app

def save_picture(profile_pic):
	random_hex = secrets.token_hex(8)
	_, f_ext = os.path.splitext(profile_pic.filename)
	picture_fn = random_hex + f_ext
	picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)
	output = (125, 125)
	image = Image.open(profile_pic)
	image.thumbnail(output)
	image.save(picture_path)
	return picture_fn

def send_reset_password_request(user):
	token = user.get_reset_token()
	print(token)
	msg =  Message('Password Reset Request', 
					sender='noreply@demo.com',
					recipients=[user.email])
	msg.body =f'''To reset your password, visit the following link:
	{url_for('authentication.reset_password', token=token, _external=True)}

	If you did not make this request then simply ignore this mail.
	'''
	mail.send(msg)