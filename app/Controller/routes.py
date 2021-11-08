from __future__ import print_function
import sys
from typing import Text
from flask import Blueprint
from flask import render_template, flash, redirect, url_for, request
from config import Config
from flask_login import login_required, current_user


from app import db
from app.Model.models import Post, User
from app.Controller.forms import PositionForm, EditForm

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


#Home page, displays all research positions
@bp_routes.route('/home', methods=['GET','POST'])
@login_required
def home():
    user = current_user
    if user.usertype == 'student' or user.usertype == 'faculty':
        totalPositions = Post.query.count()
        position = Post.query.order_by(Post.date1.desc())
        return render_template('home.html', title="Home", posts=position.all(), totalPosts=totalPositions)
    else:
        flash('Please log in to access this page.')
        return redirect(url_for('routes.index'))


#IMPORTANT
# To change the tags that appear, go to research.py and edit them manually in line 15
# Be sure to delete db file everytime you do this since you are editing the db schema, otherwise it will not appear

@bp_routes.route('/post', methods=['GET','POST'])
@login_required
def post():
    user = current_user
    if user.usertype == 'student':
        return redirect(url_for('routes.home'))
    else:
        hform = PositionForm()
        if hform.validate_on_submit():
            newpost = Post(project_title = hform.project_title.data,
            description = hform.description.data,
            date1 = hform.date1.data,
            date2 = hform.date2.data,
            time = hform.time.data,
            requirements = hform.requirements.data, 
            faculty_info = hform.faculty_info.data)
            research_field = hform.research.data
            for t in research_field:
                newpost.research_field.append(t)
            db.session.add(newpost)
            db.session.commit()
            flash('Reseach position has been posted '+ newpost.project_title)
            return redirect(url_for('routes.index'))
        return render_template('_post.html', title="Home", form=hform)

#If the user registers as a student, they are immediately sent here to finish setting up profile
#@bp_routes.route('/setup', methods=['GET','POST'])
#@login_required
#def setup():
#    user = current_user
#    if user.usertype=='student':
#        return render_template('setup.html')
#    else:
#        flash("You must be a student to view this page")
#        return redirect(url_for('routes.home'))

@bp_routes.route('/setup', methods=['GET','POST'])
@login_required
def setup():
    eform = EditForm()
    user = current_user
    if user.usertype=='student':
        if eform.validate_on_submit():
            user.firstname = eform.firstname.data
            user.lastname = eform.lastname.data
            user.email = eform.email.data
            user.set_password = eform.set_password .data
            db.session.add(user)
            db.session.commit()
            flash("Your account has been updated")
        return render_template('setup.html', form = eform)
    else:
        flash("You must be a student to view this page")
        return redirect(url_for('routes.home'))
