import json
from pathlib import Path

PLUGINS_JSON = Path("cs3/plugins.json")
OUTPUT = Path("deploy/index.html")

plugins = json.loads(PLUGINS_JSON.read_text(encoding="utf-8"))

cs_rows = []
iptv_rows = []

for p in plugins:
    row = f"""
    <tr>
      <td><img src="{p.get('iconUrl','')}" width="28"></td>
      <td>
        <b>{p.get('name','')}</b><br>
        <small>{p.get('description','')}</small>
      </td>
      <td>{p.get('version','')}</td>
      <td>{", ".join(p.get("authors", []))}</td>
      <td><a href="{p.get('url','')}">Download</a></td>
    </tr>
    """

    if "iptv" in ",".join(p.get("tvTypes", [])).lower():
        iptv_rows.append(row)
    else:
        cs_rows.append(row)

html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Alkhalifi TV Repository</title>
<meta name="viewport" content="width=device-width, initial-scale=1">

<style>
:root {{
  --bg: #ffffff;
  --fg: #111;
  --card: #f4f4f4;
  --border: #ddd;
  --accent: #007aff;
}}

body.dark {{
  --bg: #0f1115;
  --fg: #eaeaea;
  --card: #181b22;
  --border: #2a2d36;
  --accent: #4da3ff;
}}

body {{
  margin: 0;
  font-family: system-ui, sans-serif;
  background: var(--bg);
  color: var(--fg);
}}

header {{
  padding: 16px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}}

button {{
  background: var(--card);
  color: var(--fg);
  border: 1px solid var(--border);
  padding: 6px 12px;
  border-radius: 8px;
  cursor: pointer;
}}

.tabs {{
  display: flex;
  gap: 8px;
  padding: 0 16px;
}}

.tabs button.active {{
  background: var(--accent);
  color: #fff;
}}

section {{
  display: none;
  padding: 16px;
}}

section.active {{
  display: block;
}}

.card {{
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 16px;
  margin-bottom: 16px;
}}

table {{
  width: 100%;
  border-collapse: collapse;
}}

th, td {{
  padding: 8px;
  border-bottom: 1px solid var(--border);
}}

th {{
  text-align: left;
  opacity: .7;
}}

.poll-option {{
  margin: 10px 0;
  cursor: pointer;
}}

.bar {{
  background: var(--border);
  height: 8px;
  border-radius: 999px;
  overflow: hidden;
  margin-top: 4px;
}}

.bar div {{
  height: 100%;
  width: 0%;
  background: var(--accent);
}}

.mobile table {{
  font-size: 13px;
}}

footer {{
  text-align: center;
  padding: 16px;
  opacity: .6;
}}
</style>
</head>

<body>

<header>
  <h2>📺 Alkhalifi TV</h2>
  <button onclick="toggleDark()">🌙</button>
</header>

<div class="tabs">
  <button class="active" onclick="openTab('iptv')">IPTV</button>
  <button onclick="openTab('cs')">CloudStream</button>
</div>

<section id="iptv" class="active">
  <div class="card">
    <h3>📊 Quick Poll</h3>
    <p>Konten mana yang paling sering kamu pakai?</p>

    <div class="poll-option" onclick="vote('iptv')">
      📺 IPTV
      <div class="bar"><div id="bar-iptv"></div></div>
    </div>

    <div class="poll-option" onclick="vote('cs')">
      ☁️ CloudStream
      <div class="bar"><div id="bar-cs"></div></div>
    </div>

    <div class="poll-option" onclick="vote('both')">
      ⭐ Keduanya
      <div class="bar"><div id="bar-both"></div></div>
    </div>

    <small id="poll-note"></small>
  </div>

  <div class="card">
    <h3>📡 IPTV Resources</h3>
    <ul>
      <li><a href="epg/guide.xml.gz">EPG Global</a></li>
      <li><a href="epg/idn.xml.gz">EPG Indonesia & MY</a></li>
      <li><a href="playlist.m3u8">Playlist M3U</a></li>
    </ul>
  </div>

  <div class="card">
    <table>
      <tr><th>Icon</th><th>Plugin</th><th>Version</th><th>Author</th><th></th></tr>
      {''.join(iptv_rows)}
    </table>
  </div>
</section>

<section id="cs">
  <div class="card">
    <table>
      <tr><th>Icon</th><th>Plugin</th><th>Version</th><th>Author</th><th></th></tr>
      {''.join(cs_rows)}
    </table>
  </div>
</section>

<footer>
BUKAN UNTUK DI JUAL · NOT 4 SALE · Pemakaian pribadi
</footer>

<script>
const POLL_KEY = "alkhalifitv_poll";

function toggleDark() {{
  document.body.classList.toggle('dark');
  localStorage.setItem('dark', document.body.classList.contains('dark'));
}}

if (localStorage.getItem('dark') === 'true') {{
  document.body.classList.add('dark');
}}

function openTab(id) {{
  document.querySelectorAll('section').forEach(s => s.classList.remove('active'));
  document.getElementById(id).classList.add('active');

  document.querySelectorAll('.tabs button').forEach(b => b.classList.remove('active'));
  event.target.classList.add('active');
}}

function vote(choice) {{
  let d = JSON.parse(localStorage.getItem(POLL_KEY)) || {{iptv:0,cs:0,both:0,voted:false}};
  if (d.voted) {{
    document.getElementById("poll-note").innerText = "✔ Kamu sudah vote";
    return;
  }}
  d[choice]++;
  d.voted = true;
  localStorage.setItem(POLL_KEY, JSON.stringify(d));
  renderPoll();
}}

function renderPoll() {{
  let d = JSON.parse(localStorage.getItem(POLL_KEY));
  if (!d) return;
  let t = d.iptv + d.cs + d.both || 1;
  ['iptv','cs','both'].forEach(k => {{
    document.getElementById('bar-' + k).style.width = (d[k]/t*100) + '%';
  }});
}}

renderPoll();

if (window.innerWidth < 768) {{
  document.body.classList.add('mobile');
}}
</script>

</body>
</html>
"""

OUTPUT.parent.mkdir(parents=True, exist_ok=True)
OUTPUT.write_text(html, encoding="utf-8")

print("✅ index.html FULL VERSION berhasil dibuat")
