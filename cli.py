"""StoryMaker CLI 진입점: storymaker run <logline>"""
import argparse
import sys

from dotenv import load_dotenv

from agents.scenario.agent import generate_scenario
from agents.storyboard.agent import generate_storyboard
from pipeline.run_pipeline import run

load_dotenv()


def main() -> None:
    # Windows 콘솔 기본 코드페이지(cp949 등)는 Gemini가 생성하는 특수 문장부호(em dash 등)를
    # 인코딩하지 못해 UnicodeEncodeError로 죽는다. 인코딩은 그대로 두고 표현 불가능한 문자만
    # 대체(replace)하도록 해서, 기존 콘솔/파이프 인코딩과의 호환성을 깨지 않는다.
    sys.stdout.reconfigure(errors="replace")

    parser = argparse.ArgumentParser(prog="storymaker")
    subparsers = parser.add_subparsers(dest="command", required=True)

    run_parser = subparsers.add_parser("run", help="전체 파이프라인 실행")
    run_parser.add_argument("logline", help="로그라인 또는 기획 아이디어")

    scenario_parser = subparsers.add_parser("scenario", help="1단계 시나리오 생성만 실행")
    scenario_parser.add_argument("logline", help="로그라인 또는 기획 아이디어")

    storyboard_parser = subparsers.add_parser(
        "storyboard", help="1~2단계(시나리오→스토리보드) 실행"
    )
    storyboard_parser.add_argument("logline", help="로그라인 또는 기획 아이디어")

    args = parser.parse_args()

    if args.command == "run":
        run(args.logline)
    elif args.command == "scenario":
        print(generate_scenario(args.logline).scene_script)
    elif args.command == "storyboard":
        scenario = generate_scenario(args.logline)
        storyboard = generate_storyboard(scenario.scene_script)
        print(storyboard.model_dump_json(indent=2))


if __name__ == "__main__":
    main()
