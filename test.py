from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle

app.config['TESTING'] = True

class FlaskTests(TestCase):

    # TODO -- write tests for every view function / feature!
    def test_homepage(self):
        with app.test_client() as client:
            res = client.get('/')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<form href="/" id="word-form">', html)

    def test_guess(self):
        with app.test_client() as client:
            res = client.post('/guess', args={'word': 'pasidfjapsdoi'})
            text = res.get_data(as_text=True)
            print(text)
            
            self.assertEqual(res.status_code, 200)