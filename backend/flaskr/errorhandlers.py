from flask import jsonify
from sqlalchemy.exc import IntegrityError


def register_handlers(app):
    @app.errorhandler(400)
    def handler(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad request"
        }), 400

    @app.errorhandler(404)
    def handler(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Not found"
        }), 404

    @app.errorhandler(422)
    def handler(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Not processable entity"
        }), 422

    @app.errorhandler(500)
    @app.errorhandler(IntegrityError)  # For handling the database Integrity errors
    def handler(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Ops, There is an internal error!, Please try again later"
        }), 500
