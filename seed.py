from models import User, db
from app import app

db.create_all()

User.query.delete()

# Add stuff
chantal = User(first_name="Chantal", last_name="Yuen")
joanne = User(first_name="Joanne", last_name="Wu")

db.session.add(chantal)
db.session.add(joanne)

db.session.commit()