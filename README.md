# 📘 BI-OSY Wiki — Operační systémy

Studijní wiki k předmětu **BI-OSY (Operační systémy)** na FIT ČVUT. Celá látka,
pojmy, řešené zkouškové úlohy a studijní plán na jednom přehledném místě.

> ### 🌐 Otevřít online: **<https://martulens.github.io/osyWiki/>**
>
> Stačí kliknout — **žádné klonování, žádná instalace**. Funguje vyhledávání,
> tmavý režim i prohlížení na mobilu.
>
> *(Odkaz začne fungovat po prvním nasazení — viz sekce **Nasazení na web** níže.)*

## 📑 Co tu najdeš

| Sekce | Obsah |
|-------|-------|
| 📚 **Skripta** | Celá látka předmětu přepracovaná z 12 přednášek do 7 tematických kapitol, včetně diagramů a obrázků. |
| 🧭 **Rozcestník pojmů** | Rejstřík pojmů, definic a vzorců s odkazy přímo do skript. |
| ❓ **Testové otázky** | Praktické příklady s postupy řešení a teoretické pravda/nepravda otázky. |
| 📒 **Sbírka řešených úloh** | Přepis studentské sbírky „Ivetčina kuchařka". |
| 🎓 **Učební pomocník** | Doporučený studijní plán, harmonogram a kontrolní seznam před zkouškou. |

## 👀 Prohlížení

**Online (doporučeno):** otevři <https://martulens.github.io/osyWiki/>. Nic se
nestahuje, nic se neinstaluje.

**Lokálně** — jen pokud chceš obsah upravovat:

```bash
git clone https://github.com/Martulens/osyWiki.git
cd osyWiki
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
mkdocs serve
```

Wiki pak poběží na <http://127.0.0.1:8000/> a po každé úpravě se sama obnoví.

## 🚀 Nasazení na web

Wiki se hostuje **zdarma** přes GitHub Pages. Repozitář musí být **veřejný**
(Pages na privátních repozitářích vyžadují placený účet).

### Automaticky — doporučeno

V repozitáři je workflow [`.github/workflows/deploy.yml`](.github/workflows/deploy.yml).
Při každém pushi do větve `master` se wiki sestaví a publikuje. Stačí jednorázově:

1. **Settings → Pages → Build and deployment → Source: `GitHub Actions`**
2. Pushnout do `master` (nebo workflow spustit ručně přes **Actions → Deploy wiki → Run workflow**).

Za chvíli je wiki živá na `https://<účet>.github.io/<repo>/`.

### Ručně

```bash
mkdocs gh-deploy
```

Sestaví wiki a pushne ji do větve `gh-pages`; tu pak v **Settings → Pages**
nastav jako zdroj.

> 💡 Pokud repozitář nepojmenuješ `osyWiki`, uprav `site_url` v `mkdocs.yml`.

## 🗂️ Struktura repozitáře

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

## 🛠️ Postaveno na

[MkDocs](https://www.mkdocs.org/) + [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/).

## 🙏 Poděkování

Sekce *Sbírka řešených úloh* obsahuje přepis studentské sbírky „Ivetčina kuchařka
— Sbírka řešených úloh z BI-OSY", jejíž autorkou je **Iveta**. Děkujeme.

---

*Hodně štěstí u zkoušky! 🍀*
