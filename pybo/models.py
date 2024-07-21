from pybo import db

# 질문 모델 클래스
# db.Model 클래스를 상속받음
# 해당 db 객체는 __init__.py 파일에서 생성한 SQLAlchemy 클래스의 객체임
# 각 속성은 db.Column임
# 괄호 안의 첫 인수는 데이터 타입(데이터의 종류)임
# 이외에도 pk인지, null 값 허용인지를 설정 가능함
class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)

class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # 질문 모델 상속받음(fk), 질문 삭제 시 해당 질문에 달린 답변도 함께 삭제(CASCADE)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id', ondelete='CASCADE'))
    # 답변 모델에서 질문 모델을 참조하기 위해 추가
    # backref는 역참조(질문에서 답변을 거꾸로 참조) 속성임
    # 질문에 달린 답변들을 참조하는 게 가능함
    question = db.relationship('Question', backref=db.backref('answer_set', cascade='all, delete-orphan'))
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)