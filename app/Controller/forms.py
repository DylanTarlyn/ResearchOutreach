from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField ,validators, DateField
from wtforms.validators import  DataRequired, Length
from wtforms.widgets.core import TextArea

from app.Model.models import Research


def get_research():
    return Research.query.all()


class PositionForm(FlaskForm):
    project_title = StringField('Title of project', validators=[DataRequired()])
    description = TextAreaField('Description of research position', validators = [Length(min=1,max=1500)])
    date1 = DateField('Start date', format='%m/%d/%Y')
    date2 = DateField('End date', format='%m/%d/%Y')
    time = StringField('How many hours would you like to work?', validators = [DataRequired()])
    #research = not sure how to format this
    requirments = StringField('A brief description of the required qualifications', validators=[DataRequired()])
    faculty_info = TextAreaField('Faculty’s name and contact information ', validators = [Length(min=1,max=1500)])
    submit = SubmitField('Post')
