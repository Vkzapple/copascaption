const state = { mode: "topic", platform: "Instagram", lang: "auto" };
const $ = (id) => document.getElementById(id);
const input = $("input");
const results = $("results");
const note = $("note");
const button = $("generate");

const BADGE_ICONS = ["fa-solid fa-face-laugh-beam", "fa-solid fa-heart", "fa-solid fa-bolt"];
const LANGUAGE_NAMES = { id: "Indonesian", en: "English" };
const INPUT_COPY = {
  topic: {
    icon: "fa-solid fa-comment-dots",
    label: "What is your topic?",
    placeholder: "e.g. Launching our new brown sugar latte at the cafe"
  },
  photo: {
    icon: "fa-solid fa-image",
    label: "Describe your photo",
    placeholder: "e.g. Selfie at the beach during sunset, wearing a straw hat and a big smile"
  }
};

function setContent(element, iconClass, text) {
  const icon = document.createElement("i");
  icon.className = iconClass;
  element.replaceChildren(icon, document.createTextNode(text));
}

function labeled(element, iconClass, text) {
  element.dataset.icon = iconClass;
  element.dataset.text = text;
  setContent(element, iconClass, text);
}

function flash(target, success) {
  setContent(
    target,
    success ? "fa-solid fa-check" : "fa-solid fa-triangle-exclamation",
    success ? "Copied!" : "Failed"
  );
  setTimeout(() => setContent(target, target.dataset.icon, target.dataset.text), 1400);
}

function bindChips(containerId, key, onChange) {
  const box = $(containerId);
  box.addEventListener("click", (event) => {
    const chip = event.target.closest(".chip");
    if (!chip) return;
    box.querySelectorAll(".chip").forEach((item) => item.classList.remove("active"));
    chip.classList.add("active");
    state[key] = chip.dataset.value;
    if (onChange) onChange();
  });
}

bindChips("modes", "mode", () => {
  const copy = INPUT_COPY[state.mode];
  setContent($("inputLabel"), copy.icon, copy.label);
  input.placeholder = copy.placeholder;
});
bindChips("platforms", "platform");
bindChips("languages", "lang");

async function copyText(text) {
  try {
    await navigator.clipboard.writeText(text);
    return true;
  } catch (error) {
    const area = document.createElement("textarea");
    area.value = text;
    area.style.position = "fixed";
    area.style.opacity = "0";
    document.body.appendChild(area);
    area.select();
    const ok = document.execCommand("copy");
    area.remove();
    return ok;
  }
}

function showLoading() {
  results.innerHTML = '<div class="loading"><div class="dots"><span></span><span></span><span></span></div>Cooking up cute captions...</div>';
}

function render(data) {
  results.innerHTML = "";

  const detected = document.createElement("div");
  detected.className = "detected";
  setContent(
    detected,
    "fa-solid fa-brain",
    `Detected: ${data.category} (${Math.round(data.confidence * 100)}%) · ${LANGUAGE_NAMES[data.language]}`
  );
  results.appendChild(detected);

  data.options.forEach((option) => {
    const full = `${option.caption}\n\n${option.hashtags.join(" ")}`;
    const card = document.createElement("article");
    card.className = "card";

    const top = document.createElement("div");
    top.className = "card-top";
    const badge = document.createElement("span");
    badge.className = "badge";
    setContent(badge, BADGE_ICONS[option.id - 1], option.style);
    const copy = document.createElement("button");
    copy.className = "copy";
    labeled(copy, "fa-solid fa-copy", "Copy");
    copy.addEventListener("click", async () => flash(copy, await copyText(full)));
    top.append(badge, copy);

    const caption = document.createElement("p");
    caption.className = "caption";
    caption.textContent = option.caption;

    const tags = document.createElement("div");
    tags.className = "tags";
    option.hashtags.forEach((tag) => {
      const el = document.createElement("span");
      el.className = "tag";
      el.textContent = tag;
      tags.appendChild(el);
    });

    card.append(top, caption, tags);

    if (data.platform === "X") {
      const meta = document.createElement("div");
      meta.className = "meta" + (full.length > 280 ? " over" : "");
      meta.textContent = `${full.length}/280 characters`;
      card.appendChild(meta);
    }
    results.appendChild(card);
  });

  const bar = document.createElement("div");
  bar.className = "json-bar";
  const toggle = document.createElement("button");
  toggle.className = "chip";
  labeled(toggle, "fa-solid fa-code", "View JSON");
  const copyJson = document.createElement("button");
  copyJson.className = "chip";
  labeled(copyJson, "fa-solid fa-copy", "Copy JSON");
  bar.append(toggle, copyJson);

  const pre = document.createElement("pre");
  pre.className = "hidden";
  const json = JSON.stringify(data, null, 2);
  pre.textContent = json;

  toggle.addEventListener("click", () => pre.classList.toggle("hidden"));
  copyJson.addEventListener("click", async () => flash(copyJson, await copyText(json)));
  results.append(bar, pre);
}

async function generate() {
  const topic = input.value.trim();
  note.textContent = "";
  if (topic.length < 4) {
    note.textContent = "Please write a few words first.";
    input.focus();
    return;
  }
  button.disabled = true;
  setContent(button, "fa-solid fa-spinner fa-spin", "Hold on...");
  showLoading();
  try {
    const response = await fetch("/api/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ topic, platform: state.platform, mode: state.mode, lang: state.lang })
    });
    if (!response.ok) throw new Error("bad response");
    render(await response.json());
  } catch (error) {
    results.innerHTML = "";
    note.textContent = "Local server is not running or returned an error. Check your terminal.";
  } finally {
    button.disabled = false;
    setContent(button, "fa-solid fa-wand-magic-sparkles", "Generate 3 Options!");
  }
}

button.addEventListener("click", generate);
input.addEventListener("keydown", (event) => {
  if (event.key === "Enter" && (event.ctrlKey || event.metaKey)) generate();
});