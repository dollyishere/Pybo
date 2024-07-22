from datetime import datetime

from flask import Blueprint, render_template, request, url_for, g, flash
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

# 질문 수정
@bp.route('/modify/<int:question_id>', methods=('GET', 'POST'))
@login_required
def modify(question_id):
    # QuestionForm(obj=question)과 같이 조회한 데이터를 obj 매개변수에 전달하여 폼 생성
    question = Question.query.get_or_404(question_id)
    if g.user != question.user:
        # 강제 오류 발생
        flash('수정권한이 없습니다')
        return redirect(url_for('question.detail', question_id=question_id))
    if request.method == 'POST':  # POST 요청
        form = QuestionForm()
        # 아무 이상이 없으면 변경된 데이터를 저장
        if form.validate_on_submit():
            form.populate_obj(question)
            question.modify_date = datetime.now()  # 수정일시 저장
            db.session.commit()
            return redirect(url_for('question.detail', question_id=question_id))
    else:  # GET 요청
        form = QuestionForm(obj=question)
    return render_template('question/question_form.html', form=form)

# 질문 삭제
@bp.route('/delete/<int:question_id>')
@login_required
def delete(question_id):
    question = Question.query.get_or_404(question_id)
    if g.user != question.user:
        flash('삭제권한이 없습니다')
        return redirect(url_for('question.detail', question_id=question_id))
    db.session.delete(question)
    db.session.commit()
    return redirect(url_for('question._list'))

# 질문 추천 라우팅 함수
@bp.route('/vote/<int:question_id>/')
@login_required
def vote(question_id):
    _question = Question.query.get_or_404(question_id)
    # 해당 유저가 작성한 글일 시, 추천 불가
    if g.user == _question.user:
        flash('본인이 작성한 글은 추천할수 없습니다')
    else:
        # 다대다 관계이므로 append 사용
        # 같은 사용자가 같은 질문을 여러 번 추천해도 추천 횟수는 증가하지 않음
        _question.voter.append(g.user)
        db.session.commit()
    return redirect(url_for('question.detail', question_id=question_id))