from datetime import datetime

from flask import Blueprint, render_template, request, url_for, g
from werkzeug.utils import redirect

from .. import db
from pybo.models import Question
from pybo.forms import QuestionForm, AnswerForm
from .auth_views import login_required

# 질문용 블루프린트
bp = Blueprint('question', __name__, url_prefix='/question')

# 질문 목록
@bp.route('/list/')
def _list():
    # get으로 요청한 url에서 페이지 값 가져올 때 사용
    # page 파라미터는 정수라는 것을 명시
    # url에 page 값이 없으면 default = 1이 적용됨
    page = request.args.get('page', type=int, default=1) # 페이지
    question_list = Question.query.order_by(Question.create_date.desc())
    # pagenite 메서드는 키워드로만 인자를 보낼 수 있음
    # page는 현재 조회할 페이지의 번호이고, per_page는 페이지마다 보여 줄 게시물이 10건이라는 의미임
    question_list = question_list.paginate(page=page, per_page=10)
    return render_template('question/question_list.html', question_list=question_list)

# 질문 상세
@bp.route('/detail/<int:question_id>/') # 숫자가 매핑되는 것을 알려줌(int)
def detail(question_id):
    form = AnswerForm()
    question = Question.query.get_or_404(question_id)
    return render_template('question/question_detail.html', question=question, form=form) 

# 질문 등록
@bp.route('/create/', methods=('GET', 'POST'))
@login_required
def create():
    form = QuestionForm()
    # post 요청으로 들어왔을 시, 데이터 신규 생성
    if request.method == 'POST' and form.validate_on_submit():
        question = Question(subject=form.subject.data, content=form.content.data, 
                            create_date=datetime.now(), user=g.user)
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('question/question_form.html', form=form)