from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
# from flaskext.markdown import Markdown

import config

# 객체 바깥에 생성
naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
db = SQLAlchemy(metadata=MetaData(naming_convention=naming_convention))
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    # config 파일 작성 항목 읽기
    app.config.from_object(config)
    # app.config.from_pyfile('config.py')

    # ORM
    db.init_app(app) # db 객체 생성
    if app.config['SQLALCHEMY_DATABASE_URI'].startswith("sqlite"):
        migrate.init_app(app, db, render_as_batch=True)
    else:
        migrate.init_app(app, db)
    migrate.init_app(app, db) # migrate 객체 생성
    from . import models
    # init_app 메서드를 통해 app으로 등록한다
    # db 객체를 create_app 안에서 생성하면 다른 모듈(블루 프린트)에서 사용할 수 없다
    # 따라서 해당 객체들은 create_app 밖에서 생성하고, init_app 함수를 통해 앱에 등록한다!


    # 블루프린트
    from .views import main_views, question_views, answer_views, auth_views
    app.register_blueprint(main_views.bp)
    app.register_blueprint(question_views.bp)
    app.register_blueprint(answer_views.bp)
    app.register_blueprint(auth_views.bp)

    # 필터
    from .filter import format_datetime
    app.jinja_env.filters['datetime'] = format_datetime

    # markdown
    # Markdown(app, extensions=['nl2br', 'fenced_code'])

    return app
