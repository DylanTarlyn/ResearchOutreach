from datetime import datetime
from app import db


post_tag = db.Table('post_tag',
    db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
    )



class Tag(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(20))
    
    def __repr__(self):
        return '<Post ({},{})>', format(self.id,self.name)



class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    body = db.Column(db.String(1500))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    likes = db.Column(db.Integer, default= 0)
    happiness_level = db.Column(db.Integer, default = 3)
    tag = db.relationship('Tag',secondary = post_tag,
    primaryjoin=(post_tag.c.post_id == id),
    backref = db.backref('post_tag', lazy='dynamic'), lazy='dynamic')


    def __repr__(self):
        return '<Post ({},{},{},{},{})>',format(self.title,self.body,self.timestamp,self.happiness_level,self.likes)

    def get_tags(self):
        return 'self.tag'


