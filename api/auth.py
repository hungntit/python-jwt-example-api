from flask import request, jsonify

from models.user import User
from services.auth_provider import authenticate
from services.jwt_handler import generate_jwt


def init(app):

    @app.route('/api/auth', methods=['POST'])
    def auth():
        username = request.json.get('username')
        password = request.json.get('password')
        if not username or not password:
            return jsonify({"message": "username or password missing", "status": 400}), 400

        user_data = authenticate(username, password)
        if not user_data:
            return jsonify({"message": "Invalid credentials", "status": 400}), 400

        # <--- generates a JWT with valid within 1 hour by now
        token = generate_jwt(payload=user_data.to_safe_json(), lifetime=60)
        return jsonify({"token": token}), 200
