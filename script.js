// ==========================================================================
// StoryMaker — front-end wired to the real FastAPI backend (server.py).
// ==========================================================================

const GENRES = [
  {
    id: "monster-in-the-house",
    icon: "👹",
    name: "Monster in the House",
    subtitle: "제한된 공간에 침입한 공포",
    description: "괴물 같은 존재가 밀폐된 공간에 침입해 사람들을 위협하는 이야기입니다.",
    elements: ["괴물 (Monster)", "제한된 공간 (House)", "죄 (Sin)"],
    mistake: "\"죄(Sin)\"가 없으면 그냥 재난 영화가 됩니다. 누군가의 잘못이 위협을 불러왔다는 인과관계가 필요합니다.",
  },
  {
    id: "golden-fleece",
    icon: "🧭",
    name: "Golden Fleece",
    subtitle: "목표를 향한 여정과 성장",
    description: "주인공이 보물, 장소, 인물 등 특정 목표를 향해 길을 떠나며 스스로 변화하는 로드무비형 이야기입니다.",
    elements: ["여정 (Road)", "동료들 (Team)", "진짜 보상 (Prize)"],
    mistake: "목적지에 도착하는 것보다 \"여정 중의 변화\"가 핵심인데, 이를 놓치면 밋밋한 이동 서사가 됩니다.",
  },
  {
    id: "out-of-the-bottle",
    icon: "🧞",
    name: "Out of the Bottle",
    subtitle: "마법 같은 소원이 삶을 바꾸다",
    description: "마법, 소원, 저주 같은 초자연적 힘이 주인공의 삶에 개입해 인생의 교훈을 주는 이야기입니다.",
    elements: ["소원 (Wish)", "마법/저주 (Spell)", "교훈 (Lesson)"],
    mistake: "마법이 교훈 없이 그냥 편리한 해결 도구로만 쓰이면 이야기가 가벼워집니다.",
  },
  {
    id: "dude-with-a-problem",
    icon: "🌀",
    name: "Dude with a Problem",
    subtitle: "평범한 인물에게 닥친 거대한 위기",
    description: "평범한 사람이 갑작스러운 사건에 휘말려 생존을 위해 싸우는 이야기입니다.",
    elements: ["평범한 주인공 (Innocent Hero)", "돌발 사건 (Sudden Event)", "생사의 투쟁 (Life-or-Death Stakes)"],
    mistake: "주인공이 처음부터 특별한 능력을 가지면 \"평범함\"에서 나오는 긴장감이 사라집니다.",
  },
  {
    id: "rites-of-passage",
    icon: "🌱",
    name: "Rites of Passage",
    subtitle: "인생의 통과의례를 겪는 성장기",
    description: "죽음, 이별, 노화, 사랑 같은 인생의 변화를 받아들이는 과정을 다루는 성장 이야기입니다.",
    elements: ["인생의 문제 (Life Problem)", "잘못된 대처법 (Wrong Way to Cope)", "수용 (Acceptance)"],
    mistake: "주인공이 너무 쉽게 문제를 받아들이면 감정적 무게와 카타르시스가 사라집니다.",
  },
  {
    id: "buddy-love",
    icon: "🤝",
    name: "Buddy Love",
    subtitle: "관계를 통해 완성되는 이야기",
    description: "두 사람(연인, 친구, 파트너)의 관계가 서로를 완전하게 만드는 이야기입니다.",
    elements: ["불완전한 주인공 (Incomplete Hero)", "상대 (The Other)", "갈등 요소 (The Complication)"],
    mistake: "두 사람이 갈등 없이 너무 쉽게 어울리면 관계의 성장 곡선이 사라집니다.",
  },
  {
    id: "whydunit",
    icon: "🕵️",
    name: "Whydunit",
    subtitle: "진실을 파헤치는 인간 본성의 탐구",
    description: "\"누가\"보다 \"왜\"에 초점을 맞춰 범죄와 인간 본성의 어두운 면을 탐구하는 이야기입니다.",
    elements: ["탐구자 (Detective)", "발견 (Discovery)", "어둠으로의 하강 (Descent into Darkness)"],
    mistake: "단순히 \"범인이 누구인가\"에만 그치면 장르의 본질인 인간 본성 탐구를 놓치게 됩니다.",
  },
  {
    id: "fool-triumphant",
    icon: "🃏",
    name: "Fool Triumphant",
    subtitle: "무시당하던 자의 위대한 승리",
    description: "세상이 무시하던 순진하거나 낮은 지위의 주인공이 기존 체제를 뒤엎고 승리하는 이야기입니다.",
    elements: ["어리숙한 주인공 (Fool)", "기존 체제 (Establishment)", "반전의 승리 (Transformation)"],
    mistake: "주인공이 너무 똑똑해지거나 유능해지면 \"Fool\"의 순수한 매력이 사라집니다.",
  },
  {
    id: "institutionalized",
    icon: "🏛️",
    name: "Institutionalized",
    subtitle: "집단 속 개인의 딜레마",
    description: "개인이 조직, 집단, 가족 등 시스템 안에서 소속과 자유 사이의 갈등을 겪는 이야기입니다.",
    elements: ["집단/가족 (Group / Family)", "선택 (Choice)", "희생 (Sacrifice)"],
    mistake: "집단을 단순한 \"악\"으로만 그리면 소속과 자유 사이의 딜레마가 얕아집니다.",
  },
  {
    id: "superhero",
    icon: "🦸",
    name: "Superhero",
    subtitle: "특별한 존재가 짊어지는 세상의 무게",
    description: "특별한 능력이나 지위를 가진 주인공이 평범한 세상과 자신의 특별함 사이에서 고뇌하는 이야기입니다.",
    elements: ["특별한 능력 (Special Power)", "적대자 (Nemesis)", "세상의 무지/거부 (World's Ignorance)"],
    mistake: "적대자가 약하면 주인공의 특별함과 갈등이 제대로 부각되지 않습니다.",
  },
];

const AUDIENCES = [
  "어린이", "청소년", "20대", "30대", "40대 이상", "가족",
  "액션", "어드벤처", "클래식", "코미디", "범죄", "다큐멘터리",
  "드라마", "신앙/종교", "공포", "키즈/가족", "LGBTQ", "음악",
  "초자연/미스터리", "로맨스", "SF/판타지", "스포츠/아웃도어", "스릴러", "여행/라이프스타일",
];

const TONES = [
  "다크", "밝음", "감성적", "코미디", "현실적", "웅장한", "판타지",
];

const EXAMPLE_LOGLINE =
  "겁쟁이 청년이 마을을 지키기 위해 용과 맞서야 하며, 그 과정에서 몰랐던 용기를 발견한다.";

// ---------------------------------------------------------------------
// Shared front-end state for the 3-step pipeline (populated by real
// /api/scenario, /api/storyboard, /api/animatic responses).
// ---------------------------------------------------------------------
const AppState = {
  sceneScript: "",
  projectSlug: "",
  shots: [],
  animaticDone: false,
};

let currentStepNumber = 1;

// Assigned inside initStepNavigation(); lets result-block buttons switch
// the visible step panel without duplicating the nav logic.
let goToStep = () => {};

document.addEventListener("DOMContentLoaded", () => {
  renderGenreGrid();
  renderChipGroup("audienceChips", AUDIENCES, "audienceReadout", "선택된 관객");
  renderChipGroup("toneChips", TONES, "toneReadout", "선택된 톤");
  initCharCounter();
  initExampleButton();
  initGenerateButton();
  initSettingsChipGroups();
  initStoryboardGenerateButton();
  initAnimaticGenerateButton();
  initResultActionButtons();
  initStepNavigation();
  loadProjectArchive();
});

// ---------------------------------------------------------------------
// Genre grid + info panel
// ---------------------------------------------------------------------
function renderGenreGrid() {
  const grid = document.getElementById("genreGrid");

  GENRES.forEach((genre) => {
    const card = document.createElement("button");
    card.type = "button";
    card.className = "genre-card";
    card.dataset.id = genre.id;
    card.innerHTML = `
      <span class="genre-card-icon">${genre.icon}</span>
      <span class="genre-card-name">${genre.name}</span>
      <span class="genre-card-subtitle">${genre.subtitle}</span>
    `;
    card.addEventListener("click", () => selectGenre(genre.id));
    grid.appendChild(card);
  });
}

function selectGenre(id) {
  const genre = GENRES.find((g) => g.id === id);
  if (!genre) return;

  document.querySelectorAll(".genre-card").forEach((card) => {
    card.classList.toggle("selected", card.dataset.id === id);
  });

  document.getElementById("genreInfoName").textContent = genre.name;
  document.getElementById("genreInfoDesc").textContent = genre.description;
  document.getElementById("genreInfoMistake").textContent = genre.mistake;

  const elementsList = document.getElementById("genreInfoElements");
  elementsList.innerHTML = "";
  genre.elements.forEach((el) => {
    const li = document.createElement("li");
    li.textContent = el;
    elementsList.appendChild(li);
  });

  document.getElementById("genreInfoEmpty").hidden = true;
  document.getElementById("genreInfoBody").hidden = false;
  document.getElementById("genreInfoPanel").classList.add("active");
}

function getSelectedGenreName() {
  const card = document.querySelector(".genre-card.selected");
  return card ? card.querySelector(".genre-card-name").textContent : "";
}

// ---------------------------------------------------------------------
// Chip groups (Target Audience / Story Tone) — multi-select
// ---------------------------------------------------------------------
function renderChipGroup(containerId, items, readoutId, readoutLabel) {
  const container = document.getElementById(containerId);
  const readout = document.getElementById(readoutId);
  const selected = new Set();

  items.forEach((item) => {
    const chip = document.createElement("button");
    chip.type = "button";
    chip.className = "chip";
    chip.textContent = item;
    chip.addEventListener("click", () => {
      if (selected.has(item)) {
        selected.delete(item);
        chip.classList.remove("selected");
      } else {
        selected.add(item);
        chip.classList.add("selected");
      }
      updateReadout();
    });
    container.appendChild(chip);
  });

  function updateReadout() {
    readout.textContent =
      selected.size === 0
        ? `${readoutLabel}: 없음`
        : `${readoutLabel}: ${Array.from(selected).join(", ")}`;
  }
}

function getSelectedChipValues(containerId) {
  return Array.from(document.querySelectorAll(`#${containerId} .chip.selected`)).map(
    (chip) => chip.textContent
  );
}

// ---------------------------------------------------------------------
// Character counter
// ---------------------------------------------------------------------
function initCharCounter() {
  const textarea = document.getElementById("loglineInput");
  const counter = document.getElementById("charCount");

  textarea.addEventListener("input", () => {
    counter.textContent = textarea.value.length;
  });
}

// ---------------------------------------------------------------------
// Example Logline button
// ---------------------------------------------------------------------
function initExampleButton() {
  const button = document.getElementById("exampleBtn");
  const textarea = document.getElementById("loglineInput");
  const counter = document.getElementById("charCount");

  button.addEventListener("click", () => {
    textarea.value = EXAMPLE_LOGLINE;
    counter.textContent = textarea.value.length;
    textarea.focus();
  });
}

function showToast(message) {
  const toast = document.getElementById("toast");
  toast.textContent = message;
  toast.classList.add("show");
  clearTimeout(showToast._timer);
  showToast._timer = setTimeout(() => {
    toast.classList.remove("show");
  }, 2600);
}

// ---------------------------------------------------------------------
// Loading overlay — shows an elapsed-time counter so a genuinely slow
// (but working) Gemini call doesn't look like it's frozen.
// ---------------------------------------------------------------------
let loadingTimerId = null;
let loadingStartedAt = 0;

function showLoading(baseText) {
  loadingStartedAt = Date.now();
  updateLoadingText(baseText);
  document.getElementById("loadingOverlay").hidden = false;

  clearInterval(loadingTimerId);
  loadingTimerId = setInterval(() => updateLoadingText(baseText), 1000);
}

function updateLoadingText(baseText) {
  const elapsedSec = Math.floor((Date.now() - loadingStartedAt) / 1000);
  document.getElementById("loadingText").textContent = `${baseText} (${elapsedSec}초 경과)`;
}

function hideLoading() {
  clearInterval(loadingTimerId);
  loadingTimerId = null;
  document.getElementById("loadingOverlay").hidden = true;
}

// ---------------------------------------------------------------------
// Backend fetch helper — aborts after timeoutMs so a genuinely stuck
// request surfaces as an error instead of spinning forever.
// ---------------------------------------------------------------------
async function postJSON(url, body, timeoutMs = 180000) {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), timeoutMs);

  let response;
  try {
    response = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
      signal: controller.signal,
    });
  } catch (err) {
    if (err.name === "AbortError") {
      throw new Error("서버 응답이 너무 오래 걸려 요청을 중단했습니다. 잠시 후 다시 시도해 주세요.");
    }
    throw err;
  } finally {
    clearTimeout(timeoutId);
  }

  if (!response.ok) {
    let detail = response.statusText;
    try {
      const errorData = await response.json();
      if (errorData && errorData.detail) {
        detail = typeof errorData.detail === "string" ? errorData.detail : JSON.stringify(errorData.detail);
      }
    } catch {
      // response body wasn't JSON — keep statusText
    }
    throw new Error(detail);
  }

  return response.json();
}

// ---------------------------------------------------------------------
// Sidebar step cards + progress bar — reflect real pipeline state
// (which steps actually produced a result) instead of static mock data.
// ---------------------------------------------------------------------
function updateSidebarProgress() {
  const stepsDone = [
    Boolean(AppState.sceneScript),
    AppState.shots.length > 0,
    AppState.animaticDone,
  ];

  const sidebarCards = document.querySelectorAll(".sidebar .steps .step-card");
  sidebarCards.forEach((card, i) => {
    const stepNumber = i + 1;
    const icon = card.querySelector(".step-icon");
    const status = card.querySelector(".step-status");

    card.classList.remove("done", "active");

    if (stepsDone[i]) {
      card.classList.add("done");
      icon.textContent = "✓";
      status.textContent = "완료";
    } else if (stepNumber === currentStepNumber) {
      card.classList.add("active");
      icon.textContent = String(stepNumber);
      status.textContent = "진행 중";
    } else {
      icon.textContent = String(stepNumber);
      status.textContent = "대기 중";
    }
  });

  const completedCount = stepsDone.filter(Boolean).length;
  const percent = Math.round((completedCount / stepsDone.length) * 100);
  document.querySelector(".progress-percent").textContent = `${percent}%`;
  document.querySelector(".progress-fill").style.width = `${percent}%`;
}

// ---------------------------------------------------------------------
// Warning list rendering (image_failures / validation_flags) — shared
// by STEP 2 and STEP 3, built with textContent only (no HTML injection).
// ---------------------------------------------------------------------
function renderWarningBlock(elementId, title, items) {
  const el = document.getElementById(elementId);
  el.innerHTML = "";

  if (!items || items.length === 0) {
    el.hidden = true;
    return;
  }

  const heading = document.createElement("p");
  heading.className = "warning-block-title";
  heading.textContent = title;

  const list = document.createElement("ul");
  items.forEach((message) => {
    const li = document.createElement("li");
    li.textContent = message;
    list.appendChild(li);
  });

  el.appendChild(heading);
  el.appendChild(list);
  el.hidden = false;
}

// ==========================================================================
// STEP 1 — Scenario generation
// ==========================================================================
function initGenerateButton() {
  const button = document.getElementById("generateBtn");
  button.addEventListener("click", () => generateScenario());
}

async function generateScenario() {
  const logline = document.getElementById("loglineInput").value.trim();
  if (!logline) {
    showToast("로그라인을 입력해 주세요.");
    return;
  }

  const payload = {
    logline,
    title: document.getElementById("projectTitle").value.trim(),
    length: document.getElementById("movieLength").value,
    genre: getSelectedGenreName(),
    audience: getSelectedChipValues("audienceChips"),
    tone: getSelectedChipValues("toneChips"),
  };

  showLoading("시나리오를 생성하는 중입니다... 보통 30~60초 정도 걸려요.");
  try {
    const data = await postJSON("/api/scenario", payload);
    AppState.sceneScript = data.scene_script;
    AppState.projectSlug = data.project_slug;

    document.getElementById("scenarioResultText").value = data.scene_script;
    document.getElementById("scenarioResultBlock").hidden = false;
    document.getElementById("projectNameDisplay").textContent =
      payload.title || (logline.length > 24 ? `${logline.slice(0, 24)}…` : logline);
    updateSidebarProgress();
    loadProjectArchive();
    showToast("시나리오가 생성되었습니다.");
  } catch (err) {
    showToast(`시나리오 생성 실패: ${err.message}`);
  } finally {
    hideLoading();
  }
}

// ==========================================================================
// STEP 2 — Storyboard generation
// ==========================================================================
function initSettingsChipGroups() {
  document.querySelectorAll(".settings-chip-group").forEach((group) => {
    const isMulti = group.dataset.select === "multi";
    const chips = group.querySelectorAll(".chip");

    chips.forEach((chip) => {
      chip.addEventListener("click", () => {
        if (isMulti) {
          chip.classList.toggle("selected");
        } else {
          chips.forEach((c) => c.classList.remove("selected"));
          chip.classList.add("selected");
        }
      });
    });
  });
}

function getSelectedSettingsChipValue(fieldName) {
  const group = document.querySelector(`.settings-chip-group[data-field="${fieldName}"]`);
  if (!group) return "";
  const chip = group.querySelector(".chip.selected");
  return chip ? chip.textContent : "";
}

function initStoryboardGenerateButton() {
  const button = document.getElementById("storyboardGenerateBtn");
  if (!button) return;
  button.addEventListener("click", () => generateStoryboard());
}

async function generateStoryboard() {
  if (!AppState.sceneScript) {
    showToast("먼저 1단계에서 시나리오를 생성해 주세요.");
    return;
  }

  const payload = {
    scene_script: AppState.sceneScript,
    project_slug: AppState.projectSlug,
    shot_count: getSelectedSettingsChipValue("shotCount"),
    camera_style: getSelectedSettingsChipValue("cameraStyle"),
  };

  showLoading("스토리보드와 콘티 이미지를 생성하는 중입니다... 샷 수에 따라 1~3분 정도 걸릴 수 있어요.");
  try {
    const data = await postJSON("/api/storyboard", payload, 300000);
    AppState.shots = data.shots;

    renderStoryboardShots(data.shots);
    renderWarningBlock(
      "storyboardImageWarning",
      "⚠ 일부 콘티 이미지 생성에 실패했습니다",
      data.image_failures
    );
    document.getElementById("storyboardResultActions").hidden = false;
    updateSidebarProgress();
    loadProjectArchive();
    showToast("스토리보드가 생성되었습니다.");
  } catch (err) {
    showToast(`스토리보드 생성 실패: ${err.message}`);
  } finally {
    hideLoading();
  }
}

// Card layout mirrors the team's 5-column docx format (Cut/Video/Content/
// Audio/Time — agents/storyboard/prompts/training.md PART 8) so the on-screen
// preview and the exported .docx show the same information.
function renderStoryboardShots(shots) {
  const grid = document.getElementById("storyboardGrid");
  grid.innerHTML = "";

  shots.forEach((shot, i) => {
    const card = document.createElement("div");
    card.className = "storyboard-card";

    const thumb = document.createElement("div");
    thumb.className = "storyboard-thumb";

    const badge = document.createElement("span");
    badge.className = "storyboard-scene-badge";
    badge.textContent = `CUT ${i + 1}`;
    thumb.appendChild(badge);

    if (shot.image_url) {
      const img = document.createElement("img");
      img.src = shot.image_url;
      img.alt = `컷 ${i + 1}`;
      thumb.appendChild(img);
    } else {
      thumb.appendChild(document.createTextNode("🖼️"));
    }

    const body = document.createElement("div");
    body.className = "storyboard-body";

    if (shot.sceneSlug) {
      const scene = document.createElement("p");
      scene.className = "storyboard-scene-slug";
      scene.textContent = shot.sceneSlug;
      body.appendChild(scene);
    }

    const notation = document.createElement("p");
    notation.className = "storyboard-notation";
    notation.textContent = shot.notation || "";
    body.appendChild(notation);

    const desc = document.createElement("p");
    desc.className = "storyboard-desc";
    desc.textContent = shot.description || "";
    body.appendChild(desc);

    const audioText = [shot.dialogue, shot.audio].filter(Boolean).join(" / ");
    const audio = document.createElement("p");
    audio.className = "storyboard-audio";
    const audioLabel = document.createElement("strong");
    audioLabel.textContent = "Audio ";
    audio.appendChild(audioLabel);
    audio.appendChild(document.createTextNode(audioText || "—"));
    body.appendChild(audio);

    const time = document.createElement("p");
    time.className = "storyboard-time";
    const timeLabel = document.createElement("strong");
    timeLabel.textContent = "Time ";
    time.appendChild(timeLabel);
    time.appendChild(document.createTextNode(shot.duration ? `${shot.duration}초` : "—"));
    body.appendChild(time);

    card.appendChild(thumb);
    card.appendChild(body);
    grid.appendChild(card);
  });
}

// ==========================================================================
// STEP 3 — Animatic generation
// ==========================================================================
function initAnimaticGenerateButton() {
  const button = document.getElementById("animaticGenerateBtn");
  if (!button) return;
  button.addEventListener("click", () => generateAnimatic());
}

async function generateAnimatic() {
  if (!AppState.shots.length) {
    showToast("먼저 2단계에서 스토리보드를 생성해 주세요.");
    return;
  }

  const payload = {
    scene_script: AppState.sceneScript,
    project_slug: AppState.projectSlug,
    shots: AppState.shots,
  };

  showLoading("애니매틱을 렌더링하는 중입니다... 최대 1~2분 정도 걸릴 수 있어요.");
  try {
    const data = await postJSON("/api/animatic", payload, 240000);

    renderTimeline(AppState.shots);
    renderVideoPreview(data.video_url);
    renderDocxLink(data.docx_url);
    renderWarningBlock("validationWarning", "⚠ 타임라인 검증 경고", data.validation_flags);
    AppState.animaticDone = true;
    updateSidebarProgress();
    loadProjectArchive();
    showToast("애니매틱 생성이 완료되었습니다.");
  } catch (err) {
    showToast(`애니매틱 생성 실패: ${err.message}`);
  } finally {
    hideLoading();
  }
}

function formatTimestamp(totalSeconds) {
  const minutes = Math.floor(totalSeconds / 60);
  const seconds = Math.floor(totalSeconds % 60);
  return `${String(minutes).padStart(2, "0")}:${String(seconds).padStart(2, "0")}`;
}

function renderTimeline(shots) {
  const list = document.getElementById("timelineList");
  list.innerHTML = "";

  let elapsed = 0;
  shots.forEach((shot, i) => {
    const item = document.createElement("div");
    item.className = "timeline-item";

    const time = document.createElement("span");
    time.className = "timeline-time";
    time.textContent = formatTimestamp(elapsed);

    const dot = document.createElement("span");
    dot.className = "timeline-dot";

    const scene = document.createElement("span");
    scene.className = "timeline-scene";
    scene.textContent = shot.sceneSlug || `씬 ${i + 1}`;

    item.appendChild(time);
    item.appendChild(dot);
    item.appendChild(scene);
    list.appendChild(item);

    elapsed += shot.duration || 0;
  });
}

function renderVideoPreview(videoUrl) {
  const container = document.getElementById("videoPreview");
  container.innerHTML = "";

  if (videoUrl) {
    const video = document.createElement("video");
    video.src = videoUrl;
    video.controls = true;
    container.appendChild(video);
    return;
  }

  const icon = document.createElement("span");
  icon.className = "video-preview-icon";
  icon.textContent = "▶";
  const label = document.createElement("span");
  label.textContent = "영상 렌더링에 실패했습니다. ffmpeg 설치 상태를 확인해 주세요.";
  container.appendChild(icon);
  container.appendChild(label);
}

function renderDocxLink(docxUrl) {
  const link = document.getElementById("downloadDocxBtn");
  const actions = document.getElementById("animaticResultActions");

  if (docxUrl) {
    link.href = docxUrl;
    link.classList.remove("disabled-link");
  } else {
    link.removeAttribute("href");
    link.classList.add("disabled-link");
  }
  actions.hidden = false;
}

// ==========================================================================
// Project archive — lets a past project be reloaded without regenerating
// (avoids re-spending Gemini tokens after a page refresh).
// ==========================================================================
async function loadProjectArchive() {
  let projects;
  try {
    const response = await fetch("/api/projects");
    if (!response.ok) return;
    projects = await response.json();
  } catch {
    return;
  }

  const list = document.getElementById("archiveList");
  list.innerHTML = "";

  if (!projects.length) {
    const empty = document.createElement("p");
    empty.className = "empty-state-text";
    empty.textContent = "아직 저장된 프로젝트가 없습니다.";
    list.appendChild(empty);
    return;
  }

  projects.forEach((project) => {
    const item = document.createElement("button");
    item.type = "button";
    item.className = "archive-item";

    const title = document.createElement("p");
    title.className = "archive-item-title";
    title.textContent = project.title;

    const progress = document.createElement("p");
    progress.className = "archive-item-progress";
    if (project.has_animatic) {
      progress.textContent = "✓ 애니매틱까지 완료";
    } else if (project.has_storyboard) {
      progress.textContent = "✓ 스토리보드까지 완료";
    } else {
      progress.textContent = "시나리오만 생성됨";
    }

    item.appendChild(title);
    item.appendChild(progress);
    item.addEventListener("click", () => loadProject(project.slug));
    list.appendChild(item);
  });
}

async function loadProject(slug) {
  showLoading("저장된 프로젝트를 불러오는 중입니다...");
  try {
    const response = await fetch(`/api/projects/${encodeURIComponent(slug)}`);
    if (!response.ok) throw new Error("프로젝트를 불러오지 못했습니다.");
    const project = await response.json();

    AppState.sceneScript = project.scene_script;
    AppState.projectSlug = project.slug;
    AppState.shots = project.shots;
    AppState.animaticDone = Boolean(project.video_url || project.docx_url);

    document.getElementById("projectNameDisplay").textContent = project.title;
    document.getElementById("scenarioResultText").value = project.scene_script;
    document.getElementById("scenarioResultBlock").hidden = false;

    let targetStep = 1;
    if (project.shots.length) {
      renderStoryboardShots(project.shots);
      renderWarningBlock(
        "storyboardImageWarning",
        "⚠ 일부 콘티 이미지 생성에 실패했습니다",
        project.image_failures
      );
      document.getElementById("storyboardResultActions").hidden = false;
      targetStep = 2;
    }
    if (project.docx_url || project.video_url) {
      renderTimeline(project.shots);
      renderVideoPreview(project.video_url);
      renderDocxLink(project.docx_url);
      renderWarningBlock("validationWarning", "⚠ 타임라인 검증 경고", project.validation_flags);
      targetStep = 3;
    }

    updateSidebarProgress();
    goToStep(targetStep, true);
    showToast(`"${project.title}" 프로젝트를 불러왔습니다.`);
  } catch (err) {
    showToast(err.message);
  } finally {
    hideLoading();
  }
}

// ==========================================================================
// Result-block action buttons — regenerate / advance to next step
// ==========================================================================
function initResultActionButtons() {
  const regenerateScenarioBtn = document.getElementById("regenerateScenarioBtn");
  if (regenerateScenarioBtn) {
    regenerateScenarioBtn.addEventListener("click", () => generateScenario());
  }

  const goToStep2Btn = document.getElementById("goToStep2Btn");
  if (goToStep2Btn) {
    goToStep2Btn.addEventListener("click", () => {
      AppState.sceneScript = document.getElementById("scenarioResultText").value;
      goToStep(2, true);
    });
  }

  const regenerateStoryboardBtn = document.getElementById("regenerateStoryboardBtn");
  if (regenerateStoryboardBtn) {
    regenerateStoryboardBtn.addEventListener("click", () => generateStoryboard());
  }

  const goToStep3Btn = document.getElementById("goToStep3Btn");
  if (goToStep3Btn) {
    goToStep3Btn.addEventListener("click", () => goToStep(3, true));
  }
}

// ==========================================================================
// Single Step View navigation — clicking a sidebar step card or a top
// pipeline card shows exactly one of the three step panels (STEP 1 / STEP 2
// / STEP 3) and keeps the sidebar and pipeline cards' active state in sync.
// ==========================================================================
function initStepNavigation() {
  const panels = document.querySelectorAll(".main > .new-project-card");
  const sidebarCards = document.querySelectorAll(".sidebar .steps .step-card");
  const pipelineCards = document.querySelectorAll(".pipeline-cards .pipeline-card");

  if (!panels.length) return;

  // Derive the initial step from whichever sidebar card is already marked
  // "active" in the existing markup, so the first paint matches it exactly.
  let initialStep = 1;
  sidebarCards.forEach((card, i) => {
    if (card.classList.contains("active")) initialStep = i + 1;
  });

  function setStep(stepNumber, animate) {
    panels.forEach((panel, i) => {
      const isTarget = i === stepNumber - 1;
      panel.hidden = !isTarget;
      if (isTarget && animate) {
        panel.classList.remove("step-fade-in");
        void panel.offsetWidth; // restart the animation on repeated switches
        panel.classList.add("step-fade-in");
      }
    });

    currentStepNumber = stepNumber;
    updateSidebarProgress();

    pipelineCards.forEach((card, i) => {
      card.classList.toggle("active", i === stepNumber - 1);
    });
  }

  sidebarCards.forEach((card, i) => {
    card.addEventListener("click", () => setStep(i + 1, true));
  });

  pipelineCards.forEach((card, i) => {
    card.addEventListener("click", () => setStep(i + 1, true));
  });

  goToStep = setStep;
  setStep(initialStep, false);
}
