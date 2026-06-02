// ═══════════════════════════════════════════════
// OpportuneAI — APP.JS
// Core logic: state, profile, matching, rendering
// ═══════════════════════════════════════════════

// ─── STATE ───
let S = {
  profile: JSON.parse(localStorage.getItem('oai_profile')) || null,
  saved:    JSON.parse(localStorage.getItem('oai_saved'))    || [],
  applied:  JSON.parse(localStorage.getItem('oai_applied'))  || [],
  accepted: JSON.parse(localStorage.getItem('oai_accepted')) || [],
  selSkills:    [],
  selInterests: [],
};
function save() {
  localStorage.setItem('oai_profile',  JSON.stringify(S.profile));
  localStorage.setItem('oai_saved',    JSON.stringify(S.saved));
  localStorage.setItem('oai_applied',  JSON.stringify(S.applied));
  localStorage.setItem('oai_accepted', JSON.stringify(S.accepted));
}

// ─── MATCHING ENGINE ───
function match(opp) {
  if (!S.profile) return { score:0, pct:0, level:'low', matched:[], missing:[], gpaOk:false, yearOk:false };
  const ss  = new Set(S.profile.skills||[]);
  const req = opp.requiredSkills;
  const gpa = parseFloat(S.profile.gpa)||0;
  const yr  = parseInt(S.profile.year)||1;

  const matched = req.filter(r => ss.has(r));
  const missing = req.filter(r => !ss.has(r));
  const skillScore = req.length > 0 ? matched.length/req.length : 1;
  const gpaOk  = gpa >= opp.minGpa;
  const yearOk = opp.eligibleYears.includes(yr);
  const gpaScore = gpaOk ? 1 : (opp.minGpa===0 ? 1 : gpa/opp.minGpa);

  let score = Math.round(Math.min(100, skillScore*60 + gpaScore*30 + (yearOk?10:0)));
  return { score, pct:score, level: score>=70?'high': score>=45?'med':'low', matched, missing, gpaOk, yearOk };
}

function predict(m) {
  if (m.score>=75) return { label:'High Chance', icon:'✦', cls:'high' };
  if (m.score>=45) return { label:'Medium Chance', icon:'◎', cls:'med' };
  return { label:'Low Chance', icon:'◌', cls:'low' };
}

// ─── DEADLINE HELPERS ───
function daysLeft(ds) {
  const d = new Date(ds); d.setHours(0,0,0,0);
  const n = new Date(); n.setHours(0,0,0,0);
  return Math.ceil((d-n)/86400000);
}
function fmtDeadline(ds) {
  const days = daysLeft(ds);
  const formatted = new Date(ds).toLocaleDateString('en-IN',{day:'numeric',month:'short',year:'numeric'});
  if (days<0)  return { text:'Deadline passed', urgent:true };
  if (days===0) return { text:'Today — last day!', urgent:true };
  if (days<=7)  return { text:`⏰ ${days} days left · ${formatted}`, urgent:true };
  return { text:`📅 ${formatted} · ${days}d left`, urgent:false };
}

// ─── CARD HTML BUILDER ───
function buildCard(opp, delay=0) {
  const m = match(opp);
  const { text:dl, urgent } = fmtDeadline(opp.deadline);
  const isSaved = S.saved.includes(opp.id);

  const pills = opp.requiredSkills.slice(0,4).map(sk => {
    const cls = S.profile ? (m.matched.includes(sk)?'sp-have':'sp-missing') : 'sp-neutral';
    return `<span class="skill-pill ${cls}">${sk}</span>`;
  }).join('');

  const more = opp.requiredSkills.length>4
    ? `<span class="skill-pill sp-neutral">+${opp.requiredSkills.length-4}</span>` : '';

  const matchHtml = S.profile
    ? `<div class="match-row">
         <span class="match-label">Match</span>
         <span class="match-pct mp-${m.level}">${m.pct}%</span>
       </div>
       <div class="match-bar">
         <div class="match-fill mf-${m.level}" style="width:0%" data-pct="${m.pct}"></div>
       </div>`
    : `<div class="match-row"><span class="match-label" style="font-size:0.7rem;color:var(--gray-400)">Profile needed for match score</span></div>`;

  const div = document.createElement('div');
  div.className = 'opp-card';
  div.style.animationDelay = delay*0.05+'s';
  div.dataset.id = opp.id;
  div.innerHTML = `
    <div class="oc-top">
      <div class="oc-icon" style="background:${opp.iconBg}">${opp.icon}</div>
      <button class="oc-save ${isSaved?'saved':''}" data-id="${opp.id}" title="Save">${isSaved?'♥':'♡'}</button>
    </div>
    <span class="oc-type type-${opp.type}">${opp.type}</span>
    <div class="oc-title">${opp.title}</div>
    <div class="oc-org">${opp.org}</div>
    <div class="oc-deadline ${urgent?'urgent':''}">${dl}</div>
    ${matchHtml}
    <div class="oc-skills">${pills}${more}</div>`;

  div.querySelector('.oc-save').addEventListener('click', e => {
    e.stopPropagation();
    toggleSave(opp.id);
    e.currentTarget.classList.toggle('saved');
    e.currentTarget.textContent = S.saved.includes(opp.id) ? '♥' : '♡';
    updateTrackerBadge();
  });
  div.addEventListener('click', () => openDetail(opp));
  return div;
}

function animateBars(parent=document) {
  setTimeout(() => {
    parent.querySelectorAll('.match-fill[data-pct]').forEach(el => {
      el.style.width = el.dataset.pct + '%';
    });
  }, 120);
}

// ─── SAVE / APPLY ───
function toggleSave(id) {
  const idx = S.saved.indexOf(id);
  if (idx===-1) { S.saved.push(id); toast('Saved! Find it in My Tracker ♥','success'); }
  else { S.saved.splice(idx,1); toast('Removed from saved'); }
  save(); updateTrackerBadge();
}
window.markApplied = (id) => {
  if (!S.applied.includes(id)) { S.applied.push(id); save(); toast('Marked as Applied! ✓','success'); updateTrackerBadge(); }
};

function updateTrackerBadge() {
  const total = S.saved.length + S.applied.length + S.accepted.length;
  const badge = document.getElementById('trackerBadge');
  if (!badge) return;
  badge.textContent = total;
  badge.classList.toggle('show', total>0);
}

// ─── DETAIL PANEL ───
function openDetail(opp) {
  const overlay = document.getElementById('detailOverlay');
  const body    = document.getElementById('dpBody');
  if (!overlay || !body) return;

  const m = match(opp);
  const pred = predict(m);
  const { text:dl, urgent } = fmtDeadline(opp.deadline);
  const isSaved   = S.saved.includes(opp.id);
  const isApplied = S.applied.includes(opp.id);

  const predColors = {
    high: { bg:'#d1fae5', border:'#6ee7b7', text:'#065f46' },
    med:  { bg:'#fff7ed', border:'#fed7aa', text:'#7c2d12' },
    low:  { bg:'#fee2e2', border:'#fca5a5', text:'#7f1d1d' },
  };
  const pc = S.profile ? predColors[pred.cls] : predColors.low;

  const skillsHtml = opp.requiredSkills.map(sk => {
    const have = S.profile && m.matched.includes(sk);
    const cls  = S.profile ? (have?'sp-have':'sp-missing') : 'sp-neutral';
    return `<span class="skill-pill ${cls}">${S.profile?(have?'✓ ':'✗ '):''}${sk}</span>`;
  }).join('');

  const gapHtml = S.profile
    ? m.missing.length===0
      ? `<div class="gap-alert complete">✦ You have all required skills! Great match.</div>`
      : `<div class="gap-alert missing">
           <strong>Skill gap — ${m.missing.length} skill(s) missing:</strong> ${m.missing.join(', ')}.
           ${m.missing.map(sk => SKILL_COURSES[sk]
             ? `<br>→ Learn <em>${sk}</em> on <a href="${SKILL_COURSES[sk].link}" target="_blank" style="color:inherit">${SKILL_COURSES[sk].platform}</a>`
             : '').join('')}
         </div>`
    : '';

  body.innerHTML = `
    <div class="dp-hero" style="background:${opp.iconBg}">
      <div class="dp-hero-icon">${opp.icon}</div>
      <span class="dp-type type-${opp.type}">${opp.type}</span>
      <div class="dp-title">${opp.title}</div>
      <div class="dp-org">${opp.org}</div>
    </div>

    ${S.profile ? `
    <div class="dp-prediction" style="background:${pc.bg};border-color:${pc.border}">
      <span class="dp-pred-icon">${pred.icon}</span>
      <div>
        <div class="dp-pred-label">AI Success Prediction</div>
        <div class="dp-pred-val" style="color:${pc.text}">${pred.label}</div>
      </div>
      <div class="dp-pred-score">
        <div class="dp-pred-label">Match Score</div>
        <div class="dp-pred-val" style="color:${pc.text}">${m.pct}%</div>
      </div>
    </div>` : `
    <div class="dp-prediction" style="background:var(--gray-50);border-color:var(--border)">
      <span class="dp-pred-icon">◌</span>
      <div>
        <div class="dp-pred-label">Set up your profile to see</div>
        <div class="dp-pred-val" style="color:var(--gray-500)">Your personalised match score</div>
      </div>
    </div>`}

    <div class="dp-section">
      <h4>About</h4>
      <p class="dp-desc">${opp.desc}</p>
    </div>

    <div class="dp-section">
      <h4>Key Details</h4>
      <div class="dp-meta-grid">
        <div class="dp-meta-item"><span>Deadline</span><strong class="${urgent?'mp-low':''}">${dl}</strong></div>
        <div class="dp-meta-item"><span>Stipend / Reward</span><strong>${opp.stipend}</strong></div>
        <div class="dp-meta-item"><span>Location</span><strong>${opp.location}</strong></div>
        <div class="dp-meta-item"><span>Min GPA</span><strong>${opp.minGpa>0?opp.minGpa+' / 10':'None'}</strong></div>
        <div class="dp-meta-item"><span>Eligible Years</span><strong>${opp.eligibleYears.map(y=>y+(y===1?'st':y===2?'nd':y===3?'rd':'th')+' yr').join(', ')}</strong></div>
        <div class="dp-meta-item"><span>Tags</span><strong>${opp.tags.join(', ')}</strong></div>
      </div>
    </div>

    <div class="dp-section">
      <h4>Required Skills</h4>
      <div class="oc-skills" style="gap:0.4rem">${skillsHtml}</div>
      ${gapHtml}
    </div>

    <div class="dp-cta">
      <button class="btn-primary" onclick="markApplied(${opp.id});document.getElementById('detailOverlay').classList.remove('open')">
        ${isApplied ? '✓ Applied' : 'Mark as Applied'}
      </button>
      <button class="btn-outline" onclick="toggleSave(${opp.id});this.textContent='${isSaved?'♡ Save':'♥ Saved'}'">
        ${isSaved?'♥ Saved':'♡ Save'}
      </button>
      <button class="btn-outline" onclick="window.open('${opp.link||'#'}','_blank')">Apply ↗</button>
    </div>`;

  overlay.classList.add('open');
  animateBars(body);
}

document.getElementById('dpClose')?.addEventListener('click', () =>
  document.getElementById('detailOverlay').classList.remove('open'));
document.getElementById('detailOverlay')?.addEventListener('click', e => {
  if (e.target === e.currentTarget) e.currentTarget.classList.remove('open');
});

// ─── TOAST ───
function toast(msg, type='') {
  const c = document.getElementById('toastContainer');
  if (!c) return;
  const t = document.createElement('div');
  t.className = `toast ${type}`;
  t.textContent = msg;
  c.appendChild(t);
  setTimeout(() => { t.classList.add('out'); setTimeout(() => t.remove(), 300); }, 2800);
}
window.toast = toast;

// ─── PROFILE MODAL ───
let curStep = 1;

function openProfileModal() {
  const modal = document.getElementById('profileModal');
  if (!modal) return;

  // Populate skill grid
  const sg = document.getElementById('skillGrid');
  const ig = document.getElementById('interestGrid');
  if (sg) {
    sg.innerHTML = '';
    S.selSkills = S.profile?.skills ? [...S.profile.skills] : [];
    SKILL_OPTIONS.forEach(sk => {
      const btn = document.createElement('button');
      btn.className = 'skill-opt' + (S.selSkills.includes(sk)?' sel':'');
      btn.textContent = sk; btn.type='button';
      btn.addEventListener('click', () => {
        const i = S.selSkills.indexOf(sk);
        if (i===-1) S.selSkills.push(sk); else S.selSkills.splice(i,1);
        btn.classList.toggle('sel');
        renderPreview('skillPreview', S.selSkills, 'selSkills');
      });
      sg.appendChild(btn);
    });
  }
  if (ig) {
    ig.innerHTML = '';
    S.selInterests = S.profile?.interests ? [...S.profile.interests] : [];
    INTEREST_OPTIONS.forEach(int => {
      const btn = document.createElement('button');
      btn.className = 'skill-opt' + (S.selInterests.includes(int)?' sel':'');
      btn.textContent = int; btn.type='button';
      btn.addEventListener('click', () => {
        const i = S.selInterests.indexOf(int);
        if (i===-1) S.selInterests.push(int); else S.selInterests.splice(i,1);
        btn.classList.toggle('sel');
        renderPreview('interestPreview', S.selInterests, 'selInterests');
      });
      ig.appendChild(btn);
    });
  }

  if (S.profile) {
    document.getElementById('fName').value    = S.profile.name||'';
    document.getElementById('fBranch').value  = S.profile.branch||'';
    document.getElementById('fYear').value    = S.profile.year||3;
    document.getElementById('fCollege').value = S.profile.college||'';
    document.getElementById('fGpa').value     = S.profile.gpa||7.5;
    document.getElementById('gpaVal').textContent = parseFloat(S.profile.gpa||7.5).toFixed(1);
    updateGpaDesc(S.profile.gpa||7.5);
  }

  renderPreview('skillPreview', S.selSkills, 'selSkills');
  renderPreview('interestPreview', S.selInterests, 'selInterests');
  goStep(1);
  modal.classList.add('open');
}
window.openProfileModal = openProfileModal;

function renderPreview(elId, arr, key) {
  const el = document.getElementById(elId);
  if (!el) return;
  el.innerHTML = arr.map(s =>
    `<span class="sel-tag">${s}
      <button onclick="removeItem('${key}','${s}','${elId}')">✕</button>
    </span>`).join('');
}
window.removeItem = (key, val, previewId) => {
  S[key] = S[key].filter(s => s!==val);
  document.querySelectorAll('.skill-opt').forEach(b => { if(b.textContent===val) b.classList.remove('sel'); });
  renderPreview(previewId, S[key], key);
};

window.goStep = function(n) {
  curStep = n;
  document.querySelectorAll('.modal-step-content').forEach((el,i) => {
    el.classList.toggle('active', i===n-1);
  });
  document.querySelectorAll('.msb-step').forEach((el,i) => {
    el.classList.remove('active','done');
    if (i===n-1) el.classList.add('active');
    else if (i<n-1) el.classList.add('done');
  });
};

document.getElementById('fGpa')?.addEventListener('input', e => {
  const v = e.target.value;
  document.getElementById('gpaVal').textContent = parseFloat(v).toFixed(1);
  updateGpaDesc(v);
});
function updateGpaDesc(v) {
  const el = document.getElementById('gpaDesc'); if (!el) return;
  const n = parseFloat(v);
  if (n>=9)   el.textContent = 'Excellent — eligible for most prestigious scholarships';
  else if(n>=8) el.textContent = 'Great — eligible for almost all opportunities';
  else if(n>=7) el.textContent = 'Good — eligible for most opportunities';
  else if(n>=6) el.textContent = 'Average — some high-value ones may need GPA improvement';
  else          el.textContent = 'Work on improving your GPA to unlock more opportunities';
}

document.getElementById('saveProfileBtn')?.addEventListener('click', () => {
  const name = document.getElementById('fName')?.value.trim();
  if (!name) { toast('Please enter your name','error'); goStep(1); return; }
  S.profile = {
    name,
    branch:   document.getElementById('fBranch')?.value.trim()||'Not specified',
    year:     parseInt(document.getElementById('fYear')?.value)||3,
    college:  document.getElementById('fCollege')?.value.trim()||'',
    gpa:      parseFloat(document.getElementById('fGpa')?.value)||7.5,
    skills:   [...S.selSkills],
    interests:[...S.selInterests],
  };
  save();
  document.getElementById('profileModal').classList.remove('open');
  
  updateSidebarProfile();
  updateProgressSection();
  renderHome();
});

document.getElementById('closeModal')?.addEventListener('click', () =>
  document.getElementById('profileModal').classList.remove('open'));
document.getElementById('profileModal')?.addEventListener('click', e => {
  if (e.target===e.currentTarget) e.currentTarget.classList.remove('open');
});

// Buttons that open profile modal
['openSetupBtn','heroCTA','pcSetupBtn','spEditBtn'].forEach(id => {
  document.getElementById(id)?.addEventListener('click', openProfileModal);
});

// ─── SIDEBAR PROFILE UPDATE ───
function updateSidebarProfile() {
  if (!S.profile) return;
  const p = S.profile;
  const av = document.getElementById('spAvatar');
  const nm = document.getElementById('spName');
  const br = document.getElementById('spBranch');
  if (av) av.textContent = p.name.charAt(0).toUpperCase();
  if (nm) nm.textContent = p.name;
  if (br) br.textContent = `${p.branch} · Year ${p.year}`;
}

// ─── PROGRESS SECTION ───
function updateProgressSection() {
  const p = S.profile;
  const nm = document.getElementById('pcName');
  const sub = document.getElementById('pcSub');
  const lr = document.getElementById('levelRing');
  const li = document.getElementById('lrInner');
  if (!p) return;

  const pct = Math.round(
    (p.name?15:0)+(p.branch?10:0)+(p.gpa?15:0)+(p.skills?.length?Math.min(p.skills.length*5,40):0)+(p.interests?.length?Math.min(p.interests.length*4,20):0)
  );
  const lvl = pct>=80?4: pct>=50?3: pct>=25?2:1;
  const lvlNames = {1:'Starter',2:'Explorer',3:'Achiever',4:'Champion'};

  if (nm) nm.textContent = p.name;
  if (sub) sub.textContent = `${p.branch} · Year ${p.year} · GPA ${p.gpa.toFixed(1)} · Profile ${pct}% complete`;
  if (lr) lr.style.background = `conic-gradient(var(--yellow) ${pct*3.6}deg, rgba(255,255,255,0.1) 0deg)`;
  if (li) li.textContent = lvl;

  document.querySelectorAll('.ls-step').forEach((el,i) => {
    el.classList.remove('active','done');
    if (i===lvl-1) el.classList.add('active');
    else if (i<lvl-1) el.classList.add('done');
  });
}

// ─── DEADLINE TICKER ───
function buildTicker() {
  const track = document.getElementById('tickerTrack');
  if (!track) return;
  const soon = [...OPPORTUNITIES]
    .filter(o => daysLeft(o.deadline) >= 0 && daysLeft(o.deadline) <= 30)
    .sort((a,b) => daysLeft(a.deadline)-daysLeft(b.deadline))
    .slice(0,8);

  if (soon.length===0) { track.innerHTML='<span class="ticker-item">No upcoming deadlines in 30 days</span>'; return; }

  const items = [...soon,...soon].map(o =>
    `<span class="ticker-item"><strong>${o.title}</strong> · ${o.org} · <span class="ti-days">${daysLeft(o.deadline)}d left</span></span>`
  ).join('');
  track.innerHTML = items;
}

// ─── HOME RENDER ───
function renderHome() {
  renderMatchesGrid();
  renderFeatured();
  renderSkillGapWidget();
}

function renderMatchesGrid() {
  const grid = document.getElementById('matchesGrid');
  if (!grid) return;
  grid.innerHTML = '';

  let opps = [...OPPORTUNITIES];
  if (S.profile) opps.sort((a,b)=>match(b).score-match(a).score);
  else opps.sort((a,b)=>daysLeft(a.deadline)-daysLeft(b.deadline));

  opps.slice(0,6).forEach((o,i) => grid.appendChild(buildCard(o,i)));
  animateBars(grid);

  const badge = document.getElementById('matchCountBadge');
  if (badge && S.profile) {
    const highs = opps.filter(o=>match(o).level==='high').length;
    badge.textContent = highs>0 ? `${highs} high matches` : 'for you';
  }
}

function renderFeatured() {
  const list = document.getElementById('featuredList');
  if (!list) return;
  list.innerHTML = '';
  const featured = OPPORTUNITIES.slice(0,5);
  featured.forEach(o => {
    const a = document.createElement('div');
    a.className='feat-item';
    a.innerHTML=`
      <div class="feat-icon" style="background:${o.iconBg}">${o.icon}</div>
      <div class="feat-info">
        <strong>${o.title}</strong>
        <span>${o.org} · ${o.type}</span>
      </div>
      <span class="feat-arrow">→</span>`;
    a.addEventListener('click', ()=>openDetail(o));
    list.appendChild(a);
  });
}

function renderSkillGapWidget() {
  const body = document.getElementById('sgwBody');
  if (!body) return;

  if (!S.profile) {
    body.innerHTML=`<div class="sgw-empty">
      <div class="sgw-empty-icon">◈</div>
      <p>Set up your profile to see personalised skill gaps</p>
      <button class="btn-yellow small" onclick="openProfileModal()">Set up →</button>
    </div>`;
    return;
  }

  const missingMap = {};
  OPPORTUNITIES.forEach(o => {
    match(o).missing.forEach(sk => { missingMap[sk]=(missingMap[sk]||0)+1; });
  });
  const top = Object.entries(missingMap).sort((a,b)=>b[1]-a[1]).slice(0,8);
  const max = top[0]?.[1]||1;

  if (top.length===0) {
    body.innerHTML=`<div class="sgw-empty"><div class="sgw-empty-icon">✦</div><p>You have all required skills! Amazing profile.</p></div>`;
    return;
  }

  body.innerHTML = top.map(([sk,cnt])=>`
    <div class="sgw-bar-row">
      <div class="sgw-skill-name">${sk}</div>
      <div class="sgw-track"><div class="sgw-fill" style="width:0%" data-pct="${Math.round(cnt/max*100)}"></div></div>
      <div class="sgw-count">${cnt}</div>
    </div>`).join('');

  setTimeout(()=>{
    body.querySelectorAll('.sgw-fill[data-pct]').forEach(el=>{el.style.width=el.dataset.pct+'%';});
  },150);
}

// ─── GLOBAL SEARCH ───
document.getElementById('globalSearch')?.addEventListener('input', e => {
  const q = e.target.value.toLowerCase().trim();
  if (!q) { renderMatchesGrid(); return; }
  const grid = document.getElementById('matchesGrid');
  if (!grid) return;
  grid.innerHTML='';
  const filtered = OPPORTUNITIES.filter(o =>
    o.title.toLowerCase().includes(q)||o.org.toLowerCase().includes(q)||
    o.type.toLowerCase().includes(q)||o.requiredSkills.some(s=>s.toLowerCase().includes(q))
  );
  if (filtered.length===0) { grid.innerHTML=`<div class="no-results" style="grid-column:1/-1"><div class="no-results-icon">◎</div><p>No results for "${q}"</p></div>`; return; }
  filtered.forEach((o,i)=>grid.appendChild(buildCard(o,i)));
  animateBars(grid);
});

// ─── KEYBOARD SHORTCUTS ───
document.addEventListener('keydown', e => {
  if (e.key==='/' && document.activeElement!==document.getElementById('globalSearch')) {
    e.preventDefault(); document.getElementById('globalSearch')?.focus();
  }
  if (e.key==='Escape') {
    document.getElementById('detailOverlay')?.classList.remove('open');
    document.getElementById('profileModal')?.classList.remove('open');
  }
});

// ─── INIT ───
function init() {
  updateSidebarProfile();
  updateProgressSection();
  buildTicker();
  renderHome();
  updateTrackerBadge();
  `Welcome back, ${USER_NAME}!`
}
init();