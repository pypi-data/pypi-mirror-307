import sys
from functools import wraps


def use_return(func):
    @wraps(func)
    def wrapper(*args, **kwargs):


        # 실제 함수 결과
        result = func(*args, **kwargs)

        # 데코레이터 사용해도 반환값 없으면 작동 안함
        if result is None:
            return result

        # 반환값 사용 추적을 위한 내부 클래스
        class TrackedValue:
            def __init__(self, value):
                self._value = value
                self._type = type(value)
                self.used = False

            def __del__(self):
                if not self.used and sys.getrefcount(self) < 4:
                    # 호출 위치 정보 가져오기
                    frame = sys._getframe(1)
                    file_name = frame.f_code.co_filename
                    line_no = frame.f_lineno
                    warning = f"{file_name}:{line_no}:\nUserWarning: {func.__name__}()의 리턴값이 사용되지 않았습니다.\n"
                    sys.stderr.write(warning)

            def __call__(self, *args, **kwargs):
                return self._value(*args, **kwargs) if callable(self._value) else self._value

            def __repr__(self):
                return repr(self._value)

            def __getattr__(self, name):
                return getattr(self._value, name)

            def __getattribute__(self, name):
                # 특정 내부 속성에 접근할 때는 used를 변경하지 않음
                if name not in {"used", "__del__"}:
                    object.__setattr__(self, "used", True)
                return object.__getattribute__(self, name)

            # os.path.join 같은 함수에서 TrackedValue 객체를 문자열로 자동 변환하도록 추가
            def __fspath__(self):
                return str(self._value)

            # 형변환 처리
            def __str__(self):
                return str(self._value)

            def __bool__(self):
                return bool(self._value)

            def __int__(self):
                return int(self._value)

            def __float__(self):
                return float(self._value)

            def __len__(self):
                return len(self._value)

            # 연산자 처리
            def __add__(self, other):
                return self._value + other

            def __sub__(self, other):
                return self._value - other

            def __mul__(self, other):
                return self._value * other

            def __truediv__(self, other):
                return self._value / other

            def __floordiv__(self, other):
                return self._value // other

            def __mod__(self, other):
                return self._value % other

            def __pow__(self, other):
                return self._value ** other

            def __lshift__(self, other):
                return self._value << other

            def __rshift__(self, other):
                return self._value >> other

            def __and__(self, other):
                return self._value & other

            def __or__(self, other):
                return self._value | other

            def __xor__(self, other):
                return self._value ^ other

            def __radd__(self, other):
                return self._value + other

            def __rsub__(self, other):
                return self._value - other

            def __rmul__(self, other):
                return self._value * other

            def __rtruediv__(self, other):
                return self._value / other

            def __rfloordiv__(self, other):
                return self._value // other

            def __rmod__(self, other):
                return self._value % other

            def __rpow__(self, other):
                return self._value ** other

            def __rlshift__(self, other):
                return self._value << other

            def __rrshift__(self, other):
                return self._value >> other

            def __rand__(self, other):
                return self._value & other

            def __ror__(self, other):
                return self._value | other

            def __rxor__(self, other):
                return self._value ^ other

            # 복합 할당 연산자 처리
            def __iadd__(self, other):
                return self._value + other

            def __isub__(self, other):
                return self._value - other

            def __imul__(self, other):
                return self._value * other

            def __itruediv__(self, other):
                return self._value / other

            def __ifloordiv__(self, other):
                return self._value // other

            def __imod__(self, other):
                return self._value % other

            def __ipow__(self, other):
                return self._value ** other

            def __ilshift__(self, other):
                return self._value << other

            def __irshift__(self, other):
                return self._value >> other

            def __iand__(self, other):
                return self._value & other

            def __ior__(self, other):
                return self._value | other

            def __ixor__(self, other):
                return self._value ^ other

            # 비교 연산 처리
            def __eq__(self, other):
                return self._value == other

            def __ne__(self, other):
                return self._value != other

            def __lt__(self, other):
                return self._value < other

            def __le__(self, other):
                return self._value <= other

            def __gt__(self, other):
                return self._value > other

            def __ge__(self, other):
                return self._value >= other

            # 추가: 객체 ID 접근 시 사용된 것으로 간주
            def __hash__(self):
                return hash(self._value)

            # 기타
            def __abs__(self):
                return abs(self._value)

            def __invert__(self):
                return not self._value

            def __complex__(self):
                return complex(self._value)

        # TrackedValue로 감싸서 반환
        return TrackedValue(result)

    return wrapper
