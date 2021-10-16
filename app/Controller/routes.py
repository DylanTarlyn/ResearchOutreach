from __future__ import print_function
import sys
from typing import Text
from flask import Blueprint
from flask import render_template, flash, redirect, url_for, request
from config import Config
from flask_login import login_required, current_user


from app import db
from app.Model.models import Post, User
from app.Controller.forms import PostForm

bp_routes = Blueprint('routes', __name__)
bp_routes.template_folder = Config.TEMPLATE_FOLDER #'..\\View\\templates'


@bp_routes.route('/', methods=['GET'])
@bp_routes.route('/index', methods=['GET'])
@login_required
def index():
    return render_template('index.html', title="Placeholder")

@bp_routes.route('/facultyTest', methods=['GET'])
@login_required
def facultyTest():
    user = current_user
    if user.usertype =='student':
        return render_template('index.html', title="Access denied >:)")
    if user.usertype =='faculty':
        return render_template('facultyTest.html')
    else:
       return render_template('index.html', title="Test failed")

@bp_routes.route('/studentTest', methods=['GET'])
@login_required
def studentTest():
    user = current_user
    if user.usertype =='student':
        return render_template('studentTest.html')
    if user.usertype =='faculty':
        return render_template('index.html', title="Access denied >:)")
    else:
       return render_template('index.html', title="Test failed")
