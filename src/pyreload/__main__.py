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

    args = parser.parse_args()
    print("Starting Flush+Reload timing attack...")
    run_attack(delay=args.delay, max_workers=args.max_workers)


if __name__ == "__main__":
    main()
