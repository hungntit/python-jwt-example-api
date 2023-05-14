from flask import request, jsonify

from models.shop import Shop
from services.auth_guard import check_jwt, auth_guard


def init(app):

    @app.route('/api/shops', methods=['POST'])
    def create_shop_by_user():
        try:
            login = check_jwt()
        except Exception as e:
            return jsonify({"message": f'{e}', "status": 401}), 401
        user_id = login['id']
        json_data: dict = request.json
        error_msg = Shop.validate_error(json_data, created=True)
        if error_msg:
            return jsonify({"message": f"{error_msg}"}), 400

        shop = Shop.from_dict(json_data)
        shop.user_id = user_id
        shop.save()
        return jsonify(shop.to_safe_json()), 200

    @app.route('/api/shops/<shop_id>', methods=['PUT'])
    def update_shop_by_user(shop_id):
        try:
            login = check_jwt()
        except Exception as e:
            return jsonify({"message": f'{e}', "status": 401}), 401
        user_id = login['id']
        shop = Shop.load_by_id(user_id, shop_id)
        if not shop:
            return jsonify({}), 404
        json_data: dict = request.json
        error_msg = Shop.validate_error(json_data, created=False)
        if error_msg:
            return jsonify({"message": f"{error_msg}"}), 400

        shop.update(json_data)
        return jsonify(shop.to_safe_json()), 200

    @app.route('/api/shops/<shop_id>', methods=['PATCH'])
    def patch_update_shop_by_user(shop_id):
        try:
            login = check_jwt()
        except Exception as e:
            return jsonify({"message": f'{e}', "status": 401}), 401
        user_id = login['id']
        shop = Shop.load_by_id(user_id, shop_id)
        if not shop:
            return jsonify({}), 404
        json_data: dict = request.json

        shop.update(json_data)
        return jsonify(shop.to_safe_json()), 200

    @app.route('/api/shops/<shop_id>', methods=['DELETE'])
    def delete_shop_of_user(shop_id):
        try:
            login = check_jwt()
        except Exception as e:
            return jsonify({"message": f'{e}', "status": 401}), 401
        user_id = login['id']
        shop = Shop.load_by_id(user_id, shop_id)
        if shop:
            shop.delete()
            return jsonify(shop.to_safe_json()), 200
        else:
            return jsonify({}), 404

    @app.route('/api/shops', methods=['GET'])
    def get_all_shops_for_user():
        try:
            login = check_jwt()
        except Exception as e:
            return jsonify({"message": f'{e}', "status": 401}), 401
        user_id = login['id']
        shops = Shop.find_all_by_user_id(user_id)
        return jsonify({"shops": [shop.to_safe_json() for shop in shops]}), 200

    @app.route('/api/shops/<shop_id>', methods=['GET'])
    def load_shop_of_user(shop_id):
        try:
            login = check_jwt()
        except Exception as e:
            return jsonify({"message": f'{e}', "status": 401}), 401
        user_id = login['id']
        shop = Shop.load_by_id(user_id, shop_id)
        if shop:
            return jsonify(shop.to_safe_json()), 200
        else:
            return jsonify({}), 404

    @app.route('/api/users/<user_id>/shops', methods=['POST'])
    @auth_guard('admin')
    def create_shop(user_id: str):
        json_data: dict = request.json
        error_msg = Shop.validate_error(json_data, created=True)
        if error_msg:
            return jsonify({"message": f"{error_msg}"}), 400

        shop = Shop.from_dict(json_data)
        shop.user_id = user_id
        shop.save()
        return jsonify(shop.to_safe_json()), 200

    @app.route('/api/users/<user_id>/shops', methods=['GET'])
    @auth_guard('admin')
    def list_all_shop(user_id: str):
        shops = Shop.find_all_by_user_id(user_id)
        return jsonify({"shops": [shop.to_safe_json() for shop in shops]}), 200

    @app.route('/api/users/<user_id>/shops/<shop_id>', methods=['GET'])
    @auth_guard('admin')
    def get_shop(user_id: str, shop_id):
        shop = Shop.load_by_id(user_id, shop_id)
        return jsonify(shop.to_safe_json()), 200

