import json
from pathlib import Path
from datetime import datetime

# ===============================
# Path
# ===============================
PLUGINS_JSON = Path("cs3/plugins.json")
OUTPUT = Path("deploy/index.html")

# ===============================
# Load plugins
# ===============================
plugins = json.loads(PLUGINS_JSON.read_text(encoding="utf-8"))

rows = []
for p in plugins:
    rows.append(f"""
    <tr>
      <td><img src="{p['iconUrl']}" width="32"></td>
      <td>
        <b>{p['name']}</b><br>
        <small>{p.get('description','')}</small>
      </td>
      <td>{p['version']}</td>
      <td>{", ".join(p.get("tvTypes", []))}</td>
      <td>{", ".join(p.get("authors", []))}</td>
      <td><a href="{p['url']}">Download</a></td>
    </tr>
    """)

# ===============================
# DISCLAIMER
# ===============================
DISCLAIMER_HTML = """
<div class="disclaimer">
  <h2>📡 IPTV Repository</h2>
  <p>
    Playlist IPTV, EPG, dan Plugin untuk
    <b>Kodi</b>, <b>TVIRL</b>, <b>TiviMate</b>, dan <b>OTT Navigator</b>.
  </p>

  <p class="warning">
    ⚠️ BUKAN UNTUK DI JUAL!!<br>
    ⚠️ NOT FOR SALE!!<br>
    Untuk pemakaian pribadi / personal use only.
  </p>

  <p class="note">
    Segala bentuk penjualan, rebrand, atau redistribusi tanpa izin
    dilarang keras.
  </p>
</div>
"""

# ===============================
# DOWNLOADS
# ===============================
DOWNLOADS_HTML = """
<div class="downloads">
  <h2>⬇️ Downloads</h2>

  <ul>
    <li>
      📅 <b>EPG Global</b><br>
      <a href="epg/guide.xml.gz">guide.xml.gz</a><br>
      <code>https://alkhalifitv.github.io/TV/epg/guide.xml.gz</code>
    </li>

    <li>
      📅 <b>EPG Indonesia & Malaysia</b><br>
      <a href="epg/idn.xml.gz">idn.xml.gz</a><br>
      <code>https://alkhalifitv.github.io/TV/epg/idn.xml.gz</code>
    </li>

    <li>
      📺 <b>Playlist IPTV</b><br>
      <a href="playlist.m3u8">playlist.m3u8</a><br>
      <code>https://alkhalifitv.github.io/TV/playlist.m3u8</code>
    </li>
  </ul>

  <p class="note">
    Gunakan URL di atas langsung di aplikasi IPTV
    (Kodi, TVIRL, TiviMate, OTT Navigator).
  </p>
</div>
"""

# ===============================
# HTML
# ===============================
now = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

html = f"""
<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="utf-8">
<title>IPTV Repository</title>

<style>
body {{
  font-family: Arial, sans-serif;
  padding: 20px;
  background: #f8fafc;
  color: #0f172a;
}}

h1 {{
  margin-bottom: 5px;
}}

.disclaimer {{
  background: #fff4f4;
  border: 2px solid #f87171;
  padding: 18px;
  margin: 20px 0;
  border-radius: 10px;
}}

.warning {{
  color: #b91c1c;
  font-weight: bold;
}}

.note {{
  font-size: 13px;
  color: #334155;
}}

.downloads {{
  background: #f1f5f9;
  border: 1px solid #94a3b8;
  padding: 16px;
  margin-bottom: 20px;
  border-radius: 10px;
}}

.downloads ul {{
  padding-left: 18px;
}}

.downloads li {{
  margin-bottom: 14px;
}}

table {{
  border-collapse: collapse;
  width: 100%;
  background: white;
}}

th, td {{
  border: 1px solid #cbd5f5;
  padding: 8px;
  text-align: left;
}}

th {{
  background: #e2e8f0;
}}

img {{
  vertical-align: middle;
}}

a {{
  color: #2563eb;
  text-decoration: none;
}}

a:hover {{
  text-decoration: underline;
}}

code {{
  background: #e5e7eb;
  padding: 2px 6px;
  border-radius: 5px;
  font-size: 12px;
}}

.footer {{
  margin-top: 30px;
  font-size: 12px;
  color: #475569;
  text-align: center;
}}
</style>

</head>
<body>

<h1>📺 IPTV Repository</h1>
<p>Auto update via GitHub Actions • Last update: {now}</p>

{DISCLAIMER_HTML}

{DOWNLOADS_HTML}

<h2>🔌 Plugin List</h2>

<table>
<tr>
  <th>Icon</th>
  <th>Plugin</th>
  <th>Version</th>
  <th>Type</th>
  <th>Author</th>
  <th>Download</th>
</tr>

{''.join(rows)}

</table>

<div class="footer">
  © alkhalifitv • Personal use only
</div>

</body>
</html>
"""

# ===============================
# Write file
# ===============================
OUTPUT.parent.mkdir(parents=True, exist_ok=True)
OUTPUT.write_text(html, encoding="utf-8")

print("✅ index.html + downloads + disclaimer berhasil dibuat")
