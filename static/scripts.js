const state = { mode: "topik", platform: "Instagram" };
const $ = (id) => document.getElementById(id);
const input = $("input");
const results = $("results");
const note = $("note");
const button = $("generate");
const EMOJIS = ["🎉", "🌷", "⚡"];

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
  const isPhoto = state.mode === "foto";
  $("inputLabel").textContent = isPhoto ? "Deskripsiin fotonya ya" : "Ceritain topiknya dong";
  input.placeholder = isPhoto
    ? "Contoh: Foto selfie di pantai saat sunset, pakai topi jerami dan senyum lebar"
    : "Contoh: Launching kopi susu gula aren di kafe baru kami";
});
bindChips("platforms", "platform");

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

function flash(target, label) {
  const original = target.dataset.label || target.textContent;
  target.dataset.label = original;
  target.textContent = label;
  setTimeout(() => { target.textContent = original; }, 1400);
}

function showLoading() {
  results.innerHTML = '<div class="loading"><div class="dots"><span></span><span></span><span></span></div>Lagi masak caption kece... 🍳</div>';
}

function render(data) {
  results.innerHTML = "";

  const detected = document.createElement("div");
  detected.className = "detected";
  detected.textContent = `Terdeteksi: ${data.category} (${Math.round(data.confidence * 100)}%)`;
  results.appendChild(detected);

  data.options.forEach((option) => {
    const full = `${option.caption}\n\n${option.hashtags.join(" ")}`;
    const card = document.createElement("article");
    card.className = "card";

    const top = document.createElement("div");
    top.className = "card-top";
    const badge = document.createElement("span");
    badge.className = "badge";
    badge.textContent = `${EMOJIS[option.id - 1]} ${option.style}`;
    const copy = document.createElement("button");
    copy.className = "copy";
    copy.textContent = "Salin";
    copy.addEventListener("click", async () => {
      flash(copy, (await copyText(full)) ? "Tersalin!" : " Gagal");
    });
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
      meta.textContent = `${full.length}/280 karakter`;
      card.appendChild(meta);
    }
    results.appendChild(card);
  });

  const bar = document.createElement("div");
  bar.className = "json-bar";
  const toggle = document.createElement("button");
  toggle.className = "chip";
  toggle.textContent = "{ } Lihat JSON";
  const copyJson = document.createElement("button");
  copyJson.className = "chip";
  copyJson.textContent = " Salin JSON";
  bar.append(toggle, copyJson);

  const pre = document.createElement("pre");
  pre.className = "hidden";
  const json = JSON.stringify(data, null, 2);
  pre.textContent = json;

  toggle.addEventListener("click", () => pre.classList.toggle("hidden"));
  copyJson.addEventListener("click", async () => {
    flash(copyJson, (await copyText(json)) ? " Tersalin!" : " Gagal");
  });
  results.append(bar, pre);
}

async function generate() {
  const topic = input.value.trim();
  note.textContent = "";
  if (topic.length < 4) {
    note.textContent = "Isi dulu dong, minimal beberapa kata";
    input.focus();
    return;
  }
  button.disabled = true;
  button.textContent = " Sebentar ya...";
  showLoading();
  try {
    const response = await fetch("/api/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ topic, platform: state.platform, mode: state.mode })
    });
    if (!response.ok) throw new Error("bad response");
    render(await response.json());
  } catch (error) {
    results.innerHTML = "";
    note.textContent = "Server lokal belum jalan atau error. Cek terminal.";
  } finally {
    button.disabled = false;
    button.textContent = " Generate 3 Opsi!";
  }
}

button.addEventListener("click", generate);
input.addEventListener("keydown", (event) => {
  if (event.key === "Enter" && (event.ctrlKey || event.metaKey)) generate();
});