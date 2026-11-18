# andrejtymko-site (vzorová verzia / wersja wzorcowa)

Statická stránka bez build kroku: čisté HTML + CSS + malý JS. Pripravená pre GitHub Pages
(`https://<user>.github.io/<repo>/`) – všetky odkazy sú relatívne. Bez cookies, bez trackerov, bez externých písiem a skriptov.

## Štruktúra
- `/` – slovenčina (predvolená), `/pl/` – poľština. Prepínač jazyka je v hlavičke.
- `/poviedky/`, `/poviedky/<slug>/`, `/knihy/`, `/knihy/<slug>/`, `/o-autorovi/`, `/kontakt/`, `/impressum/`, `/ochrana-sukromia/`
- `/pl/opowiadania/`, `/pl/opowiadania/<slug>/`, `/pl/ksiazki/`, `/pl/o-autorze/`, `/pl/kontakt/`, `/pl/impressum/`, `/pl/polityka-prywatnosci/`
- `assets/` – CSS, JS, obálky (stiahnuté z Payhipu, zmenšené na WebP).

## Tlačidlá „Kúpiť“
Obyčajné odkazy na `https://payhip.com/b/<ID>` (otvoria sa v novom okne). Žiadny externý skript sa nenačítava.
Poľské tlačidlá sú označené „wersja słowacka“, kým na Payhipe nie sú poľské produkty.

## Úprava obsahu / pridanie jazyka (/de/, /en/)
Obsah je v `_tools/data.py`, šablóny v `_tools/build.py`. Po zmene spustite `python3 _tools/build.py` (potrebuje Pillow) –
vygeneruje sa čisté HTML do koreňa. Pre nemčinu/angličtinu: pridať jazyk do `LANGS`, `LANG_PREFIX`, `PATHS`, `T`
a polia `t_de`/`d_de` v `data.py`. Pre GitHub Pages netreba nič ďalšie (`.nojekyll` je pribalený, bez CNAME – doménu pripojíme neskôr).

## Zástupné texty
Impressum, ochrana súkromia a kontakt sú označené **DOPLNIŤ** – právne údaje nie sú vymyslené.
`_tools/pl_raw.json` obsahuje len začiatky poľských prekladov (na ukážky), nie celé texty.
