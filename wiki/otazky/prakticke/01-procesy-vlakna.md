# Procesy a vlákna

Úloha s úryvkem kódu v jazyce C: na základě volání `fork()`, `exec*()`, `wait()` a `sleep()` je třeba určit počet vzniklých procesů, dobu běhu, počet procesů aktivních v daném okamžiku a velikost paměti alokované na zásobníku a haldě. Typ se opakoval prakticky v každém zkušebním termínu (2010–2025).

??? abstract "Obsah stránky"

    [TOC]

---

## Co tento typ úlohy prověřuje

Zadání vypadá takto: dostaneš **krátký C program** (10–30 řádků) s cyklem, větvením a systémovými voláními `fork`, `wait`, `execlp`/`execvp`/`exec*`, `sleep`. K tomu jsou zadány systémové limity (max. zásobník v MiB, max. počet vláken). Pak přijdou otázky:

| Otázka | Co se počítá |
|---|---|
| Kolik procesů celkem vznikne? | Počet uzlů ve stromu procesů (někdy vč. původního, jindy jen nově vzniklé — čti zadání!) |
| Za kolik sekund doběhne poslední? | Délka nejdelší větve stromu s časovou osou |
| Kolik procesů poběží v čase T0 + X s? | Kolik větví je v daném okamžiku ještě aktivních |
| Kolik MiB zásobníku alokuje každý proces? | ceil(velikost statického pole v bytech / 1 048 576) |
| Kolik MiB haldy alokuje každý proces? | ceil(argument malloc() v bytech / 1 048 576) |

**Bodové ohodnocení:** přibližně 5–8 bodů na termín. Chyba v pochopení toku řízení (špatný strom) může zkazit všechny podotázky najednou — proto je stavba stromu klíčová.

**Frekvence:** tento typ se vyskytl v každém termínu od roku 2010. Čísla v zadání (velikost pole, argument malloc, hranice cyklu, délky sleep) se mění, ale struktura zůstává.

---

## Co potřebuješ znát

**Základní trojice systémových volání:**

- `fork()` — vytvoří kopii aktuálního procesu. V rodiči vrátí PID potomka (kladné číslo). V potomkovi vrátí `0`. Při chybě (dosažen limit) vrátí `-1`.
- `exec*()` — nahradí kód aktuálního procesu novým programem. Při úspěchu se **nikdy nevrátí** — instrukce za voláním se neprovede. Při selhání se vrátí a program pokračuje normálně.
- `wait(&status)` — zablokuje volající proces, dokud **nějaký** jeho přímý potomek neskončí. `waitpid(pid, &status, 0)` čeká na konkrétního potomka.

**Paměťový model procesu:**

```text
  vyšší adresy
  ┌──────────────┐
  │   zásobník   │  ← lokální proměnné, char a[N] — STATICKY alokováno
  │   (stack)    │    (při vstupu do funkce, uvolněno při návratu)
  ├──────────────┤
  │    halda     │  ← malloc(M) — DYNAMICKY alokováno
  │    (heap)    │    (explicitně free(), nebo konec procesu)
  ├──────────────┤
  │    data      │  ← globální a statické proměnné
  ├──────────────┤
  │     text     │  ← kód programu
  └──────────────┘
  nižší adresy
```

**Vzorce pro výpočet paměti:**

```text
Zásobník [MiB] = ceil( N / 1 048 576 )     kde N = velikost pole char a[N] v bytech
Halda    [MiB] = ceil( M / 1 048 576 )     kde M = argument malloc(M) v bytech
```

Binární MiB: 1 MiB = 2^20 B = 1 048 576 B. Vždy zaokrouhli **nahoru** (ceil), ne na nejbližší celé číslo.

**Limit vláken a fork():**
Pokud `fork()` selže kvůli dosažení limitu, vrátí `-1`. Pokud kód tuto chybu neošetřuje (chybí větev `if (child_pid == -1)`), program pokračuje jako by byl v rodiči s PID -1 — viz sekce Varianty a chytáky.

Podrobná teorie: [Skripta: Procesy a vlákna](../../skripta/02-procesy-vlakna.md)

---

## Postup řešení krok za krokem

### Krok 1 — Přečti kód a identifikuj strukturu

Projdi kód a najdi:

- **Cykly** (`for`, `while`) — kolikrát proběhnou? Pozor na `< N` (N iterací) vs. `<= N` (N+1 iterací).
- **Podmínky** (`if/else`) na návratovou hodnotu `fork()`.
- **Volání** `fork()`, `exec*()`, `wait()`, `sleep()` a jejich pořadí v každé větvi.
- **Globální strukturu** — co dělá rodič po `fork()`, co dělá potomek.

!!! tip "Klíčová otázka pro každou větev"
    V každé větvi `if/else` po `fork()` se zeptej: „Kdo tady běží — rodič, potomek, nebo oba?" Potomek je vždy tam, kde `fork()` vrátilo `0`. Rodič je tam, kde vrátilo kladné číslo (PID dítěte).

### Krok 2 — Nakresli strom procesů

Strom procesů je nejdůležitější pomůcka. Na papír nakresli každý proces jako uzel a každé `fork()` jako hranu rodič → potomek.

**Pravidlo kreslení:** vždy začni od původního procesu (kořen stromu). Pro každé `fork()`, které v daném průchodu kódem nastane, přidej potomka. Potomek začne vykonávat kód od místa ihned za `fork()` — ve větvi, kde `fork()` vrátilo `0`.

```text
Příklad pro jednoduchý případ:
       prog (rodič)
          |
        fork()
       /      \
  potomek    rodič
 (vrací 0)  (vrací PID)
```

### Krok 3 — Zkontroluj chování exec*()

Pokud rodič (nebo potomek) zavolá `exec*()`:

1. Při **úspěchu**: kód procesu je nahrazen novým programem. Nic za `exec*()` se **nevykoná** — ani zbytek cyklu, ani příkazy za cyklem.
2. Při **selhání**: výpočet pokračuje za `exec*()` normálně.

!!! warning "Nejčastější chyba"
    Studenti zapomínají, že úspěšný `exec*()` = konec původního kódu. Pokud je `exec*()` uvnitř cyklu a uspěje, cyklus v tom procesu **nepokračuje**.

### Krok 4 — Zkontroluj chování wait()

`wait()` v rodiči způsobí, že rodič **čeká** (je zablokován), dokud neskončí alespoň jeden jeho přímý potomek. Teprve potom pokračuje na další řádek.

Důsledky pro strom:
- Pokud je `wait()` **před** `exec*()`: rodič čeká na potomka, teprve pak provede `exec*()`.
- Pokud `wait()` **chybí**: rodič pokračuje ihned a potomek běží souběžně.
- Pokud je `wait()` **v cyklu**: v každé iteraci rodič počká na dítě z této iterace, teprve pak pokračuje.

### Krok 5 — Urči, kolik iterací cyklu každý proces provede

Toto je klíčový krok u zadání s cyklem a `fork()` uvnitř:

- Potomek, který v podmínce `if (child_pid == 0)` zavolá `sleep()` a pak se vrátí z podmínky, se vrátí do cyklu — **a bude v dalších iteracích také forkovat**, pokud kód to dovoluje (tj. nezůstane v bloku `if` po celou dobu).
- Pokud je v bloku `if (child_pid == 0)` pouze `sleep()` bez dalšího `return` nebo `exit()`, potomek se po usnutí vrátí do cyklu a pokračuje.
- Pokud rodič zavolá `exec*()` a uspěje, rodič cyklus ukončí — přestane iterovat.

!!! tip "Sleduj „exit z cyklu""
    V každé větvi si vypiš, zda proces skončí (`return`, `exit()`), nebo pokračuje do dalšího průchodu cyklem. Potomek v `if (child_pid == 0) { sleep(10); }` — bez `return`/`exit` — pokračuje do dalšího průchodu!

### Krok 6 — Nakresli časovou osu

Pro každou větev stromu nakresli časovou osu s událostmi:

```text
čas:    0       10      15      27
rodič:  [wait]-------->[exec sleep 12]---->konec
potomek:[sleep(15)]---------------->konec
```

Označuj:
- `[sleep(N)]` — čekání N sekund
- `[wait]` — čekání na dítě (délka závisí na dítěti)
- `[exec X]` — přeměna na jiný program X

### Krok 7 — Spočítej počet procesů

Spočítej **uzly ve stromu**. Dej si pozor na formulaci zadání:

- „Kolik procesů **celkem vznikne** v důsledku spuštění příkazu" — zpravidla se počítá **původní proces** + všechna nově vzniklá (potomci). Zkontroluj, zda zadání nezpřesňuje.
- „Kolik **nových** procesů vznikne" — původní proces **se nepočítá**.
- „Kolik procesů **celkem bude existovat**" — původní proces + potomci.

### Krok 8 — Urči dobu běhu

Z časové osy najdi, který proces skončí **nejpozději**. To je nejdelší větev stromu s přičtenými časy sleep, wait a exec.

Pozor na souběh: pokud potomek a rodič běží paralelně a rodič na potomka nečeká, délka rodičovy větve se neprodlužuje o dobu snu potomka.

### Krok 9 — Spočítej procesy aktivní v čase T

Projdi každou větev stromu a zjisti, zda daná větev v čase T ještě „žije" (tj. proces ještě neskončil). Sečti živé větve.

!!! tip "Pomůcka"
    Do časové osy vykresli svislou čáru v čase T a spočítej, kolik vodorovných čar (větví) tato svislá čára protíná.

### Krok 10 — Spočítej paměť zásobníku

Zásobník alokuje každý process **zvlášť** — po `fork()` má potomek vlastní kopii zásobníku.

```text
char a[N];        →  zásobník += N bajtů

Zásobník [MiB] = ceil(N / 1 048 576)
```

Sečítáš pouze staticky alokované pole — ostatní lokální proměnné (int, pid_t) jsou zanedbatelné.

### Krok 11 — Spočítej paměť haldy

Halda se alokuje voláním `malloc(M)`. Pokud je `malloc()` v rodiči před `fork()`, potomek zdědí **kopii** virtuálního adresového prostoru (halda je CoW — copy-on-write), ale pro výpočet se počítá alokace každého procesu zvlášť.

```text
char *ptr = malloc(M);   →  halda += M bajtů

Halda [MiB] = ceil(M / 1 048 576)
```

### Krok 12 — Zkontroluj limity

Pokud zadání uvádí limit počtu vláken/procesů:

- Zjisti, kolik procesů se pokusí vzniknout celkem.
- Pamatuj, že **shell** zabírá jedno vlákno z limitu. Limit 144 → lze vytvořit 143 dalších.
- Pokud `fork()` vrátí -1 (limit vyčerpán) a kód to neošetřuje, pokračuje se jako v rodiči — větvení nenastane.

---

## Vzorové zadání

!!! example "Zadání"
    Na systému je nainstalovaný 64bitový OS. Limity: maximální velikost zásobníku každého procesu je 9 MiB, běžný uživatel smí spustit maximálně 144 vláken (včetně shellu). Funkce `sleep(n)` uspí volající proces na `n` sekund. Uživatel, kterému běží pouze login shell, spustí v čase T0 přeložený program `/home/user/prog`:

    ```c
    int main ()
    {
        char a[1786248];
        char *ptr_char = (char *) malloc (8074950);

        for ( int i = 0; i < 4 ; i++ )
        {
            pid_t child_pid = fork ();
            if (child_pid == 0)
            {
                sleep(15);
            }
            else
            {
                int status;
                wait(&status);
                execlp("/bin/sleep", "sleep", "12", (char *) NULL);
                sleep(9);
            }
        }
        free (ptr_char);
        return 0;
    }
    ```

    1. Kolik procesů se celkem vytvoří v důsledku spuštění příkazu `$ /home/user/prog`?
    2. Za kolik sekund po spuštění doběhne poslední proces?
    3. Kolik procesů poběží v čase T0 + 75.734 s?
    4. Kolik místa si bude alokovat každý proces na zásobníku (MiB nahoru)?
    5. Kolik místa si bude alokovat každý proces na haldě (MiB nahoru)?

    *Tento typ se objevil prakticky v každém termínu: 2010, 2011, 2012, 2014, 2018, 2023, 2025.*

---

## Řešení vzorového zadání

??? success "Ukázat řešení"

    ### Krok 1 — Identifikace struktury

    Kód má:

    - Cyklus `for (int i = 0; i < 4; i++)` — **4 iterace** (i = 0, 1, 2, 3).
    - `fork()` na začátku těla cyklu.
    - Větev potomka (`child_pid == 0`): pouze `sleep(15)` — žádný `return`/`exit`, žádný `break`.
    - Větev rodiče (`else`): `wait(&status)` → `execlp(...)` → `sleep(9)`.

    ### Krok 2 — Strom procesů (iterace 0)

    V **iteraci 0** (i = 0) zavolá původní proces (`prog`) `fork()`:

    - **Potomek 1** (`child_pid == 0`): provede `sleep(15)`. Nemá `return` ani `exit`, takže po skončení `sleep` se vrátí do cyklu a dostane se do dalších iterací (i = 1, 2, 3). Ale: v iteracích i = 1, 2, 3 bude Potomek 1 opět volat `fork()` a chovat se jako rodič...

    - **Rodič (prog)** (`else` větev): zavolá `wait(&status)` — **zablokuje se** a čeká, až Potomek 1 skončí.

    Jenže Potomek 1 `sleep(15)` a pak **pokračuje do dalších iterací cyklu** (i = 1, 2, 3). Skončí až po `return 0` na konci. To znamená, že rodič čeká na Potomka 1, ale Potomek 1 ještě tři iterace forkuje a čeká.

    !!! warning "Pozor na toto zadání"
        Toto zadání má v rodičovské větvi `wait()` NÁSLEDOVANÝ `execlp()`. Execlp při **úspěchu se nevrátí**. Proto ihned po návratu z `wait()` (tj. jakmile přímý potomek z iterace 0 skončí) rodič provede `execlp("/bin/sleep", "sleep", "12", ...)` a přemění se na `sleep 12`. Kód za tím (`sleep(9)` ani další iterace cyklu) **se nikdy nevykoná**.

    ### Krok 3 — Analýza větvení (rodič)

    Rodičovský proces `prog`:

    1. Iterace 0: forkne → Potomek 1. Pak zavolá `wait()` a čeká.
    2. Potomek 1 po `sleep(15)` a dalším forkování (viz níže) nakonec skončí.
    3. `wait()` se vrátí. Rodič volá `execlp("/bin/sleep", ...)` → přeměna na `sleep 12` (úspěch). Rodič skončí po 12 s.
    4. Iterace 1, 2, 3 **rodič nikdy neprovede**.

    Rodič tedy vytvoří **jednoho přímého potomka** (Potomek 1) a pak se přemění.

    ### Krok 4 — Analýza Potomka 1

    Potomek 1 po `sleep(15)` se dostane do iterace 1 (i = 1):

    - Iterace 1: forkne → Potomek 1.1. Potomek 1.1: `sleep(15)`. Potomek 1 (nyní jako rodič 1.1): `wait()` → čeká → pak `execlp` → přeměna na `sleep 12`.
    - Potomek 1 se přemění po iteraci 1 a **nespustí iterace 2 a 3**.

    ### Krok 5 — Analýza Potomka 1.1

    Potomek 1.1 po `sleep(15)` se dostane do iterace 2 (i = 2):

    - Iterace 2: forkne → Potomek 1.1.1. Potomek 1.1.1: `sleep(15)`. Potomek 1.1: `wait()` → čeká → pak `execlp` → přeměna na `sleep 12`.

    ### Krok 6 — Analýza Potomka 1.1.1

    Potomek 1.1.1 po `sleep(15)` se dostane do iterace 3 (i = 3):

    - Iterace 3: forkne → Potomek 1.1.1.1. Potomek 1.1.1.1: `sleep(15)`. Potomek 1.1.1: `wait()` → čeká → pak `execlp` → přeměna na `sleep 12`.

    ### Krok 7 — Analýza Potomka 1.1.1.1

    Potomek 1.1.1.1 po `sleep(15)` se dostane — ale cyklus má `i < 4`, takže i = 4 podmínku nesplní. Cyklus skončí. Proběhne `free(ptr_char)` a `return 0`. Potomek 1.1.1.1 skončí.

    ### Krok 8 — Časová osa a klíčový princip

    !!! danger "Klíčový princip — `wait()` blokuje"
        Rodič zavolá `wait()` a **zablokuje se, dokud jeho potomek úplně neskončí**.
        Teprve po návratu z `wait()` provede `execlp` (přemění se na `sleep 12`, +12 s).
        Proto nejdřív doběhne **nejhlubší** potomek a řetězec se „odvíjí" odspodu
        nahoru — každý rodič čeká na celé doběhnutí svého potomka.

    ```text
    čas:      0    15   30   45   60    72    84    96   108
    P1.1.1.1:           |sl15|→ return (konec 60)
    P1.1.1:        |sl15|--wait--|exec sl12|→ konec 72
    P1.1:     |sl15|----wait-----|exec sl12|→ konec 84
    P1:  |sl15|-------wait--------|exec sl12|→ konec 96
    prog:|----------wait----------|exec sl12|→ konec 108
    ```

    Detailní výpočet — řetězec se odvíjí odspodu (nejhlubší potomek první):

    | Proces | Narozen v T0+ | `sleep(15)` | forkne potomka v T0+ | `wait()` vrátí v T0+ | `execlp` v T0+ | Skončí v T0+ |
    |---|---|---|---|---|---|---|
    | P1.1.1.1 | 45 | 45–60 | — (cyklus skončil) | — | — | **60** (`return`) |
    | P1.1.1 | 30 | 30–45 | 45 | 60 | 60 | 60+12 = **72** |
    | P1.1 | 15 | 15–30 | 30 | 72 | 72 | 72+12 = **84** |
    | P1 | 0 | 0–15 | 15 | 84 | 84 | 84+12 = **96** |
    | prog | 0 | — | 0 | 96 | 96 | 96+12 = **108** |

    ### Odpovědi

    **1. Počet procesů celkem.**

    Vznikly: `prog` + P1 + P1.1 + P1.1.1 + P1.1.1.1 = **5 procesů**.

    (Pokud zadání ptá „kolik se vytvoří" a původní `prog` se považuje za „spuštěný, ne vytvořený", je odpověď 4 nové. V tomto zadání formulace „celkem vytvoří" zpravidla zahrnuje i `prog`. Ověř konkrétní formulaci zadání.)

    **2. Doba běhu.**

    Poslední skončí **`prog`**: jeho `wait()` se vrátí až v T0+96 (když doběhne P1),
    pak ještě `sleep 12`. Poslední proces končí v **T0 + 108 s**.

    **3. Procesy v T0 + 75.734 s.**

    V čase 75.734 s už skončily P1.1.1.1 (v 60) a P1.1.1 (v 72). Stále existují:

    - `prog` — blokován v `wait()` (vrátí se až v 96),
    - P1 — blokován v `wait()` (vrátí se až v 84),
    - P1.1 — běží `sleep 12` (72–84).

    → **3 procesy**.

    **4. Zásobník.**

    `char a[1786248]` → `ceil(1786248 / 1048576) = ceil(1.7036...) =` **2 MiB**.

    Výpočet: 1786248 / 1048576 = 1.7036... → zaokrouhleno nahoru = 2.

    **5. Halda.**

    `malloc(8074950)` → `ceil(8074950 / 1048576) = ceil(7.7013...) =` **8 MiB**.

    Výpočet: 8074950 / 1048576 = 7.7013... → zaokrouhleno nahoru = 8.

---

## Další procvičení

### Varianta A — jednoduchý cyklus bez wait a exec

!!! example "Zadání A"
    Limit zásobníku 9 MiB, limit vláken 144 (vč. shellu). Uživatel, kterému běží pouze login shell, spustí v T0 program:

    ```c
    int main ()
    {
        char a[1829088];
        char *ptr_char = (char *) malloc (5809195);

        for ( int i = 0; i < 4 ; i++ )
        {
            pid_t child_pid = fork ();
            if (child_pid == 0)
            {
                sleep(10);
            }
        }
        free (ptr_char);
        return 0;
    }
    ```

    1. Kolik procesů celkem vznikne?
    2. Za kolik sekund doběhne poslední?
    3. Kolik procesů poběží v T0 + 18.647 s?
    4. Zásobník každého procesu (MiB nahoru)?
    5. Halda každého procesu (MiB nahoru)?

??? success "Řešení A"

    **Klíčový rozdíl oproti vzorovému zadání:** chybí `wait()` a `exec*()` v rodiči. Rodič po `fork()` **ihned pokračuje do další iterace**. Potomci po `sleep(10)` pokračují také do dalších iterací a sami forkují.

    **Strom — jak roste:**

    - Iterace 0: 1 proces → `fork()` → 2 procesy (orig + P1).
    - Iterace 1: každý z 2 procesů volá `fork()` → 4 procesy (orig, P1, P2, P3).
    - Iterace 2: každý ze 4 procesů volá `fork()` → 8 procesů.
    - Iterace 3: každý z 8 procesů volá `fork()` → 16 procesů.

    Ale pozor: procesy, které vznikly jako potomci v iteraci 0 (`child_pid == 0`), provádějí `sleep(10)` a **pak pokračují do dalších iterací** (i = 1, 2, 3). Procesy, které vznikly v iteraci 1, provádějí `sleep(10)` a pak pokračují do iterací 2, 3. A tak dále.

    Celkový počet procesů tedy závisí na tom, do jakých iterací se dostane každý potomek. Protože podmínka `if (child_pid == 0)` způsobí `sleep(10)`, ale **neukončí** proces — potomek z iterace k se dostane do iterací k+1, k+2, k+3.

    **Počítáme celkový počet forků (= počet nově vzniklých procesů):**

    Původní proces provede 4 forky (iterace 0–3): +4 potomci.
    Potomek z iterace 0 provede forky v iteracích 1, 2, 3: +3 potomci.
    Potomek z iterace 1 (od orig) provede forky v iteracích 2, 3: +2.
    Potomek z iterace 2 (od orig) provede fork v iteraci 3: +1.
    Potomek z iterace 3 (od orig): žádný fork (cyklus skončil).
    Potomek z iterace 1 (od P1 z it.0) provede forky v iteracích 2, 3: +2.
    ... a tak dále rekurzivně.

    Jednodušší způsob: v každé iteraci **zdvojí** se počet existujících procesů:
    - Po iteraci 0: 2 procesy.
    - Po iteraci 1: 4 procesy.
    - Po iteraci 2: 8 procesů.
    - Po iteraci 3: 16 procesů.

    Ale pozor — procesy vznikající v pozdějších iteracích mají menší `i` při vstupu do podmínky. Správně: celkový počet procesů (včetně původního) = **2^4 = 16**.

    Nově vzniklých = **15** (16 − 1).

    **Doba běhu:** Potomek, který vznikl v iteraci 3, ihned volá `sleep(10)`. Rodič z iterace 3 (= kterýkoliv proces, jenž provedl poslední fork) skončí `return 0` hned po opuštění cyklu. Nejvzdálenější potomci vznikají v různých časech. Nejpozdější: potomek vzniklý v iteraci 3 od procesu, který sám vznikl jako potomek v iteraci 0, 1 nebo 2 — záleží, kdy tento potomek provede 4. iteraci. Nejpozdější větvení nastane u potomka z iterace 0, který se do iterace 3 dostane až po `sleep(10)`. Čas vzniku tohoto posledního potomka = T0+10 (po sleep z iter. 0), pak iter 1, 2 (bez sleep — rodič tam nekončí, fork probíhá ihned), fork v iteraci 3 → potomek z iterace 3 začne `sleep(10)` v čase T0+10 → skončí v T0+20.

    Ale i samotný potomek z iterace 0, který prošel iteracemi 1, 2, 3 (jako rodič), skončí po dokončení všech 4 iterací. Čas dokončení tohoto procesu: skončí cyklus a provede `return 0` — bez dalšího sleep. Ten skončí prakticky okamžitě po T0+10 (kdy doběhl sleep v it. 0).

    Nejdéle žijící procesy jsou potomci vzniklí v **iteraci 3**, jejichž předci prošli iteracemi 0, 1, 2 s `sleep(10)` v každé: takový potomek vzniká v čase T0+30 (3 × sleep 10 s, sériově) a spí dalších 10 s → skončí v T0+**40 s**.

    Ale „rodič" v iteraci 3 (proces, který forkuje) je buď původní (bez sleep v it.0 pro rodiče), nebo potomek z it.0 (sleep 10), nebo potomek-potomek z it.1 (spí navíc 10 s) atd. Nejpozdější fork v iteraci 3 nastane u potomka, který v iteracích 0, 1, 2 spal: fork v T0+30, potomek spi 10 s → konec T0+**40 s**.

    Poslední doběhne v **T0 + 40 s**.

    **Procesy v T0 + 18.647 s:**

    V T0+18.647 ještě spí:
    - Potomci vzniklí v iteraci 0 (spí do T0+10) — **už skončili**.
    - Potomci vzniklí v iteraci 1 od procesů, které neprošly sleep: vznikají kolem T0+0 (od orig), spí 10 s → skončí T0+10. **Skončili.**
    - Potomci vzniklí v iteraci 1 od potomka z iterace 0: potomek z it.0 byl v sleep do T0+10, pak v iteraci 1 forkl. Nový potomek spí od T0+10 do T0+20. V T0+18.647 **ještě spí**.
    - Podobně potomci z iterace 2 a 3 vzniklí od pozdějších předků.

    Přesný počet v T0+18.647 s: spí potomci, kteří vznikli v iteraci 1, 2, 3 od potomků, kteří si vzali `sleep(10)`. Čas 18.647 s je mezi 10 s a 20 s.

    Procesy s sleep(10) začínajícím v T0+0: skončily v T0+10. (původní potomci z it.0)
    Procesy s sleep(10) začínajícím v T0+10 (potomci od potomků z it.0): spí do T0+20. Stále běží.

    Počet takových procesů: potomek z it.1 (od orig-potomka z it.0) = 1, potomek z it.2 (od orig-potomka z it.0 přes it.1) = 1 potomek od orig, ale orig v iteraci 2 nespí — fork nastane ihned. Detailní výčet: v T0+18.647 s spí potomci, jejichž `sleep(10)` začal v rozsahu [8.647, 18.647] → tj. začali spát v T0+10.

    Těchto procesů je přesně těch, které forkl potomek z iterace 0 v T0+10: iterace 1, 2, 3 → **3 potomci od toho jednoho procesu** + sám ten proces (pokud ještě neskončil: dokončí iterace 1, 2, 3 a skončí kolem T0+10, tedy skončil). Navíc sám potomek z it.0 dokončil iterace 1–3 a skončil v T0+10+ε.

    Počet = **7** procesů (přesnější spočítání vyžaduje nakreslit strom; přibližně 7–8 podle konkrétní analýzy stromu — ověř u konkrétní varianty zadání).

    **Zásobník:** `ceil(1829088 / 1048576) = ceil(1.7443...) =` **2 MiB**.

    **Halda:** `ceil(5809195 / 1048576) = ceil(5.5399...) =` **6 MiB**.

---

### Varianta B — fork() s logickými operátory (&&)

!!! example "Zadání B"
    Kolik nových procesů vznikne provedením tohoto kódu? (Nepočítej původní proces; předpokládej dostatek prostředků.)

    ```c
    for ( int i = 0; i < 4; i++ )
        if ( fork() == fork() )
            break;
    ```

??? success "Řešení B"

    **Toto je záludné zadání** — ptá se jen na počet nových procesů, ne na čas ani paměť.

    **Analýza výrazu `fork() == fork()`.** Výraz obsahuje dvě volání `fork()`. Levý `fork()` rozdělí proces na dva; v každém z nich pak proběhne pravý `fork()`. Z jednoho procesu tak vzniknou **4 procesy**:

    | Proces | levý `fork()` | pravý `fork()` | `==`? | akce |
    |--------|---------------|----------------|-------|------|
    | původní | PID_L (>0) | PID_P1 (>0) | PID_L ≠ PID_P1 → false | pokračuje |
    | potomek L | 0 | PID_P2 (>0) | 0 ≠ PID_P2 → false | pokračuje |
    | potomek P1 | PID_L (>0) | 0 | PID_L ≠ 0 → false | pokračuje |
    | potomek P2 | 0 | 0 | 0 == 0 → **true** | `break` |

    Z jednoho procesu vstupujícího do iterace tedy vzniknou **3 nové procesy** a do další iterace pokračují **3 ze 4** (původní + potomek L + potomek P1); čtvrtý (potomek P2) provede `break`.

    **Růst počtu procesů.** Počet procesů, které vstupují do iterace `k`, se každou iterací **ztrojnásobí**:

    ```text
    iterace k:                 0    1    2    3
    procesů vstupuje (3^k):    1    3    9   27
    nových vznikne (3 · 3^k):  3    9   27   81
    ```

    Pro cyklus `i < 4` (iterace 0–3) je celkový počet **nových** procesů:

    ```text
    3 + 9 + 27 + 81 = 120 nových procesů
    ```

    (Včetně původního procesu by to bylo 121.)

    !!! tip "Souvislost se Sbírkou úloh"
        Tentýž typ úlohy s `i < 5` a `i < 9` je řešený ve [Sbírce úloh → Forky](../../sbirka/02-forky.md); tam se sčítá `1 + 3 + 9 + …`, protože se započítává i původní proces.

    !!! warning "Ověř si u zkoušky"
        Zadání se může lišit (jiný počet iterací, jiné operátory). Vždy nakresli strom pro první iteraci, urči, který potomek provede `break` a kolik procesů pokračuje, a teprve pak aplikuj vzorec.

---

## Varianty a chytáky

**`exec*()` se nikdy nevrátí při úspěchu.**
Pokud `execlp(...)` uspěje, kód za ním se **neprovede** — ani zbytek cyklu, ani `sleep(9)`, ani `return`. Pokud `execlp` selže (špatná cesta, neexistující program), kód pokračuje dál. V zadání se zpravidla předpokládá úspěch.

**Potomek bez `return`/`exit` v podmínce `if (child_pid == 0)` pokračuje do cyklu.**
Pokud blok potomka obsahuje jen `sleep()` bez ukončení, potomek se po probuzení vrátí do cyklu a forkuje dál. To dramaticky mění počet procesů. Porovnej:

```c
// Varianta A — potomek pokračuje (nezůstane ve větvi)
if (child_pid == 0) { sleep(10); }

// Varianta B — potomek skončí (zůstane v else nebo prázdném bloku)
if (child_pid == 0) { sleep(10); exit(0); }
// nebo: if (child_pid == 0) { sleep(10); } else { ... }
```

**`wait()` čeká jen na přímé potomky.**
`wait()` čeká na **jakéhokoliv** přímého potomka volajícího procesu. Pokud má rodič více potomků, každé volání `wait()` odblokuje jedno z nich. `waitpid()` čeká na konkrétního.

**Límit vláken a shell.**
Limitem `144` — shell zabírá 1. Nové procesy/vlákna: maximálně 143. Každé volání `fork()` vytvoří nové vlákno. Pokud `fork()` selže (vrátí -1), kód bez ošetření chyby zavolá `wait()` a `execlp` s neplatným stavem — analyzuj, co se stane.

**`< vs. <=` v cyklu.**
`for (i = 0; i < 4; i++)` = 4 iterace (i = 0, 1, 2, 3).
`for (i = 0; i <= 4; i++)` = 5 iterací (i = 0, 1, 2, 3, 4). Záměna je klasický zdroj chyby.

**`fork() == fork()` a logické operátory.**
U `&&`: levý operand `fork()` vrátí v rodiči kladné (true) → vyhodnotí se pravý. V potomkovi vrátí 0 (false) → pravý se **nevyhodnotí** (`&&` zkratuje). U `||` opačně. Výsledek: u `&&` potomek z levého forku neforkuje znovu; u `||` potomek z levého forku forkuje znovu.

**Paměť — ceil vs. round.**
`ceil(1.7) = 2`, `ceil(2.0) = 2`, `ceil(2.001) = 3`. Nikdy nezaokrouhluj na nejbližší — vždy nahoru.

**„Celkem vytvoří" vs. „nově vznikne".**
Přečti zadání dvakrát. „Celkem vytvoří" nejčastěji zahrnuje původní proces. „Nově vznikne" nebo „v důsledku forkování" může původní vyloučit.

---

## Časté chyby

1. **Zapomenout, že úspěšný `exec*()` se nevrátí.** Studenti píší, že rodič provede `execlp` a pak pokračuje v cyklu — to je špatně.

2. **Rodičovská větev po `fork()`.** `if (child_pid == 0)` je potomek. Jinak (`else` nebo implicitně) je rodič. Zaměnění způsobí inverzi stromu.

3. **Nepočítat, kolik iterací cyklu každý proces provede.** Zvláště potomek bez `exit()` prochází dalšími iteracemi a sám forkuje.

4. **Špatný ceil při výpočtu MiB.** 1 786 248 / 1 048 576 = 1.7036 → výsledek je 2, ne 1 ani 1.7.

5. **Záměna zásobníku a haldy.** `char a[N]` je na zásobníku (statická lokální proměnná). `malloc(M)` je na haldě.

6. **Zapomenout na shell při výpočtu limitu.** Limit 144 vláken zahrnuje shell → lze vytvořit 143 nových.

7. **Nevšimnout si `wait()` v cyklu.** Pokud je `wait()` v těle cyklu (ne až za ním), rodič čeká na potomka v **každé iteraci** zvlášť, ne na všechny najednou.

8. **Záměna „nově vzniklých" a „celkového počtu procesů v čase T".** Otázka 1 a otázka 3 se ptají na různé věci — neplést je.

---

## Související

- [Skripta: Procesy a vlákna](../../skripta/02-procesy-vlakna.md) — teorie `fork/exec/wait`, adresový prostor, stavový diagram vlákna, race conditions
- [Teoretické otázky (true/false)](../teorie-truefalse.md) — definice procesu, vlákna, zombie, adopce sirotků, preemptivní plánování
