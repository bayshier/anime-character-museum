#!/usr/bin/env python3
# 第九批策展：+29 位高人气补强（乔巴/鹰眼/雏田/自来也/白哉/蓝染/西索/库洛洛/桔梗/奈落/炼狱/胡蝶忍/钉崎/宿傩/乔瑟夫/吉良/新八/高杉/知世/马斯坦/不二/手冢/藤真/及川/拉克丝/城之内/撒旦先生/琉克/埃尔文）
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

MEDIA = {
    "onepiece": 21, "naruto": 20, "bleach": 269, "hxh": 136, "inuyasha": 249,
    "jujutsu": 113415, "gintama": 918, "ccsakura": 232, "fma": 121,
    "slamdunk": 170, "haikyuu": 20464, "dbz": 813, "deathnote": 1535,
}
SEARCH = {
    "demon_slayer": dict(q="Kimetsu no Yaiba", ymin=2019, ymax=2019),
    "jojo2012":     dict(q="JoJo's Bizarre Adventure", ymin=2012, ymax=2012),
    "jojo2016":     dict(q="JoJo's Bizarre Adventure: Diamond", ymin=2016, ymax=2016),
    "tennis":       dict(q="Prince of Tennis", ymin=2001, ymax=2002),
    "seed":         dict(q="Mobile Suit Gundam SEED", ymin=2002, ymax=2003),
    "yugioh":       dict(q="Yu-Gi-Oh! Duel Monsters", ymin=2000, ymax=2001),
    "titan":        dict(q="Attack on Titan", ymin=2013, ymax=2013),
}

ANIME_META = {
    "onepiece":     ("海贼王", "One Piece", 1999, "尾田荣一郎"),
    "naruto":       ("火影忍者", "Naruto", 2002, "岸本齐史"),
    "bleach":       ("死神", "Bleach", 2004, "久保带人"),
    "hxh":          ("全职猎人", "Hunter × Hunter (1999)", 1999, "富坚义博"),
    "inuyasha":     ("犬夜叉", "InuYasha", 2000, "高桥留美子"),
    "demon_slayer": ("鬼灭之刃", "Demon Slayer: Kimetsu no Yaiba", 2019, "吾峠呼世晴"),
    "jujutsu":      ("咒术回战", "Jujutsu Kaisen", 2020, "芥见下下"),
    "jojo2012":     ("JOJO的奇妙冒险", "JoJo's Bizarre Adventure (TV)", 2012, "荒木飞吕彦"),
    "jojo2016":     ("JOJO的奇妙冒险 不灭钻石", "JoJo's Bizarre Adventure: Diamond Is Unbreakable", 2016, "荒木飞吕彦"),
    "gintama":      ("银魂", "Gintama", 2006, "空知英秋"),
    "ccsakura":     ("魔卡少女樱", "Cardcaptor Sakura", 1998, "CLAMP"),
    "fma":          ("钢之炼金术师", "Fullmetal Alchemist", 2003, "荒川弘"),
    "tennis":       ("网球王子", "The Prince of Tennis", 2001, "许斐刚"),
    "slamdunk":     ("灌篮高手", "Slam Dunk", 1993, "井上雄彦"),
    "haikyuu":      ("排球少年!!", "Haikyuu!!", 2014, "古馆春一"),
    "seed":         ("机动战士高达SEED", "Mobile Suit Gundam SEED", 2002, "矢立肇 · 富野由悠季"),
    "yugioh":       ("游戏王", "Yu-Gi-Oh! Duel Monsters", 2000, "高桥和希"),
    "dbz":          ("龙珠Z", "Dragon Ball Z", 1989, "鸟山明"),
    "deathnote":    ("死亡笔记", "Death Note", 2006, "大场鸫 · 小畑健"),
    "titan":        ("进击的巨人", "Attack on Titan", 2013, "谏山创"),
}

# (cid, animeKey, hall, [搜索token], 名中, 名日, 声优, 观察引导, 讲解词, 名台词)
B9 = [
 ("chopper", "onepiece", "90s", ["chopper"], "托尼托尼·乔巴", "トニートニー・チョッパー", "大谷育江",
  "圆圆的粉鼻子，与帽子下一对小鹿角。",
  "吃了人人果实的驯鹿，草帽团的船医。甜点是他的命门，变形是他的绝技——最可爱的团员，也是最怕被夸的团员。","我要成为能治百病的神医！"),
 ("mihawk", "onepiece", "90s", ["mihawk"], "乔拉可尔·米霍克", "ジュラキュール・ミホーク", "青野武",
  "鹰一样的金色竖瞳，与背后的黑色巨剑「夜」。",
  "王下七武海的「鹰眼」，世界最强的剑士。索隆一生要超越的男人——他静坐在孤堡里，等一个能终结自己时代的人。","弱者连死法都挑三拣四。"),
 ("hinata", "naruto", "00s", ["hinata hyuga", "hinata"], "日向雏田", "日向ヒナタ", "水树奈奈",
  "及腰的深蓝长发，与总是羞怯的白眼。",
  "日向一族的宗家大小姐，柔拳与白眼的继承者。从躲在栅栏后的注视，到替鸣人挡刀的那句告白——忍者世界里最勇敢的温柔。","因为我喜欢鸣人君！"),
 ("jiraiya", "naruto", "00s", ["jiraiya"], "自来也", "自来也", "大冢周夫",
  "白色的长发，与额头上的「油」字护额。",
  "传说中的三忍之一，鸣人的师父。他把一生写成了书，也把答案留在了徒弟的掌心——豪杰物语的最后一页，是微笑着赴死。","忍者的真正含义，我来教你！"),
 ("byakuya", "bleach", "00s", ["byakuya"], "朽木白哉", "朽木白哉", "堀内贤雄",
  "黑发的贵气与围巾，与袖中千本樱的刀光。",
  "六番队队长，朽木家第三十一代当主。他是一护要翻越的贵族高墙，也是露琪亚背后沉默千年的守护。","千本樱景严！"),
 ("aizen", "bleach", "00s", ["aizen"], "蓝染惣右介", "藍染惣右介", "速水奖",
  "温和的眼镜与褐色发卷，与后来那一袭白衣。",
  "五番队队长，虚圈的真正帝王。他把整个尸魂界当成了棋盘——「没有人能站在天上」是他的信仰，也是他最大的谎言。","崩玉！"),
 ("hisoka", "hxh", "90s", ["hisoka"], "西索", "ヒソカ", "高桥广树",
  "扑克牌与扑克脸，与头发般的红卷发。",
  "变化系战力巅峰，猎人的「魔术师」。他只为强者的战斗而微笑——小杰与奇犽身边最危险的变色龙。","嘻嘻……原来如此。"),
 ("kuroro", "hxh", "90s", ["kuroro", "chrollo"], "库洛洛·鲁西鲁", "クロロ・ルシルフル", "小野健一",
  "额头的十字刺青，与永远摊开的那本盗贼之书。",
  "幻影旅团的团长，偷走能力写进书的「盗贼之王」。酷拉皮卡的复仇之火指向的终点——团长的书里藏着整团人的命运。","盗贼极意。"),
 ("kikyo", "inuyasha", "00s", ["kikyo"], "桔梗", "桔梗（ききょう）", "日高法子",
  "巫女服与白色发带，与腰间的破魔之弓。",
  "守护四魂之玉的巫女，五十年前的悲剧女主角。她的复活是这部战国物语里最温柔的痛——爱与职责，从来难两全。","破魔矢！"),
 ("naraku", "inuyasha", "00s", ["naraku"], "奈落", "奈落", "森川智之",
  "狒狒皮毛之下的黑发，与永远算计众生的眼睛。",
  "从鬼蜘蛛的嫉妒里诞生的半妖，四魂之玉的操盘手。他让全员的力量与执念纠缠成结——最耐心的反派，最漫长的战国。","四魂之玉是我的。"),
 ("rengoku", "demon_slayer", "20s", ["rengoku", "kyojuro"], "炼狱杏寿郎", "煉獄杏寿郎", "日野聪",
  "烈焰色的发梢，与羽织上的火焰纹样。",
  "炎柱，鬼杀队最热血的大哥。无限列车上那一战，把「要承担已死之人的意志」喊进了所有人的心里。","我的心在燃烧！"),
 ("shinobu", "demon_slayer", "20s", ["shinobu", "kochou"], "胡蝶忍", "胡蝶しのぶ", "早见沙织",
  "渐变的紫蝶发饰，与微笑里藏着的恨意。",
  "虫柱，唯一砍不下鬼头颅却依然战斗的柱。她把愤怒炼成毒素，把温柔炼成假面——蝴蝶翅膀下的火，烧了五十年。","让疼痛加倍吧。"),
 ("nobara", "jujutsu", "20s", ["nobara"], "钉崎野蔷薇", "釘崎野薔薇", "濑户麻沙美",
  "橙棕色的短发，与手里的锤子和稻草人。",
  "咒术高专一年级，「我」的美学贯彻者。刍灵术的钉子钉进的是她的自尊——东京都内的都市女巫，从不认输。"," resonance！"),
 ("sukuna", "jujutsu", "20s", ["sukuna"], "两面宿傩", "両面宿傩", "中村悠一",
  "脸颊与额上的第二双眼睛，与四条手臂的鬼神之姿。",
  "千年前的咒术之王，二十根手指就是二十枚封印。他借虎杖的身体苏醒，看戏也参与——最优雅的恶，最强的问题儿童。","醒め、解！"),
 ("joseph", "jojo2012", "10s", ["joseph joestar", "joseph"], "乔瑟夫·乔斯达", "ジョセフ・ジョースター", "杉田智和",
  "把墨镜别在头巾上，与永远猜对手台词的坏笑。",
  "乔斯达家族第二代，波纹与智谋的双修。「你的下一句话是……」——他把战斗变成了一场场心理魔术。","你的下一句话是——！"),
 ("kishibe", "jojo2016", "10s", ["kira yoshikage", "kira"], "吉良吉影", "吉良吉影", "小野健一",
  "深色的西装与领带，与耳后悄然逼近的「杀手皇后」。",
  "杜王町的上班族，只想过平静生活的杀人狂。不灭钻石篇最终 BOSS——最安静的恶，藏在最普通的日常里。","杀手皇后已经踩过了！"),
 ("shinpachi", "gintama", "00s", ["shinpachi"], "志村新八", "志村新八", "阪口大助",
  "腰间的武士刀，与那一副从不离脸的眼镜。",
  "万事屋的第二号成员，吐槽担当。「眼镜才是本体」——他是这部无节操喜剧里，唯一认真活着常识人。","吐槽不是我唯一的技能！"),
 ("takasugi", "gintama", "00s", ["takasugi"], "高杉晋助", "高杉晋助", "子安武人",
  "左眼的眼带与紫色的和服，与叼在嘴边的烟管。",
  "攘夷志士的鬼兵队头目，银时的旧友与宿敌。他烧掉半个世界只为告别那个时代——最悲哀的反派，最决绝的眼泪。","这个时代，我不需要。"),
 ("tomoyo", "ccsakura", "90s", ["tomoyo", "daidouji"], "大道寺知世", "大道寺知世", "岩男润子",
  "乌黑的长直发，与永远举着的摄像机。",
  "小樱最好的朋友，大道寺集团的千金。她为小樱做衣服、拍影像、唱和声——「最喜欢为喜欢的人做喜欢的事」。","小樱酱最可爱了！"),
 ("mustang", "fma", "00s", ["mustang"], "罗伊·马斯坦", "ロイ・マスタング", "大川透",
  "黑色的军装与白手套，与指尖打响的火焰。",
  "「焰之炼金术师」，亚美斯特利斯的大佐。他要爬上大总统的位置，为伊修瓦尔的花海讨一个说法。","烧个精光吧。"),
 ("fuji-sd", "tennis", "00s", ["fuji syusuke", "shusuke", "fuji"], "不二周助", "不二周助", "甲斐田雪",
  "微睁的蓝色眼睛，与嘴角挂着的天使微笑。",
  "青春学园的「天才」，微笑的网球杀手。三重反击技「Triple Counter」是他温柔的外壳——真睁开眼时，球场就是他的。","还差得远呢。"),
 ("tezuka", "tennis", "00s", ["tezuka"], "手冢国光", "手塚国光", "置鲇龙太郎",
  "一丝不苟的短发，与镜片后零度的眼神。",
  "青春学园网球部部长，「青学的支柱」。全国制霸是他的军令状——左手零式抽杀，托起了整个队伍的脊梁。","大家，为青学而战。"),
 ("fujima", "slamdunk", "90s", ["fujima"], "藤真健司", "藤真健司", "神谷浩史",
  "清秀的面孔，与教练席上蓄势待发的目光。",
  "翔阳的队长兼教练，「神奈川双璧」的另一半。他坐在场边运筹，也随时可以上场终结比赛——樱木最想打倒的天才。","翔阳的时代是我们的。"),
 ("oikawa", "haikyuu", "10s", ["oikawa"], "及川彻", "及川徹", "浪川大辅",
  "茶褐色的短发，与伸出右手食指的挑衅笑容。",
  "青叶城西的队长，天才堆里的凡人王。「不要小看我们」——他用一万次发球练习，把「天赋」两个字打上了引号。","不要紧，下一球！"),
 ("lacus", "seed", "00s", ["lacus"], "拉克丝·克莱因", "ラクス・クライン", "田中理惠",
  "粉色的长发，与怀里的粉色哈罗。",
  "PLANT 的歌姬，克莱因议长的女儿。她用歌声反对战争，用温柔改写了 SEED 世界的结局。","为了和平的明天。"),
 ("jonouchi", "yugioh", "00s", ["jonouchi", "joey wheeler"], "城之内克也", "城之内克也", "高桥广树",
  "金色的长发与街头的义气，与牌组里的真红眼黑龙。",
  "游戏的挚友，「运气与热血」的决斗者。他从不良少年打到决斗者王国亚军——凡人的手腕，也能握住传奇。","真红眼黑龙！"),
 ("mr-satan", "dbz", "80s", ["mr. satan", "satan", "hercule"], "撒旦先生", "ミスター・サタン", "郷里大辅",
  "爆炸头的黑色卷发，与冠军腰带和一身肌肉。",
  "世界格斗冠军，「打倒沙鲁的英雄」。他不会气功，却敢站上最前线——凡人的勇气，有时候比神明更耀眼。","都交给我撒旦先生！"),
 ("ryuk", "deathnote", "00s", ["ryuk"], "琉克", "リューク", "松山鹰志",
  "高高的身材与苹果，与翅膀下咧开的尖牙笑。",
  "把死亡笔记丢进人间的死神。他不为善恶，只为解闷——盯着人类这场大戏，啃着苹果等结局。","人类真有趣。"),
 ("erwin", "titan", "10s", ["erwin", "erwin smith"], "埃尔文·史密斯", "エルヴィン・スミス", "小野大辅",
  "笔挺的军装立于调查兵团最前，与永远坚定的眉目。",
  "调查兵团团长，「献出心脏」的喊话者。他把所有人的心脏聚成一柄长枪——自己却成了那柄枪最好的枪尖。","献出你们的心脏！"),
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
for c in B9:
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

json.dump(report, open("/tmp/museum_b9_report.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
ok_n = sum(1 for c in report["characters"] if c["imageOk"])
print(f"\n=== 第八批完成：{ok_n}/{len(B9)}；未解决：{len(report['missing'])} ===", flush=True)
print(json.dumps(report["missing"], ensure_ascii=False))
