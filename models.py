"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


def connect_db(app):
    """ Connect to database. """

    db.app = app
    db.init_app(app)



class User(db.Model):
    """ User """

    __tablename__ = "users"

    def __repr__(self):
        return f'<User: {self.id} {self.first_name} {self.last_name}>'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    first_name = db.Column(db.String(50),
                           nullable=False)
    last_name = db.Column(db.String(50),
                          nullable=False)
    image_url = db.Column(db.Text,
                          default="https://bit.ly/2RD7Vny",
                          nullable=False)
    
    posts = db.relationship('Post', backref="user")


class Post(db.Model):
    """ Post """

    __tablename__ = "posts"

    def __repr__(self):
        return f'<Post: {self.id} {self.title} {self.created_at} {self.user_id}>'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    
    title = db.Column(db.String(100),
                        nullable=False)

    content = db.Column(db.Text,
                        nullable=False)
    
    created_at = db.Column(db.DateTime(timezone=True),
                           default=datetime.now,
                           nullable=False)

    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id'),
                        nullable=False)
    
    # direct navigation: posts -> posts_tags 
    entries = db.relationship('PostTag', backref="post")


class Tag(db.Model):
    """ Tag """

    __tablename__ = "tags"

    def __repr__(self):
        return f'<Tag: {self.id} {self.name}>'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

    name = db.Column(db.String(30),
                        nullable=False,
                        unique=True)

    # direct navigation: tags -> posts_tags 
    entries = db.relationship('PostTag', backref="tag")

    # direct navigation: tags -> posts & back
    posts = db.relationship('Post', secondary="posts_tags", backref='tags')


class PostTag(db.Model):
    """ Join table for Post ids and Tag ids """

    __tablename__ = "posts_tags"

    def __repr__(self):
        return f'<PostTag: post_id{self.post_id}, tag_id{self.tag_id}>'

    post_id = db.Column(db.Integer,
                        db.ForeignKey("posts.id"),
                        primary_key=True,
                        nullable=False)

    tag_id = db.Column(db.Integer,
                        db.ForeignKey("tags.id"),
                        primary_key=True,
                        nullable=False)