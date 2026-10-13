/* 主题曲数据 · 来自 AnimeThemes 开放档案，勿手改 */
const THEMES = {
  "gundam": {
    "animeName": "Mobile Suit Gundam",
    "slug": "mobile_suit_gundam",
    "op": {
      "title": "Tobe! Gundam (Fly! Gundam)",
      "video": "https://v.animethemes.moe/Gundam-OP1.webm",
      "seq": 99
    },
    "ed": {
      "title": "Eien Ni Amuro (Forever Amuro)",
      "video": "https://v.animethemes.moe/Gundam-ED1.webm",
      "seq": 99
    }
  },
  "urusei": {
    "animeName": "Urusei Yatsura",
    "slug": "urusei_yatsura",
    "op": {
      "title": "Lum no Love Song",
      "video": "https://v.animethemes.moe/UruseiYatsura-OP1.webm",
      "seq": 1
    },
    "ed": {
      "title": "Uchuu wa Taihen da!",
      "video": "https://v.animethemes.moe/UruseiYatsura-ED1.webm",
      "seq": 1
    }
  },
  "tsubasa": {
    "animeName": "Captain Tsubasa",
    "slug": "captain_tsubasa",
    "op": {
      "title": "Start Dash!",
      "video": "https://v.animethemes.moe/CaptainTsubasa2018-OP1.webm",
      "seq": 1
    },
    "ed": {
      "title": "Moete Hero",
      "video": "https://v.animethemes.moe/CaptainTsubasa2018-ED1.webm",
      "seq": 1
    }
  },
  "dragonball": {
    "animeName": "Dragon Ball",
    "slug": "dragon_ball",
    "op": {
      "title": "Makafushigi Adventure",
      "video": "https://v.animethemes.moe/DragonBall-OP1.webm",
      "seq": 99
    },
    "ed": {
      "title": "Romatikku Ageru Yo",
      "video": "https://v.animethemes.moe/DragonBall-ED1.webm",
      "seq": 99
    }
  },
  "seiya": {
    "animeName": "Saint Seiya",
    "slug": "saint_seiya",
    "op": {
      "title": "Pegasus Gensou",
      "video": "https://v.animethemes.moe/SaintSeiya-OP1.webm",
      "seq": 1
    },
    "ed": {
      "title": "Eien Blue",
      "video": "https://v.animethemes.moe/SaintSeiya-ED1.webm",
      "seq": 1
    }
  },
  "cityhunter": {
    "animeName": "City Hunter",
    "slug": "city_hunter",
    "op": {
      "title": "CITY HUNTER ~Ai yo Kienaide~",
      "video": "https://v.animethemes.moe/CityHunter-OP1.webm",
      "seq": 1
    },
    "ed": {
      "title": "Get Wild",
      "video": "https://v.animethemes.moe/CityHunter-ED1.webm",
      "seq": 99
    }
  },
  "dbz": {
    "animeName": "Dragon Ball Z",
    "slug": "dragon_ball_z",
    "op": {
      "title": "Cha-La Head-Cha-La",
      "video": "https://v.animethemes.moe/DragonBallZ-OP1-NCBD1080.webm",
      "seq": 1
    },
    "ed": {
      "title": "Dete Koi Tobikiri ZENKAI Power!",
      "video": "https://v.animethemes.moe/DragonBallZ-ED1.webm",
      "seq": 1
    }
  },
  "maruko": {
    "animeName": "Chibi Maruko-chan",
    "slug": "chibi_maruko_chan",
    "op": {
      "title": "Yume Ippai",
      "video": "https://v.animethemes.moe/ChibiMarukoChan-OP1.webm",
      "seq": 99
    },
    "ed": {
      "title": "Odoru Pompokorin",
      "video": "https://v.animethemes.moe/ChibiMarukoChan-ED1.webm",
      "seq": 1
    }
  },
  "shinchan": {
    "animeName": "Crayon Shin-chan",
    "slug": "crayon_shin_chan",
    "op": {
      "title": "Doubutsuen wa Taihen da",
      "video": "https://v.animethemes.moe/CrayonShinChan-OP1.webm",
      "seq": 1
    },
    "ed": {
      "title": "Uta wo Utaou",
      "video": "https://v.animethemes.moe/CrayonShinChan-ED1.webm",
      "seq": 1
    }
  },
  "slamdunk": {
    "animeName": "Slam Dunk",
    "slug": "slam_dunk",
    "op": {
      "title": "Kimi ga Suki da to Sakebitai",
      "video": "https://v.animethemes.moe/SlamDunk-OP1.webm",
      "seq": 1
    },
    "ed": {
      "title": "Anata Dake Mitsumeteru",
      "video": "https://v.animethemes.moe/SlamDunk-ED1.webm",
      "seq": 1
    }
  },
  "eva": {
    "animeName": "Neon Genesis Evangelion",
    "slug": "neon_genesis_evangelion",
    "op": {
      "title": "Zankoku na Tenshi no Thesis",
      "video": "https://v.animethemes.moe/NeonGenesisEvangelion-OP1.webm",
      "seq": 99
    },
    "ed": {
      "title": "Fly Me to the Moon",
      "video": "https://v.animethemes.moe/NeonGenesisEvangelion-ED1.webm",
      "seq": 1
    }
  },
  "conan": {
    "animeName": "Detective Conan",
    "slug": "detective_conan",
    "op": {
      "title": "Mune ga Dokidoki",
      "video": "https://v.animethemes.moe/DetectiveConan-OP1-NCDVD480.webm",
      "seq": 1
    },
    "ed": {
      "title": "Step by Step",
      "video": "https://v.animethemes.moe/DetectiveConan-ED1.webm",
      "seq": 1
    }
  },
  "pokemon": {
    "animeName": "Pokemon",
    "slug": "pokemon",
    "op": {
      "title": "Mezase Pokemon Master",
      "video": "https://v.animethemes.moe/Pokemon-OP1.webm",
      "seq": 1
    },
    "ed": {
      "title": "Hyakugojuuichi",
      "video": "https://v.animethemes.moe/Pokemon-ED1.webm",
      "seq": 1
    }
  },
  "onepiece": {
    "animeName": "One Piece",
    "slug": "one_piece",
    "op": {
      "title": "We Are!",
      "video": "https://v.animethemes.moe/OnePiece-OP1-NCDVD480.webm",
      "seq": 1
    },
    "ed": {
      "title": "memories",
      "video": "https://v.animethemes.moe/OnePiece-ED1-NCDVD480.webm",
      "seq": 1
    }
  },
  "digimon": {
    "animeName": "Digimon Adventure",
    "slug": "digimon_adventure",
    "op": {
      "title": "Butter-Fly",
      "video": "https://v.animethemes.moe/DigimonAdventure-OP1.webm",
      "seq": 99
    },
    "ed": {
      "title": "I wish",
      "video": "https://v.animethemes.moe/DigimonAdventure-ED1.webm",
      "seq": 1
    }
  },
  "macross": {
    "animeName": "Macross",
    "slug": "macross",
    "op": {
      "title": "Macross",
      "video": "https://v.animethemes.moe/Macross-OP1.webm",
      "seq": 99
    },
    "ed": {
      "title": "Runner",
      "video": "https://v.animethemes.moe/Macross-ED1.webm",
      "seq": 1
    }
  },
  "touch": {
    "animeName": "Touch",
    "slug": "touch",
    "op": {
      "title": "Touch",
      "video": "https://v.animethemes.moe/Touch-OP1.webm",
      "seq": 1
    },
    "ed": {
      "title": "Kimi ga Inakereba",
      "video": "https://v.animethemes.moe/Touch-ED1.webm",
      "seq": 1
    }
  },
  "slayers": {
    "animeName": "Slayers",
    "slug": "slayers",
    "op": {
      "title": "Get along",
      "video": "https://v.animethemes.moe/Slayers-OP1.webm",
      "seq": 99
    },
    "ed": {
      "title": "KUJIKENAIKARA!",
      "video": "https://v.animethemes.moe/Slayers-ED1.webm",
      "seq": 99
    }
  },
  "rayearth": {
    "animeName": "Magic Knight Rayearth",
    "slug": "magic_knight_rayearth",
    "op": {
      "title": "Yuzurenai Negai",
      "video": "https://v.animethemes.moe/MagicKnightRayearth-OP1.webm",
      "seq": 99
    },
    "ed": {
      "title": "Asu e no Yuuki",
      "video": "https://v.animethemes.moe/MagicKnightRayearth-ED1.webm",
      "seq": 99
    }
  },
  "ccsakura": {
    "animeName": "Cardcaptor Sakura",
    "slug": "cardcaptor_sakura",
    "op": {
      "title": "Catch You Catch Me",
      "video": "https://v.animethemes.moe/CardcaptorSakura-OP1.webm",
      "seq": 1
    },
    "ed": {
      "title": "Groovy!",
      "video": "https://v.animethemes.moe/CardcaptorSakura-ED1.webm",
      "seq": 1
    }
  },
  "hxh": {
    "animeName": "Hunter x Hunter",
    "slug": "hunter_x_hunter",
    "op": {
      "title": "Ohayou",
      "video": "https://v.animethemes.moe/HunterHunter-OP1.webm",
      "seq": 1
    },
    "ed": {
      "title": "Kaze no Uta",
      "video": "https://v.animethemes.moe/HunterHunter-ED1.webm",
      "seq": 1
    }
  },
  "ghostshell": {
    "animeName": "Ghost in the Shell",
    "slug": "ghost_in_the_shell",
    "op": {
      "title": "Making of a Cyborg",
      "video": "https://v.animethemes.moe/GhostInTheShell-OP1.webm",
      "seq": 99
    },
    "ed": {
      "title": "Reincarnation",
      "video": "https://v.animethemes.moe/GhostInTheShell-ED1.webm",
      "seq": 99
    }
  },
  "berserk": {
    "animeName": "Berserk",
    "slug": "berserk",
    "op": {
      "title": "Tell Me Why",
      "video": "https://v.animethemes.moe/Berserk-OP1.webm",
      "seq": 99
    },
    "ed": {
      "title": "Waiting So Long",
      "video": "https://v.animethemes.moe/Berserk-ED1.webm",
      "seq": 99
    }
  },
  "trigun": {
    "animeName": "Trigun",
    "slug": "trigun",
    "op": {
      "title": "H.T.",
      "video": "https://v.animethemes.moe/Trigun-OP1.webm",
      "seq": 99
    },
    "ed": {
      "title": "Kaze wa Mirai ni Fuku",
      "video": "https://v.animethemes.moe/Trigun-ED1.webm",
      "seq": 99
    }
  },
  "bebop": {
    "animeName": "Cowboy Bebop",
    "slug": "cowboy_bebop",
    "op": {
      "title": "Tank!",
      "video": "https://v.animethemes.moe/CowboyBebop-OP1.webm",
      "seq": 99
    },
    "ed": {
      "title": "The Real Folk Blues",
      "video": "https://v.animethemes.moe/CowboyBebop-ED1.webm",
      "seq": 1
    }
  },
  "catseye": {
    "animeName": "Cat's Eye",
    "slug": "cats_eye",
    "op": {
      "title": "Cat's Eye",
      "video": "https://v.animethemes.moe/CatsEye-OP1.webm",
      "seq": 1
    },
    "ed": {
      "title": "Dancing with the sunshine",
      "video": "https://v.animethemes.moe/CatsEye-ED1.webm",
      "seq": 1
    }
  },
  "versailles": {
    "animeName": "Rose of Versailles",
    "slug": "rose_of_versailles",
    "op": {
      "title": "Bara wa Utsukushiku Chiru",
      "video": "https://v.animethemes.moe/RoseOfVersailles-OP1.webm",
      "seq": 99
    },
    "ed": {
      "title": "Ai no Hikari to Kage",
      "video": "https://v.animethemes.moe/RoseOfVersailles-ED1.webm",
      "seq": 99
    }
  },
  "maison": {
    "animeName": "Maison Ikkoku",
    "slug": "maison_ikkoku",
    "op": {
      "title": "Kanashimi yo Konnichiwa",
      "video": "https://v.animethemes.moe/MaisonIkkoku-OP1.webm",
      "seq": 1
    },
    "ed": {
      "title": "Ashita Hareru ka",
      "video": "https://v.animethemes.moe/MaisonIkkoku-ED1.webm",
      "seq": 1
    }
  },
  "gto": {
    "animeName": "Great Teacher Onizuka",
    "slug": "great_teacher_onizuka",
    "op": {
      "title": "Driver's High",
      "video": "https://v.animethemes.moe/GreatTeacherOnizuka-OP1.webm",
      "seq": 1
    },
    "ed": {
      "title": "Last Piece",
      "video": "https://v.animethemes.moe/GreatTeacherOnizuka-ED1.webm",
      "seq": 1
    }
  },
  "astroboy": {
    "animeName": "Tetsuwan Atom",
    "slug": "tetsuwan_atom",
    "op": {
      "title": "Tetsuwan Atom",
      "video": "https://v.animethemes.moe/TetsuwanAtom-OP1-Lyrics.webm",
      "seq": 99
    },
    "ed": {
      "title": "Tetsuwan Atom",
      "video": "https://v.animethemes.moe/TetsuwanAtom-ED1.webm",
      "seq": 99
    }
  },
  "drslump": {
    "animeName": "Dr. Slump: Arale-chan",
    "slug": "dr_slump_arale_chan",
    "op": {
      "title": "Waiwai World",
      "video": "https://v.animethemes.moe/DrSlumpAraleChan-OP1.webm",
      "seq": 1
    },
    "ed": {
      "title": "Ara Ara Arale-chan",
      "video": "https://v.animethemes.moe/DrSlumpAraleChan-ED1.webm",
      "seq": 1
    }
  },
  "hokuto": {
    "animeName": "Hokuto no Ken",
    "slug": "hokuto_no_ken",
    "op": {
      "title": "Ai wo Torimodose!!",
      "video": "https://v.animethemes.moe/HokutoNoKen-OP1.webm",
      "seq": 1
    },
    "ed": {
      "title": "Yuria... Eien ni",
      "video": "https://v.animethemes.moe/HokutoNoKen-ED1.webm",
      "seq": 1
    }
  },
  "ranma": {
    "animeName": "Ranma ½",
    "slug": "ranma",
    "op": {
      "title": "Jaja Uma ni Sasenai de",
      "video": "https://v.animethemes.moe/Ranma-OP1.webm",
      "seq": 1
    },
    "ed": {
      "title": "Platonic Tsuranuite",
      "video": "https://v.animethemes.moe/Ranma-ED1.webm",
      "seq": 1
    }
  },
  "sailormoon": {
    "animeName": "Bishoujo Senshi Sailor Moon",
    "slug": "bishoujo_senshi_sailor_moon",
    "op": {
      "title": "Moonlight Densetsu",
      "video": "https://v.animethemes.moe/SailorMoon-OP1.webm",
      "seq": 99
    },
    "ed": {
      "title": "Heart Moving",
      "video": "https://v.animethemes.moe/SailorMoon-ED1.webm",
      "seq": 1
    }
  },
  "lupin": {
    "animeName": "Lupin III: Part II",
    "slug": "lupin_iii_part_ii",
    "op": {
      "title": "Theme from Lupin III '77",
      "video": "https://v.animethemes.moe/LupinIIIPartII-OP1.webm",
      "seq": 1
    },
    "ed": {
      "title": "Love Theme",
      "video": "https://v.animethemes.moe/LupinIIIPartII-ED1.webm",
      "seq": 1
    }
  },
  "laputa": {
    "animeName": "Tenkuu no Shiro Laputa",
    "slug": "tenkuu_no_shiro_laputa",
    "op": {
      "title": "Sora kara Futtekita Shoujo",
      "video": "https://v.animethemes.moe/TenkuuNoShiroLaputa-OP1.webm",
      "seq": 99
    },
    "ed": null
  },
  "oroad": {
    "animeName": "Kimagure Orange☆Road",
    "slug": "kimagure_orangeroad",
    "op": {
      "title": "Night of summer side",
      "video": "https://v.animethemes.moe/KimagureOrangeRoad-OP1.webm",
      "seq": 1
    },
    "ed": {
      "title": "Natsu no Mirage",
      "video": "https://v.animethemes.moe/KimagureOrangeRoad-ED1.webm",
      "seq": 1
    }
  },
  "troopers": {
    "animeName": "Yoroiden Samurai Troopers",
    "slug": "yoroiden_samurai_troopers",
    "op": {
      "title": "Stardust Eyes",
      "video": "https://v.animethemes.moe/YoroidenSamuraiTroopers-OP1.webm",
      "seq": 1
    },
    "ed": {
      "title": "Far away",
      "video": "https://v.animethemes.moe/YoroidenSamuraiTroopers-ED1.webm",
      "seq": 1
    }
  },
  "wataru": {
    "animeName": "Mashin Eiyuuden Wataru",
    "slug": "mashin_eiyuuden_wataru",
    "op": {
      "title": "Step",
      "video": "https://v.animethemes.moe/MashinEiyuudenWataru-OP1.webm",
      "seq": 99
    },
    "ed": {
      "title": "Achiachi Adventure",
      "video": "https://v.animethemes.moe/MashinEiyuudenWataru-ED1.webm",
      "seq": 99
    }
  },
  "tekkaman": {
    "animeName": "Uchuu no Kishi Tekkaman Blade",
    "slug": "uchuu_no_kishi_tekkaman_blade",
    "op": {
      "title": "Reason",
      "video": "https://v.animethemes.moe/UchuuNoKishiTekkamanBlade-OP1.webm",
      "seq": 1
    },
    "ed": {
      "title": "Energy of Love",
      "video": "https://v.animethemes.moe/UchuuNoKishiTekkamanBlade-ED1.webm",
      "seq": 1
    }
  },
  "nadesico": {
    "animeName": "Kidou Senkan Nadesico",
    "slug": "kidou_senkan_nadesico",
    "op": {
      "title": "You Get to Burning",
      "video": "https://v.animethemes.moe/KidouSenkanNadesico-OP1.webm",
      "seq": 99
    },
    "ed": {
      "title": "Watashi Rashiku",
      "video": "https://v.animethemes.moe/KidouSenkanNadesico-ED1.webm",
      "seq": 1
    }
  },
  "kindaichi": {
    "animeName": "Kindaichi Shounen no Jikenbo",
    "slug": "kindaichi_shounen_no_jikenbo",
    "op": {
      "title": "Confused Memories",
      "video": "https://v.animethemes.moe/Kindaichi-OP1.webm",
      "seq": 1
    },
    "ed": {
      "title": "Futari",
      "video": "https://v.animethemes.moe/Kindaichi-ED1.webm",
      "seq": 1
    }
  },
  "chuka": {
    "animeName": "Chuuka Ichiban!",
    "slug": "chuuka_ichiban",
    "op": {
      "title": "Sora",
      "video": "https://v.animethemes.moe/ChuukaIchiban-OP1.webm",
      "seq": 1
    },
    "ed": {
      "title": "Aoi Sora ni Deaeta",
      "video": "https://v.animethemes.moe/ChuukaIchiban-ED1.webm",
      "seq": 1
    }
  },
  "ginga999": {
    "animeName": "Ginga Tetsudou 999",
    "slug": "ginga_tetsudou_999",
    "op": {
      "title": "Ginga Tetsudou 999",
      "video": "https://v.animethemes.moe/GingaTetsudou999-OP1.webm",
      "seq": 99
    },
    "ed": {
      "title": "Aoi Chikyuu",
      "video": "https://v.animethemes.moe/GingaTetsudou999-ED1.webm",
      "seq": 99
    }
  },
  "mononoke": {
    "animeName": "Mononoke Hime",
    "slug": "mononoke_hime",
    "op": null,
    "ed": {
      "title": "Mononoke Hime",
      "video": "https://v.animethemes.moe/MononokeHime-ED1.webm",
      "seq": 99
    }
  },
  "gundam_w": {
    "animeName": "Mobile Suit Gundam Wing",
    "slug": "mobile_suit_gundam_wing",
    "op": {
      "title": "Just Communication",
      "video": "https://v.animethemes.moe/GundamWing-OP1.webm",
      "seq": 1
    },
    "ed": {
      "title": "It's Just Love!",
      "video": "https://v.animethemes.moe/GundamWing-ED1.webm",
      "seq": 99
    }
  },
  "initiald": {
    "animeName": "Initial D First Stage",
    "slug": "initial_d_first_stage",
    "op": {
      "title": "Around the World",
      "video": "https://v.animethemes.moe/InitialDFirstStage-OP1.webm",
      "seq": 1
    },
    "ed": {
      "title": "Rage Your Dream",
      "video": "https://v.animethemes.moe/InitialDFirstStage-ED1.webm",
      "seq": 1
    }
  },
  "sainttail": {
    "animeName": "Kaitou Saint Tail",
    "slug": "kaitou_saint_tail",
    "op": {
      "title": "Toki o Koete",
      "video": "https://v.animethemes.moe/KaitouSaintTail-OP1.webm",
      "seq": 1
    },
    "ed": {
      "title": "Junshin",
      "video": "https://v.animethemes.moe/KaitouSaintTail-ED1.webm",
      "seq": 1
    }
  },
  "kenshin": {
    "animeName": "Rurouni Kenshin: Meiji Kenkaku Romantan",
    "slug": "rurouni_kenshin_meiji_kenkaku_romantan",
    "op": {
      "title": "Sobakasu",
      "video": "https://v.animethemes.moe/RurouniKenshin-OP1.webm",
      "seq": 1
    },
    "ed": {
      "title": "Tactics",
      "video": "https://v.animethemes.moe/RurouniKenshin-ED1.webm",
      "seq": 1
    }
  },
  "letsgo": {
    "animeName": "Bakusou Kyoudai Let's & Go MAX",
    "slug": "bakusou_kyoudai_lets_go_max",
    "op": {
      "title": "Brave Heart",
      "video": "https://v.animethemes.moe/BakusouKyoudaiMax-OP1.webm",
      "seq": 99
    },
    "ed": {
      "title": "My name is Car Boy",
      "video": "https://v.animethemes.moe/BakusouKyoudaiMax-ED1.webm",
      "seq": 1
    }
  },
  "patlabor": {
    "animeName": "Mobile Police Patlabor: Early Days",
    "slug": "mobile_police_patlabor_early_days",
    "op": {
      "title": "Mirai wa Lovers",
      "video": "https://v.animethemes.moe/MobilePolicePatlaborEarlyDays-OP1.webm",
      "seq": 99
    },
    "ed": null
  },
  "yyh": {
    "animeName": "Yuu☆Yuu☆Hakusho",
    "slug": "yuuyuuhakusho",
    "op": {
      "title": "Hohoemi no Bakudan",
      "video": "https://v.animethemes.moe/YuuYuuHakusho-OP1.webm",
      "seq": 99
    },
    "ed": {
      "title": "Homework ga Owaranai",
      "video": "https://v.animethemes.moe/YuuYuuHakusho-ED1.webm",
      "seq": 1
    }
  },
  "nadia": {
    "animeName": "Fushigi no Umi no Nadia",
    "slug": "fushigi_no_umi_no_nadia",
    "op": {
      "title": "Blue Water",
      "video": "https://v.animethemes.moe/FushigiNoUmiNoNadia-OP1.webm",
      "seq": 99
    },
    "ed": {
      "title": "Yes! I Will",
      "video": "https://v.animethemes.moe/FushigiNoUmiNoNadia-ED1.webm",
      "seq": 99
    }
  },
  "logh": {
    "animeName": "Ginga Eiyuu Densetsu",
    "slug": "ginga_eiyuu_densetsu",
    "op": {
      "title": "Skies of Love",
      "video": "https://v.animethemes.moe/GingaEiyuuDensetsu-OP1-Lyrics.webm",
      "seq": 1
    },
    "ed": {
      "title": "Hikari no Hashi wo koete",
      "video": "https://v.animethemes.moe/GingaEiyuuDensetsu-ED1-Lyrics.webm",
      "seq": 1
    }
  },
  "escaflowne": {
    "animeName": "Tenkuu no Escaflowne",
    "slug": "tenkuu_no_escaflowne",
    "op": {
      "title": "Yakusoku wa Iranai",
      "video": "https://v.animethemes.moe/TenkuuNoEscaflowne-OP1.webm",
      "seq": 99
    },
    "ed": {
      "title": "Mystic Eyes",
      "video": "https://v.animethemes.moe/TenkuuNoEscaflowne-ED1.webm",
      "seq": 99
    }
  },
  "tenchi": {
    "animeName": "Tenchi Muyou! Ryououki",
    "slug": "tenchi_muyou_ryououki",
    "op": {
      "title": "Tenchi Muyou! Ryououki no Theme",
      "video": "https://v.animethemes.moe/TenchiMuyouRyououki-OP1.webm",
      "seq": 99
    },
    "ed": {
      "title": "Renai no Sainou",
      "video": "https://v.animethemes.moe/TenchiMuyouRyououki-ED1.webm",
      "seq": 99
    }
  },
  "guruguru": {
    "animeName": "Mahoujin Guru Guru",
    "slug": "mahoujin_guru_guru",
    "op": {
      "title": "Trip Trip Trip",
      "video": "https://v.animethemes.moe/MahoujinGuruGuru2017-OP1-NCBD1080.webm",
      "seq": 1
    },
    "ed": {
      "title": "Round&Round&Round",
      "video": "https://v.animethemes.moe/MahoujinGuruGuru2017-ED1-NCBD1080.webm",
      "seq": 1
    }
  },
  "kinniku": {
    "animeName": "Kinnikuman",
    "slug": "kinnikuman",
    "op": {
      "title": "Kinnikuman Go Fight!",
      "video": "https://v.animethemes.moe/Kinnikuman-OP1.webm",
      "seq": 1
    },
    "ed": {
      "title": "Niku 2x9 Rock 'n Roll",
      "video": "https://v.animethemes.moe/Kinnikuman-ED1.webm",
      "seq": 1
    }
  },
  "harlock": {
    "animeName": "Uchuu Kaizoku Captain Harlock",
    "slug": "uchuu_kaizoku_captain_harlock",
    "op": {
      "title": "Captain Harlock",
      "video": "https://v.animethemes.moe/UchuuKaizokuCaptainHarlock-OP1.webm",
      "seq": 99
    },
    "ed": {
      "title": "Warera no Tabidachi",
      "video": "https://v.animethemes.moe/UchuuKaizokuCaptainHarlock-ED1.webm",
      "seq": 99
    }
  },
  "kiteretsu": {
    "animeName": "Kiteretsu Daihyakka",
    "slug": "kiteretsu_daihyakka",
    "op": {
      "title": "Oyome-san ni Natte Agenaizo",
      "video": "https://v.animethemes.moe/KiteretsuDaihyakka-OP1.webm",
      "seq": 1
    },
    "ed": {
      "title": "Magical Boy Magical Heart",
      "video": "https://v.animethemes.moe/KiteretsuDaihyakka-ED1.webm",
      "seq": 1
    }
  },
  "utena": {
    "animeName": "Shoujo Kakumei Utena",
    "slug": "shoujo_kakumei_utena",
    "op": {
      "title": "Rinbu - revolution",
      "video": "https://v.animethemes.moe/ShoujoKakumeiUtena-OP1.webm",
      "seq": 99
    },
    "ed": {
      "title": "Truth",
      "video": "https://v.animethemes.moe/ShoujoKakumeiUtena-ED1.webm",
      "seq": 1
    }
  },
  "votoms": {
    "animeName": "Soukou Kihei Votoms",
    "slug": "soukou_kihei_votoms",
    "op": {
      "title": "Honoo no Sadame",
      "video": "https://v.animethemes.moe/SoukouKiheiVotoms-OP1.webm",
      "seq": 99
    },
    "ed": {
      "title": "Itsumo Anata ga",
      "video": "https://v.animethemes.moe/SoukouKiheiVotoms-ED1.webm",
      "seq": 99
    }
  }
};
