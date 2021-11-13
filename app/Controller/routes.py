from __future__ import print_function
import sys
from typing import Text
from flask import Blueprint
from flask import render_template, flash, redirect, url_for, request
from config import Config
from flask_login import login_required, current_user


from app import db
from app.Model.models import Post, User, Research
from app.Controller.forms import PositionForm, EditForm, sortDate, SortTopics

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


#Home page, displays all research positions
#Source for sorting by tags: https://docs.sqlalchemy.org/en/14/orm/tutorial.html

#Issues with this: Cannot sort by two things at once, ie by oldest and by a tag. Can sort independently if either set to 
# "Select Date" or "Select Topic". If both have values, it only sorts by whichever comes last since it overwrites the 
# previously met condition. Not sure how to sort by two conditions
@bp_routes.route('/home', methods=['GET','POST'])
@login_required
def home():
    user = current_user
    dSort=sortDate()
    rSort=SortTopics()
    position=Post.query.order_by(sortdate())
    position = Post.query.order_by(Post.date1.desc())
    if dSort.validate_on_submit(): #Sorting
        if rSort.myposts.data==True: #Sorting by only their posts
            position=current_user.get_user_posts()
            if dSort.date.data=='Newest': 
                position = current_user.get_user_posts().order_by(Post.date1.desc())
            if dSort.date.data=='Oldest': 
                position = current_user.get_user_posts().order_by(Post.date1)
            if rSort.rTopics.data == 'Test1':
                position=current_user.get_user_posts().filter(Post.research_field.any(Research.field=='Test1'))
            if rSort.rTopics.data == 'Test2':
                position=current_user.get_user_posts().filter(Post.research_field.any(Research.field=='Test2'))
            if rSort.rTopics.data == 'Test3':
                position=current_user.get_user_posts().filter(Post.research_field.any(Research.field=='Test3'))
            if rSort.rTopics.data == 'Test4':
                position=current_user.get_user_posts().filter(Post.research_field.any(Research.field=='Test4'))
            if rSort.rTopics.data == 'Test5':
                position=current_user.get_user_posts().filter(Post.research_field.any(Research.field=='Test5'))
        else: #Sorting all posts
            if dSort.date.data == 'Newest':
                position = Post.query.order_by(Post.date1.desc())
            if dSort.date.data == 'Oldest':
                position = Post.query.order_by(Post.date1)
            if rSort.rTopics.data == 'Test1':
                position=Post.query.filter(Post.research_field.any(Research.field=='Test1'))
            if rSort.rTopics.data == 'Test2':
                position=Post.query.filter(Post.research_field.any(Research.field=='Test2'))
            if rSort.rTopics.data == 'Test3':
                position=Post.query.filter(Post.research_field.any(Research.field=='Test3'))
            if rSort.rTopics.data == 'Test4':
                position=Post.query.filter(Post.research_field.any(Research.field=='Test4'))
            if rSort.rTopics.data == 'Test5':
                position=Post.query.filter(Post.research_field.any(Research.field=='Test5'))
    return render_template('home.html', title="Home", posts=position.all(), totalPosts=position.count(), dform=dSort, rform=rSort, user=user)

def sortdate():
    sort=sortDate()
    return sort.date.data
    
def sorttopic():
    sort=SortTopics()
    return sort.rTopics.data


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
            faculty_info = hform.faculty_info.data,
            user_id=current_user.id)
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
