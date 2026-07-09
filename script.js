// ==========================================================================
// StoryMaker — static front-end only. No backend, no API, no AI calls.
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

document.addEventListener("DOMContentLoaded", () => {
  renderGenreGrid();
  renderChipGroup("audienceChips", AUDIENCES, "audienceReadout", "선택된 관객");
  renderChipGroup("toneChips", TONES, "toneReadout", "선택된 톤");
  initCharCounter();
  initExampleButton();
  initGenerateButton();
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

// ---------------------------------------------------------------------
// Generate button — UI-only feedback, no backend/API involved
// ---------------------------------------------------------------------
function initGenerateButton() {
  const button = document.getElementById("generateBtn");
  button.addEventListener("click", () => {
    showToast("UI 프로토타입입니다 — 백엔드는 추후 연동됩니다.");
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

// ==========================================================================
// STEP 2 (스토리보드 생성) & STEP 3 (애니매틱 생성) — additive only.
// Nothing above this line is modified. Still no backend, no API, no AI calls.
// ==========================================================================

const PROTOTYPE_TOAST_MESSAGE = "UI Prototype입니다. 백엔드는 추후 연결됩니다.";

document.addEventListener("DOMContentLoaded", () => {
  initSettingsChipGroups();
  initStoryboardGenerateButton();
  initAnimaticGenerateButton();
});

// ---------------------------------------------------------------------
// Settings chip groups (STEP 2 shot/style options, STEP 3 video options)
// data-select="single" -> only one chip active at a time (radio-like)
// data-select="multi"  -> chips toggle independently (checkbox-like)
// ---------------------------------------------------------------------
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

// ---------------------------------------------------------------------
// STEP 2 — Storyboard generate button (UI-only, no backend/API)
// ---------------------------------------------------------------------
function initStoryboardGenerateButton() {
  const button = document.getElementById("storyboardGenerateBtn");
  if (!button) return;
  button.addEventListener("click", () => {
    showToast(PROTOTYPE_TOAST_MESSAGE);
  });
}

// ---------------------------------------------------------------------
// STEP 3 — Animatic generate button (UI-only, no backend/API)
// ---------------------------------------------------------------------
function initAnimaticGenerateButton() {
  const button = document.getElementById("animaticGenerateBtn");
  if (!button) return;
  button.addEventListener("click", () => {
    showToast(PROTOTYPE_TOAST_MESSAGE);
  });
}

// ==========================================================================
// Single Step View navigation — additive only.
// Clicking a sidebar step card or a top pipeline card shows exactly one of
// the three step panels (STEP 1 / STEP 2 / STEP 3) and keeps the sidebar
// and pipeline cards' active state in sync. Nothing above this line is
// touched; no backend, no API.
// ==========================================================================

document.addEventListener("DOMContentLoaded", () => {
  initStepNavigation();
});

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

    sidebarCards.forEach((card, i) => {
      card.classList.toggle("active", i === stepNumber - 1);
    });

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

  setStep(initialStep, false);
}
