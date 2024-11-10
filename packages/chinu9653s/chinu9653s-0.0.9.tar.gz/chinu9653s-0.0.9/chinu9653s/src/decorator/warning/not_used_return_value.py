import sys
from functools import wraps


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
                self.used = False  # 반환값 사용 여부

            def __del__(self):
                if not self.used:
                    warning = f"{file_name}:{line_no}:\nUserWarning: {func.__name__}()의 반환값이 사용되지 않았습니다.\n"
                    sys.stderr.write(warning)

            def __getattr__(self, name):
                self.used = True  # 속성에 접근할 때 사용된 것으로 표시
                return getattr(self._value, name)

            def __call__(self, *args, **kwargs):
                self.used = True  # 호출될 때 사용된 것으로 표시
                return self._value(*args, **kwargs) if callable(self._value) else self._value

            def __repr__(self):
                self.used = True  # 문자열로 표현될 때 사용된 것으로 표시
                return repr(self._value)

        # result가 TrackedValue로 감싸지지 않고 사용될 때 경고를 피하기 위해 바로 사용된 것으로 표시
        if isinstance(result, TrackedValue) or not callable(result):
            TrackedValue.used = True  # 바로 사용된 것으로 설정
        else:
            TrackedValue.used = False  # 사용되지 않은 경우 설정 유지

        return TrackedValue(result)

    return wrapper
