#!/usr/bin/env python3
# 80-90年代动漫人物博物馆 · 策展数据抓取（AniList GraphQL → 本地图片）
import json, os, subprocess, time

UA = ["-H", "User-Agent: MangaCharacterMuseum/0.1 (educational static exhibit; contact via github)"]
API = "https://graphql.anilist.co"
OUT = "/Users/radar/Downloads/gitlab127001/anime-character-museum/exhibits"
os.makedirs(OUT, exist_ok=True)

def gql(query, variables):
    payload = json.dumps({"query": query, "variables": variables})
    for attempt in range(6):
        r = subprocess.run(
            ["curl", "-s", "--max-time", "20", "-X", "POST", API,
             "-H", "Content-Type: application/json", *UA, "-d", payload],
            capture_output=True, text=True)
        try:
            d = json.loads(r.stdout)
        except Exception as e:
            print(f"  ! gql retry {attempt+1}: {e} / {r.stdout[:120]}", flush=True)
            time.sleep(3 + attempt * 3)
            continue
        if isinstance(d, dict) and d.get("errors"):
            wait = 12 + attempt * 12
            print(f"  ! gql errors, backoff {wait}s: {str(d['errors'])[:140]}", flush=True)
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

# ---------- 作品检索表 ----------
ANIME = {
    "doraemon":  dict(q="Doraemon",                    ymin=1978, ymax=1981, zh="哆啦A梦",        en="Doraemon (1979)"),
    "gundam":    dict(q="Kidou Senshi Gundam",         ymin=1978, ymax=1981, zh="机动战士高达",    en="Mobile Suit Gundam"),
    "astroboy":  dict(q="Tetsuwan Atom",               ymin=1980, ymax=1981, zh="铁臂阿童木",      en="Astro Boy (1980)"),
    "drslump":   dict(q="Dr. Slump",                   ymin=1980, ymax=1982, zh="阿拉蕾（IQ博士）", en="Dr. Slump"),
    "urusei":    dict(q="Urusei Yatsura",              ymin=1981, ymax=1982, zh="福星小子",        en="Urusei Yatsura"),
    "tsubasa":   dict(q="Captain Tsubasa",             ymin=1983, ymax=1984, zh="足球小将",        en="Captain Tsubasa"),
    "hokuto":    dict(q="Hokuto no Ken",               ymin=1984, ymax=1985, zh="北斗神拳",        en="Fist of the North Star"),
    "dragonball":dict(q="Dragon Ball",                 ymin=1986, ymax=1987, zh="龙珠",           en="Dragon Ball"),
    "seiya":     dict(q="Saint Seiya",                 ymin=1986, ymax=1987, zh="圣斗士星矢",      en="Saint Seiya"),
    "cityhunter":dict(q="City Hunter",                 ymin=1987, ymax=1988, zh="城市猎人",        en="City Hunter"),
    "astroboy2": None,
    "ranma":     dict(q="Ranma",                       ymin=1989, ymax=1990, zh="乱马½",          en="Ranma ½"),
    "dbz":       dict(q="Dragon Ball Z",               ymin=1989, ymax=1990, zh="龙珠Z",          en="Dragon Ball Z"),
    "maruko":    dict(q="Chibi Maruko-chan",           ymin=1989, ymax=1991, zh="樱桃小丸子",      en="Chibi Maruko-chan"),
    "sailormoon":dict(q="Bishoujo Senshi Sailor Moon", ymin=1992, ymax=1992, zh="美少女战士",      en="Sailor Moon"),
    "yyh":       dict(q="Yu Yu Hakusho",               ymin=1992, ymax=1992, zh="幽游白书",        en="Yu Yu Hakusho"),
    "shinchan":  dict(q="Crayon Shin-chan",            ymin=1992, ymax=1993, zh="蜡笔小新",        en="Crayon Shin-chan"),
    "slamdunk":  dict(q="Slam Dunk",                   ymin=1993, ymax=1994, zh="灌篮高手",        en="Slam Dunk"),
    "eva":       dict(q="Neon Genesis Evangelion",     ymin=1995, ymax=1996, zh="新世纪福音战士",  en="Neon Genesis Evangelion"),
    "kenshin":   dict(q="Rurouni Kenshin",             ymin=1996, ymax=1997, zh="浪客剑心",        en="Rurouni Kenshin"),
    "letsgo":    dict(q="Bakusou Kyoudai Let's & Go",  ymin=1996, ymax=1997, zh="四驱兄弟",        en="Let's & Go!!"),
    "conan":     dict(q="Detective Conan",             ymin=1996, ymax=1997, zh="名侦探柯南",      en="Detective Conan"),
    "pokemon":   dict(q="Pokemon",                     ymin=1997, ymax=1998, zh="宝可梦",          en="Pokémon"),
    "onepiece":  dict(q="One Piece",                   ymin=1999, ymax=2000, zh="海贼王",          en="One Piece"),
    "digimon":   dict(q="Digimon Adventure",           ymin=1999, ymax=2000, zh="数码宝贝大冒险",  en="Digimon Adventure"),
}
del ANIME["astroboy2"]

# ---------- 人物策展表 ----------
C = [
 # id, animeKey, hall, matchTokens, 中文名, 日文名, CV, 观察点, 讲解词, 台词(可空)
 ("doraemon","doraemon","80s",["doraemon"],"哆啦A梦","ドラえもん","大山羡代",
  "圆圆的蓝色身体、红鼻子，还有肚子上的四次元口袋。",
  "来自22世纪的猫型育儿机器人，为照看野比大雄留在了20世纪。四次元口袋里掏出的每一个秘密道具，都是几代人关于未来的想象力清单。","大雄——！"),
 ("nobita","doraemon","80s",["nobita"],"野比大雄","野比のび太","小原乃梨子",
  "圆圆的眼镜、怯生生的站姿，以及慢半拍的反射神经。",
  "学习和运动都不拿手的小学生，却在射击和翻花绳上是隐藏天才。平凡如他，也一样能走进了不起的冒险。",None),
 ("amuro","gundam","80s",["amuro"],"阿姆罗·雷","アムロ・レイ","古谷彻",
  "白色联邦军服与操作终端前专注的眼神。",
  "14岁便登上RX-78-2高达迎击吉恩军的天才少年。从害怕战斗的孩子成长为背负时代的王牌，机器人动画的「宿敌叙事」由他与红色彗星共同写就。","阿姆罗，出击啦！"),
 ("char","gundam","80s",["char aznable","aznable"],"夏亚·阿兹纳布尔","シャア・アズナブル","池田秀一",
  "红色专用机、制服与面具下的金发。",
  "吉恩公国的王牌，「红色彗星」以三倍速闻名战场。与阿姆罗贯穿一生的恩怨对决，是日本动画史上最著名的宿敌篇章。",None),
 ("arale","drslump","80s",["arale"],"阿拉蕾","則巻アラレ","小山茉美",
  "大大的圆眼镜、背上小小的翅膀，见面先来一句「呦」。",
  "则卷千兵卫博士造出来的少女型机器人，力大无穷却天真烂漫。企鹅村的日常因为她而鸡飞狗跳——鸟山明笔下最早的国民萌物。","呦——！"),
 ("lum","urusei","80s",["lum"],"拉姆","ラム","平野文",
  "虎纹比基尼、及腰的绿发，还有指尖跳动的小电击。",
  "鬼星来的外星少女，一场赌约之后成了诸星当的「未婚妻」。一句「达令~」伴随放电的拥抱，是80年代最热闹的青春闹剧符号。","达令~"),
 ("tsubasa","tsubasa","80s",["tsubasa ozora","ozora"],"大空翼","大空翼","日高法子",
  "永不服输的眼神，和腾空倒勾射门的身影。",
  "从街头少年一路踢向世界的前锋传奇。岬太郎的黄金搭档与 curve shoot 的轨迹，让无数孩子因此走上球场。","足球是我的朋友！"),
 ("kenshiro","hokuto","80s",["kenshiro"],"健次郎","ケンシロウ","神谷明",
  "胸前七道疤，点穴之后-count-的必杀连击。",
  "世纪末的救世主，北斗神拳第六十四代传人。在文明崩坏的荒野上以拳贯彻爱与悲伤——「你已经死了」，随后是爆裂的经穴。","你已经死了。"),
 ("goku","dragonball","80s",["son goku","goku"],"孙悟空","孫悟空","野泽雅子",
  "天真的笑容、尾巴，还有双手合十推出去的龟派气功。",
  "深山里长大的纯真少年，为寻找龙珠踏上冒险，最终成为守护宇宙的赛亚人战士。龟派气功与卡卡罗特，是一代人热血的原点。","龟·派·气·功——！"),
 ("seiya","seiya","80s",["seiya"],"星矢","星矢（セイヤ）","古谷彻",
  "天马座青铜圣衣与如流星般落下的拳影。",
  "为寻姐姐而战的天马座圣斗士，用燃烧的小宇宙守护雅典娜。天马流星拳划过之处，是少年热血突破极限的瞬间。","燃烧吧，我的小宇宙！"),
 ("shiryu","seiya","80s",["shiryu"],"紫龙","紫龍（シリュウ）","铃置洋孝",
  "天龙座圣衣与徒手劈开瀑布的修行姿态。",
  "庐山五老峰的天龙座圣斗士。为伙伴不惜献出视力的忠诚，让他在圣域诸黄金之间显得最沉静、也最滚烫。","庐山升龙霸！"),
 ("ryo","cityhunter","80s",["ryo saeba","saeba"],"冴羽獠","冴羽リョウ","神谷明",
  "绿色夹克与 Colt Python 左轮，背景是新宿的夜色。",
  "新宿的清道夫，在XYZ留言板接受委托的都市猎人。表面好色轻浮，出手却从无虚发——黑色幽默包裹的都市侠客。",None),
 ("kaori","cityhunter","80s",["kaori"],"槇村香","槇村香","伊仓一惠",
  "肩上扛着的百吨大锤，和脱口而出的怒吼。",
  "城市猎人的搭档与管理者，用百吨锤纠正阿獠的一切越轨。刀子嘴豆腐心，是新宿故事里最亮的那盏灯。","阿獠你这个大变态！"),
 ("ranma","ranma","80s",["ranma"],"早乙女乱马","早乙女乱馬","山口胜平",
  "乌黑的辫子；淋了冷水变少女，热水变回少年。",
  "天道道场的少年继承人，因掉进咒泉乡的「女溺泉」获得双重身份。格斗与婚约的爆笑日常，是高桥留美子喜剧的巅峰之作。",None),
 ("vegeta","dbz","80s",["vegeta"],"贝吉塔","ベジータ","堀川亮",
  "战斗服的肩甲，与永远高傲上扬的眉梢。",
  "贝吉塔行星的王子，以侵略者的姿态登场，却在与悟空一生的追逐中成为守护者。骄傲从未低头——王者的尊严即如此。","我是战斗民族最后的骄傲。"),
 ("astroboy","astroboy","80s",["astro boy","atom"],"阿童木","鉄腕アトム","清水玛丽",
  "尖尖的双马尾发型，脚底喷射的蓝色火焰。",
  "天马博士为纪念亡子制造的少年机器人，十万马力与正义之心。手冢治虫铸就的国民英雄，电视动画时代的起点在此回响。",None),
 ("maruko","maruko","90s",["maruko"],"樱桃小丸子","さくらももこ","TARAKO",
  "锯齿状的刘海、红白小帽，和「嘿嘿」的懒散笑。",
  "清水市小学三年级学生，讨厌功课、爱睡懒觉，与爷爷友藏一家过着鸡毛蒜皮又暖洋洋的日子。平成家庭剧场的治愈原点。",None),
 ("usagi","sailormoon","90s",["usagi"],"月野兔","月野うさぎ","三石琴乃",
  "头上一对月牙形发髻，变身后的水手服与额饰。",
  "爱哭贪吃的中学生，变身后是水手月亮。与伙伴们守护公主的宿命，让「美少女变身」成为一代女孩的魔法起点。","我要代表月亮消灭你们！"),
 ("yusuke","yyh","90s",["yusuke"],"浦饭幽助","浦飯幽助","佐佐木望",
  "墨绿的学兰制服，与指尖聚起灵气的灵丸手势。",
  "为救人而死的不良少年，经灵界测试重生为灵界侦探。从街头斗殴到暗黑武术会，富坚义博的热血与狡黠在他身上同时闪光。","灵丸！"),
 ("hiei","yyh","90s",["hiei"],"飞影","飛影","桧山修之",
  "竖起的黑发、颈间白巾，右臂上缠着封印邪眼的布带。",
  "冰河之村弃婴，妖界出身的刀客。毒舌孤高的背后藏着义气，一手「邪王炎杀黑龙波」烧穿战场。",None),
 ("kurama","yyh","90s",["kurama"],"藏马","蔵馬","绪方惠美",
  "垂腰的红色长发，指尖缠绕的玫瑰藤鞭。",
  "妖狐与人类少年的融合体，温柔笑容之下是妖狐的真身。玫瑰为鞭、植物为兵，灵界侦探团里最沉静的军师。",None),
 ("shinchan","shinchan","90s",["shinnosuke","nohara"],"野原新之助","野原しんのすけ","矢岛晶子",
  "粗粗的眉毛、圆圆的脑袋，还有那支尴尬的屁股舞。",
  "春日部五岁的幼儿园学生，早熟毒舌得让大人脸红。动感超人与美女姐姐，构成平成家庭最没节操也最真诚的喜剧。",None),
 ("hanamichi","slamdunk","90s",["hanamichi","sakuragi"],"樱木花道","桜木花道","草尾毅",
  "火红的短发，和写满「天才」两个字的自信。",
  "被五十次甩掉的篮球门外汉，为晴子的一个微笑加入湘北。超级新人的弹跳与不服输，让「我是天才」响彻神奈川。","因为我是天才！"),
 ("rukawa","slamdunk","90s",["rukawa"],"流川枫","流川楓","绿川光",
  "沉默的侧脸，与边打瞌睡边飙单车的杂技。",
  "湘北的王牌新人前锋，面无表情的得分机器。与樱木花道的水火不容，是这部作品最经典的欢喜冤家。",None),
 ("mitsui","slamdunk","90s",["mitsui"],"三井寿","三井寿","置鲇龙太郎",
  "不良时期的及肩长发，和跪在地板上的那双眼睛。",
  "曾经的MVP，迷失两年后带着一群不良回到体育馆。当他说出那句话，泪水的重量超过任何一记三分球。","教练，我想打篮球。"),
 ("shinji","eva","90s",["shinji"],"碇真嗣","碇シンジ","绪方惠美",
  "插在衣领里的手，与初号机驾驶舱的幽蓝液体。",
  "被父亲一通电话叫来的第三适格者。在使徒与人心之间，他怯懦、逃跑、又不得不战斗——「不能逃避」是他对自己的全部呐喊。","不能逃避，不能逃避……"),
 ("rei","eva","90s",["ayanami","rei ayanami"],"绫波丽","綾波レイ","林原惠美",
  "蓝色短发、红色瞳孔，与过分苍白的皮肤。",
  "神秘沉默的第一适格者，零号机驾驶员。淡漠表情下的存在之问，让「三无少女」自此成为动画史的固定类型。",None),
 ("asuka","eva","90s",["asuka"],"明日香","惣流・アスカ・ラングレー","宫村优子",
  "橙红色的长发，与标志性的傲娇口头禅。",
  "第二适格者，二号机驾驶员。骄傲与脆弱同时燃烧，用最强的音量宣告自己的存在。","你是个笨蛋吗？"),
 ("kenshin","kenshin","90s",["kenshin"],"绯村剑心","緋村剣心","凉风真世",
  "脸颊的十字伤疤，与永不杀人的逆刃刀。",
  "幕末人称「刽子手拔刀斋」，明治之后立誓不再杀人。十字伤疤与逆刃刀相伴流浪，守护乱世里微小的和平。","恶·即·斩。"),
 ("goseiba","letsgo","90s",["seiba"],"星马豪","星馬豪","池泽春菜",
  "冲锋战车的红白车身，与不等信号就冲刺的性子。",
  "四驱兄弟中的弟弟，Magnum 车系的创造者。与哥哥烈配合默契，掀起了席卷全国小学生的迷你四驱旋风。",None),
 ("conan","conan","90s",["conan"],"江户川柯南","江戸川コナン","高山南",
  "蓝色西装、领结变声器，和黑框眼镜后的锐利眼神。",
  "高中生侦探工藤新一被灌下神秘毒药后缩小的身体。个子变小，推理不减——「真相只有一个」回荡在每个案件的终点。","真相只有一个！"),
 ("pikachu","pokemon","90s",["pikachu"],"皮卡丘","ピカチュウ","大谷育江",
  "红色的脸颊，与闪电形状的尾巴。",
  "小智的第一位伙伴，电气属性的黄色宝可梦。十万伏特的电力加上「皮卡皮卡」的叫声，是世界第一IP的招牌面孔。","皮卡皮卡！"),
 ("ash","pokemon","90s",["ash ketchum","satoshi"],"小智","サトシ","松本梨香",
  "红白棒球帽，和永远背不腻的旅行背包。",
  "来自真新镇的十岁少年，目标是宝可梦大师。与皮卡丘从冤家到最佳搭档，二十多年的旅途教会我们：出发比抵达更重要。","我要成为宝可梦大师！"),
 ("luffy","onepiece","90s",["luffy"],"蒙奇·D·路飞","モンキー・D・ルフィ","田中真弓",
  "头上的草帽，与橡胶手臂甩出的灿烂大笑。",
  "误食橡胶果实的少年，为集结伙伴扬帆出海。香克斯的草帽戴在头上，「海贼王」的誓言改写了大航海时代的浪漫。","我是要成为海贼王的男人！"),
 ("agumon","digimon","90s",["agumon"],"亚古兽","アグモン","山口胜平",
  "橙色的恐龙身形，头顶三根标志性的爪角。",
  "八神太一的搭档，恐龙型数码宝贝。从幼年期一路进化到战斗暴龙兽的每一次光芒，都是1999年那个夏天的冒险记忆。","小型火焰！"),
]

AUTHOR = {
    "doraemon":"藤子·F·不二雄","gundam":"矢立肇 · 富野由悠季","astroboy":"手冢治虫","drslump":"鸟山明",
    "urusei":"高桥留美子","tsubasa":"高桥阳一","hokuto":"武论尊 · 原哲夫","dragonball":"鸟山明",
    "seiya":"车田正美","cityhunter":"北条司","ranma":"高桥留美子","dbz":"鸟山明",
    "maruko":"樱桃子","sailormoon":"武内直子","yyh":"富坚义博","shinchan":"臼井仪人",
    "slamdunk":"井上雄彦","eva":"庵野秀明（GAINAX）","kenshin":"和月伸宏","letsgo":"越田哲弘",
    "conan":"青山刚昌","pokemon":"田尻智（Game Freak）","onepiece":"尾田荣一郎","digimon":"本乡昭由（原案）",
}

# ---------- 抓取（media id 已由前序搜索解析，直接复用，省 24 个请求防限流）----------
SEARCH_Q = """
query ($s: String) { Page(perPage: 10) { media(search: $s, type: ANIME, sort: SEARCH_MATCH) {
  id title { romaji english } startDate { year } format } } }"""
CHARS_Q = """
query ($id: Int) { Media(id: $id, type: ANIME) { id
  characters(perPage: 50, sort: [RELEVANCE]) { edges { node {
    id name { full } image { large } } } } } }"""

MEDIA_IDS = {
    "doraemon": (2471, 1979), "gundam": (80, 1979), "astroboy": (3044, 1980),
    "drslump": (2222, 1981), "urusei": (1293, 1981), "tsubasa": (2116, 1983),
    "hokuto": (967, 1984), "dragonball": (223, 1986), "seiya": (1254, 1986),
    "cityhunter": (1470, 1987), "ranma": (210, 1989), "dbz": (813, 1989),
    "maruko": (951, 1990), "sailormoon": (530, 1992), "yyh": (392, 1992),
    "shinchan": (966, 1992), "slamdunk": (170, 1993), "eva": (30, 1995),
    "kenshin": (45, 1996), "letsgo": (2705, 1996), "conan": (235, 1996),
    "pokemon": (527, 1997), "onepiece": (21, 1999), "digimon": (552, 1999),
}

report = {"anime": {}, "characters": [], "missing": []}
media_ids = {}
for key, (mid, yr) in MEDIA_IDS.items():
    media_ids[key] = mid
    report["anime"][key] = {"anilistId": mid, "romaji": ANIME[key]["en"], "year": yr}
print(f"作品表就绪：{len(media_ids)} 部", flush=True)

# 再拉人物图
for c in C:
    cid, akey, hall, tokens, zh, jp, cv, feature, intro, quote = c
    if akey not in media_ids:
        report["missing"].append({"char": cid, "reason": "anime-unresolved"})
        continue
    node = None
    for round_no in range(4):  # 限流环境下逐人重试
        data = gql(CHARS_Q, {"id": media_ids[akey]})
        time.sleep(2.8)
        media = ((data or {}).get("data") or {}).get("Media") or {}
        edges = media.get("characters", {}).get("edges", [])
        if edges:
            for e in edges:
                full = (e["node"]["name"]["full"] or "").lower().replace("　", " ")
                if any(t in full for t in tokens):
                    node = e["node"]
                    break
            if node:
                break
        print(f"  ! {cid} 第{round_no+1}轮未取到列表（限流?），追加等待", flush=True)
        time.sleep(8 + round_no * 12)
    if not node:
        print(f"✗ {cid}: 人物未匹配 {tokens}")
        report["missing"].append({"char": cid, "reason": "char-not-found"})
        continue
    img_url = node["image"]["large"]
    img_path = f"{OUT}/{cid}.jpg"
    ok = fetch_img(img_url, img_path)
    meta = ANIME[akey]
    report["characters"].append({
        "id": cid, "anilistCharId": node["id"], "nameEn": node["name"]["full"],
        "nameZh": zh, "nameJp": jp, "cv": cv, "hall": hall,
        "animeKey": akey, "animeZh": meta["zh"], "animeEn": meta["en"],
        "year": report["anime"][akey]["year"], "author": AUTHOR[akey],
        "feature": feature, "intro": intro, "quote": quote or "",
        "source": f"https://anilist.co/character/{node['id']}",
        "image": f"exhibits/{cid}.jpg", "imageOk": ok,
    })
    print(f"{'✓' if ok else '✗'} {zh} ({node['name']['full']}) <- {img_url}")

json.dump(report, open("/tmp/museum_fetch_report.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
ok_n = sum(1 for c in report["characters"] if c["imageOk"])
print(f"\n=== 完成：{ok_n}/{len(C)} 人图片就绪；未解决：{len(report['missing'])} ===")
print(json.dumps(report["missing"], ensure_ascii=False))
