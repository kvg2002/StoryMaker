"""animatic_renderer.py(검증된 ffmpeg 스크립트)를 서브프로세스로 안전하게 호출한다.

렌더러 스크립트는 이미지 경로를 현재 작업 디렉터리 기준 상대 경로로 참조하므로,
cwd를 콘티 이미지가 있는 폴더로 지정해 실행한다. 스크립트 내용 자체는 수정하지 않는다
(기획서 원칙: "에이전트가 즉석에서 ffmpeg 명령을 재작성하지 않게 한다").
"""
import subprocess
import sys
from pathlib import Path

RENDERER_SCRIPT = Path(__file__).parent / "animatic_renderer.py"


def render_animatic(timeline_path: Path, output_path: Path, cwd: Path) -> None:
    cwd.mkdir(parents=True, exist_ok=True)
    result = subprocess.run(
        [
            sys.executable,
            str(RENDERER_SCRIPT.resolve()),
            str(timeline_path.resolve()),
            str(output_path.resolve()),
        ],
        cwd=str(cwd),
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(f"animatic_renderer 실패: {result.stderr}")
