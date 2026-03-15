#!/usr/bin/env python3
"""
おうちくじ — generate_pages.py
music01.html ~ music10.html を生成します。
"""

import os

# ─── パスワード一覧（8文字） ───────────────────────
# くじの紙に印刷してプレゼントに同封してね！
PASSWORDS = {
    1:  "yokld45j",
    2:  "ay2zgsms",
    3:  "2err70lt",
    4:  "lhyx8u8d",
    5:  "9uwanxgf",
    6:  "1xwt3iu4",
    7:  "xy0100vy",
    8:  "gx510unk",
    9:  "st71unpc",
    10: "u0vclygb",
}

# ─── YouTube 動画データ ──────────────────────────────
# (video_id, タイトル, アーティスト, "me" or "you")
YT_DATA = [
    [ ("dQw4w9WgXcQ", "Never Gonna Give You Up", "Rick Astley",     "me"),
      ("kXYiU_JCYtU", "Numb",                    "Linkin Park",     "you") ],
    [ ("JGwWNGJdvx8", "Shape of You",             "Ed Sheeran",     "me"),
      ("YqeW9_5kURI", "Someone Like You",          "Adele",          "you") ],
    [ ("lp-EO5I60KA", "Bohemian Rhapsody",        "Queen",          "me"),
      ("fJ9rUzIMcZQ", "Stairway to Heaven",        "Led Zeppelin",   "you") ],
    [ ("1G6tftTrUHgg", "Numb Little Bug",          "Em Beihold",    "me"),
      ("4NRXx6U8BFQ",  "abcdefu",                  "GAYLE",          "you") ],
    [ ("CevxZvSJLk8", "Radioactive",               "Imagine Dragons","me"),
      ("hLQl3WQQoQ0", "Someone You Loved",         "Lewis Capaldi",  "you") ],
    [ ("60ItHLz5WEA", "Africa",                    "Toto",           "me"),
      ("7wtfhZwyrcc", "Take On Me",                "a-ha",           "you") ],
    [ ("2Vv-BfVoq4g", "Perfect",                   "Ed Sheeran",    "me"),
      ("OPf0YbXqDm0", "Uptown Funk",               "Bruno Mars",     "you") ],
    [ ("09R8_2nJtjg", "Stay With Me",              "Sam Smith",      "me"),
      ("nfWlot6h_JM", "Shake It Off",              "Taylor Swift",   "you") ],
    [ ("djV11Xbc914", "Africa (Weezer cover)",     "Weezer",        "me"),
      ("YkgkThdzX-8", "Watermelon Sugar",          "Harry Styles",   "you") ],
    [ ("RBumgq5yVrA", "Viva la Vida",              "Coldplay",       "me"),
      ("1qN72LEQnaU", "Believer",                  "Imagine Dragons","you") ],
]

# ─── 賞の定義 ─────────────────────────────────────────
# (ファイル番号, 表示名, 絵文字)
PRIZES = [
    (1,  "A賞",   "🥇"),
    (2,  "B賞",   "🥈"),
    (3,  "C賞",   "🥉"),
    (4,  "D賞①",  "🎀"),
    (5,  "D賞②",  "🎀"),
    (6,  "E賞①",  "🌸"),
    (7,  "E賞②",  "🌸"),
    (8,  "E賞③",  "🌸"),
    (9,  "F賞①",  "🎁"),
    (10, "F賞②",  "🎁"),
]

OWNER_LABELS = {"me": "わたしが選んだ", "you": "あなたが選んだ"}

TEMPLATE = '''<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{prize_name} — おうちくじ</title>
  <meta name="description" content="おうちくじ {prize_name}">
  <link rel="stylesheet" href="../css/style.css">
</head>
<body data-password="{password}">

  <header class="site-header">
    <a class="back-link" href="../index.html">← くじ一覧</a>
    <nav></nav>
  </header>

  <div class="page-wrap">

    <section class="kuji-hero">
      <div class="letter-card">

        <div class="artwork-frame">
          <!--
            画像を追加するとき:
            <img src="../images/music{num:02d}.jpg" alt="{prize_name}">
          -->
          {emoji}
        </div>

        <div class="letter-eyebrow fade-up">
          <span class="dot"></span>
          おうちくじ &nbsp;/&nbsp; {prize_name}
        </div>

        <h1 class="letter-title fade-up">
          <span class="num-accent">{prize_name}</span>の<br>メッセージ
        </h1>

        <p class="letter-desc fade-up">
          ボイスメッセージを聴いてから、<br>
          一緒に動画も楽しもうね 🎀
        </p>

        <div class="voice-player fade-up">
          <button class="play-btn" id="play-btn" aria-label="再生 / 一時停止">
            <svg class="icon-play" viewBox="0 0 24 24" fill="currentColor">
              <path d="M8 5v14l11-7z"/>
            </svg>
            <svg class="icon-pause" viewBox="0 0 24 24" fill="currentColor">
              <path d="M6 19h4V5H6v14zm8-14v14h4V5h-4z"/>
            </svg>
          </button>
          <div class="player-controls">
            <div class="player-label">🎙 ボイスメッセージ</div>
            <div class="player-time">
              <span class="time-current">0:00</span>
              <span class="time-total">0:00</span>
            </div>
            <div class="progress-bar">
              <div class="progress-fill"></div>
            </div>
            <p class="player-status">タップして聴いてね 🎀</p>
            <p class="audio-error">⚠ 音声ファイルが見つかりません（audio/music{num:02d}.mp3）</p>
          </div>
        </div>

        <div class="waveform-deco">
          <div class="bar"></div><div class="bar"></div><div class="bar"></div>
          <div class="bar"></div><div class="bar"></div><div class="bar"></div>
          <div class="bar"></div><div class="bar"></div><div class="bar"></div>
        </div>

        <div class="scroll-hint">
          <span class="hint-emoji">▽</span>
          スクロールして動画へ
        </div>

      </div>
    </section>

    <section class="today-section">
      <div class="today-header">
        <div class="today-badge">🎬 YouTube</div>
        <h2>この動画、一緒に見よ！</h2>
        <p class="today-sub">
          <!-- ここの文言は自由に編集してね -->
        </p>
      </div>

      <div class="fav-section">
        <div class="fav-cards">

          <div class="fav-card">
            <div class="yt-embed-wrap" data-ytid="{yt1_id}">
              <div class="yt-thumbnail">
                <img src="https://img.youtube.com/vi/{yt1_id}/mqdefault.jpg"
                     alt="{yt1_title}" loading="lazy">
                <div class="yt-play-icon"></div>
              </div>
              <span class="yt-owner-tag {yt1_owner}">{yt1_owner_label}</span>
            </div>
            <div class="fav-card-body">
              <p class="fav-card-title">{yt1_title}</p>
              <p class="fav-card-channel">{yt1_channel}</p>
            </div>
          </div>

          <div class="fav-card">
            <div class="yt-embed-wrap" data-ytid="{yt2_id}">
              <div class="yt-thumbnail">
                <img src="https://img.youtube.com/vi/{yt2_id}/mqdefault.jpg"
                     alt="{yt2_title}" loading="lazy">
                <div class="yt-play-icon"></div>
              </div>
              <span class="yt-owner-tag {yt2_owner}">{yt2_owner_label}</span>
            </div>
            <div class="fav-card-body">
              <p class="fav-card-title">{yt2_title}</p>
              <p class="fav-card-channel">{yt2_channel}</p>
            </div>
          </div>

        </div>
      </div>
    </section>

  </div>

  <footer class="site-footer">
    <a href="../index.html">おうちくじ</a>
    &nbsp;·&nbsp; {prize_name}
    &nbsp;<span class="heart">♡</span>
  </footer>

  <audio id="track-audio" preload="none">
    <source src="../audio/music{num:02d}.mp3" type="audio/mpeg">
  </audio>

  <script src="../js/password.js"></script>
  <script src="../js/script.js"></script>
</body>
</html>
'''

out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'music')
os.makedirs(out_dir, exist_ok=True)

print("=" * 48)
print("🎁 おうちくじ パスワード一覧")
print("=" * 48)

for (num, prize_name, emoji), yt_pair in zip(PRIZES, YT_DATA):
    yt1, yt2 = yt_pair
    pw = PASSWORDS[num]

    html = TEMPLATE.format(
        num=num,
        prize_name=prize_name,
        emoji=emoji,
        password=pw,
        yt1_id=yt1[0], yt1_title=yt1[1], yt1_channel=yt1[2],
        yt1_owner=yt1[3], yt1_owner_label=OWNER_LABELS[yt1[3]],
        yt2_id=yt2[0], yt2_title=yt2[1], yt2_channel=yt2[2],
        yt2_owner=yt2[3], yt2_owner_label=OWNER_LABELS[yt2[3]],
    )

    path = os.path.join(out_dir, f'music{num:02d}.html')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"  {prize_name:<6}  →  {pw}")

print("=" * 48)
print("✓ 全10ページ生成完了！")
print()
print("💡 くじの紙にパスワードを印刷してプレゼントに入れてね")
