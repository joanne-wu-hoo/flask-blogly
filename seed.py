from models import User, Post, Tag, PostTag, db
from app import app

db.drop_all()
db.create_all()

# User.query.delete()
# Post.query.delete()

# Add fake users
chantal = User(first_name="Chantal", last_name="Yuen")
joanne = User(first_name="Joanne", last_name="Wu")


db.session.add(chantal)
db.session.add(joanne)

db.session.commit()

# Add posts
first_post = Post(title="Cat Post!", content="Hello Cat", user_id="1")
second_post = Post(title="Dog Post!", content="Hello Dog", user_id="1")

db.session.add(first_post)
db.session.add(second_post)

db.session.commit()

# Add tags
cat = Tag(name="Cat")
dog = Tag(name="Dog")

db.session.add(cat)
db.session.add(dog)

db.session.commit()


# Add tags to posts
post_tag_1 = PostTag(post_id=1, tag_id=1)
post_tag_2 = PostTag(post_id=2, tag_id=2)

db.session.add(post_tag_1)
db.session.add(post_tag_2)

db.session.commit()