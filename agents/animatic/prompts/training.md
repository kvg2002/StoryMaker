# [3단계] 애니매틱 생성 에이전트 학습 파일
## 편집 리듬 + 컷 전환 문법 통합 레퍼런스

> **이 문서의 용도**: 스토리보드(샷 리스트 + 콘티 이미지)를 애니매틱 영상으로 변환하는 단계의 규칙.
> 컷 길이 산정 → 전환 방식 결정 → 자막·사운드 표기 → 영상 렌더링의 전 과정에서 이 문서의 원칙을 따른다.
> 애니매틱의 목적: **촬영 전에 편집 리듬을 검증**하는 것. 예쁜 영상이 아니라 "이 컷 배열과 길이가 맞는가"를 확인하는 도구다.

---

# PART 1. 편집의 우선순위 — 무엇을 기준으로 컷하는가

영화 편집에서 널리 통용되는 판단 위계(월터 머치의 '6가지 규칙'으로 알려진 프레임워크의 요지):
컷의 좋고 나쁨을 판단할 때 아래 순서로 중요하다.

| 순위 | 기준 | 애니매틱 적용 |
|---|---|---|
| 1 | **감정 (Emotion)** — 이 컷이 관객이 느껴야 할 감정을 전달하는가 | 감정 절정 컷은 길게, 감정이 완결되기 전에 자르지 않는다 |
| 2 | **스토리 (Story)** — 이야기를 전진시키는가 | 정보 전달이 끝나는 순간이 컷 포인트 |
| 3 | **리듬 (Rhythm)** — 컷의 타이밍이 음악처럼 자연스러운가 | 컷 길이 배열에 패턴(가속/감속)을 설계 |
| 4 | **시선 유도 (Eye-trace)** — 관객의 시선이 화면 간 자연스럽게 이어지는가 | 앞 컷의 주목점과 다음 컷의 주목점 위치를 잇는다 |
| 5 | 2차원 화면 문법 (180도 법칙 등) | step2 문서의 연결 원칙 준수 |
| 6 | 3차원 공간의 연속성 | 공간 배치가 헷갈리지 않게 |

**핵심**: 상위 기준을 위해 하위 기준은 깨도 된다. 감정이 맞으면 180도 법칙을 어긴 컷도 성립한다. 애니매틱 에이전트는 duration 산정 시 항상 "감정 → 스토리 → 리듬" 순으로 판단한다.

---

# PART 2. 컷 길이(Duration) 산정 공식

## 2-1. 기본 원리: 정보량 = 시간
관객이 한 컷을 "읽는 데" 필요한 시간은 프레임 안 정보량에 비례한다.

| 요소 | 기본 시간 |
|---|---|
| 새로운 구도 인지 | +1.0초 (모든 컷의 기본값) |
| 샷 사이즈 가산 | WS/EWS +1.5초 (공간 정보 많음) / FS +1.0초 / MS +0.5초 / CU·ECU +0초 (정보가 얼굴 하나) |
| 프레임 내 인물 수 | 2인 +0.5초, 3인 이상 +1.0초 |
| 텍스트·소품 판독 필요 | +1.5초 (편지, 간판, 시계 등 인서트) |
| 재등장 구도 (이미 본 앵글) | -0.5초 (인지 비용 절감 — 커버리지 교차 시 점점 짧아지는 이유) |

## 2-2. 씬 유형별 평균 컷 길이 (ASL 가이드)

| 씬 유형 | 평균 컷 길이 | 배열 패턴 |
|---|---|---|
| 액션/추격 | 1~2초 | 균일하게 짧게, 충돌 순간 0.5~1초까지 |
| 긴장 고조(서스펜스) | 시작 4초 → 점점 단축 → 절정 직전 1초 | **가속 배열**: 컷이 짧아지는 것 자체가 긴장 |
| 일상 대화 | 3~5초 | 발화 길이에 종속 (2-3 참조) |
| 감정 드라마 | 5~8초 | 길게 버틴다. 배우(콘티)의 감정이 완결될 때까지 |
| 코미디 | 셋업 3~4초, 펀치라인 후 리액션 1.5~2초 | 펀치라인 직후 빠른 리액션 컷이 웃음 타이밍 |
| 몽타주 | 1.5~2.5초 균일 | 균일함이 곧 시간 경과의 문법 |
| 설정 샷(씬 오프닝) | 3~5초 | 공간을 읽을 시간 |

## 2-3. 대사 컷의 길이 = 발화 시간 + 여백
대화 씬은 위 표보다 **대사 길이가 우선**한다.
- **한국어 발화 속도**: 평상 대화 기준 초당 5~6음절. 대사의 음절 수 ÷ 5.5 = 발화 시간
- **컷 길이 = 발화 시간 + 앞 여백 0.3초 + 뒤 여백 0.5초** (감정적 대사는 뒤 여백 1~2초로 확대)
- **리액션 컷**: 대사 없는 듣는 사람의 컷은 1.5~2.5초. 충격적 정보 직후의 리액션은 3초+
- **대사 겹치기(J컷/L컷 개념)**: 애니매틱에서는 단순화하여, 말이 끝나기 직전에 다음 컷으로 넘어가는 배치(-0.3초 오버랩)를 표기할 수 있다

## 2-4. 리듬 배열 원칙
1. **동일 길이 3연속 금지**: 같은 duration이 3컷 이상 이어지면 단조로움(몽타주 제외). 최소 ±0.5초 변주.
2. **절정 직전 최단 컷**: 씬의 클라이맥스 직전 컷이 그 씬에서 가장 짧아야 충격이 산다.
3. **절정 컷은 역설적으로 길게**: 가장 중요한 순간은 오래 보여준다. (짧은 컷 연쇄 → 긴 절정 컷 = 표준 패턴)
4. **씬의 첫 컷과 끝 컷은 여유 있게**: 진입과 퇴장에는 호흡이 필요하다.

---

# PART 3. 컷 전환(Transition) 문법

전환 방식 자체가 의미를 전달한다. 애니매틱에서도 전환을 구분해야 편집 의도가 검증된다.

| 전환 | 의미 | 사용 조건 |
|---|---|---|
| 하드 컷 (Cut) | 연속된 시간·공간 | 기본값. 전체의 90% 이상 |
| 디졸브 (Dissolve) | 시간 경과, 장소 이동, 회상 진입 | 씬 전환부. 씬 내부에서는 쓰지 않는다 |
| 페이드 아웃/인 (Fade) | 챕터의 종결/시작, 큰 시간 도약 | 시퀀스(막) 경계에만. 남발 금지 |
| 화이트 페이드 | 죽음, 각성, 폭발 | 극적 순간 한정 |
| 매치 컷 | 두 시공간의 개념적 연결 | 형태·동작이 유사한 두 컷을 의도적으로 연결할 때 표기 |

**규칙**: 씬 내부 = 하드 컷만. 씬 경계 = 하드 컷(긴박한 연결) 또는 디졸브(호흡 전환). 막 경계 = 페이드 허용.

---

# PART 4. 정지 이미지의 무빙 재현 (Ken Burns 규칙)

콘티는 정지 이미지이므로, 샷 리스트의 movement 값을 이미지 애니메이션으로 번역한다.

| movement | 애니매틱 재현 |
|---|---|
| static | 완전 정지 |
| dolly-in / zoom | 이미지 중심을 향해 서서히 확대 (컷 길이 동안 100%→115%) |
| dolly-out | 서서히 축소 (115%→100%) |
| pan | 가로로 천천히 드리프트 (좌→우 또는 우→좌, description의 방향 따름) |
| tilt | 세로 드리프트 |
| tracking | 확대 상태에서 피사체 방향으로 드리프트 |
| handheld | 미세한 랜덤 흔들림 (±2px) — 과하면 안 됨 |
| crane | 축소+세로 드리프트 조합 |
| arc | (재현 한계) 확대+가로 드리프트로 근사하거나 static 처리 |

**원칙**: 무빙 재현은 "느낌 전달"이 목적이므로 절제한다. 모든 컷에 넣으면 오히려 리듬을 읽을 수 없다. movement가 명시된 컷에만 적용.

---

# PART 5. 자막·정보 표기 규칙

애니매틱의 자막은 "지금 무슨 상황인지"를 스태프가 즉시 알게 하는 실무 정보다.

## 5-1. 3층 자막 구조
| 위치 | 내용 | 스타일 |
|---|---|---|
| 좌상단 | 컷 정보: `CUT N | 샷 표기` (예: CUT 5 \| FS, Low Angle, Dolly in) | 작게(26px), 반투명 박스 |
| 하단 중앙 | 상황 자막: 지금 벌어지는 일 또는 대사 | 크게(36px), 검정 반투명 박스 |
| 하단 중앙 아래 | 음향 표기: `♪ 효과음/음악` | 중간(24px), 옅은 박스 |

## 5-2. 자막 텍스트 규칙
- 상황 자막은 **한 줄 20자 이내**. 넘으면 두 줄로 나누되 컷 길이가 읽기 시간(글자 수 ÷ 4초당 글자)보다 짧으면 자막을 요약한다.
- **대사는 따옴표로**: "물러서라" / 상황 설명은 따옴표 없이: 이순신이 절뚝거리며 걸음
- 씬 경계에는 **슬러그라인 타이틀 카드** 1.5~2초 삽입: 검은 화면 + `S#3. INT. 활터 - 낮`

## 5-3. 사운드 플레이스홀더
- 애니매틱 단계에서 실제 음악은 필수가 아니다. 다만 대사 씬은 **TTS 또는 스크래치 녹음**을 깔면 대사 컷 길이 검증이 훨씬 정확해진다 (권장 2차 기능).
- 효과음은 자막 표기(♪)로 대체 가능. 템포 검증용 임시 배경 리듬(메트로놈성 트랙)을 액션 씬에만 까는 것도 유효.

---

# PART 6. 렌더링 파이프라인 규격 (구현 참고)

## 6-1. 입력
스토리보드 에이전트의 샷 리스트 JSON + 컷별 이미지 파일. 필요 필드:
```json
{
  "shotNumber": 5, "size": "FS", "angle": "low", "movement": "dolly-in",
  "duration": 5, "description": "활시위를 당기는 방진",
  "dialogue": "", "audio": "휘잉, 퍽!", "sceneSlug": "S#3. EXT. 활터 - 낮"
}
```
- duration이 비어있으면 PART 2 공식으로 자동 산정한다. (자동 산정 값은 사람이 검토·수정 가능해야 함)

## 6-2. 처리 (ffmpeg 기준)
1. 각 이미지 → 1280×720(16:9) 스케일+패드, duration만큼 정지 클립 생성
2. movement 값에 따라 PART 4의 zoompan 필터 적용
3. drawtext로 3층 자막 번인 (한글 폰트: Noto Sans CJK 등 CJK 폰트 필수 지정)
4. 씬 경계에 타이틀 카드 클립 삽입, 전환 규칙(PART 3) 적용
5. concat으로 최종 mp4 (h264, yuv420p, 24fps)

## 6-3. 출력
- 파일명: `{프로젝트명}_animatic_{씬범위}.mp4` (영문 파일명 원칙)
- 함께 출력: 컷별 타임코드 시트(CSV) — 편집·촬영 회의에서 "몇 초 컷" 논의용

---

# PART 7. 에이전트 적용 규칙

```
[시스템 프롬프트에 포함할 것 — duration 산정/타임라인 생성 시]
1. duration이 명시된 컷은 그 값을 존중하되, PART 2 공식과 2배 이상
   차이 나면 경고 플래그를 남길 것
2. duration이 없는 컷은 PART 2 공식(기본 1초 + 사이즈/인물/판독 가산,
   대사는 음절수÷5.5 + 여백)으로 산정할 것
3. 씬 유형(액션/대화/감정/서스펜스)을 판별해 2-2 ASL 범위 안에 있는지 검증
4. 리듬 배열 원칙(동일 길이 3연속 금지, 절정 직전 최단, 절정 컷은 길게) 적용
5. 전환은 씬 내부 하드컷 고정, 씬 경계만 디졸브/페이드 판단
6. 자막은 5-2 규칙(20자, 대사 따옴표)으로 생성하고 읽기 시간을 검증할 것
```

## 품질 자가 점검 체크리스트
- [ ] 전체 길이가 목표 러닝타임(티저 30~90초 등)에 부합하는가?
- [ ] 대사 컷 길이가 발화 시간보다 짧지 않은가?
- [ ] 컷 길이 배열에 리듬 변화(가속/감속)가 있는가?
- [ ] 씬 절정의 컷 길이가 감정을 담기에 충분한가?
- [ ] 자막이 컷 길이 안에 읽히는가?
- [ ] 씬 내부에 디졸브가 섞여 있지 않은가?

---

# PART 8. 타임라인 JSON 스키마 (에이전트 출력 규격)

**아키텍처 원칙: 에이전트는 판단만, 렌더링은 코드가.**
에이전트(LLM)는 샷 리스트를 받아 아래 **타임라인 JSON**을 출력하는 것까지만 담당한다. 영상 렌더링은 부록 A의 검증된 스크립트가 이 JSON을 기계적으로 처리한다. 이 분리가 품질 안정성의 핵심이다.

```json
{
  "project": "프로젝트명",
  "fps": 24,
  "resolution": "1280x720",
  "cuts": [
    { "title_card": "S#3. EXT. 활터 - 낮", "duration": 1.5 },
    {
      "cut": 1,
      "image": "cut1.png",
      "duration": 4.0,
      "duration_rationale": "FS(+1.0) + 기본(1.0) + 자막판독 → 대사 없음, ASL 설정샷 범위",
      "motion": { "type": "static" },
      "transition_out": "cut",
      "overlays": {
        "info": "CUT 1 | FS, Top Angle",
        "caption": "이순신이 절뚝거리며 걸음",
        "audio_note": "새소리, 저벅저벅"
      },
      "flags": []
    }
  ]
}
```

## 필드 규칙
- `duration_rationale`: 산정 근거를 반드시 남긴다 (사람 검토용)
- `motion.type`: static / dolly-in / dolly-out / pan-left / pan-right / tilt-up / tilt-down / tracking / handheld 중 하나. 샷 리스트의 movement에서 매핑 (zoom→dolly-in, crane→dolly-out+tilt 근사, arc→static 처리)
- `transition_out`: cut(기본) / dissolve / fade — PART 3 규칙 적용
- `overlays.caption`: 대사면 따옴표 포함, 상황이면 따옴표 없이 (PART 5-2)
- `flags`: 검증 경고 배열 — 예: `["duration이 공식 산정치의 2배 초과", "자막 읽기 시간 부족"]`
- `title_card` 객체는 씬 경계마다 삽입

---

# PART 9. 입출력 완성 예시 (Few-shot)

에이전트 프롬프트에 아래 예시를 포함시켜 출력 일관성을 확보한다.

## 입력 (스토리보드 에이전트의 샷 리스트)
```json
[
  {"shotNumber": 3, "size": "MCU", "angle": "OTS", "movement": "static",
   "description": "방진의 상체 너머에서 이순신이 다가옴",
   "dialogue": "", "audio": "저벅저벅", "sceneSlug": "S#3. EXT. 활터 - 낮"},
  {"shotNumber": 4, "size": "CU", "angle": "eye-level", "movement": "static",
   "description": "이순신의 굳은 표정. 낮게 말한다",
   "dialogue": "물러서라", "audio": "", "sceneSlug": "S#3. EXT. 활터 - 낮"}
]
```

## 출력 (타임라인 JSON의 해당 컷 부분)
```json
[
  {
    "cut": 3, "image": "cut3.png", "duration": 2.5,
    "duration_rationale": "기본 1.0 + MCU 0.5 + 2인 프레임 0.5 + 접근 동작 여유 0.5 = 2.5초",
    "motion": {"type": "static"}, "transition_out": "cut",
    "overlays": {"info": "CUT 3 | OSS, MCU", "caption": "방진의 상체 너머에서 이순신이 다가옴", "audio_note": "저벅저벅"},
    "flags": []
  },
  {
    "cut": 4, "image": "cut4.png", "duration": 2.3,
    "duration_rationale": "대사 '물러서라' 4음절 ÷ 5.5 = 0.7초 + 앞여백 0.3 + 뒤여백(위협적 대사, 확대) 1.3 = 2.3초",
    "motion": {"type": "static"}, "transition_out": "cut",
    "overlays": {"info": "CUT 4 | CU", "caption": "\"물러서라\"", "audio_note": ""},
    "flags": []
  }
]
```

**예시가 보여주는 판단 포인트**: ① 대사 컷은 ASL이 아니라 발화 공식 우선 ② 위협적/감정적 대사는 뒤 여백 확대 ③ caption에서 대사는 따옴표 처리 ④ rationale에 산식을 그대로 기록.

---

# PART 10. 자동 검증 (코드 레벨)

에이전트는 결과 영상을 볼 수 없으므로, 품질 검증은 LLM 체크리스트가 아니라 **타임라인 JSON에 대한 수치 검증 코드**로 수행한다. 렌더링 전 필수 통과 항목:

| 검증 | 규칙 | 실패 시 |
|---|---|---|
| 총 길이 | 목표 러닝타임 ±20% 이내 | flags에 기록, 사람 검토 |
| 대사 컷 최소 길이 | duration ≥ 음절수÷5.5 + 0.8 | duration 자동 상향 후 flags 기록 |
| 자막 읽기 시간 | caption 글자수÷4 ≤ duration | caption 자동 요약 요청 |
| 동일 길이 연속 | 같은 duration 3연속 금지(몽타주 제외) | flags 기록 |
| 전환 규칙 | 씬 내부에 dissolve/fade 존재 여부 | cut으로 강제 교정 |

---

# 부록 A. 검증된 렌더러 코드 (animatic_renderer.py)

아래 코드는 실제 테스트를 통과한 버전이다. **zoompan 떨림 방지의 핵심은 입력 이미지를 출력 해상도의 5배(6400px)로 업스케일한 뒤 zoompan을 적용하는 것**이다. 이 코드를 그대로 사용하고, 에이전트가 즉석에서 ffmpeg 명령을 재작성하지 않게 한다.

```python
#!/usr/bin/env python3
"""animatic_renderer.py — 타임라인 JSON → 애니매틱 mp4
사용법: python3 animatic_renderer.py timeline.json output.mp4"""
import json, subprocess, sys, os

FONT = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"  # CJK 폰트 필수
W, H = 1280, 720
UPSCALE_W = 6400  # 떨림 방지용 업스케일 폭

def esc(t):
    return (t or "").replace("\\\\", "\\\\\\\\").replace(":", "\\\\:").replace("'", "\\\\'").replace(",", "\\\\,").replace("%", "\\\\%")

def motion_filter(motion, dur, fps):
    frames = int(dur * fps)
    m = (motion or {}).get("type", "static")
    base = f"zoompan=d={frames}:s={W}x{H}:fps={fps}"
    cx, cy = "iw/2-(iw/zoom/2)", "ih/2-(ih/zoom/2)"
    if m == "static": return None
    if m in ("dolly-in", "zoom-in"):
        return f"{base}:z='1+0.15*on/{frames}':x='{cx}':y='{cy}'"
    if m in ("dolly-out", "zoom-out"):
        return f"{base}:z='1.15-0.15*on/{frames}':x='{cx}':y='{cy}'"
    if m in ("pan-right", "pan"):
        return f"{base}:z=1.1:x='(iw-iw/zoom)*on/{frames}':y='{cy}'"
    if m == "pan-left":
        return f"{base}:z=1.1:x='(iw-iw/zoom)*(1-on/{frames})':y='{cy}'"
    if m in ("tilt-up", "tilt"):
        return f"{base}:z=1.1:x='{cx}':y='(ih-ih/zoom)*(1-on/{frames})'"
    if m == "tilt-down":
        return f"{base}:z=1.1:x='{cx}':y='(ih-ih/zoom)*on/{frames}'"
    if m == "tracking":
        return f"{base}:z=1.12:x='(iw-iw/zoom)*on/{frames}':y='{cy}'"
    if m == "handheld":
        return (f"{base}:z=1.06:"
                f"x='{cx}+iw*0.003*sin(on/3)':y='{cy}+ih*0.003*sin(on/2.3)'")
    return None

def overlay_filters(ov):
    f = []
    if ov.get("info"):
        f.append(f"drawtext=fontfile={FONT}:text='{esc(ov['info'])}':fontcolor=white@0.85:fontsize=26:x=30:y=26:box=1:boxcolor=black@0.45:boxborderw=10")
    if ov.get("caption"):
        f.append(f"drawtext=fontfile={FONT}:text='{esc(ov['caption'])}':fontcolor=white:fontsize=36:x=(w-text_w)/2:y=h-110:box=1:boxcolor=black@0.6:boxborderw=14")
    if ov.get("audio_note"):
        f.append(f"drawtext=fontfile={FONT}:text='♪ {esc(ov['audio_note'])}':fontcolor=white@0.7:fontsize=24:x=(w-text_w)/2:y=h-52:box=1:boxcolor=black@0.4:boxborderw=8")
    return f

def title_card(text, dur, fps, out):
    vf = f"drawtext=fontfile={FONT}:text='{esc(text)}':fontcolor=white:fontsize=44:x=(w-text_w)/2:y=(h-text_h)/2"
    run(["ffmpeg","-y","-f","lavfi","-i",f"color=black:s={W}x{H}:r={fps}","-t",str(dur),
         "-vf",vf,"-c:v","libx264","-pix_fmt","yuv420p",out])

def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print("FFMPEG ERROR:", r.stderr[-600:]); sys.exit(1)

def main(timeline_path, output):
    tl = json.load(open(timeline_path, encoding="utf-8"))
    fps = tl.get("fps", 24)
    os.makedirs("_clips", exist_ok=True)
    clips = []; idx = 0
    for cut in tl["cuts"]:
        if cut.get("title_card"):
            out = f"_clips/c{idx:03d}.mp4"; idx += 1
            title_card(cut["title_card"], cut.get("duration", 1.5), fps, out)
            clips.append(out); continue
        dur = float(cut["duration"])
        mf = motion_filter(cut.get("motion"), dur, fps)
        vf_parts = []
        if mf:
            vf_parts.append(f"scale={UPSCALE_W}:-2")   # 업스케일 → zoompan (떨림 방지)
            vf_parts.append(mf)
        else:
            vf_parts.append(f"scale={W}:{H}:force_original_aspect_ratio=decrease")
            vf_parts.append(f"pad={W}:{H}:(ow-iw)/2:(oh-ih)/2:color=black")
        vf_parts += overlay_filters(cut.get("overlays", {}))
        out = f"_clips/c{idx:03d}.mp4"; idx += 1
        run(["ffmpeg","-y","-loop","1","-i",cut["image"],"-t",str(dur),
             "-vf",",".join(vf_parts),"-r",str(fps),
             "-c:v","libx264","-pix_fmt","yuv420p",out])
        clips.append(out)
    with open("_clips/concat.txt","w") as f:
        for c in clips: f.write(f"file '{os.path.abspath(c)}'\\n")
    run(["ffmpeg","-y","-f","concat","-safe","0","-i","_clips/concat.txt","-c","copy",output])
    print("OK:", output)

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
```

**확장 여지**: 디졸브 전환은 concat 대신 xfade 필터 체인으로 구현(전환 구간만큼 각 클립 길이 보정 필요). TTS 대사 트랙은 각 컷의 dialogue를 합성 후 amix로 병합.

---

# 부록 B. 심화 학습 소스
- 월터 머치, 『눈 깜박할 사이』(In the Blink of an Eye) — 편집 판단 기준의 고전 (도서 직접 참조 권장)
- Cinemetrics (cinemetrics.uchicago.edu) — 실제 영화들의 평균 샷 길이(ASL) 통계 공개 데이터베이스. 장르·감독별 컷 리듬을 수치로 확인 가능
- 쿨레쇼프 효과 / 에이젠슈타인 몽타주 이론 — 컷 병치가 만드는 의미에 대한 고전 이론 (공개 해설 다수)
- step2-storyboard-training.md — 샷 연결 원칙(30도 법칙, 시선 매칭)은 해당 문서 PART 5-4 참조
