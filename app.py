"""StoryMaker 웹 UI: 로그라인 입력 -> 시나리오/스토리보드/애니매틱 생성 결과 확인.

실행: uv run streamlit run app.py
"""
from dotenv import load_dotenv

load_dotenv()

import streamlit as st

from pipeline.run_pipeline import PipelineResult, run

st.set_page_config(page_title="StoryMaker", page_icon="🎬")
st.title("🎬 StoryMaker")
st.caption("로그라인 한 줄 → 시나리오 → 스토리보드 → 애니매틱")

logline = st.text_input("로그라인 또는 기획 아이디어", placeholder="겁쟁이가 용을 잡아야 한다")
generate_clicked = st.button("생성 시작", type="primary", disabled=not logline)

if generate_clicked:
    with st.spinner("파이프라인 실행 중... (샷 개수에 따라 수 분 걸릴 수 있습니다)"):
        try:
            result: PipelineResult = run(logline)
        except Exception as e:
            st.error(f"생성 중 오류가 발생했습니다: {e}")
            result = None

    if result is not None:
        st.session_state["result"] = result

result: PipelineResult | None = st.session_state.get("result")

if result is not None:
    st.divider()
    st.subheader("1. 시나리오")
    with st.expander("씬 대본 보기", expanded=False):
        st.text(result.scenario.scene_script)

    st.subheader("2. 스토리보드")
    images_dir = result.project_dir / "images"
    for i, shot in enumerate(result.storyboard.shots, start=1):
        cols = st.columns([1, 2])
        image_path = images_dir / f"cut{i}.png"
        with cols[0]:
            if image_path.exists():
                st.image(str(image_path), caption=f"Cut {i}")
            else:
                st.info(f"Cut {i} 이미지 없음")
        with cols[1]:
            st.markdown(f"**{shot.size}, {shot.angle}, {shot.movement}** ({shot.duration}초)")
            st.write(shot.description)
            if shot.dialogue:
                st.write(f"대사: {shot.dialogue}")
            if shot.audio:
                st.caption(f"음향: {shot.audio}")

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

    st.subheader("3. 애니매틱")
    if result.validation_flags:
        with st.expander(f"⚠️ 타임라인 검증 플래그 {len(result.validation_flags)}건", expanded=True):
            for flag in result.validation_flags:
                st.write(f"- {flag}")

    if result.video_path is not None and result.video_path.exists():
        st.video(str(result.video_path))
    else:
        st.info("애니매틱 mp4가 아직 없습니다 (콘티 이미지 생성 실패 또는 렌더링 오류).")
