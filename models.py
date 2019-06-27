"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def connect_db(app):
    """ Connect to database. """

    db.app = app
    db.init_app(app)





class User(db.Model):
    """ User """

    __tablename__ = "users"

    def __repr__(self):
        return f'<{self.id} {self.first_name} {self.last_name}>'

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



