import statistics  # 중간값 계산을 위해
from pyreload.run import get_time_from_run


CHAR_SET = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
NOISE_SAMPLES = 10
MAX_LENGTH = 64  # 플래그의 최대 길이 설정

def run_attack():
    known_flag = ""

    for _ in range(MAX_LENGTH):
        best_time = 0
        best_char = ""

        for c in CHAR_SET:
            test_guess = known_flag + c

            time_measurements = []
            for _ in range(NOISE_SAMPLES):
                time = get_time_from_run(test_guess)
                time_measurements.append(time)

            reliable_time = statistics.median(time_measurements)

            if reliable_time > best_time:
                best_time = reliable_time
                best_char = c

        known_flag += best_char
        print(f"\nFound next char: {best_char} (Time: {best_time})")
        print(f"Current Flag: {known_flag}\n")
