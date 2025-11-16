import statistics  # 중간값 계산을 위해
import asyncio
from pyreload.run import get_time_from_run


CHAR_SET = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
NOISE_SAMPLES = 10
MAX_LENGTH = 128  # 플래그의 최대 길이 설정

async def measure_char_time(prefix, char):
    """특정 문자에 대한 실행 시간을 비동기적으로 측정하고 중앙값을 반환합니다."""
    test_guess = prefix + char
    
    # NOISE_SAMPLES 만큼 동시에 시간 측정 실행
    # get_time_from_run이 동기 함수이므로 to_thread를 사용해 비동기적으로 실행합니다.
    tasks = [asyncio.to_thread(get_time_from_run, test_guess) for _ in range(NOISE_SAMPLES)]
    time_measurements = await asyncio.gather(*tasks)
    
    reliable_time = statistics.median(time_measurements)
    return char, reliable_time

async def run_attack_async():
    """CHAR_SET의 모든 문자에 대한 테스트를 비동기적으로 실행하여 플래그를 찾습니다."""
    known_flag = ""

    for _ in range(MAX_LENGTH):
        # CHAR_SET의 모든 문자에 대해 시간 측정을 위한 비동기 작업 생성
        tasks = [measure_char_time(known_flag, c) for c in CHAR_SET]
        
        # 모든 작업을 동시에 실행하고 결과 수집
        results = await asyncio.gather(*tasks)
        
        # 가장 긴 시간이 걸린 문자 찾기
        if not results:
            print("공격 실패: 시간 측정 결과가 없습니다.")
            break

        best_char, best_time = max(results, key=lambda item: item[1])

        if not best_char:
            print("다음 문자를 찾지 못했습니다.")
            break

        known_flag += best_char
        print(f"\nFound next char: {best_char} (Time: {best_time})")
        print(f"Current Flag: {known_flag}\n")

def run_attack():
    """비동기 공격을 실행하기 위한 동기 래퍼 함수입니다."""
    try:
        asyncio.run(run_attack_async())
    except KeyboardInterrupt:
        print("\n사용자에 의해 중단되었습니다.")

# 기존 run_attack 함수를 run_attack_async를 호출하도록 변경하거나,
# 스크립트의 메인 실행 부분에서 asyncio.run(run_attack_async())를 직접 호출할 수 있습니다.
# 여기서는 기존 함수 시그니처를 유지하기 위해 래퍼 함수를 사용했습니다.