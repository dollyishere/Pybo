import time
import functools

# 데코레이터 함수
def decorate(original_func):
  # 데코레이터 함수의 올바른 동작 보장
  # 정확히는 데코레이터 만들 때 원래 함수의 메타데이터를 유지해 원래 함수처럼 보이게 함
  @functools.wraps(original_func)
  def wrapper(*args, **kwargs): # *args, **kwargs 입력 인수 추가
    # *args는 위치 인수, **kwargs는 키워드 인수임
    start = time.time()
    original_func(*args, **kwargs) # 전달 받은 *args, **kwargs를 입력 파라미터로 하여 기존 함수 수행
    end = time.time()
    print(f"함수 총 수행시간: {end - start}초")
  return wrapper # wrapper 함수 리턴(클로저)

# 데코레이터 실 사용 예시
# 함수 자체를 호출하는 게 아니라, 적용하고 싶은 함수에 어노테이션으로 붙여서 적용
@decorate
def myfunc(msg):
    """ 데코레이터 확인 함수 """
    print("'%s'을 출력합니다." % msg)