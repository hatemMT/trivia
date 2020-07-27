import random

from flask import request, jsonify, Response, abort
from sqlalchemy import or_, sql

from .models import Question, commit_session, Category

QUESTIONS_PER_PAGE = 10


def register_controllers(app):
    @app.route('/categories')
    def categories():
        categories = Category.query.all()
        return jsonify({c.id: c.type for c in categories})

    @app.route('/questions')
    def read_questions():
        current_page = request.args.get('page', 1)
        search_text = request.args.get('searchTerm', None)

        def questions_filter():
            if search_text:
                return Question.question.ilike(f'%{search_text}%')
            else:
                return sql.true()

        return format_questions_data(Category.query.all(),
                                     Question.query.filter(questions_filter())
                                     .order_by('id').offset((int(current_page) - 1) * QUESTIONS_PER_PAGE)
                                     .limit(QUESTIONS_PER_PAGE).all(),
                                     Question.query.filter(questions_filter()).count())

    def format_questions_data(categories_list, questions_list, total_questions):
        return jsonify({
            "questions": [{"id": q.id,
                           "question": q.question, "answer": q.answer,
                           "difficulty": q.difficulty, "category": q.category_id
                           } for q in questions_list
                          ],
            "total_questions": total_questions,
            "categories": {c.id: c.type for c in categories_list},
            "current_category": None
        })

    @app.route('/questions/<int:qid>', methods=['DELETE'])
    def delete_question(qid):
        Question.query.filter(Question.id == qid).delete()
        commit_session()
        return Response(status=200)

    @app.route('/questions', methods=['POST'])
    def add_question():
        if request.content_type != 'application/json': abort(400)
        q_payload = request.get_json()
        validate(q_payload)
        q_payload["category"] = Category.query.filter(Category.id == q_payload.get("category", -1)).one_or_none()

        new_q = Question(**q_payload)
        new_q.insert()
        return jsonify(new_q.format()), 201

    def validate(q_payload):
        question = q_payload.get('question')
        answer = q_payload.get('answer')
        category = q_payload.get('category')
        difficulty = q_payload.get('difficulty')
        if "" in [question, answer, category, difficulty] or \
                None in [question, answer, category, difficulty]:
            abort(Response(response='{"message": "Validation Error, Please check the data" }',
                           content_type='application/json', status=400))

    @app.route('/categories/<int:cid>/questions')
    def get_questions_by_category(cid):
        if Category.query.filter(Category.id == cid).count() == 0: abort(400)
        questions = Question.query.filter(Question.category_id == cid).all()

        return jsonify({
            "questions": [q.format() for q in questions],
            "total_questions": len(questions),
            "current_category": cid
        })

    @app.route('/quizzes', methods=['POST'])
    def get_quiz_question():
        json = request.get_json()
        category = json.get('quiz_category')['id']
        prev_question = json.get('previous_questions')
        query = Question.query.filter(or_(Question.category_id == category, category == 0)).filter(
            Question.id.notin_(prev_question))
        total_available = query.count()
        if total_available > 0:
            question_found = query.offset(random.randint(0, total_available - 1)).first()
            return jsonify(question_found.format())
        return Response(response='{"message": "Questions finished !"}', status=404)
