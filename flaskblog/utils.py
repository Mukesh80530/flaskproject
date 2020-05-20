import os
import secrets
from PIL import Image
from flaskblog import app

def save_picture(profile_pic):
	random_hex = secrets.token_hex(8)
	_, f_ext = os.path.splitext(profile_pic.filename)
	picture_fn = random_hex + f_ext
	picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
	output = (125, 125)
	image = Image.open(profile_pic)
	image.thumbnail(output)
	image.save(picture_path)
	return picture_fn