#!/usr/bin/env python3
# 第十一批策展：+27 位补强（五右卫门/日向小次郎/面堂/雅木茶/天津饭/早濑未沙/彩子/大和/海王满/雪代巴/安室透/明哥/白胡子/弥勒/雷欧力/神威/大蛇丸/鹿丸/Archer/喷火龙/童磨/早川秋/修拉赫特/黄昏/约尔/虹夏/西撒）
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
    "lupin": 1412, "tsubasa": 2116, "urusei": 1293, "dragonball": 223, "macross": 321,
    "slamdunk": 170, "digimon": 552, "sailormoon": 530, "kenshin": 45, "conan": 235,
    "onepiece": 21, "inuyasha": 249, "hxh": 136, "gintama": 918, "naruto": 20,
    "fatesn": 356, "pokemon": 527, "spy": 140960, "bocchi": 130003, "chainsaw": 127230, "frieren": 154587,
}
SEARCH = {
    "jojo2012":     dict(q="JoJo's Bizarre Adventure", ymin=2012, ymax=2012),
    "demon_slayer": dict(q="Kimetsu no Yaiba", ymin=2019, ymax=2019),
}

ANIME_META = {
    "lupin":        ("鲁邦三世(第二部)", "Lupin III: Part II", 1977, "Monkey Punch（加藤一彦）"),
    "tsubasa":      ("足球小将", "Captain Tsubasa", 1983, "高桥阳一"),
    "urusei":       ("福星小子", "Urusei Yatsura", 1981, "高桥留美子"),
    "dragonball":   ("龙珠", "Dragon Ball", 1986, "鸟山明"),
    "macross":      ("超时空要塞Macross", "Macross", 1982, "河森正治（Studio Nue）"),
    "slamdunk":     ("灌篮高手", "Slam Dunk", 1993, "井上雄彦"),
    "digimon":      ("数码宝贝大冒险", "Digimon Adventure", 1999, "本乡昭由（原案）"),
    "sailormoon":   ("美少女战士", "Sailor Moon", 1992, "武内直子"),
    "kenshin":      ("浪客剑心", "Rurouni Kenshin", 1996, "和月伸宏"),
    "conan":        ("名侦探柯南", "Detective Conan", 1996, "青山刚昌"),
    "onepiece":     ("海贼王", "One Piece", 1999, "尾田荣一郎"),
    "inuyasha":     ("犬夜叉", "InuYasha", 2000, "高桥留美子"),
    "hxh":          ("全职猎人", "Hunter × Hunter (1999)", 1999, "富坚义博"),
    "gintama":      ("银魂", "Gintama", 2006, "空知英秋"),
    "naruto":       ("火影忍者", "Naruto", 2002, "岸本齐史"),
    "fatesn":       ("Fate/stay night", "Fate/stay night", 2006, "TYPE-MOON"),
    "pokemon":      ("宝可梦", "Pokémon", 1997, "田尻智（原案）"),
    "demon_slayer": ("鬼灭之刃", "Demon Slayer: Kimetsu no Yaiba", 2019, "吾峠呼世晴"),
    "chainsaw":     ("电锯人", "Chainsaw Man", 2022, "藤本树"),
    "frieren":      ("葬送的芙莉莲", "Frieren: Beyond Journey's End", 2023, "山田钟人 · 阿部司"),
    "spy":          ("间谍过家家", "SPY × FAMILY", 2022, "远藤达哉"),
    "bocchi":       ("孤独摇滚!", "BOCCHI THE ROCK!", 2022, "はまじあき（芳文社）"),
    "jojo2012":     ("JOJO的奇妙冒险", "JoJo's Bizarre Adventure (TV)", 2012, "荒木飞吕彦"),
}

# (cid, animeKey, hall, [搜索token], 名中, 名日, 声优, 观察引导, 讲解词, 名台词)
B11 = [
 ("goemon", "lupin", "80s", ["goemon"], "十三代目石川五右卫门", "石川五エ門", "石丸博也",
  "深色的和服与腰间的居合刀，与永远最早收刀的从容。",
  "鲁邦一伙的剑豪，居合斩的高手。他话最少、刀最快——斩完之后把刀立起来抖一刀，是他全部的仪式感。","又是一刀两断。"),
 ("hyuga-k", "tsubasa", "80s", ["hyuga", "kojiro"], "日向小次郎", "日向小次郎", "饭冢昭三",
  "剃刀般的目光，与猛虎扑食般的射门姿态。",
  "东邦的王牌前锋，「猛虎射门」的创始人。大空翼一生的宿敌——他用最硬的脚法，把足球踢成了热血漫。","猛虎射门！"),
 ("mendou", "urusei", "80s", ["mendou", "shutaro"], "面堂终太郎", "面堂終太郎", "神谷明",
  "学生会长制服与身后的刀剑收藏，与自恋到发光的脸。",
  "面堂财阀的独生子，拉姆心中的完美未婚夫候补。诸星当的情敌——他的完美，是这部闹剧里最好笑的包袱。","我这般完美，你懂什么！"),
 ("yamcha", "dragonball", "80s", ["yamcha"], "雅木茶", "ヤムチャ", "宫内幸平",
  "脸上的伤疤与棒球手套，与年轻时狼牙风风拳的架势。",
  "前沙漠大盗，布尔玛的初恋。后来他成了龙珠世界最强棒球选手——伤疤是岁月，幽默是温柔。","狼牙风风拳！"),
 ("tenzin", "dragonball", "80s", ["tien", "tenshinhan"], "天津饭", "天津飯", "绪方贤一",
  "额头上的第三只眼，与道服下扎马步的双腿。",
  "鹤仙人门下的英才，与悟空从宿敌变成战友。他的「气功炮」是燃烧生命的决死技——三只眼睛看得比谁都认真。","气功炮！"),
 ("misa-hayase", "macross", "80s", ["misa hayase", "hayase"], "早濑未沙", "早瀬未沙", "土井美加",
  "统合军的军装与一丝不苟的短发。",
  "超时空要塞的舰桥军官，一条辉的上司。从命令到恋爱——她在明美的歌声背后，撑起了这部宇宙 romantic 的另一半。","一条君，出击！"),
 ("ayako", "slamdunk", "90s", ["ayako"], "彩子", "彩子", "原荣里子",
  "利落的马尾与篮球队经理的手账。",
  "湘北的经理，赤木的青梅竹马。她管住这群问题儿童，也懂每一个人的软肋——队里最清醒的人。","樱木，基础练习去！"),
 ("yamato-d", "digimon", "90s", ["yamato", "yamato ishida"], "石田大和", "石田ヤマト", "风间勇刀",
  "金色的狮子头与口琴，与胸前的友情徽章。",
  "太一的挚友与对照，加布兽的搭档。他从「别扭的弟弟」长成「可靠的哥哥」——友气的徽章是全剧最难亮起的一枚。","加布兽进化！"),
 ("michiru", "sailormoon", "90s", ["michiru", "michiru kaioh"], "海王满", "海王みちる", "峰惠子",
  "海蓝色的波浪长发，与手中的深海镜。",
  "水手海王星，天王遥的搭档。小提琴与绘画的天才——她与遥的默契，是美战最优雅的一道风景。","深海镜射！"),
 ("tomoe-y", "kenshin", "90s", ["tomoe", "yukishiro tomoe"], "雪代巴", "雪代巴", "岩男润子",
  "素白的和服与头上的红色发带，与垂眸时的静。",
  "剑心的妻子，幕末阴谋里的无辜者。她脸上的那道伤，就是剑心十字伤的起点——最安静的悲剧女主角。","对不起……丈夫。"),
 ("amuro-t", "conan", "90s", ["amuro tooru", "tooru amuro", "furuya"], "安室透", "安室透", "古谷彻",
  "波洛咖啡厅的围裙与便服，与沉静微笑下的锐利。",
  "公安警察降谷零，组织代号「波本」。在黑衣组织、公安与咖啡店之间的三重人生——柯南世界最忙碌的男人。","我是公安警察，降谷零。"),
 ("doflamingo", "onepiece", "90s", ["doflamingo"], "唐吉诃德·多弗朗明哥", "ドンキホーテ・ドフラミンゴ", "田中秀幸",
  "永远摘不下来的墨镜，与粉红色的羽毛大衣。",
  "「天夜叉」，德雷斯罗萨的黑暗国王。线线果实的操纵者——他把自己的过去织成一张困住全国的网。","海贼就是海贼！"),
 ("whitebeard", "onepiece", "90s", ["whitebeard", "newgate"], "爱德华·纽盖特（白胡子）", "エドワード・ニューゲート", "园部启一",
  "月牙般的白色胡须，与薙刀「丛云切」和满身的输液管。",
  "四皇之一的「世界最强男人」，把船员都唤作儿子。顶上战争那一战与那句话，是整个大航海时代最响的回声。","ONE PIECE 是真实存在的！"),
 ("miroku", "inuyasha", "00s", ["miroku"], "弥勒", "弥勒", "辻谷耕史",
  "僧袍与念珠，与右手掌心的黑色风穴。",
  "流浪的法师，风穴的诅咒传人。好色又可靠，法术与玩笑齐飞——诅咒尽头的自由，是他一路向前的理由。","风穴！"),
 ("leorio", "hxh", "90s", ["leorio"], "雷欧力", "レオリオ", "乡田穗积",
  "深色的西装与手提箱，与藏在箱子里的医书。",
  "为了免费学医而参加猎人试验的大哥。他是最像普通人的伙伴——怒吼与小杰的眼泪，是猎人最动人的开场。","我只是想当医生，救那些穷人。"),
 ("kamui", "gintama", "00s", ["kamui"], "神威", "神威", "日野聪",
  "夜兔族的单肩背包与长辫，与笑起来眯成缝的眼睛。",
  "神乐的哥哥，春雨第七师团长。战斗天才的空洞微笑——银魂最狠的反派，也是最可怜的孩子。","来战斗吧。"),
 ("orochimaru", "naruto", "00s", ["orochimaru"], "大蛇丸", "大蛇丸", "Kujira",
  "蛇一般竖瞳与长舌，与草薙剑和蜕下的蛇皮。",
  "传说中的三忍之一，禁术的不懈追求者。他把佐助当作下一个容器——火影世界最冷的「老师」。","想要力量的话，来找我吧。"),
 ("shikamaru", "naruto", "00s", ["shikamaru"], "奈良鹿丸", "奈良シカマル", "森久保祥太郎",
  "梳起的马尾与手里永远下不完的将棋。",
  "奈良一族的军师，IQ 200 的天才战略家。他把「真麻烦」挂在嘴边，却愿意为伙伴拼上性命——云淡风轻的英雄。","真麻烦啊……"),
 ("archer", "fatesn", "00s", ["archer"], "Archer（英灵卫宫）", "アーチャー", "诹访部顺一",
  "红色的大衣与白色的双剑，与讥讽笑容里的疲惫。",
  "不属于任何时代的英灵，红A。他与士郎的对话是整部 Fate 的题眼——否定理想的自己，才是最痛的考验。","I am the bone of my sword."),
 ("charizard", "pokemon", "90s", ["charizard"], "喷火龙", "リザードン", "三木真一郎",
  "喷火的尾巴与翅膀上的旧伤，与爱睡火山口的习惯。",
  "小智最倔强的伙伴，从「不听话」到王牌的对决成长史。对里奇一战，它把骄傲烧成了真正的火焰。","喷火龙，火焰旋涡！"),
 ("douma", "demon_slayer", "20s", ["douma", "doma"], "童磨", "童磨", "冈本信彦",
  "彩虹色的眼睛与手上的双扇，与永远无害的微笑。",
  "上弦之贰，万世极乐教的教主。笑容背后的虚无是全篇最冷的恐怖——他不理解痛苦，所以格外残忍。","一起成佛吧。"),
 ("aki", "chainsaw", "20s", ["aki hayakawa", "hayakawa"], "早川秋", "早川アキ", "坂田将吾",
  "梳得一丝不苟的黑发与公文包，与西装修身的手感。",
  "公安对魔特异四课的前辈，电次与帕瓦的监护人。他与未来恶魔的契约，是这部混沌物语里最扎心的伏笔。","电次，拜托了。"),
 ("stark", "frieren", "20s", ["stark"], "修拉赫特", "シュタルク", "小林千晃",
  "战士的红色战衣，与握到发白的手柄。",
  "勇者一行的传人，芙莉莲旅途上的护卫。他胆小得可爱，却总在最危险的时刻站到最前面——恐惧与勇气从来共存。","我可是要保护大家的男人！"),
 ("loid", "spy", "20s", ["loid", "twilight"], "劳埃德·福杰（黄昏）", "ロイド・フォージャー", "浪川大辅",
  "绿色的西装与无框眼镜，与推起来的报纸。",
  "西德海姆的头号间谍「黄昏」，为了任务组建临时家庭。他从演一个父亲，到真的成为父亲——谍战喜剧里最柔软的伏线。","阿尼亚，爸爸没事。"),
 ("yor", "spy", "20s", ["yor", "yor briar"], "约尔·福杰", "ヨル・フォージャー", "种崎敦美",
  "黑色的刺杀装束与发间的玫瑰花饰。",
  "白天是市政厅的职员，夜里是杀手「荆棘公主」。她下手没轻重，持家也没轻重——这个家的妈妈，是全世界最危险的太太。","我下手没轻重，请多包涵。"),
 ("nijika", "bocchi", "20s", ["nijika"], "伊地知虹夏", "伊地知虹夏", "铃代纱弓",
  "金色的侧马尾与鼓棒，与额头三角发卡。",
  "下北泽 live house「STARRY」的鼓手，团结乐队的太阳。是她把波奇从纸箱里捡进了乐队——青春喜剧的心跳担当。","波奇酱，一起上吧！"),
 ("caesar", "jojo2012", "10s", ["caesar", "zeppeli"], "西撒·齐贝林", "シーザー・ツェペリ", "佐藤拓也",
  "泡泡般的战斗服纹样，与指间飞出的波纹气泡。",
  "齐贝林家的波纹天才，乔瑟夫的挚友与对手。他与乔瑟夫的诀别，是 JOJO 初代篇最悲恸的一页——泡沫破碎之前，他从未服输。","西撒·齐贝林，来应战了！"),
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
for c in B11:
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
            ok = True
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

json.dump(report, open("/tmp/museum_b11_report.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
ok_n = sum(1 for c in report["characters"] if c["imageOk"])
print(f"\n=== 第八批完成：{ok_n}/{len(B11)}；未解决：{len(report['missing'])} ===", flush=True)
print(json.dumps(report["missing"], ensure_ascii=False))
