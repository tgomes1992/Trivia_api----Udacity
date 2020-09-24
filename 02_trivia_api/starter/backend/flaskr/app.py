import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


  # create and configure the app
app = Flask(__name__)
setup_db(app)

cors = CORS(app) 


@app.route('/')
def home():
  return jsonify("hello word")

@app.route('/db')
def dbteste():
  questions = Question.query.all()
  lista = []
  for i in questions:
    lista.append(i.question)
  return jsonify(lista)


  # '''
  # @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  # '''

  # '''
  # @TODO: Use the after_request decorator to set Access-Control-Allow
  # '''

@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
  return response



  # '''
  # @TODO: 
  # Create an endpoint to handle GET requests 
  # for all available categories.
  # '''

@app.route("/category", methods=['GET'])
def get_categories():
  categories  = Category.query.all()
  format_category = [category.format() for category in categories]
  lista = []
  for i in categories:
    lista.append(i.type)
  return jsonify({'category':lista})
  # '''
  # @TODO: 
  # Create an endpoint to handle GET requests for questions, 
  # including pagination (every 10 questions). 
  # This endpoint should return a list of questions, 
  # number of total questions, current category, categories. 

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
    ndict["category"] = i.category-1
    ndict["difficulty"] = i.difficulty
    ndict["id"] = i.id
    ndict["question"] =i.question
    lista.append(ndict)
  

  return jsonify({
    'questions': format_Question[start:end],
    'totalQuestion': len(format_Question),
    'categories': cat,
    })


  # TEST: At this point, when you start the application
  # you should see questions and categories generated,
  # ten questions per page and pagination at the bottom of the screen for three pages.
  # Clicking on the page numbers should update the questions. 
  # '''

  # '''

@app.route("/questions/<int:id>/delete",methods=['DELETE'])
def delete_questions(id):
  question  = Question.query.get(id)
  Question.delete(question)
  return jsonify({
    'success':True
  })


  # @TODO: 

@app.route("/add/questions",methods=['POST'])
def add_questions():
  resposta = request.get_json()
  cat = int(resposta['category'])
  question = Question(question=resposta['question'],
                      answer=resposta['answer'],
                      category= cat+1,
                      difficulty=resposta['difficulty'])
  Question.insert(question)
  return jsonify({
    'success':True
  })






  # Create an endpoint to POST a new question, 
  # which will require the question and answer text, 
  # category, and difficulty score.

  # TEST: When you submit a question on the "Add" tab, 
  # the form will clear and the question will appear at the end of the last page
  # of the questions list in the "List" tab.  
  # '''

  # '''
  # @TODO: 
  # Create a POST endpoint to get questions based on a search term. 
  # It should return any questions for whom the search term 
  # is a substring of the question. 

  # TEST: Search by any phrase. The questions list will update to include 
  # only question that include that string within their question. 
  # Try using the word "title" to start. 
  # '''

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
      ndict['category'] = i.category-1
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
  questions  = Question.query.filter_by(category=id+1)
  format_Question = [question.format() for question in questions]
  current_categorie  = Category.query.get(id+1)
  ques = []

  for i in questions:
    ques.append(i.question)

  return jsonify({
    'questions': format_Question,
    'totalQuestion': len(ques),
    'currentCategory': current_categorie.type
  })



  # '''
  # @TODO: 
  # Create a POST endpoint to get questions to play the quiz. 
  # This endpoint should take category and previous question parameters 
  # and return a random questions within the given category, 
  # if provided, and that is not one of the previous questions. 

  # TEST: In the "Play" tab, after a user selects "All" or a category,
  # one question at a time is displayed, the user is allowed to answer
  # and shown whether they were correct or not. 
  # '''

  # '''

  # @TODO: 
  # Create error handlers for all expected errors 
  # including 404 and 422. 
  # '''


@app.route("/quizzes", methods=['POST'])
def play_game():
  resposta = request.get_json()
  category = int(resposta['quiz_category']['id']) + 1
  if resposta['quiz_category']['type'] == 'click':
    question = Question.query.all()
  else:
    question = Question.query.filter_by(category=category)
  format_Question = [question.format() for question in question]
  numero = random.randrange(0,len(format_Question))
  print(resposta)
  return jsonify({
    'question' :  format_Question[numero]
  })

app.run(debug=True)



