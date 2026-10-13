#!/usr/bin/env python3
# 第二批策展：+26 作品 +67 人物（复用 v1 的 gql 抓取方式）
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
CHARS_Q = """query ($id: Int) { Media(id: $id, type: ANIME) { id
  characters(perPage: 50, sort: [RELEVANCE]) { edges { node {
    id name { full } image { large } } } } } }"""

# ---------- 新作品检索表 ----------
NEW_ANIME = {
    "macross":   dict(q="Super Dimension Fortress Macross", ymin=1982, ymax=1983, zh="超时空要塞Macross", en="Macross"),
    "touch":     dict(q="Touch",                            ymin=1985, ymax=1986, zh="棒球英豪",         en="Touch"),
    "lupin":     dict(q="Lupin III",                        ymin=1977, ymax=1978, zh="鲁邦三世(第二部)", en="Lupin III: Part II"),
    "akira":     dict(q="AKIRA",                            ymin=1988, ymax=1988, zh="阿基拉",           en="AKIRA"),
    "nausicaa":  dict(q="Nausicaa of the Valley of the Wind", ymin=1984, ymax=1984, zh="风之谷",         en="Nausicaä of the Valley of the Wind"),
    "laputa":    dict(q="Castle in the Sky",                ymin=1986, ymax=1986, zh="天空之城",         en="Castle in the Sky"),
    "totoro":    dict(q="My Neighbor Totoro",               ymin=1988, ymax=1988, zh="龙猫",            en="My Neighbor Totoro"),
    "lunlun":    dict(q="Hana no Ko Lunlun",                ymin=1980, ymax=1981, zh="花仙子",           en="Hana no Ko Lunlun"),
    "ikkyu":     dict(q="Ikkyu-san",                        ymin=1975, ymax=1980, zh="聪明的一休",        en="Ikkyū-san"),
    "niels":     dict(q="Nils no Fushigi na Tabi",          ymin=1980, ymax=1981, zh="尼尔斯骑鹅旅行记",  en="The Wonderful Adventures of Nils"),
    "oroad":     dict(q="Kimagure Orange Road",             ymin=1987, ymax=1988, zh="橙路",            en="Kimagure Orange Road"),
    "troopers":  dict(q="Yoroiden Samurai Troopers",        ymin=1988, ymax=1989, zh="魔神坛斗士",        en="Ronin Warriors"),
    "patlabor":  dict(q="Kidou Keisatsu Patlabor",          ymin=1989, ymax=1990, zh="机动警察",         en="Patlabor: The TV Series"),
    "wataru":    dict(q="Mashin Hero Wataru",               ymin=1988, ymax=1989, zh="魔神英雄传",        en="Mashin Hero Wataru"),
    "slayers":   dict(q="Slayers",                          ymin=1995, ymax=1995, zh="秀逗魔导士",        en="Slayers"),
    "tekkaman":  dict(q="Tekkaman Blade",                   ymin=1992, ymax=1992, zh="宇宙骑士",         en="Tekkaman Blade"),
    "nadesico":  dict(q="Martian Successor Nadesico",       ymin=1996, ymax=1997, zh="机动战舰",         en="Martian Successor Nadesico"),
    "rayearth":  dict(q="Magic Knight Rayearth",            ymin=1994, ymax=1994, zh="魔法骑士",         en="Magic Knight Rayearth"),
    "ccsakura":  dict(q="Cardcaptor Sakura",                ymin=1998, ymax=1998, zh="魔卡少女樱",        en="Cardcaptor Sakura"),
    "kindaichi": dict(q="Kindaichi Shounen no Jikenbo",     ymin=1997, ymax=1998, zh="金田一少年事件簿",  en="The Kindaichi Case Files"),
    "chuka":     dict(q="Chuuka Ichiban",                   ymin=1997, ymax=1998, zh="中华一番",         en="Cooking Master Boy"),
    "hxh":       dict(q="Hunter x Hunter",                  ymin=1999, ymax=1999, zh="全职猎人",         en="Hunter × Hunter (1999)"),
    "ghostshell":dict(q="Ghost in the Shell",               ymin=1995, ymax=1995, zh="攻壳机动队",        en="Ghost in the Shell"),
    "berserk":   dict(q="Berserk",                          ymin=1997, ymax=1998, zh="剑风传奇",         en="Berserk (1997)"),
    "trigun":    dict(q="Trigun",                           ymin=1998, ymax=1998, zh="枪神",            en="Trigun"),
    "bebop":     dict(q="Cowboy Bebop",                     ymin=1998, ymax=1999, zh="星际牛仔",         en="Cowboy Bebop"),
}

# 已知作品的 media id（第一批）
KNOWN = {"doraemon":2471,"gundam":80,"astroboy":3044,"drslump":2222,"urusei":1293,"tsubasa":2116,
         "hokuto":967,"dragonball":223,"seiya":1254,"cityhunter":1470,"ranma":210,"dbz":813,
         "maruko":951,"sailormoon":530,"yyh":392,"shinchan":966,"slamdunk":170,"eva":30,
         "kenshin":45,"letsgo":2705,"conan":235,"pokemon":527,"onepiece":21,"digimon":552}

NEW_AUTHOR = {
    "macross":"河森正治（Studio Nue）","touch":"安达充","lupin":"加藤一彦","akira":"大友克洋",
    "nausicaa":"宫崎骏","laputa":"宫崎骏（吉卜力）","totoro":"宫崎骏（吉卜力）","lunlun":"神保史郎（东映）",
    "ikkyu":"","niels":"塞尔玛·拉格洛夫（原作）","oroad":"松本泉","troopers":"矢立肇（SUNRISE）",
    "patlabor":"结城正美（HEADGEAR）","wataru":"矢立肇（SUNRISE）","slayers":"神坂一","tekkaman":"龙之子制作",
    "nadesico":"麻宫骑亚","rayearth":"CLAMP","ccsakura":"CLAMP","kindaichi":"天树征丸 · 佐藤文也",
    "chuka":"小川悦司","hxh":"富坚义博","ghostshell":"士郎正宗","berserk":"三浦建太郎",
    "trigun":"内藤泰弘","bebop":"渡边信一郎（SUNRISE）",
}

C2 = [
 # ---- 既有作品加人 ----
 ("krillin","dragonball","80s",["krillin"],"克林","クリリン","中尾隆圣",
  "没有鼻子的圆脸，和额头的六颗点。",
  "悟空最好的伙伴，地球人出身的最强战士之一。没有赛亚人的血统，却一次次站在最强的敌人面前。",""),
 ("piccolo","dragonball","80s",["piccolo"],"比克","ピッコロ","古川登志夫",
  "绿色的皮肤、触角，和肩上飘着的白色披风。",
  "从大魔王到悟空最可靠的战友，那美克星人的沉默守护者。与悟饭的师徒情，是龙珠里最温柔的转折。",""),
 ("bulma","dragonball","80s",["bulma"],"布尔玛","ブルマ","鹤弘美",
  "蓝色的头发，和永不离手的龙珠雷达。",
  "万能天才少女，胶囊公司的千金。整个龙珠宇宙的冒险，都是从她骑着自行车寻找龙珠开始的。",""),
 ("gohan","dbz","80s",["gohan"],"孙悟饭","孫悟飯","野泽雅子",
  "头顶一根呆毛，爆发时双眼金光。",
  "悟空的长子，藏在书堆里的学者梦与毁天灭地的潜力。面对沙鲁的那一击，是全宇宙最温柔的愤怒。",""),
 ("trunks","dbz","80s",["trunks"],"特兰克斯","トランクス","草尾毅",
  "淡紫色的短发，和背上的勇者之剑。",
  "从毁灭的未来逆流而来的少年，独自一人向命运挥剑。他的出现，让「绝望」第一次有了退路。",""),
 ("frieza","dbz","80s",["frieza","freeza"],"弗利萨","フリーザ","中尾隆圣",
  "雪白的躯体、紫色的甲纹，和优雅的漂浮姿态。",
  "宇宙帝王的优雅与残忍并存，那美克星之战的最终黑暗。他的存在定义了「绝望的强度」。",""),
 ("hyoga","seiya","80s",["hyouga","hyoga"],"冰河","氷河（ヒョウガ）","池田秀一",
  "白金色的头发，与天鹅座圣衣的冰晶羽翼。",
  "东西伯利亚冻土上的白鸟，天鹅座圣斗士。为师父与母亲，把冰之拳练成了最悲伤的温柔。","曙光女神之宽恕！"),
 ("ikki","seiya","80s",["ikki"],"一辉","一輝（イッキ）","玄田哲章",
  "狂野的发型，与凤凰座圣衣的不死火焰。",
  "凤凰座的孤独战士，在死亡岛修成的不死之身。最恨的弟弟瞬，也是他唯一柔软的地方。","凤翼天翔！"),
 ("miyagi","slamdunk","90s",["miyagi"],"宫城良田","宮城リョータ","",
  "矮小却飞快的身影，与不服输的坏笑。",
  "湘北的闪电控卫，用速度弥补身高的差距。安静时是天才，暴走时是问题儿童。",""),
 ("akagi","slamdunk","90s",["akagi"],"赤木刚宪","赤木剛憲","梁田清之",
  "高大的身板，与篮下霸气的低吼。",
  "湘北的队长与精神支柱，「大猩猩」的绰号下是最滚烫的冠军梦。",""),
 ("sendoh","slamdunk","90s",["sendoh"],"仙道彰","仙道彰","岛田敏",
  "额前垂下的一缕发，与懒洋洋的笑容。",
  "陵南的王牌，神奈川最全面的天才。与流川枫、樱木的对位，是全作最华丽的锋线对决。",""),
 ("kuwabara","yyh","90s",["kuwabara"],"桑原和真","桑原和真","千叶繁",
  "梳得高高的发油头，与凝聚在拳上的灵气之剑。",
  "幽助的损友兼死党，灵力第二高的「人类」，「打架要走正门」是他的美学，「义气」是他的必杀技。","灵剑！"),
 ("shizuka","doraemon","80s",["shizuka"],"源静香","源静香","野村道子",
  "黑长直的发带，和小提琴……的杀伤力。",
  "大雄未来的新娘，温柔聪慧的大小姐。洗澡被闯入是她的世纪噩梦，「静香」是一代人的白月光。",""),
 ("gian","doraemon","80s",["gian","takeshi goda"],"刚田武（胖虎）","剛田武（ジャイアン）","立壁和也",
  "壮硕的身板，与永远跑调的演唱会。",
  "孩子的孩子王，用拳头与「演唱会」统治空地。粗鲁的外表下，是最讲义气的邻居大哥。","你的东西就是我的东西。"),
 ("suneo","doraemon","80s",["suneo"],"骨川小夫","骨川スネ夫","肝付兼太",
  "尖尖的嘴巴，与炫耀不完的新玩具。",
  "富家少爷与大雄的「损友」，毒舌又爱炫耀。关键时刻，他永远是那个嘴硬心软的同伴。",""),
 ("rei-moon","sailormoon","90s",["rei hino","hino"],"火野丽","火野レイ","富泽美智惠",
  "乌黑的长发，与神社巫女的红色巫女服。",
  "火川神社的巫女少女，水手火星。毒舌急性子，却是最早与小兔并肩作战的伙伴。",""),
 ("ami","sailormoon","90s",["ami mizuno","mizuno"],"水野亚美","水野アミ","久川绫",
  "蓝色的短发，与不离手的书本和超级电脑。",
  "水手水星，IQ 300 的天才少女。安静腼腆的外表下，藏着全队最清醒的头脑。",""),
 ("misato","eva","90s",["misato"],"葛城美里","葛城ミサト","三石琴乃",
  "耳边的十字架，与罐装啤酒的生活气息。",
  "NERV 作战部长，EVA 战线的实际指挥官。白天是雷厉风行的军人，回家后是抱着啤酒瘫倒的大姐姐。",""),
 ("kaworu","eva","90s",["kaworu"],"渚薰","渚カヲル","石田彰",
  "银灰色的头发，与恰到好处的温柔微笑。",
  "第五适格者，自由之天使。他用一首钢琴曲与一句「我喜欢你」，成为真嗣命运里最短暂的救赎。",""),
 ("ran","conan","90s",["ran mouri","mouri ran","ran mori"],"毛利兰","毛利蘭","山崎和佳奈",
  "清秀的侧脸，与空手道冠军的铁拳。",
  "等待新一归来的空手道少女。她的每一次回头，都是这部推理剧最柔软的悬念。",""),
 ("shinichi","conan","90s",["shinichi"],"工藤新一","工藤新一","山口胜平",
  "校服下的侦探气质，与福尔摩斯式的自信。",
  "让案件无所遁形的高中生侦探。被灌下毒药之前，他是平成年间最耀眼的「平成福尔摩斯」。","我是高中生侦探工藤新一！"),
 ("zoro","onepiece","90s",["zoro","zolo"],"罗罗诺亚·索隆","ロロノア・ゾロ","中井和哉",
  "绿色的短发，与腰间三把刀的独特拔刀姿势。",
  "草帽团的剑士，「三刀流」的开创者。为与挚友的约定，他把「世界第一剑豪」刻进了航海的每一步。","背上的伤是剑士的耻辱！"),
 ("nami","onepiece","90s",["nami"],"娜美","ナミ","冈村明美",
  "橙色的短发，与画满航线的海图。",
  "草帽团的航海士，能用身体感知天气的天才。为买回村子自由而忍辱的八年，是海贼王最催泪的伏笔。",""),
 ("misty","pokemon","90s",["misty","kasumi"],"小霞","カスミ","饭冢雅弓",
  "侧扎的马尾，与腰间的六颗精灵球。",
  "华蓝市的 Gym 馆主少女，水属性专家。从抢走小智自行车的暴躁同伴，到无可替代的旅伴。",""),
 ("meowth","pokemon","90s",["meowth","nyarth"],"喵喵","ニャース","犬山犬子",
  "头顶的金币印记，与直立行走的猫爪。",
  "火箭队里会说话的宝可梦，为爱学会人语。反派三人组的最强话术担当，也是最让人心疼的打工猫。",""),
 ("raoh","hokuto","80s",["raoh","raou"],"拉欧","ラオウ","内海贤二",
  "魁梧的黑色铠甲，与直冲天际的斗气。",
  "健次郎的义兄，北斗神拳的修罗之王。他要的不是杀戮，而是把世纪末的天命扛在自己肩上。","我的一生，没有一丝后悔。"),
 ("akane","ranma","80s",["akane"],"天道茜","天道あかね","日高法子",
  "利落的短发，与练就空手道的少女身手。",
  "天道道场的继承人，乱马的「未婚妻」。嘴上嫌他烦，心里比谁都先站出来护他。",""),
 ("ataru","urusei","80s",["ataru"],"诸星当","諸星あたる","古川登志夫",
  "虎纹学兰，与见到美女就走不动路的贱样。",
  "地球的「代表」，靠运气赢下拉姆的捉迷藏。好色又命硬的平凡少年，是这部宇宙级闹剧的核心。",""),
 ("hiroshi","shinchan","90s",["hiroshi"],"野原广志","野原ひろし","藤原启治",
  "西装公文包，与臭袜子的杀伤力。",
  "双叶商事的上班族，双月薪房贷三十二年的普通父亲。小新的喜剧里，最真实的大人视角。",""),
 ("kaoru-k","kenshin","90s",["kaoru"],"神谷薰","神谷薫","",
  "束起的马尾，与竹刀道场继承人的飒爽。",
  "神谷活心流道场的主人，收留流浪剑心的少女。她相信「活心流」是用来守护人的剑。",""),
 # ---- 新作品 ----
 ("minmay","macross","80s",["minmay"],"林明美","リン・ミンメイ","饭岛真理",
  "乌黑的长发，与舞台上闪亮的偶像裙摆。",
  "从中华料理店女孩到宇宙偶像，一首《爱·おぼえていますか》让敌我双方同时放下了武器。",""),
 ("hikaru-m","macross","80s",["hikaru ichijou","hikaru ichijo","ichijou","ichijo"],"一条辉","一条輝","长谷有洋",
  "统合军的飞行员制服，与 VF 战机座舱里的专注侧脸。",
  "从杂技演员到统合军王牌，在明美与早濑未沙之间成长。第一次宇宙大战的王牌飞行员。",""),
 ("focker","macross","80s",["roy focker","focker"],"罗伊·福克","ロイ・フォッカー","神谷明",
  "骷髅中队徽章，与机身上涂满战功的白色 VF-1S。",
  "一条辉的师父，骷髅战机的传奇队长。他的陨落教会了后辈：王牌的天空也有尽头。",""),
 ("tatsuya","touch","80s",["tatsuya"],"上杉达也","上杉達也","",
  "慵懒的笑眼，与投手丘上认真起来的侧脸。",
  "双胞胎里的弟弟，天赋藏在不羁的外表之下。为了「带南去甲子园」的约定，他终于推开了那扇门。",""),
 ("minami","touch","80s",["minami"],"浅仓南","浅倉南","日高法子",
  "体操服与运动员的利落身姿，笑起来有浅浅的酒窝。",
  "校园里的女神，体操部的王牌。在达也与和也之间的青春心事，是安达充最干净的笔触。",""),
 ("lupin","lupin","80s",["lupin"],"鲁邦三世","ルパン三世","山田康雄",
  "红色西装，与偷不走他笑容的越狱身手。",
  "怪盗世家第三代，世界大盗的孙子。偷画的更偷心，身边永远是追不完的钱形警部。",""),
 ("jigen","lupin","80s",["jigen"],"次元大介","次元大介","小林清志",
  "压低的帽檐，与叼在嘴角的香烟。",
  "拔枪快过影子的高手，鲁邦最铁的搭档。帽子下的脸从没看全过，枪法却从没让人失望过。",""),
 ("fujiko","lupin","80s",["fujiko"],"峰不二子","峰不二子","增山江威子",
  "红发与剪影般的身段，永远猜不透的立场。",
  "谜一样的女盗，今天帮鲁邦明天卖鲁邦。她是全员追逐的谜题，也是这部作品最潇洒的变量。",""),
 ("kaneda","akira","80s",["kaneda"],"金田","金田正太郎","岩田光央",
  "红色的外套，与那辆永远有人想要的红摩托。",
  "暴走族「金田团」的老大，为了找回朋友铁雄冲进新东京的黑暗。Akira 的红色旋风，重新定义了赛博朋克。",""),
 ("nausicaa","nausicaa","80s",["nausicaa","nausica"],"娜乌西卡","ナウシカ","岛本须美",
  "蓝色的旧战斗服，与驭风滑翔的身影。",
  "风之谷的公主，腐海真相的追寻者。她用温柔接住疯狂的世界——宫崎骏笔下最初的蓝衣圣女。",""),
 ("sheeta","laputa","80s",["sheeta"],"希达","シータ","横泽启子",
  "垂到腰间的双辫，与胸前发光的飞行石。",
  "拉普达王室的末裔，温柔却敢于纵身一跃。她念出的毁灭咒文，是对「文明」最沉痛的提醒。",""),
 ("pazu","laputa","80s",["pazu"],"巴斯","パズー","田中真弓",
  "矿工服与护目镜，和小镇屋顶上的喊声。",
  "矿镇孤儿少年，为证明天空之城存在而拼命。那句「从天上落下来的女孩子」，是动画史最浪漫的开场。",""),
 ("totoro","totoro","80s",["totoro"],"龙猫","トトロ","高木均",
  "灰色的巨大绒毛，头顶的树叶与树洞里的呼噜。",
  "住在樟树里的森林精灵，只有孩子能看见。一把伞、一袋橡果——它成了吉卜力之后所有温柔的起点。",""),
 ("lunlun-c","lunlun","80s",["lunlun"],"小蓓","ルンルン","冈本茉莉",
  "黄色的帽子，与随行的会说话小狗小猫。",
  "寻找七色花的旅行少女，一路走过欧洲的风光。华语世界的第一批「少女番」记忆。",""),
 ("ikkyu-c","ikkyu","80s",["ikkyu","ikkyuu"],"一休","一休さん","藤田淑子",
  "光光的脑袋上五个手指印，与盘腿打坐的身影。",
  "小和尚一休的机智日常，每集都在「休息，休息一下」里化险为夷。华语世界的启蒙级动画记忆。","休息，休息一下~"),
 ("nils","niels","80s",["nils"],"尼尔斯","ニルス","",
  "小小的人影，与家鹅马丁背上的天空之旅。",
  "被小精灵变成拇指大的顽童，骑着家鹅走遍瑞典。世界名著改编的勇气与地理启蒙。",""),
 ("kyosuke","oroad","80s",["kyousuke","kyosuke"],"春日恭介","春日恭介","古谷彻",
  "从自行车后座飘起的白帽，与「跳跃」时的红光。",
  "拥有超能力的转学生，在恭介、圆与薰的三角里笨拙成长。昭和末年最青涩的恋爱循环。",""),
 ("madoka","oroad","80s",["madoka"],"鲇川圆","鮎川まどか","鹤弘美",
  "垂腰的长发，与打起架来全都不含糊的眼神。",
  "「圆」一样的少女——美到发光，飙车打架样样行。喇叭裙与打火机的传说，是平成青春的符号。",""),
 ("ryo-st","troopers","80s",["ryo sanada","sanada"],"真田辽","真田遼","草尾毅",
  "黑发红铠，与烈火之铠点燃的炽焰。",
  "烈火的辽，五大武士之首。以仁义之心驾驭铠甲，为地球而战的昭和热血收尾之作。",""),
 ("noa","patlabor","80s",["noa izumi","izumi noa","izumi"],"泉野明","泉野明","富泽美智惠",
  "英格拉姆驾驶舱里的笑，与机库里的暴走日常。",
  "特车二课第一小队的先锋，英格拉姆一号机驾驶员。把警用机器人开出了生活剧的温度。",""),
 ("wataru","wataru","80s",["wataru"],"战部渡（瓦塔诺）","戦部ワタル","田中真弓",
  "背着登龙剑的小小身影，与白龙丸的鳞光。",
  "创界山的救世主，小学四年级的勇者。每层山的boss战与「登龙剑」，是机甲勇者番的起点。",""),
 ("lina","slayers","90s",["lina inverse","lina"],"莉娜·因巴斯","リナ・インバース","林原惠美",
  "娇小的身板，与吟唱咒文时夸张的手势。",
  "「龙破斩」的天才魔剑士，暴力与财迷兼得的少女。她一开口念咒，城镇就要做好重建的准备。","龙破斩！"),
 ("gourry","slayers","90s",["gourry"],"高里·加布列夫","ガウリイ","松本保典",
  "金色长发，与背上比人还长的光之剑。",
  "护送莉娜的剑士保镖，脑子偶尔迟到，剑法从不迟到。光之剑的真正身份，是全篇最大的温柔伏笔。",""),
 ("dboy","tekkaman","90s",["tekkaman blade","d-boy","takaya"],"D-Boy（相羽高野）","相羽高野","森川智之",
  "结晶化的绿白铠甲，与射出的 Voltekka 光束。",
  "从坠落森林醒来的失忆少年，对抗拉达姆的宇宙骑士。每变身一次，就离遗忘家人近一步。",""),
 ("ruri","nadesico","90s",["ruri"],"星野琉璃","星野ルリ","南央美",
  "齐刘海与两侧的长发，冷淡的电子音调。",
  "抚子号的天才少年 Operator，吐槽担当。一句「真是一群笨蛋」，是 90 年代御宅文化的传世梗。","真是一群笨蛋。"),
 ("hikaru-mk","rayearth","90s",["hikaru shidou","shidou"],"狮堂光","獅堂光","",
  "红色的铠甲机神，与炎之神雷克斯的咆哮。",
  "从东京塔被召唤到锡菲罗的初中生，火属性魔神雷克斯的驾驶员。CLAMP 的奇幻起点。",""),
 ("sakura-cc","ccsakura","90s",["sakura kinomoto","kinomoto"],"木之本樱","木之本桜","丹下樱",
  "带翅膀的小帽子，与封印之杖划出的魔法阵。",
  "意外打开库洛牌书册的小学生，一张张收回牌的魔法日常。她定义了「萌系魔法少女」的黄金模板。",""),
 ("kero","ccsakura","90s",["kero","kerberos"],"可鲁贝洛斯（小可）","ケルベロス","久川绫",
  "黄色的圆翅膀，和永远叼着的甜点。",
  "库洛牌的守护兽，封印期间退化成吃点小甜食的毛绒玩具。嘴上嫌弃小樱，关键时刻最拼命。",""),
 ("kindaichi","kindaichi","90s",["kindaichi"],"金田一一","金田一一","松野太纪",
  "松垮的校服领带，与推演案情时锐利的眼神。",
  "名侦探金田一耕助的孙子，IQ 180 的吊车尾高中生。每桩密室诡计，都在他「以爷爷的名义」下瓦解。","我以爷爷的名义发誓！"),
 ("mao","chuka","90s",["mao xing","maoxing","liu maoxing","mao"],"刘昴星","劉昴星（リュウ・マオシン）","田中真弓",
  "白色的厨师服，与端出锅的闪耀料理。",
  "史上最年轻的特级厨师候选人，菊下楼的天才少年。他的每一道菜，都在发光——字面意义上的发光。",""),
 ("gon","hxh","90s",["gon freecss","freecss","gon"],"小杰·富力士","ゴン=フリークス","竹内顺子",
  "绿色的渔夫装，与钓竿划出的弧线。",
  "为寻找父亲踏上猎人试炼的少年，直觉与野性是他的天赋。富坚笔下的纯粹，自他开始。",""),
 ("killua","hxh","90s",["killua"],"奇犽·揍敌客","キルア=ゾルディック","三桥加奈子",
  "银白色的头发，与指尖变出的悠悠球。",
  "暗杀世家的继承人，与小杰一见如故的天才。从杀手到朋友，他学会了「想要什么」这件事。",""),
 ("motoko","ghostshell","90s",["motoko","kusanagi"],"草薙素子","草薙素子","田中敦子",
  "义体躯壳下水中的蓝色潜影。",
  "公安九课的少校，全身义体的攻壳特工。「魂壳」之间她追问的那个问题，启发了后来的整个赛博世界。",""),
 ("guts","berserk","90s",["guts"],"格斯","ガッツ","神奈延年",
  "比人还大的斩龙剑，与右眼的旧伤。",
  "佣兵团的独行剑士，背着巨剑迎向宿命。黄金时代篇的友情与背叛，是90年代最沉重的黑暗史诗。",""),
 ("vash","trigun","90s",["vash"],"法修·史丹比特","ヴァッシュ","小野坂昌也",
  "红色的风衣，与竖起的金色刺猬头。",
  "悬赏六百亿的「人间台风」，却坚持不杀一人。荒漠星球的西部剧里，最温柔的和平主义者。","Love & Peace!"),
 ("spike","bebop","90s",["spike"],"斯派克·斯皮格尔","スパイク","山寺宏一",
  "西装领带下的散漫，与柔术般凌厉的拳脚。",
  "BEBOP 号的赏金猎人，黑白通吃的浪子。他把过去留在火星，把爵士乐过成了人生。",""),
 ("faye","bebop","90s",["faye"],"菲·瓦伦坦","フェイ","林原惠美",
  "紫红的短发，与赌桌前的小动作。",
  "欠下一屁股债的冷艳女骗子，真实身份被封存在五十四年的冷冻里。BEBOP 号最锋利也最柔软的人。",""),
]

media_ids2 = {}
report2 = {"anime": {}, "characters": [], "missing": []}

for key, meta in NEW_ANIME.items():
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
        media_ids2[key] = picked["id"]
        print(f"✓ {key}: {picked['title']['romaji']} ({picked['startDate']['year']}, {picked['format']}) -> {picked['id']}", flush=True)
        report2["anime"][key] = {"anilistId": picked["id"], "romaji": picked["title"]["romaji"], "year": picked["startDate"]["year"]}
    else:
        print(f"✗ {key}: 未命中 [{meta['ymin']},{meta['ymax']}]", flush=True)
        report2["missing"].append({"anime": key, "reason": "media-not-found"})

ALL_IDS = {**KNOWN, **media_ids2}

for c in C2:
    cid, akey, hall, tokens, zh, jp, cv, feature, intro, quote = c
    img_path = f"{OUT}/{cid}.jpg"
    if os.path.exists(img_path) and os.path.getsize(img_path) > 3000:
        print(f"= {cid}: 已存在，跳过下载", flush=True)
        ok = True
        node = None
    else:
        if akey not in ALL_IDS:
            report2["missing"].append({"char": cid, "reason": "anime-unresolved"})
            continue
        node = None
        for rnd in range(3):
            data = gql(CHARS_Q, {"id": ALL_IDS[akey]})
            time.sleep(3.0)
            media = ((data or {}).get("data") or {}).get("Media") or {}
            edges = media.get("characters", {}).get("edges", [])
            if edges:
                for e in edges:
                    full = (e["node"]["name"]["full"] or "").lower()
                    if any(t in full for t in tokens):
                        node = e["node"]
                        break
                if node:
                    break
            print(f"  ! {cid} 第{rnd+1}轮未取到列表", flush=True)
            time.sleep(10 + rnd * 10)
        if not node:
            print(f"✗ {cid}: 人物未匹配 {tokens}", flush=True)
            report2["missing"].append({"char": cid, "reason": "char-not-found"})
            continue
        ok = fetch_img(node["image"]["large"], img_path)
    report2["characters"].append({
        "id": cid, "anilistCharId": (node or {}).get("id"),
        "nameEn": (node or {}).get("name", {}).get("full", ""),
        "nameZh": zh, "nameJp": jp, "cv": cv, "hall": hall,
        "animeKey": akey,
        "animeZh": (NEW_ANIME.get(akey) or {}).get("zh", ""),
        "animeEn": (NEW_ANIME.get(akey) or {}).get("en", ""),
        "year": report2.get("anime", {}).get(akey, {}).get("year"),
        "author": NEW_AUTHOR.get(akey, ""),
        "feature": feature, "intro": intro, "quote": quote or "",
        "source": f"https://anilist.co/character/{(node or {}).get('id')}" if node else "",
        "image": f"exhibits/{cid}.jpg", "imageOk": ok,
    })
    print(f"{'✓' if ok else '✗'} {zh}", flush=True)

json.dump(report2, open("/tmp/museum_fetch2_report.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
ok_n = sum(1 for c in report2["characters"] if c["imageOk"])
print(f"\n=== 第二批完成：{ok_n}/{len(C2)}；未解决：{len(report2['missing'])} ===", flush=True)
print(json.dumps(report2["missing"], ensure_ascii=False))
