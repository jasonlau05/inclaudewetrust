// Alex · Intaglio Note
// Profile fields use the knowledge base's PROFILE-SCHEMA keys so Gemini can map them to PS-xxx.
const FIELDS = [
  ["age", "PS-001", "Age", "number"],
  ["life_stage", "PS-002", "Life stage", ["student", "early career", "mid-career", "pre-retirement", "retired", "other"]],
  ["household_status", "PS-003", "Household"],
  ["occupation", "PS-007", "Occupation"],
  ["income", "PS-005", "Income"],
  ["income_stability", "PS-006", "Income stability"],
  ["essential_expenses", "PS-009", "Essential expenses"],
  ["cash_reserves", "PS-010", "Cash reserves"],
  ["debts", "PS-011", "Debts (type, balance, APR)", "textarea"],
  ["employer_match", "PS-013", "Employer match"],
  ["available_accounts", "PS-014", "Available accounts", "textarea"],
  ["current_assets", "PS-017", "Current assets", "textarea"],
  ["goals", "PS-022", "Goals and timing", "textarea"],
  ["retirement_plan", "PS-023", "Retirement plan"],
  ["risk_tolerance", "PS-025", "Risk tolerance", ["low", "moderate", "high"]],
  ["dependents", "PS-020", "Dependents"],
  ["contribution_capacity", "PS-031", "Can invest per month"],
  ["tax_profile", "PS-016", "Tax: filing status, bracket, state"],
];

const STARTERS = [
  "What should I do with an extra $500 a month?",
  "Am I too concentrated in my employer's stock?",
  "How do VTI and VXUS compare for my situation?",
  "Is my 401(k) too aggressive for my timeline?",
];

const TOOL_BLURB = {
  get_quotes: "Price, day change, 52-week range, P/E, yield and beta for up to 10 tickers.",
  get_performance: "Historical returns, volatility and worst drawdown for one ticker, up to 10 years.",
  get_fund_info: "Fund expense ratio, category, asset mix, top sectors and top 10 holdings.",
  get_news: "Recent headlines for a ticker, company or topic.",
};
const plural = (n, one, many = `${one}s`) => `${n} ${n === 1 ? one : many}`;

const CITE_RE = /\b(?:R|PB|GR|PS|RN)-\d{3}\b|\bMCP-[A-Z]+\b/g;
const CITE_TEST = new RegExp(CITE_RE.source); // non-global: .test() without lastIndex state

const $ = (sel) => document.querySelector(sel);
const form = $("#profile");
const log = $("#log");
const rail = $("#evidence");

let kb = {};
let status = null;
let messages = [];   // [{role, text}] sent to the API
let answers = [];    // [{serial, data, cited, el}]
let selected = -1;

// ── Guilloché ───────────────────────────────────────────────────────────────

function curve(radius, amp, freq, phase, steps = 360) {
  let d = "";
  for (let i = 0; i <= steps; i++) {
    const t = (i / steps) * Math.PI * 2;
    const r = radius + amp * Math.sin(freq * t + phase);
    d += `${i ? "L" : "M"}${(r * Math.cos(t)).toFixed(2)} ${(r * Math.sin(t)).toFixed(2)}`;
  }
  return d + "Z";
}

// The provenance mark: outer petals encode rules cited, inner rings encode market calls.
function rosette(petals, rings, cls = "") {
  const k = Math.min(Math.max(petals, 3), 24);
  const outer = [0, 1, 2].map((j) => `<path pathLength="1" d="${curve(33, 9, k, (j * Math.PI) / k / 1.5)}"/>`).join("");
  const inner = Array.from({ length: Math.min(rings, 8) }, (_, j) =>
    `<path pathLength="1" d="${curve(8 + j * 3.2, 1.3, k * 2 + j * 2, j)}"/>`).join("");
  return `<svg class="${cls}" viewBox="-50 -50 100 100" aria-hidden="true">
    <g fill="none" stroke="#1f3a2e" stroke-width=".55"><circle pathLength="1" r="47"/><circle pathLength="1" r="44.5"/>${outer}</g>
    <g fill="none" stroke="#7f5300" stroke-width=".9">${inner}</g></svg>`;
}

function drawBand() {
  const svg = $("#band-guilloche");
  svg.setAttribute("viewBox", "0 0 1440 72");
  let paths = "";
  for (let j = 0; j < 7; j++) {
    let d = "";
    for (let x = 0; x <= 1440; x += 6) {
      const y = 36 + 22 * Math.sin(x / 38 + j * 0.9) * Math.cos(x / 410 + j * 0.35);
      d += `${x ? "L" : "M"}${x} ${y.toFixed(1)}`;
    }
    paths += `<path d="${d}"/>`;
  }
  svg.innerHTML = `<g fill="none" stroke="#fff" stroke-width=".6">${paths}</g>`;
}

// ── Helpers ─────────────────────────────────────────────────────────────────

const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[c]);
const serialOf = (n) => `A ${String(n).padStart(4, "0")}`;

function parseResult(text) {
  if (!text) return null;
  try { return JSON.parse(text.replace(/^ERROR: /, "")); } catch { return null; }
}

function fmtET(iso) {
  const d = new Date(iso);
  if (Number.isNaN(d.getTime())) return iso;
  return d.toLocaleString("en-US", { timeZone: "America/New_York", month: "short", day: "numeric", hour: "numeric", minute: "2-digit" }) + " ET";
}

// Latest market timestamp any tool returned, for the note's serial line.
function dataAsOf(calls) {
  const stamps = [];
  for (const c of calls) {
    const r = parseResult(c.result);
    for (const q of r?.quotes ?? []) if (q.quote_time) stamps.push(q.quote_time);
    if (r?.as_of && /T/.test(r.as_of)) stamps.push(r.as_of);
  }
  return stamps.sort().at(-1);
}

function argSummary(call) {
  const a = call.args || {};
  if (a.symbols) return a.symbols.join(", ");
  if (a.symbol) return a.symbol;
  if (a.query) return `“${a.query}”${a.limit ? `, ${a.limit} headlines` : ""}`;
  return JSON.stringify(a);
}

function callNote(call) {
  const r = parseResult(call.result);
  if (!r) return "No result captured";
  if (call.result.startsWith("ERROR") || r.error) return `Failed: ${r.error ?? "tool error"}`;
  const bad = (r.quotes ?? []).filter((q) => q.error).map((q) => q.symbol);
  const when = r.quotes?.[0]?.quote_time ?? r.as_of ?? r.retrieved_at;
  const parts = ["Yahoo Finance, delayed"];
  if (when) parts.push(/T/.test(when) ? fmtET(when) : when);
  if (bad.length) parts.push(`not found: ${bad.join(", ")}`);
  return parts.join(" · ");
}

function citedIds(text) {
  return [...new Set(text.match(CITE_RE) ?? [])].filter((id) => kb[id]);
}

// Wrap every known KB id in the rendered answer as a focusable citation.
function linkCitations(root) {
  const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
  const nodes = [];
  while (walker.nextNode()) if (CITE_TEST.test(walker.currentNode.nodeValue)) nodes.push(walker.currentNode);
  for (const node of nodes) {
    CITE_RE.lastIndex = 0;
    const frag = document.createDocumentFragment();
    let last = 0;
    for (const m of node.nodeValue.matchAll(CITE_RE)) {
      frag.append(node.nodeValue.slice(last, m.index));
      if (kb[m[0]]) {
        const b = document.createElement("button");
        b.type = "button";
        b.className = "cite";
        b.dataset.id = m[0];
        b.textContent = m[0];
        b.title = kb[m[0]];
        frag.append(b);
      } else frag.append(m[0]);
      last = m.index + m[0].length;
    }
    frag.append(node.nodeValue.slice(last));
    node.replaceWith(frag);
  }
  CITE_RE.lastIndex = 0;
}

// ── Evidence rail ───────────────────────────────────────────────────────────

function evidenceHTML(a, { withMark = true } = {}) {
  const calls = a.data.tool_calls;
  const tools = calls.map((c) => {
    const failed = c.result?.startsWith("ERROR");
    return `<div class="ev-item${failed ? " err" : ""}" data-tool="${esc(c.name)}">
      <span class="id">${esc(c.name)}</span> <span class="what">${esc(argSummary(c))}</span>
      <span class="when">${esc(callNote(c))}</span>
      <details><summary>Raw result</summary><pre>${esc(JSON.stringify(parseResult(c.result) ?? c.result, null, 2))}</pre></details>
    </div>`;
  }).join("");
  const rules = a.cited.map((id) => `<div class="ev-item ev-rule" data-id="${id}"><span class="id">${id}</span><span class="what">${esc(kb[id])}</span></div>`).join("");
  const t = a.data.tokens || {};
  return `${withMark ? `<div class="provenance">${rosette(a.cited.length, calls.length, "settle")}
      <p><b>${plural(calls.length, "market call")} · ${plural(a.cited.length, "KB citation")}</b>
      Each outer petal is a knowledge-base ID this answer cites; each inner ring is a market-data call.</p></div>` : ""}
    <section class="ev-section"><h3 class="pane-title">Market data</h3>${tools || `<p class="muted">No market data needed for this answer.</p>`}</section>
    <section class="ev-section"><h3 class="pane-title">Knowledge base</h3>${rules || `<p class="muted">No rule IDs cited.</p>`}</section>
    <dl class="ev-meta"><dt>Model</dt><dd>${esc(a.data.model)}</dd><dt>Time</dt><dd>${(a.data.elapsed_ms / 1000).toFixed(1)} s</dd>
      <dt>Tokens</dt><dd>${t.prompt ?? "?"} in${t.cached ? ` (${t.cached} cached)` : ""} · ${t.output ?? "?"} out</dd></dl>`;
}

function renderRail() {
  if (selected < 0) {
    const tools = (status?.tools ?? []).map((t) => `<div class="ev-item"><span class="id">${esc(t.name)}</span><p>${esc(TOOL_BLURB[t.name] ?? t.description.replace(/[`\s]+/g, " ").split(/(?<=\.)\s/)[0])}</p></div>`).join("");
    const count = (p) => Object.keys(kb).filter((k) => k.startsWith(p)).length;
    rail.innerHTML = `<h2 class="pane-title" id="evidence-title">Evidence</h2>
      <div class="provenance">${rosette(8, 3)}<p><b>Every answer gets a mark</b>Its petals count the knowledge-base IDs it cites; its rings count the market-data calls behind it.</p></div>
      <section class="ev-section tool-list"><h3 class="pane-title">Market data tools</h3>${tools || `<p class="muted">Connecting…</p>`}</section>
      <section class="ev-section"><h3 class="pane-title">Knowledge base</h3>
        <dl class="ev-meta"><dt>Rules</dt><dd>${count("R-")}</dd><dt>Playbooks</dt><dd>${count("PB-")}</dd><dt>Guardrails</dt><dd>${count("GR-")}</dd><dt>Profile fields</dt><dd>${count("PS-")}</dd></dl></section>`;
    return;
  }
  const a = answers[selected];
  rail.innerHTML = `<h2 class="pane-title" id="evidence-title" tabindex="-1">Evidence for ${a.serial}</h2>${evidenceHTML(a)}`;
}

function select(i) {
  selected = i;
  answers.forEach((a, j) => a.el.classList.toggle("selected", j === i));
  renderRail();
}

const railHidden = () => getComputedStyle(rail).display === "none";

// Clicking a note's mark: show its evidence wherever evidence lives at this width.
function showEvidence(i) {
  if (railHidden()) {
    const box = answers[i].el.querySelector(".inline-evidence");
    box.open = true;
    box.scrollIntoView({ block: "start", behavior: "smooth" });
    return;
  }
  select(i); // re-render replays the settle animation
  rail.scrollTo({ top: 0, behavior: "smooth" });
  $("#evidence-title").focus({ preventScroll: true });
}

function focusCite(id, on) {
  rail.classList.toggle("focusing", on);
  document.querySelectorAll("#evidence .ev-item, .inline-evidence .ev-item")
    .forEach((el) => el.classList.toggle("lit", on && el.dataset.id === id));
  document.querySelectorAll(`.cite[data-id="${id}"]`).forEach((el) => el.classList.toggle("lit", on));
  if (on) rail.querySelector(`.ev-item[data-id="${id}"]`)?.scrollIntoView({ block: "nearest", behavior: "smooth" });
}

// ── Profile ─────────────────────────────────────────────────────────────────

function buildForm() {
  for (const [key, code, label, kind] of FIELDS) {
    const row = document.createElement("div");
    row.className = "field";
    let el;
    if (Array.isArray(kind)) {
      el = document.createElement("select");
      el.add(new Option("unknown", ""));
      for (const opt of kind) el.add(new Option(opt, opt));
      el.classList.add("unknown");
      el.addEventListener("change", () => el.classList.toggle("unknown", !el.value));
    } else if (kind === "textarea") {
      el = document.createElement("textarea");
      el.rows = 1;
      el.placeholder = "unknown";
    } else {
      el = document.createElement("input");
      el.type = kind === "number" ? "number" : "text";
      el.placeholder = "unknown";
      if (kind === "number") el.min = 0;
    }
    el.id = `f-${key}`;
    el.name = key;
    row.innerHTML = `<code>${code}</code><label for="f-${key}">${label}</label>`;
    row.append(el);
    form.append(row);
  }
}

function readProfile() {
  const out = {};
  for (const [key, , , kind] of FIELDS) {
    const v = form.elements[key].value.trim();
    if (v) out[key] = kind === "number" ? Number(v) : v;
  }
  return out;
}

function fillProfile(p) {
  for (const [key] of FIELDS) {
    const el = form.elements[key];
    el.value = p[key] ?? "";
    el.classList.toggle("unknown", el.tagName === "SELECT" && !el.value);
  }
}

function setPersona(btn) {
  document.querySelectorAll("#personas button").forEach((b) => b.setAttribute("aria-pressed", String(b === btn)));
}

// ── Conversation ────────────────────────────────────────────────────────────

function addNode(html, cls) {
  $("#welcome")?.remove();
  const div = document.createElement("div");
  div.className = cls;
  div.innerHTML = html;
  log.append(div);
  div.scrollIntoView({ block: "end", behavior: "smooth" });
  return div;
}

function resetChat() {
  messages = [];
  answers = [];
  selected = -1;
  log.innerHTML = "";
  log.append(welcomeNode());
  $("#session").textContent = "NO NOTES ISSUED";
  renderRail();
}

function welcomeNode() {
  const s = document.createElement("section");
  s.className = "welcome";
  s.id = "welcome";
  s.innerHTML = `<h2>Ask about your money. See every rule and number behind the answer.</h2>
    <p>Pick a sample person on the left or fill in your own situation. Alex answers from a curated investing knowledge base and pulls delayed market data from Yahoo Finance as it needs it.</p>
    <div class="starters">${STARTERS.map((q) => `<button type="button">${esc(q)}</button>`).join("")}</div>`;
  s.querySelectorAll(".starters button").forEach((b) => b.addEventListener("click", () => ask(b.textContent)));
  return s;
}

async function ask(text) {
  const q = text.trim();
  if (!q || $("#send").disabled) return;
  messages.push({ role: "user", text: q });
  addNode(esc(q), "question");
  const serial = serialOf(answers.length + 1);
  const note = addNode(`<div class="note-head"><span class="serial">${serial} · PENDING</span></div>
    <div class="pending">${rosette(8, 3, "engrave")}<p><b>Alex is working · <span class="elapsed" aria-live="off">0</span> s</b><br>
    Reading the profile, applying the knowledge base, and fetching market data where it's needed.</p></div>`, "note");
  note.setAttribute("aria-busy", "true");
  const started = performance.now();
  const timer = setInterval(() => { note.querySelector(".elapsed").textContent = Math.round((performance.now() - started) / 1000); }, 500);
  $("#send").disabled = true;

  try {
    const res = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ profile: readProfile(), messages }),
    });
    const data = await res.json().catch(() => ({}));
    if (!res.ok) throw Object.assign(new Error(data.detail || `Server returned ${res.status}`), { status: res.status });
    messages.push({ role: "assistant", text: data.reply });
    issue(note, serial, data);
  } catch (err) {
    messages.pop();
    note.classList.add("failed");
    note.innerHTML = `<div class="note-head"><span class="serial">${serial} · NOT ISSUED</span></div>
      <div class="prose">${esc(failureCopy(err))}</div>
      <button class="secondary retry" type="button">Try again</button>`;
    note.querySelector(".retry").addEventListener("click", () => { note.previousElementSibling?.remove(); note.remove(); ask(q); });
  } finally {
    note.removeAttribute("aria-busy");
    clearInterval(timer);
    $("#send").disabled = false;
  }
}

function failureCopy(err) {
  if (err.status === 429) return "Alex has used up today's Gemini quota. Wait a minute and try again; your profile and question are kept.";
  if (err.status === 502) return "The model or market-data service failed. Try again.";
  if (!err.status) return "Alex couldn't reach the server. Check that it's running, then try again.";
  return "Something went wrong on the server. Try again.";
}

function issue(note, serial, data) {
  const a = { serial, data, cited: citedIds(data.reply), el: note };
  const i = answers.push(a) - 1;
  const asOf = dataAsOf(data.tool_calls);
  note.innerHTML = `<div class="note-head">
      <div><span class="serial">${serial}${asOf ? ` · DATA ${esc(fmtET(asOf).toUpperCase())}` : ""}</span>
      <div class="note-meta">${plural(data.tool_calls.length, "market call")} · ${plural(a.cited.length, "KB citation")} · ${(data.elapsed_ms / 1000).toFixed(1)} s</div></div>
      <button class="mark-btn" type="button" aria-label="Show evidence for ${serial}">${rosette(a.cited.length, data.tool_calls.length, "settle")}</button>
    </div>
    <div class="prose">${DOMPurify.sanitize(marked.parse(data.reply))}</div>
    <details class="inline-evidence"><summary>Evidence · ${plural(data.tool_calls.length, "call")} · ${plural(a.cited.length, "citation")}</summary>${evidenceHTML(a, { withMark: false })}</details>`;
  linkCitations(note.querySelector(".prose"));
  note.querySelectorAll(".prose a").forEach((l) => { l.target = "_blank"; l.rel = "noopener"; });
  note.querySelector(".mark-btn").addEventListener("click", () => showEvidence(i));
  note.addEventListener("focusin", () => selected !== i && select(i));
  $("#session").textContent = `SESSION ${serial}`;
  $("#model").textContent = data.model; // may be a fallback model when the primary's quota ran out
  select(i);
  note.scrollIntoView({ block: "start", behavior: "smooth" });
}

// Citation focus reveals its source in the rail (event delegation; works for every note).
for (const [evt, on] of [["mouseover", true], ["focusin", true], ["mouseout", false], ["focusout", false]]) {
  log.addEventListener(evt, (e) => {
    const c = e.target.closest?.(".cite");
    if (!c) return;
    const note = c.closest(".note");
    const i = answers.findIndex((a) => a.el === note);
    if (on && i !== selected) select(i);
    focusCite(c.dataset.id, on);
  });
}

// ── Boot ────────────────────────────────────────────────────────────────────

async function boot() {
  drawBand();
  buildForm();
  resetChat();

  const [st, kbRes, personas] = await Promise.allSettled([
    fetch("/api/status").then((r) => r.json()),
    fetch("/api/kb").then((r) => r.json()),
    fetch("/api/personas").then((r) => r.json()),
  ]);

  if (kbRes.status === "fulfilled") {
    kb = kbRes.value;
    const n = (p) => Object.keys(kb).filter((k) => k.startsWith(p)).length;
    $("#kb-stat").innerHTML = `Knowledge base · <b>${n("R-")} rules</b> · ${n("PB-")} playbooks`;
  }
  if (st.status === "fulfilled") {
    status = st.value;
    $("#tool-count").textContent = `${status.tools.length} tools connected`;
    $("#model").textContent = status.model;
  } else {
    $("#pip").classList.add("down");
    $("#tool-count").textContent = "Not connected";
  }
  if (personas.status === "fulfilled") {
    const box = $("#personas");
    for (const p of personas.value) {
      const b = document.createElement("button");
      b.type = "button";
      b.textContent = (p.label || p.id).replace(/\s*\(PB-\d+\)/, "");
      b.setAttribute("aria-pressed", "false");
      b.addEventListener("click", () => { fillProfile(p); setPersona(b); resetChat(); });
      box.append(b);
    }
  }
  renderRail();
}

$("#ask").addEventListener("submit", (e) => {
  e.preventDefault();
  const q = $("#question").value;
  if (!q.trim() || $("#send").disabled) return; // keep the draft while Alex is still working
  $("#question").value = "";
  ask(q);
});
$("#question").addEventListener("keydown", (e) => {
  if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); $("#ask").requestSubmit(); }
});
$("#reset").addEventListener("click", resetChat);
$("#clear-profile").addEventListener("click", () => { form.reset(); fillProfile({}); setPersona(null); });
$("#profile-toggle").addEventListener("click", (e) => {
  const open = $("#profile-pane").classList.toggle("open");
  e.target.setAttribute("aria-expanded", String(open));
  e.target.textContent = open ? "Hide fields" : "Show fields";
});

boot();
