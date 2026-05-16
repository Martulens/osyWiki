# Rozcestník pojmů

Tato stránka je centrální rejstřík celého předmětu **BI-OSY (Operační systémy)**. Najdeš zde definice a stručné vysvětlení všech klíčových pojmů, seřazené abecedně v rámci každé kapitoly, s přímými odkazy na příslušné skripta. Máš-li konkrétní pojem, použij **vyhledávací pole** (ikona lupy) v horním navigačním panelu — je to nejrychlejší cesta.

!!! tip "Jak stránku používat"
    Vyhledej pojem v libovolné sekci, přečti stručnou definici a klikni na tučný název — dostaneš se do celé kapitoly, kde je téma rozvinuto do hloubky s příklady a kódem.

---

## Rychlá navigace

- [01 — Úvod do operačních systémů](#01-uvod-do-operacnich-systemu) · [celá kapitola](skripta/01-uvod.md)
- [02 — Procesy a vlákna](#02-procesy-a-vlakna) · [celá kapitola](skripta/02-procesy-vlakna.md)
- [03 — Synchronizace a meziprocesová komunikace](#03-synchronizace-a-meziprocesova-komunikace) · [celá kapitola](skripta/03-synchronizace.md)
- [04 — Uváznutí (deadlock)](#04-uvaznuti-deadlock) · [celá kapitola](skripta/04-deadlock.md)
- [05 — Plánování procesů a vláken](#05-planovani-procesu-a-vlaken) · [celá kapitola](skripta/05-planovani.md)
- [06 — Správa paměti](#06-sprava-pameti) · [celá kapitola](skripta/06-pamet.md)
- [07 — Datová úložiště a souborové systémy](#07-datova-uloziste-a-souborove-systemy) · [celá kapitola](skripta/07-souborove-systemy.md)
- [Vzorce na jednom místě](#vzorce-na-jednom-miste)

---

## 01 Úvod do operačních systémů

→ Celá kapitola ve skriptech: [Úvod do operačních systémů](skripta/01-uvod.md)

**[ABI](skripta/01-uvod.md)** (Application Binary Interface) — binární rozhraní mezi aplikacemi a jádrem OS; implementováno systémovými voláními (syscalls). Odlišuj od API: ABI = syscalls, API = knihovní funkce.

**[API](skripta/01-uvod.md)** (Application Programming Interface) — rozhraní mezi aplikacemi a knihovnami; volání knihovních funkcí (např. `printf`, `malloc`). Neprovede přechod do kernel módu.

**[BARs](skripta/01-uvod.md)** (Base Address Registers) — registry PCI/PCIe zařízení umožňující dynamické přiřazení paměťových adres nebo čísel portů I/O prostoru.

**[BIOS](skripta/01-uvod.md)** (Basic Input-Output System) — starší firmware pro inicializaci HW a bootování; rozpoznává boot sektor podle signatury `0x55 0xAA` na offsetu 510–511.

**[Boot sektor](skripta/01-uvod.md)** (MBR) — první sektor bootovacího zařízení (512 B); obsahuje bootstrap kód. BIOS ho načte na adresu `0x07C00` v paměti.

**[Bootovací signatura](skripta/01-uvod.md)** — hodnoty `0x55 0xAA` na offsetu 510–511 boot sektoru; BIOS podle nich rozpozná bootovatelné médium.

**[Cache](skripta/01-uvod.md)** (skrytá paměť) — rychlá mezipaměť uvnitř CPU (L1/L2/L3) maskující latenci hlavní paměti; programátorovi "neviditelná", spravuje ji HW.

**[CLI](skripta/01-uvod.md)** (Command Line Interface) — textové uživatelské rozhraní; příkazová řádka.

**[CPU](skripta/01-uvod.md)** (Central Processing Unit) — primární procesor počítače; implementuje konkrétní ISA definující sadu instrukcí, registry a organizaci paměti/I/O.

**[Démon](skripta/01-uvod.md)** (daemon) — systémová služba běžící v user módu na pozadí, reagující na události nebo požadavky jiných procesů; komunikuje s jádrem přes syscalls (např. `sshd`, `systemd`).

**[GUI](skripta/01-uvod.md)** (Graphical User Interface) — grafické uživatelské rozhraní.

**[I/O prostor](skripta/01-uvod.md)** (port-mapped I/O) — přístup k I/O zařízením přes speciální instrukce `in`/`out` na x86-64; odlišný od paměťového prostoru.

**[ISA](skripta/01-uvod.md)** (Instruction Set Architecture) — architektura souboru instrukcí definující instrukce, registry a organizaci paměti a I/O. Dělí se na System ISA (pro kernel) a User ISA (pro aplikace).

**[ISR](skripta/01-uvod.md)** (Interrupt Service Routine) — obslužná rutina přerušení/výjimky vykonávaná jádrem OS v kernel módu.

**[Jádro OS](skripta/01-uvod.md)** (kernel) — část OS běžící v kernel módu; implementuje správu I/O, procesů, paměti, FS a sítě.

**[Kernel mód](skripta/01-uvod.md)** — privilegovaný režim CPU (ring 0 / EL1 / S-mode); veškeré operace jsou povoleny; zde běží jádro OS.

**[libc](skripta/01-uvod.md)** (glibc) — standardní knihovna jazyka C; obsahuje obálky systémových volání (`write`, `read`) i vyšší funkce (`printf`, `malloc`). Nepatří do jádra OS.

**[Long mode](skripta/01-uvod.md)** — 64-bitový režim procesoru x86-64; aktivuje plnohodnotnou 64-bitovou adresaci a stránkování.

**[Memory-mapped I/O](skripta/01-uvod.md)** — přístup k I/O zařízením přes paměťový adresní prostor standardními instrukcemi (`mov`, `ldr`); zařízení se tváří jako paměť.

**[Multitasking](skripta/01-uvod.md)** — schopnost OS spouštět více procesů zdánlivě současně prostřednictvím sdílení času CPU (time slicing).

**[Multithreading](skripta/01-uvod.md)** — schopnost procesu obsahovat více souběžně plánovaných vláken.

**[NVRAM / Flash](skripta/01-uvod.md)** — non-volatile paměť pro firmware (BIOS, UEFI) a konfiguraci HW; obsah přežije výpadek napájení.

**[Operační systém](skripta/01-uvod.md)** (OS) — základní software, prostředník mezi HW a aplikacemi; spravuje fyzické i logické prostředky a poskytuje rozhraní aplikacím a uživatelům.

**[POSIX](skripta/01-uvod.md)** — standard definující přenositelné rozhraní unixových OS; specifikuje čísla file descriptorů (stdin = 0, stdout = 1, stderr = 2), názvy a chování syscalls.

**[Protected mode](skripta/01-uvod.md)** — 32-bitový chráněný režim x86-64; umožňuje privilegované módy, stránkování a virtuální paměť.

**[Přerušení](skripta/01-uvod.md)** (interrupt) — **asynchronní** reakce CPU na vnější událost (dokončení I/O, přetečení časovače, HW chyba); přichází z okolí CPU bez ohledu na aktuální instrukci.

**[RAM](skripta/01-uvod.md)** (Random-Access Memory) — hlavní operační paměť; volatile (ztrácí obsah po odpojení napájení); obsahuje jádro OS a běžící procesy.

**[Real mode](skripta/01-uvod.md)** — počáteční 16-bitový režim x86-64 po resetu; 20-bitový fyzický adresní prostor; bez stránkování a privilegovaných módů.

**[Reset vector](skripta/01-uvod.md)** — předem definovaná fyzická adresa, od níž CPU po resetu začíná vykonávat kód (x86-64: `0xFFFFFFFF0`).

**[Ring 0](skripta/01-uvod.md)** — nejvyšší privilegovaný stupeň v x86-64 = kernel mód; veškeré operace povoleny.

**[Ring 3](skripta/01-uvod.md)** — nejnižší privilegovaný stupeň v x86-64 = user mód pro aplikace; přímý přístup k I/O ani ke správě paměti není povolen.

**[Scancode](skripta/01-uvod.md)** — kód vrácený klávesnicí z I/O portu `0x60`; reprezentuje stisk nebo uvolnění klávesy (není to ASCII znak). Bit 7 = 0: stisk, bit 7 = 1: uvolnění.

**[SMP](skripta/01-uvod.md)** (Symmetric Multi-Processing) — podpora více CPU jader; OS plánuje vlákna na různá jádra paralelně.

**[Sběrnice](skripta/01-uvod.md)** (bus) — přenosové médium pro data a řídicí povely mezi částmi výpočetního systému (PCIe, SATA, USB, Fibre Channel).

**[strace](skripta/01-uvod.md)** — linuxový nástroj pro sledování systémových volání volaných z procesu (ekvivalent `truss` na Solarisu).

**[Systémové volání](skripta/01-uvod.md)** (syscall) — jediný způsob, jak uživatelský proces může legálně požádat jádro OS o privilegovanou operaci. Na x86-64/Linux: číslo syscall do `rax`, argumenty do `rdi`, `rsi`, `rdx`, …, instrukce `syscall`.

**[UEFI](skripta/01-uvod.md)** (Unified Extensible Firmware Interface) — moderní náhrada BIOSu s bohatšími možnostmi; hledá EFI soubor v partici ESP.

**[User mód](skripta/01-uvod.md)** — omezený režim CPU pro uživatelské procesy (ring 3 / EL0 / U-mode); přímý přístup k I/O ani ke správě paměti není povolen.

**[VGA framebuffer](skripta/01-uvod.md)** — textový video buffer grafické karty dostupný na adrese `0xB8000` v reálném režimu; každý znak = 2 B (ASCII kód + barva).

**[Výjimka](skripta/01-uvod.md)** (exception) — **synchronní** přerušení vzniklé při zpracování instrukce (syscall, dělení nulou, výpadek stránky). Záměrně vyvolává ji aplikace instrukcí `syscall`.

**[Výpadek stránky](skripta/01-uvod.md)** (page fault) — výjimka vzniklá přístupem na virtuální adresu, k níž není namapována fyzická stránka; řeší ji správa paměti v jádře.

---

## 02 Procesy a vlákna

→ Celá kapitola ve skriptech: [Procesy a vlákna](skripta/02-procesy-vlakna.md)

**[Adopce sirotků](skripta/02-procesy-vlakna.md)** — mechanismus, při kterém `init` (PID 1) přijme potomky procesu, který skončil dříve než oni, a po jejich ukončení správně převezme návratový kód.

**[Deterministický algoritmus](skripta/02-procesy-vlakna.md)** — algoritmus, který ze stejných vstupů vždy produkuje stejné výstupy bez ohledu na časování a pořadí operací.

**[ELF](skripta/02-procesy-vlakna.md)** (Executable and Linkable Format) — binární formát spustitelných souborů v unixových OS (GNU/Linux, BSD). Obsahuje sekce TEXT, DATA a metadata.

**[`execve()`](skripta/02-procesy-vlakna.md)** — systémové volání, které zcela přepíše adresový prostor procesu obsahem nového spustitelného souboru; výpočet začíná od začátku nového programu. Původní kód přestane existovat.

**[`fork()`](skripta/02-procesy-vlakna.md)** — systémové volání v Unixu vytvářející nový proces jako kopii rodiče. V rodiči vrátí PID potomka, v potomkovi vrátí 0. Při chybě vrátí -1.

**[Kontext vlákna](skripta/02-procesy-vlakna.md)** — veškeré informace potřebné k obnovení výpočtu vlákna od místa přerušení; zejména čítač instrukcí (PC) a hodnoty všech registrů CPU.

**[Kritická sekce](skripta/02-procesy-vlakna.md)** (critical section) — část kódu, ve které vlákno přistupuje ke sdílenému prostředku. Sdružené kritické sekce dvou vláken se týkají téhož prostředku.

**[Light-weight process](skripta/02-procesy-vlakna.md)** (LWP) — historický název pro vlákno.

**[Multitasking / Multithreading](skripta/02-procesy-vlakna.md)** — schopnost OS zdánlivě (nebo skutečně na vícejádrovém HW) provádět více úloh souběžně střídáním vláken na jádrech CPU.

**[PE](skripta/02-procesy-vlakna.md)** (Portable Executable) — binární formát spustitelných souborů v MS Windows (`.exe`, `.dll`).

**[PID](skripta/02-procesy-vlakna.md)** (Process ID) — jedinečné celé číslo identifikující proces (nebo vlákno) v rámci OS. Přiřadí ho jádro při `fork()`.

**[POSIX Thread Library](skripta/02-procesy-vlakna.md)** (pthreads) — přenositelné rozhraní pro práci s vlákny na unixových systémech. Klíčové funkce: `pthread_create()`, `pthread_join()`, `pthread_exit()`.

**[PPID](skripta/02-procesy-vlakna.md)** (Parent Process ID) — číslo rodičovského procesu.

**[Preemptivní plánování](skripta/02-procesy-vlakna.md)** — strategie, při které OS přiděluje vláknům časová kvanta a může vlákno přerušit i bez jeho souhlasu po uplynutí kvanta nebo příchodu přerušení.

**[Proces](skripta/02-procesy-vlakna.md)** — instance spuštěného programu; základní entita OS pro alokaci prostředků (paměť, vlákna, soubory, zámky…). Má vlastní virtuální adresový prostor.

**[Program](skripta/02-procesy-vlakna.md)** — spustitelný binární soubor uložený v sekundární paměti, obsahující kód (TEXT), data (DATA) a metadata. Jeho formát závisí na cílovém OS (ELF, PE).

**[`pthread_create()`](skripta/02-procesy-vlakna.md)** — vytvoří nové vlákno, které bude vykonávat zadanou funkci; číslo vlákna uloží na adresu předanou prvním argumentem.

**[`pthread_exit()`](skripta/02-procesy-vlakna.md)** — ukončí pouze volající vlákno; sdílené struktury procesu zůstanou zachovány, dokud neskončí poslední vlákno skupiny.

**[`pthread_join()`](skripta/02-procesy-vlakna.md)** — zablokuje volající vlákno, dokud zadané vlákno neskončí; analogie `wait()` pro vlákna.

**[Přepínání kontextu](skripta/02-procesy-vlakna.md)** (context switch) — mechanismus uložení kontextu běžícího vlákna a obnovení kontextu jiného vlákna; zajišťuje iluzi nepřerušovaného běhu každého vlákna.

**[Race condition](skripta/02-procesy-vlakna.md)** (časově závislá chyba) — nedeterministická chyba vzniklá nekontrolovaným souběžným přístupem více vláken ke sdíleným datům; výsledek závisí na pořadí instrukcí, má náhodný výskyt a je velmi těžko odhalitelná.

**[Sdružené kritické sekce](skripta/02-procesy-vlakna.md)** — kritické sekce dvou nebo více vláken, které se týkají téhož sdíleného prostředku; k race condition dojde, pokud vstoupí do svých sdružených sekcí naráz.

**[Stav vlákna](skripta/02-procesy-vlakna.md)** — Idle (nové), Ready (čeká na CPU), Running (běží na jádře), Blocked (čeká na událost), Zombie (ukončuje se, ale rodič ještě nepřevzal kód), Free (zrušeno).

**[`task_struct`](skripta/02-procesy-vlakna.md)** — datová struktura v Linuxovém jádře reprezentující jak proces, tak vlákno; obsahuje `pid`, `tgid`, paměťový deskriptor `mm`, tabulku souborů `files`, stav `exit_state` a další.

**[TGID](skripta/02-procesy-vlakna.md)** (Thread Group ID) — identifikátor skupiny vláken; všechna vlákna jednoho procesu sdílí stejné TGID, rovnající se PID hlavního vlákna.

**[TID](skripta/02-procesy-vlakna.md)** (Thread ID) — číslo vlákna; v Linuxu totožné s `pid` v `task_struct`.

**[Virtuální adresový prostor](skripta/02-procesy-vlakna.md)** — izolovaný paměťový prostor každého procesu; skládá se ze segmentů TEXT, DATA, heap, stack a mapovaných sdílených knihoven. Procesy navzájem do sebe nevidí.

**[Vlákno](skripta/02-procesy-vlakna.md)** — výpočetní entita (proud instrukcí), které OS přiděluje jádro CPU. Vlákna v procesu sdílí adresový prostor, ale mají vlastní zásobník a kontext.

**[`wait()` / `waitpid()`](skripta/02-procesy-vlakna.md)** — systémové volání zablokující rodičovský proces, dokud se potomek (nebo konkrétní potomek) neukončí; předá návratový kód potomka.

**[Zásobník vlákna](skripta/02-procesy-vlakna.md)** (stack) — privátní paměťová oblast vlákna pro lokální proměnné a historii volání funkcí. V Linuxu se alokuje pomocí `mmap()` před spuštěním vlákna.

**[Zombie](skripta/02-procesy-vlakna.md)** — stav ukončeného procesu, jehož `task_struct` ještě nebyla uvolněna, protože rodič nepřevzal návratový kód voláním `wait()`.

**[Časové kvantum](skripta/02-procesy-vlakna.md)** (time slice) — časový úsek, po který OS nechá vlákno běžet na jádře CPU, než provede přeplánování; typicky 10–50 ms.

**[Vzájemné vyloučení](skripta/02-procesy-vlakna.md)** (mutual exclusion) — princip, že sdružené kritické sekce nesmí být vykonávány souběžně; nejvýše jedno vlákno smí být v kritické sekci najednou.

---

## 03 Synchronizace a meziprocesová komunikace

→ Celá kapitola ve skriptech: [Synchronizace a meziprocesová komunikace](skripta/03-synchronizace.md)

**[Aktivní čekání](skripta/03-synchronizace.md)** (busy waiting, spinning) — vlákno ve smyčce opakovaně testuje podmínku vstupu do kritické sekce; spotřebovává 100 % jednoho jádra CPU po celou dobu čekání.

**[Atomická operace](skripta/03-synchronizace.md)** — operace, která se z pohledu ostatních vláken jeví jako nedělitelná; nelze ji přerušit přepínačem kontextu. Základ správné implementace synchronizačních primitiv.

**[Bariéra](skripta/03-synchronizace.md)** (barrier) — synchronizační primitiv pro iterační výpočty; vlákna volají `barrier_wait()` a čekají, dokud to neudělá požadovaný počet vláken; pak jsou všechna uvolněna. POSIX: `pthread_barrier_t`.

**[Binární semafor](skripta/03-synchronizace.md)** — semafor inicializovaný na 1, chová se jako mutex; hodnoty nabývá pouze 0 a 1. `sem_wait` = mutex_lock, `sem_post` = mutex_unlock.

**[Čtenáři-písaři](skripta/03-synchronizace.md)** (Readers-Writers) — klasická synchronizační úloha: více čtenářů může číst paralelně, ale písař potřebuje výlučný přístup. Spravedlivé řešení vyžaduje explicitní FIFO frontu čekajících vláken; bez ní trpí písaři hladověním.

**[Deadlock](skripta/03-synchronizace.md)** (uváznutí) — situace, kdy skupina vláken čeká na události, které může vyvolat pouze jedno z čekajících vláken; systém se zasekne. Viz kapitola 04.

**[Funkce test()](skripta/03-synchronizace.md)** — pomocná funkce v řešení večeřících filosofů; zkontroluje, zda filosof může jíst (oba sousedé nejedí a filosof má hlad). Pokud ano, nastaví stav na `eating` a zavolá `sem_post` na filosofův semafor.

**[Generální semafor](skripta/03-synchronizace.md)** (počítací semafor) — semafor s čítačem > 1; vhodný pro počítání dostupných instancí prostředku nebo pro signalizaci (inicializace na 0).

**[Hladovění písařů](skripta/03-synchronizace.md)** — situace v úloze čtenářů-písařů, kdy nepřetržitý proud čtenářů trvale blokuje přístup písařů k sdílenému prostředku.

**[Hladovění](skripta/03-synchronizace.md)** (starvation) — vlákno je ve stavu Ready, ale je opakovaně předbíháno ostatními vlákny a nedostane se k prostředkům; není blokováno, ale nepostupuje.

**[Instrukce TSL](skripta/03-synchronizace.md)** (Test-and-Set-Lock) — atomická hardwarová instrukce: načte hodnotu z paměti do registru a nastaví paměťové místo na nenulovou hodnotu v jedné nedělitelné operaci. x86-64: `xchg`, `cmpxchg`; SPARC: `cas`, `ldstub`; RISC-V: `lr`/`sc`.

**[Inverzní prioritní problém](skripta/03-synchronizace.md)** (priority inversion) — uváznutí při aktivním čekání: vlákno s vysokou prioritou obsadí jádro busy-waitingem a vytlačí nízko-prioritní vlákno, které drží zámek, takže ho nemůže uvolnit.

**[Kritická sekce](skripta/03-synchronizace.md)** (critical section/region) — část kódu, kde vlákno přistupuje ke sdílenému prostředku; v jednom okamžiku smí být uvnitř nejvýše jedno vlákno.

**[Livelock](skripta/03-synchronizace.md)** — vlákna aktivně mění svůj stav v reakci na ostatní, ale žádné z nich nedokončí výpočet. Na rozdíl od deadlocku nejsou vlákna blokována (jsou Running/Ready).

**[Mutex](skripta/03-synchronizace.md)** (MUTual EXclusion lock) — blokující synchronizační primitiv; vlákno čekající na zamčený mutex je přepnuto do stavu Blocked a nespotřebovává CPU. POSIX: `pthread_mutex_t`.

**[Optimální řešení](skripta/03-synchronizace.md)** — synchronizační schéma maximalizující paralelismus; pro N filosofů dovoluje `floor(N/2)` jíst současně.

**[POSIX Threads](skripta/03-synchronizace.md)** (pthreads) — standardní API pro vlákna v Unixu; poskytuje `pthread_mutex_t`, `pthread_cond_t`, `sem_t`, `barrier_t`.

**[Podmíněná proměnná](skripta/03-synchronizace.md)** (condition variable) — synchronizační primitiv umožňující vláknu atomicky odemknout mutex a zablokovat se; probuzení nastane po zavolání `cond_signal` nebo `cond_broadcast`. POSIX: `pthread_cond_t`.

**[Producent-konzument](skripta/03-synchronizace.md)** (producer-consumer) — klasická synchronizační úloha: producent vkládá data do sdílené fronty (kapacita N), konzument je odebírá. Nutná synchronizace výlučného přístupu (`mutex`) a stavu fronty (`empty`, `full` semafory nebo podmíněné proměnné).

**[Race condition](skripta/03-synchronizace.md)** — viz sekce 02.

**[Semafor](skripta/03-synchronizace.md)** — synchronizační primitiv s celočíselným čítačem a frontou čekajících vláken. `sem_wait`: sníží čítač nebo zablokuje; `sem_post`: zvýší čítač nebo probudí čekající. POSIX: `sem_t`.

**[Spící holiči](skripta/03-synchronizace.md)** (Sleeping Barbers) — klasická synchronizační úloha: N holičů, N křesel, M čekacích míst. Zákazník odejde, je-li čekárna plná. Řešení: mutex + 2 semafory (`customers`, `barbers`). Optimální, ale bez FIFO nespravedlivé.

**[Spravedlivé řešení](skripta/03-synchronizace.md)** — synchronizační schéma, ve kterém žádné vlákno není předbíháno; čekající jsou obsloužena v FIFO pořadí. Standardní API (POSIX, WinAPI) FIFO pořadí nezaručuje — nutno implementovat explicitně.

**[Spurious wakeup](skripta/03-synchronizace.md)** (falešné probuzení) — vlákno čekající na podmíněné proměnné se může probudit bez zavolání `cond_signal`; proto musí být podmínka testována ve smyčce `while`, ne `if`.

**[Večeřící filosofové](skripta/03-synchronizace.md)** (Dining Philosophers) — klasická synchronizační úloha: N filosofů, N vidliček; každý potřebuje dvě sousední. Naivní řešení → deadlock; vrácení vidliček → livelock; správné optimální řešení: mutex + N semaforů s funkcí `test()`.

**[`cond_wait(var, mutex)`](skripta/03-synchronizace.md)** — atomicky odemkne mutex a zablokuje vlákno; po probuzení mutex opět zamkne. Podmínku kontrolovat ve `while` (ne `if`) kvůli spurious wakeup.

**[`cond_signal(var)`](skripta/03-synchronizace.md)** — probudí aspoň jedno vlákno čekající na podmíněné proměnné.

**[`mutex_lock`](skripta/03-synchronizace.md)** — zamkne mutex; pokud je zamčen, zablokuje volající vlákno.

**[`mutex_unlock`](skripta/03-synchronizace.md)** — odemkne mutex nebo probudí jedno čekající vlákno.

**[`sem_post`](skripta/03-synchronizace.md)** — zvýší čítač semaforu o 1 nebo probudí jedno čekající vlákno.

**[`sem_wait`](skripta/03-synchronizace.md)** — sníží čítač semaforu o 1; pokud je 0, zablokuje volající vlákno.

---

## 04 Uváznutí (deadlock)

→ Celá kapitola ve skriptech: [Uváznutí (deadlock)](skripta/04-deadlock.md)

**[Alokace prostředku](skripta/04-deadlock.md)** — přidělení prostředku vláknu na jeho žádost. Varianty: blokující (čeká neomezeně), s časovým limitem (`mutex_try_lock`), neblokující (okamžitě vrátí výsledek).

**[Alokační graf](skripta/04-deadlock.md)** (resource allocation graph) — orientovaný graf s uzly prostředků a vláken. Hrana prostředek→vlákno = vlákno drží prostředek; hrana vlákno→prostředek = vlákno čeká. **Cyklus v grafu = uváznutí.**

**[Bankéřův algoritmus](skripta/04-deadlock.md)** (banker's algorithm, Dijkstra 1965) — algoritmus předcházení uváznutí; před každým přidělením prostředku OS "zkusmo" přidělí a ověří bezpečnost výsledného stavu. Pokud by stav byl nebezpečný, vlákno čeká.

**[Bezpečná posloupnost](skripta/04-deadlock.md)** — pořadí vláken, v němž lze každé vlákno postupně uspokojit z volných prostředků + prostředků uvolněných předchozími vlákny; existence bezpečné posloupnosti = bezpečný stav.

**[Bezpečný stav](skripta/04-deadlock.md)** (safe state) — stav systému, ze kterého existuje alespoň jedna bezpečná posloupnost; žádné vlákno neuvázne.

**[Checkpoint](skripta/04-deadlock.md)** — pravidelně ukládaný snímek stavu vlákna/systému; umožňuje rollback při zotavení z uváznutí.

**[Coffmanovy podmínky](skripta/04-deadlock.md)** — čtyři **nutné** podmínky uváznutí (musí platit **všechny současně**): vzájemné vyloučení, neodnímatelnost, drž a čekej, kruhové čekání. Porušení jediné uváznutí znemožní.

**[Deadlock](skripta/04-deadlock.md)** (uváznutí) — situace, kdy skupina vláken čeká na události nebo prostředky, které může vyvolat pouze jedno z čekajících vláken; žádné z nich nemůže pokročit.

**[Detekce uváznutí](skripta/04-deadlock.md)** — pravidelné spouštění algoritmu pracujícího s maticí aktuálních požadavků `Q_c` a vektorem volných prostředků `C`; označuje vlákna, která lze uspokojit; neoznačená = uvázlá.

**[Drž a čekej](skripta/04-deadlock.md)** (hold and wait) — Coffmanova podmínka č. 3: vlákno, které drží prostředky, může žádat o další bez uvolnění stávajících.

**[Kruhové čekání](skripta/04-deadlock.md)** (circular wait) — Coffmanova podmínka č. 4: existuje cyklus vláken, kde každé čeká na prostředek držený dalším vláknem v cyklu.

**[Matice přidělených prostředků A](skripta/04-deadlock.md)** (allocation matrix) — `A[k][i]` = počet prostředků typu i aktuálně přidělených vláknu k.

**[Matice chybějících prostředků M](skripta/04-deadlock.md)** (need matrix) — `M = Q - A`; `M[k][i]` = kolik prostředků typu i vlákno k ještě potřebuje. Klíčový vstup Bankéřova algoritmu.

**[Matice požadavků Q](skripta/04-deadlock.md)** (request matrix) — `Q[k][i]` = **maximální** počet prostředků typu i, které vlákno k může celkem potřebovat.

**[Matice aktuálních požadavků Q_c](skripta/04-deadlock.md)** (current request matrix) — používaná při detekci; obsahuje prostředky, které vlákna **právě nyní** aktivně požadují (ne maximální hodnoty jako Q).

**[Nebezpečný stav](skripta/04-deadlock.md)** (unsafe state) — stav, ze kterého může (ale nemusí) nastat uváznutí; žádná bezpečná posloupnost neexistuje.

**[Neodnímatelnost](skripta/04-deadlock.md)** (no preemption) — Coffmanova podmínka č. 2: přidělený prostředek nelze vláknu násilím odebrat, musí ho uvolnit dobrovolně.

**[Neodnímatelný prostředek](skripta/04-deadlock.md)** (nonpreemptable resource) — prostředek, který nelze odebrat bez rizika poškození dat nebo stavu (např. tiskárna).

**[Odnímatelný prostředek](skripta/04-deadlock.md)** (preemptable resource) — prostředek, který lze vláknu odebrat bez trvalých následků (např. stránka fyzické paměti — lze odložit na disk).

**[Prevence uváznutí](skripta/04-deadlock.md)** (deadlock prevention) — statické porušení jedné z Coffmanových podmínek ve fázi návrhu programu; nejpraktičtější: vzestupné číslování prostředků (porušení kruhového čekání).

**[Předcházení uváznutí](skripta/04-deadlock.md)** (deadlock avoidance) — dynamické rozhodování o každém přidělení prostředku (Bankéřův algoritmus); systém nikdy nevstoupí do nebezpečného stavu.

**[Pštrosí strategie](skripta/04-deadlock.md)** (ostrich algorithm) — ignorování problému uváznutí; vhodné tam, kde je uváznutí vzácné a náklady na sofistikované řešení vysoké. Používá většina univerzálních OS.

**[Rollback a restart](skripta/04-deadlock.md)** — zotavení: uvázlá vlákna jsou vrácena do dříve uloženého checkpointu a znovu spuštěna. Nedeterminismus snižuje pravděpodobnost opakování uváznutí.

**[Vektor existujících prostředků E](skripta/04-deadlock.md)** (existence vector) — `E[i]` = celkový počet prostředků typu i v systému; neměnný.

**[Vektor volných prostředků F](skripta/04-deadlock.md)** (free vector) — `F[i]` = počet aktuálně volných prostředků typu i. Platí: `E[i] = F[i] + suma(A[k][i])`.

**[Vzájemné vyloučení](skripta/04-deadlock.md)** (mutual exclusion) — Coffmanova podmínka č. 1: prostředek je přidělen nejvýše jednomu vláknu v daném okamžiku; nelze sdílet bez koordinace.

**[Vzestupné číslování prostředků](skripta/04-deadlock.md)** — technika prevence kruhového čekání: vlákna smí alokovat prostředky pouze v rostoucím pořadí přiřazených čísel; nelze vytvořit cyklus v alokačním grafu.

**[Výpočetní prostředek](skripta/04-deadlock.md)** (resource) — fyzický (paměť, tiskárna, síťová karta) nebo logický (soubor, mutex, semafor) systémový zdroj, ke kterému vlákna soupeří o přístup.

**[Zotavení z uváznutí](skripta/04-deadlock.md)** (deadlock recovery) — ukončení uvázlých vláken (jednorázově nebo postupně) nebo rollback a restart; nutná předchozí detekce.

---

## 05 Plánování procesů a vláken

→ Celá kapitola ve skriptech: [Plánování procesů a vláken](skripta/05-planovani.md)

**[CFS](skripta/05-planovani.md)** (Completely Fair Scheduler) — výchozí plánovač Linuxu pro běžná vlákna; zajišťuje proporcionální přidělování CPU pomocí vruntime a červeno-černého stromu. Vlákno s nejnižším vruntime vždy dostane CPU jako další.

**[CPU-bound vlákno](skripta/05-planovani.md)** — vlákno intenzivně využívající CPU, málo blokujících operací; typické pro vědecké výpočty. Dynamická priorita ho penalizuje, ale dává mu větší kvantum.

**[Červeno-černý strom](skripta/05-planovani.md)** — vyvážená datová struktura, do které CFS ukládá vlákna setříděná podle vruntime; operace vložení/odebrání v O(log n). Nejlevější uzel = vlákno s nejnižším vruntime.

**[FCFS](skripta/05-planovani.md)** (First-Come-First-Served) — kooperativní strategie; vlákno běží, dokud samo neuvolní CPU; FIFO fronta. Minimalizuje přepínání, ale nevhodné pro uživatelská vlákna (jedno vadné vlákno zablokuje systém).

**[Fiber](skripta/05-planovani.md)** — v MS Windows vlákno spravované výhradně v uživatelském prostoru; analogie user-level thread modelu many-to-one.

**[fork-bomba](skripta/05-planovani.md)** — útok, při kterém proces rekurzivně vytváří nové procesy, dokud nevyčerpá systémový limit; bránit lze příkazem `ulimit -u`.

**[Hladovění](skripta/05-planovani.md)** (starvation) — vlákno s nízkou prioritou nedostává CPU po neomezeně dlouhou dobu, protože jsou neustále přítomna vlákna s vyšší prioritou.

**[I/O-bound vlákno](skripta/05-planovani.md)** — vlákno krátce využívající CPU, pak čeká na V/V operace; typické pro databáze a webové servery. Dynamická priorita ho zvýhodňuje.

**[Job](skripta/05-planovani.md)** — v MS Windows množina procesů sdílejících kvóty a limity (CPU, paměť, počet procesů).

**[Kooperativní plánování](skripta/05-planovani.md)** (cooperative scheduling) — vlákno CPU uvolní samo (dokončení nebo blokující volání); OS ho nepřeruší násilně. Vhodné jen pro prověřená kernel vlákna.

**[LWP](skripta/05-planovani.md)** (Lightweight Process) — v Solarisu mapování mezi user-level threads a kernel threads; od Solarisu 8 je podporován pouze model one-to-one.

**[Model many-to-many](skripta/05-planovani.md)** — hybridní implementace: m uživatelských vláken namapováno na n kernel vláken (m ≥ n); kombinuje výhody obou přístupů.

**[Model many-to-one](skripta/05-planovani.md)** — více uživatelských vláken namapováno na jedno kernel vlákno; blokující systémové volání zablokuje celý proces; nelze využít více jader najednou.

**[Model one-to-one](skripta/05-planovani.md)** — každé uživatelské vlákno odpovídá jednomu kernel vláknu; standard v Linux, Windows, macOS; umožňuje paralelismus na více jádrech, ale vyšší režie přepínání.

**[PCB](skripta/05-planovani.md)** (Process Control Block) — datová struktura v jádru OS uchovávající informace o procesu: PID, PPID, přidělená paměť, tabulka deskriptorů souborů, bezpečnostní identita. Jedna položka tabulky procesů.

**[Plánování s odnímáním](skripta/05-planovani.md)** (preemptive scheduling) — OS odebere CPU vláknu po uplynutí časového kvanta; vhodné pro interaktivní systémy, kratší odezva.

**[Prioritní RR se statickou prioritou](skripta/05-planovani.md)** — každé vlákno má pevnou neměnnou prioritu; CPU dostane vlákno z nejvyšší obsazené fronty; nebezpečí hladovění vláken s nízkou prioritou. Linux: `SCHED_RR`.

**[Prioritní RR s dynamickou prioritou](skripta/05-planovani.md)** — priorita a kvantum se mění podle chování vlákna: I/O-bound → priorita +, kvantum ÷2; CPU-bound → priorita -, kvantum ×2. Řeší hladovění a snižuje počet přepnutí. Výchozí v moderních OS.

**[Response time](skripta/05-planovani.md)** (doba odezvy) — čas od zadání požadavku do první reakce systému; kritická metrika pro interaktivní aplikace.

**[Round-Robin](skripta/05-planovani.md)** (RR) — preemptivní strategie s jednou FIFO frontou; všechna vlákna dostávají stejné kvantum (10–50 ms). Efektivita = `tq / (tcs + tq) × 100 %`. Odezva zablokovaného vlákna D = `pocet_ostatnich × (tcs + tq)`.

**[SCHED_BATCH](skripta/05-planovani.md)** — třída Linuxu pro výpočetně náročné dávkové úlohy; používá CFS, snížená priorita odezvy.

**[SCHED_FIFO](skripta/05-planovani.md)** — třída Linuxu pro real-time vlákna s kooperativním FCFS; vlákno běží bez přerušení, dokud se samo nevzdá nebo nepřijde vlákno s vyšší prioritou.

**[SCHED_IDLE](skripta/05-planovani.md)** — třída Linuxu pro vlákna běžící pouze při nulové zátěži systému.

**[SCHED_OTHER](skripta/05-planovani.md)** — výchozí třída plánování Linuxu pro běžná vlákna; používá CFS.

**[SCHED_RR](skripta/05-planovani.md)** — třída Linuxu pro real-time vlákna s preemptivním prioritním RR; statická priorita, pevné kvantum (100 ms).

**[SYS třída v Solarisu](skripta/05-planovani.md)** — kooperativní plánování se statickou prioritou; vyhrazeno pro kernel vlákna; běžný uživatel do ní vlákno zařadit nemůže.

**[Tabulka procesů](skripta/05-planovani.md)** — zřetězený seznam PCB struktur, který jádro OS udržuje pro všechny aktivní procesy.

**[TCB](skripta/05-planovani.md)** (Thread Control Block) — datová struktura pro každé vlákno: TID, registry CPU, zásobník, priorita, stav, plánovací informace.

**[TS třída v Solarisu](skripta/05-planovani.md)** (Time Sharing) — preemptivní plánování s dynamickou prioritou a proměnným kvantem; parametry (ts_quantum, ts_tqexp, ts_slpret) definovány tabulkou příkazu `dispadmin`.

**[Turnaround time](skripta/05-planovani.md)** (doba zpracování) — čas od spuštění úlohy do jejího dokončení; kritická metrika pro dávkové úlohy.

**[Vlákno reálného času](skripta/05-planovani.md)** (Realtime thread) — vlákno, které musí zareagovat na událost v garantovaném čase; nevyžaduje nutně velký CPU výkon.

**[Zóna](skripta/05-planovani.md)** (Solaris) — virtuální instance OS sdílející jádro s hostitelským systémem; obdoba Linux kontejnerů (cgroups/namespaces).

**[`/proc`](skripta/05-planovani.md)** — pseudo-souborový systém v Linuxu existující pouze v RAM; umožňuje číst a nastavovat parametry jádra a informace o procesech (`/proc/sys/kernel/threads-max`).

**[`ulimit`](skripta/05-planovani.md)** — unixový příkaz pro nastavení limitů procesů/vláken na úrovni uživatele (`ulimit -u 100` omezí počet vláken); chrání před fork-bombou.

**[Efektivita CPU](skripta/05-planovani.md)** — podíl doby, kdy CPU vykonává užitečnou práci: `efektivita = tq / (tcs + tq)` pro Round-Robin.

**[min_vruntime](skripta/05-planovani.md)** — nejmenší vruntime z aktuálně neblokovaných vláken; při probuzení z blokujícího volání se vruntime vlákna nastaví na tuto hodnotu (vlákno dostane CPU brzy, ale ne příliš velké zvýhodnění).

**[nice hodnota](skripta/05-planovani.md)** — číslo -20 až 19 nastavující váhu vlákna v CFS; záporná = vyšší váha = vruntime roste pomaleji = více CPU; kladná = méně CPU.

**[vruntime](skripta/05-planovani.md)** (virtual runtime) — vážený běhový čas vlákna v CFS; roste pomaleji pro vlákna s vyšší váhou (nižší nice); vlákno s nejnižším vruntime dostane CPU jako další.

---

## 06 Správa paměti

→ Celá kapitola ve skriptech: [Správa paměti](skripta/06-pamet.md)

**[ASLR](skripta/06-pamet.md)** (Address Space Layout Randomization) — náhodné posunutí adres segmentů VAS při startu procesu pro ztížení exploitů.

**[Aging](skripta/06-pamet.md)** — softwarová simulace LRU: každá stránka má n-bitový čítač C; OS periodicky posune C doprava a nastaví MSB na hodnotu R bitu, poté resetuje R. Oběť = stránka s nejmenším C.

**[Anonymní VMA](skripta/06-pamet.md)** — VMA bez svázaného souboru (halda, zásobník, .bss); inicializuje se nulami (demand-zero page).

**[Aréna](skripta/06-pamet.md)** (glibc) — oblast paměti + mutex pro správu haldy v jednom vláknu; hlavní aréna pro hlavní vlákno (roste přes `sbrk`), sekundární pro ostatní (přes `mmap`).

**[ASID](skripta/06-pamet.md)** (Address Space ID) — identifikátor VAS v TLB; umožňuje koexistenci záznamů více procesů v TLB bez nutnosti flush při každém přepnutí kontextu.

**[Assembler](skripta/06-pamet.md)** — převádí assembly kód na binární objektový soubor (`.o`) s nevyřešenými externími symboly; každá sekce začíná od adresy 0.

**[Base register](skripta/06-pamet.md)** — registr obsahující fyzickou adresu začátku oblasti procesu; spolu s limit registrem slouží pro relokaci a ochranu adres (historická metoda bez stránkování).

**[Brk](skripta/06-pamet.md)** (program break) — konec haldy v adresovém prostoru procesu; posouvá se systémovými voláními `brk`/`sbrk`.

**[Buddy alokátor](skripta/06-pamet.md)** — alokátor fyzické paměti s oblastmi o velikostech mocnin dvou (`2^i`); umožňuje rychlé slučování sousedních volných oblastí (buddies). Linux ho používá pro fyzické rámce.

**[Cache](skripta/06-pamet.md)** (skrytá paměť) — mezipaměť mezi CPU a hlavní pamětí; funguje na principu časové a prostorové lokality. Průměrný čas přístupu: `t_avg = r_h * t_h + (1 - r_h) * t_m`.

**[CMA](skripta/06-pamet.md)** (Contiguous Memory Allocator) — alokátor pro velké (> 4 MB) souvislé bloky fyzické paměti; rezervuje paměť při startu systému.

**[COW](skripta/06-pamet.md)** (Copy-on-Write) — optimalizace při `fork()`: obě kopie sdílejí rámce do prvního zápisu; při zápisu OS vytvoří novou kopii rámce jen pro zapisující proces.

**[Demand paging](skripta/06-pamet.md)** (stránkování na žádost) — stránka se načte do fyzické paměti až při prvním přístupu k ní (page fault); šetří paměť.

**[Dirty bit D](skripta/06-pamet.md)** — bit v PTE; nastaví HW při zápisu; 1 = stránka byla modifikována a musí být zapsána na disk (do swap nebo zdrojového souboru) před odstraněním z paměti.

**[DMA](skripta/06-pamet.md)** (Direct Memory Access) — přenos dat mezi I/O zařízením a fyzickou pamětí bez účasti CPU; vyžaduje souvislé fyzické oblasti (proto buddy alokátor).

**[Dynamické linkování](skripta/06-pamet.md)** — spustitelný soubor odkazuje na sdílené knihovny (`.so`, `.dll`); váže symboly za běhu (load-time nebo run-time/lazy binding).

**[Dynamické oddíly](skripta/06-pamet.md)** — historická metoda správy paměti alokací jedné souvislé oblasti pro každý proces; trpí fragmentací.

**[ELF](skripta/06-pamet.md)** — formát objektových a spustitelných souborů v Linuxu; metadaje dostupná přes `readelf -a`.

**[FIFO](skripta/06-pamet.md)** (algoritmus náhrady stránek) — nahradí stránku, která je v paměti nejdéle; nejjednodušší, ale nejhorší počet výpadků; nezohledňuje nedávnost přístupu. V příkladu: 9 výpadků.

**[File-backed VMA](skripta/06-pamet.md)** — VMA svázaná se souborem (`.text`, dynamická knihovna).

**[Fragmentace](skripta/06-pamet.md)** — rozpad fyzické paměti na malé volné ostrůvky, do nichž se nový proces nevejde; řeší ji stránkování.

**[Fyzická adresa](skripta/06-pamet.md)** — skutečná adresa v hlavní paměti; výsledek překladu z virtuální adresy přes MMU.

**[Halda](skripta/06-pamet.md)** (heap) — oblast VAS pro dynamicky alokovanou paměť (`malloc`, `new`); roste od nižších adres nahoru; spravuje ji knihovna glibc.

**[Hierarchie paměti](skripta/06-pamet.md)** — víceúrovňová organizace: registry (~1 ns) → L1–L3 cache (~1–10 ns) → hlavní paměť (~50 ns) → SSD (~0,1 ms) → HDD (~10 ms).

**[Hit ratio](skripta/06-pamet.md)** (`r_h`) — podíl přístupů, při nichž jsou data nalezena v cache: `r_h = n_h / (n_h + n_m)`. Klíčový parametr výkonu.

**[Hlavní paměť](skripta/06-pamet.md)** (main memory) — fyzická DRAM paměť; nejmenší adresovatelná jednotka je byte; přistupují k ní CPU instrukce load/store.

**[Huge pages](skripta/06-pamet.md)** — větší stránky/rámce (2 MB, 1 GB na x86-64); snižují frekvenci TLB miss pro paměťově náročné aplikace (databáze, vědecké výpočty).

**[Chunk](skripta/06-pamet.md)** — alokační jednotka haldy v glibc; obsahuje metadata (velikost, příznak obsazenosti) a uživatelská data.

**[Invertovaná ST](skripta/06-pamet.md)** — stránkovací tabulka s jedním záznamem na fyzický rámec; jedna pro celý systém; úspora paměti, ale pomalejší překlad (hašování s kolizemi). Používala: PowerPC, UltraSPARC (TSB).

**[Jednoúrovňová ST](skripta/06-pamet.md)** — stránkovací tabulka s jedním záznamem (PTE) na každou stránku VAS; na 32-bit CPU se 4KB stránkami = 4 MB na proces. Pro 128 procesů = 512 MB jen na tabulky.

**[Kompilátor](skripta/06-pamet.md)** — překládá zdrojový kód do assembly; výstupem jsou symbolické (nevyřešené) adresy.

**[KPTI](skripta/06-pamet.md)** (Kernel Page Table Isolation) — obrana proti Meltdown; odděluje stránkovací tabulky jádra od VAS uživatelských procesů.

**[Limit register](skripta/06-pamet.md)** — registr obsahující velikost oblasti procesu; přístup za limit vyvolá výjimku (ochrana paměti).

**[Linker](skripta/06-pamet.md)** — sloučí objektové moduly do spustitelného souboru (load module); vyřeší nevyřešené symboly a vypočítá adresy sekcí.

**[Loader](skripta/06-pamet.md)** — část OS zavádějící program do paměti; vytváří VAS na základě metadat z ELF.

**[LRU](skripta/06-pamet.md)** (Least Recently Used) — nahradí stránku, ke které se nejdéle nepřistupovalo; nejlepší aproximace optimálního algoritmu. Obtížná implementace (nutný HW čítač). V příkladu: 7 výpadků.

**[MMU](skripta/06-pamet.md)** (Memory Management Unit) — hardwarová jednotka v CPU překládající virtuální adresy na fyzické pomocí stránkovacích tabulek a TLB.

**[NRU](skripta/06-pamet.md)** (Not Recently Used) — algoritmus náhrady: třídí stránky do 4 tříd podle R a D bitů (třída 0 = R=0,D=0 = nejlepší oběť; třída 3 = R=1,D=1 = nejhorší). Nahradí z nejnižší neprázdné třídy. V příkladu: 7 výpadků.

**[Objekový modul](skripta/06-pamet.md)** (object module) — binární soubor (`.o`) s přemístitelným kódem a nevyřešenými externími symboly; není přímo spustitelný.

**[Optimální algoritmus](skripta/06-pamet.md)** — nahradí stránku, ke které bude přistoupeno nejpozději v budoucnosti; generuje minimální počet výpadků, ale **nelze implementovat** (nezná budoucnost). Slouží jako referenční mez. V příkladu: 6 výpadků.

**[Page fault](skripta/06-pamet.md)** (výpadek stránky) — přerušení nastávající, když MMU zjistí bit P=0 v PTE; OS načte stránku z disku nebo inicializuje nulami, aktualizuje ST a TLB, vrátí řízení procesu.

**[Paging-out](skripta/06-pamet.md)** — OS odloží vybrané stránky na disk (swap nebo zdrojový soubor) pro uvolnění rámců.

**[Present bit P](skripta/06-pamet.md)** — bit v PTE; 1 = stránka je v hlavní paměti, 0 = page fault.

**[Prepaging](skripta/06-pamet.md)** (před-stránkování) — při page fault se načtou i sousední stránky na základě prostorové lokality; snižuje počet I/O operací.

**[Prostorová lokalita](skripta/06-pamet.md)** — data blízká aktuálně používaným budou brzy potřeba; proto cache načítá celou cache line a OS předstránkuje sousední stránky.

**[PTBR](skripta/06-pamet.md)** (Page Table Base Register) — registr CPU ukazující na top-level stránkovací tabulku aktivního procesu; na x86-64 registr CR3.

**[PTE](skripta/06-pamet.md)** (Page Table Entry) — jeden záznam stránkovací tabulky; obsahuje číslo rámce, P bit, D bit, R/A bit, W, X, U/S, C.

**[Rámec](skripta/06-pamet.md)** (frame) — pevně velká oblast fyzické paměti stejné velikosti jako stránka (typicky 4 KB).

**[Reference bit R](skripta/06-pamet.md)** (Accessed bit A) — bit v PTE; HW ho nastaví při každém přístupu ke stránce (čtení nebo zápis); OS ho periodicky resetuje pro sledování "nedávnosti".

**[Reverzní mapování](skripta/06-pamet.md)** — mechanismus (přes `anon_vma`/`address_space`) pro dohledání všech procesů mapujících daný fyzický rámec; nutné pro aktualizaci jejich ST po výběru oběti.

**[Slab alokátor](skripta/06-pamet.md)** — alokátor jádra OS pro malé objekty fixní velikosti (task_struct, inode…); pracuje nad oblastmi od buddy alokátoru; eviduje se přes `cat /proc/slabinfo`.

**[Statické linkování](skripta/06-pamet.md)** — linker zahrne vše potřebné přímo do spustitelného souboru; program je nezávislý na externích knihovnách.

**[Stránka](skripta/06-pamet.md)** (page) — pevně velká oblast VAS (typicky 4 KB na x86-64, 8 KB na SPARC); základ stránkování.

**[Stránkování](skripta/06-pamet.md)** (paging) — mechanismus správy paměti: VAS rozdělen na stránky, fyzická paměť na rámce stejné velikosti; v hlavní paměti musí být jen aktuálně potřebné stránky.

**[Stránkovací tabulka](skripta/06-pamet.md)** (Page Table, PT) — datová struktura OS mapující čísla stránek VAS na čísla fyzických rámců.

**[Swap](skripta/06-pamet.md)** — diskový prostor (oddíl nebo soubor) pro ukládání anonymních stránek odložených z fyzické paměti.

**[Swapping](skripta/06-pamet.md)** — dočasné přesunutí celého procesu na disk při kritickém nedostatku paměti; pomalejší než paging-out.

**[TLB](skripta/06-pamet.md)** (Translation Lookaside Buffer) — hardwarová n-cestná asociativní cache nedávných překladů adres (stránka → rámec); TLB hit je řádově rychlejší než prohledání ST v paměti.

**[TLB miss](skripta/06-pamet.md)** — překlad nebyl nalezen v TLB; nutno prohledat stránkovací tabulku v hlavní paměti.

**[TLB shootdown](skripta/06-pamet.md)** — invalidace položek TLB na všech CPU jádrech po změně mapování rámce; nutné při aktualizaci sdílených stránek.

**[Thrashing](skripta/06-pamet.md)** (paměťový kolaps) — situace, kdy součet Working Set všech aktivních procesů překročí velikost RAM; procesy si vzájemně kradou rámce, CPU tráví většinu času obsluhou page faultů.

**[Časová lokalita](skripta/06-pamet.md)** — data nedávno použitá budou s vysokou pravděpodobností potřeba znovu v blízké budoucnosti; základ efektivity cache.

**[VAS](skripta/06-pamet.md)** (Virtual Address Space) — virtuální adresní prostor; izolovaný logický prostor adres každého procesu; instrukce load/store generují virtuální adresy, MMU je překládá na fyzické.

**[VMA](skripta/06-pamet.md)** (Virtual Memory Area, `struct vm_area_struct`) — souvislý blok virtuální paměti s daným účelem (`.text`, heap, zásobník, knihovna) a přístupovými právy (R, W, X).

**[Virtuální adresa](skripta/06-pamet.md)** — adresa generovaná procesem; skládá se z čísla stránky (index do ST) a offsetu (pozice uvnitř stránky/rámce).

**[Víceúrovňová ST](skripta/06-pamet.md)** — hierarchická stránkovací tabulka; tabulky nižších úrovní existují jen pro skutečně používané oblasti VAS; šetří paměť. x86-64: 4 úrovně (PML4 → PDPT → PD → PT), index po 9 bitech, 12 bitů offset = 48-bit virtuální adresa.

**[Working Set](skripta/06-pamet.md)** (WS) — množina stránek aktivně používaných procesem v daném časovém okně; rozumný počet rámců pro daný proces pro minimální výpadky.

**[`execve()`](skripta/06-pamet.md)** — systémové volání nahrazující obraz procesu novým programem; odstraní starý VAS, vytvoří nový podle ELF, nastaví PC na Entry Point.

**[`mmap()`](skripta/06-pamet.md)** — systémové volání pro mapování souboru nebo anonymní paměti do VAS procesu; základ pro sdílené knihovny, sdílenou paměť a zásobník vláken.

**[Clock algoritmus](skripta/06-pamet.md)** — modifikovaný FIFO s kruhovým bufferem a ručičkou; stránky s R=1 dostanou "druhou šanci" (reset R, ručička dál); stránky s R=0 jsou oběti. V příkladu: 8 výpadků.

---

## 07 Datová úložiště a souborové systémy

→ Celá kapitola ve skriptech: [Datová úložiště a souborové systémy](skripta/07-souborove-systemy.md)

**[B strom](skripta/07-souborove-systemy.md)** — vyvážený strom řádu n: každý vnitřní uzel má ceil(n/2)–n potomků; O(log N) vložení/smazání/vyhledání. Každý uzel se vejde do jednoho bloku/stránky.

**[B+ strom](skripta/07-souborove-systemy.md)** — varianta B stromu: vnitřní uzly obsahují pouze klíče a ukazatele, data jsou jen v listech; listy propojeny ukazateli → efektivní sekvenční průchod. Základ moderních FS (NTFS, XFS, BTRFS).

**[Block Read Ahead](skripta/07-souborove-systemy.md)** — přednačítání sousedních datových bloků do Page cache při I/O požadavku; využívá prostorovou lokalitu; zlepšuje výkon sekvenčního čtení.

**[Boot block](skripta/07-souborove-systemy.md)** — oblast FS s kódem zavaděče OS (nebo prázdná, není-li oblast bootovatelná).

**[CHS](skripta/07-souborove-systemy.md)** (Cylinder-Head-Sector) — starší způsob adresování sektorů HDD trojicí [cylindr, povrch, sektor].

**[COW](skripta/07-souborove-systemy.md)** (Copy-on-Write) — při modifikaci se původní bloky nikdy nepřepisují; nová data jdou do nových bloků, atomicky se přepíše ukazatel v superbloku. Zaručuje vždy konzistentní stav FS + základ snapshotů.

**[Cylinder Group](skripta/07-souborove-systemy.md)** (CG) — oblast UFS reprezentující skupinu cylindrů s vlastní zálohou superbloku, bitmap a i-nodů; soubor alokován uvnitř jedné CG = hlavičky se pohybují jen v malé oblasti.

**[DAS](skripta/07-souborove-systemy.md)** (Direct-Attached Storage) — úložiště přímo připojené k systému přes SATA/SAS/…; OS vidí sektory.

**[Datový blok](skripta/07-souborove-systemy.md)** (cluster) — logická jednotka FS, skupinování sektorů; typicky 1 KB–2 MB dle FS a konfigurace. Administrátor volí velikost při `mkfs`.

**[DNLC / Dentry cache](skripta/07-souborove-systemy.md)** — cache v RAM pro přeložená jména adresářů/souborů a jejich v-nody; dramaticky urychluje opakovaný přístup k souborům (7,5× v příkladu).

**[FAT](skripta/07-souborove-systemy.md)** (File Allocation Table) — tabulka adres bloků souboru: každý řádek obsahuje Free/adresu dalšího bloku/EOF. Adresář si pamatuje jen adresu prvního bloku. Varianty: FAT12/16/32 (28 b fakticky)/exFAT (64 b).

**[Floating gate MOSFET](skripta/07-souborove-systemy.md)** — typ tranzistoru s plovoucí bránou izolovanou z obou stran; základ NAND flash buňky. Přítomnost náboje = logická 0, absence = logická 1.

**[FS layout](skripta/07-souborove-systemy.md)** — typické rozložení dat ve FS: boot block → super block → struktury volného prostoru → tabulka i-nodů → datové bloky.

**[FTL](skripta/07-souborove-systemy.md)** (Flash Translation Layer) — firmware SSD překládající LBA adresy na fyzické NAND stránky/bloky; zajišťuje wear leveling, garbage collection a správu vadných bloků.

**[FUSE](skripta/07-souborove-systemy.md)** (Filesystem in Userspace) — umožňuje implementovat FS jako uživatelský proces bez zásahu do jádra; nevýhoda: vyšší latence kvůli přepínání kontextu.

**[Garbage collection (SSD)](skripta/07-souborove-systemy.md)** — proces uvolňování neplatných NAND bloků a přípravy prázdných bloků pro zápis.

**[Hard link](skripta/07-souborove-systemy.md)** — přímý odkaz na i-node z adresáře; soubor existuje, dokud je alespoň jeden hard link. Nelze přes hranice FS.

**[HDD](skripta/07-souborove-systemy.md)** (Hard Disk Drive) — magnetické rotační úložiště; data kódována změnou směru magnetizace na feromagnetických plotnách. Seek time 1–10 ms, rotační zpoždění avg 3–6 ms.

**[I-node](skripta/07-souborove-systemy.md)** (index node) — datová struktura pevné velikosti pro každý soubor/adresář; obsahuje atributy + 12 přímých adres + 1 nepřímou 1. úrovně + 1 nepřímou 2. úrovně + 1 nepřímou 3. úrovně. Základ UFS, Ext2/3/4.

**[IFS](skripta/07-souborove-systemy.md)** (Installable File System) — API v OS/2 a MS Windows pro dynamické načítání ovladačů FS za běhu.

**[LBA](skripta/07-souborove-systemy.md)** (Logical Block Addressing) — lineární adresování sektorů sekvenčně od 0; novější a jednodušší než CHS.

**[Multihosting](skripta/07-souborove-systemy.md)** — jedno úložiště připojeno k více systémům současně (např. přes SCSI nebo SAN).

**[Multipathing](skripta/07-souborove-systemy.md)** — více nezávislých síťových cest mezi systémem a úložištěm (SAN); zvyšuje propustnost i odolnost.

**[NAND flash](skripta/07-souborove-systemy.md)** — organizace flash buněk do sériové struktury analogické NAND hradlu; mazání probíhá vždy po celých blocích najednou.

**[NAS](skripta/07-souborove-systemy.md)** (Network-Attached Storage) — síťové úložiště sdílené přes NFS nebo SMB; OS vidí soubory, nikoliv sektory.

**[NCQ](skripta/07-souborove-systemy.md)** (Native Command Queuing) — technologie reorderingu příkazů přímo v řadiči SATA disku pro minimalizaci pohybu hlaviček.

**[NFS](skripta/07-souborove-systemy.md)** (Network File System) — síťový protokol pro sdílení souborového systému v unixových systémech.

**[Page cache](skripta/07-souborove-systemy.md)** — mezipaměť v RAM pro nedávno použité datové bloky FS; cache hit = data z RAM bez disk I/O. Strategie zápisu: write-behind (interní úložiště) nebo write-through (přenosná média).

**[Perpendicular Recording](skripta/07-souborove-systemy.md)** — moderní technika záznamu HDD: magnetické domény kolmo na povrch plotny; vyšší hustota záznamu než longitudinal recording.

**[RAID](skripta/07-souborove-systemy.md)** (Redundant Array of Independent Disks) — sdružení fyzických disků pro kapacitu, výkon a/nebo redundanci.

**[RAID 0 (striping)](skripta/07-souborove-systemy.md)** — prokládání dat po blocích; žádná redundance; sekvenční R/W až m-krát rychlejší; výpadek jednoho disku = ztráta všech dat.

**[RAID 1 (mirroring)](skripta/07-souborove-systemy.md)** — zrcadlení na všechny disky; redundance `(m-1)/m × 100 %`; čtení až m-krát rychlejší; zápis = rychlost jednoho disku.

**[RAID 10](skripta/07-souborove-systemy.md)** — kombinace RAID 1 + RAID 0; redundance 50 %; sekvenční R/W až (m/2)-krát rychlejší; IOPS až m-krát.

**[RAID 5](skripta/07-souborove-systemy.md)** — prokládání + distribuovaná parita; redundance `100/m %`; výpadek **jednoho** disku; využití `(m-1)/m`; zápis pomalejší (4 I/O na 1 logický zápis).

**[RAID 6](skripta/07-souborove-systemy.md)** — prokládání + dvojitá parita; redundance `200/m %`; výpadek **dvou** disků; využití `(m-2)/m`; zápis nejpomalejší.

**[Rotational delay](skripta/07-souborove-systemy.md)** — průměrné rotační zpoždění HDD = polovina doby jedné otáčky = `60 / (2 × RPM)` sekund. Při 10 000 RPM ≈ 3 ms.

**[SAN](skripta/07-souborove-systemy.md)** (Storage Area Network) — dedikovaná síť úložišť (Fibre Channel nebo Ethernet); OS vidí sektory přes síť; podporuje multihosting a multipathing.

**[SCAN](skripta/07-souborove-systemy.md)** (výtahový algoritmus) — algoritmus plánování přístupu na HDD: hlavičky se pohybují jedním směrem, obslouží vše, pak se otočí. Omezuje stárnutí požadavků.

**[Seek time](skripta/07-souborove-systemy.md)** — čas přesunu hlaviček HDD nad správný cylindr; typicky 1–10 ms; hlavní složka latence při náhodném přístupu.

**[Sektor](skripta/07-souborove-systemy.md)** — nejmenší fyzicky adresovatelná jednotka datového úložiště (512 B nebo 4 KB); obsahuje synchronizaci, data a ECC.

**[Slab alokátor](skripta/07-souborove-systemy.md)** — viz sekce 06.

**[SLC / MLC / TLC / QLC](skripta/07-souborove-systemy.md)** — typy NAND flash: ukládají 1/2/3/4 bity do jedné buňky; více bitů = vyšší kapacita, nižší trvanlivost a spolehlivost. SLC: 50 000–100 000 zápisů; QLC: 100–1 000 zápisů.

**[SMB / CIFS / Samba](skripta/07-souborove-systemy.md)** — síťový protokol pro sdílení FS v prostředí MS Windows.

**[Soft link](skripta/07-souborove-systemy.md)** (symbolický link) — speciální soubor obsahující cestu k cíli; funguje přes hranice FS; při smazání cíle vzniká "dangling link".

**[SSD](skripta/07-souborove-systemy.md)** (Solid State Drive) — úložiště na bázi NAND flash; bez pohyblivých částí; konstantní latence (nezávislá na poloze); omezený počet zápisů.

**[SSTF](skripta/07-souborove-systemy.md)** (Shortest Service Time First) — algoritmus plánování HDD: obslouží požadavek nejblíže aktuální pozici hlavičky; lepší výkon než FIFO, ale hrozí stárnutí vzdálených požadavků.

**[Super block](skripta/07-souborove-systemy.md)** — metadata FS: typ, velikost datových bloků, celková velikost, obsazenost, adresy klíčových struktur; uložen i v záložních kopiích.

**[UFS](skripta/07-souborove-systemy.md)** (Unix File System / BSD FFS) — klasický unixový FS s i-nody a Cylinder Groups; datový blok 8 KB (Solaris); i-node 128 B; kořenový adresář = i-node č. 2. Inspiroval Ext2/3/4 a HFS+.

**[V-node](skripta/07-souborove-systemy.md)** (virtual node) — abstraktní reprezentace souboru/adresáře v rámci VFS; každý konkrétní FS implementuje operace nad v-nody po svém.

**[VFS](skripta/07-souborove-systemy.md)** (Virtual File System) — abstraktní vrstva jádra unixového OS; rozhraní mezi procesy a konkrétními implementacemi FS; zajišťuje, že `open`, `read`, `write` fungují stejně pro ext4, UFS, FAT32 i NFS.

**[Wear leveling](skripta/07-souborove-systemy.md)** — technika FTL rovnoměrně rozložující zápisy na buňky NAND flash pro prodloužení životnosti SSD.

**[Write-behind cache](skripta/07-souborove-systemy.md)** (write-back) — zápisová strategie: zápis do Page cache ihned, na disk se zpožděním (flush přes `sync()`). Výkon vyšší, ale hrozí ztráta dat při výpadku napájení.

**[Write-through cache](skripta/07-souborove-systemy.md)** — zápisová strategie: zápis do cache i na disk současně; bezpečnější, ale pomalejší. Používá se u přenosných médií.

**[ZBR](skripta/07-souborove-systemy.md)** (Zone Bit Recording) — technika HDD: vnější zóny stopy mají více sektorů než vnitřní; zvyšuje celkovou kapacitu disku.

**[ZFS](skripta/07-souborove-systemy.md)** (Zettabyte File System) — moderní FS integrující SW RAID, COW, Merkle strom kontrolních součtů, snapshoty a self-healing. Detekuje a opravuje všechny typy poškození dat (bit corruption, lost/misdirected/torn writes).

**[Žurnálování](skripta/07-souborove-systemy.md)** (Journaling) — FS zapisuje záznamy o chystaných změnách do žurnálu před jejich provedením; po pádu systému se záznamy přehrají → FS vrácen do konzistentního stavu. Implementují: UFS, Ext3/4, NTFS, XFS.

**[Žurnál](skripta/07-souborove-systemy.md)** — speciální oblast na disku (nebo externím SSD) pro záznamy o chystaných změnách FS.

---

## Vzorce na jednom místě

!!! info "Tato sekce shrnuje nejdůležitější vzorce a výpočty z celého předmětu."

### Cache a paměť

| Veličina | Vzorec |
|---|---|
| Průměrný čas přístupu | `t_avg = r_h × t_h + (1 - r_h) × t_m` |
| Hit ratio | `r_h = n_h / (n_h + n_m)` |
| Velikost jednoúrovňové ST (32-bit, 4 KB stránky) | `2^20 záznamu × 4 B = 4 MB na proces` |
| Počet adres v bloku (stránkovací tabulka) | `počet adres = velikost bloku / velikost adresy` |
| Maximální velikost souboru přes i-node | `(12 + 2^k + 2^2k + 2^3k) × vel. bloku`, kde `k = log2(blok / adresa)` |

**Příklad i-node** (blok 4 KB, adresa 4 B → k=10):
`(12 + 1024 + 1 048 576 + 1 073 741 824) × 4 KB ≈ 4 TB`

### Plánování — Round-Robin

| Veličina | Vzorec |
|---|---|
| Efektivita CPU | `tq / (tcs + tq) × 100 %` |
| Doba odezvy zablokovaného vlákna D | `pocet_ostatnich_vlaken × (tcs + tq)` |
| Přepnutí kontextu pro CPU-bound vlákno (zdvojování kvanta) | suma: `1 + 2 + 4 + 8 + ... = N` → log2(N) přepnutí (poslední kvantum zkráceno) |

**Příklad:** vlákno potřebuje 100×T, kvantum se zdvojuje:
`1 + 2 + 4 + 8 + 16 + 32 + 37 = 100` → **7 přepnutí** (vs. 100 u fixního kvanta)

### Algoritmy náhrady stránek (srovnání)

| Algoritmus | Výpadků (příklad 12 přístupů, 3 rámce) | Implementace |
|---|---|---|
| Optimální | 6 | nelze (referenční mez) |
| NRU | 7 | jednoduchá (třídy R, D) |
| LRU | 7 | složitá / HW čítač |
| Clock | 8 | střední (kruhový buf. + R bit) |
| Aging | 9 | střední (SW simulace LRU) |
| FIFO | 9 | nejjednodušší (fronta) |

### RAID — kapacita a spolehlivost

| RAID | Využitá kapacita (m disků) | Odolnost |
|---|---|---|
| RAID 0 | `m × kapacita` (100 %) | žádná |
| RAID 1 | `1 × kapacita` (50 % pro m=2) | výpadek m-1 disků |
| RAID 10 | `m/2 × kapacita` (50 %) | výpadek 1 disku z každé zrcadlové dvojice |
| RAID 5 | `(m-1)/m × celková kapacita` | výpadek **1** disku |
| RAID 6 | `(m-2)/m × celková kapacita` | výpadek **2** disků |

**Příklad RAID 5:** 6 disků po 4 TB → využití `5/6 ≈ 83 %` → **20 TB** pro data.

**Parita v RAID 5:** `P = D0 XOR D1 XOR ... XOR D_(m-2)`. Obnova výpadlého `D_k`: `D_k = P XOR D0 XOR ... (všechna ostatní)`.

### Přístup na HDD

| Složka | Vzorec / typická hodnota |
|---|---|
| Celková doba přístupu k sektoru | `T = seek_time + rotational_delay + transfer_time` |
| Průměrné rotační zpoždění | `60 / (2 × RPM)` sekund; při 10 000 RPM → 3 ms |
| Sekvenční vs. náhodný přístup | sekvenční bývá 100–400× rychlejší než náhodný |

### FAT — limity souborového systému

```
Max. velikost FS  = 2^(počet bitů adresy) × velikost datového bloku
Max. velikost FAT = 2^(počet bitů adresy) × velikost jedné položky FAT
```

**Příklad FAT32** (28 b adresa, blok 1 KB):
- Max. FS: `2^28 × 1 KB = 256 GB`
- Max. soubor: omezen 32-bit délkovým polem → **4 GB**

### Bankéřův algoritmus — postup

```
1. Vypočti M = Q - A  (chybějící prostředky každého vlákna)
2. Algoritmus bezpečnosti:
   a) Najdi neuspokojené vlákno T: M[T] <= F?
      ANO → T označit jako hotové, F += A[T], opakuj a)
      NE  → přejdi na b)
   b) Jsou všechna vlákna označena?
      ANO → stav je BEZPEČNÝ
      NE  → stav je NEBEZPEČNÝ (zbylá vlákna jsou potenciálně uvázlá)
```

### Stránkování — struktura adresy

```
Virtuální adresa: [ číslo stránky (page#) | offset ]
Fyzická adresa:   [ číslo rámce (frame#)  | offset ]

Offset = log2(velikost stránky) bitů
Číslo stránky = (celková šířka adresy) - offset bitů
```

**Příklad:** 32-bit adresa, 4 KB stránka → 12 b offset, 20 b číslo stránky → `2^20 = 1M` stránek ve VAS.
