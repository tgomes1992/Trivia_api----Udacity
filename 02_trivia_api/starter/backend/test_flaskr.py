import os
import unittest
import json
from flask import jsonify
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
        print ("Test completed")

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_category(self):
        res = self.client().get('/category')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)


    def test_get_category_error(self):
        res = self.client().get('/categorys')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
      

    def test_get_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)


    def test_get_questions_error(self):
        res = self.client().get('/question')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        

    def test_search_questions(self):
        question_test = "president"
        res = self.client().post('/searchquestion',json=question_test)
        data = json.loads(res.data)
        self.assertTrue(len(data['questions'])==1)
        self.assertEqual(res.status_code, 200)

    def test_search_questions_error(self):
        question_test = "kkkkkkkkkk"
        res = self.client().post('/searchquestion', json=question_test)
        data = json.loads(res.data)
        self.assertEqual(len(data['questions']),0)
        self.assertEqual(res.status_code, 200)
  
        
        

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()