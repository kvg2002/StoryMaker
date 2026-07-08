"""StoryMaker 웹 UI: 단계별 검토형 위자드.

1단계(시나리오) → 사람이 검토·수정 → 2단계(스토리보드) → 사람이 검토·수정 → 3단계(애니매틱).
각 단계는 사람이 "다음 단계로" 버튼을 눌러야만 진행된다 — 한 번에 끝까지 자동 실행되지 않는다.

실행: uv run streamlit run app.py
"""
from dotenv import load_dotenv

load_dotenv()

import streamlit as st

from agents.scenario.agent import generate_scenario
from agents.scenario.schemas import ScenarioOutput
from agents.storyboard.agent import generate_storyboard
from agents.storyboard.schemas import Shot, StoryboardOutput
from pipeline.run_pipeline import OUTPUTS_ROOT, run_from_storyboard, slugify_logline

st.set_page_config(page_title="StoryMaker", page_icon="🎬")
st.title("🎬 StoryMaker")
st.caption("로그라인 한 줄 → 시나리오 → 스토리보드 → 애니매틱 (단계마다 검토 후 직접 진행)")

st.session_state.setdefault("stage", "input")
st.session_state.setdefault("shot_revision", 0)


def _reset_all() -> None:
    for key in list(st.session_state.keys()):
        del st.session_state[key]


def _go_to_input() -> None:
    _reset_all()


# ── 0단계: 로그라인 입력 ──────────────────────────────────────────────
st.subheader("0. 로그라인")
logline = st.text_input(
    "로그라인 또는 기획 아이디어",
    value=st.session_state.get("logline", ""),
    placeholder="겁쟁이가 용을 잡아야 한다",
    disabled=st.session_state["stage"] != "input",
)

if st.session_state["stage"] == "input":
    if st.button("1단계: 시나리오 생성", type="primary", disabled=not logline):
        with st.spinner("시나리오 생성 중..."):
            try:
                scenario: ScenarioOutput = generate_scenario(logline)
            except Exception as e:
                st.error(f"시나리오 생성 실패: {e}")
                st.stop()
        st.session_state["logline"] = logline
        st.session_state["project_dir"] = OUTPUTS_ROOT / slugify_logline(logline)
        st.session_state["scenario_text"] = scenario.scene_script
        st.session_state["stage"] = "scenario"
        st.rerun()
    st.stop()

st.button("처음부터 다시", on_click=_go_to_input)

# ── 1단계: 시나리오 검토·수정 ──────────────────────────────────────────
st.divider()
st.subheader("1. 시나리오 (검토 및 수정)")
scenario_text = st.text_area(
    "씬 대본 — 필요하면 직접 수정하세요",
    value=st.session_state["scenario_text"],
    height=300,
    key="scenario_text_input",
)
st.session_state["scenario_text"] = scenario_text

if st.session_state["stage"] == "scenario":
    col1, col2 = st.columns(2)
    if col1.button("🔄 시나리오 다시 생성"):
        with st.spinner("시나리오 재생성 중..."):
            try:
                scenario = generate_scenario(st.session_state["logline"])
            except Exception as e:
                st.error(f"시나리오 재생성 실패: {e}")
                st.stop()
        st.session_state["scenario_text"] = scenario.scene_script
        st.rerun()
    if col2.button("2단계: 스토리보드 생성 →", type="primary"):
        with st.spinner("스토리보드(샷 리스트) 생성 중..."):
            try:
                storyboard: StoryboardOutput = generate_storyboard(
                    st.session_state["scenario_text"]
                )
            except Exception as e:
                st.error(f"스토리보드 생성 실패: {e}")
                st.stop()
        st.session_state["shots"] = storyboard.shots
        st.session_state["shot_revision"] += 1
        st.session_state["stage"] = "storyboard"
        st.rerun()
    st.stop()

# ── 2단계: 스토리보드 검토·수정 ────────────────────────────────────────
st.divider()
st.subheader("2. 스토리보드 (샷 리스트 검토 및 수정)")

revision = st.session_state["shot_revision"]
edited_shots = []
for i, shot in enumerate(st.session_state["shots"], start=1):
    with st.expander(f"Cut {i} — {shot.size}, {shot.angle}, {shot.movement}", expanded=False):
        c1, c2, c3 = st.columns(3)
        size = c1.text_input("사이즈", value=shot.size, key=f"shot{i}_size_r{revision}")
        angle = c2.text_input("앵글", value=shot.angle, key=f"shot{i}_angle_r{revision}")
        movement = c3.text_input("무빙", value=shot.movement, key=f"shot{i}_movement_r{revision}")
        duration = st.number_input(
            "길이(초)", value=int(shot.duration), min_value=1, step=1,
            key=f"shot{i}_duration_r{revision}",
        )
        description = st.text_area(
            "설명", value=shot.description, key=f"shot{i}_description_r{revision}"
        )
        c4, c5 = st.columns(2)
        dialogue = c4.text_input("대사", value=shot.dialogue, key=f"shot{i}_dialogue_r{revision}")
        audio = c5.text_input("음향", value=shot.audio, key=f"shot{i}_audio_r{revision}")
        scene_slug = st.text_input(
            "씬 슬러그", value=shot.sceneSlug, key=f"shot{i}_sceneSlug_r{revision}"
        )
    edited_shots.append(
        Shot(
            size=size,
            angle=angle,
            movement=movement,
            duration=int(duration),
            description=description,
            dialogue=dialogue,
            audio=audio,
            sceneSlug=scene_slug,
        )
    )

if st.session_state["stage"] == "storyboard":
    col1, col2 = st.columns(2)
    if col1.button("🔄 스토리보드 다시 생성"):
        with st.spinner("스토리보드 재생성 중..."):
            try:
                storyboard = generate_storyboard(st.session_state["scenario_text"])
            except Exception as e:
                st.error(f"스토리보드 재생성 실패: {e}")
                st.stop()
        st.session_state["shots"] = storyboard.shots
        st.session_state["shot_revision"] += 1
        st.rerun()
    if col2.button("3단계: 애니매틱 생성 →", type="primary"):
        final_scenario = ScenarioOutput(scene_script=st.session_state["scenario_text"])
        final_storyboard = StoryboardOutput(shots=edited_shots)
        with st.spinner("이미지·타임라인·검증·렌더링 진행 중... (수 분 걸릴 수 있습니다)"):
            try:
                result = run_from_storyboard(
                    final_scenario, final_storyboard, st.session_state["project_dir"]
                )
            except Exception as e:
                st.error(f"애니매틱 생성 실패: {e}")
                st.stop()
        st.session_state["result"] = result
        st.session_state["stage"] = "done"
        st.rerun()
    st.stop()

# ── 3단계: 결과 ──────────────────────────────────────────────────────
st.divider()
st.subheader("3. 애니매틱 결과")
result = st.session_state["result"]

if result.image_failures:
    with st.expander(f"⚠️ 이미지 생성 실패 {len(result.image_failures)}건", expanded=False):
        for failure in result.image_failures:
            st.write(f"- {failure}")

if result.docx_path.exists():
    st.download_button(
        "스토리보드 워드(.docx) 다운로드",
        data=result.docx_path.read_bytes(),
        file_name=result.docx_path.name,
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    )

if result.validation_flags:
    with st.expander(f"⚠️ 타임라인 검증 플래그 {len(result.validation_flags)}건", expanded=True):
        for flag in result.validation_flags:
            st.write(f"- {flag}")

if result.video_path is not None and result.video_path.exists():
    st.video(str(result.video_path))
else:
    st.info("애니매틱 mp4가 아직 없습니다 (콘티 이미지 생성 실패 또는 렌더링 오류).")
