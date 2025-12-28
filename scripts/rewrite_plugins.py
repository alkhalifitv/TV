import json
from pathlib import Path

# ===== PATH =====
INPUT = Path("private-cs3/plugins.json")
OUT_DIR = Path("cs3")

PLUGINS_OUT = OUT_DIR / "plugins.json"
REPO_OUT = OUT_DIR / "repo.json"

# ===== PUBLIC CONFIG =====
PUBLIC_BASE = "https://alkhalifitv.github.io/TV"
PUBLIC_REPO = "https://github.com/alkhalifitv/TV"
REPO_ICON = f"{PUBLIC_BASE}/logo/group/movies.png"

OUT_DIR.mkdir(parents=True, exist_ok=True)

# ===== LOAD PRIVATE =====
with INPUT.open("r", encoding="utf-8") as f:
    plugins = json.load(f)

public_plugins = []

for p in plugins:
    name = p.get("internalName") or p.get("name")
    if not name:
        continue

    p["url"] = f"{PUBLIC_BASE}/cs3/{name}.cs3"
    p["repositoryUrl"] = PUBLIC_REPO
    p["iconUrl"] = f"{PUBLIC_BASE}/logo/{name}.png"

    public_plugins.append(p)

# ===== WRITE plugins.json =====
PLUGINS_OUT.write_text(
    json.dumps(public_plugins, indent=2, ensure_ascii=False),
    encoding="utf-8"
)

# ===== WRITE repo.json =====
repo = {
    "name": "alkhalifitv.github.io indonesia",
    "description": "Cloudstream Indonesia Repo",
    "iconUrl": REPO_ICON,
    "manifestVersion": 1,
    "pluginLists": [
        f"{PUBLIC_BASE}/cs3/plugins.json"
    ]
}

REPO_OUT.write_text(
    json.dumps(repo, indent=2, ensure_ascii=False),
    encoding="utf-8"
)

print("✅ rewrite_plugins.py selesai (PUBLIC plugins + repo.json)")
