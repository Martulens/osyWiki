# Teoretické otázky (pravda / nepravda)

Teoretická část zkoušky BI-OSY je test tvrzení, u kterých student rozhoduje **PRAVDA / NEPRAVDA**, případně krátké teoretické otázky s výběrem jedné správné možnosti. Na ProgTestu se generuje náhodný výběr otázek z poolu, takže se vyplatí projít všechny typy.

!!! tip "Jak stránku používat"
    1. Přečti si tvrzení / otázku.
    2. Sám se rozhodni, zda je **PRAVDA** nebo **NEPRAVDA** (případně urči správnou možnost).
    3. Rozbal blok **Odpověď** a porovnej se zdůvodněním.

    Tvrzení jsou seskupena podle kapitol skript a **deduplikována** — ekvivalentní tvrzení z různých termínů jsou uvedena jen jednou.

---

??? abstract "Obsah stránky"

    [TOC]

## Operační systémy obecně

Tvrzení o jádru, systémových voláních, režimech CPU a architektuře počítače.

1. Standardní knihovna C je součástí operačního systému.

    ??? success "Odpověď"
        **NEPRAVDA** — standardní knihovna C není součástí OS; přes ABI (Application Binary Interface) pouze zprostředkuje aplikaci přístup ke službám jádra (systémovým voláním).

2. Procesor po resetu začíná vykonávat instrukce v user módu a do kernel módu se musí později sám přepnout.

    ??? success "Odpověď"
        **NEPRAVDA** — po resetu procesor startuje v privilegovaném (kernel/supervisor) režimu, aby mohl provést inicializaci systému.

3. Procesor může odmítnout požadavek na přístup k I/O zařízení, pokud není v privilegovaném režimu — v tom případě vyvolá výjimku.

    ??? success "Odpověď"
        **PRAVDA** — privilegované instrukce (přístup k I/O, správa přerušení apod.) lze provést jen v kernel módu; pokus v user módu vede k výjimce.

4. Přetečení časovače je jedním ze zdrojů vnějšího přerušení.

    ??? success "Odpověď"
        **PRAVDA** — časovač je hardwarové zařízení mimo CPU a jeho přetečení generuje vnější (hardwarové) přerušení, na kterém stojí mj. plánování procesů.

5. Vyberte správné tvrzení: V jakém režimu běží jádro (kernel) operačního systému?

    ??? success "Odpověď"
        Správně: **„Kernel běží typicky v režimu supervisor.“** — Nepravdivé jsou varianty tvrdící, že kernel běží v user módu, že moduly/ovladače běží jen v user módu nebo že ve virtuálním stroji běží jen v user módu.

6. Vyberte správné tvrzení: V jakém režimu běží uživatelský proces?

    ??? success "Odpověď"
        Správně: **„Uživatelský proces běží typicky v režimu user.“** — Nepravdivé jsou varianty „pokud běží jako root, běží v supervisor“ nebo „v supervisor“; spuštění jako root nemění režim CPU, mění jen oprávnění v rámci OS.

7. Které z následujících instrukcí jsou na procesoru x86 dostupné v režimu user: `LIDT`, `CLI`, `OUT dx, eax`, `MOV ax, bx`, `SHL eax, 3`?

    ??? success "Odpověď"
        Dostupné v user módu: **`MOV ax, bx`** a **`SHL eax, 3`** (běžné výpočetní instrukce). Privilegované (jen kernel mód): `LIDT` (načtení tabulky přerušení), `CLI` (zákaz přerušení), `OUT` (zápis na periferii).

8. Moderní víceprocesorový počítač (např. notebook s vícejádrovým CPU) je architektury MIMD.

    ??? success "Odpověď"
        **PRAVDA** — víceprocesorové/vícejádrové počítače vykonávají více instrukčních proudů nad více datovými proudy, tedy MIMD.

9. Operační systém Windows na běžném vícejádrovém počítači podporuje SMP (symetrický multiprocesoring).

    ??? success "Odpověď"
        **PRAVDA** — moderní OS podporují SMP, kde jsou si všechna jádra/procesory rovnocenná.

10. Plánování procesů a přepínání kontextu řídí část jádra, která reaguje na přerušení časovače nebo na události (I/O, `sleep()`) a rozhoduje, který proces poběží dál.

    ??? success "Odpověď"
        **PRAVDA** — to je přesně role plánovače (scheduler) jako součásti jádra.

[Skripta → Úvod](../skripta/01-uvod.md)

---

## Procesy a vlákna

Tvrzení o procesech, vláknech, systémových voláních `fork`/`exec`/`wait` a sdílených prostředcích.

1. Vlákna v rámci jednoho procesu sdílejí globální proměnné a otevřené soubory.

    ??? success "Odpověď"
        **PRAVDA** — vlákna jednoho procesu sdílejí adresní prostor (data, halda, kód) i tabulku otevřených souborů; vlastní mají jen zásobník a registry.

2. Volání `execve()` přepne běžící vlákno do jiného již existujícího procesu.

    ??? success "Odpověď"
        **NEPRAVDA** — `execve()` nahradí obraz *aktuálního* procesu novým programem; nevytváří nový proces ani se nepřepíná do jiného existujícího procesu.

3. Když potomek skončí dříve než rodič a rodič se ukončí bez volání `wait()`, zůstane potomek trvale zombie a nepůjde odstranit.

    ??? success "Odpověď"
        **NEPRAVDA** — osiřelý proces (i zombie) převezme proces `init` (PID 1), který za něj zavolá `wait()` a uklidí ho.

4. Thread Control Block (TCB) obsahuje identifikaci vlákna (TID), informace pro přepínání kontextu (obsah registrů, ukazatel zásobníku) a informace pro plánování (priorita, plánovací algoritmus).

    ??? success "Odpověď"
        **PRAVDA** — to je přesně obsah TCB.

5. Vícevláknový proces s N vlákny sdílí jednu stránkovací tabulku, a tedy i stejný virtuální adresní prostor.

    ??? success "Odpověď"
        **PRAVDA** — všechna vlákna procesu sdílejí stejný virtuální adresní prostor a tím i stránkovací tabulku.

6. V C se po `fork()` rodiči vrátí PID potomka (kladné číslo) a potomkovi 0.

    ??? success "Odpověď"
        **PRAVDA** — `fork()` vrací 0 v potomkovi, kladný PID potomka v rodiči a -1 při chybě.

7. Po neúspěšném `fork()` (např. při dosažení limitu počtu procesů) vrátí volání hodnotu -1.

    ??? success "Odpověď"
        **PRAVDA** — po vyčerpání limitu procesů/vláken `fork()` selže a vrací -1; nový proces nevznikne.

8. Staticky alokované pole (např. `char a[N]`) se umisťuje na zásobník, dynamicky alokovaná paměť přes `malloc()` na haldu.

    ??? success "Odpověď"
        **PRAVDA** — lokální pole jde na zásobník (stack), `malloc()` alokuje na haldě (heap).

9. Potomek vytvořený `fork()` dostává kopii adresního prostoru rodiče, takže globální proměnná má v rodiči i potomkovi stejnou adresu, ale zápis do ní v jednom procesu se neprojeví v druhém.

    ??? success "Odpověď"
        **PRAVDA** — po `fork()` má potomek vlastní (zkopírovaný) adresní prostor; virtuální adresa proměnné je stejná, ale fyzicky jde o oddělené paměti, takže změny nejsou viditelné v druhém procesu.

[Skripta → Procesy a vlákna](../skripta/02-procesy-vlakna.md)

---

## Synchronizace

Tvrzení o zámcích, semaforech, kritické sekci, aktivním čekání a časově závislých chybách.

1. Kritická sekce je jakákoliv část kódu mezi uzamčením a odemčením zámku (např. mezi `pthread_mutex_lock()` a `pthread_mutex_unlock()`).

    ??? success "Odpověď"
        **PRAVDA** — kritická sekce je úsek kódu chráněný zámkem, ve kterém smí být současně nejvýše jedno vlákno.

2. Jeden mutex chrání jeden nebo skupinu sdílených prostředků, ale nelze používat více různých mutexů k ochraně téhož sdíleného prostředku (bez vnořeného zamykání).

    ??? success "Odpověď"
        **PRAVDA** — pokud by tentýž prostředek chránily různé mutexy nezávisle, ztratí se vzájemné vyloučení; vzájemné vyloučení garantuje jen jeden společný mutex.

3. Program, který ze dvou a více vláken současně zapisuje do sdílené proměnné bez dostatečné synchronizace, obsahuje časově závislou chybu (data race).

    ??? success "Odpověď"
        **PRAVDA** — současný zápis více vláken bez ochrany kritické sekce je klasická časově závislá chyba.

4. Pokud je semafor inicializován hodnotou ≥ 2, může do kritické sekce chráněné jen tímto semaforem vstoupit současně více vláken, což u operace typu „přičti ke sdílené proměnné“ způsobuje časově závislou chybu.

    ??? success "Odpověď"
        **PRAVDA** — semafor s počáteční hodnotou 2 pustí dovnitř dvě vlákna zároveň; pro vzájemné vyloučení by musel být inicializován na 1 (binární semafor / mutex). Proto úlohy se `sem_init(&sem, 0, 2)` obsahují data race.

5. Semafor lze implementovat pomocí mutexu a podmíněné proměnné.

    ??? success "Odpověď"
        **PRAVDA** — semafor se dá sestavit z čítače chráněného mutexem a podmíněné proměnné, na které vlákna čekají, je-li čítač nulový.

6. Při buzení čekajícího vlákna je u implementace semaforu vhodnější `pthread_cond_signal()` než `pthread_cond_broadcast()`.

    ??? success "Odpověď"
        **PRAVDA** — stačí probudit jedno vlákno; `broadcast` probudí zbytečně všechna vlákna (i když principiálně korektní, je to neefektivní).

7. Vzájemné vyloučení lze řešit aktivním čekáním pomocí atomické instrukce TSL nebo XCHG.

    ??? success "Odpověď"
        **PRAVDA** — TSL/XCHG atomicky přečte a nastaví zámek; vstup do kritické sekce se realizuje smyčkou testující zámek (busy waiting).

8. Při optimálním a korektním řešení problému spících holičů (N holičů, M zákazníků) stačí 3 semafory: mutex pro sdílené proměnné, jeden pro uspání holičů a jeden pro uspání zákazníků.

    ??? success "Odpověď"
        **PRAVDA** — klasické řešení používá tři semafory: binární mutex a dva synchronizační semafory.

9. Pro problém inverze priorit: nastane, když proces s nízkou prioritou drží zámek potřebný procesu s vysokou prioritou a je přitom předbíhán procesy se střední prioritou.

    ??? success "Odpověď"
        **PRAVDA** — inverze priorit nastává u pevných (statických) priorit, kdy proces s vysokou prioritou nepřímo čeká na proces s nízkou prioritou.

[Skripta → Synchronizace](../skripta/03-synchronizace.md)

---

## Uváznutí (deadlock)

Tvrzení o uváznutí, Coffmanových podmínkách, bankéřově algoritmu, prevenci uváznutí a livelocku.

1. Pokud bankéřův algoritmus neoznačí aktuální stav za bezpečný, znamená to, že systém je právě v uváznutí.

    ??? success "Odpověď"
        **NEPRAVDA** — nebezpečný stav znamená jen, že *může* dojít k uváznutí; systém v uváznutí ještě nemusí být.

2. Neodnímatelné prostředky lze procesu odebrat bez rizika narušení konzistence jeho výpočtu.

    ??? success "Odpověď"
        **NEPRAVDA** — neodnímatelný prostředek z definice nelze bezpečně odebrat; jeho odejmutí by narušilo probíhající operaci. (Neodnímatelnost je jedna z Coffmanových podmínek.)

3. Prevence uváznutí číslováním prostředků: prostředky se alokují jen v předem stanoveném pořadí, čímž se eliminuje kruhové čekání.

    ??? success "Odpověď"
        **PRAVDA** — pevné pořadí alokace znemožní vznik cyklu v grafu čekání, a tím i kruhové čekání.

4. Systém je v bezpečném stavu, pokud existuje pořadí, ve kterém lze postupně uspokojit všechny procesy/vlákna.

    ??? success "Odpověď"
        **PRAVDA** — bezpečný stav je definován existencí bezpečné posloupnosti uspokojení všech procesů.

5. Jsou-li splněny všechny čtyři Coffmanovy podmínky, je systém vždy v uváznutí.

    ??? success "Odpověď"
        **NEPRAVDA** — splnění všech čtyř Coffmanových podmínek je *nutné*, ne *postačující*; systém může být i bezpečný (zkouškové úlohy explicitně uvádějí variantu „bezpečný stav, přestože všechny Coffmanovy podmínky jsou splněné“).

6. Pokud graf alokačních závislostí neobsahuje cyklus, systém není v uváznutí (je v bezpečném stavu).

    ??? success "Odpověď"
        **PRAVDA** — pro prostředky s jednou instancí platí, že absence cyklu znamená absenci uváznutí. (U více instancí na typ je třeba ověřit bankéřovým algoritmem.)

7. Vyhladovění (livelock/starvation) je totéž jako deadlock.

    ??? success "Odpověď"
        **NEPRAVDA** — při deadlocku jsou vlákna trvale zablokována a nic nedělají; při livelocku vlákna stále něco vykonávají (reagují na sebe), ale nepostupují kupředu.

!!! warning "Ověřit"
    Konkrétní úlohy s kódem typu `lock_guard` nad polem mutexů (`g_M[pos % 4]`, `g_M[(pos+1) % 4]`, …) mají odpovědi (deadlock / livelock / busy waiting / možné hodnoty proměnné) závislé na *konkrétních* hodnotách `pos` a pořadí zamykání. Vyhodnocuj je vždy individuálně podle zadaného příkladu — obecně platí jen, že zamykání více mutexů v různém pořadí může vést k deadlocku, a že `lock_guard` nad jediným hromadným `lock(...)` (atomické uzamčení více zámků) deadlocku zabrání, ale může vést k livelocku.

[Skripta → Uváznutí (deadlock)](../skripta/04-deadlock.md)

---

## Plánování procesů

Tvrzení o plánovači, prioritách, časovém kvantu a přepínání kontextu.

1. Při plánování s dynamickou prioritou se obvykle sníží priorita i časové kvantum procesu, který v posledním běhu vyčerpal celé své časové kvantum.

    ??? success "Odpověď"
        **PRAVDA** — proces, který spotřebuje celé kvantum (CPU-bound), je typicky penalizován snížením priority; I/O-bound proces, který kvantum nevyčerpá, je naopak zvýhodněn.

2. Přepnutí kontextu mezi vlákny je v Linuxu implementováno výhradně pomocí systémového volání `sched_yield()`.

    ??? success "Odpověď"
        **NEPRAVDA** — přepnutí kontextu nastává hlavně při přerušení časovače, při blokujících operacích (I/O, `sleep()`) apod.; `sched_yield()` je jen jeden z mnoha možných spouštěčů, nikoli jediný.

3. Při statické (pevné) prioritě se proces s nízkou prioritou nemusí vůbec dostat na CPU, pokud jsou stále připraveny procesy s vyšší prioritou.

    ??? success "Odpověď"
        **PRAVDA** — pevné priority mohou vést k vyhladovění nízkoprioritních procesů.

4. Pokud běh vícevláknového procesu probíhá většinu času ve stavu BLOCKED, zrychlení procesoru ani přidání jader dobu jeho běhu výrazně nezkrátí.

    ??? success "Odpověď"
        **PRAVDA** — doba běhu I/O-bound procesu (vlákna převážně BLOCKED) je dána čekáním, ne výpočetním výkonem, takže rychlejší/další jádra nepomohou.

5. Pokud jsou vlákna procesu většinu času ve stavu READY/RUNNING (CPU-bound) a běží na omezeném počtu jader, je celkový výpočetní výkon konstantní — proto lze dobu běhu přepočítat trojčlenkou podle počtu dostupných vláken procesoru.

    ??? success "Odpověď"
        **PRAVDA** — celkový potřebný výpočet (vlákna × čas) je konstanta; doba běhu se mění nepřímo úměrně počtu dostupných hardwarových vláken.

[Skripta → Plánování procesů](../skripta/05-planovani.md)

---

## Správa paměti

Tvrzení o virtuální paměti, stránkování, TLB, tabulkách stránek, algoritmech náhrady stránek a alokátorech.

1. Bit „present“ v záznamu stránkové tabulky indikuje, zda je stránka aktuálně namapována do fyzické paměti.

    ??? success "Odpověď"
        **PRAVDA** — present bit říká, zda je stránka přítomna ve fyzické paměti; je-li 0, přístup vyvolá výpadek stránky (page fault).

2. Když dojde k výpadku stránky (page fault), systém ukončí běžící proces, protože nelze pokračovat.

    ??? success "Odpověď"
        **NEPRAVDA** — page fault běžně obslouží jádro: chybějící stránku nahraje do fyzické paměti (případně vyhodí jinou) a běh procesu pokračuje.

3. Algoritmus LRU (Least Recently Used) pro náhradu stránek nelze implementovat.

    ??? success "Odpověď"
        **NEPRAVDA** — LRU implementovat lze (např. čítače, seznam); jen je nákladný, proto se v praxi používají aproximace (NRU, Clock, Aging, Second chance).

4. Algoritmus pro náhradu stránek se spouští vždy, když MMU vygeneruje výjimku/trap.

    ??? success "Odpověď"
        **NEPRAVDA** — algoritmus náhrady se spustí jen při výpadku stránky, kdy je potřeba uvolnit rámec a žádný volný není; ne každá výjimka MMU je page fault a ne každý page fault vyžaduje náhradu.

5. Virtuální adresní prostor uživatelského procesu je typicky rozdělen (od nejnižších adres k vyšším) v pořadí: Text, Data, Heap, …, Stack.

    ??? success "Odpověď"
        **PRAVDA** — typické rozvržení je Text (kód), Data, Heap rostoucí nahoru a Stack na vysokých adresách rostoucí dolů.

6. Funkce `free()` vždy okamžitě vrací uvolněnou paměť jádru pomocí `munmap()` nebo `brk()`.

    ??? success "Odpověď"
        **NEPRAVDA** — `free()` zpravidla vrátí blok jen do uživatelského alokátoru (arény) pro budoucí použití; jádru se paměť vrací jen někdy a ne okamžitě.

7. Funkce `free()` v glibc může sloučit sousední volné bloky, ale jen v rámci stejné arény.

    ??? success "Odpověď"
        **PRAVDA** — slučování (coalescing) sousedních volných bloků probíhá v rámci jedné arény, kde jsou bloky správcovány společně.

8. Cache hit ratio TLB se může zvýšit, pokud systém použije pro proces větší stránky.

    ??? success "Odpověď"
        **PRAVDA** — větší stránky pokryjí stejným počtem položek TLB větší adresní prostor, čímž roste úspěšnost vyhledání v TLB.

9. Cache hit ratio TLB se může zvýšit, pokud systém použije pro proces menší stránky.

    ??? success "Odpověď"
        **NEPRAVDA** — menší stránky pokryjí méně paměti, hit ratio TLB naopak klesá.

10. Současné serverové a desktopové procesory umožňují používat různě velké stránky pro různé procesy.

    ??? success "Odpověď"
        **PRAVDA** — moderní procesory podporují více velikostí stránek (huge pages apod.).

11. Současné procesory umožňují aplikacím za běhu měnit velikost TLB podle potřeby.

    ??? success "Odpověď"
        **NEPRAVDA** — velikost TLB je pevně daná hardwarem; aplikace ji měnit nemůže.

12. Offset adresy definuje pozici dat uvnitř rámce (resp. stránky).

    ??? success "Odpověď"
        **PRAVDA** — offset určuje pozici uvnitř rámce/stránky; pro různě velké stránky má offset různý počet bitů.

13. Logická (virtuální) adresa se skládá z čísla stránky a offsetu; fyzická adresa z čísla rámce a offsetu.

    ??? success "Odpověď"
        **PRAVDA** — virtuální adresa = číslo stránky + offset, fyzická adresa = číslo rámce + offset. Velikost offsetu je u obou dána velikostí stránky/rámce.

14. U klasické (přímé) tabulky stránek si jádro musí pamatovat pro každý proces právě jednu tabulku stránek.

    ??? success "Odpověď"
        **PRAVDA** — klasická tabulka stránek je per-proces; při N procesech tedy existuje aspoň N tabulek.

15. U invertované tabulky stránek si jádro musí pamatovat jen jednu (společnou) tabulku stránek.

    ??? success "Odpověď"
        **PRAVDA** — invertovaná tabulka je jedna pro celý systém; má jeden řádek na každý fyzický rámec.

16. Na řádce klasické tabulky stránek je uloženo číslo rámce a bity present, modify a reference.

    ??? success "Odpověď"
        **PRAVDA** — řádek klasické tabulky obsahuje číslo rámce + řídicí bity (present, modify/dirty, reference). Číslo stránky se v ní neukládá (slouží jako index).

17. Na řádce invertované tabulky stránek je uloženo číslo stránky a číslo procesu.

    ??? success "Odpověď"
        **PRAVDA** — invertovaná tabulka indexovaná číslem rámce ukládá na řádku číslo stránky a číslo procesu (plus present/modify/reference). Offset se v tabulkách nikdy neukládá.

18. Na řádce TLB je uloženo číslo stránky, číslo rámce a bity reference/modify.

    ??? success "Odpověď"
        **PRAVDA** — TLB je cache mapování stránka → rámec; na řádce je číslo stránky, číslo rámce a řídicí bity. Offset v TLB není.

19. Při překladu adresy přes invertovanou tabulku stránek lze použít rozptylovací (hash) funkci k urychlení vyhledávání.

    ??? success "Odpověď"
        **PRAVDA** — invertovaná tabulka se prohledává podle (proces, stránka); aby se nemusela procházet lineárně, používá se hašování. U klasické tabulky se hash nepoužívá (přímá indexace).

20. Při překladu adresy se číslo rámce používá jako index do TLB.

    ??? success "Odpověď"
        **NEPRAVDA** — TLB se prohledává podle čísla *stránky*, ne rámce; výsledkem je číslo rámce.

21. Počet řádků klasické tabulky stránek je dán počtem stránek (2 na velikost čísla stránky); počet řádků invertované tabulky je dán počtem rámců (2 na velikost čísla rámce).

    ??? success "Odpověď"
        **PRAVDA** — klasická tabulka má řádek na každou virtuální stránku, invertovaná na každý fyzický rámec.

[Skripta → Správa paměti](../skripta/06-pamet.md)

---

## Datová úložiště a souborové systémy

Tvrzení o discích, RAID, NAS, inodech, souborových systémech a typech odkazů.

1. SSD disky nemají pohyblivé mechanické části, zatímco HDD obsahují otáčející se plotny a pohyblivou čtecí hlavu.

    ??? success "Odpověď"
        **PRAVDA** — to je základní konstrukční rozdíl mezi SSD a HDD.

2. RAID 2, 3 a 4 se v běžných datových úložištích prakticky nepoužívají.

    ??? success "Odpověď"
        **PRAVDA** — v praxi převažují RAID 0, 1, 5, 6, 10; úrovně 2, 3 a 4 jsou dnes spíše historické.

3. Pro NAS (Network-Attached Storage) platí, že data jsou přístupná na úrovni (distribuovaného) souborového systému přes síťové protokoly.

    ??? success "Odpověď"
        **PRAVDA** — NAS poskytuje přístup na úrovni souborů přes protokoly jako NFS či SMB (na rozdíl od SAN, které pracuje na úrovni bloků).

4. RAID 10 se čtyřmi identickými disky nenabízí oproti RAID 5 (rovněž 4 disky) žádné výhody, protože hůře využívá kapacitu a rychlost čtení i zápisu je v obou případech stejná.

    ??? success "Odpověď"
        **NEPRAVDA** — RAID 10 sice využívá kapacitu hůře (poloviční), ale má jiný (zpravidla lepší) výkon zápisu a odlišnou odolnost proti výpadkům; rychlosti tedy nejsou v obou případech stejné.

5. Každý soubor je v unixovém OS jednoznačně identifikován číslem inode v rámci daného souborového systému.

    ??? success "Odpověď"
        **PRAVDA** — inode číslo je jednoznačné v rámci jednoho souborového systému (proto hard link nemůže přesáhnout hranici FS).

6. Obsah adresáře je podobně jako obsah souboru uložen v jednom nebo více datových blocích.

    ??? success "Odpověď"
        **PRAVDA** — adresář je speciální soubor, jehož „obsahem“ jsou položky (jméno → inode) uložené v datových blocích.

7. Symbolický link (soft link) může odkazovat napříč různými souborovými systémy, zatímco hard link jen v rámci téhož souborového systému.

    ??? success "Odpověď"
        **PRAVDA** — soft link uchovává cestu (řetězec) a může mířit kamkoliv; hard link je další jméno pro tentýž inode, a inode čísla jsou jen lokální v rámci FS.

8. Operační systém nemůže používat více souborových systémů současně, pokud jsou na stejném fyzickém disku.

    ??? success "Odpověď"
        **NEPRAVDA** — na jednom fyzickém disku může být více oddílů s různými souborovými systémy a OS je všechny může připojit a používat současně.

9. Při mazání souboru je třeba načíst inody celé cesty včetně mazaného souboru, ale obsah datových bloků samotného souboru se kvůli smazání číst nemusí.

    ??? success "Odpověď"
        **PRAVDA** — pro smazání stačí načíst inody po cestě a uvolnit bloky podle odkazů; vlastní data souboru se nečtou.

10. Při operaci `mv` mezi dvěma adresáři na témže souborovém systému se obsah souboru fyzicky nekopíruje — mění se jen adresářové položky.

    ??? success "Odpověď"
        **PRAVDA** — přesun v rámci jednoho FS jen přepojí adresářovou položku (inode zůstává). Mezi různými FS je `mv` naopak kopírováním a smazáním, takže se data přenášejí blok po bloku.

[Skripta → Datová úložiště a souborové systémy](../skripta/07-souborove-systemy.md)
