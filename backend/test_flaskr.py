import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_categories_success(self):
        res = self.client().get('/categories')
        self.assertEqual(res.status_code, 200)

    def test_get_questions_success(self):
        res = self.client().get('/questions')
        self.assertEqual(res.status_code, 200)

    def test_get_questions_paginated_success(self):
        res = self.client().get('/questions?page=1')
        self.assertEqual(res.status_code, 200)

    def test_get_questions_no_resource_found(self):
        res = self.client().get('/questions?page=100')
        self.assertEqual(res.status_code, 404)

    def test_delete_question_by_id_success(self):
        res = self.client().delete('/questions/2')
        self.assertEqual(res.status_code, 200)

    def test_delete_question_by_id_id_not_exist(self):
        res = self.client().delete('/questions/1')
        self.assertEqual(res.status_code, 422)

    def test_submit_question_success(self):
        request = {
            "question": "What is my name?",
            "answer": "WLIU",
            "category": 1,
            "difficulty": 5
        }
        res = self.client().post('/questions', 
                                 data=json.dumps(request),
                                 content_type='application/json')
        self.assertEqual(res.status_code, 200)

    def test_submit_question_missing_field(self):
        request = {
            "question": "What is your name?",
            "answer": "XXX",
            "difficulty": 1
        }
        res = self.client().post('/questions', 
                                 data=json.dumps(request),
                                 content_type='application/json')
        self.assertEqual(res.status_code, 400)

    def test_search_questions_success(self):
        request = {
            "searchTerm": "What"
        }
        res = self.client().post('/questions/search', 
                                 data=json.dumps(request),
                                 content_type='application/json')
        self.assertEqual(res.status_code, 200)

    def test_search_questions_no_results(self):
        request = {
            "searchTerm": "xxxxxxxxxxx"
        }
        res = self.client().post('/questions/search', 
                                 data=json.dumps(request),
                                 content_type='application/json')
        self.assertEqual(res.status_code, 404)

    def test_get_questions_by_category_success(self):
        res = self.client().get('/categories/1/questions')
        self.assertEqual(res.status_code, 200)

    def test_get_questions_by_category_no_results(self):
        res = self.client().get('/categories/100/questions')
        self.assertEqual(res.status_code, 404)

    def test_play_quizzes_all_success(self):
        request = {
            "previous_questions": [],
            "quiz_category": {
                "id": 0,
                "type": "All"
            }
        }
        res = self.client().post('/quizzes',
                                 data=json.dumps(request),
                                 content_type='application/json')
        self.assertEqual(res.status_code, 200)

    def test_play_quizzes_category_1_success(self):
        request = {
            "previous_questions": [],
            "quiz_category": {
                "id": 1,
                "type": "Science"
            }
        }
        res = self.client().post('/quizzes',
                                 data=json.dumps(request),
                                 content_type='application/json')
        self.assertEqual(res.status_code, 200)

    def test_play_quizzes_category_1_last_question_success(self):
        request = {
            "previous_questions": [20, 21],
            "quiz_category": {
                "id": 1,
                "type": "Science"
            }
        }
        res = self.client().post('/quizzes',
                                 data=json.dumps(request),
                                 content_type='application/json')
        
        self.assertEqual(res.status_code, 200)
        self.assertTrue(res.get_json()['question'] is not None)

    def test_play_quizzes_category_1_no_question_left_success(self):
        request = {
            "previous_questions": [20, 21, 22],
            "quiz_category": {
                "id": 1,
                "type": "Science"
            }
        }
        res = self.client().post('/quizzes',
                                 data=json.dumps(request),
                                 content_type='application/json')

        self.assertEqual(res.status_code, 200)
        self.assertTrue(res.get_json()['question'] is None)

    def test_play_quizzes_category_bad_request(self):
        request = {
            "quiz_category": {
                "id": 1,
                "type": "Science"
            }
        }
        res = self.client().post('/quizzes',
                                 data=json.dumps(request),
                                 content_type='application/json')

        self.assertEqual(res.status_code, 400)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()