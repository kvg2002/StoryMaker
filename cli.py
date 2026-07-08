"""StoryMaker CLI 진입점: storymaker run <logline>"""
import argparse

from pipeline.run_pipeline import run


def main() -> None:
    parser = argparse.ArgumentParser(prog="storymaker")
    subparsers = parser.add_subparsers(dest="command", required=True)

    run_parser = subparsers.add_parser("run", help="전체 파이프라인 실행")
    run_parser.add_argument("logline", help="로그라인 또는 기획 아이디어")

    args = parser.parse_args()

    if args.command == "run":
        run(args.logline)


if __name__ == "__main__":
    main()
