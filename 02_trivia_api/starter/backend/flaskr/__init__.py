import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from flaskr.models import setup_db, Question, Category



def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  cors = CORS(app) 
  
  QUESTIONS_PER_PAGE = 10

  @app.route('/')
  def home():
    return jsonify("hello word")
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  
  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
    return response

  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''

  @app.route("/category", methods=['GET'])
  def get_categories():
    categories  = Category.query.all()
    format_category = [category.format() for category in categories]
    lista = []
    for i in categories:
      lista.append(i.type)
    return jsonify({'category':lista})


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
  @app.route("/questions",methods=['GET'])
  def get_questions():
    page = request.args.get('page', 1 , type=int)
    start = (page-1)
    end = QUESTIONS_PER_PAGE
    questions  = Question.query.all()
    format_Question = [question.format() for question in questions]
    category = Category.query.all()
    format_category = [categories.format() for categories in category]
    cat = [] 
    lista = []
    for i in category:
      cat.append(i.type)

    for i in questions: 
      ndict = {}
      ndict["answer"] = i.answer
      categoria =  Category.query.get(i.category)
      ndict["category"] = i.category
      ndict["difficulty"] = i.difficulty
      ndict["id"] = i.id
      ndict["question"] =i.question
      lista.append(ndict)   

    return jsonify({
      'questions': format_Question,
      'totalQuestion': len(format_Question),
      'categories': cat,
      })


  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''

  @app.route("/questions/<int:id>/delete",methods=['DELETE'])
  def delete_questions(id):
    question  = Question.query.get(id)
    Question.delete(question)
    return jsonify({
    'success':True
  })

  @app.route("/add/questions",methods=['POST'])
  def add_questions():
    resposta = request.get_json()
    print(resposta)
    cat = int(resposta['category'])
    print(cat)
    question = Question(question=resposta['question'],
                        answer=resposta['answer'],
                        category= cat+1,
                        difficulty=resposta['difficulty'])
    Question.insert(question)
    return jsonify({
      'success':True
    })


  

  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''

  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''

  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''


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
  @app.route("/searchquestion", methods=['POST'])
  def search():
    resposta = request.get_json()
    comp = resposta.lower()
    ## questions  
    totQuestions = []
    question = Question.query.all()
    for i in question:  
      ndict = {}
      if comp in i.question.lower():
        ndict['question'] = i.question
        ndict['category'] = i.category
        ndict['difficulty'] = i.difficulty
        ndict['answer'] = i.answer
        totQuestions.append(ndict)
    ## totalquestions
    ## currentcategory
    return jsonify({
      'questions': totQuestions,
      'totalQuestions': len(totQuestions),
    })
  
  @app.route("/categories/<int:id>/questions", methods=['GET'])
  def get_questions_categories(id): 
    questions  = Question.query.filter_by(category=str(id+1))
    format_Question = [question.format() for question in questions]
    current_categorie  = Category.query.get(int(id+1))
    ques = []

    for i in questions:
      ques.append(i.question)

    return jsonify({
      'questions': format_Question,
      'totalQuestion': len(ques),
      'category': current_categorie.type
    })

  @app.route("/quizzes", methods=['POST'])
  def play_game():
    resposta = request.get_json()
    previous=resposta['previous_questions']
    category = int(resposta['quiz_category']['id'])+1
    if resposta['quiz_category']['type'] == 'click':
      question = Question.query.all()
    else:
      question = Question.query.filter_by(category=str(category))
    if len(previous)<=5:
      format_Question = [question.format() for question in question]
      numero = random.randrange(0,len(format_Question))
      print(numero)
      actual_question = format_Question[numero]
      if actual_question['id'] in previous:
        actual_question = ""
    return jsonify({
      'question' :  actual_question
    })

  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422.
  '''
  @app.errorhandler(404)
  def page_not_found(e):
    # note that we set the 404 status explicitly
    return jsonify('BAD request!'), 404

  @app.errorhandler(422)
  def other_error(e):
    # note that we set the 404 status explicitly
    return jsonify('Empty page!'), 404
    
  return app











