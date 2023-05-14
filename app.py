from flask import Flask
from api.auth import init as init_auth_routes
from api.user_routes import init as init_user_routes
from api.shop_routes import init as init_shop_routes

from api.routes import init as init_routes


def create_app():
    flask_app = Flask(__name__)
    init_auth_routes(flask_app)
    init_routes(flask_app)
    init_user_routes(flask_app)
    init_shop_routes(flask_app)
    return flask_app


if __name__ == '__main__':
    app = create_app()
    app.run()
