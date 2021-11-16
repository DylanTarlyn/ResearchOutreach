from datetime import datetime
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login

#TO DO:
#Add programming language model/table w id and name to connect to user & association table w user id and  language id
#Tech electives?
#Add above to research.py to init site with?

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

research_tag = db.Table('research_tag',
    db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
    db.Column('research_id', db.Integer, db.ForeignKey('research.id'))
    )

user_research=db.Table('user_research_tag',
    db.Column('user_id',db.Integer,db.ForeignKey('user.id')),
    db.Column('research_id', db.Integer, db.ForeignKey('research.id'))
)   

class Research(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    field = db.Column(db.String(30))

class Language(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    field = db.Column(db.String(30))

language_tag=db.Table('language_tag',
    db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
    db.Column('language_id', db.Integer, db.ForeignKey('language.id'))
    )

user_language=db.Table('user_language',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('language_id', db.Integer, db.ForeignKey('language.id'))
    )




class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_title = db.Column(db.String(150))
    description = db.Column(db.String(300))
    date1 = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    date2 = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    time = db.Column(db.Integer)
    research_field = db.relationship('Research', secondary = research_tag, primaryjoin=(research_tag.c.post_id == id), backref = db.backref('research_tag', lazy='dynamic'), lazy ='dynamic')
    language_field = db.relationship('Language', secondary = language_tag, primaryjoin=(language_tag.c.post_id == id), backref = db.backref('language_tag', lazy='dynamic'), lazy ='dynamic')
    requirements = db.Column(db.String(300))
    faculty_info = db.Column(db.String(200))
    user_id=db.Column(db.Integer, db.ForeignKey('user.id'))
    
    def get_tags(self):
        return self.research_field
    
    def get_lang(self):
        return self.language_field

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(120), unique=True, index=True) #Needs to be @wsu.edu domain
    password_hash = db.Column(db.String(128))
    usertype = db.Column(db.String(10))
    posts = db.relationship('Post', backref='writer', lazy='dynamic')
    firstname=db.Column(db.String(30))
    lastname=db.Column(db.String(30))
    phone =  db.Column(db.Integer)
    gpa = db.Column(db.Float)
    major =  db.Column(db.String(30))
    graduation = db.Column(db.DateTime)
    research_field = db.relationship('Research', secondary = user_research, primaryjoin=(user_research.c.user_id == id), backref = db.backref('user_research', lazy='dynamic'), lazy ='dynamic')
    language_field = db.relationship('Language', secondary = user_language, primaryjoin=(user_language.c.user_id == id), backref = db.backref('user_language', lazy='dynamic'), lazy ='dynamic')
    experience = db.Column(db.String(300))

    def get_user_tags(self):
        return self.research_field
    
    def get_user_lang(self):
        return self.language_field

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def get_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_usertype(self):
        return self.usertype

    def get_user_posts(self):
        return self.posts
