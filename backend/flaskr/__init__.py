import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category
import util as util
from exceptions import *

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  cors = CORS(app, resources={r"/*": {"origins": "*"}})

  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
    return response

  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories')
  def get_categories():
    try:
      categories = util.get_categories(formatted=True)

      if not categories:
        raise ResourceNotFound

      return jsonify({
        "success": True,
        "categories": categories,
        "total_categories": len(categories)
        })

    except ResourceNotFound:
      abort(404)

    except Exception:
      abort(500)

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
  @app.route('/questions')
  def get_paginated_questions():
    try:
      categories = util.get_categories(formatted=True)
      current_category = request.args.get('cateogry')

      questions = util.get_questions(formatted=False)
      page = request.args.get('page', 1, type=int)
      start = QUESTIONS_PER_PAGE * (page - 1)
      end = start + QUESTIONS_PER_PAGE

      questions_on_selected_page = [question.format() for question in questions[start: end]]
      
      if not questions_on_selected_page:
        raise ResourceNotFound

      return jsonify({
        "success": True,
        "questions": questions_on_selected_page,
        "total_questions": len(questions),
        "categories": categories,
        "current_category": current_category
        })

    except ResourceNotFound:
      abort(404)

    except Exception:
      abort(500)


  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<question_id>', methods=['DELETE'])
  def delete_question(question_id):
    try:
      selected_question = Question.query.get(question_id)
      selected_question.delete()

      return jsonify({
        "success": True
        })

    except Exception:
      abort(422)

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
  def submit_question():
    try:
      
      try:
        body = request.get_json()
        question_str = body['question']
        answer_str = body['answer']
        category_str = body['category']
        difficulty_str = body['difficulty']
      except:
        raise BadRequest

      new_question = Question(question = question_str,
                              answer = answer_str,
                              category = category_str,
                              difficulty = difficulty_str)
      new_question.insert()
      
      return jsonify({
        "success": True
        })

    except BadRequest:
      abort(400)

    except Exception:
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
  def search_questions():
    try:

      try:
        body = request.get_json()
        search_term = body['searchTerm']
        current_category = body.get('currentCategory')
      except:
        raise BadRequest

      search = "%{}%".format(search_term.lower())

      filtered_questions = Question.query.filter(Question.question.ilike(search)).order_by('id').all()

      if not filtered_questions:
        raise ResourceNotFound

      formatted_questions = [question.format() for question in filtered_questions]
      
      return jsonify({
        "questions": formatted_questions,
        "total_questions": len(filtered_questions),
        "current_category": current_category
        })

    except BadRequest:
      abort(400)

    except ResourceNotFound:
      abort(404)

    except Exception:
      abort(500)

  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<category_id>/questions')
  def get_questions_by_category(category_id):
    try:
      questions = util.get_questions(category_id=category_id, formatted=True)

      if not questions:
        raise ResourceNotFound

      return jsonify({
        "success": True,
        "questions": questions,
        "total_questions": len(questions),
        "current_category": category_id
        })

    except ResourceNotFound:
      abort(404)

    except Exception:
      abort(500)

  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random question within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  @app.route('/quizzes', methods=['POST'])
  def play_quizzes():
    try:
  
      try:
        body = request.get_json()
        previous_questions_id = body['previous_questions']
        quiz_category = body['quiz_category']
        quiz_category_id = quiz_category['id']
      except:
        raise BadRequest
  
      questions = util.get_questions(category_id=quiz_category_id, formatted=False)

      unanswered_questions = [question for question in questions 
                              if question.id not in previous_questions_id]

      if not unanswered_questions:
        rand_question = None
      else:
        rand_question = random.choice(unanswered_questions).format()

      return jsonify({
        "success": True,
        "question": rand_question
        })

    except BadRequest:
      abort(400)

    except Exception:
      abort(500)
      

  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(400)
  def bad_request(error):
    return jsonify(error_messages["BadRequest"]), 400

  @app.errorhandler(404)
  def resource_not_found(error):
    return jsonify(error_messages["ResourceNotFound"]), 404

  @app.errorhandler(422)
  def unprocessable_entity(error):
    return jsonify(error_messages["UnprocessableEntity"]), 422

  @app.errorhandler(500)
  def internal_error(error):
    return jsonify(error_messages["InternalError"]), 500
  
  return app

    