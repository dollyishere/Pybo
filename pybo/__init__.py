from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

import config

# 객체 바깥에 생성
db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    # config 파일 작성 항목 읽기
    app.config.from_object(config)
    # app.config.from_pyfile('config.py')

    # ORM
    db.init_app(app) # db 객체 생성
    migrate.init_app(app, db) # migrate 객체 생성
    from . import models
    # init_app 메서드를 통해 app으로 등록한다
    # db 객체를 create_app 안에서 생성하면 다른 모듈(블루 프린트)에서 사용할 수 없다
    # 따라서 해당 객체들은 create_app 밖에서 생성하고, init_app 함수를 통해 앱에 등록한다!


    # 블루프린트
    from .views import main_views, question_views, answer_views
    app.register_blueprint(main_views.bp)
    app.register_blueprint(question_views.bp)
    app.register_blueprint(answer_views.bp)

    return app
