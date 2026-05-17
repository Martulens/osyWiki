# BI-OSY Wiki — Operační systémy

[![Deploy wiki](https://github.com/Martulens/osyWiki/actions/workflows/deploy.yml/badge.svg)](https://github.com/Martulens/osyWiki/actions/workflows/deploy.yml)

Studijní wiki k předmětu **BI-OSY (Operační systémy)** na FIT ČVUT.
Celá látka, pojmy, řešené zkouškové úlohy a studijní plán přehledně na jednom místě.

## Otevřít wiki

> ### **<https://martulens.github.io/osyWiki/>**

## Co tu najdeš

| Sekce | Obsah |
|-------|-------|
| 📚 **Skripta** | Celá látka předmětu přepracovaná z 12 přednášek do 7 tematických kapitol, včetně diagramů a obrázků. |
| 🧭 **Rozcestník pojmů** | Rejstřík pojmů, definic a vzorců s odkazy přímo do skript. |
| ❓ **Testové otázky** | Praktické příklady s postupy řešení a teoretické pravda/nepravda otázky. |
| 📒 **Sbírka řešených úloh** | Přepis studentské sbírky „Ivetčina kuchařka". |
| 🎓 **Učební pomocník** | Doporučený studijní plán, harmonogram a kontrolní seznam před zkouškou. |

## Jak wiki používat

- **Hledání** — lupa v horní liště nebo klávesa <kbd>/</kbd>; prohledá celou wiki.
- **Tmavý / světlý režim** — přepínač v horní liště.
- **Mobil** — wiki je plně responzivní, funguje i na telefonu.

## Spuštění lokálně (nepovinné)

Jen pokud chceš obsah **upravovat** nebo si ho prohlížet offline:

```bash
git clone https://github.com/Martulens/osyWiki.git
cd osyWiki
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
mkdocs serve
```

Wiki pak běží na <http://127.0.0.1:8000/> a po každé úpravě se sama obnoví.

## Přispívání

Našel jsi chybu nebo chceš něco doplnit? Uprav příslušný soubor v `wiki/`
a pošli pull request, nebo [založ issue](https://github.com/Martulens/osyWiki/issues).
Obsah je obyčejný Markdown.

## Struktura repozitáře

```text
wiki/                        zdrojový obsah (Markdown) — docs_dir pro MkDocs
  index.md                   úvodní rozcestník
  skripta/                   7 kapitol skript + obrázky
  otazky/                    praktické příklady a teoretické otázky
  sbirka/                    přepis Sbírky řešených úloh
  rozcestnik.md              rejstřík pojmů
  pomocnik.md                učební pomocník
mkdocs.yml                   konfigurace MkDocs Material
requirements.txt             Python závislosti
.github/workflows/deploy.yml automatické nasazení na GitHub Pages
```

## Postaveno na

[MkDocs](https://www.mkdocs.org/) + [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/).

## Poděkování

Sekce *Sbírka řešených úloh* obsahuje přepis studentské sbírky „Ivetčina kuchařka
— Sbírka řešených úloh z BI-OSY", jejíž autorkou je **Iveta**. Děkujeme.

---

*Hodně štěstí u zkoušky! 🍀*
