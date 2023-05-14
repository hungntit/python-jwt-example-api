from flask import request, jsonify

from models.user import User
from services.auth_guard import auth_guard


def init(app):
    @app.route('/api/auth/register', methods=['POST'])
    def create_user():
        json_data: dict = request.json
        error_msg = User.validate_error(json_data, created=True)
        if error_msg:
            return jsonify({"message": f"{error_msg}"}), 400
        username = json_data.get("username")
        exist_user = User.load_by_username(username)
        if exist_user:
            return jsonify({"message": "User exist", "status": 400}), 400
        new_user = User.from_dict(json_data, encrypt_password=True, update_role=False)
        new_user.save()
        return jsonify(new_user.to_safe_json()), 200

    @app.route('/api/users', methods=['GET'])
    @auth_guard('admin')
    def list_users():
        users = User.load_data()
        return jsonify({"users": [user.to_safe_json() for user in users]}), 200

    @app.route('/api/users/<user_id>', methods=['GET'])
    @auth_guard('admin')
    def get_user(user_id: str):
        user = User.load_by_id(user_id)
        return jsonify(user), 200
