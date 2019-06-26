"""Blogly application."""

from flask import Flask, render_template, request, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()


@app.route("/")
def redirect_to_user_list():
    """ Redirect to list of users """
    return redirect('/users')


@app.route("/users")
def show_user_list():
    """ Show all users """
    users = User.query.all()
    return render_template('users_list.html', users=users)


@app.route("/users/new")
def show_add_user_form():
    """ Show add form for users """
    return render_template("new_user_form.html")


@app.route("/users", methods=["POST"])
def process_new_user():
    """ Process add form and redirect to /users """
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    image_url = request.form.get("image_url")

    if image_url == "":
        image_url = None

    # add new user to database
    new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(new_user)
    db.session.commit()

    flash("User added!", "success")
    return redirect("/users")


@app.route("/users/<user_id>")
def show_user_profile(user_id):
    """ Show user profile page """

    user = User.query.get(user_id)

    return render_template('user_profile.html', user=user)


@app.route("/users/<user_id>/edit")
def show_user_edit_form(user_id):
    """ Show edit page for user"""

    user = User.query.get(user_id)

    return render_template('edit_user_profile.html', user=user)


@app.route("/users/<user_id>/edit", methods=["POST"])
def process_user_edit_form(user_id):
    """ Process edit form for user"""

    # get values from form
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    image_url = request.form.get("image_url")

    user = User.query.get(user_id)

    # update fields
    user.first_name = first_name
    user.last_name = last_name
    user.image_url = image_url

    db.session.commit()

    return redirect('/users')


@app.route("/users/<user_id>/delete", methods=["POST"])
def delete_user(user_id):
    """ Delete user """
    user = User.query.get(user_id)

    db.session.delete(user)
    db.session.commit()

    flash(f"{user.first_name} {user.last_name} deleted", "danger")
    return redirect("/users")
