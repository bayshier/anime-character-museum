#!/usr/bin/env python3
# 主题曲抓取：AnimeThemes API → 每部作品取 OP1（+ED1）
import json, subprocess, time

API = "https://api.animethemes.moe/anime"
THEMES_Q = ("https://api.animethemes.moe/anime?filter%5Bname%5D={q}"
            "&include=animethemes.animethemeentries.videos,animethemes.song"
            "&page%5Bsize%5D=8")

# animeKey -> AnimeThemes 检索名
ANIME_NAMES = {
    "doraemon":"Doraemon","gundam":"Mobile Suit Gundam","astroboy":"Astro Boy","drslump":"Dr. Slump",
    "urusei":"Urusei Yatsura","tsubasa":"Captain Tsubasa","hokuto":"Fist of the North Star",
    "dragonball":"Dragon Ball","seiya":"Saint Seiya","cityhunter":"City Hunter","ranma":"Ranma",
    "dbz":"Dragon Ball Z","maruko":"Chibi Maruko-chan","sailormoon":"Sailor Moon","yyh":"Yu Yu Hakusho",
    "shinchan":"Crayon Shin-chan","slamdunk":"Slam Dunk","eva":"Neon Genesis Evangelion",
    "kenshin":"Rurouni Kenshin","letsgo":"Bakusou Kyoudai Let's & Go","conan":"Detective Conan",
    "pokemon":"Pokemon","onepiece":"One Piece","digimon":"Digimon Adventure",
    "macross":"Macross","touch":"Touch","lupin":"Lupin","akira":"AKIRA",
    "nausicaa":"Nausicaa of the Valley of the Wind","laputa":"Castle in the Sky","totoro":"My Neighbor Totoro",
    "lunlun":"Hana no Ko Lunlun","ikkyu":"Ikkyuu-san","niels":"Nils no Fushigi na Tabi",
    "oroad":"Kimagure Orange Road","troopers":"Ronin Warriors","patlabor":"Patlabor",
    "wataru":"Mashin Hero Wataru","slayers":"Slayers","tekkaman":"Tekkaman Blade",
    "nadesico":"Martian Successor Nadesico","rayearth":"Magic Knight Rayearth","ccsakura":"Cardcaptor Sakura",
    "kindaichi":"Kindaichi","chuka":"Cooking Master Boy","hxh":"Hunter x Hunter","ghostshell":"Ghost in the Shell",
    "berserk":"Berserk","trigun":"Trigun","bebop":"Cowboy Bebop",
    "catseye":"Cat's Eye","ginga999":"Galaxy Express 999","versailles":"Rose of Versailles",
    "maison":"Maison Ikkoku","shurato":"Shurato","mononoke":"Princess Mononoke","gundam_w":"Gundam Wing",
    "initiald":"Initial D","gto":"Great Teacher Onizuka","sainttail":"Saint Tail",
    "rantarou":"Nintama Rantarou","jojoova":"JoJo's Bizarre Adventure",
}

def fetch(q):
    url = THEMES_Q.format(q=q.replace(" ", "%20").replace("&", "%26").replace("'", "%27"))
    for a in range(4):
        r = subprocess.run(["curl","-s","--max-time","25","-H","Accept: application/vnd.api+json",
                            "-H","User-Agent: MangaCharacterMuseum/0.1", url], capture_output=True, text=True)
        try:
            return json.loads(r.stdout)
        except Exception:
            time.sleep(5 + a*5)
    return None

def pick_theme(anime_obj, want="OP"):
    """优先 sequence=1 且非 EN 曲目"""
    best = None
    for t in anime_obj.get("animethemes", []):
        if t.get("type") != want:
            continue
        seq = t.get("sequence") or 99
        song = (t.get("song") or {}).get("title", "")
        for e in t.get("animethemeentries", []):
            for v in e.get("videos", []):
                link = v.get("link", "")
                if not link or link.endswith("-EN.webm"):
                    continue
                cand = {"title": song, "video": link, "seq": seq}
                if best is None or cand["seq"] < best["seq"]:
                    best = cand
    return best

out, misses = {}, []
for key, name in ANIME_NAMES.items():
    d = fetch(name)
    time.sleep(1.1)
    anime_list = (d or {}).get("anime") or []
    target = None
    for a in anime_list:
        if name.lower().split(":")[0][:10] in (a.get("name") or "").lower() or name.lower()[:10] in (a.get("name") or "").lower():
            target = a; break
    if not target and anime_list:
        target = anime_list[0]
    if not target:
        misses.append({"key": key, "reason": "anime-not-found", "q": name})
        print(f"✗ {key} ({name}) 未找到", flush=True)
        continue
    op = pick_theme(target, "OP")
    ed = pick_theme(target, "ED")
    if op or ed:
        out[key] = {"animeName": target.get("name"),
                    "slug": (target.get("slug") or target.get("name", "").lower().replace(" ", "-")),
                    "op": op, "ed": ed}
        t = op or ed
        print(f"✓ {key}: {(op or ed)['title']} [{target.get('name')}]", flush=True)
    else:
        misses.append({"key": key, "reason": "no-themes", "name": target.get("name")})
        print(f"✗ {key} ({target.get('name')}) 无曲目", flush=True)

json.dump({"themes": out, "misses": misses}, open("/tmp/museum_themes.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"\n主题曲完成：{len(out)}/{len(ANIME_NAMES)}；缺：{[m['key'] for m in misses]}")
