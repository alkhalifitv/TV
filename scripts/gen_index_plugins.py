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

plugin_rows = []
for p in plugins:
    plugin_rows.append(f"""
    <tr>
      <td><img src="{p['iconUrl']}" width="28"></td>
      <td>
        <b>{p['name']}</b><br>
        <small>{p.get('description','')}</small>
      </td>
      <td>{p['version']}</td>
      <td>{", ".join(p.get("authors", []))}</td>
      <td><a href="{p['url']}">Download</a></td>
    </tr>
    """)

# ===============================
# HTML Blocks
# ===============================
DISCLAIMER = """
<div class="card warning">
  <b>⚠️ NOT FOR SALE</b><br>
  Repo ini <b>bukan untuk dijual</b>.<br>
  Hanya untuk pemakaian pribadi / personal use.
</div>
"""

IPTV_SECTION = """
<div class="card">
  <h2>📺 IPTV</h2>
  <ul class="list">
    <li>
      <b>EPG Global</b><br>
      <a href="epg/guide.xml.gz">guide.xml.gz</a>
    </li>
    <li>
      <b>EPG Indonesia & Malaysia</b><br>
      <a href="epg/idn.xml.gz">idn.xml.gz</a>
    </li>
    <li>
      <b>Playlist IPTV</b><br>
      <a href="playlist.m3u8">playlist.m3u8</a>
    </li>
  </ul>
</div>
"""

CLOUDSTREAM_SECTION = f"""
<div class="card">
  <h2>☁️ CloudStream / CS3 Plugins</h2>
  <table>
    <tr>
      <th></th>
      <th>Plugin</th>
      <th>Version</th>
      <th>Author</th>
      <th></th>
    </tr>
    {''.join(plugin_rows)}
  </table>
</div>
"""

# ===============================
# HTML
# ===============================
now = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>alkhalifitv</title>

<style>
:root {{
  --bg: #0b1220;
  --card: #111827;
  --text: #e5e7eb;
  --muted: #9ca3af;
  --border: #1f2937;
  --accent: #38bdf8;
  --warn: #7f1d1d;
}}

body {{
  background: var(--bg);
  color: var(--text);
  font-family: system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
  margin: 0;
  padding: 20px;
}}

h1 {{
  margin: 0 0 6px 0;
}}

h2 {{
  margin-top: 0;
}}

a {{
  color: var(--accent);
  text-decoration: none;
}}

a:hover {{
  text-decoration: underline;
}}

small {{
  color: var(--muted);
}}

.card {{
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 16px;
  margin-bottom: 18px;
}}

.warning {{
  background: var(--warn);
  border-color: #991b1b;
}}

.list {{
  list-style: none;
  padding-left: 0;
}}

.list li {{
  margin-bottom: 10px;
}}

table {{
  width: 100%;
  border-collapse: collapse;
}}

th, td {{
  border-bottom: 1px solid var(--border);
  padding: 8px;
  text-align: left;
}}

th {{
  color: var(--muted);
  font-weight: normal;
}}

img {{
  vertical-align: middle;
}}

.footer {{
  margin-top: 30px;
  text-align: center;
  font-size: 12px;
  color: var(--muted);
}}
</style>
</head>

<body>

<h1>alkhalifitv</h1>
<small>Auto update via GitHub Actions • {now}</small>

{DISCLAIMER}

{IPTV_SECTION}

{CLOUDSTREAM_SECTION}

<div class="footer">
  © alkhalifitv — personal use only
</div>

</body>
</html>
"""

# ===============================
# Write file
# ===============================
OUTPUT.parent.mkdir(parents=True, exist_ok=True)
OUTPUT.write_text(html, encoding="utf-8")

print("✅ index.html (dark + minimal) generated")
