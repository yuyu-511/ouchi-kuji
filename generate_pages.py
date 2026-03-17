#!/usr/bin/env python3
"""
おうちくじ — generate_pages.py
music01.html ~ music10.html を生成します。
"""

import os

# ─── パスワード一覧（8文字） ───────────────────────
PASSWORDS = {
    "a-prize":   "yokld45j",
    "b-prize":   "ay2zgsms",
    "c-prize":   "2err70lt",
    "d-prize-1": "lhyx8u8d",
    "d-prize-2": "9uwanxgf",
    "e-prize-1": "1xwt3iu4",
    "e-prize-2": "xy0100vy",
    "e-prize-3": "gx510unk",
    "f-prize-1": "st71unpc",
    "f-prize-2": "u0vclygb",
}

# ─── YouTube 動画データ ──────────────────────────────
# (video_id, タイトル, アーティスト, "me" or "you")
YT_DATA = [
    [ ("8qI-ITMED1Y", "Miss", "Florence Road",     "me"),
      ("06E14_7t710", "ネーブルオレンジ",               "乃木坂46",     "you") ],
    [ ("Ik2Mp8S6AMQ", "大丈夫",              "般若",      "me"),
      ("manIJU0GybQ", "そうだ、僕は恋をしたんだ。",              "手羽先センセーション",   "you") ],
    [ ("Creg6oEIsNw", "Bitch",                   "Hannah Grae",    "me"),
      ("rw10Q_mVJeY", "君の声",                    "MyDearDarlin'",     "you") ],
    [ ("qzl4Gy0thqA", "ペンギンの赤ちゃん",              "あにまるず",       "me"),
      ("SxBcSL45SoY", "イルカのショー",                  "やまかんりにん","you") ],
    [ ("mIX-wEpFcdE", "アフリカヤマネ",        "ててらぼペット部",          "me"),
      ("loji6Wvz4tU", "シマエナガ",        "tabinotomo",   "you") ],
    [ ("tAEyAGcmHKk", "出所",             "家族チャーハン",     "me"),
      ("QOmHcuQYLyY", "バーのマスター",          "フースーヤ",          "you") ],
    [ ("Lv_0wD9p2rk", "交換日記",          "陣内智則",    "me"),
      ("DCqBgBghnGk", "プロ野球選手",          "NONSTYLE",          "you") ],
    [ ("tUSe0VP4ZBo", "feels like HEAVEN",     "バカリズム",        "me"),
      ("Z4j4TR9Gmzo", "旅館",          "ヤーレンズ",   "you") ],
    [ ("yWISbDZxvAg", "フグのてっちり",               "エマスちゃんねる","me"),
      ("4t8JCicyYfc", "英語禁止人狼",         "QuizKnock",  "you") ],
    [ ("YFvJOPSgwN4?", "シェフ500円 vs 素人10,000円 料理対決",                    "川越シェフだぜ。",           "me"),
      ("rSm1vaphnQY", "3人でおもちづくり",                "よにのちゃんねる",           "you") ],
]

# ─── 賞の定義 ─────────────────────────────────────────
# (ファイル名スラッグ, 表示名, 絵文字, 音声ファイル名)
PRIZES = [
    ("a-prize",   "A賞",   "🥇", "a-prize.m4a"),
    ("b-prize",   "B賞",   "🥈", "b-prize.m4a"),
    ("c-prize",   "C賞",   "🥉", "c-prize.m4a"),
    ("d-prize-1", "D賞①",  "🎀", "d-prize-1.m4a"),
    ("d-prize-2", "D賞②",  "🎀", "d-prize-2.m4a"),
    ("e-prize-1", "E賞①",  "🌸", "e-prize-1.m4a"),
    ("e-prize-2", "E賞②",  "🌸", "e-prize-2.m4a"),
    ("e-prize-3", "E賞③",  "🌸", "e-prize-3.m4a"),
    ("f-prize-1", "F賞①",  "🎁", "f-prize-1.m4a"),
    ("f-prize-2", "F賞②",  "🎁", "f-prize-2.m4a"),
]

# ─── today-sub 文言 ───────────────────────────────────
TODAY_SUB = {
    "a-prize":   "今日の動画は音楽！一つ目は最近いちばんハマってるアーティストの曲をピックしてみましたっ！ 二人の再生リストにも別の曲が追加してあるんだけど、これもおすすめだから聞いてみてっ　二つ目はネーブルオレンジ！最初の頃にライブで聞いた思い出の曲！中でも思い入れ強めな大好きなやつなんですっ",
    "b-prize":   "今日の動画は音楽ですっ！一つ目の曲はおれが中学生くらいの頃からのお気に入りで、じわじわじーんと系のやつですっ で、手羽センの方はゆりあが上手なやつう！大好きな曲ですっ！",
    "c-prize":   "今日の動画は音楽だよーっ！ 一つ目の方は最近気に入ってるアーティストさんなんですっ！まだ新しいレーベルになってからはほぼ曲出てないんだけど、この曲は特にお気に入り！で、二つ目の「君の声」はふたりの再生リストの一番上にあるやつで、おれも大好きなんですっ！今日は一緒に音楽聴こうねーっ",
    "d-prize-1": "今日の動画はどうぶつーーー！一つ目はぺんぎんですっ、で、二つ目はイルカ！夏くらいに名古屋港で両方見たよねーっ！楽しかったなあ。実はペンギン飼えるらしくて、かわいいよねーっ",
    "d-prize-2": "今日の動画は動物ですっ！一つ目はね、ヤマネです！こないだ教えてもらってからハマってるやーつっ！大好き！二つ目はシマエナガですう！これもゆりあに教えてもらってからおれも大好きになったんだよねー。いつか生で見てみたいですねっ",
    "e-prize-1": "今日の動画はお笑いですっ！ふたりとも大好きなお笑い！一つ目の動画はたぶん知らないと思うけど、個人的にめちゃ大好きで、応援してる芸人さんですっ！面白いから見てみてっ！二つ目は元気でるやつ！ゆりあ大好きだもんねーっふたりでお笑い見て元気だそう！！",
    "e-prize-2": "今日の動画はお笑い！！一つ目はおれが小学生のころくらいから大好きなネタなんですよお。なんか本当はこの続きみたいなのもあった気がするんだけど、、、めちゃ面白くて好きなやつ！二つ目はのんすたあ！TimeTreeでもいつかライブ行きたいねーって言って追加してたよね。のんすたらいぶ行きたいねーっ",
    "e-prize-3": "今日の動画はお笑いの動画だよお。一つ目はバカリズムさんの「信用」っていうライブのやつ！このライブめちゃ好きでどれも面白いんだけど、今公開されてる中で一番好きなやつをピックしてみましたあ！二つ目はヤーレンズ！ゆりあヤーレンズ大好きだもんねーっ笑 おれも大好き！一緒にたくさん笑おうねっ！",
    "f-prize-1": "今日の動画はYouTuberの動画なの！一つ目は、実は割とよく見てる好きなYouTuberさんの動画なんですっ 生き物系の動画上げる人でなんかちゃんと愛を持って動物と接してそうな感じが好きなんだよねー。二つ目はくいずのーっく！なんか英語禁止企画っていうわりと王道な企画してたんだけど、めちゃおもしろかったっ！一緒にみましょっ",
    "f-prize-2": "今日の動画はYouTuberの動画です！一つ目はね、最近ハマってる料理の方の動画です！対決企画が面白いんだよー！二つ目はよにのちゃんねる！こっちもお料理してるやつあったから選んでみましたっ よにのちゃんねるで料理してるの珍しいらしくて二個しかなかったっ 面白かったから一緒にみよーねっ！",
}

OWNER_LABELS = {"me": "my favorite song", "you": "your favorite song"}

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
            <img src="../images/{slug}.jpg" alt="{prize_name}">
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
          ボイスメッセージですっ<br><br>
          下の動画も一緒に見ようねっ！
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
            <p class="player-status">タップして聴いてね </p>
            <p class="audio-error">⚠ 音声ファイルが見つかりません（audio/{audio_file}）</p>
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
          {today_sub}
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
    <source src="../audio/{audio_file}" type="audio/mp4">
  </audio>

  <script src="../js/password.js"></script>
  <script src="../js/script.js"></script>
</body>
</html>
'''

out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'kuji')
os.makedirs(out_dir, exist_ok=True)

print("=" * 52)
print("🎁 おうちくじ パスワード一覧")
print("=" * 52)

for (slug, prize_name, emoji, audio_file), yt_pair in zip(PRIZES, YT_DATA):
    yt1, yt2 = yt_pair
    pw = PASSWORDS[slug]

    html = TEMPLATE.format(
        slug=slug,
        prize_name=prize_name,
        emoji=emoji,
        audio_file=audio_file,
        password=pw,
        today_sub=TODAY_SUB[slug],
        yt1_id=yt1[0], yt1_title=yt1[1], yt1_channel=yt1[2],
        yt1_owner=yt1[3], yt1_owner_label=OWNER_LABELS[yt1[3]],
        yt2_id=yt2[0], yt2_title=yt2[1], yt2_channel=yt2[2],
        yt2_owner=yt2[3], yt2_owner_label=OWNER_LABELS[yt2[3]],
    )

    path = os.path.join(out_dir, f'{slug}.html')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"  {prize_name:<6}  →  {pw}  （kuji/{slug}.html）")

print("=" * 52)
print("✓ 全10ページ生成完了！")
print()
print("💡 くじの紙にパスワードを印刷してプレゼントに入れてね")
