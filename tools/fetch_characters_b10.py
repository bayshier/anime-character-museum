#!/usr/bin/env python3
# 第十批策展：+30 位高人气补强（布欧/巴达克/托奇/泽北/琴酒/天王遥/斋藤一/酷拉皮卡/太一/美冴/罗/女帝/迹部/桂/纲手/斑/日番谷/乌尔奇奥拉/格雷/凛/士郎/阿尔冯斯/朋也/长门有希/西谷/猗窝座/徐伦/帕瓦/费伦）
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
    "dbz": 813, "hokuto": 967, "slamdunk": 170, "conan": 235, "sailormoon": 530,
    "kenshin": 45, "hxh": 136, "digimon": 552, "shinchan": 966, "onepiece": 21,
    "tennis": 22, "gintama": 918, "naruto": 20, "bleach": 269, "fairytail": 6702,
    "fatesn": 356, "fma": 121, "haikyuu": 20464, "haruhi": 849,
    "chainsaw": 127230, "frieren": 154587, "yugioh": 481,
}
SEARCH = {
    "clannad":     dict(q="CLANNAD", ymin=2007, ymax=2008),
    "demon_slayer": dict(q="Kimetsu no Yaiba", ymin=2019, ymax=2019),
    "jojo_sea":    dict(q="JoJo's Bizarre Adventure: Stone Ocean", ymin=2021, ymax=2022),
}

ANIME_META = {
    "dbz":          ("龙珠Z", "Dragon Ball Z", 1989, "鸟山明"),
    "hokuto":       ("北斗神拳", "Fist of the North Star", 1984, "武论尊 · 原哲夫"),
    "slamdunk":     ("灌篮高手", "Slam Dunk", 1993, "井上雄彦"),
    "conan":        ("名侦探柯南", "Detective Conan", 1996, "青山刚昌"),
    "sailormoon":   ("美少女战士", "Sailor Moon", 1992, "武内直子"),
    "kenshin":      ("浪客剑心", "Rurouni Kenshin", 1996, "和月伸宏"),
    "hxh":          ("全职猎人", "Hunter × Hunter (1999)", 1999, "富坚义博"),
    "digimon":      ("数码宝贝大冒险", "Digimon Adventure", 1999, "本乡昭由（原案）"),
    "shinchan":     ("蜡笔小新", "Crayon Shin-chan", 1992, "臼井仪人"),
    "onepiece":     ("海贼王", "One Piece", 1999, "尾田荣一郎"),
    "tennis":       ("网球王子", "The Prince of Tennis", 2001, "许斐刚"),
    "gintama":      ("银魂", "Gintama", 2006, "空知英秋"),
    "naruto":       ("火影忍者", "Naruto", 2002, "岸本齐史"),
    "bleach":       ("死神", "Bleach", 2004, "久保带人"),
    "fairytail":    ("妖精的尾巴", "Fairy Tail", 2009, "真岛浩"),
    "fatesn":       ("Fate/stay night", "Fate/stay night", 2006, "TYPE-MOON"),
    "fma":          ("钢之炼金术师", "Fullmetal Alchemist", 2003, "荒川弘"),
    "haikyuu":      ("排球少年!!", "Haikyuu!!", 2014, "古馆春一"),
    "haruhi":       ("凉宫春日的忧郁", "The Melancholy of Haruhi Suzumiya", 2006, "谷川流"),
    "chainsaw":     ("电锯人", "Chainsaw Man", 2022, "藤本树"),
    "frieren":      ("葬送的芙莉莲", "Frieren: Beyond Journey's End", 2023, "山田钟人 · 阿部司"),
    "clannad":      ("CLANNAD", "CLANNAD", 2007, "Key"),
    "demon_slayer": ("鬼灭之刃", "Demon Slayer: Kimetsu no Yaiba", 2019, "吾峠呼世晴"),
    "jojo_sea":     ("JOJO的奇妙冒险 石之海", "JoJo's Bizarre Adventure: Stone Ocean", 2021, "荒木飞吕彦"),
}

# (cid, animeKey, hall, [搜索token], 名中, 名日, 声优, 观察引导, 讲解词, 名台词)
B10 = [
 ("buu", "dbz", "80s", ["buu"], "魔人布欧", "魔人ブウ", "盐屋浩三",
  "粉红色的圆滚滚身躯，与头顶那根弯弯的触角。",
  "比比迪创造的魔人，封印数十亿年后被巴菲迪唤醒。他会把敌人变成巧克力吃掉，也会因为一颗糖球而脾气爆发——纯粹的破坏，天真的恐怖。","布欧要把你变成糖果！"),
 ("bardock", "dbz", "80s", ["bardock"], "巴达克", "バーダック", "野泽雅子",
  "战斗服与满脸伤疤，与腰间那条染血的腰带。",
  "悟空的父亲，赛亚人的下级战士。他预见到了星球毁灭的未来，独自迎向弗利萨的死亡之球——赛亚人的骄傲在他身上燃烧到最后一秒。","悟空……拜托你了。"),
 ("toki", "hokuto", "80s", ["toki"], "托奇", "トキ", "",
  "温和的浅色长袍，与修罗一般的消瘦面容。",
  "北斗神拳传人之一，健次郎的义兄。他把绝症留给自己，把温柔留在拉欧与健次郎之间——修武之国最悲伤的圣人。","健次郎，北斗神拳就托付给你了。"),
 ("sawakita", "slamdunk", "90s", ["sawakita"], "泽北荣治", "沢北栄治", "堀秀行",
  "标志性的爆炸卷发，与球场上漫不经心的运球。",
  "山王的王牌，高中篮球界的「第一人」。他在与流川枫的一对一里教会了天才什么叫差距——也让全国大赛的最后一秒成为传说。","日本第一。"),
 ("gin", "conan", "90s", ["gin"], "琴酒", "ジン", "堀内贤雄",
  "银白色的长发，与黑色风衣下永远冷冽的眼神。",
  "黑衣组织的核心成员，伏特加的上司。新一被他灌下毒药变成柯南——整部作品的起点，就是他扣下扳机的那一瞬。","組織に隙は無い。"),
 ("haruka", "sailormoon", "90s", ["haruka tenou", "tenou"], "天王遥", "天王はるか", "绪方惠美",
  "利落的金色短发，与赛车手套和男性化的着装。",
  "水手天王星，外部太阳系战士。她以假小子的身份登场迷倒众生——驾驶跑车的守护者，与海王满组成最酷的二人组。","世界震荡！"),
 ("saito-h", "kenshin", "90s", ["saitou hajime", "hajime saito", "saito"], "斋藤一", "斎藤一", "铃置洋孝",
  "警察制服与竖起的锋利目光，与牙间咬着的香烟。",
  "前新选组三番队长，流亡于明治时代的「恶·即·斩」。他与剑心从死斗走向默契——警察的刀，比浪客的剑更冷更直。","悪・即・斬！"),
 ("kurapika", "hxh", "90s", ["kurapika"], "酷拉皮卡", "クラピカ", "甲斐田雪",
  "栗色的及肩发，与眼眸燃烧成绯红的一瞬。",
  "窟卢塔族的最后幸存者，为族人的眼睛向幻影旅团复仇。锁链手是他的誓言也是他的枷锁——猎人世界最悲壮的复仇者。","我要把你们全部送进监狱！"),
 ("taichi", "digimon", "90s", ["taichi", "taichi kamiya"], "八神太一", "八神太一", "藤田淑子",
  "护目镜与勇敢徽章，与冲锋在最前的笑。",
  "被选召的孩子们的首领，勇气的化身。他从莽撞的足球少年成长为真正的领袖——数码世界的冒险，是整个平成的暑假。","亚古兽进化！"),
 ("misae", "shinchan", "90s", ["misae", "misae nohara"], "野原美冴", "野原みさえ", "楢桥美纪",
  "烫起的卷发与家居服，与手里追打小新的扫帚。",
  "野原家的主妇，小新的母亲。她为房贷与孩子的叛逆操碎了心——每一次「小新——！」的怒吼，都是最日常的亲情喜剧。","小新——！！"),
 ("law", "onepiece", "90s", ["trafalgar law", "trafalgar"], "特拉法尔加·罗", "トラファルガー・ロー", "神谷浩史",
  "绒帽与斑点牛仔裤，与腰间佩刀「鬼哭」。",
  "心脏海贼团的船长，手术果实的「死神」。他与路飞结成海贼同盟——冷静的外科医生，把整个新世界当成了手术室。"," ROOM！"),
 ("hancock", "onepiece", "90s", ["boa hancock", "hancock"], "波雅·汉库克", "ボア・ハンコック", "三石琴乃",
  "乌黑的长发与蛇形耳环，与女儿岛的王者仪态。",
  "九蛇海贼团船长，王下七武海唯一的女性，「海贼女帝」。她美得让全世界原谅她，却只在路飞面前脸红——傲娇女帝的恋爱病。","甜甜甘风！"),
 ("atobe", "tennis", "00s", ["atobe"], "迹部景吾", "跡部景吾", "诹访部顺一",
  "眼角的泪痣与紫色发梢，与球场王座般的气场。",
  "冰帝学园网球部的部长，「冰帝的女王」。三百球发球挑战与「沉醉在本大爷的华丽球技下吧」——他的自信就是他的美学。","沉醉在本大爷的球技下吧！"),
 ("katsura", "gintama", "00s", ["katsura"], "桂小太郎", "桂小太郎", "石田彰",
  "紫色的长发与木刀，与那一身攘夷志士的和服。",
  "攘夷志士「攘夷浪士的桂」，银时的旧战友。他不叫假发——全书最执着的自我介绍梗，藏着江户最温柔的理想主义者。","不是假发，是桂！"),
 ("tsunade", "naruto", "00s", ["tsunade"], "纲手", "綱手", "胜生真沙子",
  "额头的阴封印与辫起的金发，与颈间的项链。",
  "传说中的三忍之一，木叶的第五代火影。她是医疗忍者的巅峰，也是赌场里人人躲着的「传说中的大肥羊」——最强女忍者的另一面。","百豪之术！"),
 ("madara", "naruto", "00s", ["madara uchiha", "madara"], "宇智波斑", "うちはマダラ", "",
  "乌黑的长发与血轮眼，与战甲上的宇智波团扇。",
  "宇智波一族的传奇首领，与初代火影共同建立木叶。他从历史里复活，把整个忍界拖进了「月之眼计划」——真正的终局棋手。","无限月读！"),
 ("hitsugaya", "bleach", "00s", ["hitsugaya"], "日番谷冬狮郎", "日番谷冬獅郎", "朴璐美",
  "矮小的少年身形，与背上冰天雪花的斩魄刀。",
  "十番队队长，尸魂界最年幼的队长天才。「冰轮丸」是他背后的千年冰龙——天才的负担，比谁都沉重。","冰轮丸！"),
 ("ulquiorra", "bleach", "00s", ["ulquiorra"], "乌尔奇奥拉·西法", "ウルキオラ・シファー", "石田彰",
  "绿色的眼线泪痕，与腰间的月牙刀。",
  "虚圈的第四刃，最像人类的破面。他追问「心」是什么，直到化作尘埃的那一刻才真正明白——虚圈最安静的哲学家。","虚闪。"),
 ("gray", "fairytail", "00s", ["gray fullbuster", "gray"], "格雷·佛尔巴斯特", "グレイ・フルバスター", "中村悠一",
  "永不穿够衣服的习惯，与双手结印的冰之造型魔法。",
  "妖尾的冰之造型魔导士，纳兹的宿敌兼挚友。火与冰的斗嘴撑起了公会的日常——冰冻的铠甲下是最热的义气。","冰之造型！"),
 ("rin", "fatesn", "00s", ["rin tohsaka", "tohsaka rin", "rin"], "远坂凛", "遠坂凛", "植田佳奈",
  "双马尾的黑发与红色上衣，与指尖的宝石魔术。",
  "远坂家的魔术师，第五次圣杯战争的参加者。外表完美的大小姐，私下是冒失的「宝石翁」——Fate 世界最真实的傲娇名门。","宝石魔术！"),
 ("shiro", "fatesn", "00s", ["shirou emiya", "emiya", "shirou"], "卫宫士郎", "衛宮士郎", "杉山纪彰",
  "红色的外套与投影魔术，与那双不会放弃的眼睛。",
  "冬木市的高中生，第八位的伪魔术师。他继承了养父「成为正义伙伴」的遗志——哪怕世界的答案是无情，也要挥出那把剑。","我要成为正义的伙伴！"),
 ("alphonse", "fma", "00s", ["alphonse", "alphonse elric"], "阿尔冯斯·艾尔利克", "アルフォンス・エルリック", "钉宫理惠",
  "全身的巨大铠甲，与头盔上的一缕呆毛。",
  "爱德华的弟弟，灵魂被封印在铠甲里的少年。钢铁之躯里装着最柔软的心——钢之炼金术师最温柔的注脚。","哥哥……！"),
 ("tomoya", "clannad", "00s", ["tomoya okazaki", "okazaki", "tomoya"], "冈崎朋也", "岡崎朋也", "中村悠一",
  "校服外套下的散漫，与球场上挥出的那只手。",
  "光坂高中的不良少年，遇见渚之后人生开始转弯。他从留级的日常走到组建家庭——CLANNAD 用一生讲完「家族」二字。","团子大家族。"),
 ("nagato-y", "haruhi", "00s", ["yuki nagato", "nagato"], "长门有希", "長門有希", "茅原实里",
  "齐刘海短发与眼镜，与永远抱在手里的书本。",
  "SOS团的沉默社员，资讯统合思念体的对有机生命体接触用人形界面。她话最少，改变世界的次数却最多——朝比奈的叹息里的天才少女。","……嗯。"),
 ("nishinoya", "haikyuu", "10s", ["nishinoya"], "西谷夕", "西谷夕", "村濑步",
  "过肩的金黑挑染长发，与自由人位置的十字接球。",
  "乌野的自由人，「守护神」本尊。一米五九的身材挡下全国最强的扣杀——他不上场发球只是因为「不想输给别人」。","滚雷！"),
 ("akaza", "demon_slayer", "20s", ["akaza"], "猗窝座", "猗窩座", "石田彰",
  "粉色的短发与全身的刺青，与拳法家的战斗姿态。",
  "上弦之参，无限列车篇的最终强敌。他不杀不吃女人，毕生追求最强——黎明的钟声里，那段武士人生的记忆让人心碎。","破坏杀·罗针！"),
 ("jolyne", "jojo_sea", "20s", ["jolyne", "jolyne cujoh"], "空条徐伦", "ジョリーン・キュージョー", "种崎敦美",
  "绿色的双发髻，与被陷害入狱的绿海豚街。",
  "乔斯达家族第六代，空条承太郎的女儿。她被陷害入狱，却用线之替身在绿海豚街写下最悲壮的家族终章。","石之自由！"),
 ("power", "chainsaw", "20s", ["power"], "帕瓦", "パワー", "村川梨衣",
  "双角的恶魔之姿，与抱着喵喵帕的表情。",
  "血之恶魔，公安对魔特异四课的搭档。她自大、撒谎、不讲卫生，却会在关键时刻挡在电次身前——最讨厌也最可爱的伙伴。","帕瓦大人登场！"),
 ("fern", "frieren", "20s", ["fern"], "费伦", "フェルン", "市之濑加那",
  "紫色的长发与冷淡的眼神，与身后那根魔法杖。",
  "芙莉莲的弟子，失去一切的战争孤儿。她把师父管得服服帖帖——攻撃魔法的天才少女，用最短的时间追上了精灵的百年。","师父，快起来。"),
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
for c in B10:
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

json.dump(report, open("/tmp/museum_b10_report.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
ok_n = sum(1 for c in report["characters"] if c["imageOk"])
print(f"\n=== 第八批完成：{ok_n}/{len(B10)}；未解决：{len(report['missing'])} ===", flush=True)
print(json.dumps(report["missing"], ensure_ascii=False))
