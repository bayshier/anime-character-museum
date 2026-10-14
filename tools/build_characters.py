#!/usr/bin/env python3
# 合并三批抓取结果 → assets/characters.js
import json, os

repo = "/Users/radar/Downloads/gitlab127001/anime-character-museum"
r1 = json.load(open("/tmp/museum_fetch_report.json", encoding="utf-8"))
r2 = json.load(open("/tmp/museum_fetch2_report.json", encoding="utf-8"))
rp = json.load(open("/tmp/museum_patch_report.json", encoding="utf-8"))

# 第一批作品的展示元数据
KNOWN_META = {
    "doraemon":("哆啦A梦","Doraemon (1979)",1979),"gundam":("机动战士高达","Mobile Suit Gundam",1979),
    "astroboy":("铁臂阿童木","Astro Boy (1980)",1980),"drslump":("阿拉蕾（IQ博士）","Dr. Slump",1981),
    "urusei":("福星小子","Urusei Yatsura",1981),"tsubasa":("足球小将","Captain Tsubasa",1983),
    "hokuto":("北斗神拳","Fist of the North Star",1984),"dragonball":("龙珠","Dragon Ball",1986),
    "seiya":("圣斗士星矢","Saint Seiya",1986),"cityhunter":("城市猎人","City Hunter",1987),
    "ranma":("乱马½","Ranma ½",1989),"dbz":("龙珠Z","Dragon Ball Z",1989),
    "maruko":("樱桃小丸子","Chibi Maruko-chan",1990),"sailormoon":("美少女战士","Sailor Moon",1992),
    "yyh":("幽游白书","Yu Yu Hakusho",1992),"shinchan":("蜡笔小新","Crayon Shin-chan",1992),
    "slamdunk":("灌篮高手","Slam Dunk",1993),"eva":("新世纪福音战士","Neon Genesis Evangelion",1995),
    "kenshin":("浪客剑心","Rurouni Kenshin",1996),"letsgo":("四驱兄弟","Let's & Go!!",1996),
    "conan":("名侦探柯南","Detective Conan",1996),"pokemon":("宝可梦","Pokémon",1997),
    "onepiece":("海贼王","One Piece",1999),"digimon":("数码宝贝大冒险","Digimon Adventure",1999),
}
B1_OVERRIDES = {  # 第一批已定案的修正
    "maruko":  {"anilistCharId": 9528,  "nameEn": "Momoko Sakura"},
    "yusuke":  {"anilistCharId": 729,   "nameEn": "Yusuke Urameshi"},
    "goseiba": {"anilistCharId": 25450, "nameEn": "Go Seiba"},
}
NAME_DISPLAY = {
    "goku": "Son Goku", "luffy": "Monkey D. Luffy", "astroboy": "Astro Boy",
    "ryo": "Ryo Saeba", "ash": "Ash Ketchum", "kenshiro": "Kenshiro",
    "mao": "Liu Maoxing", "gian": "Takeshi Goda (Gian)", "dboy": "D-Boy (Takaya Aoba)",
    "jotaro": "Jotaro Kujo", "oscar": "Oscar de Jarjayes",
}
DROP_QUOTES = {"vegeta"}

chars = {c["id"]: c for c in r1["characters"]}
for cid, ov in B1_OVERRIDES.items():
    if cid in chars:
        chars[cid].update(ov)

for c in r2["characters"]:
    if c["id"] in chars:
        continue
    akey = c["animeKey"]
    if akey in KNOWN_META:
        c["animeZh"], c["animeEn"], c["year"] = KNOWN_META[akey]
    c["source"] = f"https://anilist.co/character/{c['anilistCharId']}" if c.get("anilistCharId") else ""
    chars[c["id"]] = c

# 补丁批次
PATCH_ANIME_YEAR = {"minmay": 1982, "hikaru-m": 1982, "focker": 1982, "lunlun-c": 1979, "maruko": 1990, "yusuke": 1992}
PATCH_META = {
    "minmay":  ("超时空要塞Macross", "Macross", "河森正治（Studio Nue）"),
    "hikaru-m":("超时空要塞Macross", "Macross", "河森正治（Studio Nue）"),
    "focker":  ("超时空要塞Macross", "Macross", "河森正治（Studio Nue）"),
    "krillin": ("龙珠", "Dragon Ball", "鸟山明"),
    "trunks":  ("龙珠Z", "Dragon Ball Z", "鸟山明"),
    "frieza":  ("龙珠Z", "Dragon Ball Z", "鸟山明"),
    "sendoh":  ("灌篮高手", "Slam Dunk", "井上雄彦"),
    "gian":    ("哆啦A梦", "Doraemon (1979)", "藤子·F·不二雄"),
    "kero":    ("魔卡少女樱", "Cardcaptor Sakura", "CLAMP"),
    "lunlun-c":("花仙子", "Hana no Ko Lunlun (1979)", "神保史郎（东映）"),
    "maruko":  ("樱桃小丸子", "Chibi Maruko-chan", "樱桃子"),
    "yusuke":  ("幽游白书", "Yu Yu Hakusho", "富坚义博"),
}
PATCH_BASE = {  # 补丁人物的基础档案（与策展表一致）
    "krillin": ("克林","クリリン","中尾隆圣","80s","dragonball",
      "没有鼻子的圆脸，和额头的六颗点。","悟空最好的伙伴，地球人出身的最强战士之一。没有赛亚人的血统，却一次次站在最强的敌人面前。",""),
    "trunks": ("特兰克斯","トランクス","草尾毅","80s","dbz",
      "淡紫色的短发，和背上的勇者之剑。","从毁灭的未来逆流而来的少年，独自一人向命运挥剑。他的出现，让「绝望」第一次有了退路。",""),
    "frieza": ("弗利萨","フリーザ","中尾隆圣","80s","dbz",
      "雪白的躯体、紫色的甲纹，和优雅的漂浮姿态。","宇宙帝王的优雅与残忍并存，那美克星之战的最终黑暗。他的存在定义了「绝望的强度」。",""),
    "sendoh": ("仙道彰","仙道彰","岛田敏","90s","slamdunk",
      "额前垂下的一缕发，与懒洋洋的笑容。","陵南的王牌，神奈川最全面的天才。与流川枫、樱木的对位，是全作最华丽的锋线对决。",""),
    "gian": ("刚田武（胖虎）","剛田武（ジャイアン）","立壁和也","80s","doraemon",
      "壮硕的身板，与永远跑调的演唱会。","孩子的孩子王，用拳头与「演唱会」统治空地。粗鲁的外表下，是最讲义气的邻居大哥。","你的东西就是我的东西。"),
    "shinichi": ("工藤新一","工藤新一","山口胜平","90s","conan",
      "校服下的侦探气质，与福尔摩斯式的自信。","让案件无所遁形的高中生侦探。被灌下毒药之前，他是平成年间最耀眼的「平成福尔摩斯」。","我是高中生侦探工藤新一！"),
    "kero": ("可鲁贝洛斯（小可）","ケルベロス","久川绫","90s","ccsakura",
      "黄色的圆翅膀，和永远叼着的甜点。","库洛牌的守护兽，封印期间退化成吃点小甜食的毛绒玩具。嘴上嫌弃小樱，关键时刻最拼命。",""),
    "lunlun-c": ("小蓓","ルンルン","冈本茉莉","80s","lunlun",
      "黄色的帽子，与随行的会说话小狗小猫。","寻找七色花的旅行少女，一路走过欧洲的风光。华语世界的第一批「少女番」记忆。",""),
    "maruko": ("樱桃小丸子","さくらももこ","TARAKO","90s","maruko",
      "锯齿状的刘海、红白小帽，和「嘿嘿」的懒散笑。","清水市小学三年级学生，讨厌功课、爱睡懒觉，与爷爷友藏一家过着鸡毛蒜皮又暖洋洋的日子。平成家庭剧场的治愈原点。",""),
    "yusuke": ("浦饭幽助","浦飯幽助","佐佐木望","90s","yyh",
      "墨绿的学兰制服，与指尖聚起灵气的灵丸手势。","为救人而死的不良少年，经灵界测试重生为灵界侦探。从街头斗殴到暗黑武术会，富坚义博的热血与狡黠在他身上同时闪光。","灵丸！"),
    "minmay": ("林明美","リン・ミンメイ","饭岛真理","80s","macross",
      "乌黑的长发，与舞台上闪亮的偶像裙摆。","从中华料理店女孩到宇宙偶像，一首《爱·おぼえていますか》让敌我双方同时放下了武器。",""),
    "hikaru-m": ("一条辉","一条輝","长谷有洋","80s","macross",
      "统合军的飞行员制服，与 VF 战机座舱里的专注侧脸。","从杂技演员到统合军王牌，在明美与早濑未沙之间成长。第一次宇宙大战的王牌飞行员。",""),
    "focker": ("罗伊·福克","ロイ・フォッカー","神谷明","80s","macross",
      "骷髅中队徽章，与机身上涂满战功的白色 VF-1S。","一条辉的师父，骷髅战机的传奇队长。他的陨落教会了后辈：王牌的天空也有尽头。",""),
}
RECOVER = {  # patch2 报告被覆盖，macross 三人组从当时日志找回
    "minmay":  {"id": 5295, "nameEn": "Minmay Lynn"},
    "hikaru-m": {"id": 5301, "nameEn": "Hikaru Ichijou"},
    "focker":  {"id": 5826, "nameEn": "Roy Focker"},
}
for cid, base in PATCH_BASE.items():
    if cid == "shinichi":
        continue  # AniList 新一与柯南合并条目，撤下避免图不对题
    info = rp.get(cid) or {}
    rec = RECOVER.get(cid) or {}
    nid = info.get("id") or rec.get("id") or B1_OVERRIDES.get(cid, {}).get("anilistCharId")
    nameEn = info.get("nameEn") or rec.get("nameEn") or B1_OVERRIDES.get(cid, {}).get("nameEn", "")
    zh, jp, cv, hall, akey, feature, intro, quote = base
    zh2, en2, author = PATCH_META[cid]
    year = PATCH_ANIME_YEAR.get(cid, KNOWN_META.get(akey, (None, None, None))[2])
    chars[cid] = {
        "id": cid, "anilistCharId": nid, "nameEn": nameEn,
        "nameZh": zh, "nameJp": jp, "cv": cv, "hall": hall,
        "animeKey": akey, "animeZh": zh2, "animeEn": en2, "year": year,
        "author": author, "feature": feature, "intro": intro, "quote": quote,
        "image": f"exhibits/{cid}.jpg",
    }


# ---- 第三批（+12 作品 +15 人物）----
r3 = json.load(open("/tmp/museum_b3_report.json", encoding="utf-8"))
r3fix = json.load(open("/tmp/museum_b3_fix_report.json", encoding="utf-8"))
B3_YEAR = {"catseye":1983,"ginga999":1978,"versailles":1979,"maison":1986,"shurato":1989,
           "mononoke":1997,"gundam_w":1995,"initiald":1998,"gto":1999,"sainttail":1995,
           "rantarou":1993,"jojoova":1993,"dragonball":1986}
B3_BASE = {
    "tetsuro": ("星野铁郎","星野鉄郎","野泽雅子","80s","ginga999",
      "破旧的夹克，与对999号列车车票的执着。","为换取通往银河尽头的免费车票而踏上旅途的少年。机械伯爵与梅特尔的身影，是松本零士写给宇宙最长的挽歌。",""),
    "kyoko": ("音无响子","音無響子","","80s","maison",
      "围裙与长发，和一刻馆破旧楼梯上的灯光。","一刻馆的管理员寡妇，五代裕作暗恋的终点。温柔的笑容里藏着对亡夫的怀念——昭和恋爱喜剧的巅峰之作。",""),
    "roshi": ("龟仙人","武天老師","宫内幸平","80s","dragonball",
      "花白的胡须、墨镜与龟壳背心。","龟派气功的创始人，悟空与克林的师父。平时是好色老头，关键时刻是撑起地球的武道之神。",""),
    "rantarou": ("猪名寺乱太郎","猪名寺乱太郎","高山南","90s","rantarou",
      "圆圆的小脑袋，和忍者学园里永远背不完的功课。","贫苦农家出身的忍者见习生，与雾丸、しんべヱ的学园日常。轻松幽默里，是90年代国民级忍者喜剧。",""),
    "san": ("小桑","サン","石田百合子","90s","mononoke",
      "脸上的红色战纹，与白狼群并肩奔跑的身影。","被狼神养大的人类女孩，「幽灵公主」。在森林与人类之间，她用獠牙替森林嘶吼——宫崎骏最野性的女主角。",""),
}
for c in r3["characters"]:
    if c["id"] not in chars:
        c = dict(c)
        c["year"] = B3_YEAR.get(c["animeKey"])
        if c["id"] == "meimi":
            c["feature"] = "双马尾的少女，与夜晚蒙面的怪盗身影。"
        if c["id"] == "shurato":
            c["author"] = ""
        chars[c["id"]] = c
for cid, base in B3_BASE.items():
    fix = r3fix.get(cid)
    zh, jp, cv, hall, akey, feature, intro, quote = base
    if fix and fix.get("imageOk"):
        chars[cid] = {
            "id": cid, "anilistCharId": fix["anilistCharId"], "nameEn": fix["nameEn"],
            "nameZh": zh, "nameJp": jp, "cv": cv, "hall": hall,
            "animeKey": akey, "animeZh": r3["characters"][0]["animeZh"] if akey == "ginga999" else "",
            "year": B3_YEAR.get(akey), "author": "", "feature": feature, "intro": intro,
            "quote": quote, "image": f"exhibits/{cid}.jpg",
        }
# 第三批作品的展示名（animeZh/animeEn 从 b3 元数据兜底）
B3_META = {}
for c in r3["characters"]:
    B3_META.setdefault(c["animeKey"], (c["animeZh"], c["animeEn"]))
B3_META["mononoke"] = ("幽灵公主", "Princess Mononoke")
B3_META["rantarou"] = ("忍者乱太郎", "Nintama Rantarou")
B3_META["dragonball"] = ("龙珠", "Dragon Ball")
for c in chars.values():
    if c.get("animeKey") in B3_META and not c.get("animeEn"):
        c["animeZh"], c["animeEn"] = B3_META[c["animeKey"]]


# ---- 第四批（+12 作品 +18 人物）----
r4 = json.load(open("/tmp/museum_b4_report.json", encoding="utf-8"))
r4fix = json.load(open("/tmp/museum_b4_fix_report.json", encoding="utf-8"))
B4_YEAR = {"kikis":1989,"porco":1992,"whisper":1995,"nadia":1990,"sara":1985,"logh":1988,
           "escaflowne":1996,"tenchi":1992,"guruguru":1994,"kinniku":1983,"granzort":1989,"remi":1996}
for c in r4["characters"]:
    if c["id"] not in chars:
        c = dict(c)
        c["year"] = B4_YEAR.get(c["animeKey"])
        c["source"] = f"https://anilist.co/character/{c['anilistCharId']}"
        chars[c["id"]] = c
if "sara" in r4fix and r4fix["sara"].get("imageOk") and "sara" not in chars:
    fx = r4fix["sara"]
    chars["sara"] = {
        "id": "sara", "anilistCharId": fx["anilistCharId"], "nameEn": fx["nameEn"],
        "nameZh": "莎拉", "nameJp": "セーラ・クルー", "cv": "岛本须美", "hall": "80s",
        "animeKey": "sara", "animeZh": "小公主莎拉", "animeEn": "Princess Sara", "year": 1985,
        "author": "克莉丝蒂安娜·F（原作·世界名作剧场）", "feature": "洋娃娃般的卷发，与寄宿学校里昂起的小下巴。",
        "intro": "从万千宠爱到沦为女佣的「小公主」。明琪校长的冷眼之下，她把童话活成了尊严的寓言。",
        "quote": "", "image": "exhibits/sara.jpg",
        "source": fx["source"],
    }


# ---- 第五批（+8 作品 +20 人物）----
r5 = json.load(open("/tmp/museum_b5_report.json", encoding="utf-8"))
for c in r5["characters"]:
    if c["id"] not in chars:
        c = dict(c)
        c["source"] = f"https://anilist.co/character/{c['anilistCharId']}"
        chars[c["id"]] = c


# ---- 第六批（+26 作品 +44 人物：00/10/20 年代）----
r6 = json.load(open("/tmp/museum_b6_report.json", encoding="utf-8"))
for c in r6["characters"]:
    if c["id"] not in chars:
        c = dict(c)
        c["source"] = f"https://anilist.co/character/{c['anilistCharId']}"
        chars[c["id"]] = c


# ---- 第七批（+7 作品 +22 人物）----
r7 = json.load(open("/tmp/museum_b7_report.json", encoding="utf-8"))
for c in r7["characters"]:
    if c["id"] not in chars:
        c = dict(c)
        c.setdefault("source", "")
        if not c.get("source") and c.get("anilistCharId"):
            c["source"] = f"https://anilist.co/character/{c['anilistCharId']}"
        chars[c["id"]] = c


r8 = json.load(open("/tmp/museum_b8_report.json", encoding="utf-8"))
for c in r8["characters"]:
    if c["id"] not in chars:
        c = dict(c)
        c.setdefault("source", "")
        if not c.get("source") and c.get("anilistCharId"):
            c["source"] = f"https://anilist.co/character/{c['anilistCharId']}"
        chars[c["id"]] = c


r9 = json.load(open("/tmp/museum_b9_report.json", encoding="utf-8"))
for c in r9["characters"]:
    if c["id"] not in chars:
        c = dict(c)
        c.setdefault("source", "")
        if not c.get("source") and c.get("anilistCharId"):
            c["source"] = f"https://anilist.co/character/{c['anilistCharId']}"
        chars[c["id"]] = c

r10 = json.load(open("/tmp/museum_b10_report.json", encoding="utf-8"))
ANIME_META10 = {
    "dbz": ("龙珠Z", "Dragon Ball Z", 1989, "鸟山明"),
    "hokuto": ("北斗神拳", "Fist of the North Star", 1984, "武论尊 · 原哲夫"),
    "slamdunk": ("灌篮高手", "Slam Dunk", 1993, "井上雄彦"),
    "conan": ("名侦探柯南", "Detective Conan", 1996, "青山刚昌"),
    "sailormoon": ("美少女战士", "Sailor Moon", 1992, "武内直子"),
    "kenshin": ("浪客剑心", "Rurouni Kenshin", 1996, "和月伸宏"),
    "hxh": ("全职猎人", "Hunter × Hunter (1999)", 1999, "富坚义博"),
    "digimon": ("数码宝贝大冒险", "Digimon Adventure", 1999, "本乡昭由（原案）"),
    "shinchan": ("蜡笔小新", "Crayon Shin-chan", 1992, "臼井仪人"),
    "onepiece": ("海贼王", "One Piece", 1999, "尾田荣一郎"),
    "tennis": ("网球王子", "The Prince of Tennis", 2001, "许斐刚"),
    "gintama": ("银魂", "Gintama", 2006, "空知英秋"),
    "naruto": ("火影忍者", "Naruto", 2002, "岸本齐史"),
    "bleach": ("死神", "Bleach", 2004, "久保带人"),
    "fairytail": ("妖精的尾巴", "Fairy Tail", 2009, "真岛浩"),
    "fatesn": ("Fate/stay night", "Fate/stay night", 2006, "TYPE-MOON"),
    "fma": ("钢之炼金术师", "Fullmetal Alchemist", 2003, "荒川弘"),
    "haikyuu": ("排球少年!!", "Haikyuu!!", 2014, "古馆春一"),
    "haruhi": ("凉宫春日的忧郁", "The Melancholy of Haruhi Suzumiya", 2006, "谷川流"),
    "chainsaw": ("电锯人", "Chainsaw Man", 2022, "藤本树"),
    "frieren": ("葬送的芙莉莲", "Frieren: Beyond Journey's End", 2023, "山田钟人 · 阿部司"),
    "clannad": ("CLANNAD", "CLANNAD", 2007, "Key"),
    "demon_slayer": ("鬼灭之刃", "Demon Slayer: Kimetsu no Yaiba", 2019, "吾峠呼世晴"),
    "jojo_sea": ("JOJO的奇妙冒险 石之海", "JoJo's Bizarre Adventure: Stone Ocean", 2021, "荒木飞吕彦"),
}
for c in r10["characters"]:
    if c["id"] not in chars:
        c = dict(c)
        meta = ANIME_META10.get(c.get("animeKey"))
        if meta and not c.get("animeZh"):
            c["animeZh"], c["animeEn"], c["year"], c["author"] = meta
        c.setdefault("source", "")
        if not c.get("source") and c.get("anilistCharId"):
            c["source"] = f"https://anilist.co/character/{c['anilistCharId']}"
        chars[c["id"]] = c

# ---- 文案修正层（混入英文词清理）----
TEXT_FIXUPS = [
    ("kenshiro", "feature", "点穴之后-count-的必杀连击。", "点穴之后的必杀连击。"),
    ("wataru", "intro", "每层山的boss战与「登龙剑」", "每层山的首领战与「登龙剑」"),
    ("kiteretsu", "intro", "撞上堀切和好子与 five代 醬的日常，靠祖传《奇天烈大百科》造出惊人的道具。藤子式邻家科幻的又一高峰。",
     "与布尔吉拉、乃乃子他们的欢乐日常，靠祖传《奇天烈大百科》造出惊人的道具。藤子式邻家科幻的又一高峰。"),
    ("ryoma", "feature", "白色的棒球帽与网球场上的「 jeszcze one more」?——不，是 F&D 的自信眼神。",
     "白色的棒球帽，与网球场上一击制胜的自信眼神。"),
    ("hijikata", "intro", "mayo 灵魂的鬼之副长", "美乃滋灵魂的鬼之副长"),
    ("kirito", "feature", "黑色的长剑与双刀流的 Entre Lines。", "黑色的长剑，与独步战场的二刀流。"),
    ("levi", "feature", "不到一米六的身影，与人类最强 Cleanup 的扫帚。", "不到一米六的身影，与人类最强士兵的扫帚。"),
    ("ai-hoshi", "feature", "偶像舞台上的星形瞳孔，与 scanner 般的谎言话术。",
     "偶像舞台上的星形瞳孔，与精准如扫描仪的谎言话术。"),
    ("violet", "feature", "braided 金发与胸前的绿宝石胸针，敲字的手指戴着手套。",
     "编起的金发与胸前的绿宝石胸针，敲字的手指戴着手套。"),    ("inosuke", "intro", "lider般的好胜心", "野猪般的好胜心"),
    ("inosuke", "intro", "。 野猪般", "。野猪般"),
    ("dio", "feature", "与石鬼面和 later 的时空超能力。", "与石鬼面和后来的替身超能力。"),
]
for _cid, _field, _old, _new in TEXT_FIXUPS:
    if _cid in chars and _old in chars[_cid].get(_field, ""):
        chars[_cid][_field] = chars[_cid][_field].replace(_old, _new)

ORDER = [
  "doraemon", "nobita", "amuro", "char", "arale", "lum", "tsubasa", "kenshiro", "goku", "seiya", "shiryu", "ryo", "kaori", "ranma", "vegeta", "astroboy", "maruko", "usagi", "yusuke", "hiei", "kurama", "shinchan", "hanamichi", "rukawa", "mitsui", "shinji", "rei", "asuka", "kenshin", "goseiba", "conan", "pikachu", "ash", "luffy", "agumon", "krillin", "piccolo", "bulma", "gohan", "trunks", "frieza", "hyoga", "ikki", "miyagi", "akagi", "sendoh", "kuwabara", "shizuka", "gian", "suneo", "rei-moon", "ami", "misato", "kaworu", "ran", "zoro", "nami", "misty", "meowth", "raoh", "akane", "ataru", "hiroshi", "kaoru-k", "minmay", "hikaru-m", "focker", "tatsuya", "minami", "lupin", "jigen", "fujiko", "kaneda", "nausicaa", "sheeta", "pazu", "totoro", "lunlun-c", "ikkyu-c", "nils", "kyosuke", "madoka", "ryo-st", "noa", "wataru", "lina", "gourry", "dboy", "ruri", "hikaru-mk", "sakura-cc", "kero", "kindaichi", "mao", "gon", "killua", "motoko", "guts", "vash", "spike", "faye", "hitomi", "tetsuro", "maetel", "oscar", "kyoko", "shurato", "roshi", "heero", "takumi", "onizuka", "meimi", "rantarou", "jotaro", "san", "kiki", "porco", "shizuku", "nadia", "sara", "reinhard", "yang", "van", "hitomie", "ryoko", "nike", "kukuri", "kinniku", "shun", "saori", "makoto", "minako", "kaito", "usopp", "sanji", "genkai", "brock", "blackjack", "parn", "deedlit", "harlock", "kiteretsu", "utena", "natsumi", "miyuki", "chirico", "leo", "inuyasha-c", "kagome", "yugi", "kaiba", "kira", "athrun", "naruto", "sasuke", "kakashi", "ichigo", "edward", "light", "l", "lelouch", "suzaku", "haruhi", "gintoki", "shana", "hikaru-go", "taiga", "natsu", "saber", "sebastian", "yui", "madoka-kaname", "homura", "eren", "levi", "mikasa", "kirito", "asuna", "saitama", "okabe", "kaneki", "deku", "bakugo", "rem", "hinata-vb", "gojo", "itadori", "anya", "denji", "bocchi", "frieren", "ai-hoshi", "tanjiro", "nezuko", "zenitsu", "ryoma", "yoh", "nagisa", "violet", "kaguya", "emma", "saga", "cell", "robin", "haibara", "kagura", "hijikata", "gaara", "rukia", "sesshomaru", "fushiguro", "armin", "todoroki", "retsu", "mu", "aldebaran", "deathmask", "aiolia", "shaka", "dohko", "milo", "aiolos", "shura", "aphrodite", "heiji", "shanks", "ace", "toguro", "renji", "erza", "misa", "itachi", "akira-toya", "sai", "kageyama", "jonathan", "dio", "inosuke", "giyu", "mr-satan", "chopper", "mihawk", "hisoka", "kuroro", "tomoyo", "fujima", "hinata", "jiraiya", "byakuya", "aizen", "kikyo", "naraku", "shinpachi", "takasugi", "mustang", "fuji-sd", "tezuka", "lacus", "jonouchi", "ryuk", "joseph", "kishibe", "oikawa", "erwin", "rengoku", "shinobu", "nobara", "sukuna", "buu", "bardock", "toki", "sawakita", "gin", "haruka", "saito-h", "kurapika", "taichi", "misae", "law", "hancock", "atobe", "katsura", "tsunade", "madara", "hitsugaya", "ulquiorra", "gray", "rin", "shiro", "alphonse", "tomoya", "nagato-y", "nishinoya", "akaza", "jolyne", "power", "fern",
]

dups = [x for x in set(ORDER) if ORDER.count(x) > 1]
assert not dups, "ORDER 重复: " + str(dups)
assert set(ORDER) == set(chars), "差异: " + str(set(ORDER) ^ set(chars))

out, missing_img = [], []
for cid in ORDER:
    c = dict(chars[cid])
    c["nameEn"] = NAME_DISPLAY.get(cid, c.get("nameEn") or "")
    if not c.get("source") and c.get("anilistCharId"):
        c["source"] = f"https://anilist.co/character/{c['anilistCharId']}"
    c.setdefault("source", "")
    if cid in DROP_QUOTES:
        c["quote"] = ""
    p = os.path.join(repo, c["image"])
    if not (os.path.exists(p) and os.path.getsize(p) > 3000):
        missing_img.append(cid)
    c.setdefault("animeZh", ""); c.setdefault("animeEn", ""); c.setdefault("source", "")
    out.append({k: c.get(k, "") for k in ("id","nameZh","nameJp","nameEn","hall","animeKey","animeZh","animeEn",
                                   "year","author","cv","feature","intro","quote","source","image")})

js = "/* 展品内容包数据 · 由策展管线生成，勿手改图片路径 */\nconst CHARACTERS = " + json.dumps(out, ensure_ascii=False, indent="  ") + ";\n"
open(f"{repo}/assets/characters.js", "w", encoding="utf-8").write(js)

halls = {}
animes = set()
quotes = 0
for c in out:
    halls[c["hall"]] = halls.get(c["hall"], 0) + 1
    animes.add(c["animeKey"])
    quotes += bool(c["quote"])
print(f"✓ characters.js: {len(out)} 件展品 | 展厅 {halls} | 作品 {len(animes)} 部 | 台词 {quotes} 条")
if missing_img:
    print("✗ 缺图:", missing_img)
else:
    print("✓ 全部图片在位")
