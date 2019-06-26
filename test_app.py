from unittest import TestCase
from app import app
from models import User

class FlaskTest(TestCase):

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_testing'
        # create testing database 
        # create entries


    def tearDown(self):
        # delete records

    # test / redirect
    # - check for b'<h1>Users</h1><ul>
    # - check status code is 200

    # test /users 
    # - shows b'<h1>Users</h1><ul>

    # test /users/new
    # - displays b'<button class='btn btn-success'>Add</button>
    # - status code is 200

    # test /users, method=post (when new user form is submitted)
    # - check that an entry was added to database
    # - check for redirect, page should have text "User added!"

    # test user profile
    # - show text <h1>{{ user.first_name }} {{ user.last_name }}</h1>
    # - status code 200

    # test that edit page renders correctly
    # - look for text b'<h1>Edit a user</h1>

    # test that edit functionality works

    # test user deletion functionality
    # - check that an entry was removed
    # - check for redirect, page should have text "deleted"

