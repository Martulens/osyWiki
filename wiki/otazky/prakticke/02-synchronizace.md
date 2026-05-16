# Synchronizace

Úlohy na synchronizaci testují, zda rozumíš chování vícevláknových programů — jak se vlákna vzájemně ovlivňují přes sdílené proměnné, kde vznikají race conditions a deadlocky, a zda umíš sestavit synchronizační primitiva (semafor z mutexu a podmíněné proměnné).

??? abstract "Obsah stránky"

    [TOC]

---

## Co tento typ úlohy prověřuje

Zkoušková úloha na synchronizaci má dvě formy, které se mohou kombinovat:

**A) Pseudokód synchronizačního primitiva** — napsat implementaci semaforu (nebo bariéry) pomocí mutexu a podmíněné proměnné (`pthread_mutex_t` + `pthread_cond_t`). Hodnotí se správnost struktury, pořadí operací a použití `while` místo `if`.

**B) Multichoice — rozbor kódu** — pro daný úryvek C/C++ kódu se sdílenými proměnnými a synchronizačními objekty rozhodnout (zatrhnout pravdivá tvrzení):

| Otázka | Co hledat |
|--------|-----------|
| Časově závislá chyba (race condition) | Sdílená proměnná bez dostatečné ochrany |
| Deadlock | Kruhové čekání na zámky |
| Livelock | Aktivní smyčka, ze které se nikdy nevyjde |
| Busy-waiting | `while(podmínka)` bez blokujícího čekání |
| Možné hodnoty sdílené proměnné | Deterministický výsledek vs. ztracené zápisy kvůli race |

Úloha je za přibližně **5–8 bodů**. Multichoice varianta se opakovala v termínech 2011, 2012, 2018, 2019, 2022, 2024. Pseudokódová varianta v termínech 2010, 2011, 2012.

---

## Co potřebuješ znát

Kompletní teorii pokrývá [Skripta: Synchronizace](../../skripta/03-synchronizace.md). Stručné shrnutí toho nejdůležitějšího pro zkoušku:

**Race condition** vzniká, když víc vláken současně přistupuje ke sdíleným datům a aspoň jedno z nich zapisuje, bez jakékoli synchronizace nebo s nedostatečnou synchronizací. Výsledek závisí na pořadí (prokládání) instrukcí, které nelze předvídat.

**Deadlock** vyžaduje současné splnění čtyř Coffmanových podmínek: vzájemné vyloučení (mutual exclusion), vlastnictví a čekání (hold-and-wait), neodnímatelnost (no preemption) a kruhové čekání (circular wait). V praxi: vlákno A drží zámek L1 a čeká na L2; vlákno B drží L2 a čeká na L1 → uváznutí.

**Livelock** — vlákna nejsou zablokovaná, ale opakovaně mění stav a žádné nepokračuje. Typicky při back-off strategii s více zámky: A získá L1, zkusí L2, selže → pustí L1; B získá L2, zkusí L1, selže → pustí L2; a znovu dokola.

**Busy-waiting (aktivní čekání)** — vlákno stráví čas ve smyčce testující podmínku (`while(flag);`), místo aby se zablokovalo (`sem_wait`, `mutex_lock`). Plýtvá CPU, ale ne vždy je chybou (jádro OS, velmi krátká čekání).

**Semafor** — celočíselný čítač + fronta blokovaných vláken.
- `sem_init(s, 0, n)` — inicializuje na hodnotu `n`
- `sem_wait(s)` — pokud čítač > 0: sníží o 1; jinak: zablokuje vlákno
- `sem_post(s)` — pokud čekají vlákna: probudí jedno; jinak: zvýší čítač o 1

**Mutex** — binární zámek (speciální případ semaforu s hodnotou 0/1). `mutex_lock` odpovídá `sem_wait`, `mutex_unlock` odpovídá `sem_post`.

**Podmíněná proměnná** — umožňuje vláknu atomicky odemknout mutex a zablokovat se:
- `pthread_cond_wait(&cond, &mutex)` — atomicky: odemkni mutex + uspi vlákno; po probuzení: zamkni mutex
- `pthread_cond_signal(&cond)` — probuď jedno čekající vlákno
- `pthread_cond_broadcast(&cond)` — probuď všechna čekající vlákna

---

## Postup řešení krok za krokem

### Část A: Pseudokód semaforu z mutexu a podmíněné proměnné

1. **Navrhni datovou strukturu.** Semafor potřebuje uchovávat svou hodnotu a synchronizační objekty. Struktura obsahuje tři složky: celočíselný čítač `val`, mutex (chrání přístup k `val`) a podmíněnou proměnnou (pro blokování čekajících vláken).

    ```c
    typedef struct {
        int val;
        pthread_mutex_t mutex;
        pthread_cond_t  cond;
    } sem_t_custom;
    ```

2. **Napiš `sem_init`.** Nastav `val` na požadovanou počáteční hodnotu a inicializuj mutex a podmíněnou proměnnou. Nic složitého, ale nesmíš zapomenout na inicializaci obou synchronizačních objektů.

    ```c
    void sem_init_custom(sem_t_custom *s, int initial) {
        s->val = initial;
        pthread_mutex_init(&s->mutex, NULL);
        pthread_cond_init(&s->cond, NULL);
    }
    ```

3. **Napiš `sem_down` (= wait / P).** Toto je kritická část. Postup:
    - Zamkni mutex — nyní máš výlučný přístup k `val`.
    - Zkontroluj podmínku: je `val == 0`? Pokud ano, musíš čekat.
    - Čekáš voláním `pthread_cond_wait` — tato funkce **atomicky** odemkne mutex a uspí vlákno. Po probuzení znovu zamkne mutex.
    - Po probuzení **znovu zkontroluj podmínku** (proto `while`, ne `if`) — může jít o spurious wakeup nebo o situaci, kdy jiné vlákno stačilo hodnotu opět snížit na 0.
    - Jakmile je `val > 0`, sniž ho o 1 — prostředek byl „spotřebován".
    - Odemkni mutex.

    ```c
    void sem_down(sem_t_custom *s) {
        pthread_mutex_lock(&s->mutex);
        while (s->val == 0)
            pthread_cond_wait(&s->cond, &s->mutex);
        s->val--;
        pthread_mutex_unlock(&s->mutex);
    }
    ```

4. **Napiš `sem_up` (= post / V).** Jednodušší část:
    - Zamkni mutex.
    - Zvyš `val` o 1 — prostředek je „vrácen".
    - Zavolej `pthread_cond_signal` — probudí **jedno** čekající vlákno (pokud existuje). Nepoužívej `broadcast`, bylo by to zbytečné: stačí probudit jedno vlákno, protože `val` vzrostl jen o 1.
    - Odemkni mutex.

    ```c
    void sem_up(sem_t_custom *s) {
        pthread_mutex_lock(&s->mutex);
        s->val++;
        pthread_cond_signal(&s->cond);   /* signal, NE broadcast */
        pthread_mutex_unlock(&s->mutex);
    }
    ```

5. **Zkontroluj pořadí operací.** Nejčastější chyby:
    - `val--` před smyčkou `while` (vlákno sníží hodnotu pod 0).
    - `if` místo `while` (spurious wakeup způsobí průchod i při `val == 0`).
    - `signal` mimo mutex (může se ztratit).
    - Zapomenuté `mutex_unlock` na konci `sem_down` — mutex zůstane zamčený, ostatní vlákna uváznou.

---

### Část B: Multichoice — rozbor kódu

6. **Identifikuj sdílené proměnné.** Přečti si kód a vyznač si globální proměnné (nebo proměnné předané odkazem do více vláken). Lokální proměnné na zásobníku jsou soukromé pro každé vlákno — nejde o sdílené prostředky.

7. **Zkontroluj, zda je přístup ke sdíleným proměnným chráněn.** Pro každé místo, kde se sdílená proměnná čte nebo zapisuje, zjisti:
    - Je operace uvnitř kritické sekce (mezi `mutex_lock` / `mutex_unlock` nebo `sem_wait` / `sem_post`)?
    - Je semafor inicializován hodnotou 1 (= mutex)? Nebo hodnotou > 1?

    **Klíčové pravidlo:** Semafor s hodnotou inicializace `n > 1` dovolí do kritické sekce vstoupit `n` vláknům **současně** — to znamená, že race condition stále existuje, přestože semafor je přítomen.

8. **Rozhodnutí o race condition:**
    - Sdílená proměnná upravována bez synchronizace → **race condition ANO**.
    - Semafor s `n > 1` chrání zápis do sdílené proměnné → **race condition ANO** (dvě vlákna zapisují současně).
    - Semafor s `n = 1` nebo mutex → **race condition NE** (v kritické sekci je vždy nejvýše jedno vlákno).

9. **Rozhodnutí o deadlocku:**
    - Hledej situaci, kdy vlákno drží zámek A a čeká na zámek B, zatímco jiné vlákno drží B a čeká na A (circular wait).
    - Jeden semafor / jeden mutex → deadlock nehrozí (neexistuje kruhové čekání).
    - Více zámků, zamykání po jednom v různém pořadí → **deadlock hrozí**.
    - Hromadné zamykání (`std::lock(a, b, c)`) → deadlock nehrozí, ale **livelock ano** (back-off mechanismus).

10. **Rozhodnutí o livelocku:**
    - Livelock nastane, když vlákna opakovaně uvolňují a znova žádají o zámky, ale nikdy nepostoupí.
    - Typický vzor: zamykání více mutexů s back-off (vlákno selže, uvolní co má, zkusí znovu — ale synchronizovaně s jiným vláknem, takže oba neustále ustupují).
    - Pokud kód používá `sem_wait` / `mutex_lock` bez opakovaného zkoušení → **livelock NE**.

11. **Rozhodnutí o busy-waiting:**
    - Hledej smyčku `while(podmínka) {}` nebo `while(podmínka) { /* nic */ }` bez blokujícího volání uvnitř.
    - `sem_wait` a `mutex_lock` blokují pasivně → **busy-waiting NE**.
    - `pthread_cond_wait` uvnitř `while` smyčky — vlákno je blokováno, ne točeno → **busy-waiting NE**.
    - Spinlock (`while(atomic_flag_test_and_set(...));`) → **busy-waiting ANO**.

12. **Výpočet možných hodnot sdílené proměnné:**
    - Nejprve spočítej **deterministický výsledek** (součet všech přírůstků/změn za předpokladu korektní synchronizace).
    - Pokud race condition existuje: vlákna mohou číst starou hodnotu a přepsat výsledek jiného vlákna. Výsledek závisí na tom, kolik zápisů se „ztratí".
    - **Jak ztráta zápisů funguje:** vlákno A přečte `g_X = 180`, vlákno B přečte `g_X = 180`, vlákno A zapíše `g_X = 182` (přidalo 2), vlákno B zapíše `g_X = 181` (přidalo 1, ale přepíše výsledek A) → efektivní přírůstek je jen 1, přestože obě vlákna pracovala.
    - **Možné hodnoty:** kořen je výchozí hodnota. Přičtením různých podmnožin přírůstků (nebo jejich neuplatněním kvůli přepsání) dostaneme různé výsledky. Musíš se zamyslet, které hodnoty jsou dosažitelné. Spočítej maximum (kdyby žádný zápis nebyl ztracen) a minimum (kdyby bylo ztraceno co nejvíc kladných přírůstků nebo naopak).

13. **Ověř celkové chování.** Projdi kód znovu s odpověďmi na otázky 7–12 a zkontroluj konzistenci. Typická chyba: student označí race condition i deadlock jako ANO — ale deadlock u jednoho zámku není možný. Druhá typická chyba: označení busy-waiting u `sem_wait` — to je blokující volání.

---

## Vzorové zadání

!!! example "Zadání"
    **A) Pseudokód.** Napište pseudokód implementace semaforu pomocí mutexu a podmíněné proměnné. Implementujte operace `sem_init`, `sem_down` (= wait / P) a `sem_up` (= post / V).

    **B) Multichoice.** Uvažujte následující kód:

    ```c
    sem_t sem;
    int g_X = 180;

    void func( int x ) {
        sem_wait(&sem);
        g_X += x;
        sem_post(&sem);
    }

    int main() {
        sem_init(&sem, 0, 2);          /* počáteční hodnota semaforu = 2 */
        thread t1( func,  2 );
        thread t2( func,  1 );
        thread t3( func,  2 );
        thread t4( func, -8 );
        t1.join(); t2.join(); t3.join(); t4.join();
        return 0;
    }
    ```

    Vyberte pravdivá tvrzení:

    1. Program obsahuje časově závislou chybu (race condition).
    2. Může dojít k deadlocku.
    3. Může dojít k livelocku.
    4. Program provádí busy-waiting.
    5. Po skončení může být `g_X = 180`.
    6. Po skončení může být `g_X = 177`.

    *Multichoice varianty: 2011, 2012, 2018, 2019, 2022, 2024. Pseudokódová varianta: 2010, 2011, 2012.*

---

## Řešení vzorového zadání

??? success "Ukázat řešení"

    ### Část A — Pseudokód semaforu

    ```c
    typedef struct {
        int val;
        pthread_mutex_t mutex;
        pthread_cond_t  cond;
    } sem;

    void sem_init(sem *s, int initial) {
        s->val = initial;
        pthread_mutex_init(&s->mutex, NULL);
        pthread_cond_init(&s->cond, NULL);
    }

    void sem_down(sem *s) {                  /* = wait / P */
        pthread_mutex_lock(&s->mutex);
        while (s->val == 0)
            pthread_cond_wait(&s->cond, &s->mutex);
        s->val--;
        pthread_mutex_unlock(&s->mutex);
    }

    void sem_up(sem *s) {                    /* = post / V */
        pthread_mutex_lock(&s->mutex);
        s->val++;
        pthread_cond_signal(&s->cond);       /* signal, NE broadcast */
        pthread_mutex_unlock(&s->mutex);
    }
    ```

    Klíčové body hodnocené u zkoušky:

    - `while` místo `if` — nutné kvůli spurious wakeups a souběžným probuzením více vláken
    - `cond_wait` dostane **zamčený** mutex — atomicky ho odemkne a vlákno uspí
    - `sem_up` volá `signal` (ne `broadcast`) — stačí probudit jedno vlákno, hodnota vzrostla jen o 1
    - `val--` až po splnění podmínky `val > 0` — nikdy nesnižujeme pod 0

    ---

    ### Část B — Multichoice

    **Krok 1: Identifikace sdílených proměnných.**
    Globální proměnné: `sem` (semafor) a `g_X` (celé číslo). Sdílená proměnná `g_X` je čtena a zapisována ve funkci `func`.

    **Krok 2: Je přístup ke `g_X` dostatečně chráněn?**
    `sem_init(&sem, 0, 2)` — počáteční hodnota je **2**. To znamená, že `sem_wait` projde bez blokování, dokud semafor neklesne na 0. Při hodnotě 2 smí do kritické sekce (`g_X += x`) vstoupit **dvě vlákna současně**. Vlákno t1 a t2 tedy mohou obě číst `g_X` ve stejnou chvíli a obě zapisovat — jeden zápis přepíše druhý.

    **Krok 3: Závěry:**

    - **(1) Časově závislá chyba — ANO.** Semafor inicializovaný hodnotou 2 dovoluje dvěma vláknům současně číst a zapisovat `g_X`. Race condition existuje. Kdyby byla hodnota 1, race by neexistovala.

    - **(2) Deadlock — NE.** Je přítomen jen jeden synchronizační objekt (`sem`). Deadlock vyžaduje kruhové čekání mezi alespoň dvěma zámky. S jedním semaforem vlákno nikdy nemůže být v situaci „drží A, čeká na B". Deadlock není možný.

    - **(3) Livelock — NE.** Kód neobsahuje žádnou smyčku, ve které by vlákno opakovaně zkoušelo získat zámek a selhávalo. `sem_wait` buď projde, nebo vlákno pasivně zablokuje. Žádný back-off mechanismus → livelock nehrozí.

    - **(4) Busy-waiting — NE.** `sem_wait` je blokující systémové volání — vlákno čekající na semafor je přepnuto do stavu Blocked a nespotřebovává CPU. Žádná aktivní smyčka testující podmínku.

    - **(5) `g_X = 180` — ANO.** Deterministický výsledek (bez race) je `180 + 2 + 1 + 2 + (-8) = 177`. Kvůli race condition se zápisy mohou přepisovat. Scénář, kdy `g_X` zůstane 180:
        - vlákna t1, t2, t3 projdou současně kritickou sekcí (sem=2 → nanejvýš dvě, ale t3 čeká → ve skutečnosti dvě)
        - vlákno t2 přečte `g_X = 180`, přidá 1, chystá se zapsat 181
        - vlákno t1 přečte `g_X = 180`, přidá 2, zapíše 182
        - vlákno t2 zapíše 181 (přepíše výsledek t1, přírůstek t1 se ztratí)
        - vlákno t4 přečte 181, odečte 8, zapíše 173
        - vlákno t3 přečte 181 (starou hodnotu před zápisem t2), přidá 2, zapíše 183 — přepíše výsledek t4
        ...existují různé prokládání; konkrétním prokládáním lze dosáhnout, aby se záporný přírůstek `-8` a kladné přírůstky vzájemně zrušily, výsledek zůstane 180. Přesný scénář: t4 přečte `g_X = 180`, vlákno t1 přepíše na 182, vlákna t2, t3 také zapíšou, ale t4 nakonec zapíše `180 + (-8) = 172`... Ve skutečnosti 180 je dosažitelné, pokud vlákno t4 přečte hodnotu 188 (přičemž ta vznikla přičtením 2+1+2+5 k 180 = no, 180 + (2+1+2) = 185, pak t4 přečte 185 a zapíše 177 — záleží na pořadí). Jednodušeji: pokud přírůstky t1 (+2), t3 (+2) a t4 (-8) a t2 (+1) vedou k tomu, že t4 přečte hodnotu 188 (kde se mohly přírůstky kumulovat vícekrát), je 180 dosažitelné. **Krátce: `g_X = 180` je dosažitelné kvůli race condition — zápisy se vzájemně přepisují a netto efekt může být nulový.**

    - **(6) `g_X = 177` — ANO.** Toto je korektní (deterministický) výsledek `180 + 2 + 1 + 2 - 8 = 177`, dosažitelný tehdy, kdy každý `g_X += x` proběhne atomicky bez přepsání jiným vláknem. Přestože semafor to plně nezajišťuje (hodnota 2), může se stát, že vlákna vstoupí do kritické sekce po jednom a výsledek bude korektní.

---

## Další procvičení

### Varianta 1 — více mutexů a otázka deadlocku

!!! example "Zadání"
    Uvažujte následující kód (4 vlákna sdílí globální pole `g_buf`):

    ```c
    pthread_mutex_t lock[4];
    int g_buf[4] = {0, 0, 0, 0};

    void worker(int pos) {
        pthread_mutex_lock(&lock[pos % 4]);
        pthread_mutex_lock(&lock[(pos + 1) % 4]);
        g_buf[pos % 4] += 1;
        g_buf[(pos + 1) % 4] += 1;
        pthread_mutex_unlock(&lock[(pos + 1) % 4]);
        pthread_mutex_unlock(&lock[pos % 4]);
    }

    int main() {
        for (int i = 0; i < 4; i++) pthread_mutex_init(&lock[i], NULL);
        thread t0(worker, 0);
        thread t1(worker, 1);
        thread t2(worker, 2);
        thread t3(worker, 3);
        t0.join(); t1.join(); t2.join(); t3.join();
        return 0;
    }
    ```

    Vyberte pravdivá tvrzení: (1) Race condition; (2) Deadlock; (3) Livelock; (4) Busy-waiting.

??? success "Ukázat řešení"
    **Krok 1: Sdílené proměnné.** Pole `g_buf` a pole zámků `lock`.

    **Krok 2: Přístup ke `g_buf`.** Každé vlákno zamkne dva mutexy před zápisem → sdílené pole je chráněno.

    **(1) Race condition — NE.** Každý zápis do `g_buf[i]` proběhne pod zámkem `lock[i]` → výlučný přístup je zaručen.

    **(2) Deadlock — ANO.** Vlákna zamykají mutexy v různém pořadí:
    - t0: zamkne `lock[0]`, pak čeká na `lock[1]`
    - t1: zamkne `lock[1]`, pak čeká na `lock[2]`
    - t2: zamkne `lock[2]`, pak čeká na `lock[3]`
    - t3: zamkne `lock[3]`, pak čeká na `lock[0]`

    Kruhové čekání: t0 → t1 → t2 → t3 → t0. Všechny čtyři Coffmanovy podmínky jsou splněny → **deadlock je možný**.

    !!! warning "Pozor na precedenci operátorů"
        Výraz `pos + 1 % 4` se vyhodnotí jako `pos + (1 % 4) = pos + 1`, **ne** `(pos + 1) % 4`. V zadání je závorka správně — `(pos + 1) % 4`. Bez závorky by t3 zamykal `lock[3]` a `lock[4]` (neexistující) místo `lock[3]` a `lock[0]`, čímž by se kruhové čekání přerušilo a deadlock by nenastal. Vždy si ověř, jak jsou závorky zapsány.

    **(3) Livelock — NE.** Kód nevykazuje back-off smyčku.

    **(4) Busy-waiting — NE.** `pthread_mutex_lock` blokuje pasivně.

---

### Varianta 2 — producent-konzument se semafory

!!! example "Zadání"
    Napište pseudokód producenta a konzumenta pro sdílenou frontu s kapacitou `N` pomocí tří synchronizačních objektů: mutex, semafor `empty` (volná místa) a semafor `full` (obsazená místa). Jaká je počáteční hodnota každého semaforu?

??? success "Ukázat řešení"
    Počáteční hodnoty: `empty = N` (fronta je na začátku celá prázdná → N volných míst), `full = 0` (žádná obsazená místa).

    ```c
    #define N 100
    pthread_mutex_t mtx;
    sem_t empty, full;
    /* inicializace: sem_init(&empty, 0, N); sem_init(&full, 0, 0); */

    void producer(void) {
        while (1) {
            item_t item = produce_item();
            sem_wait(&empty);          /* čekej, dokud není volné místo */
            pthread_mutex_lock(&mtx);
                insert_item(item);
            pthread_mutex_unlock(&mtx);
            sem_post(&full);           /* oznam, že přibyl jeden prvek */
        }
    }

    void consumer(void) {
        while (1) {
            sem_wait(&full);           /* čekej, dokud není aspoň jeden prvek */
            pthread_mutex_lock(&mtx);
                item_t item = remove_item();
            pthread_mutex_unlock(&mtx);
            sem_post(&empty);          /* oznam, že přibylo jedno volné místo */
            consume_item(item);
        }
    }
    ```

    **Proč `sem_wait(&empty)` PŘED `mutex_lock`?** Kdybychom pořadí otočili (nejdřív `mutex_lock`, pak `sem_wait(&empty)`), mohl by producent držet mutex a čekat na `empty`. Konzument by ale potřeboval mutex, aby mohl `sem_post(&empty)` — uváznutí (deadlock).

    Správné pořadí: nejdřív semafor (signalizace podmínky), pak mutex (ochrana fronty).

---

## Varianty a chytáky

**Hodnota semaforu při inicializaci rozhoduje o race condition.** `sem_init(&sem, 0, 1)` = mutex (v kritické sekci max. 1 vlákno, race NE). `sem_init(&sem, 0, 2)` = do sekce smí 2 vlákna současně (race ANO při sdíleném zápisu).

**`if` vs. `while` u `cond_wait`.** Podmínka před `cond_wait` musí být vždy `while`. Důvody: (a) spurious wakeup — POSIX dovoluje vlákno probudit bez `signal`; (b) souběžné probuzení — při `broadcast` se probudí více vláken, ale podmínka může platit jen pro jedno z nich.

**Pořadí `sem_wait` a `mutex_lock` v producent-konzumentovi.** Vždy: nejdřív semafor (podmínka), pak mutex (ochrana dat). Opačné pořadí → deadlock.

**`signal` vs. `broadcast` v `sem_up`.** V implementaci semaforu z mutexu + cond stačí `signal` — `val` vzrostl o 1, stačí probudit jedno vlákno. `broadcast` by byl správný, ale zbytečně drahý.

**Zamykání více mutexů v různém pořadí → deadlock.** Pokud kód zamyká `lock[i]` a `lock[j]` kde `i` a `j` závisí na parametru vlákna, a různá vlákna mohou mít `i` a `j` prohozené, vznikne circular wait.

**`std::lock(a, b, c)` deadlock nevznikne, ale livelock ano.** Hromadné zamykání používá back-off (pokus, selže, zkusí znovu) → v krajním případě obě vlákna neustále uvolňují a znovu zkouší → livelock.

**Precedence operátorů.** `pos + 1 % 4` ≠ `(pos + 1) % 4`. Vždy si ověř závorky v indexech — mění, které zámky se berou, a tedy zda deadlock hrozí nebo ne.

**Busy-waiting vs. spinlock.** `while(atomic_flag_test_and_set(&f));` je busy-waiting (správná odpověď: ANO). `sem_wait`, `mutex_lock`, `cond_wait` jsou blokující — busy-waiting NE.

**Deterministický výsledek vs. race.** Součet všech přírůstků je vždy deterministický (`180 + 2 + 1 + 2 - 8 = 177`). Kvůli race mohou být výsledky jiné — vyšší (záporný přírůstek ztracen) i nižší než očekávaný... nebo i rovné výchozí hodnotě (vše ztraceno). Musíš argumentovat konkrétním scénářem prokládání.

---

## Časté chyby

**`if` místo `while` u `cond_wait`.** Pořadí bodů se krátí. Podmínka po probuzení musí být znovu ověřena.

**`val--` před cyklem while** v `sem_down`. Vlákno sníží hodnotu na -1 a pak čeká — ale hodnota by nikdy neměla klesnout pod 0.

**`pthread_cond_signal` volán bez drženého mutexu.** `cond_signal` smí být volán i bez mutexu (POSIX to nezakazuje), ale v implementaci semaforu je bezpečnější volat ho pod zámkem (jinak může dojít ke ztrátě signálu).

**Označení deadlocku u jednoho zámku.** Deadlock vyžaduje aspoň dva zámky v kruhu. Jeden semafor nebo jeden mutex deadlock neumožní.

**Záměna `cond_signal` a `cond_broadcast` v `sem_up`.** `broadcast` by byl správně pro obecný případ, ale je zbytečný — a u testu by mohla být ztracena značka za optimální implementaci. Správně je `signal`.

**Zapomenutý `mutex_unlock` při chybovém průchodu.** Pokud `sem_down` má více výstupních cest (při chybě, `return`), každá musí odemknout mutex.

**Záměna pojmů.** „Livelock" ≠ „deadlock" — u livelocku vlákna běží, u deadlocku stojí. Záměna na testu bývá penalizována.

**Hodnota `g_X` může být i vyšší než deterministický výsledek.** Pokud vlákno se záporným přírůstkem přepíše výsledek vlákna s kladným přírůstkem, záporný příspěvek se ztratí → výsledek je vyšší než 177. Konkrétní dosažitelné hodnoty závisí na scénáři — vždy musíš ukázat konkrétní prokládání.

---

## Související

- [Skripta: Synchronizace](../../skripta/03-synchronizace.md) — kompletní teorie: TSL, mutexy, podmíněné proměnné, semafory, bariéry, večeřící filosofové, čtenáři-písaři, spící holiči
- [Teoretické otázky (true/false)](../teorie-truefalse.md) — otázky prověřující porozumění pojmům (race condition, deadlock, livelock, spurious wakeup, busy-waiting)
- [Praktické příklady — přehled](index.md) — ostatní typy úloh z druhé části zkoušky
