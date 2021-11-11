from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField ,validators, DateField, PasswordField
from wtforms.fields.core import BooleanField
from wtforms.validators import  DataRequired, Length, Email, EqualTo
from wtforms.widgets.core import TextArea
from wtforms_sqlalchemy.fields import QuerySelectMultipleField
from wtforms.widgets import ListWidget, CheckboxInput

from app.Model.models import Research


def get_research():
    return Research.query.all()

def get_researchlabel(theresearch):
    return theresearch.field


class PositionForm(FlaskForm):
    project_title = StringField('Title of project', validators=[DataRequired()])
    description = TextAreaField('Description of research position', validators = [Length(min=1,max=1500)])
    date1 = DateField('Start date', format='%m/%d/%Y')
    date2 = DateField('End date', format='%m/%d/%Y')
    time = StringField('How many hours would you like to work?', validators = [DataRequired()])
    research = QuerySelectMultipleField('Fields', query_factory = get_research, get_label = get_researchlabel, widget = ListWidget(prefix_label=False),option_widget = CheckboxInput())
    requirements = StringField('A brief description of the required qualifications', validators=[DataRequired()])
    faculty_info = TextAreaField('Faculty’s name and contact information ', validators = [Length(min=1,max=1500)])
    submit = SubmitField('Post')

class EditForm(FlaskForm):
    firstname =  StringField('First Name', validators=[DataRequired()])
    lastname =  StringField('Last Name', validators=[DataRequired()])
    email =  StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    sumbit = SubmitField('Submit')
    
class SortForm(FlaskForm):
    choices=SelectField(choices=[('Newest'),('Oldest'),('Test1'),('Test2')])
    myposts=BooleanField('Display my posts only')
    submit=SubmitField('Apply filters')
