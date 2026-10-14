# AGENTS.md · 给下一个 Agent 的完整交接

> 本文件记录 anime-character-museum 的当前进度、数据管线与扩库指南。
> 如果你（人类或 AI）要继续维护这个项目，从这里开始。

## 项目现状（2026-10-13）

- **324 位人物 / 122 部作品 / 五座年代展厅**（80s 91 · 90s 111 · 00s 67 · 10s 28 · 20s 27）；第八批黄金十二宫、第九/十/十一批高人气补强共 85 位（2026-10-14）。**对外文案一律不写精确数量**（用户 2026-10-14 决定，统一「数百位」表达；精确数字只出现在本文件与页面动态统计，扩库后无需再同步 README/个人站/矩阵卡）
- 展品编号全局唯一：EX-01 → EX-297（`assets/characters.js` 数组顺序即编号）
- **主题曲**：99/119 部内嵌（`assets/themes.js`，来自 AnimeThemes 开放档案），其余 YouTube 跳转兜底
- **全息闪卡**：档案弹窗内实时生成（`assets/holocard.js`），支持翻面/缩放/自动旋转/PNG 下载（超采样 2100px）
- **搜索**：导航栏输入框，按人物中/日/英名、作品、声优、原作者、台词实时过滤
- **UI**：动漫 App 风（深空夜色 + 樱粉/紫/青渐变 + 玻璃拟态），样式全部在 `assets/styles.css`
- **线上**：https://bayshier.github.io/anime-character-museum/ （GitHub Pages，master 分支根目录）

## 架构（纯静态，零构建）

```
index.html            大厅 + 档案弹窗（立绘/闪卡双展）+ 主题曲 video
assets/characters.js  297 条展品内容包（由 tools/build_characters.py 生成）
assets/themes.js      99 条主题曲数据（由 tools/build_themes.py 生成）
assets/museum.js      展厅渲染 / 搜索 / 档案弹窗 / 主题曲自动播放
assets/holocard.js    全息闪卡查看器（改编自 holo-card-studio, MIT）
assets/styles.css     全部样式（动漫 App 风）
exhibits/*.jpg        214 张展品图（920×1380，4× Lanczos + 锐化，源自 AniList）
vendor/               本地化的 three.module.js 与 postprocessing 插件（勿依赖 CDN）
tools/                策展管线脚本（见下）
```

## 数据管线（tools/）

| 脚本 | 作用 | 依赖 |
|---|---|---|
| `tools/build_characters.py` | 合并各批抓取报告 → `assets/characters.js`（含 TEXT_FIXUPS 文案修正层、编号断言） | `/tmp/museum_*_report.json`（历史报告，需随批归档） |
| `tools/build_themes.py` | `/tmp/museum_themes.json` → `assets/themes.js` | 抓取报告 |
| `tools/fetch_themes.py` | AnimeThemes 主题曲抓取（精确名匹配） | 网络 |
| `tools/fetch_characters_reference.py` | 人物抓取参考实现（Character 直搜 + media 归属校验） | 网络 |

**扩库标准流程**：
1. 在抓取脚本中按既有格式追加人物条目（id / 搜索名 / 中文名 / 日文名 / CV / 展厅 / 观察点 / 讲解词 / 台词）；
   **cid 必须带作品前缀防撞车**（历史教训：第四批鲇川圆与第六批鹿目圆都叫 `madoka`，图互相覆盖、条目重复）
2. 用 AniList GraphQL 解析 media id（**加 `format == "TV"` 过滤**防 DVD 杂志版误中）→
   `Character(search:) + media 归属校验` 拿图（**比按作品人物表 RELEVANCE 前 50 更可靠**）
3. 下载展品图到 `exhibits/<cid>.jpg` 后，**4× Lanczos + UnsharpMask 放大到 ≥920px**（AniList 原图上限 230×345）
4. 跑 `build_characters.py`（会断言 ORDER 重复与图片在位）→ 更新 `index.html` 的 `?v=` 缓存破坏参数

## 已知坑（务必阅读）

- **AniList GraphQL**：返回键大小写敏感（`Media`/`Page` 大写）；429 有两种响应体
  （`{"errors":[...]}` 或无 `data` 键），限流降级桶会持续拒绝大查询——请求间隔 ≥3s 并做退避重试
- **AniList 译名与常见罗马字不同**：Krillin→Kuririn、Frieza→Freeza、Sendoh→Sendou、
  Gian→Takeshi Gouda；**新一与柯南是合并条目**（无独立新一形象）；拿不准就按作品人物表捞
- **AnimeThemes**：`filter[name]` 是**精确匹配**（先 `/search?q=` 找真名再查），
  模糊匹配会混入完全无关的番剧（曾有 AKIRA 匹配到异世界新番的事故）；视频直链允许外站嵌入
- **人物 id 撞车**：同一名字在不同作品会撞（如多个 Madoka）——用 media 归属校验区分
- **文案混入英文词**：AI 策展的中文文案要跑 `[A-Za-z]{4,}` 扫描（`build_characters.py` 已内置 TEXT_FIXUPS 修正层，新批词条要人工过一遍）
- **缓存破坏**：改任何资产都要 bump `index.html` 的 `?v=` 参数
- **网络**：本机 github.com:443 间歇拦截（push 用重试循环）；Jikan API 被墙（用 AniList 替代）

## 待办 / 路线图

- [ ] 继续扩库（候选：圣斗士黄金十二宫、银魂万事屋、JOJO 各代、Fate 全员、死神队长阵容）
- [ ] 闪卡稀有度体系（按年代/人气分 N/R/SR/SSR 卡框）、卡包抽卡模式
- [ ] 图生 3D 展台（Tripo/Meshy，需 API Key；产物约定 `models/<id>.glb`）
- [ ] 每批扩库后把 `/tmp/museum_*_report.json` 归档进 `tools/reports/`（管线合并依赖历史报告）
