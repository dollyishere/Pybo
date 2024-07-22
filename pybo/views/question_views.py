from datetime import datetime

from flask import Blueprint, render_template, request, url_for
from werkzeug.utils import redirect

from .. import db
from pybo.models import Question
from pybo.forms import QuestionForm, AnswerForm

bp = Blueprint('question', __name__, url_prefix='/question')

# 질문 목록
@bp.route('/list/')
def _list():
    question_list = Question.query.order_by(Question.create_date.desc())
    return render_template('question/question_list.html', question_list=question_list)

# 질문 상세
@bp.route('/detail/<int:question_id>/') # 숫자가 매핑되는 것을 알려줌(int)
def detail(question_id):
    form = AnswerForm()
    question = Question.query.get_or_404(question_id)
    return render_template('question/question_detail.html', question=question, form=form) 

# 질문 등록
@bp.route('/create/', methods=('GET', 'POST'))
def create():
    form = QuestionForm()
    # post 요청으로 들어왔을 시, 데이터 신규 생성
    if request.method == 'POST' and form.validate_on_submit():
        question = Question(subject=form.subject.data, content=form.content.data, create_date=datetime.now())
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('question/question_form.html', form=form)