/**
 * AI Career Assistant - Main JavaScript
 * Handles theme, sidebar, animations, charts, and UI interactions
 */

// ── Theme Management ──────────────────────────────────────────────────────────
const ThemeManager = {
  init() {
    // Logged-in users: theme is stored on the server (see profile / toggle-theme).
    if (document.body.dataset.syncTheme === 'server') return;
    const saved = localStorage.getItem('theme') || 'dark';
    this.apply(saved);
  },
  apply(theme) {
    document.body.className = document.body.className
      .replace(/theme-\w+/g, '').trim();
    document.body.classList.add(`theme-${theme}`);
    localStorage.setItem('theme', theme);
    const icon = document.getElementById('themeIcon');
    if (icon) icon.textContent = theme === 'dark' ? '☀️' : '🌙';
  },
  toggle() {
    const current = localStorage.getItem('theme') || 'dark';
    this.apply(current === 'dark' ? 'light' : 'dark');
  }
};

// ── Sidebar Management ────────────────────────────────────────────────────────
const Sidebar = {
  init() {
    this.el = document.querySelector('.sidebar');
    this.overlay = document.getElementById('sidebarOverlay');
    this.bindEvents();
  },
  toggle() {
    if (window.innerWidth <= 768) {
      this.el?.classList.toggle('mobile-open');
      this.overlay?.classList.toggle('d-none');
    } else {
      this.el?.classList.toggle('sidebar-collapsed');
      const main = document.querySelector('.main-content');
      if (main) {
        main.style.marginLeft = this.el?.classList.contains('sidebar-collapsed') ? '70px' : '260px';
      }
    }
  },
  close() {
    this.el?.classList.remove('mobile-open');
    this.overlay?.classList.add('d-none');
  },
  bindEvents() {
    document.getElementById('sidebarToggle')?.addEventListener('click', () => this.toggle());
    this.overlay?.addEventListener('click', () => this.close());
  }
};

// ── Loading Overlay ───────────────────────────────────────────────────────────
const Loader = {
  show(msg = 'Processing...') {
    let overlay = document.getElementById('loadingOverlay');
    if (!overlay) {
      overlay = document.createElement('div');
      overlay.id = 'loadingOverlay';
      overlay.className = 'loading-overlay';
      overlay.innerHTML = `
        <div class="text-center text-white">
          <div class="spinner mx-auto mb-3"></div>
          <p id="loadingMsg" class="mb-0">${msg}</p>
        </div>`;
      document.body.appendChild(overlay);
    } else {
      document.getElementById('loadingMsg').textContent = msg;
      overlay.style.display = 'flex';
    }
  },
  hide() {
    const overlay = document.getElementById('loadingOverlay');
    if (overlay) overlay.style.display = 'none';
  }
};

// ── Toast Notifications ───────────────────────────────────────────────────────
const Toast = {
  show(message, type = 'info', duration = 4000) {
    const container = this._getContainer();
    const id = `toast-${Date.now()}`;
    const icons = { success: '✅', danger: '❌', warning: '⚠️', info: 'ℹ️' };
    const toast = document.createElement('div');
    toast.id = id;
    toast.className = `alert alert-${type} d-flex align-items-center gap-2 mb-2 shadow`;
    toast.style.cssText = 'min-width:280px;max-width:400px;animation:fadeInUp 0.3s ease;';
    toast.innerHTML = `<span>${icons[type] || 'ℹ️'}</span><span class="flex-grow-1">${message}</span>
      <button type="button" class="btn-close btn-close-white ms-2" onclick="this.parentElement.remove()"></button>`;
    container.appendChild(toast);
    setTimeout(() => toast.remove(), duration);
  },
  _getContainer() {
    let c = document.getElementById('toastContainer');
    if (!c) {
      c = document.createElement('div');
      c.id = 'toastContainer';
      c.style.cssText = 'position:fixed;top:80px;right:20px;z-index:9999;';
      document.body.appendChild(c);
    }
    return c;
  }
};

// ── ATS Score Ring Animation ──────────────────────────────────────────────────
function animateScoreRing(score) {
  const circle = document.getElementById('scoreCircle');
  const valueEl = document.getElementById('scoreValue');
  if (!circle) return;

  const radius = circle.r.baseVal.value;
  const circumference = 2 * Math.PI * radius;
  circle.style.strokeDasharray = circumference;
  circle.style.strokeDashoffset = circumference;

  // Color based on score
  const color = score >= 70 ? '#22c55e' : score >= 50 ? '#f59e0b' : '#ef4444';
  circle.style.stroke = color;

  // Animate
  setTimeout(() => {
    const offset = circumference - (score / 100) * circumference;
    circle.style.strokeDashoffset = offset;
  }, 300);

  // Count up number
  if (valueEl) {
    let current = 0;
    const step = score / 60;
    const timer = setInterval(() => {
      current = Math.min(current + step, score);
      valueEl.textContent = Math.round(current);
      if (current >= score) clearInterval(timer);
    }, 16);
  }
}

// ── File Upload Drag & Drop ───────────────────────────────────────────────────
function initUploadZone() {
  const zone = document.getElementById('uploadZone');
  const input = document.getElementById('resumeFile');
  if (!zone || !input) return;

  zone.addEventListener('click', () => input.click());
  zone.addEventListener('dragover', e => { e.preventDefault(); zone.classList.add('dragover'); });
  zone.addEventListener('dragleave', () => zone.classList.remove('dragover'));
  zone.addEventListener('drop', e => {
    e.preventDefault();
    zone.classList.remove('dragover');
    const file = e.dataTransfer.files[0];
    if (file) {
      input.files = e.dataTransfer.files;
      updateFilePreview(file);
    }
  });
  input.addEventListener('change', () => {
    if (input.files[0]) updateFilePreview(input.files[0]);
  });
}

function updateFilePreview(file) {
  const preview = document.getElementById('filePreview');
  const name    = document.getElementById('fileName');
  const size    = document.getElementById('fileSize');
  if (preview) preview.classList.remove('d-none');
  if (name) name.textContent = file.name;
  if (size) size.textContent = (file.size / 1024).toFixed(1) + ' KB';
}

// ── Copy to Clipboard ─────────────────────────────────────────────────────────
function copyToClipboard(text, btn) {
  navigator.clipboard.writeText(text).then(() => {
    const original = btn.innerHTML;
    btn.innerHTML = '✅ Copied!';
    btn.classList.add('btn-success');
    setTimeout(() => { btn.innerHTML = original; btn.classList.remove('btn-success'); }, 2000);
  }).catch(() => Toast.show('Failed to copy', 'danger'));
}

// ── Chatbot ───────────────────────────────────────────────────────────────────
const Chatbot = {
  init() {
    this.form = document.getElementById('chatForm');
    this.input = document.getElementById('chatInput');
    this.messages = document.getElementById('chatMessages');
    if (!this.form) return;
    this.form.addEventListener('submit', e => { e.preventDefault(); this.send(); });
    document.getElementById('voiceBtn')?.addEventListener('click', () => this.startVoice());
  },
  async send() {
    const msg = this.input?.value.trim();
    if (!msg) return;
    this.addMessage(msg, 'user');
    this.input.value = '';
    this.showTyping();
    try {
      const res = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: msg })
      });
      const data = await res.json();
      this.hideTyping();
      this.addMessage(data.response || 'Sorry, I could not process that.', 'bot');
    } catch {
      this.hideTyping();
      this.addMessage('Connection error. Please try again.', 'bot');
    }
  },
  addMessage(text, sender) {
    const div = document.createElement('div');
    div.className = `chat-message ${sender}`;
    // Convert markdown-like bold to HTML
    const formatted = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>').replace(/\n/g, '<br>');
    div.innerHTML = `<div class="chat-bubble">${formatted}</div>`;
    this.messages?.appendChild(div);
    this.messages?.scrollTo({ top: this.messages.scrollHeight, behavior: 'smooth' });
  },
  showTyping() {
    const div = document.createElement('div');
    div.id = 'typingIndicator';
    div.className = 'chat-message bot';
    div.innerHTML = '<div class="chat-bubble"><span class="typing-dots">●●●</span></div>';
    this.messages?.appendChild(div);
    this.messages?.scrollTo({ top: this.messages.scrollHeight, behavior: 'smooth' });
  },
  hideTyping() {
    document.getElementById('typingIndicator')?.remove();
  },
  startVoice() {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
      Toast.show('Voice input not supported in this browser.', 'warning');
      return;
    }
    const recognition = new SpeechRecognition();
    recognition.lang = 'en-US';
    recognition.onresult = e => {
      if (this.input) this.input.value = e.results[0][0].transcript;
    };
    recognition.start();
    Toast.show('Listening... Speak now', 'info', 3000);
  }
};

// ── Charts ────────────────────────────────────────────────────────────────────
function initDashboardCharts(lineLabels, lineScores, doughnutLabels, doughnutData) {
  const tickColor = document.body.classList.contains('theme-light') ? '#64748b' : '#94a3b8';
  const gridColor = document.body.classList.contains('theme-light') ? 'rgba(15,23,42,0.08)' : 'rgba(255,255,255,0.05)';

  // ATS score history (line) — neon gradient fill + glow points
  const ctx1 = document.getElementById('atsChart');
  if (ctx1 && lineLabels && lineScores && lineLabels.length) {
    const c = ctx1.getContext('2d');
    const h = ctx1.parentElement?.clientHeight || 280;
    const grad = c.createLinearGradient(0, 0, 0, h);
    grad.addColorStop(0, 'rgba(99, 102, 241, 0.45)');
    grad.addColorStop(0.45, 'rgba(14, 165, 233, 0.12)');
    grad.addColorStop(1, 'rgba(14, 165, 233, 0)');

    new Chart(ctx1, {
      type: 'line',
      data: {
        labels: lineLabels,
        datasets: [{
          label: 'ATS Score',
          data: lineScores,
          borderColor: '#a78bfa',
          backgroundColor: grad,
          borderWidth: 3,
          fill: true,
          tension: 0.42,
          pointBackgroundColor: '#6366f1',
          pointBorderColor: '#e0e7ff',
          pointBorderWidth: 2,
          pointRadius: 6,
          pointHoverRadius: 9,
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { display: false } },
        scales: {
          y: { min: 0, max: 100, grid: { color: gridColor }, ticks: { color: tickColor } },
          x: { grid: { display: false }, ticks: { color: tickColor } }
        }
      }
    });
  }

  // Skill mix (doughnut) — labels/data come from the server when available
  const ctx2 = document.getElementById('skillsChart');
  if (ctx2) {
    const dLabels = (doughnutLabels && doughnutLabels.length)
      ? doughnutLabels
      : ['Technical', 'Soft Skills', 'AI / ML', 'Web Dev'];
    const dData = (doughnutData && doughnutData.length)
      ? doughnutData
      : [1, 1, 1, 1];
    new Chart(ctx2, {
      type: 'doughnut',
      data: {
        labels: dLabels,
        datasets: [{
          data: dData,
          backgroundColor: ['#6366f1', '#06b6d4', '#22c55e', '#f59e0b', '#a855f7'],
          borderWidth: 0,
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { position: 'bottom', labels: { color: tickColor, padding: 16 } }
        },
        cutout: '65%',
      }
    });
  }
}

// ── Scroll Animations ─────────────────────────────────────────────────────────
function initScrollAnimations() {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('animate-fade-up');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1 });

  document.querySelectorAll('.animate-on-scroll').forEach(el => observer.observe(el));
}

// ── Search & Filter ───────────────────────────────────────────────────────────
function initSearch(inputId, targetClass) {
  const input = document.getElementById(inputId);
  if (!input) return;
  input.addEventListener('input', () => {
    const query = input.value.toLowerCase();
    document.querySelectorAll(`.${targetClass}`).forEach(item => {
      const text = item.textContent.toLowerCase();
      item.style.display = text.includes(query) ? '' : 'none';
    });
  });
}

// ── Skill Input Tags ──────────────────────────────────────────────────────────
function initSkillInput(inputId, containerId, hiddenId) {
  const input = document.getElementById(inputId);
  const container = document.getElementById(containerId);
  const hidden = document.getElementById(hiddenId);
  if (!input || !container) return;

  const skills = [];

  function render() {
    container.innerHTML = skills.map((s, i) =>
      `<span class="skill-tag skill-tag-neutral">${s}
        <span class="ms-1 cursor-pointer" onclick="removeSkill(${i},'${inputId}','${containerId}','${hiddenId}')">×</span>
      </span>`
    ).join('');
    if (hidden) hidden.value = skills.join(', ');
  }

  input.addEventListener('keydown', e => {
    if ((e.key === 'Enter' || e.key === ',') && input.value.trim()) {
      e.preventDefault();
      const skill = input.value.trim().replace(/,$/, '');
      if (skill && !skills.includes(skill)) {
        skills.push(skill);
        render();
      }
      input.value = '';
    }
  });

  window[`removeSkill`] = (i, iId, cId, hId) => {
    skills.splice(i, 1);
    render();
  };
}

// ── Particles (hero background) ───────────────────────────────────────────────
function initParticles() {
  const container = document.querySelector('.hero-particles');
  if (!container) return;
  for (let i = 0; i < 20; i++) {
    const p = document.createElement('div');
    p.className = 'particle';
    const size = Math.random() * 6 + 2;
    p.style.cssText = `
      width:${size}px; height:${size}px;
      left:${Math.random() * 100}%;
      top:${Math.random() * 100}%;
      animation-delay:${Math.random() * 4}s;
      animation-duration:${3 + Math.random() * 4}s;
      opacity:${0.2 + Math.random() * 0.5};
    `;
    container.appendChild(p);
  }
}

// ── Init ──────────────────────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  ThemeManager.init();
  Sidebar.init();
  Chatbot.init();
  initUploadZone();
  initScrollAnimations();
  initParticles();

  // Auto-dismiss alerts
  document.querySelectorAll('.alert-dismissible').forEach(alert => {
    setTimeout(() => {
      alert.style.opacity = '0';
      alert.style.transition = 'opacity 0.5s';
      setTimeout(() => alert.remove(), 500);
    }, 5000);
  });

  // Tooltip init (Bootstrap)
  document.querySelectorAll('[data-bs-toggle="tooltip"]').forEach(el => {
    new bootstrap.Tooltip(el);
  });
});
