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
        self.database_path = "postgres://{}/{}".format('postgres:Mashni@localhost:5433', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_retrive_categories(self):
        res = self.client().get('/categories')
        data=json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)
        self.assertEqual(len(data['categories']),6)   

    def test_retrive_questions(self):
        res = self.client().get('/questions')
        data=json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)
        self.assertEqual(len(data['questions']),10)
        self.assertEqual(data['total_questions'],19)
        self.assertEqual(len(data['categories']),6)   

    def test_delete_question(self):
        res = self.client().delete('/questions/10')
        data=json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)
    
    def test_new_question(self):
        res = self.client().post('/questions',json={
            'question': "Q1",
            'answer': 'answer1',
            'difficulty': 1,
            'category':1
        })
        data=json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)
        
    def test_search(self):
        res = self.client().post('/questions/search',json={
            'searchTerm': "1990"
        })
        data=json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)
        self.assertEqual(data['total_questions'],1)

    def retrive_questions_by_cagtegory(self):
        res = self.client().get('/categories/2/questions')
        data=json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)
        self.assertEqual(len(data['questions']),4)
    
    def test_satrt_quiz(self):
        res = self.client().post('/quizzes',json={
            'quiz_category':{
                'type': 'Art',
                'id': '2'
            },
            'previous_questions':{}
        })
        data=json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)
        self.assertEqual(len(data['questions']),4)
    

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()