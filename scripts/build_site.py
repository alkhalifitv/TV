import json
from pathlib import Path

plugins = json.loads(Path("cs3/plugins.json").read_text(encoding="utf-8"))

cards = []
for p in plugins:
    cards.append(f"""
    <div class="card plugin">
      <img src="{p.get('iconUrl','')}" loading="lazy">
      <div>
        <b>{p.get('name','')}</b><br>
        <small>{p.get('description','')}</small><br>
        <small>v{p.get('version','')}</small><br>
        <a href="{p.get('url','')}">Download</a>
      </div>
    </div>
    """)

html = f"""<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="utf-8">
<title>Alkhalifi TV</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body{{margin:0;font-family:system-ui;background:#0f1115;color:#eaeaea}}
header{{padding:14px;background:#181b22}}
.tabs button{{margin:6px;padding:8px 14px;border-radius:12px;border:0}}
.tabs button.active{{background:#4da3ff;color:#000}}
section{{display:none;padding:16px}}
section.active{{display:block}}
.card{{background:#181b22;border-radius:14px;padding:14px;margin-bottom:12px}}
.plugin{{display:flex;gap:12px}}
.plugin img{{width:42px;height:42px;border-radius:10px}}
.disclaimer{{border:1px dashed #444;font-size:13px}}
</style>
</head>
<body>

<header><h2>📺 Alkhalifi TV</h2></header>

<div class="tabs">
<button class="active" onclick="openTab('iptv',this)">IPTV</button>
<button onclick="openTab('cs',this)">CloudStream</button>
</div>

<section id="iptv" class="active">
<div class="card">
<ul>
<li><a href="epg/guide.xml.gz">EPG Global</a></li>
<li><a href="epg/idn.xml.gz">EPG Indonesia</a></li>
<li><a href="playlist.m3u8">Playlist IPTV</a></li>
</ul>
</div>
</section>

<section id="cs">{''.join(cards)}</section>

<div class="card disclaimer">
<b>⚠️ Disclaimer</b><br>
Konten IPTV, EPG, dan CloudStream di repo ini hanya untuk
<b>pemakaian pribadi</b>.<br>
<b>DILARANG DIPERJUALBELIKAN · NOT FOR SALE</b>
</div>

<script>
function openTab(id,btn){{
document.querySelectorAll('section').forEach(s=>s.classList.remove('active'));
document.getElementById(id).classList.add('active');
document.querySelectorAll('.tabs button').forEach(b=>b.classList.remove('active'));
btn.classList.add('active');
}}
</script>
</body>
</html>
"""

Path("index.html").write_text(html, encoding="utf-8")
print("✅ build_site.py OK")
