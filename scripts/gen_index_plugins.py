import json
from pathlib import Path

INPUT = Path("private-cs3/plugins.json")
OUT_DIR = Path("cs3")

PUBLIC_BASE = "https://alkhalifitv.github.io/TV"
PUBLIC_REPO = "https://github.com/alkhalifitv/TV"

OUT_DIR.mkdir(parents=True, exist_ok=True)

plugins = json.loads(INPUT.read_text(encoding="utf-8"))
public = []

for p in plugins:
    name = p.get("internalName") or p.get("name")
    if not name:
        continue

    p["url"] = f"{PUBLIC_BASE}/cs3/{name}.cs3"
    p["repositoryUrl"] = PUBLIC_REPO
    p["iconUrl"] = f"{PUBLIC_BASE}/logo/{name}.png"
    public.append(p)

(Path("cs3/plugins.json")).write_text(
    json.dumps(public, indent=4, ensure_ascii=False),
    encoding="utf-8"
)

repo = {
    "name": "alkhalifitv.github.io indonesia",
    "description": "Cloudstream Indonesia Repo",
    "iconUrl": f"{PUBLIC_BASE}/logo/group/movies.png",
    "manifestVersion": 1,
    "pluginLists": [
        f"{PUBLIC_BASE}/cs3/plugins.json"
    ]
}

(Path("cs3/repo.json")).write_text(
    json.dumps(repo, indent=2, ensure_ascii=False),
    encoding="utf-8"
)

print("✅ rewrite_plugins.py OK")
