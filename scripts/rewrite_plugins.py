import json
from pathlib import Path

INPUT = Path("private-cs3/plugins.json")
OUTPUT = Path("cs3/plugins.json")

PUBLIC_BASE = "https://alkhalifitv.github.io/TV"
PUBLIC_REPO = "https://github.com/alkhalifitv/TV"

with INPUT.open("r", encoding="utf-8") as f:
    plugins = json.load(f)

for p in plugins:
    name = p.get("internalName") or p.get("name")

    # rewrite cs3 url
    p["url"] = f"{PUBLIC_BASE}/cs3/{name}.cs3"

    # rewrite repo url
    p["repositoryUrl"] = PUBLIC_REPO

    # rewrite icon url
    ext = "png"
    p["iconUrl"] = f"{PUBLIC_BASE}/logo/{name}.{ext}"

OUTPUT.parent.mkdir(parents=True, exist_ok=True)
with OUTPUT.open("w", encoding="utf-8") as f:
    json.dump(plugins, f, indent=4, ensure_ascii=False)

print("✅ plugins.json berhasil direwrite ke versi PUBLIC")
