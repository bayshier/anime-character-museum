#!/usr/bin/env python3
# themes.json → assets/themes.js
import json

d = json.load(open("/tmp/museum_themes.json", encoding="utf-8"))
themes = d["themes"]
js = "/* 主题曲数据 · 来自 AnimeThemes 开放档案，勿手改 */\nconst THEMES = " + json.dumps(themes, ensure_ascii=False, indent="  ") + ";\n"
open("/Users/radar/Downloads/gitlab127001/anime-character-museum/assets/themes.js", "w", encoding="utf-8").write(js)
op_n = sum(1 for t in themes.values() if t.get("op"))
print(f"✓ themes.js: {len(themes)} 部作品（含 OP {op_n}）")
