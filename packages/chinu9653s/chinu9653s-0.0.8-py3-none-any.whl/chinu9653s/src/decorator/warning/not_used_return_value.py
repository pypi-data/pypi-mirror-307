import sys
from functools import wraps

# # 사용 예시
# @use_return
# def get_value():
#     return 42
#
#
# # 경고 발생
# get_value()
#
# # 경고 없음 (반환값 사용)
# x = get_value()


def use_return(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # 호출 위치 정보 가져오기
        frame = sys._getframe(1)
        file_name = frame.f_code.co_filename
        line_no = frame.f_lineno

        # 실제 함수 결과
        result = func(*args, **kwargs)

        # 반환값 사용 추적을 위한 내부 클래스
        class TrackedValue:
            def __init__(self, value):
                self._value = value
                self.used = False

            def __del__(self):
                if not self.used:
                    warning = f"{file_name}:{line_no}:\nUserWarning: {func.__name__}()의 반환값이 사용되지 않았습니다.\n"
                    sys.stderr.write(warning)

            def __getattr__(self, name):
                self.used = True
                return getattr(self._value, name)

            def __call__(self, *args, **kwargs):
                self.used = True
                return self._value(*args, **kwargs) if callable(self._value) else self._value

            def __repr__(self):
                self.used = True
                return repr(self._value)

        return TrackedValue(result)

    return wrapper
