# BI-OSY Wiki — Operační systémy

Studijní wiki k předmětu **BI-OSY (Operační systémy)** na FIT ČVUT, postavená nad
[MkDocs Material](https://squidfunk.github.io/mkdocs-material/). Vznikla jako pomůcka
pro přípravu na zkoušku.

## Obsah

- **Skripta** — látka celého předmětu přepracovaná z přednášek do 7 tematických
  kapitol, včetně diagramů a obrázků.
- **Rozcestník pojmů** — souhrnný rejstřík pojmů, definic a vzorců s odkazy do skript.
- **Testové otázky** — praktické příklady (postupy řešení) a teoretické
  pravda/nepravda otázky, vše s řešením.
- **Sbírka řešených úloh** — přepis studentské sbírky „Ivetčina kuchařka".
- **Učební pomocník** — doporučený studijní plán a kontrolní seznam.

## Lokální spuštění

```bash
python3 -m venv venv
./venv/bin/pip install -r requirements.txt
./venv/bin/mkdocs serve
```

Wiki bude dostupná na `http://127.0.0.1:8000/`.

Statické sestavení webu: `./venv/bin/mkdocs build` (výstup ve složce `site/`).

## Struktura

- `wiki/` — zdrojové markdown soubory (MkDocs `docs_dir`).
- `mkdocs.yml` — konfigurace MkDocs Material.
- `requirements.txt` — Python závislosti.

## Poděkování

Sekce *Sbírka řešených úloh* obsahuje přepis studentské sbírky „Ivetčina kuchařka
— Sbírka řešených úloh z BI-OSY", jejíž autorkou je **Iveta**. Děkujeme.
