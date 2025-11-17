import argparse
from pyreload.brute import run_attack


def main():
    parser = argparse.ArgumentParser(description="Flush+Reload 타이밍 공격")
    parser.add_argument(
        "--delay",
        type=float,
        default=0.1,
        help="각 시도 사이의 지연 시간(초) (기본값: 0.1)",
    )

    args = parser.parse_args()
    print("Starting Flush+Reload timing attack...")
    run_attack(delay=args.delay)


if __name__ == "__main__":
    main()
