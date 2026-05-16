# Učební pomocník

Tahle stránka tě provede přípravou na zkoušku z **BI-OSY** — od prvního čtení skript
až po poslední opakování večer před termínem. Není to další výkladová stránka:
je to **plán a návod**, jak ostatní tři části wiki používat efektivně.

!!! abstract "Tři části wiki a jak je propojit"
    - 📚 **[Skripta](skripta/index.md)** — odsud se učíš novou látku.
    - 🧭 **[Rozcestník pojmů](rozcestnik.md)** — sem se vracíš ověřit, že pojmy znáš.
    - ❓ **[Testové otázky](otazky/index.md)** — tady si ověříš, že látku **umíš použít**.

??? abstract "Obsah stránky"

    [TOC]

## Jak vypadá zkouška

Zkouška BI-OSY má **dvě části** a obě je potřeba zvládnout:

| Část | Co to je | Jak se připravit |
|------|----------|------------------|
| **Teoretický test** | Sada tvrzení, u každého rozhoduješ **pravda / nepravda** | [Teoretické otázky](otazky/teorie-truefalse.md) |
| **Praktické příklady** | 6–7 výpočetních úloh, dohromady zhruba **40 bodů** | [Praktické příklady](otazky/prakticke/index.md) |

Praktická část se losuje z pevného poolu úloh. **Konkrétní čísla se mění, ale typy úloh
zůstávají stejné** napříč termíny 2010–2025. Když zvládneš všech 7 typů, jsi připraven.

!!! warning "Binární jednotky"
    Skoro každá početní úloha pracuje s **binárními** prefixy:
    `1 KiB = 1024 B`, `1 MiB = 2^20 B`, `1 GiB = 2^30 B`, `1 TiB = 2^40 B`.
    Pozor: `1 MB ≠ 1 MiB`. Výsledky v MiB se zaokrouhlují **nahoru**: `ceil(byty / 1048576)`.

## Doporučený postup učení

Osvědčený cyklus — projdi ho pro každou kapitolu zvlášť, kapitoly ber v pořadí 01 → 07
(navazují na sebe):

1. **Přečti kapitolu skript.** Nepřeskakuj obrázky a admonice `!!! tip "U zkoušky"` — ty ukazují, co je důležité.
2. **Projdi `## Shrnutí`** na konci kapitoly. Co ti není jasné, dočti znovu.
3. **Otevři [Rozcestník pojmů](rozcestnik.md)** a u dané sekce si projeď pojmy. Cíl: ke každému pojmu řekneš definici vlastními slovy.
4. **Vyřeš odpovídající typ úlohy** v [Praktických příkladech](otazky/prakticke/index.md) — nejdřív zkus sám, teprve pak rozbal řešení.
5. **Projdi T/F otázky** daného tématu v [Teoretických otázkách](otazky/teorie-truefalse.md).

Když takhle projdeš všech 7 kapitol, udělej **závěrečné kolo**: namíchané T/F otázky
+ jeden příklad od každého typu na čas.

!!! tip "Aktivní vybavování"
    Nejúčinnější není číst, ale **vybavovat si**. Po přečtení sekce zavři skripta
    a zkus zpaměti zopakovat hlavní myšlenky. Rozbalovací bloky `??? ...` v testových
    otázkách jsou k tomu navržené — odpověď uvidíš, až ji opravdu chceš vidět.

## Studijní plán podle času

=== "Mám 2 týdny"

    Komfortní tempo, zvládneš všechno do hloubky.

    | Dny | Náplň |
    |-----|-------|
    | 1–2 | Kap. 01 Úvod + 02 Procesy a vlákna |
    | 3–4 | Kap. 03 Synchronizace |
    | 5–6 | Kap. 04 Deadlock + 05 Plánování |
    | 7–9 | Kap. 06 Správa paměti (nejobsáhlejší) |
    | 10–11 | Kap. 07 Disky a souborové systémy |
    | 12–13 | Všechny typy praktických úloh na čas |
    | 14 | T/F otázky + Rozcestník pojmů, lehké opakování |

=== "Mám 1 týden"

    Rychlejší tempo, kombinuj čtení s procvičováním.

    | Dny | Náplň |
    |-----|-------|
    | 1 | Kap. 01 + 02 + jejich úlohy |
    | 2 | Kap. 03 + úlohy na synchronizaci |
    | 3 | Kap. 04 + 05 + Bankéř a plánování |
    | 4 | Kap. 06 + úlohy na stránkování a náhradu stránek |
    | 5 | Kap. 07 + úlohy na RAID a souborové systémy |
    | 6 | Všechny T/F otázky, Rozcestník pojmů |
    | 7 | Praktické úlohy namíchaně na čas |

=== "Mám 3 dny"

    Priorita = body. Zaměř se na úlohy, které se objevují téměř vždy.

    | Den | Náplň |
    |-----|-------|
    | 1 | **Deadlock/Bankéř**, **Plánování**, **RAID** — projdi skripta jen zběžně, hlavně řeš úlohy |
    | 2 | **Stránkování**, **Souborové systémy (UFS/FAT)**, **Procesy/fork** |
    | 3 | **Synchronizace** (multichoice), **T/F otázky**, vzorce z Rozcestníku |

=== "Noc před zkouškou"

    Žádné nové učení — jen vyladění toho, co umíš.

    - Projdi sekci **Vzorce na jednom místě** v [Rozcestníku pojmů](rozcestnik.md).
    - Projeď **postupy řešení** u každého typu v [Praktických příkladech](otazky/prakticke/index.md) (zadání + postup, řešení jen zkontroluj).
    - Přečti **T/F otázky** — je jich hodně a jsou rychlé body.
    - Vyspi se. Unavený mozek počítá chyby.

## Co se učit u každé kapitoly

| Kapitola | Na co se zaměřit | Procvič si |
|----------|------------------|------------|
| [01 Úvod](skripta/01-uvod.md) | Role OS, systémová volání, uživatelský vs. privilegovaný režim, přerušení | T/F: OS obecně |
| [02 Procesy a vlákna](skripta/02-procesy-vlakna.md) | `fork`/`exec`/`wait`, stavy vlákna, zombie/sirotek, kritická sekce | Úloha: Procesy a vlákna |
| [03 Synchronizace](skripta/03-synchronizace.md) | Semafory vs. mutex vs. podmíněná proměnná, sestavení semaforu, race/deadlock/livelock | Úloha: Synchronizace |
| [04 Deadlock](skripta/04-deadlock.md) | **Coffmanovy podmínky**, **Bankéřův algoritmus**, alokační graf | Úloha: Deadlock |
| [05 Plánování](skripta/05-planovani.md) | Round-robin, **statická priorita** (výpočet času běhu), CFS | Úloha: Plánování |
| [06 Správa paměti](skripta/06-pamet.md) | Stránkovací tabulky (klasická/invertovaná/TLB), překlad adres, **algoritmy náhrady stránek** | Úloha: Správa paměti |
| [07 Disky a FS](skripta/07-souborove-systemy.md) | **RAID** (kapacita, rychlost, spolehlivost), disk I/O, **UFS/FAT** vzorce, FS operace | Úlohy: Disky a RAID, Souborové systémy |

## Mapa: typ úlohy → kde se to naučit

Praktická část se skládá z opakujících se typů úloh. Tahle tabulka říká, kde každý typ
nastudovat a kde procvičit:

| Typ úlohy | Skripta | Testové otázky |
|-----------|---------|----------------|
| Procesy, `fork`-strom, paměť procesu | [02 Procesy a vlákna](skripta/02-procesy-vlakna.md) | [Procesy a vlákna](otazky/prakticke/01-procesy-vlakna.md) |
| Synchronizace, multichoice race/deadlock | [03 Synchronizace](skripta/03-synchronizace.md) | [Synchronizace](otazky/prakticke/02-synchronizace.md) |
| Bankéřův algoritmus | [04 Deadlock](skripta/04-deadlock.md) | [Deadlock](otazky/prakticke/03-deadlock.md) |
| Plánování se statickou prioritou | [05 Plánování](skripta/05-planovani.md) | [Plánování procesů](otazky/prakticke/04-planovani.md) |
| Stránkování, náhrada stránek | [06 Správa paměti](skripta/06-pamet.md) | [Správa paměti](otazky/prakticke/05-pamet.md) |
| RAID + spolehlivost, disk I/O | [07 Disky a FS](skripta/07-souborove-systemy.md) | [Disky a RAID](otazky/prakticke/06-disky-raid.md) |
| UFS/FAT, FS operace (`cp`/`mv`/`ln`/`rm`) | [07 Disky a FS](skripta/07-souborove-systemy.md) | [Souborové systémy](otazky/prakticke/07-souborove-systemy.md) |

## Strategie u zkoušky

Pořadí, ve kterém úlohy řešíš, rozhoduje o počtu bodů. Nezačínej od první úlohy —
začni od těch, kde získáš body nejrychleji.

!!! success "Pořadí řešení"
    1. **Nejdřív rychlé body** — T/F otázky a krátké vzorcové úlohy (max. velikost souboru, velikost FAT tabulky, kapacita RAID). Hotové za 1–2 minuty.
    2. **Pak jisté úlohy** — Bankéř a Plánování. Pokud znáš postup, jsou to mechanické výpočty za hodně bodů.
    3. **Středně náročné** — stránkování (multichoice), TSL kód, fork-strom.
    4. **Nakonec časově náročné** — FS operace přes hranice systému, dlouhé sekvence náhrady stránek, RAID se všemi podotázkami.

### Hierarchie obtížnosti

??? note "Snadné (1–2 minuty)"
    - Maximální velikost souboru v UFS / FAT (dosadit do vzorce)
    - Velikost FAT tabulky
    - Bitmapa vs. zřetězený seznam volných bloků (jednoduchá nerovnost)
    - T/F teorie — pokud látku znáš

??? note "Střední (~5 minut)"
    - Fork-strom s `&&` / `||`
    - Stránkování — multichoice
    - TSL / XCHG kód
    - Sestavení semaforu z mutexů a podmíněné proměnné

??? note "Náročné (10–15 minut)"
    - Fork-strom s `execlp` + `wait` + iterací
    - Bankéř s 5 procesy, včetně ověření Coffmanových podmínek
    - Plánování s background load a více úrovněmi priorit
    - Náhrada stránek (LRU/Clock/NRU) na dlouhé referenční sekvenci
    - RAID — všech 6 podotázek včetně spolehlivosti
    - FS operace `mv` přes hranice souborových systémů s velkým souborem

!!! tip "Drobné taktiky"
    - **Bankéř a Plánování patří k sobě** — oba jsou jen mechanický postup. Naučíš-li se jeden, máš skoro i druhý.
    - **Stránkování multichoice** = hodně bodů za málo času, nevynechávej ho.
    - **RAID** — nauč se sekvenci vzorců pro každý typ, ne výsledky.
    - **FS operace** odlož na konec, snadno na nich utopíš čas.
    - Píšeš-li mezivýpočty, **piš je čitelně** — za správný postup s drobnou číselnou chybou bývají dílčí body.

## Kontrolní seznam připravenosti

Než půjdeš na zkoušku, měl bys umět odpovědět **ano** u každého bodu. Když ne, klikni
do skript a dostuduj.

- [ ] Vím, co vrací `fork()` v rodiči a v potomkovi a co dělá `execve()` a `wait()`. → [02](skripta/02-procesy-vlakna.md)
- [ ] Spočítám počet procesů ve fork-stromu a paměť procesu v MiB. → [02](skripta/02-procesy-vlakna.md)
- [ ] Vyjmenuji stavy vlákna a přechody mezi nimi. → [02](skripta/02-procesy-vlakna.md)
- [ ] Vysvětlím rozdíl mezi mutexem, semaforem a podmíněnou proměnnou. → [03](skripta/03-synchronizace.md)
- [ ] Poznám v kódu race condition, deadlock, livelock a aktivní čekání. → [03](skripta/03-synchronizace.md)
- [ ] Vyjmenuji **4 Coffmanovy podmínky** a vím, že musí platit všechny. → [04](skripta/04-deadlock.md)
- [ ] Projdu **Bankéřův algoritmus** a najdu bezpečnou posloupnost. → [04](skripta/04-deadlock.md)
- [ ] Spočítám čas běhu procesů při plánování se statickou prioritou. → [05](skripta/05-planovani.md)
- [ ] Vím, kolik řádků má klasická, invertovaná a TLB tabulka a co je v každé. → [06](skripta/06-pamet.md)
- [ ] Přeložím virtuální adresu na fyzickou přes stránkovací tabulku. → [06](skripta/06-pamet.md)
- [ ] Aplikuji algoritmy náhrady stránek (FIFO, LRU, Clock, NRU, Optimální). → [06](skripta/06-pamet.md)
- [ ] Spočítám kapacitu, rychlost a spolehlivost pro RAID 0/1/5/6/10. → [07](skripta/07-souborove-systemy.md)
- [ ] Spočítám max. velikost souboru v UFS i ve FAT. → [07](skripta/07-souborove-systemy.md)
- [ ] Určím počet čtení/zápisů i-nodů a bloků u operací `cp`/`mv`/`ln`/`rm`. → [07](skripta/07-souborove-systemy.md)

Když máš zaškrtnuto všechno, jsi připraven. Hodně štěstí u zkoušky! 🍀
