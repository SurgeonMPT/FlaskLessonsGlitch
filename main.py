from flask import Flask
from flask_login import LoginManager

from data import db_session
from data.error_handlers import not_found, forbidden, unauthorized
from data.models.users import User
from routes.main_routes import bp as main_bp
from routes.news_routes import bp as news_bp
from api import news_api
from test import default_test

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

# Регистрация Blueprints
app.register_blueprint(main_bp)
app.register_blueprint(news_bp)

# Настройка Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)

def main():
    # Регистрация обработчиков ошибок

    app.register_error_handler(404, not_found)
    app.register_error_handler(403, forbidden)
    app.register_error_handler(401, unauthorized)
    db_session.global_init("db/blogs.db")
    default_test(db_session)
    app.register_blueprint(news_api.blueprint)
    app.run()


if __name__ == '__main__':
    main()