import json
from pathlib import Path
from datetime import datetime

PLUGINS_JSON = Path("cs3/plugins.json")
OUTPUT = Path("deploy/index.html")

plugins = json.loads(PLUGINS_JSON.read_text(encoding="utf-8"))

plugin_rows = []
for p in plugins:
    text = f"{p['name']} {p.get('description','')} {' '.join(p.get('authors',[]))}".lower()
    plugin_rows.append(f"""
    <tr data-search="{text}">
      <td><img src="{p['iconUrl']}" width="26"></td>
      <td>
        <b>{p['name']}</b><br>
        <small>{p.get('description','')}</small>
      </td>
      <td>{p['version']}</td>
      <td>{", ".join(p.get("authors", []))}</td>
      <td><a href="{p['url']}">Download</a></td>
    </tr>
    """)

now = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>alkhalifitv</title>

<style>
:root {{
  --bg:#0b1220;
  --card:#111827;
  --text:#e5e7eb;
  --muted:#9ca3af;
  --border:#1f2937;
  --accent:#38bdf8;
  --warn:#7f1d1d;
}}

.light {{
  --bg:#f9fafb;
  --card:#ffffff;
  --text:#111827;
  --muted:#6b7280;
  --border:#e5e7eb;
  --accent:#2563eb;
  --warn:#fee2e2;
}}

body {{
  background:var(--bg);
  color:var(--text);
  font-family:system-ui, sans-serif;
  padding:20px;
}}

a {{ color:var(--accent); text-decoration:none; }}
small {{ color:var(--muted); }}

.card {{
  background:var(--card);
  border:1px solid var(--border);
  border-radius:14px;
  padding:16px;
  margin-bottom:18px;
}}

.warning {{
  background:var(--warn);
}}

.tabs {{
  display:flex;
  gap:10px;
  margin:16px 0;
}}

.tab-btn {{
  background:var(--card);
  border:1px solid var(--border);
  color:var(--text);
  padding:8px 16px;
  border-radius:999px;
  cursor:pointer;
}}

.tab-btn.active {{
  background:var(--accent);
  color:white;
}}

.tab-content {{ display:none; }}
.tab-content.active {{ display:block; }}

button {{
  background:var(--border);
  color:var(--text);
  border:none;
  padding:6px 10px;
  border-radius:8px;
  cursor:pointer;
}}

button:hover {{
  background:var(--accent);
  color:white;
}}

input {{
  background:var(--card);
  border:1px solid var(--border);
  color:var(--text);
  padding:8px 12px;
  border-radius:10px;
  width:100%;
  margin-bottom:12px;
}}

table {{
  width:100%;
  border-collapse:collapse;
}}

th, td {{
  border-bottom:1px solid var(--border);
  padding:8px;
}}

th {{ color:var(--muted); font-weight:normal; }}

.footer {{
  margin-top:30px;
  text-align:center;
  font-size:12px;
  color:var(--muted);
}}
</style>

<script>
function switchTab(id) {{
  document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));
  document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
  document.getElementById(id).classList.add('active');
  document.getElementById('btn-' + id).classList.add('active');
  localStorage.setItem('tab', id);
}}

function toggleTheme() {{
  document.body.classList.toggle('light');
  localStorage.setItem('theme',
    document.body.classList.contains('light') ? 'light' : 'dark');
}}

function copyUrl(path) {{
  const url = location.origin + location.pathname.replace(/\\/[^\\/]*$/, '/') + path;
  navigator.clipboard.writeText(url);
  alert('Copied:\\n' + url);
}}

function searchPlugin(q) {{
  q = q.toLowerCase();
  document.querySelectorAll('#cloudstream tr[data-search]').forEach(r => {{
    r.style.display = r.dataset.search.includes(q) ? '' : 'none';
  }});
}}

window.onload = () => {{
  if (localStorage.getItem('theme') === 'light')
    document.body.classList.add('light');

  switchTab(localStorage.getItem('tab') || 'iptv');
}};
</script>
</head>

<body>

<h1>alkhalifitv</h1>
<small>Auto update • {now}</small>

<div class="card warning">
  <b>⚠️ NOT FOR SALE</b><br>
  Repo ini <b>bukan untuk dijual</b> — personal use only
</div>

<button onclick="toggleTheme()">🌗 Toggle Theme</button>

<div class="tabs">
  <button id="btn-iptv" class="tab-btn" onclick="switchTab('iptv')">📺 IPTV</button>
  <button id="btn-cloudstream" class="tab-btn" onclick="switchTab('cloudstream')">☁️ CloudStream</button>
</div>

<div id="iptv" class="tab-content">
  <div class="card">
    <h2>📺 IPTV</h2>

    <p><b>EPG Global</b><br>
      <a href="epg/guide.xml.gz">Download</a>
      <button onclick="copyUrl('epg/guide.xml.gz')">Copy</button></p>

    <p><b>EPG Indonesia & Malaysia</b><br>
      <a href="epg/idn.xml.gz">Download</a>
      <button onclick="copyUrl('epg/idn.xml.gz')">Copy</button></p>

    <p><b>Playlist IPTV</b><br>
      <a href="playlist.m3u8">Download</a>
      <button onclick="copyUrl('playlist.m3u8')">Copy</button></p>
  </div>
</div>

<div id="cloudstream" class="tab-content">
  <div class="card">
    <h2>☁️ CloudStream Plugins</h2>
    <input placeholder="Search plugin..." oninput="searchPlugin(this.value)">
    <table>
      <tr><th></th><th>Plugin</th><th>Version</th><th>Author</th><th></th></tr>
      {''.join(plugin_rows)}
    </table>
  </div>
</div>

<div class="footer">
  © alkhalifitv — GitHub Pages
</div>

</body>
</html>
"""

OUTPUT.parent.mkdir(parents=True, exist_ok=True)
OUTPUT.write_text(html, encoding="utf-8")

print("🔥 GOD MODE index.html generated")
