# Skripta

Souvislý výklad celé látky předmětu **BI-OSY (Operační systémy)**. Vzniklo přepracováním
12 přednášek do **7 tematických kapitol** — každá kapitola se dá přečíst samostatně
a obsahuje diagramy a obrázky převzaté ze slidů přednášek.

!!! tip "Jak skripta číst"
    Kapitoly na sebe navazují, takže při prvním studiu postupuj odshora dolů.
    Každá kapitola končí oddílem **Shrnutí** (rychlé zopakování) a **Klíčové pojmy**
    (definice, které najdeš souhrnně i v [Rozcestníku pojmů](../rozcestnik.md)).

## Kapitoly

| # | Kapitola | Obsah |
|---|----------|-------|
| 01 | [Úvod do operačních systémů](01-uvod.md) | Model výpočetního systému, HW, role OS, systémová volání |
| 02 | [Procesy a vlákna](02-procesy-vlakna.md) | Program/proces/vlákno, `fork`/`exec`/`wait`, stavy, kritické sekce |
| 03 | [Synchronizace a meziprocesová komunikace](03-synchronizace.md) | Kritická sekce, zámky, semafory, podmíněné proměnné, klasické úlohy |
| 04 | [Uváznutí (deadlock)](04-deadlock.md) | Coffmanovy podmínky, alokační graf, Bankéřův algoritmus |
| 05 | [Plánování procesů a vláken](05-planovani.md) | PCB/TCB, Round-robin, prioritní plánování, CFS, FCFS |
| 06 | [Správa paměti](06-pamet.md) | Hierarchie pamětí, virtuální paměť, stránkování, náhrada stránek |
| 07 | [Datová úložiště a souborové systémy](07-souborove-systemy.md) | HDD/SSD, RAID, FAT, UFS, VFS, žurnálování, moderní FS |

## Mapování na přednášky

| Kapitola | Přednášky |
|----------|-----------|
| 01 Úvod | P01 Introduction |
| 02 Procesy a vlákna | P02 Threads |
| 03 Synchronizace | P03 IPC tools + P04 IPC problems |
| 04 Uváznutí | P05 Deadlock |
| 05 Plánování | P06 Scheduling |
| 06 Správa paměti | P07 Memory Introduction + P08 Memory VM + P09 Memory PRA |
| 07 Disky a FS | P10 Data storage + P11 FS Disk + P12 FS OS |

## Kam dál

- Procvičit látku na zkouškových úlohách → [Testové otázky](../otazky/index.md)
- Nevíš, kde začít a jak si rozvrhnout učení → [Učební pomocník](../pomocnik.md)
- Hledáš konkrétní definici → [Rozcestník pojmů](../rozcestnik.md)
