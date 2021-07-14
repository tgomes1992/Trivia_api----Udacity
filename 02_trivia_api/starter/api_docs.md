# Trivia API - Documentation

## Intro

This is the summary of the TRIVIA API documentation , a API that allow the user to play a very simple game , a Trivia Game , searching , adding and choosing questions in a random  way. 

This documentation regards the API not the frontend itself, that is a free choice o every developer and this documentation is made for development purposes , not for deployment

## Installation

 - Using your command line interface(CLI) run the following command 

> pip install -r requirements.txt 
	This command will allow  the user to install all project dependencies

	After installation the users will be able to start making get and post requests to the database


## Endpoints -  Detailment

### /category - Allowed methods =['GET']
This endpoint allows the user to get all the given categories

### /add/questions - Allowed methods =['POST']
This endpoint allows the user to get to create new questions in the DATABASE

### /questions - Allowed methods =['POST']
This endpoint allows the user to get all the given questions

### /questions/<int:id>/delete - Allowed methods =['DELETE']
This endpoint allows the user to delete a given question,based on the id

### /searchquestion - Allowed methods =['POST']
This endpoint allows the user to search question , the data to be posted needs to be in the json format

### /categories/<int:id>/questions - Allowed methods =['POST']
This endpoint allows the user to search question , by a gien category id

### /quizzes - Allowed methods =['POST']
This endpoint allows the user to start to play the game, the answer needs to be sent in the JSON FORMAT

# Thank You !
Developed By Thiago Gomes

