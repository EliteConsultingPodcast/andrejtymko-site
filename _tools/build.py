#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Static site generator for the sample site. Output = plain HTML in the repo root (no build step needed on GitHub Pages).
Run:  python3 _tools/build.py
Add a language: add an entry to LANGS + strings in T + slugs in PATHS, then rebuild.
"""
import json, os, re, html, shutil
from pathlib import Path
from PIL import Image
import sys
sys.path.insert(0, str(Path(__file__).parent))
from data import *

ROOT = Path(__file__).resolve().parent.parent
PL_RAW = json.load(open(ROOT/"_tools"/"pl_raw.json", encoding="utf-8"))

LANGS = ["sk", "pl"]          # /de/ and /en/ can be added later
LANG_NAME = {"sk": "Slovenčina", "pl": "Polski", "de": "Deutsch", "en": "English"}
LANG_PREFIX = {"sk": [], "pl": ["pl"]}

# directory slugs per language
PATHS = {
  "sk": dict(home=[], books=["knihy"], stories=["poviedky"], about=["o-autorovi"], contact=["kontakt"], imprint=["impressum"], privacy=["ochrana-sukromia"]),
  "pl": dict(home=[], books=["ksiazki"], stories=["opowiadania"], about=["o-autorze"], contact=["kontakt"], imprint=["impressum"], privacy=["polityka-prywatnosci"]),
}

T = {
 "sk": dict(
   lang="sk", locale="sk-SK",
   nav=dict(home="Domov", books="Knihy", stories="Poviedky", about="O autorovi", contact="Kontakt"),
   site_title="Andrej Tymko", tagline="Príbehy z Tatier, Álp a Himalájí",
   hero_quote="Kým snívaš, žiješ.", hero_cite="– Andrej Tymko",
   hero_lead="Poviedky a knihy o tatranských nosičoch, chatároch a horaloch. Text aj audio, priamo od autora.",
   hero_cta1="Pozrieť poviedky", hero_cta2="Knihy",
   intro_h="Autor", intro_p="V Tatrách som sa našiel. Skalnatý svet bol mojím druhým domovom. Vyše dvanásť rokov som fungoval ako tatranský šerpa.",
   intro_more="Viac o autorovi",
   featured_h="Knihy", featured_more="Všetky knihy",
   grid_h="Poviedky", grid_all="Všetky poviedky", grid_n=8,
   buy="Kúpiť", buy_text="Text", buy_audio="Audio", buy_both="Kúpiť – text + audio", buy_audio_only="Kúpiť – audio", buy_text_only="Kúpiť – text",
   buy_book="Kúpiť knihu",
   via="Platba a stiahnutie súboru cez Payhip.", opens_payhip="Otvorí sa Payhip v novom okne.",
   kind=dict(both="Text + audio", audio="Audio", text="Text", pair="Text a audio zvlášť", book="Kniha"),
   details="Podrobnosti", back_stories="← Všetky poviedky", back_books="← Všetky knihy",
   excerpt_h="Ukážka z textu", excerpt_note="Ukážka zo začiatku poviedky. Celý text získate po kúpe.",
   no_excerpt="Ukážka z textu zatiaľ nie je pripravená.",
   pl_note="", price_each="€",
   stories_h="Poviedky", stories_lead="Všetky poviedky, ktoré sú práve v obchode na Payhipe. Ku každej patrí text, audio alebo oboje.",
   search="Hľadať poviedku…", search_label="Hľadať poviedku", nores="Nič sa nenašlo.",
   books_h="Knihy", books_lead="Dve knihy v elektronickej podobe.",
   about_h="O autorovi", about_bio_h="Moje horské ego v kocke", about_photo_alt="Andrej Tymko", about_src="Zdroj: autorov profil na Payhipe.",
   contact_h="Kontakt", contact_p="Kontaktné údaje autora budú doplnené.", contact_todo="DOPLNIŤ: kontaktný e-mail / formulár", contact_shop="Obchod s poviedkami nájdete na Payhipe:",
   imprint_h="Impressum", privacy_h="Ochrana súkromia",
   todo="DOPLNIŤ", todo_note="Táto stránka je zástupný text. Právne údaje nie sú vyplnené a musia byť doplnené pred zverejnením.",
   imprint_fields=["Prevádzkovateľ / autor", "Adresa", "IČO / DIČ (ak sa uplatňuje)", "Kontaktný e-mail", "Zodpovedná osoba za obsah"],
   privacy_fields=["Prevádzkovateľ údajov a kontakt", "Aké osobné údaje sa spracúvajú (pri platbe ich spracúva Payhip)", "Právny základ a doba uchovávania", "Práva dotknutej osoby", "Dozorný orgán"],
   privacy_fact="Technické informácie o tejto webovej stránke: stránka nepoužíva cookies, analytické ani reklamné nástroje a nenačítava externé skripty ani písma. Pri kliknutí na tlačidlo „Kúpiť“ sa otvorí stránka Payhip, kde platbu a doručenie súboru spracúva Payhip podľa vlastných podmienok.",
   footer_demo="Vzorová verzia stránky – obsah čaká na kontrolu.", footer_shop="Obchod na Payhipe", footer_rights="© Andrej Tymko",
   skip="Preskočiť na obsah", menu="Menu", lang_switch="Jazyk", lang_title="Slovensky",
   formats_note="",
 ),
 "pl": dict(
   lang="pl", locale="pl-PL",
   nav=dict(home="Strona główna", books="Książki", stories="Opowiadania", about="O autorze", contact="Kontakt"),
   site_title="Andrej Tymko", tagline="Opowieści z Tatr, Alp i Himalajów",
   hero_quote="Póki śnisz, żyjesz.", hero_cite="– Andrej Tymko",
   hero_lead="Opowiadania i książki o tatrzańskich nosiczach, gospodarzach schronisk i góralach. Tekst i audio, prosto od autora.",
   hero_cta1="Zobacz opowiadania", hero_cta2="Książki",
   intro_h="Autor", intro_p="W Tatrach odnalazłem siebie. Skalny świat był moim drugim domem. Przez ponad dwanaście lat pracowałem jako tatrzański szerpa.",
   intro_more="Więcej o autorze",
   featured_h="Książki", featured_more="Wszystkie książki",
   grid_h="Opowiadania", grid_all="Wszystkie opowiadania", grid_n=8,
   buy="Kup", buy_text="Tekst", buy_audio="Audio", buy_both="Kup – tekst + audio", buy_audio_only="Kup – audio", buy_text_only="Kup – tekst",
   buy_book="Kup książkę",
   via="Płatność i pobranie plików przez Payhip.", opens_payhip="Payhip otworzy się w nowym oknie.",
   kind=dict(both="Tekst + audio", audio="Audio", text="Tekst", pair="Tekst i audio osobno", book="Książka"),
   details="Szczegóły", back_stories="← Wszystkie opowiadania", back_books="← Wszystkie książki",
   excerpt_h="Fragment tekstu", excerpt_note="Fragment początku polskiego tłumaczenia. Pełnej polskiej wersji jeszcze nie ma w sprzedaży.",
   no_excerpt="Polskie tłumaczenie tego opowiadania nie jest jeszcze dostępne.",
   svk="wersja słowacka", svk_long="wersja słowacka",
   pl_banner="Produkty w sklepie Payhip są na razie dostępne wyłącznie po słowacku. Przyciski zakupu prowadzą do wersji słowackiej.",
   stories_h="Opowiadania", stories_lead="Wszystkie opowiadania, które są obecnie w sklepie na Payhip. Do każdego należy tekst, audio lub jedno i drugie.",
   search="Szukaj opowiadania…", search_label="Szukaj opowiadania", nores="Nic nie znaleziono.",
   books_h="Książki", books_lead="Dwie książki w wersji elektronicznej.",
   about_h="O autorze", about_bio_h="Moje górskie ego w pigułce", about_photo_alt="Andrej Tymko", about_src="Źródło: profil autora w Payhip (tłumaczenie robocze ze słowackiego).",
   contact_h="Kontakt", contact_p="Dane kontaktowe autora zostaną uzupełnione.", contact_todo="DOPLNIŤ: adres e-mail / formularz kontaktowy", contact_shop="Sklep z opowiadaniami znajdziesz w Payhip:",
   imprint_h="Impressum", privacy_h="Polityka prywatności",
   todo="DOPLNIŤ", todo_note="Ta strona jest tekstem zastępczym. Dane prawne nie są wypełnione i muszą zostać uzupełnione przed publikacją.",
   imprint_fields=["Wydawca / autor", "Adres", "IČO / DIČ (jeśli dotyczy)", "Kontaktowy adres e-mail", "Osoba odpowiedzialna za treść"],
   privacy_fields=["Administrator danych i kontakt", "Jakie dane osobowe są przetwarzane (przy płatności przetwarza je Payhip)", "Podstawa prawna i okres przechowywania", "Prawa osoby, której dane dotyczą", "Organ nadzorczy"],
   privacy_fact="Informacje techniczne o tej stronie: strona nie używa plików cookie, narzędzi analitycznych ani reklamowych i nie ładuje zewnętrznych skryptów ani czcionek. Po kliknięciu przycisku „Kup” otwiera się strona Payhip, gdzie płatność i dostarczenie plików obsługuje Payhip zgodnie z własnymi warunkami.",
   footer_demo="Wersja wzorcowa strony – treść czeka na kontrolę.", footer_shop="Sklep na Payhip", footer_rights="© Andrej Tymko",
   skip="Przejdź do treści", menu="Menu", lang_switch="Język", lang_title="Po polsku",
 ),
}

def esc(s): return html.escape(s, quote=True)

# ---------- images ----------
COVER_DIR = ROOT/"assets"/"covers"
def cover_info(cid):
    im = Image.open(COVER_DIR/f"{cid}.webp"); w, h = im.size
    return w, h, ("cover" if w/h >= 1.25 else "contain")

# ---------- Polish excerpts ----------
def pl_excerpt(n, poem=False, maxw=120):
    raw = PL_RAW[str(n)][1]
    parts = raw.split("\n---\n", 1)
    body = parts[1] if len(parts) > 1 else raw
    body = body.replace("\\!", "!").replace("\\.", ".").replace("\\-", "-")
    body = re.sub(r"\n\s*## .*", "", body)  # drop sub headings
    if poem:
        lines = [l.strip() for l in body.strip().split("\n") if l.strip()][:6]
        return ["\n".join(l.rstrip() for l in lines)], True
    paras = [p.strip() for p in re.split(r"\n\s*\n", body.strip()) if p.strip()]
    out, words = [], 0
    for p in paras:
        sentences = re.split(r"(?<=[\.\!\?…”\"])\s+", p)
        cur = []
        for s in sentences:
            wc = len(s.split())
            if words + wc > maxw and words >= 60:
                if cur: out.append(" ".join(cur))
                return out, True
            cur.append(s); words += wc
        out.append(" ".join(cur))
        if words >= 90: return out, (p is not paras[-1])
    return out, False

# ---------- paths ----------
def pdir(lang, key, *extra): return LANG_PREFIX[lang] + PATHS[lang][key] + list(extra)

def rel(frm, to):
    """relative URL from directory-page frm (list) to directory-page to (list)"""
    up = len(frm)
    url = "../" * up + "/".join(to)
    if to: url += "/"
    return url if url else "./"

def asset(frm, name): return "../" * len(frm) + "assets/" + name

# ---------- layout ----------
def layout(lang, here, title, body, other_paths, desc="", extra_head="", body_class="", scripts=""):
    t = T[lang]
    up = len(here)
    def L(key, *extra): return rel(here, pdir(lang, key, *extra))
    nav = "".join(
        f'<li><a href="{L(k)}"{" aria-current=\"page\"" if (pdir(lang,k)==here or (k!="home" and here[:len(pdir(lang,k))]==pdir(lang,k))) else ""}>{esc(t["nav"][k])}</a></li>'
        for k in ["home","books","stories","about","contact"])
    langs = "".join(
        (f'<a class="lang{" is-active" if l==lang else ""}" hreflang="{l}" lang="{l}" href="{rel(here, other_paths[l])}"{" aria-current=\"true\"" if l==lang else ""} title="{esc(LANG_NAME[l])}">{l.upper()}</a>')
        for l in LANGS)
    alts = "".join(f'<link rel="alternate" hreflang="{l}" href="{rel(here, other_paths[l])}">' for l in LANGS)
    alts += f'<link rel="alternate" hreflang="x-default" href="{rel(here, other_paths["sk"])}">'
    banner = f'<div class="notice" role="note">{esc(t["pl_banner"])}</div>' if lang == "pl" else ""
    return f'''<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)} · Andrej Tymko</title>
<meta name="description" content="{esc(desc or t["tagline"])}">
<link rel="icon" href="{asset(here,'favicon.svg')}" type="image/svg+xml">
<link rel="stylesheet" href="{asset(here,'css/style.css')}">
{alts}{extra_head}
</head>
<body class="{body_class}">
<a class="skip" href="#main">{esc(t["skip"])}</a>
<header class="site-header">
  <div class="wrap bar">
    <a class="brand" href="{L('home')}"><svg viewBox="0 0 40 24" width="34" height="20" aria-hidden="true"><path d="M0 24 L13 5 L20 14 L27 2 L40 24 Z" fill="currentColor"/><path d="M27 2 L31 8 L27 7 L24 9 Z" fill="#fff" opacity=".85"/></svg><span>Andrej Tymko</span></a>
    <button class="menu-btn" aria-expanded="false" aria-controls="nav" type="button">{esc(t["menu"])}</button>
    <nav id="nav" class="nav" aria-label="Menu"><ul>{nav}</ul>
      <div class="langs" role="group" aria-label="{esc(t["lang_switch"])}">{langs}</div></nav>
  </div>
</header>
{banner}
<main id="main">
{body}
</main>
<footer class="site-footer">
  <div class="wrap foot">
    <div><strong>Andrej Tymko</strong><br><span class="muted">{esc(t["tagline"])}</span></div>
    <ul class="foot-links">
      <li><a href="{L('imprint')}">{esc(t["imprint_h"])}</a></li>
      <li><a href="{L('privacy')}">{esc(t["privacy_h"])}</a></li>
      <li><a href="{STORE_URL}" rel="noopener" target="_blank">{esc(t["footer_shop"])}</a></li>
    </ul>
    <p class="muted small">{esc(t["footer_rights"])} · {esc(t["footer_demo"])}</p>
  </div>
</footer>
<script src="{asset(here,'js/site.js')}" defer></script>{scripts}
</body></html>
'''

# ---------- components ----------
def buy_buttons(lang, item, size=""):
    t = T[lang]; k = item["kind"]; ids = item["ids"]
    suffix = f' <span class="svk">({t["svk"]})</span>' if lang == "pl" else ""
    def btn(label, pid, price, cls=""):
        return (f'<a class="btn {cls} {size}" href="{PAYHIP}{pid}" target="_blank" rel="noopener" data-payhip="{pid}">'
                f'<span class="lbl">{esc(label)}{suffix}</span><span class="price">{("%.2f" % price).replace(".", ",")}\u00a0€</span></a>')
    price = item.get("price", 1)
    if k == "pair":
        return btn(t["buy_text"], ids["text"], price, "btn-outline") + btn(t["buy_audio"], ids["audio"], price)
    if k == "both": return btn(t["buy_both"], ids["both"], price)
    if k == "audio": return btn(t["buy_audio_only"], ids["audio"], price)
    if k == "text": return btn(t["buy_text_only"], ids["text"], price)
    if k == "book": return btn(t["buy_book"], ids["book"], price)

def title_of(lang, it):
    return (it["title_pl"] if lang == "pl" and it.get("title_pl") else it["title_sk"])

def card(lang, here, it, is_story=True):
    t = T[lang]
    w, h, fit = cover_info(it["cover"])
    detail = rel(here, pdir(lang, "stories" if is_story else "books", it["slug"]))
    title = title_of(lang, it)
    teaser = it["t_pl"] if lang == "pl" else it["t_sk"]
    kind = t["kind"][it["kind"]]
    has_pl = bool(it.get("title_pl"))
    sub = ""
    if lang == "pl" and has_pl and it["title_pl"] != it["title_sk"]:
        sub = f'<p class="orig">{esc(it["title_sk"])}</p>'
    if lang == "sk" and has_pl:
        pass
    search = esc((it["title_sk"] + " " + (it.get("title_pl") or "")).lower())
    return f'''<article class="card" data-search="{search}">
  <a class="card-img {fit}" href="{detail}" tabindex="-1" aria-hidden="true"><img src="{asset(here, 'covers/'+it['cover']+'.webp')}" width="{w}" height="{h}" loading="lazy" alt=""></a>
  <div class="card-body">
    <p class="badge">{esc(kind)}</p>
    <h3><a href="{detail}">{esc(title)}</a></h3>{sub}
    <p class="teaser">{esc(teaser)}</p>
    <div class="buy">{buy_buttons(lang, it)}</div>
    <a class="more" href="{detail}">{esc(t["details"])} →</a>
  </div>
</article>'''

def book_feature(lang, here, it):
    t = T[lang]
    w, h, fit = cover_info(it["cover"])
    detail = rel(here, pdir(lang, "books", it["slug"]))
    teaser = it["t_pl"] if lang == "pl" else it["t_sk"]
    label = it["label_pl"] if lang == "pl" else it["label_sk"]
    return f'''<article class="book">
  <a class="book-img" href="{detail}" tabindex="-1" aria-hidden="true"><img src="{asset(here, 'covers/'+it['cover']+'.webp')}" width="{w}" height="{h}" loading="lazy" alt=""></a>
  <div class="book-body">
    <p class="badge">{esc(label)}</p>
    <h3><a href="{detail}">{esc(title_of(lang, it))}</a></h3>
    <p>{esc(teaser)}</p>
    <div class="buy">{buy_buttons(lang, it)}</div>
    <a class="more" href="{detail}">{esc(t["details"])} →</a>
  </div>
</article>'''

def hero(lang, here):
    t = T[lang]
    return f'''<section class="hero">
  <div class="wrap hero-in">
    <p class="eyebrow">{esc(t["tagline"])}</p>
    <h1>Andrej Tymko</h1>
    <p class="lead">{esc(t["hero_lead"])}</p>
    <blockquote class="hq"><p>„{esc(t["hero_quote"].rstrip("."))}.“</p><footer>{esc(t["hero_cite"])}</footer></blockquote>
    <p class="cta"><a class="btn" href="{rel(here, pdir(lang,'stories'))}">{esc(t["hero_cta1"])}</a> <a class="btn btn-ghost" href="{rel(here, pdir(lang,'books'))}">{esc(t["hero_cta2"])}</a></p>
  </div>
  <svg class="ridge" viewBox="0 0 1440 220" preserveAspectRatio="none" aria-hidden="true">
    <path class="r3" d="M0 220 L0 150 L110 95 L190 130 L300 60 L380 110 L470 80 L560 140 L690 40 L790 105 L880 70 L1000 135 L1120 55 L1230 110 L1330 85 L1440 130 L1440 220 Z"/>
    <path class="r2" d="M0 220 L0 175 L90 140 L210 165 L330 120 L440 160 L560 125 L700 170 L820 130 L950 165 L1080 120 L1200 160 L1320 135 L1440 165 L1440 220 Z"/>
    <path class="r1" d="M0 220 L0 200 L140 182 L300 198 L470 180 L650 200 L820 184 L1000 200 L1180 183 L1440 200 L1440 220 Z"/>
  </svg>
</section>'''

# ---------- pages ----------
def other_map(key, *extra, story_slug=None):
    return {l: pdir(l, key, *extra) for l in LANGS}

def page_home(lang):
    t = T[lang]; here = pdir(lang, "home")
    books = "".join(book_feature(lang, here, b) for b in BOOKS)
    cards = "".join(card(lang, here, s) for s in STORIES[:t["grid_n"]])
    body = hero(lang, here) + f'''
<section class="section intro"><div class="wrap narrow">
  <h2>{esc(t["intro_h"])}</h2>
  <p class="big">{esc(t["intro_p"])}</p>
  <p><a class="more" href="{rel(here, pdir(lang,'about'))}">{esc(t["intro_more"])} →</a></p>
</div></section>
<section class="section"><div class="wrap">
  <div class="sec-head"><h2>{esc(t["featured_h"])}</h2><a class="more" href="{rel(here, pdir(lang,'books'))}">{esc(t["featured_more"])} →</a></div>
  <div class="books">{books}</div>
</div></section>
<section class="section alt"><div class="wrap">
  <div class="sec-head"><h2>{esc(t["grid_h"])}</h2><a class="more" href="{rel(here, pdir(lang,'stories'))}">{esc(t["grid_all"])} →</a></div>
  <div class="grid">{cards}</div>
  <p class="center"><a class="btn btn-outline" href="{rel(here, pdir(lang,'stories'))}">{esc(t["grid_all"])}</a></p>
</div></section>'''
    return here, layout(lang, here, t["site_title"] + " – " + t["tagline"], body, other_map("home"), desc=t["hero_lead"], body_class="home")

def page_books(lang):
    t = T[lang]; here = pdir(lang, "books")
    body = f'''<section class="page-head"><div class="wrap"><h1>{esc(t["books_h"])}</h1><p class="lead">{esc(t["books_lead"])}</p></div></section>
<section class="section"><div class="wrap"><div class="books">{"".join(book_feature(lang, here, b) for b in BOOKS)}</div></div></section>'''
    return here, layout(lang, here, t["books_h"], body, other_map("books"), desc=t["books_lead"])

def page_stories(lang):
    t = T[lang]; here = pdir(lang, "stories")
    cards = "".join(card(lang, here, s) for s in STORIES)
    body = f'''<section class="page-head"><div class="wrap"><h1>{esc(t["stories_h"])}</h1><p class="lead">{esc(t["stories_lead"])}</p>
<label class="search"><span class="sr">{esc(t["search_label"])}</span><input id="q" type="search" placeholder="{esc(t["search"])}" autocomplete="off"></label></div></section>
<section class="section"><div class="wrap"><div class="grid" id="grid">{cards}</div><p id="nores" class="center muted" hidden>{esc(t["nores"])}</p></div></section>'''
    return here, layout(lang, here, t["stories_h"], body, other_map("stories"), desc=t["stories_lead"])

def paras(lst): return "".join(f"<p>{esc(p)}</p>" for p in lst)

def page_story(lang, it):
    t = T[lang]; here = pdir(lang, "stories", it["slug"])
    w, h, fit = cover_info(it["cover"])
    title = title_of(lang, it)
    lead = it["t_pl"] if lang == "pl" else it["t_sk"]
    more = it["d_pl"] if lang == "pl" else it["d_sk"]
    sub = f'<p class="orig">{esc(it["title_sk"])}</p>' if (lang == "pl" and it.get("title_pl") and it["title_pl"] != it["title_sk"]) else ""
    exc_html = ""
    if lang == "sk":
        if it.get("excerpt_sk"):
            ex = it["excerpt_sk"].split("\n\n")
            exc_html = f'<section class="excerpt"><h2>{esc(t["excerpt_h"])}</h2><div class="quote">{"".join("<p>"+esc(p)+"</p>" for p in ex)}<p class="ell">…</p></div><p class="muted small">{esc(t["excerpt_note"])}</p></section>'
    else:
        if it.get("pl_n"):
            ps, cut = pl_excerpt(it["pl_n"], poem=it.get("poem", False))
            inner = "".join(("<p class=\"verse\">" + esc(p).replace("\n", "<br>") + "</p>") if it.get("poem") else f"<p>{esc(p)}</p>" for p in ps)
            exc_html = f'<section class="excerpt"><h2>{esc(t["excerpt_h"])}</h2><div class="quote">{inner}{"<p class=\"ell\">…</p>" if cut else ""}</div><p class="muted small">{esc(t["excerpt_note"])}</p></section>'
        else:
            exc_html = f'<section class="excerpt"><h2>{esc(t["excerpt_h"])}</h2><p class="muted">{esc(t["no_excerpt"])}</p></section>'
    body = f'''<article class="detail"><div class="wrap">
  <p class="crumb"><a href="{rel(here, pdir(lang,'stories'))}">{esc(t["back_stories"])}</a></p>
  <div class="detail-grid">
    <figure class="detail-cover {fit}"><img src="{asset(here, 'covers/'+it['cover']+'.webp')}" width="{w}" height="{h}" alt="{esc(title)}"></figure>
    <div class="detail-main">
      <p class="badge">{esc(t["kind"][it["kind"]])}</p>
      <h1>{esc(title)}</h1>{sub}
      <p class="lead">{esc(lead)}</p>
      {paras(more)}
      <div class="buy buy-lg">{buy_buttons(lang, it, "btn-lg")}</div>
      <p class="muted small">{esc(t["via"])} {esc(t["opens_payhip"])}</p>
    </div>
  </div>
  {exc_html}
</div></article>'''
    return here, layout(lang, here, title, body, other_map("stories", it["slug"]), desc=lead)

def page_book(lang, it):
    t = T[lang]; here = pdir(lang, "books", it["slug"])
    w, h, fit = cover_info(it["cover"])
    title = title_of(lang, it)
    lead = it["t_pl"] if lang == "pl" else it["t_sk"]
    more = it["d_pl"] if lang == "pl" else it["d_sk"]
    label = it["label_pl"] if lang == "pl" else it["label_sk"]
    body = f'''<article class="detail"><div class="wrap">
  <p class="crumb"><a href="{rel(here, pdir(lang,'books'))}">{esc(t["back_books"])}</a></p>
  <div class="detail-grid">
    <figure class="detail-cover {fit}"><img src="{asset(here, 'covers/'+it['cover']+'.webp')}" width="{w}" height="{h}" alt="{esc(title)}"></figure>
    <div class="detail-main">
      <p class="badge">{esc(label)}</p>
      <h1>{esc(title)}</h1>
      <p class="lead">{esc(lead)}</p>
      {paras(more)}
      <div class="buy buy-lg">{buy_buttons(lang, it, "btn-lg")}</div>
      <p class="muted small">{esc(t["via"])} {esc(t["opens_payhip"])}</p>
    </div>
  </div>
</div></article>'''
    return here, layout(lang, here, title, body, other_map("books", it["slug"]), desc=lead)

def page_about(lang):
    t = T[lang]; here = pdir(lang, "about")
    bio = BIO_PL if lang == "pl" else BIO_SK
    end = BIO_PL_END if lang == "pl" else BIO_SK_END
    body = f'''<section class="page-head"><div class="wrap"><h1>{esc(t["about_h"])}</h1></div></section>
<section class="section"><div class="wrap about">
  <figure class="portrait"><img src="{asset(here,'covers/STORE.webp')}" width="{cover_info('STORE')[0]}" height="{cover_info('STORE')[1]}" alt="{esc(t["about_photo_alt"])}"></figure>
  <div class="prose">
    <h2>{esc(t["about_bio_h"])}</h2>
    {paras(bio)}
    <p class="pull">{esc(end[0])}</p><p>{esc(end[1])}</p>
    <p class="muted small">{esc(t["about_src"])}</p>
  </div></div></section>'''
    return here, layout(lang, here, t["about_h"], body, other_map("about"), desc=bio[0])

def page_contact(lang):
    t = T[lang]; here = pdir(lang, "contact")
    body = f'''<section class="page-head"><div class="wrap"><h1>{esc(t["contact_h"])}</h1></div></section>
<section class="section"><div class="wrap narrow prose">
  <p>{esc(t["contact_p"])}</p>
  <p class="todo-box"><span class="todo">{esc(t["todo"])}</span> {esc(t["contact_todo"].replace("DOPLNIŤ: ",""))}</p>
  <p>{esc(t["contact_shop"])} <a href="{STORE_URL}" target="_blank" rel="noopener">payhip.com/AndrejTymko</a></p>
</div></section>'''
    return here, layout(lang, here, t["contact_h"], body, other_map("contact"))

def page_legal(lang, key):
    t = T[lang]; here = pdir(lang, key)
    head = t["imprint_h"] if key == "imprint" else t["privacy_h"]
    fields = t["imprint_fields"] if key == "imprint" else t["privacy_fields"]
    items = "".join(f'<li><strong>{esc(f)}:</strong> <span class="todo">{esc(t["todo"])}</span></li>' for f in fields)
    fact = f'<p>{esc(t["privacy_fact"])}</p>' if key == "privacy" else ""
    body = f'''<section class="page-head"><div class="wrap"><h1>{esc(head)}</h1></div></section>
<section class="section"><div class="wrap narrow prose">
  <p class="notice-inline"><span class="todo">{esc(t["todo"])}</span> {esc(t["todo_note"])}</p>
  <ul class="fields">{items}</ul>
  {fact}
</div></section>'''
    return here, layout(lang, here, head, body, other_map(key), desc=t["todo_note"])

def write(here, content):
    d = ROOT.joinpath(*here); d.mkdir(parents=True, exist_ok=True)
    (d/"index.html").write_text(content, encoding="utf-8")

def main():
    pages = []
    for lang in LANGS:
        pages += [page_home(lang), page_books(lang), page_stories(lang), page_about(lang), page_contact(lang), page_legal(lang, "imprint"), page_legal(lang, "privacy")]
        pages += [page_story(lang, s) for s in STORIES]
        pages += [page_book(lang, b) for b in BOOKS]
    # 404 page (relative-safe, links to both languages)
    for here, content in pages: write(here, content)
    ROOT.joinpath(".nojekyll").write_text("")
    # 404.html at root (GitHub Pages)
    (ROOT/"404.html").write_text('''<!doctype html><html lang="sk"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>404 · Andrej Tymko</title>
<style>body{font-family:Georgia,serif;max-width:32rem;margin:15vh auto;padding:0 1rem;color:#1f2d3a}a{color:#2c5d63}</style></head><body>
<h1>404</h1><p>Stránka sa nenašla. / Nie znaleziono strony.</p><p><a href="./">Domov</a> · <a href="pl/">Polski</a></p></body></html>''', encoding="utf-8")
    print(len(pages), "pages")

if __name__ == "__main__":
    main()
