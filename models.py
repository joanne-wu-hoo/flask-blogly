from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def connect_db(app):
    """ Connect to database. """

    db.app = app
    db.init_app(app)


"""Models for Blogly."""


class User(db.Model):
    """ User """

    __tablename__ = "users"

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

    @classmethod
    def get_number_of_users(cls):
        return len(cls.query.all())



