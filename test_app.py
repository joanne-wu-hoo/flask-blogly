from unittest import TestCase
from app import app
from models import db, connect_db, User, Post

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_testing'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)
db.create_all()

class FlaskTest(TestCase):

    # PART ONE TESTS
    def setUp(self):
        Post.query.delete()
        User.query.delete()

        self.client = app.test_client()
        app.config['TESTING'] = True
        new_user = User(first_name="Jane", last_name="Doe")

        db.session.add(new_user)
        db.session.commit()

        self.user_id = new_user.id

        new_post = Post(title="Hello", content="World", user_id=self.user_id)

        db.session.add(new_post)
        db.session.commit()       


    def test_home_redirect(self):
        """ test that /
        - redirects to page that contains b'<h1>Users</h1>'
        - has status code 200 """

        result = self.client.get('/', follow_redirects=True)

        self.assertEqual(result.status_code, 200)
        self.assertIn(b'<h1>Users</h1>', result.data)


    def test_user_list(self):
        """ test that /users 
        - shows b'<h1>Users</h1>'
        - has status code 200 """

        result = self.client.get('/users')

        self.assertEqual(result.status_code, 200)
        self.assertIn(b'<h1>Users</h1>', result.data)


    def test_new_user_form(self):
        """  test that /users/new
        - displays b'<button class='btn btn-success'>Add</button>
        - has status code 200 """
        
        result = self.client.get('/users/new')

        self.assertEqual(result.status_code, 200)
        self.assertIn(b"Add</button>", result.data)

    
    def test_add_new_user(self):
        """ test user form submission by checking that /users, method=post 
        # - adds an entry to database
        # - redirects to page with text "User added!" """

        result = self.client.post('/users', data={ 'first_name': 'John',
                                              'last_name': 'Doe',
                                              'image_url': None },
                                              follow_redirects=True)

        self.assertEqual(db.session.query(User).count(), 2)
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'User added!', result.data)
        

    def test_user_profile(self):
        """ test that /users/<user_id> 
        - shows text <h1>{{ user.first_name }} {{ user.last_name }}</h1>
        - has status code 200 """

        user = User.query.filter(User.first_name == "Jane").one()
        result = self.client.get(f'/users/{user.id}')

        self.assertEqual(result.status_code, 200)
        self.assertIn(b'<h1>Jane Doe</h1>', result.data)


    def test_edit_functionality(self):
        """ test that edit functionality works """
        user = User.query.filter(User.first_name == "Jane").one()

        result = self.client.post(f'/users/{user.id}/edit', data={"first_name": "Santa",
                                                                  "last_name": "Claus",
                                                                  "image_url": user.image_url},
                                                            follow_redirects=True)

        self.assertEqual(result.status_code, 200)
        self.assertIn(b'Santa Claus', result.data)   


    def test_delete_user(self):
        """ test that user deletion functionality
        - removes user
        - redirects to page with text "deleted" """

        result = self.client.post(f'/users/{self.user_id}/delete', follow_redirects=True)
        
        self.assertEqual(db.session.query(User).count(), 0)
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'deleted', result.data)

    # PART TWO TESTS

    def test_add_post(self):
        """ test_add_post checks that
        - entry was made in post data table
        - redirect page has text 'Post added!' """ 
        
        result = self.client.post(f'/users/{self.user_id}/posts', 
                                 data={"title": "Bye",
                                       "content": "Planet",
                                       "user_id": self.user_id},
                                 follow_redirects=True)

        self.assertEqual(db.session.query(Post).count(), 2)
        titles = [p.title for p in Post.query.all()]
        self.assertEqual(titles, ['Hello', 'Bye'])
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'Post added!', result.data)

    def test_edit_post(self):
        """ test_edit_post checks that
        - requested edits were made """
        
        post = Post.query.first()
        
        result = self.client.post(f'/posts/{post.id}/edit', data={"title": "Good",
                                                                  "content": "Morning"},
                                                            follow_redirects=True)

        self.assertEqual(result.status_code, 200)
        self.assertIn(b'Post edited', result.data)   

    def test_delete_post(self):
        """ test_delete_post checks that
        - entry was deleted in post data table
        - redirect page has text 'Post deleted' """

        post = Post.query.first()
        result = self.client.post(f'/posts/{post.id}/delete', follow_redirects=True)

        self.assertEqual(db.session.query(Post).count(), 0)
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'Post deleted', result.data)
    
    # test_new_post_form checks that 
    # - form was correctly rendered

    # test_show_post checks that
    # - post was correctly rendered

    # test_show_edit_post_form checks that
    # - edit form was correctly rendered







