import json
from pathlib import Path

PLUGINS_JSON = Path("cs3/plugins.json")
OUTPUT = Path("deploy/index.html")

plugins = json.loads(PLUGINS_JSON.read_text(encoding="utf-8"))

rows = []
for p in plugins:
    rows.append(f"""
    <tr>
      <td><img src="{p['iconUrl']}" width="32"></td>
      <td><b>{p['name']}</b><br><small>{p.get('description','')}</small></td>
      <td>{p['version']}</td>
      <td>{", ".join(p.get("tvTypes", []))}</td>
      <td>{", ".join(p.get("authors", []))}</td>
      <td><a href="{p['url']}">Download</a></td>
    </tr>
    """)

html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>TV Plugin Repository</title>
<style>
body {{ font-family: Arial, sans-serif; padding: 20px; }}
table {{ border-collapse: collapse; width: 100%; }}
th, td {{ border: 1px solid #ccc; padding: 8px; }}
th {{ background: #f4f4f4; }}
img {{ vertical-align: middle; }}
</style>
</head>
<body>

<h1>📺 TV Plugin Repository</h1>
<p>Last update otomatis via GitHub Actions</p>

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

</body>
</html>
"""

OUTPUT.parent.mkdir(parents=True, exist_ok=True)
OUTPUT.write_text(html, encoding="utf-8")

print("✅ index.html plugin berhasil dibuat")
