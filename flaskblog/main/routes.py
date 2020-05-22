from flask import render_template, request, Blueprint
from flaskblog.models import Post

mains = Blueprint('mains', __name__)

@mains.route('/')
@mains.route('/home')
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page= page, per_page=3)
    return render_template('home.html', posts = posts)

@mains.route('/about')
def about():
    return render_template('about.html')