from datetime import datetime
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

research_tag = db.Table('research_tag',
    db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
    db.Column('research_id', db.Integer, db.ForeignKey('research.id'))
    )

class Research(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    field = db.Column(db.String(30))
    def __repr__(self):
        return '<Post ({},{})', format(self.id,self.field)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_title = db.Column(db.String(150))
    description = db.Column(db.String(300))
    date1 = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    date2 = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    time = db.Column(db.Integer)
    research_field = db.relationship('Research', secondary = research_tag, primaryjoin=(research_tag.c.post_id == id), backref = db.backref('research_tag', lazy='dynamic'), lazy ='dynamic')
    requirements = db.Column(db.String(300))
    faculty_info = db.Column(db.String(200))
    
    def get_tags(self):
        return self.research_field

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(120), unique=True, index=True) #Needs to be @wsu.edu domain
    password_hash = db.Column(db.String(128))
    usertype = db.Column(db.String(10))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def get_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_usertype(self):
        return self.usertype