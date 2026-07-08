"""타임라인 JSON 수치 검증 규칙 (기획서 5.6절: 총 길이, 자막 읽기 시간, 연속 컷 등).

에이전트는 결과 영상을 볼 수 없으므로, 품질 검증은 체크리스트가 아니라 이 수치 검증 코드가 담당한다.
Timeline의 Cut들은 필요 시 이 함수 안에서 직접 보정된다(duration 상향, transition_out 강제 교정).
"""
import re

from agents.animatic.schemas import Cut, Timeline

QUOTE_CHARS = '"\'“”『』'
SYLLABLES_PER_SECOND = 5.5
LEAD_PAD_SECONDS = 0.8
CAPTION_CHARS_PER_SECOND = 4
TOTAL_LENGTH_TOLERANCE = 0.2
SAME_DURATION_RUN_LIMIT = 3


def _count_syllables(text: str) -> int:
    return len(re.findall(r"[가-힣]", text))


def _is_dialogue_caption(caption: str) -> bool:
    return len(caption) >= 2 and caption[0] in QUOTE_CHARS and caption[-1] in QUOTE_CHARS


def _check_total_length(timeline: Timeline, target_runtime_seconds: float | None) -> list[str]:
    if target_runtime_seconds is None:
        return []
    total = sum(cut.duration for cut in timeline.cuts)
    lower = target_runtime_seconds * (1 - TOTAL_LENGTH_TOLERANCE)
    upper = target_runtime_seconds * (1 + TOTAL_LENGTH_TOLERANCE)
    if not (lower <= total <= upper):
        return [f"총 길이 {total:.1f}초가 목표 러닝타임 {target_runtime_seconds:.1f}초의 ±20% 범위를 벗어남"]
    return []


def _check_dialogue_and_caption(timeline: Timeline) -> list[str]:
    flags = []
    for cut in timeline.cuts:
        if not isinstance(cut, Cut):
            continue
        caption = cut.overlays.caption
        if not caption:
            continue

        if _is_dialogue_caption(caption):
            dialogue_text = caption[1:-1]
            required = _count_syllables(dialogue_text) / SYLLABLES_PER_SECOND + LEAD_PAD_SECONDS
            if cut.duration < required:
                flags.append(
                    f"컷 {cut.cut}: 대사 길이 부족으로 duration {cut.duration:.1f}→{required:.1f}초 자동 상향"
                )
                cut.duration = round(required, 2)
        else:
            max_duration_for_caption = len(caption) / CAPTION_CHARS_PER_SECOND
            if cut.duration < max_duration_for_caption:
                flags.append(f"컷 {cut.cut}: 자막 읽기 시간 부족(caption 길이 대비 duration 부족)")
    return flags


def _check_same_duration_runs(timeline: Timeline) -> list[str]:
    flags = []
    run_duration = None
    run_length = 0
    for entry in timeline.cuts:
        if not isinstance(entry, Cut):
            run_duration, run_length = None, 0
            continue
        if entry.duration == run_duration:
            run_length += 1
        else:
            run_duration, run_length = entry.duration, 1
        if run_length == SAME_DURATION_RUN_LIMIT:
            flags.append(f"동일 길이(duration {run_duration}) 컷이 {SAME_DURATION_RUN_LIMIT}개 연속")
    return flags


def _check_transitions_inside_scenes(timeline: Timeline) -> list[str]:
    flags = []
    cuts = timeline.cuts
    for i, entry in enumerate(cuts):
        if not isinstance(entry, Cut) or entry.transition_out == "cut":
            continue
        next_entry = cuts[i + 1] if i + 1 < len(cuts) else None
        is_scene_boundary = next_entry is None or not isinstance(next_entry, Cut)
        if not is_scene_boundary:
            flags.append(
                f"컷 {entry.cut}: 씬 내부 전환({entry.transition_out})을 cut으로 강제 교정"
            )
            entry.transition_out = "cut"
    return flags


def validate_timeline(
    timeline: Timeline, target_runtime_seconds: float | None = None
) -> list[str]:
    flags: list[str] = []
    flags += _check_total_length(timeline, target_runtime_seconds)
    flags += _check_dialogue_and_caption(timeline)
    flags += _check_same_duration_runs(timeline)
    flags += _check_transitions_inside_scenes(timeline)
    return flags
