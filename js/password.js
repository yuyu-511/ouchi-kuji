/* ═══════════════════════════════════════════════
   おうちくじ — password.js
   ページごとのパスワード保護（クライアントサイド）
   ═══════════════════════════════════════════════ */

(function () {
  // body の data-password 属性からパスワードを取得
  const correctPw = document.body.dataset.password;
  if (!correctPw) return;

  // sessionStorage で「このページは解錠済み」か確認
  const pageKey = 'unlocked_' + location.pathname;
  if (sessionStorage.getItem(pageKey) === '1') return;

  // ── オーバーレイ生成 ──────────────────────────
  const overlay = document.createElement('div');
  overlay.id = 'pw-overlay';
  overlay.innerHTML = `
    <div class="pw-box">
      <div class="pw-deco">🎁</div>
      <h2 class="pw-title">パスワードを入力</h2>
      <p class="pw-sub">くじに書いてある<br>8文字のパスワードを入れてね</p>

      <div class="pw-input-wrap">
        <input
          type="password"
          id="pw-input"
          class="pw-input"
          maxlength="8"
          placeholder="••••••••"
          autocomplete="off"
          spellcheck="false"
        >
        <button id="pw-submit" class="pw-submit">開く →</button>
      </div>

      <p class="pw-error" id="pw-error">パスワードが違うよ 🥺</p>

      <div class="pw-dots">
        <span></span><span></span><span></span>
      </div>
    </div>
  `;
  document.body.appendChild(overlay);

  // 本文を隠す
  document.body.style.overflow = 'hidden';

  const input   = document.getElementById('pw-input');
  const submitBtn = document.getElementById('pw-submit');
  const errorEl = document.getElementById('pw-error');

  input.focus();

  // ── 解錠処理 ──────────────────────────────────
  function tryUnlock() {
    const val = input.value.trim();

    if (val === correctPw) {
      // 正解！
      sessionStorage.setItem(pageKey, '1');
      overlay.classList.add('pw-unlocked');
      document.body.style.overflow = '';
      setTimeout(() => overlay.remove(), 600);
    } else {
      // 不正解
      errorEl.classList.add('show');
      input.value = '';
      input.classList.add('shake');
      setTimeout(() => {
        input.classList.remove('shake');
        errorEl.classList.remove('show');
        input.focus();
      }, 1600);
    }
  }

  submitBtn.addEventListener('click', tryUnlock);
  input.addEventListener('keydown', e => {
    if (e.key === 'Enter') tryUnlock();
  });
})();
