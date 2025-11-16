from pyreload.run import get_time_from_run


# --- 메인 실행 부분 ---

# 테스트할 비밀번호 인자
guess = "a"

# 프로그램 실행 및 시간 값 파싱
time_value = get_time_from_run(guess)

if time_value is not None:
    print(f"입력: '{guess}'")
    print(f"측정된 시간: {time_value}")
else:
    print(f"입력 '{guess}'에 대한 시간 값을 가져오는 데 실패했습니다.")
