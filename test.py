from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle
from json import loads

app.config['TESTING'] = True

class FlaskTests(TestCase):

    # TODO -- write tests for every view function / feature!
    def test_homepage(self):
        """Testing home route for status code and included html"""
        with app.test_client() as client:
            res = client.get('/')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<form href="/" id="word-form">', html)

    def test_guess(self):
        """Testing requests to guess route"""
        with app.test_client() as client:
            res = client.get('/guess?word=pasidfjapsdoi')
            text = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('not-word', text)

            res = client.get('/guess?word=thyroparathyroidectomize')
            text = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('not-on-board', text)

            # res = client.get('/guess?word=slow')
            # text = res.get_data(as_text=True)
            # self.assertEqual(res.status_code, 200)
            # self.assertIn('ok', text)
        
    def test_game_over(self):
        """Testing high score and games played counting"""
        with app.test_client() as client:
            res = client.get('/game-over?score=15')
            data = loads(res.get_data(as_text=True))
            self.assertEqual(data['new_high_score'], True)
            self.assertEqual(data['games_played'], 1)

            res = client.get('/game-over?score=15')
            data = loads(res.get_data(as_text=True))
            self.assertEqual(data['new_high_score'], False)
            self.assertEqual(data['games_played'], 2)