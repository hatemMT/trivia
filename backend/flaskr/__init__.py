from flask import Flask
from flask_cors import CORS

from .controllers import register_controllers
from .errorhandlers import register_handlers
from .models import setup_db


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.after_request
    def response_filter(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PUT, PATCH, OPTIONS, DELETE')
        return response

    ######## App Controllers #######
    register_controllers(app)

    ######## Error handlers #########
    register_handlers(app)

    return app


if __name__ == '__main__':
    create_app().run()
