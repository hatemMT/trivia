# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.8

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```
or with the Migration tool 
```bash
flask db upgrade
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 


## Endpoints Documentation:
- GET '/questions[?page=n][&searchTerm=searchterm]' →
Returns all the questions available in pages of 10 items each and all the categories available 
and with optional filtering by question name (case insensitive)

    `curl http://localhost:5000/questions?page=1&seachTerm=somequestion`
    
    - the page query parameter is optional if not set then returns page number 1
    - the searchTerm is optional and if not provided all the items returned
    - The response will be like that with status code `200 OK` :
    ```json
      {
      "questions": [{"id": 1,
                     "question": "Sample question",
                     "answer": "Sample answer",
                     "difficulty": 5,
                     "category": 1
                     }],
      "total_questions": 1,
      "categories": {"1": "sports"},
      "current_category": null
      }
    ```
- POST '/questions' → Add new question to the list

    ```
    curl -X POST http://localhost:5000/questions` -H 'Content-Type: application/json' \
                                                -d '{"question":"Sample questions ?", \
                                                "answer":"Sample answer", \
                                                "difficulty": 5, \
                                                "category": 1 \
                                                    }'
    
    
    ```
    If the data is valid then the response will be json like that with status code `201 CREATED`  :
    ```json
    {
    "id": 1,
    "question": "Sample question",
    "answer": "Sample answer",
    "difficulty": 5,
    "category": 1
    }
    ```
    If the data is invalid then bad request retuned `400 BAD REQUEST` with body like that :
    ```json
        {
          "message": "Validation Error, Please check the data"
        }   
     ``` 
- GET `/categories/<cat_id>/questions` → Fetch the questions in a specific category

    ```bash
        curl http://localhost:5000/categories/1/questions 
    ``` 
    If the category exitst then the sample response will be `200 OK` with body :
    ```json
    {
      "questions": [{
                    "id": 1,
                    "question": "...",
                    "answer": "...",
                    "category": 1,
                    "difficulty": 5
                    }
                ],
      "total_questions": 20,
      "current_category": 1
    }  
    ```
   *Questions list is trimmed for simplicity*
    
    Else if the category is not found the `400 BAD REQUEST` returned with body 
    ```json
      {
       "success": false,
       "error": 400,
       "message": "Bad request"
      }
    ```
- DELETE '/questions/<qid>' → Delete the question with id specified in path param
        sample request :
                ```bash
                    curl -X DELETE http://localhost:5000/questions/1
                ``` 
        sample response : `200 OK` with empty body


- POST '/quizzes' → Fetch the next random question for quiz 
    depending on the passed data which is :

    - previous questions ids
    - the category of questions specified (if `0` is provided as category id then it indicates all categories)
    
    sample request command :
    ```bash
        curl -X POST http://localhost:5000/quizzes -H 'Content-Type: application/json' \
                -d '{    \
                        "previous_questions": [7,3,6], \
                        "quiz_category" :{"id": 0} \
                    }'
    ```
    Sample response if there is still questions matching criteria : 
    ```json
      {
        "id": 8,
        "question": "question text",
        "answer": "anser text",
        "category": 5,
        "difficulty": 4
      } 
     ```
     if there is no more questions then `404 NOT FOUND` response returns with body :
     ```json
        {"message": "Questions finished !"}
     ```


## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
