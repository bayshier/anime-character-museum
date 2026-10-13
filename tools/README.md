# 策展管线脚本

| 脚本 | 作用 |
|---|---|
| `fetch_characters_v1.py` / `v2.py` | 人物抓取参考实现（AniList GraphQL：media 解析 → Character 搜索 → media 归属校验 → 图片下载）。v2 含限流退避与批量示例 |
| `fetch_themes.py` | AnimeThemes 主题曲抓取（精确名匹配 + OP/ED 直链） |
| `build_characters.py` | 合并各批抓取报告 → `assets/characters.js`（含文案修正层、ORDER 重复断言、图片在位校验）。⚠️ 依赖 `/tmp/museum_*_report.json` 历史报告，新批报告需与历史报告同在 |
| `build_themes.py` | `/tmp/museum_themes.json` → `assets/themes.js` |

用法与坑见根目录 [AGENTS.md](../AGENTS.md)。
