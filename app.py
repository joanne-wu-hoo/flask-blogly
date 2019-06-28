"""Blogly application."""

from flask import Flask, render_template, request, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag, PostTag
from datetime import datetime
import time, pytz

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()


# PART ONE
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

    # If user input is blank, set to None
    # so database will go to default URL
    if image_url == "":
        image_url = None

    # add new user to database
    new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(new_user)
    db.session.commit()

    flash("User added!", "success")
    return redirect("/users")


@app.route("/users/<int:user_id>")
def show_user_profile(user_id):
    """ Show user profile page """

    user = User.query.get(user_id)

    return render_template('user_profile.html', user=user)


@app.route("/users/<int:user_id>/edit")
def show_user_edit_form(user_id):
    """ Show edit page for user"""

    user = User.query.get(user_id)

    return render_template('edit_user_profile.html', user=user)


@app.route("/users/<int:user_id>/edit", methods=["POST"])
def process_user_edit_form(user_id):
    """ Process edit form for user"""

    # get values from form
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["image_url"]

    # NOTE: use [] instead of get to raise an explicit error

    user = User.query.get(user_id)

    # update fields
    user.first_name = first_name
    user.last_name = last_name
    user.image_url = image_url

    db.session.commit()

    return redirect('/users')


@app.route("/users/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id):
    """ Delete user """
    user = User.query.get(user_id)
    posts = user.posts

    for post in posts:
        db.session.delete(post)
    
    db.session.delete(user)
    db.session.commit()

    flash(f"{user.first_name} {user.last_name} deleted", "danger")
    return redirect("/users")

# PART TWO

@app.route("/users/<int:user_id>/posts/new")
def show_add_post_form(user_id):
    """ Show form to add post """
    user = User.query.get(user_id)
    tags = Tag.query.all()

    return render_template('new_post_form.html', user=user, tags=tags)


@app.route("/users/<int:user_id>/posts", methods=["POST"])
def make_new_post(user_id):
    """ Handles new post and redirects to user detail page """
    # get post inputs from form
    title = request.form["title"]
    content = request.form["content"]

    # add post to database
    new_post = Post(title=title, content=content, user_id=user_id)

    db.session.add(new_post)
    db.session.commit()

    # get all tags
    tags = Tag.query.all()

    # for selected tags, add entry to post_tag table
    for tag_id in request.form.getlist('tags'):
        new_post_tag_entry = PostTag(post_id=new_post.id, tag_id=tag_id)
        db.session.add(new_post_tag_entry)
        db.session.commit()

    # flash message
    flash("Post added!", 'success')
    return redirect(f'/users/{user_id}')


@app.route("/posts/<int:post_id>")
def show_post(post_id):
    """ Show post """
    # change post_id to int???? guess not
    # print(type(post_id))
    post = Post.query.get(post_id)
    return render_template("show_post.html", post=post)


@app.route("/posts/<int:post_id>/edit")
def show_edit_post_form(post_id):
    """ Show form to edit post """
    post = Post.query.get(post_id)
    
    # get all tags
    tags = Tag.query.all()

    # get tags for post
    tags_for_post = post.tags


    return render_template("edit_post.html", post=post, tags=tags, 
                                             tags_for_post=tags_for_post)


@app.route("/posts/<int:post_id>/edit", methods=["POST"])
def handle_post_edit(post_id):
    """ Handle editing of post by
    - 
    - redirect back to post """

    # get form contents
    title = request.form["title"]
    content = request.form["content"]
    post = Post.query.get(post_id)

    # update fields
    post.title = title
    post.content = content

    #first deleted related entries, add new tags into posts_tags
    #    PostTag.query.filter(...).delete()

    for entry in post.entries:
        db.session.delete(entry)
        db.session.commit()


    for tag_id in request.form.getlist('tags'):
        new_post_tag_entry = PostTag(post_id=post.id, tag_id=tag_id)
        db.session.add(new_post_tag_entry)
        db.session.commit()


    flash('Post edited', 'success')
    return redirect(f'/posts/{post_id}')

@app.route("/posts/<int:post_id>/delete", methods=["POST"])
def delete_post(post_id):
    """ Delete post and returns to user page """

    post = Post.query.get(post_id)
    entries = post.entries
    user_id = post.user.id

    for entry in entries:
        db.session.delete(entry)

    db.session.delete(post)
    db.session.commit()

    flash('Post deleted', 'danger')

    return redirect(f'/users/{user_id}')


# PART THREE!
@app.route("/tags")
def list_all_tags():
    """ Lists all tags, with links to the tag detail page. """
    tags = Tag.query.all()
    return render_template("show_all_tags.html", tags=tags)


@app.route("/tags/<int:tag_id>")
def show_tag_detail(tag_id):
    """ List posts correspnding to tag. """
    tag = Tag.query.get(tag_id)
    return render_template("show_tagged_posts.html", tag=tag)


@app.route("/tags/new")
def show_add_new_tag_form():
    """ Shows a form to add a new tag """
    return render_template("new_tag_form.html")


@app.route("/tags/new", methods=["POST"])
def handle_new_tag():
    """ Process add form, adds tag, and redirect to tag list. """
    new_tag_name = request.form['name']

    new_tag = Tag(name=new_tag_name)

    db.session.add(new_tag)
    db.session.commit()

    flash('Tag added', 'success')
    return redirect("/tags")


@app.route("/tags/<int:tag_id>/edit")
def show_edit_tag_form(tag_id):
    """ Show edit form for a tag. """
    tag = Tag.query.get(tag_id)
    return render_template('edit_tag.html', tag=tag)


@app.route("/tags/<int:tag_id>/edit", methods=["POST"])
def handle_tag_edit(tag_id):
    """ Process tag edits """
    tag = Tag.query.get(tag_id)
    tag.name = request.form['name']

    db.session.commit()

    flash('Tag edited', 'success')
    return redirect("/tags")


@app.route("/tags/<int:tag_id>/delete", methods=["POST"])
def delete_tag(tag_id):
    """ Delete selected tag and associated entries in join table (posts_tags) """
    # get selected tag
    tag_to_delete = Tag.query.get(tag_id)
    # get associated entries in posts_tags table
    entries_to_delete = tag_to_delete.entries

    for entry in entries_to_delete:
        db.session.delete(entry)

    db.session.delete(tag_to_delete)
    
    db.session.commit()

    flash("Tag deleted", "success")
    return redirect("/tags")


# when posting, get time zone and time
# datetime.timezone(datetime.timedelta(days=-1, seconds=61200), 'PDT')
# datetime.datetime.utcnow()

# get into SQL format
# SQL FORMAT IS:  2019-06-27 11:20:44.213257-07
# python formating is: time.strftime('%Y-%m-%d %H:%M:%S.%f-')

# find timezone offset example
# cet = pytz.timezone('CET')
# dt = datetime.datetime(2010, 10, 31, 2, 12, 30)
# offset = cet.utcoffset(dt)