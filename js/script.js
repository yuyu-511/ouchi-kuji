/* ═══════════════════════════════════════════════
   おうちくじ — script.js
   ═══════════════════════════════════════════════ */

document.addEventListener('DOMContentLoaded', () => {

  /* ────────────────────────────────────
     1. AUDIO PLAYER (voice message)
  ──────────────────────────────────── */
  const playBtn      = document.getElementById('play-btn');
  const audioEl      = document.getElementById('track-audio');
  const progressBar  = document.querySelector('.progress-bar');
  const progressFill = document.querySelector('.progress-fill');
  const timeEl       = document.querySelector('.time-current');
  const durationEl   = document.querySelector('.time-total');
  const statusEl     = document.querySelector('.player-status');
  const errorEl      = document.querySelector('.audio-error');
  const waveform     = document.querySelector('.waveform-deco');

  if (playBtn && audioEl) {
    const fmt = s => {
      if (isNaN(s)) return '0:00';
      const m = Math.floor(s / 60);
      const sec = String(Math.floor(s % 60)).padStart(2, '0');
      return `${m}:${sec}`;
    };

    playBtn.addEventListener('click', () => {
      if (audioEl.paused) {
        audioEl.play().catch(() => showError());
      } else {
        audioEl.pause();
      }
    });

    audioEl.addEventListener('play', () => {
      playBtn.classList.add('playing');
      if (waveform) waveform.classList.add('playing');
      if (statusEl) { statusEl.textContent = '▶ 再生中'; statusEl.classList.add('active'); }
    });

    audioEl.addEventListener('pause', () => {
      playBtn.classList.remove('playing');
      if (waveform) waveform.classList.remove('playing');
      if (statusEl) { statusEl.textContent = '一時停止中'; statusEl.classList.remove('active'); }
    });

    audioEl.addEventListener('ended', () => {
      playBtn.classList.remove('playing');
      if (waveform) waveform.classList.remove('playing');
      if (progressFill) progressFill.style.width = '0%';
      if (timeEl) timeEl.textContent = '0:00';
      if (statusEl) { statusEl.textContent = 'タップして聴いてね '; statusEl.classList.remove('active'); }
    });

    audioEl.addEventListener('timeupdate', () => {
      if (!audioEl.duration) return;
      const pct = (audioEl.currentTime / audioEl.duration) * 100;
      if (progressFill) progressFill.style.width = pct + '%';
      if (timeEl) timeEl.textContent = fmt(audioEl.currentTime);
    });

    audioEl.addEventListener('loadedmetadata', () => {
      if (durationEl) durationEl.textContent = fmt(audioEl.duration);
    });

    if (progressBar) {
      progressBar.addEventListener('click', e => {
        const rect = progressBar.getBoundingClientRect();
        const pct  = (e.clientX - rect.left) / rect.width;
        audioEl.currentTime = pct * audioEl.duration;
      });
    }

    audioEl.addEventListener('error', () => showError());

    function showError() {
      if (errorEl) errorEl.style.display = 'block';
      if (statusEl) statusEl.textContent = '音声ファイルが見つかりません';
      playBtn.classList.remove('playing');
    }
  }

  /* ────────────────────────────────────
     2. TODAY'S MUSIC — スクロール表示
  ──────────────────────────────────── */
  const todaySection = document.querySelector('.today-section');
  if (todaySection) {
    const observer = new IntersectionObserver(
      entries => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            entry.target.classList.add('visible');
            observer.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.1 }
    );
    observer.observe(todaySection);
  }

  /* ────────────────────────────────────
     3. YOUTUBE サムネイル → iframe
  ──────────────────────────────────── */
  document.querySelectorAll('.yt-thumbnail').forEach(thumb => {
    thumb.addEventListener('click', () => {
      const wrap    = thumb.closest('.yt-embed-wrap');
      const videoId = wrap.dataset.ytid;
      if (!videoId) return;

      const iframe = document.createElement('iframe');
      iframe.src = `https://www.youtube.com/embed/${videoId}?autoplay=1&rel=0&modestbranding=1`;
      iframe.allow = 'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture';
      iframe.allowFullscreen = true;

      thumb.classList.add('hidden');
      wrap.appendChild(iframe);
    });
  });

  /* ────────────────────────────────────
     4. フェードアニメーション
  ──────────────────────────────────── */
  document.querySelectorAll('.fade-up').forEach((el, i) => {
    el.style.animationDelay = (i * 0.08 + 0.05) + 's';
  });

});
