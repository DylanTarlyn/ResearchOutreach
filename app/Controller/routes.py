from __future__ import print_function
import sys
from typing import Text
from flask import Blueprint
from flask import render_template, flash, redirect, url_for, request
from config import Config
from flask_login import login_required, current_user


from app import db
from app.Model.models import Post, User
from app.Controller.forms import PositionForm

bp_routes = Blueprint('routes', __name__)
bp_routes.template_folder = Config.TEMPLATE_FOLDER #'..\\View\\templates'


#Landing page w/ links to sign in or register
@bp_routes.route('/', methods=['GET'])
@bp_routes.route('/index', methods=['GET'])
def index():
    if current_user.is_authenticated:
        return redirect(url_for('routes.home'))
    else:
        return render_template('index.html', title="Welcome")

#Home page, displays all research positions
@bp_routes.route('/home', methods=['GET','POST'])
@login_required
def home():
    user = current_user
    if user.usertype == 'student' or user.usertype == 'faculty':
        totalPositions = Post.query.count()
        position = Post.query.order_by(Post.project_title)
        return render_template('home.html', title="Home", posts=position, totalPosts=totalPositions)
    else:
        flash('Please log in to access this page.')
        return redirect(url_for('routes.index'))


@bp_routes.route('/post', methods=['GET','POST'])
@login_required
def post():
    user = current_user
    if user.usertype == 'student':
        return redirect(url_for('routes.home'))
    else:
        hform = PositionForm()
        if hform.validate_on_submit():
            newpost = Post(project_title = hform.project_title.data, description = hform.description.data, requirments = hform.requirments.data, 
            info = hform.faculty_info.data)
           # researchs = hform.research.data
           # for t in researchs:
            #    newpost.researchs.append(t)
            db.session.add(newpost)
            db.session.commit()
            flash('Reseach position has been posted '+ newpost.project_title)
            return redirect(url_for('routes.index'))
        return render_template('_post.html', title="Home", form=hform)

