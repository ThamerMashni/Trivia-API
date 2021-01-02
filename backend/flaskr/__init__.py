import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS 
import random
import json
import sys

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_questions(request,selection):
  page = request.args.get('page',1, type=int)
  start = (page -1) * QUESTIONS_PER_PAGE
  end = start + QUESTIONS_PER_PAGE

  questions = [question.format() for question in selection]
  current_questions = questions[start:end]

  return current_questions

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app)



  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  '''
  @: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
 
    response.headers.add('Access-Control-Allow-Origin','*')
    response.headers.add('Access-Control-Allow-Headers','Content-Type')
    response.headers.add('Access-Control-Allow-Methods','GET, POST, PATCH, DELETE')
    return response    

  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  
  @app.route('/categories', methods=['GET'])
  def retrive_categories():
    try:
      categories = Category.query.order_by(Category.id).all()

      formated_categories = {}
      for category in categories:
        formated_categories[category.id] = category.type
      
      return jsonify({
        'success': True,
        'categories':formated_categories,
        })
    except:
      abort(404)


  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  
  @app.route('/questions', methods=['GET'])
  def retrive_questions():
    try:
      selection = Question.query.order_by(Question.id).all()
      current_questions = paginate_questions(request,selection)
      categories = Category.query.order_by(Category.id).all()
      
      formated_categories = {}
      for category in categories:
        formated_categories[category.id] = category.type
      
      if len(current_questions)== 0 :
        abort(404)

      return jsonify({
        'success': True,
        'questions': current_questions,
        'total_questions': len(selection),
        'categories': formated_categories,
        'current_category': ''
        })
    except:
      abort(404)



  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    try:
      question = Question.query.filter(Question.id == question_id).one_or_none()
      question.delete()

      return jsonify({
        "success": True,
        "deleted": question_id
      })
    except:
      abort(404)
  
 
  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  @app.route('/questions', methods=['POST'])
  def new_question():
    try:
      form = request.get_json()
      question = form.get('question')
      answer = form.get('answer')
      difficulty = form.get('difficulty')
      category = form.get('category')

      if difficulty is None or  question is None or answer is None or category is None :
        abort(422)

      newQuestion = Question(question=question, answer=answer, difficulty=difficulty, category=category)
      newQuestion.insert()
      newQuestion.question
      return jsonify({
        'success': True,
        'newQuestion':newQuestion.question
      })
    except:
      print(sys.exc_info)
      abort(422)


  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  @app.route('/questions/search', methods=['POST'])
  def search():

    try:
      form = request.get_json()
      term = form.get('searchTerm')
      if(term is ''):
        abort(404)

      selection = Question.query.filter(Question.question.ilike('%{}%'.format(term))).all()
      current_questions = paginate_questions(request, selection)


      return jsonify({
        "success": True,
        "questions": current_questions,
        "total_questions": len(selection),
      })
    except:
      print(sys.exc_info)
      abort(404)

  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<int:category_id>/questions', methods=['GET'])
  def retrive_questions_by_cagtegory(category_id):
    try:
      selection = Question.query.filter(Question.category == category_id).all()
      current_questions = paginate_questions(request,selection)

      if(len(current_questions)==0):
        abort(404)

      return jsonify({
        'success': True,
        'questions': current_questions,
        'total_questions': len(selection),
      })
    except:
      print(sys.exc_info())
      abort(404)
      

  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  @app.route('/quizzes', methods=['POST'])
  def satrt_quiz():
    try:
      body = request.get_json()
      category = body.get('quiz_category')
      previous_questions = body.get('previous_questions')
      
      if category['type'] == 'click':
        available_questions = Question.query.filter(
          Question.id.notin_((previous_questions))).all()
      else:
        available_questions = Question.query.filter_by(
          category=category['id']).filter(Question.id.notin_((previous_questions))).all()
              
      new_question = available_questions[random.randrange(0, len(available_questions))].format() if len(available_questions) > 0 else None

      return jsonify({
        'success': True,
        'question': new_question,
        'category':  new_question['category']
      })
    except:
      abort(422)
      

  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      "success": False,
      "error": 404,
      "message": "resource not found"
    }), 404

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      "success": False,
      "error": 422,
      "message": "unprocessable"
    }), 422

  @app.errorhandler(405)
  def not_allowed(error):
    return jsonify({
      "success": False,
      "error": 405,
      "message": "Method not allowed"
    }), 405
  
  return app

    