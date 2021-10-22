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

#How to restrict page access by user: 
#   user = current_user
#   if user.usertype == 'student' (or if user.usertype == 'faculty'):
#   issue flash message
#   redirect to another page if they should not be allowed to view it
#   else:
#   do normal thing for that route
# 
#   feel free to use the facultyTest and studentTest html templates if you want to mess around with this


# This route will display all of the posts
# If the user is a student they can apply to posts
# If the user is a faculty they can create new posts via a link in the navbar


@bp_routes.route('/home', methods=['GET','POST'])
@login_required
def home():
    return render_template('home.html', title="Home")


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
            researchs = hform.research.data
            for t in researchs:
                newpost.researchs.append(t)
            db.session.add(newpost)
            db.session.commit()
            flash('Reseach position has been posted '+ newpost.project_title)
            return redirect(url_for('routes.index'))
        return render_template('_post.html', title="Home", form=hform)

