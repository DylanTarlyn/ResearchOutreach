from __future__ import print_function
import sys
from typing import Text
from flask import Blueprint
from flask import render_template, flash, redirect, url_for, request
from config import Config
from flask_login import login_required, current_user


from app import db
from app.Model.models import Post, User, Research
from app.Controller.forms import PositionForm, EditForm, sortDate, SortTopics, SetupForm, SortLangauages

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

@bp_routes.route('/home', methods=['GET','POST'])
@login_required
def home():
    user = current_user
    dSort=sortDate()
    rSort=SortTopics()
    lSort = SortLangauages()
    topic = rSort.rTopics.data #use for sorting by topic
    language = lSort.language.data #use for sorting by language
    position = Post.query.order_by(Post.date1.desc())
    if dSort.validate_on_submit(): #Sorting
        if rSort.myposts.data==True: #Sorting by only their posts
            position=current_user.get_user_posts()
            if dSort.date.data=='Select Date':
                if rSort.rTopics.data == 'Select Topic':
                    position = current_user.get_user_posts().order_by(Post.date1.desc())
                else:
                    position = current_user.get_user_posts().filter(Post.research_field.any(
                        Research.field==topic)).order_by(Post.date1.desc())
            if dSort.date.data=='Newest': 
                if rSort.rTopics.data == 'Select Topic':
                    position = current_user.get_user_posts().order_by(Post.date1.desc())
                else:
                    position = current_user.get_user_posts().filter(Post.research_field.any(
                        Research.field==topic)).order_by(Post.date1.desc())
            if dSort.date.data=='Oldest': 
                if rSort.rTopics.data == 'Select Topic':
                    position = current_user.get_user_posts().order_by(Post.date1)
                else:
                    position = current_user.get_user_posts().filter(Post.research_field.any(
                        Research.field==topic)).order_by(Post.date1)
        else: #Sorting all posts
            if dSort.date.data=='Select Date':
                if rSort.rTopics.data == 'Select Topic':
                    position=Post.query.order_by(Post.date1.desc())
                else:        
                    position = Post.query.filter(Post.research_field.any(Research.field==topic)).order_by(Post.date1.desc())
            if dSort.date.data == 'Newest':
                if rSort.rTopics.data == 'Select Topic':
                    position=Post.query.order_by(Post.date1.desc())
                else:        
                    position = Post.query.filter(Post.research_field.any(Research.field==topic)).order_by(Post.date1.desc())
            if dSort.date.data == 'Oldest':
                if rSort.rTopics.data == 'Select Topic':
                    position=Post.query.order_by(Post.date1)
                else:
                    position = Post.query.filter(Post.research_field.any(Research.field==topic)).order_by(Post.date1)
    return render_template('home.html', title="Home", posts=position.all(), totalPosts=position.count(), dform=dSort, rform=rSort, user=user)

@bp_routes.route('/suggested', methods=['GET','POST'])
@login_required
def suggested(): 
    user = current_user
    dSort=sortDate()
    rSort=SortTopics()
    lSort = SortLangauages()

    #PUT QUERY FOR POSTS HERE (place holder used)
    #If the user tags contains x, filter x
    #If it contains x and y, filter x and y
    position = Post.query.filter(Post.research_field.any(Research.field=='Topic1'))

        #multi sort both researach topics and languages that match the research topics and languages for the user
        #Query the table for research fields and language fields where they == user research and language research 
        # (See models.py and the sorting above) 

    return render_template('home.html', title="Home", posts=position.all(), totalPosts=position.count(), dform=dSort, rform=rSort, user=user)


#IMPORTANT
# To change the topics and languages that appear, go to research.py and edit them manually in line 15
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
            faculty_info = user.firstname + ' '+ user.lastname + ' ' +user.email + ' ' +str(user.phone),
            user_id=current_user.id)
            research_field = hform.research.data
            for t in research_field:
                newpost.research_field.append(t)
            language_field = hform.language.data
            for l in language_field:
                newpost.language_field.append(l)
            db.session.add(newpost)
            db.session.commit()
            flash('Research position '+ newpost.project_title + ' has been posted')
            return redirect(url_for('routes.home'))
        return render_template('_post.html', title="Home", form=hform)

#Should probably move below to auth routes

@bp_routes.route('/setup', methods=['GET','POST'])
@login_required
def setup():
    eform = SetupForm()
    user = current_user
    if user.usertype=='student':
        if eform.validate_on_submit():
            user.firstname=eform.firstname.data
            user.lastname=eform.lastname.data
            user.phone=eform.phone.data
            user.gpa=eform.gpa.data
            user.major=eform.major.data
            user.graduation=eform.graduation.data
            user.experience=eform.experience.data

            research_field = eform.research.data
            for t in research_field:
                user.research_field.append(t)
            language_field = eform.language.data
            for l in language_field:
                user.language_field.append(l)

            db.session.add(user)
            db.session.commit()
            flash("Your account has been updated")
            return redirect(url_for('routes.home'))
    if user.usertype=='faculty':
        flash("You must be a student to view this page")
        return redirect(url_for('routes.home'))

    return render_template('setup.html', form = eform)

@bp_routes.route('/edit', methods=['GET','POST','DELETE'])
@login_required
def edit():
    eform =EditForm()
    user=current_user
    if request.method == 'POST': #For updating
        if eform.validate_on_submit():
            user.firstname=eform.firstname.data
            user.lastname=eform.lastname.data
            user.phone=eform.phone.data
            user.gpa=eform.gpa.data
            user.major=eform.major.data
            user.graduation=eform.graduation.data
            user.experience=eform.experience.data

            #remove tags otherwise more will just be added to existing
            if user:
                research_field=user.research_field.all()
                for t in research_field:
                    user.research_field.remove(t)
                db.session.commit()

                language_field=user.language_field.all()
                for t in language_field:
                    user.language_field.remove(t)
                db.session.commit()

            research_field = eform.research.data
            for t in research_field:
                user.research_field.append(t)
            language_field = eform.language.data
            for l in language_field:
                user.language_field.append(l)

            db.session.add(user)
            db.session.commit()
            flash("Your account has been updated")
    if request.method == 'GET': #For autofilling info
        eform.firstname.data=user.firstname
        eform.lastname.data=user.lastname
        eform.phone.data=user.phone
        eform.gpa.data=user.gpa
        eform.major.data=user.major
        eform.graduation.data=user.graduation
        eform.experience.data=user.experience


    return render_template('myprofile.html', form = eform, user=user)
