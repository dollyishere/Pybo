from flask import Blueprint, url_for
from werkzeug.utils import redirect

from pybo.models import Question

# main은 불루 프린트의 별칭이며, 나중에 url_for 함수에 사용됨
# url_prefix는 라우팅 함수의 애너테이션 URL 앞에 기본으로 붙일 접두어 URL을 의미함
# 그러니까 만약 url_prefix='/main'이라고 했다면 main을 붙이고 들어가야 한다는 이야기임
# spring의 controller랑 같은 거 같은데?
bp = Blueprint('main', __name__, url_prefix='/')

# 기본 경로
@bp.route('/')
def index():
    return redirect(url_for('question._list')) # 질문 목록 페이지로 리다이렉트
# 라우팅 함수명으로 매핑된 url을 역으로 찾게 됨
# redirect(URL) - URL로 페이지 이동
# url_for(라우팅 함수명) - 라우팅 함수에 매칭되어 있는 URL 리턴
# _list인 이유는 list가 python 예약어라서!