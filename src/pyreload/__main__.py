import argparse
from pyreload.brute_async import run_attack


def main():
    parser = argparse.ArgumentParser(description="Flush+Reload 타이밍 공격")
    parser.add_argument(
        "--delay",
        type=float,
        default=0.032,
        help="각 시도 사이의 지연 시간(초) (기본값: 0.032)",
    )

    parser.add_argument(
        "--max-workers",
        type=int,
        default=3,
        help="병렬 처리에 사용할 최대 워커 수 (기본값: 3)",
    )

    parser.add_argument(
        "--max-retries",
        type=int,
        default=5,
        help="최대 재시도 횟수 (기본값: 5)",
    )

    args = parser.parse_args()
    print("Starting Flush+Reload timing attack...")
    print(f"Settings:\r\n    delay={args.delay}, max_workers={args.max_workers}, max_retries={args.max_retries}")
    run_attack(delay=args.delay, max_workers=args.max_workers, max_retries_ref=args.max_retries)


if __name__ == "__main__":
    main()
