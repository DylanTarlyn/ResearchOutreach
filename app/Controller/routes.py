from __future__ import print_function
import sys
from flask import Blueprint
from flask import render_template, flash, redirect, url_for, request
from config import Config

from app import db
from app.Model.models import Post , Tag , postTags
from app.Controller.forms import PostForm

bp_routes = Blueprint('routes', __name__)
bp_routes.template_folder = Config.TEMPLATE_FOLDER #'..\\View\\templates'


@bp_routes.route('/', methods=['GET'])
@bp_routes.route('/index', methods=['GET'])
def index():
    posts = Post.query.order_by(Post.timestamp.desc())
    return render_template('index.html', title="Smile Portal", posts=posts.all(), total_smile= posts.count())

#@bp_routes.route('/likes/', methods = ['GET'])
#def likes ():
#    likes = Post.query.order_by(Post.likes.desc())
#    return render_template('_post.html', likes=likes)

@bp_routes.route('/likes/<post_id>', methods =['POST'])
def likes(post_id):
    post = Post.query.filter_by(id=post_id).first()
    if post:
        post.likes +=1
        db.session.add(post)
        db.session.commit()
    return redirect(url_for('routes.index'))

#code was gotten from flask exercise
@bp_routes.route('/smile/', methods = ['GET' , 'POST'])
def smile ():
    pform = PostForm()
    if pform.validate_on_submit():
        newpost = Post(title = pform.title.data, body = pform.body.data, happiness_level= pform.happiness_level.data)
        db.session.add(newpost)
        db.session.commit()
        flash('New Post ' + newpost.title)
        return redirect(url_for('routes.index'))
    return render_template('create.html', form = pform)



    