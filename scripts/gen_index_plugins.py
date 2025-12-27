import json
from pathlib import Path
from datetime import datetime

PLUGINS_JSON = Path("cs3/plugins.json")
OUTPUT = Path("deploy/index.html")

plugins = json.loads(PLUGINS_JSON.read_text(encoding="utf-8"))

rows = []
for p in plugins:
    search = f"{p['name']} {p.get('description','')} {' '.join(p.get('authors',[]))}".lower()
    rows.append(f"""
<tr data-search="{search}">
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

html = f"""<!DOCTYPE html>
<html lang="en">
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
  margin:0;
  background:var(--bg);
  color:var(--text);
  font-family:system-ui, sans-serif;
}}

a {{ color:var(--accent); text-decoration:none; }}
small {{ color:var(--muted); }}

.header {{
  position:sticky;
  top:0;
  z-index:100;
  background:var(--bg);
  padding:16px 20px 10px;
  border-bottom:1px solid var(--border);
}}

.tabs {{
  display:flex;
  gap:10px;
  margin-top:10px;
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

.content {{
  max-height:calc(100vh - 210px);
  overflow-y:auto;
  padding:20px;
}}

.card {{
  background:var(--card);
  border:1px solid var(--border);
  border-radius:14px;
  padding:16px;
  margin-bottom:16px;
}}

.warning {{ background:var(--warn); }}

button {{
  background:var(--border);
  color:var(--text);
  border:none;
  padding:6px 10px;
  border-radius:8px;
  cursor:pointer;
}}

button:hover {{ background:var(--accent); color:white; }}

input {{
  width:100%;
  padding:8px 12px;
  border-radius:10px;
  border:1px solid var(--border);
  background:var(--card);
  color:var(--text);
  margin-bottom:12px;
}}

table {{
  width:100%;
  border-collapse:collapse;
}}

th, td {{
  padding:8px;
  border-bottom:1px solid var(--border);
}}

th {{ color:var(--muted); font-weight:normal; }}

.tab-content {{ display:none; }}
.tab-content.active {{ display:block; }}

.footer {{
  text-align:center;
  font-size:12px;
  color:var(--muted);
  padding:12px;
}}

/* ===== MOBILE COMPACT ===== */
.mobile .header {{ padding:12px 14px 8px; }}
.mobile .tab-btn {{ padding:6px 12px; font-size:13px; }}
.mobile .content {{ padding:12px; max-height:calc(100vh - 180px); }}
.mobile table td, .mobile table th {{ font-size:13px; padding:6px; }}

/* ===== POLL ===== */
.poll-option {{ margin:10px 0; cursor:pointer; }}
.bar {{ background:var(--border); border-radius:999px; height:8px; overflow:hidden; }}
.bar div {{ height:100%; width:0%; background:var(--accent); transition:.3s; }}
</style>

<script>
function switchTab(id) {{
  document.querySelectorAll('.tab-content').forEach(t=>t.classList.remove('active'));
  document.querySelectorAll('.tab-btn').forEach(b=>b.classList.remove('active'));
  document.getElementById(id).classList.add('active');
  document.getElementById('btn-'+id).classList.add('active');
  localStorage.setItem('tab', id);
}}

function toggleTheme() {{
  document.body.classList.toggle('light');
  localStorage.setItem('theme',
    document.body.classList.contains('light') ? 'light':'dark');
}}

function detectMobile() {{
  document.body.classList.toggle('mobile', window.innerWidth <= 768);
}}

function copyUrl(path) {{
  const base = location.origin + location.pathname.replace(/\\/[^\\/]*$/, '/');
  navigator.clipboard.writeText(base + path);
  alert("Copied!");
}}

function searchPlugin(q) {{
  q=q.toLowerCase();
  document.querySelectorAll('#cloudstream tr[data-search]')
    .forEach(r=>r.style.display=r.dataset.search.includes(q)?'':'none');
}}

/* ===== POLL ===== */
const POLL_KEY="alkhalifitv_poll";
function vote(c){{
  let d=JSON.parse(localStorage.getItem(POLL_KEY))||{{iptv:0,cs:0,both:0,voted:false}};
  if(d.voted)return;
  d[c]++; d.voted=true;
  localStorage.setItem(POLL_KEY,JSON.stringify(d));
  renderPoll();
}}
function renderPoll(){{
  let d=JSON.parse(localStorage.getItem(POLL_KEY));
  if(!d)return;
  let t=d.iptv+d.cs+d.both||1;
  ['iptv','cs','both'].forEach(k=>{
    document.getElementById('bar-'+k).style.width=(d[k]/t*100)+'%';
  });
}}

window.onload=()=>{
  if(localStorage.getItem('theme')==='light')document.body.classList.add('light');
  detectMobile();
  renderPoll();
  switchTab(localStorage.getItem('tab')||'iptv');
}
window.onresize=detectMobile;
</script>
</head>

<body>

<div class="header">
  <h1>alkhalifitv</h1>
  <small>Auto update • {now}</small><br><br>
  <button onclick="toggleTheme()">🌗 Theme</button>

  <div class="tabs">
    <button id="btn-iptv" class="tab-btn" onclick="switchTab('iptv')">📺 IPTV</button>
    <button id="btn-cloudstream" class="tab-btn" onclick="switchTab('cloudstream')">☁️ CloudStream</button>
  </div>
</div>

<div id="iptv" class="tab-content">
  <div class="content">

    <div class="card poll">
      <b>📊 Quick Poll</b>
      <div class="poll-option" onclick="vote('iptv')">📺 IPTV<div class="bar"><div id="bar-iptv"></div></div></div>
      <div class="poll-option" onclick="vote('cs')">☁️ CloudStream<div class="bar"><div id="bar-cs"></div></div></div>
      <div class="poll-option" onclick="vote('both')">⭐ Keduanya<div class="bar"><div id="bar-both"></div></div></div>
    </div>

    <div class="card warning">
      <b>⚠️ NOT FOR SALE</b><br>
      Personal use only
    </div>

    <div class="card">
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
</div>

<div id="cloudstream" class="tab-content">
  <div class="content">
    <div class="card">
      <input placeholder="Search plugin..." oninput="searchPlugin(this.value)">
      <table>
        <tr><th></th><th>Plugin</th><th>Version</th><th>Author</th><th></th></tr>
        {''.join(rows)}
      </table>
    </div>
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
print("🔥 FINAL FULL VERSION generated")
