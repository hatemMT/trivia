from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Integer

database_name = "trivia"
database_path = "postgres://admin:secret@{}/{}".format('192.168.99.100:5432', database_name)

db = SQLAlchemy()


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    Migrate(app, db)


def commit_session():
    db.session.commit()


'''
Category
'''


class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(Integer, primary_key=True)
    type = db.Column(String)
    questions = db.relationship('Question', backref='category')

    def __init__(self, type):
        self.type = type

    def format(self):
        return {
            'id': self.id,
            'type': self.type
        }


'''
Question

'''


class Question(db.Model):
    __tablename__ = 'questions'

    id = db.Column(Integer, primary_key=True)
    question = db.Column(String)
    answer = db.Column(String)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    difficulty = db.Column(Integer)

    def __init__(self, question, answer, category, difficulty):
        self.question = question
        self.answer = answer
        self.category = category
        self.difficulty = difficulty

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'question': self.question,
            'answer': self.answer,
            'category': self.category.id,
            'difficulty': self.difficulty
        }
