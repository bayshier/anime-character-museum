#!/usr/bin/env python3
# 第八批策展：黄金十二宫 10 位 + 热门补强 16 位（共 26 件，复用 v2 抓取方式）
import json, os, subprocess, time

API = "https://graphql.anilist.co"
UA = ["-H", "User-Agent: MangaCharacterMuseum/0.1"]
OUT = "/Users/radar/Downloads/gitlab127001/anime-character-museum/exhibits"
os.makedirs(OUT, exist_ok=True)

def gql(query, variables):
    payload = json.dumps({"query": query, "variables": variables})
    for attempt in range(6):
        r = subprocess.run(["curl", "-s", "--max-time", "20", "-X", "POST", API,
                            "-H", "Content-Type: application/json", *UA, "-d", payload],
                           capture_output=True, text=True)
        try:
            d = json.loads(r.stdout)
        except Exception as e:
            print(f"  ! gql retry {attempt+1}: {e}", flush=True)
            time.sleep(3 + attempt * 3)
            continue
        if isinstance(d, dict) and d.get("errors"):
            wait = 12 + attempt * 12
            print(f"  ! gql errors, backoff {wait}s: {str(d['errors'])[:100]}", flush=True)
            time.sleep(wait)
            continue
        return d
    return None

def fetch_img(url, path):
    for attempt in range(4):
        r = subprocess.run(["curl", "-s", "--max-time", "40", "-o", path, *UA, url])
        if r.returncode == 0 and os.path.exists(path) and os.path.getsize(path) > 3000:
            return True
        time.sleep(2 + attempt * 2)
    return False

SEARCH_Q = """query ($s: String) { Page(perPage: 10) { media(search: $s, type: ANIME, sort: SEARCH_MATCH) {
  id title { romaji english } startDate { year } format } } }"""
CHARS_Q = """query ($id: Int, $page: Int) { Media(id: $id, type: ANIME) { id
  characters(perPage: 50, page: $page, sort: [RELEVANCE]) { edges { node {
    id name { full } image { large } } } } } }"""

# 已知 media id（前七批汇总）
MEDIA = {
    "seiya": 1254, "bleach": 269, "conan": 235, "deathnote": 1535,
    "hikaru_go": 135, "fairytail": 6702, "haikyuu": 20464,
    "naruto": 20, "yyh": 392, "onepiece": 21,
}
# 需要搜索解析的
SEARCH = {
    "demon_slayer": dict(q="Kimetsu no Yaiba", ymin=2019, ymax=2019),
    "jojo2012":     dict(q="JoJo's Bizarre Adventure", ymin=2012, ymax=2012),
}

ANIME_META = {
    "seiya":        ("圣斗士星矢", "Saint Seiya", 1986, "车田正美"),
    "bleach":       ("死神", "Bleach", 2004, "久保带人"),
    "conan":        ("名侦探柯南", "Detective Conan", 1996, "青山刚昌"),
    "deathnote":    ("死亡笔记", "Death Note", 2006, "大场鸫 × 小畑健"),
    "hikaru_go":    ("棋魂", "Hikaru no Go", 2001, "堀田由美 × 小畑健"),
    "fairytail":    ("妖精的尾巴", "Fairy Tail", 2009, "真岛浩"),
    "haikyuu":      ("排球少年!!", "Haikyuu!!", 2014, "古馆春一"),
    "naruto":       ("火影忍者", "Naruto", 2002, "岸本齐史"),
    "yyh":          ("幽游白书", "Yu Yu Hakusho", 1992, "富坚义博"),
    "onepiece":     ("海贼王", "One Piece", 1999, "尾田荣一郎"),
    "demon_slayer": ("鬼灭之刃", "Demon Slayer: Kimetsu no Yaiba", 2019, "吾峠呼世晴"),
    "jojo2012":     ("JOJO的奇妙冒险", "JoJo's Bizarre Adventure (TV)", 2012, "荒木飞吕彦"),
}

# (cid, animeKey, hall, [搜索token], 名中, 名日, 声优, 观察引导, 讲解词, 名台词)
B8 = [
 # ---- 黄金十二宫（圣斗士星矢 · 80年代馆） ----
 ("mu", "seiya", "80s", ["mu"], "白羊座穆", "ムウ", "盐屋翼",
  "淡紫色的长发，与眉宇间的圣域印记。",
  "白羊座的黄金圣斗士，圣域唯一能修复圣衣的匠人。嘉米尔高原上的静谧智者，念力与守礼并存。","水晶墙！"),
 ("aldebaran", "seiya", "80s", ["aldebaran"], "金牛座阿鲁迪巴", "アルデバラン", "乡里大辅",
  "魁梧的身躯，与牛角般张开的金色圣头盔饰。",
  "金牛座的黄金圣斗士，巴西出身的大力士。他认可了星矢的拳头，也把黄金圣斗士的骄傲输得堂堂正正。","巨型号角！"),
 ("deathmask", "seiya", "80s", ["deathmask", "death mask"], "巨蟹座迪斯马斯克", "デスマスク", "",
  "紫色的长发，与圣衣肩甲上狰狞的鬼面。",
  "巨蟹座的黄金圣斗士，以敌人的脸庞收藏战果。积尸气冥界波把对手直接送进黄泉——他的名字就是招式的注解。","积尸气冥界波！"),
 ("aiolia", "seiya", "80s", ["aiolia", "aolia"], "狮子座艾欧里亚", "アイオリア", "田中秀幸",
  "烈焰般的红色长发，与狮面金盔下的锐利眼神。",
  "狮子座的黄金圣斗士，射手座艾俄洛斯之弟。从被谎言蒙蔽的复仇之狮，到十二宫最堂堂正正的一战。","闪电光速拳！"),
 ("shaka", "seiya", "80s", ["shaka"], "处女座沙加", "シャカ", "三矢雄二",
  "闭目的金色圣衣，与胸前串珠的佛门气息。",
  "处女座的黄金圣斗士，离神最近的男人。睁眼即是天地崩坏——最接近神的男人，最后却为凡人的眼泪拔刀。","天魔降伏！"),
 ("dohko", "seiya", "80s", ["dohko"], "天秤座童虎", "童虎（ドウコウ）", "矢田耕司",
  "佝偻的老人身形，与背后平放的十二件黄金武器。",
  "天秤座的黄金圣斗士，上一次圣战的幸存者。以老人的姿态在五老峰监视哈迪斯之塔二百四十三年。","庐山百龙霸！"),
 ("milo", "seiya", "80s", ["milo"], "天蝎座米罗", "ミロ", "",
  "金色卷发，与圣衣护手上竖起的十五根毒针。",
  "天蝎座的黄金圣斗士，毒针「猩红毒针」的执针者。他的骄傲是只对配得上的对手出满十五针。","猩红毒针！"),
 ("aiolos", "seiya", "80s", ["aiolos"], "射手座艾俄洛斯", "アイオロス", "屋良有作",
  "弓手般的展翼金圣衣，与英年早逝的传说。",
  "射手座的黄金圣斗士，救下襁褓雅典娜的真正英雄。他的黄金之弓与圣衣，是贯穿全篇的精神图腾。","原子闪电光速拳！"),
 ("shura", "seiya", "80s", ["shura"], "摩羯座修罗", "シュラ", "",
  "利落的双刀圣衣护手，与斩裂大地的圣剑。",
  "摩羯座的黄金圣斗士，圣剑「艾克薛利巴」的持有者。他的右手是最锋利的圣剑，也是被忠诚蒙蔽的悲剧。","圣剑！"),
 ("aphrodite", "seiya", "80s", ["aphrodite"], "双鱼座阿布罗狄", "アフロディーテ", "速水奖",
  "海蓝色的长发，与满殿玫瑰的双鱼宫。",
  "双鱼座的黄金圣斗士，自诩最美的男人。玫瑰是他的武器也是他的花圃——毒艳与优雅共存的最美之战。","皇家魔宫玫瑰！"),
 # ---- 热门补强 ----
 ("inosuke", "demon_slayer", "20s", ["inosuke"], "嘴平伊之助", "嘴平伊之助", "松冈祯丞",
  "野猪头套下是一张少女般的脸，与两把锯齿刀。",
  "兽之呼吸的使用者，山里养大的野孩子。 lider般的好胜心与全然不通人情的温柔，用腹肌说话的搭档。","猪突猛进！"),
 ("giyu", "demon_slayer", "20s", ["giyu", "giyuu", "tomioka"], "富冈义勇", "冨岡義勇", "樱井孝宏",
  "左右不对称的羽织，与沉默如水的刀光。",
  "水柱，鬼杀队里最沉默的男人。「不要被别人可怜」——他把温柔全藏进了那句笨拙的辩护里。","壹之型 水面斩！"),
 ("kageyama", "haikyuu", "10s", ["kageyama"], "影山飞雄", "影山飛雄", "石谷春贵",
  "乌黑的利落短发，与场上精准得可怕的托球。",
  "乌野的「王样」，天才排球 setter。从中二之王的独裁到真正的队伍大脑，他的托球会找到全场唯一的落点。","There you are!（就是那里！）"),
 ("renji", "bleach", "00s", ["renji"], "阿散井恋次", "阿散井恋次", "杉山纪彰",
  "束起的红色长发，与眉毛上的刺青和蛇尾丸。",
  "六番队副队长，露琪亚的青梅竹马。为救她与朽木白刀锋相向的那一夜，是死神最热血的伏笔。","咆哮吧 蛇尾丸！"),
 ("heiji", "conan", "90s", ["heiji"], "服部平次", "服部平次", "堀川亮",
  "小麦色的皮肤，与大阪腔和棒球帽。",
  "与新一齐名的西之高中生侦探，「关东的工藤，关西的服部」。热血清爽的大阪骑士，平次的推理从不输主场。","犯人是……你！"),
 ("akira-toya", "hikaru_go", "00s", ["akira toya", "toya akira", "touya"], "塔矢亮", "塔矢アキラ", "",
  "整齐的深色短发，与棋盘前过分认真的眼神。",
  "围棋名门之子，与进藤光宿命对弈的天才棋士。他追逐着「光」的影子，把一生的胜负都押在了三尺棋盘上。","我来挑战你！"),
 ("sai", "hikaru_go", "00s", ["fujiwara no sai", "no sai", "sai"], "藤原佐为", "藤原佐為", "",
  "垂地的长发，与平安时代的官人装束和团扇。",
  "千年前附身棋盘的棋魂，因一局冤棋含恨而终。他借进藤光的手落下千年的执念——那一局，是神之一手。","神之一手！"),
 ("erza", "fairytail", "00s", ["erza"], "艾尔撒·史卡雷特", "エルザ・スカーレット", "平野绫",
  "绯红的长发，与一秒换装的空间魔法武器库。",
  "妖尾最强的女魔导士「妖精女王」，S 级的执刀者。她的铠甲库里有上百套战装，藏着一个被奴役过的童年。","天伦铠甲！"),
 ("jonathan", "jojo2012", "10s", ["jonathan joestar", "jonathan"], "乔纳森·乔斯达", "ジョナサン・ジョースター", "兴津和幸",
  "绅士的正装，与波澜壮阔的「波纹」呼吸法。",
  "乔斯达家族的第一代绅士，波纹的继承者。他的一生开启了百年乔斯达家族与 DIO 的宿命之战。","这是我最后的波纹了！"),
 ("dio", "jojo2012", "10s", ["dio brando", "dio"], "迪奥·布兰度", "ディオ・ブランドー", "子安武人",
  "金色的发型，与石鬼面和 later 的时空超能力。",
  "从贫民窟爬上来的恶之帝王，乔斯达家族百年的宿敌。「 不做人了」是JOJO世界一切恩怨的起点。","WRYYYY！"),
 ("misa", "deathnote", "00s", ["misa amane", "misa"], "弥海砂", "弥海砂", "平野绫",
  "金色双马尾，与哥特萝莉装和死神之眼。",
  "第二基拉，为爱人两度交换寿命的偶像。死神之眼看不清自己的结局——她是这部黑色推理里最悲剧的痴心人。","我是弥海砂！"),
 ("shanks", "onepiece", "90s", ["shanks"], "红发香克斯", "シャンクス", "池田秀一",
  "标志性的三道疤，与宽松的红发海贼团披风。",
  "四皇之一，把草帽托付给路飞的男人。一条手臂换一个时代的约定，是整个大航海时代的起点。","这顶草帽，就寄放在你那了。"),
 ("ace", "onepiece", "90s", ["portgas", "ace"], "波特卡斯·D·艾斯", "ポートガス・D・エース", "古谷彻",
  "赤裸的上身与背上的白胡子海贼团纹身，与帽檐缀着笑脸的橘色牛仔帽。",
  "路飞的义兄，烧烧果实的前任能力者。顶上战争那一声「谢谢你爱我」，是海贼王最痛的一章。","火拳！"),
 ("itachi", "naruto", "00s", ["itachi"], "宇智波鼬", "うちはイタチ", "石川英郎",
  "深红的写轮眼，与额头上的护额划痕和乌鸦。",
  "佐助的兄长，宇智波一族的灭门者与守护者。他把真相和村子都背在自己身上，一个人走完了忍者最暗的夜。","原谅我，佐助，这是最后一次了。"),
 ("toguro", "yyh", "90s", ["younger toguro", "toguro otouto", "toguro"], "户愚吕弟", "戸愚呂（弟）", "玄田哲章",
  "可控的夸张肌肉，与黑暗武道会上最沉重的压迫感。",
  "黑暗武道会的最强冠军，把灵魂卖给「最强」的前武术家。他的百分百，是幽助一代人关于强敌的最初记忆。","这边可是百分之百哦。"),
]

# ---------- 解析搜索型 media ----------
report = {"anime": {}, "characters": [], "missing": []}
for key, meta in SEARCH.items():
    data = gql(SEARCH_Q, {"s": meta["q"]})
    time.sleep(3.0)
    picked = None
    if data and data.get("data"):
        for m in data["data"]["Page"]["media"]:
            y = (m.get("startDate") or {}).get("year") or 0
            if meta["ymin"] <= y <= meta["ymax"]:
                picked = m
                break
    if picked:
        MEDIA[key] = picked["id"]
        print(f"✓ {key}: {picked['title']['romaji']} ({picked['startDate']['year']}) -> {picked['id']}", flush=True)
    else:
        print(f"✗ {key}: media 未命中", flush=True)
        report["missing"].append({"anime": key, "reason": "media-not-found"})

# ---------- 按作品分组抓人物表 ----------
by_anime = {}
for c in B8:
    by_anime.setdefault(c[1], []).append(c)

roster = {}  # animeKey -> edges
for akey, group in by_anime.items():
    mid = MEDIA.get(akey)
    if not mid:
        for c in group:
            report["missing"].append({"char": c[0], "reason": "anime-unresolved"})
        continue
    edges, page = [], 1
    while True:
        data = gql(CHARS_Q, {"id": mid, "page": page})
        time.sleep(3.0)
        media = ((data or {}).get("data") or {}).get("Media") or {}
        chunk = media.get("characters", {}).get("edges", [])
        edges.extend(chunk)
        if len(chunk) < 50 or page >= 3:
            break
        page += 1
    roster[akey] = edges
    print(f"≡ {akey}: 拿到 {len(edges)} 位人物", flush=True)

for akey, edges in roster.items():
    for c in [x for x in by_anime[akey]]:
        cid, _, hall, tokens, zh, jp, cv, feature, intro, quote = c
        img_path = f"{OUT}/{cid}.jpg"
        node = None
        if os.path.exists(img_path) and os.path.getsize(img_path) > 3000:
            print(f"= {cid}: 已存在，跳过下载", flush=True)
            node = {"id": None, "name": {"full": ""}, "image": {"large": img_path}}
        else:
            for e in edges:
                full = ((e.get("node") or {}).get("name") or {}).get("full") or ""
                low = full.lower()
                if any(t in low for t in tokens):
                    node = e["node"]
                    break
            if not node:
                print(f"✗ {cid}: 未匹配 {tokens}", flush=True)
                report["missing"].append({"char": cid, "reason": "char-not-found"})
                continue
            ok = fetch_img(node["image"]["large"], img_path)
        zh_anime, en_anime, year, author = ANIME_META[akey]
        report["characters"].append({
            "id": cid, "anilistCharId": (node or {}).get("id"),
            "nameEn": (node or {}).get("name", {}).get("full", ""),
            "nameZh": zh, "nameJp": jp, "cv": cv, "hall": hall,
            "animeKey": akey, "animeZh": zh_anime, "animeEn": en_anime,
            "year": year, "author": author,
            "feature": feature, "intro": intro, "quote": quote or "",
            "source": f"https://anilist.co/character/{(node or {}).get('id')}" if (node or {}).get("id") else "",
            "image": f"exhibits/{cid}.jpg", "imageOk": ok,
        })
        print(f"{'✓' if ok else '✗'} {zh}", flush=True)

json.dump(report, open("/tmp/museum_b8_report.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
ok_n = sum(1 for c in report["characters"] if c["imageOk"])
print(f"\n=== 第八批完成：{ok_n}/{len(B8)}；未解决：{len(report['missing'])} ===", flush=True)
print(json.dumps(report["missing"], ensure_ascii=False))
