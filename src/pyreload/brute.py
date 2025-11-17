import statistics  # 중간값 계산을 위해
from pyreload.run import get_time_from_run
from pyreload.progprint import print_progress


CHAR_SET = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
NOISE_SAMPLES = 10
MAX_LENGTH = 128  # 플래그의 최대 길이 설정

def run_attack(delay=3.0):
    known_flag = ""

    for _ in range(MAX_LENGTH):
        best_time = 0
        best_char = ""

        print_progress(0, len(CHAR_SET))
        for idx, c in enumerate(CHAR_SET):
            test_guess = known_flag + c

            time_measurements = []
            for _ in range(NOISE_SAMPLES):
                time = get_time_from_run(test_guess, delay=delay)
                if time is None:
                    print("Abort! Last guess:")
                    print(test_guess)
                    return
                time_measurements.append(time)

            reliable_time = statistics.median(time_measurements)

            if reliable_time > best_time:
                best_time = reliable_time
                best_char = c
            
            print_progress(idx + 1, len(CHAR_SET))
        print()

        known_flag += best_char
        print(f"\nFound next char: {best_char} (Time: {best_time})")
        print(f"Current Flag: {known_flag}\n")
