from datetime import datetime

from flask import Blueprint, url_for, request, render_template, g, flash
from werkzeug.utils import redirect

from pybo import db
from ..forms import AnswerForm
from pybo.models import Question, Answer
from pybo.views.auth_views import login_required

# 답변용 블루프린트
bp = Blueprint("answer", __name__, url_prefix='/answer')

# 답변 등록
@bp.route('/create/<int:question_id>', methods=('POST', ))
@login_required
def create(question_id):
    form = AnswerForm()
    question = Question.query.get_or_404(question_id)
    if form.validate_on_submit():
        content = request.form['content']
        answer = Answer(content=content, create_date=datetime.now(), user=g.user)
        
    # question = Question.query.get_or_404(question_id)
    # # form으로 전송된 데이터 항목 중 name 속성이 content인 값
    # content = request.form['content']
    # answer = Answer(content=content, create_date=datetime.now())
        # # 질문에 달린 답변들
        question.answer_set.append(answer)
    # # 아래처럼 저장하는 방법도 있다(Answer 모델 그대로 사용)
    # # answer = Answer(question=question, content=content, create_date=datetime.now())
    # # db.session.add(answer)
        db.session.commit()
        return redirect('{}#answer_{}'.format(
            url_for('question.detail', question_id=question_id), answer.id))
    return render_template('question/question_detail.html', question=question, form=form)

# 답변 수정 함수
@bp.route('/modify/<int:answer_id>', methods=('GET', 'POST'))
@login_required
def modify(answer_id):
    answer = Answer.query.get_or_404(answer_id)
    if g.user != answer.user:
        flash('수정권한이 없습니다')
        return redirect(url_for('question.detail', question_id=answer.question.id))
    if request.method == "POST":
        form = AnswerForm()
        if form.validate_on_submit():
            form.populate_obj(answer)
            answer.modify_date = datetime.now()  # 수정일시 저장
            db.session.commit()
            return redirect('{}#answer_{}'.format(
                url_for('question.detail', question_id=answer.question.id), answer.id))
    else:
        form = AnswerForm(obj=answer)
    return render_template('answer/answer_form.html', form=form)

# 답변 삭제 함수
@bp.route('/delete/<int:answer_id>')
@login_required
def delete(answer_id):
    answer = Answer.query.get_or_404(answer_id)
    question_id = answer.question.id
    if g.user != answer.user:
        flash('삭제권한이 없습니다')
    else:
        db.session.delete(answer)
        db.session.commit()
    return redirect(url_for('question.detail', question_id=question_id))

# 답변 추천 함수
# 질문과 동일
@bp.route('/vote/<int:answer_id>/')
@login_required
def vote(answer_id):
    _answer = Answer.query.get_or_404(answer_id)
    if g.user == _answer.user:
        flash('본인이 작성한 글은 추천할수 없습니다')
    else:
        _answer.voter.append(g.user)
        db.session.commit()
    return redirect('{}#answer_{}'.format(
                url_for('question.detail', question_id=_answer.question.id), _answer.id))