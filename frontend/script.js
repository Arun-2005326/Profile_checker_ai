/* ── PlacementReady AI · Frontend Logic ── */

const API = ''; // Empty string means use the same domain as the frontend

// ── Shared fetch helper – surfaces FastAPI error details ─────────────────
async function fetchAPI(path) {
  const res = await fetch(`${API}${path}`);
  if (!res.ok) {
    let detail = `Server error (${res.status})`;
    try { const body = await res.json(); detail = body.detail || detail; } catch {}
    throw new Error(detail);
  }
  return res.json();
}

// ── Helpers ──────────────────────────────────────────────────────────────
function show(id)  { document.getElementById(id)?.classList.remove('hidden'); }
function hide(id)  { document.getElementById(id)?.classList.add('hidden'); }
function setText(id, val) { const el = document.getElementById(id); if (el) el.textContent = val ?? '—'; }

function setLoading(msg = 'Analyzing profile…') {
  hide('results-empty');
  hide('github-result');
  hide('lc-result');
  hide('hr-result');
  hide('error-block');
  hide('gh-ai-feedback-wrap');
  setText('loading-text', msg);
  show('loading');
}

function clearLoading() {
  hide('loading');
}

function showError(msg) {
  hide('loading');
  hide('results-empty');
  setText('error-message', msg);
  show('error-block');
}

function clearError() {
  hide('error-block');
  show('results-empty');
}

// ── Score ring animation ─────────────────────────────────────────────────
function animateRing(ringId, score, max = 100) {
  const ring = document.getElementById(ringId);
  if (!ring) return;
  const circumference = 2 * Math.PI * 50; // r=50 → ~314
  const offset = circumference - (score / max) * circumference;
  ring.style.strokeDasharray = circumference;
  ring.style.strokeDashoffset = circumference; // start at 0
  requestAnimationFrame(() => {
    requestAnimationFrame(() => {
      ring.style.strokeDashoffset = offset;
    });
  });
}

// ── Counter animation ────────────────────────────────────────────────────
function animateNumber(id, target, duration = 900) {
  const el = document.getElementById(id);
  if (!el) return;
  const start = performance.now();
  const from = 0;
  function step(now) {
    const t = Math.min((now - start) / duration, 1);
    const eased = 1 - Math.pow(1 - t, 3);
    el.textContent = Math.round(from + (target - from) * eased);
    if (t < 1) requestAnimationFrame(step);
  }
  requestAnimationFrame(step);
}

// ── Score label color ────────────────────────────────────────────────────
function scoreColor(score) {
  if (score >= 75) return '#22c55e';
  if (score >= 50) return '#eab308';
  return '#ef4444';
}

// ── GitHub ───────────────────────────────────────────────────────────────
async function checkGitHub() {
  const username = document.getElementById('github').value.trim();
  if (!username) { pulseInput('github'); return; }

  const btn = document.getElementById('github-btn');
  btn.disabled = true;
  setLoading(`Fetching GitHub profile for @${username}…`);

  try {
    const data = await fetchAPI(`/github/${username}`);

    clearLoading();
    hide('results-empty');
    show('github-result');

    // Score pill
    const pill = document.getElementById('gh-score-pill');
    pill.textContent = `${data.score ?? 0}/100`;
    pill.style.background = `linear-gradient(135deg, ${scoreColor(data.score)}, ${scoreColor(data.score)}aa)`;

    // Ring
    animateRing('gh-ring', data.score ?? 0, 100);
    animateNumber('gh-score-num', data.score ?? 0);

    // Metrics
    setText('gh-repos',     data.repos     ?? '—');
    setText('gh-stars',     data.stars     ?? '—');
    setText('gh-followers', data.followers ?? '—');
    
    // Documentation metric
    const qm = data.quality_metrics || {};
    const docScore = (qm.readme_score || 0) + (qm.license_score || 0);
    setText('gh-docs', `${docScore}/10`);

    // AI Feedback
    console.log("AI Feedback Data:", data.ai_feedback);
    if (data.ai_feedback) {
      setText('gh-ai-feedback', data.ai_feedback);
      show('gh-ai-feedback-wrap');
    } else {
      hide('gh-ai-feedback-wrap');
    }

    // Standard Recommendations
    if (data.feedback && data.feedback.length) {
      const list = document.getElementById('gh-feedback-list');
      list.innerHTML = data.feedback.map(f => `<li>${f}</li>`).join('');
      show('gh-feedback-wrap');
    } else {
      hide('gh-feedback-wrap');
    }

  } catch (err) {
    showError(`GitHub Error: ${err.message}`);
  } finally {
    btn.disabled = false;
  }
}



// ── LeetCode ─────────────────────────────────────────────────────────────
async function checkLeetCode() {
  const username = document.getElementById('leetcode').value.trim();
  if (!username) { pulseInput('leetcode'); return; }

  setLoading(`Fetching LeetCode profile for ${username}…`);

  try {
    const data = await fetchAPI(`/leetcode/${username}`);

    clearLoading();
    hide('results-empty');
    show('lc-result');

    setText('lc-score-pill', `${data.score ?? 0} pts`);
    setText('lc-solved',  data.total_solved  ?? data.totalSolved  ?? '—');
    setText('lc-easy',    data.easy_solved   ?? data.easySolved   ?? '—');
    setText('lc-medium',  data.medium_solved ?? data.mediumSolved ?? '—');
    setText('lc-hard',    data.hard_solved   ?? data.hardSolved   ?? '—');

  } catch (err) {
    showError(`LeetCode Error: ${err.message}`);
  }
}

// ── HackerRank ───────────────────────────────────────────────────────────
async function checkHackerRank() {
  const username = document.getElementById('hackerrank').value.trim();
  if (!username) { pulseInput('hackerrank'); return; }

  setLoading(`Fetching HackerRank profile for ${username}…`);

  try {
    const data = await fetchAPI(`/hackerrank/${username}`);

    clearLoading();
    hide('results-empty');
    show('hr-result');

    setText('hr-score-pill', `${data.score ?? 0} pts`);
    setText('hr-score', data.score ?? '—');

  } catch (err) {
    showError(`HackerRank Error: ${err.message}`);
  }
}

// ── Input pulse on empty ─────────────────────────────────────────────────
function pulseInput(id) {
  const el = document.getElementById(id);
  if (!el) return;
  el.style.transition = 'box-shadow 0.15s';
  el.style.boxShadow  = '0 0 0 3px rgba(239,68,68,0.4)';
  el.focus();
  setTimeout(() => { el.style.boxShadow = ''; }, 800);
}

// ── Enter key support ────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  document.getElementById('github')?.addEventListener('keydown',     e => e.key === 'Enter' && checkGitHub());
  document.getElementById('leetcode')?.addEventListener('keydown',   e => e.key === 'Enter' && checkLeetCode());
  document.getElementById('hackerrank')?.addEventListener('keydown', e => e.key === 'Enter' && checkHackerRank());

  // Inject SVG gradient so ring uses gradient stroke
  const svgDefs = `<svg width="0" height="0" style="position:absolute">
    <defs>
      <linearGradient id="ring-gradient" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%"   stop-color="#3b82f6"/>
        <stop offset="100%" stop-color="#6366f1"/>
      </linearGradient>
    </defs>
  </svg>`;
  document.body.insertAdjacentHTML('afterbegin', svgDefs);
});