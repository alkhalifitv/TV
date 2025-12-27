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
# Disclaimer
# ===============================
DISCLAIMER_HTML = """
<div class="disclaimer">
  <h2>📡 IPTV Repository</h2>

  <p>
    Playlist TV dan Plugin untuk
    <b>Kodi</b>, <b>TVIRL</b>, <b>TiviMate</b>, dan <b>OTT Navigator</b>.
  </p>

  <p class="warning">
    ⚠️ BUKAN UNTUK DI JUAL!!<br>
    ⚠️ NOT FOR SALE!!<br>
    Untuk pemakaian pribadi / personal use only.
  </p>

  <p class="note">
    Repo ini disediakan untuk keperluan edukasi dan penggunaan pribadi.
    Segala bentuk penjualan, rebrand, atau distribusi ulang tanpa izin
    tidak diperbolehkan.
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
<title>TV Plugin Repository</title>

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

p {{
  margin-top: 0;
}}

.disclaimer {{
  background: #fff4f4;
  border: 2px solid #f87171;
  padding: 18px;
  margin: 20px 0;
  border-radius: 10px;
}}

.disclaimer h2 {{
  margin-top: 0;
}}

.warning {{
  color: #b91c1c;
  font-weight: bold;
}}

.note {{
  font-size: 13px;
  color: #334155;
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

.footer {{
  margin-top: 30px;
  font-size: 12px;
  color: #475569;
  text-align: center;
}}
</style>

</head>
<body>

<h1>📺 TV Plugin Repository</h1>
<p>Auto update via GitHub Actions • Last update: {now}</p>

{DISCLAIMER_HTML}

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

print("✅ index.html plugin + disclaimer berhasil dibuat")
