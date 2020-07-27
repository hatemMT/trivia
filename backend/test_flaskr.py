import json
import random
import unittest

from flaskr import create_app
from flaskr.models import setup_db, db, Category

DATABASE_HOST = '192.168.99.100'
DATABASE_PORT = '5432'
TRIVIA_DATABASE_NAME = "trivia_test"
DATABASE_USER_PASSWORD = "admin:secret"

HOST = 'http://localhost:5000'

VALID_QUESTION = {
    "question": "Question 1",
    "answer": "Answer 1",
    "difficulty": 5,
    "category": 1
}

INVALID_QUESTION = {}


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia endpoint's tests"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.database_path = f"postgresql://{DATABASE_USER_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{TRIVIA_DATABASE_NAME}"  # .format(f'{DATABASE_HOST}:{DATABASE_PORT}',
        #     TRIVIA_DATABASE_NAME)
        setup_db(self.app, self.database_path)
        self.db = db
        self.db.create_all()  # Create the schema
        self.client = self.app.test_client()  # initialize the http client

    def tearDown(self):
        self.db.drop_all()  # Drop the schema

    def test_validNewQuestionRequest_shouldBePersisted(self):
        # insert category
        self.create_new_category("sports")
        response = self.create_new_question(VALID_QUESTION)
        self.assertEqual(201, response.status_code)
        self.assertEqual(VALID_QUESTION["question"], response.json["question"])
        self.assertEqual(VALID_QUESTION["difficulty"], response.json["difficulty"])
        self.assertEqual(VALID_QUESTION["category"], response.json["category"])

    def test_invalidNewQuestionRequest_shouldReturn400(self):
        response = self.create_new_question(INVALID_QUESTION)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['message'], 'Validation Error, Please check the data')

    def test_questionsQueryWithoutPageSpecified_firstPageReturned(self):
        self.create_new_category("sports")
        random_questions = [self.create_new_question(self.generateQuestionData(i)).json for i in range(1, 21)]
        # {'categories': {}, 'current_category': None, 'questions': [], 'total_questions': 0}
        question_response = self.queryQuestions()
        self.assertEqual(random_questions[0:10], question_response.json['questions'])

    def test_questionsQueryWithPageSpecified_correctPageReturned(self):
        self.create_new_category("sports")
        random_questions = [self.create_new_question(self.generateQuestionData(i)).json for i in range(1, 21)]
        # {'categories': {}, 'current_category': None, 'questions': [], 'total_questions': 0}
        question_response = self.queryQuestions(2)
        self.assertEqual(random_questions[10:20], question_response.json['questions'])

    def test_questionByCategoryQuery_thenQuestionsReturned(self):
        sport_category = self.create_new_category("sports")
        sport_questions = [self.create_new_question(self.generateQuestionData(i, sport_category.id)).json
                           for i in range(1, 6)]
        education_category = self.create_new_category("education")
        education_questions = [self.create_new_question(self.generateQuestionData(i, education_category.id)).json
                               for i in range(1, 6)]
        sport_response = self.questions_by_category(sport_category.id)
        education_response = self.questions_by_category(education_category.id)

        self.assertEqual(sport_questions, sport_response.json['questions'])
        self.assertEqual(education_questions, education_response.json['questions'])

    def test_givenQuizzesRequestForAnyCategory_thenAValidQuestionShouldReturn(self):
        sport_category = self.create_new_category("sports")
        sport_questions = [self.create_new_question(self.generateQuestionData(1, sport_category.id)).json]
        education_category = self.create_new_category("education")
        education_questions = [self.create_new_question(self.generateQuestionData(2, education_category.id)).json]
        previous_questions = []
        quiz_category = 0  # For Any category
        quiz_question1_response = self.nextQuizQuestion(quiz_category, previous_questions)
        self.assertIn(quiz_question1_response.json, sport_questions + education_questions)
        previous_questions.append(quiz_question1_response.json['id'])
        quiz_question2_response = self.nextQuizQuestion(quiz_category, previous_questions)
        self.assertIn(quiz_question2_response.json, sport_questions + education_questions)

    def test_givenQuizzesRequestForSpecificCategory_OnlyQuestionsInCategoryReturns(self):
        sport_category = self.create_new_category("sports")
        sport_questions = [self.create_new_question(self.generateQuestionData(i, sport_category.id)).json
                           for i in range(1, 6)]
        education_category = self.create_new_category("education")
        education_questions = [self.create_new_question(self.generateQuestionData(i, education_category.id)).json
                               for i in range(1, 6)]
        previous_questions = []
        for _ in sport_questions:
            quiz_sport_question_response = self.nextQuizQuestion(sport_category.id, previous_questions)
            self.assertIn(quiz_sport_question_response.json, sport_questions)
            previous_questions.append(quiz_sport_question_response.json['id'])
        previous_questions = []
        for _ in education_questions:
            quiz_sport_question_response = self.nextQuizQuestion(education_category.id, previous_questions)
            self.assertIn(quiz_sport_question_response.json, education_questions)
            previous_questions.append(quiz_sport_question_response.json['id'])

    def test_givenQuizQuestionRequest_randomQuestionReturns(self):
        sport_category = self.create_new_category("sports")
        sport_questions = [self.create_new_question(self.generateQuestionData(i, sport_category.id)).json
                           for i in range(1, 3)]
        questions_randomly_returned = [self.nextQuizQuestion(0, []).json for _ in range(0, 10)]
        self.assertIn(sport_questions[0], questions_randomly_returned)
        self.assertIn(sport_questions[1], questions_randomly_returned)

    def test_wrongRequestUrl_notFoundResponse(self):
        response = self.client.get('/notexisting')
        self.assertEqual(response.status_code, 404)
        expected_body = {'error': 404, 'message': 'Not found', 'success': False}
        self.assertEqual(expected_body, response.json)

    def test_internalServerError_500ResponseWithJsonData(self):
        wrong_cat_id = -1  # not existing
        response = self.create_new_question(self.generateQuestionData(1, wrong_cat_id))
        self.assertEqual(response.status_code, 500)
        expected_body = {'error': 500, 'message': 'Ops, There is an internal error!, Please try again later',
                         'success': False}
        self.assertEqual(expected_body, response.json)

    # ↓
    # ↓
    # ↓
    # ↓
    # ↓ Utilities methods  ↓↓↓↓↓↓↓

    def create_new_category(self, category_type):
        category = Category(type=category_type)
        self.db.session.add(category)
        self.db.session.commit()
        return category

    def create_new_question(self, valid_question):
        response = self.client.post(f'{HOST}/questions', data=json.dumps(valid_question),
                                    content_type='application/json')
        return response

    def queryQuestions(self, page=None):
        if page:
            return self.client.get(f'{HOST}/questions?page={page}')
        return self.client.get(f'{HOST}/questions')

    @staticmethod
    def generateQuestionData(index, category=1):
        return {
            "question": "Question " + str(index),
            "answer": "Answer " + str(index),
            "difficulty": random.randint(1, 5),
            "category": category
        }

    def questions_by_category(self, cat_id):
        return self.client.get(f'{HOST}/categories/{cat_id}/questions')

    def nextQuizQuestion(self, quiz_category, previous_questions):
        payload = {
            "quiz_category": {"id": quiz_category},
            "previous_questions": previous_questions
        }
        return self.client.post(f'{HOST}/quizzes', data=json.dumps(payload), content_type='application/json')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
