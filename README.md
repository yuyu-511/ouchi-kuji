# iggy157 — Music Site

音楽ページ群。GitHub Pages でホスティング。

## 🗂 ディレクトリ構成

```
music-site/
├── index.html              # Home（10曲へのナビゲーション）
├── music/
│   ├── music01.html        # Track 01
│   ├── music02.html        # Track 02
│   ├── ...
│   └── music10.html        # Track 10
├── audio/
│   ├── music01.mp3         # 自作音声ファイル（要配置）
│   ├── music02.mp3
│   └── ...
├── images/
│   ├── music01.jpg         # アートワーク画像（任意・後から追加可）
│   ├── music02.jpg
│   └── ...
├── css/
│   └── style.css
├── js/
│   └── script.js
├── generate_pages.py       # 音楽ページ再生成スクリプト
└── README.md
```

---

## 🚀 セットアップ（一発コマンド）

```bash
# 1. 新しいリポジトリを作成（GitHubで事前に作成しておく）
#    例: iggy157/music または iggy157/iggy157-music

# 2. このディレクトリを丸ごとclone先に配置してpush
git init
git add .
git commit -m "initial: music site"
git branch -M main
git remote add origin https://github.com/iggy157/YOUR_REPO_NAME.git
git push -u origin main

# 3. GitHub > Settings > Pages > Source: main / root で有効化
```

---

## 📝 カスタマイズ方法

### 音声ファイルを追加する
`audio/music01.mp3` のように配置するだけで自動的に再生ボタンと紐づきます。

### アートワーク画像を追加する（後から可）
`images/music01.jpg` に画像を配置してから、
`music/music01.html` 内のコメントアウトされた `<img>` タグを有効化してください：

```html
<!-- ここを有効化 -->
<img src="../images/music01.jpg" alt="Track 01">
```

### YouTube動画IDを変更する
`generate_pages.py` の `YT_DATA` リストの動画IDを変更して
再度 `python3 generate_pages.py` を実行するか、
各 `music/musicXX.html` の `data-ytid="..."` を直接編集してください。

### トラック名・説明を変更する
各 `music/musicXX.html` の以下を編集：
- `<h1 class="track-title">` → 曲名
- `<p class="track-description">` → 曲の説明
- `<div class="card-title">` (index.html) → ホームページのカード名

---

## 🔧 ページの再生成

YouTube IDやタイトルをまとめて変更したい場合：

```bash
# generate_pages.py の YT_DATA を編集してから
python3 generate_pages.py
```

## ローカルホストで確認
```bash
python3 -m http.server 8080
```
