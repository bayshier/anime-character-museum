/* 经典动漫人物博物馆 · 展厅渲染与档案弹窗 */
(function () {
  "use strict";

  var HALLS = [
    { key: "80s", title: "80年代馆", sub: "HALL OF THE 1980s",
      desc: "从机器人到圣衣，从小学生到世纪末救世主——电视机前的十年热血。" },
    { key: "90s", title: "90年代馆", sub: "HALL OF THE 1990s",
      desc: "篮球、侦探、水手服与数码世界——平成年代的群星。" },
    { key: "00s", title: "00年代馆", sub: "HALL OF THE 2000s",
      desc: "游戏王、火影与炼金术——平成少年的热血续章。" },
    { key: "10s", title: "10年代馆", sub: "HALL OF THE 2010s",
      desc: "巨人、刀剑与魔法少女——网络时代的群像史诗。" },
    { key: "20s", title: "20年代馆", sub: "HALL OF THE 2020s",
      desc: "咒术、间谍、摇滚与芙莉莲——正在书写的新经典。" }
  ];

  var state = { hall: "all", q: "" };

  /* Fisher-Yates 洗牌：每次打开页面、切换展厅都随机排列展品 */
  function shuffle(arr) {
    var a = arr.slice();
    for (var i = a.length - 1; i > 0; i--) {
      var j = Math.floor(Math.random() * (i + 1));
      var t = a[i]; a[i] = a[j]; a[j] = t;
    }
    return a;
  }

  /* 展示用缩略图（WebP 460×690）；闪卡纹理才加载原图 */
  function thumbOf(src) {
    return String(src).replace(/^exhibits\//, "exhibits/thumb/").replace(/\.jpg$/, ".webp");
  }

  /* Three.js 闪卡查看器按需加载：首次打开档案才拉取 three.module.js（约 1.3MB） */
  var holoLoading = null;
  function ensureHolo() {
    if (window.HoloCard) return Promise.resolve();
    if (!holoLoading) {
      holoLoading = import("./holocard.js").catch(function (e) {
        holoLoading = null;
        throw e;
      });
    }
    return holoLoading;
  }

  function el(tag, cls, text) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text !== undefined) n.textContent = text;
    return n;
  }

  /* 搜索：人物中/日/英名、作品中/英名、声优、原作者、名台词 */
  function matchChar(c, q) {
    var hay = [c.nameZh, c.nameJp, c.nameEn, c.animeZh, c.animeEn, c.cv, c.author, c.quote]
      .join(" ").toLowerCase();
    return hay.indexOf(q.toLowerCase()) !== -1;
  }

  function renderSearch(q) {
    var root = document.getElementById("halls");
    var hits = CHARACTERS.filter(function (c) { return matchChar(c, q); });
    var section = el("section", "hall-section");
    var title = el("h2", "hall-title", "🔍 搜索结果");
    title.appendChild(el("small", "", q.toUpperCase()));
    section.appendChild(title);
    section.appendChild(el("p", "hall-desc", "在五座展馆的全部展品中检索（命中 " + hits.length + " 件）"));
    if (!hits.length) {
      var empty = el("p", "search-empty");
      empty.appendChild(document.createTextNode("没有找到与 "));
      empty.appendChild(el("b", "", q));
      empty.appendChild(document.createTextNode(" 相关的展品——试试「龙珠」「灌篮」「圣斗士」或人物名。"));
      section.appendChild(empty);
    } else {
      var grid = el("div", "grid");
      hits.forEach(function (c) {
        grid.appendChild(buildCase(c, EXNO[c.id]));
      });
      section.appendChild(grid);
    }
    root.appendChild(section);
  }

  /* 展品编号：全局唯一，EX-01 起按入库顺序 */
  var EXNO = {};
  function numberExhibits() {
    CHARACTERS.forEach(function (c, i) {
      EXNO[c.id] = "EX-" + String(i + 1).padStart(2, "0");
    });
  }

  function buildCase(ch, no) {
    var btn = el("button", "case");
    btn.setAttribute("data-char", ch.id);

    var thumb = el("span", "case-thumb");
    var img = el("img", "case-photo");
    img.src = thumbOf(ch.image); img.alt = ch.nameZh + "（" + ch.animeZh + "）"; img.loading = "lazy"; img.decoding = "async";
    thumb.appendChild(img);
    thumb.appendChild(el("span", "case-no", no));
    var scrim = el("span", "case-scrim");
    scrim.appendChild(el("span", "case-name", ch.nameZh));
    scrim.appendChild(el("span", "case-from", ch.animeZh + " · " + ch.year));
    thumb.appendChild(scrim);
    btn.appendChild(thumb);
    btn.appendChild(el("span", "case-hall", ch.year));

    btn.addEventListener("click", function () { openArchive(ch, no); });
    return btn;
  }

  function render() {
    var root = document.getElementById("halls");
    root.innerHTML = "";

    if (state.q) { renderSearch(state.q); return; }

    HALLS.forEach(function (hall) {
      if (state.hall !== "all" && state.hall !== hall.key) return;
      var chars = shuffle(CHARACTERS.filter(function (c) { return c.hall === hall.key; }));
      var section = el("section", "hall-section");
      var title = el("h2", "hall-title", hall.title);
      title.appendChild(el("small", "", hall.sub));
      section.appendChild(title);
      section.appendChild(el("p", "hall-desc", hall.desc + "（" + chars.length + " 件展品）"));

      var grid = el("div", "grid");
      chars.forEach(function (c) { grid.appendChild(buildCase(c, EXNO[c.id])); });
      section.appendChild(grid);
      root.appendChild(section);
    });
  }

  /* ---------- 档案弹窗 ---------- */
  var modal = document.getElementById("archive");

  var currentChar = null, currentNo = "";
  function openArchive(ch, no) {
    currentChar = ch; currentNo = no;
    document.getElementById("archive-img").src = thumbOf(ch.image);
    document.getElementById("archive-img").alt = ch.nameZh;
    document.getElementById("archive-no").textContent = "展品编号 " + no;
    document.getElementById("archive-name").textContent = ch.nameZh;
    document.getElementById("archive-jp").textContent = ch.nameJp;
    document.getElementById("archive-en").textContent = ch.nameEn;

    var facts = document.getElementById("archive-facts");
    facts.innerHTML = "";
    [
      ["登场作品", ch.animeZh + "（" + ch.animeEn + "）"],
      ["首播年份", String(ch.year)],
      ["原作者", ch.author],
      ["配音", ch.cv || "—"]
    ].forEach(function (row) {
      var dt = el("dt", "", row[0]); var dd = el("dd", "", row[1]);
      facts.appendChild(dt); facts.appendChild(dd);
    });

    document.getElementById("archive-feature").textContent = ch.feature;
    document.getElementById("archive-intro").textContent = ch.intro;
    document.getElementById("archive-quote-wrap").hidden = !ch.quote;
    document.getElementById("archive-quote").textContent = ch.quote ? "「" + ch.quote + "」" : "";
    document.getElementById("archive-src").href = ch.source;
    fillTheme(ch);
    showHolo(ch, no);

    modal.hidden = false;
    document.body.style.overflow = "hidden";
  }

  /* ---------- 闪卡：随档案直接展示 ---------- */
  function showHolo(ch, no) {
    var holo = document.getElementById("figure-holo");
    var label = document.getElementById("holo-label");
    var btns = document.getElementById("holo-btns");
    var flat = document.getElementById("figure-flat");
    holo.hidden = false; label.hidden = false; btns.hidden = false;
    function start(openFn) {
      openFn().then(function (hc) {
        return window.HoloCard.open(ch.image, ch, no).then(function (ok) {
          if (!ok) {
            setTimeout(function () {
              window.HoloCard.open(ch.image, ch, no).then(function (ok2) {
                if (!ok2) { holo.hidden = true; label.hidden = true; btns.hidden = true; }
              });
            }, 800);
          }
        });
      }).catch(function (e) {
        window.__holoErr = String((e && e.message) || e);
        holo.hidden = true; label.hidden = true; btns.hidden = true;
      });
    }
    if (window.HoloCard) start(function () { return Promise.resolve(); });
    else start(ensureHolo);
  }
  function hideHolo() {
    var holo = document.getElementById("figure-holo");
    var label = document.getElementById("holo-label");
    var btns = document.getElementById("holo-btns");
    holo.hidden = true; label.hidden = true; btns.hidden = true;
    if (window.HoloCard) window.HoloCard.close();
  }

  /* ---------- 主题曲：开档案即自动缓冲播放 + 站外跳转 ---------- */
  function fillTheme(ch) {
    var video = document.getElementById("archive-theme-video");
    var songEl = document.getElementById("archive-theme-song");
    var hint = document.getElementById("archive-theme-hint");
    var linksEl = document.getElementById("archive-theme-links");
    video.pause();
    video.removeAttribute("src");
    video.load();
    hint.hidden = true;
    linksEl.innerHTML = "";

    var yt = document.createElement("a");
    yt.href = "https://www.youtube.com/results?search_query=" +
      encodeURIComponent(ch.animeEn + " OP theme");
    yt.target = "_blank"; yt.rel = "noopener";
    yt.textContent = "▶ YouTube 搜完整版";
    linksEl.appendChild(yt);

    var theme = (typeof THEMES !== "undefined") ? THEMES[ch.animeKey] : null;
    var t = theme && (theme.op || theme.ed);
    if (!t) {
      songEl.textContent = "暂无可内嵌曲目，欢迎从上方链接试听：";
      return;
    }
    video.src = t.video;
    songEl.textContent = (theme.op ? "OP" : "ED") + " · " + t.title +
      (theme.op && theme.ed ? "（另有 ED 可在站内切换试听）" : "");
    /* 自动缓冲播放：先尝试有声，被浏览器拦截则静音自动播 */
    video.muted = false;
    var p = video.play();
    if (p && p.catch) {
      p.catch(function () {
        video.muted = true;
        video.play().catch(function () {});
        hint.hidden = false;
      });
    }
  }

  function closeArchive() {
    modal.hidden = true;
    document.body.style.overflow = "";
    hideHolo();
  }

  modal.addEventListener("click", function (e) {
    if (e.target.hasAttribute("data-close")) closeArchive();
  });
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && !modal.hidden) closeArchive();
  });

  /* ---------- 展厅切换 ---------- */
  document.querySelectorAll(".hall-tab").forEach(function (tab) {
    tab.addEventListener("click", function () {
      document.querySelectorAll(".hall-tab").forEach(function (t) { t.classList.remove("is-active"); });
      tab.classList.add("is-active");
      state.hall = tab.getAttribute("data-hall");
      render();
      window.scrollTo({ top: 0, behavior: "smooth" });
    });
  });

  /* ---------- 门厅统计 ---------- */
  function stats() {
    var box = document.getElementById("stats");
    var halls = {};
    var animes = {};
    CHARACTERS.forEach(function (c) {
      halls[c.hall] = (halls[c.hall] || 0) + 1;
      animes[c.animeKey] = 1;
    });
    [
      CHARACTERS.length + " 位人物",
      Object.keys(animes).length + " 部作品",
      Object.keys(halls).length + " 座展厅",
      "1980 – 至今"
    ].forEach(function (t) { box.appendChild(el("span", "", t)); });
    document.getElementById("intro-count").textContent = String(CHARACTERS.length);
  }

  /* ---------- 闪卡按钮 ---------- */
  document.getElementById("holo-dl").addEventListener("click", function () {
    if (window.HoloCard) window.HoloCard.download();
  });
  document.getElementById("holo-flip").addEventListener("click", function () {
    if (window.HoloCard) window.HoloCard.flip();
  });

  /* ---------- 搜索框（150ms 防抖） ---------- */
  var searchBox = document.getElementById("search");
  var debounceTimer = null;
  searchBox.addEventListener("input", function () {
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(function () {
      state.q = searchBox.value.trim();
      render();
    }, 150);
  });

  numberExhibits();
  stats();
  render();
})();
