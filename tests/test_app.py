import os
import unittest

os.environ["TESTING"] = "true"

from app import app, TimelinePost

class TestApp(unittest.TestCase):
    def setUp(self):
        os.environ["TESTING"] = "true"
        self.app = app.test_client()
        TimelinePost.create_table()

    def tearDown(self):
        TimelinePost.drop_table()
        os.environ.pop("TESTING", None)

    def test_home_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_hobbies_page(self):
        response = self.app.get('/hobbies')
        self.assertEqual(response.status_code, 200)

    def test_timeline_page(self):
        response = self.app.get('/timeline')
        self.assertEqual(response.status_code, 200)

    def test_timeline_post_creation(self):
        test_data = {
            'name': 'Test User',
            'email': 'test@example.com',
            'content': 'This is a test post'
        }
        
        response = self.app.post('/api/timeline_post', data=test_data)
        self.assertEqual(response.status_code, 200)
        
        posts = TimelinePost.select()
        self.assertEqual(len(posts), 1)
        self.assertEqual(posts[0].name, test_data['name'])
        self.assertEqual(posts[0].email, test_data['email'])
        self.assertEqual(posts[0].content, test_data['content'])

    def test_timeline_post_retrieval(self):
        post1 = TimelinePost.create(
            name='User 1',
            email='user1@example.com',
            content='First test post'
        )
        post2 = TimelinePost.create(
            name='User 2',
            email='user2@example.com',
            content='Second test post'
        )
        
        response = self.app.get('/api/timeline_post')
        self.assertEqual(response.status_code, 200)
        
        import json
        data = json.loads(response.data)
        
        self.assertIn('timeline_posts', data)
        self.assertEqual(len(data['timeline_posts']), 2)
        
        posts = data['timeline_posts']
        names = [post['name'] for post in posts]
        self.assertIn('User 1', names)
        self.assertIn('User 2', names)

    def test_malformed_timeline_post(self):
        response = self.app.post("/api/timeline_post", data={"email": "john@example.com", "content": "Hello world, I'm John!"})
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid name" in html

        response = self.app.post("/api/timeline_post", data={"name": "John Doe", "email": "john@example.com", "content": ""})
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid content" in html

        response = self.app.post("/api/timeline_post", data={"name": "John Doe", "email": "not-an-email", "content": "Hello world, I'm John!"})
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid email" in html

if __name__ == '__main__':
    unittest.main() 