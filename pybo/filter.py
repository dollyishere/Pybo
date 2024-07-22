# filter용 파일 => utils라는 폴더 만들어서 모아둬도 좋을지도?

# fmt는 날짜 포맷 형식임(따로 지정 안할 시 default 값)
def format_datetime(value, fmt='%Y년 %m월 %d일 %p %I:%M'):
    return value.strftime(fmt)