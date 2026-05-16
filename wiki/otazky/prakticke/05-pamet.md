# Správa paměti

Dva typy úloh, které se v každém termínu pravidelně opakují: **stránkování** (struktura adres, velikost a počet řádek tabulek, překlad virtuální adresy na fyzickou) a **algoritmy náhrady stránek** (FIFO, LRU, Clock, NRU, Optimální, Aging aplikované na referenční sekvenci).

??? abstract "Obsah stránky"

    [TOC]

---

## Co tento typ úlohy prověřuje

- Schopnost rozložit virtuální a fyzickou adresu na číslo stránky/rámce a offset.
- Znalost rozdílů mezi jednoúrovňovou, invertovanou tabulkou stránek a TLB — kolik tabulek jádro udržuje a kolik řádek každá má.
- Schopnost krok za krokem aplikovat algoritmus náhrady stránek na zadanou referenční sekvenci a spočítat počet výpadků stránky (page faultů).

---

## Co potřebuješ znát

### Vzorce pro stránkovací tabulky

| Veličina | Vzorec |
|---|---|
| Počet bitů offsetu | `offset_bitů = log2(velikost_stránky_v_B)` |
| Počet bitů čísla stránky | `page_bits = délka_virtuální_adresy − offset_bitů` |
| Počet bitů čísla rámce | `frame_bits = délka_fyzické_adresy − offset_bitů` |
| Počet řádek — jednoúrovňová ST | `2^page_bits` (jedna řádka na každou stránku ve VAS) |
| Počet řádek — invertovaná ST | `2^frame_bits` (jedna řádka na každý fyzický rámec) |
| Počet tabulek — jednoúrovňová ST | jedna na každý proces (celkem ≥ N tabulek pro N procesů) |
| Počet tabulek — invertovaná ST | **jedna** pro celý systém |
| Počet řádek TLB | pevně daný hardware, typicky 64–1024; zadáno přímo |

### Obsah řádky (PTE)

- **Jednoúrovňová ST:** číslo rámce + present bit (P) + reference bit (R) + dirty bit (D) + přístupová práva.
- **Invertovaná ST:** číslo stránky + číslo procesu (PID) + řídicí bity (P, R, D) + index zřetězení pro kolize.
- **TLB:** číslo stránky + číslo rámce + ASID + řídicí bity (R, D, W, X...).

### Klíčová pravidla

- Virtuální adresa obsahuje číslo **stránky** (ne rámce).
- Fyzická adresa obsahuje číslo **rámce** (ne stránky).
- Offset je v obou adresách **identický** a nezměněný.
- Počet řádek se počítá z **délky adresy**, nikoli z toho, kolik paměti proces aktuálně využívá.

### Referenční materiál

[Skripta: Správa paměti](../../skripta/06-pamet.md)

---

## Postup řešení krok za krokem

### A. Stránkovací tabulky — překlad adres a velikost tabulek

Tento postup platí pro jakékoli zadání s otázkami na strukturu adres nebo velikost/počet tabulek.

1. **Přečti zadání opatrně** — zjisti: velikost stránky/rámce (v B nebo KiB/MiB), délku virtuální adresy (v bitech), délku fyzické adresy (v bitech), typ tabulky (jednoúrovňová / invertovaná), počet procesů a (případně) počet položek TLB.

2. **Spočítej bity offsetu.**
   Offset je index bytu uvnitř stránky. Protože velikost stránky je vždy mocnina 2, platí:
   ```text
   offset_bitů = log2(velikost_stránky_v_B)
   ```
   Příklad: stránka 16 384 B = 2^14 B → offset = **14 bitů**.

3. **Spočítej bity čísla stránky.**
   Zbytek bitů virtuální adresy po odečtení offsetu:
   ```text
   page_bits = délka_VA − offset_bitů
   ```
   Příklad: VA = 36 bitů, offset = 14 → page_bits = **22 bitů**.

4. **Spočítej bity čísla rámce.**
   Analogicky pro fyzickou adresu:
   ```text
   frame_bits = délka_FA − offset_bitů
   ```
   Příklad: FA = 36 bitů, offset = 14 → frame_bits = **22 bitů**.

5. **Rozlož strukturu adres** — nakresli si schéma:
   ```text
   Virtuální adresa (36 bitů):  [ číslo stránky: 22 b | offset: 14 b ]
   Fyzická adresa   (36 bitů):  [ číslo rámce:   22 b | offset: 14 b ]
   ```

6. **Urči typ tabulky a spočítej počet řádek.**
   - **Jednoúrovňová (klasická) tabulka stránek:**
     Jedna řádka na každou stránku ve VAS → počet řádek = `2^page_bits`.
     Příklad: `2^22 = 4 194 304` řádek.
   - **Invertovaná tabulka stránek:**
     Jedna řádka na každý fyzický rámec → počet řádek = `2^frame_bits`.
     Příklad: `2^22 = 4 194 304` řádek (v tomto konkrétním zadání stejně, ale obecně se liší!).
   - **TLB:**
     Počet položek TLB je pevný hardware parametr — přečti ze zadání (např. 512 položek).

7. **Urči počet tabulek, které jádro musí udržovat.**
   - Jednoúrovňová ST: jádro udržuje **jednu tabulku na každý proces**. Pro N procesů jde o N tabulek (nebo více, pokud procesy mají více vláken s oddělenými ST).
   - Invertovaná ST: jádro udržuje **jednu tabulku pro celý systém**, bez ohledu na počet procesů.
   - TLB: jedno TLB sdílí všechny procesy (záznamy jsou rozlišeny přes ASID nebo se při přepnutí kontextu invalidují).

8. **Ověř pravdivost tvrzení v multichoice** — časté pasti:
   - „Logická adresa obsahuje číslo rámce" → **NEPRAVDA** (obsahuje číslo stránky).
   - „Fyzická adresa obsahuje číslo stránky" → **NEPRAVDA** (obsahuje číslo rámce).
   - „Invertovaná ST má jednu řádku na stránku VAS" → **NEPRAVDA** (má jednu na rámec).
   - „Větší stránky zvyšují TLB hit ratio" → **PRAVDA** (větší stránka pokryje více adres jedinou TLB položkou).
   - „TLB lze za běhu zvětšovat" → **NEPRAVDA** (je pevná součást HW).

---

### B. Algoritmy náhrady stránek — aplikace na referenční sekvenci

Tento postup platí pro všechny algoritmy. Vždy si kresli tabulku: sloupce = přístupy ze sekvence, řádky = rámce.

1. **Přečti zadání** — zjisti: počet rámců (jsou prázdné, nebo předem naplněné?), referenční sekvenci, jaký algoritmus použít.

2. **Inicializuj tabulku** — na začátku jsou všechny rámce prázdné (nebo vyplněné dle zadání). Očísluj nebo pojmenuj rámce (a, b, c, ...).

3. **Procházej sekvenci po jednom přístupu.**
   Pro každý přístup (stránku X) urči:
   - Je stránka X **již v některém rámci?** → **HIT**, nic se nemění (u některých algoritmů jen aktualizuj metadata — R bit, čas přístupu, čítač).
   - Stránka X **není v žádném rámci** → **PAGE FAULT** (výpadek stránky).

4. **Při PAGE FAULT — volný rámec existuje:** umísti stránku do nejmenšího volného rámce (abecedně první: a před b před c...). Zaznamenej jako výpadek.

5. **Při PAGE FAULT — žádný volný rámec:** vyber **oběť** podle příslušného algoritmu (viz níže), nahraď ji novou stránkou. Zaznamenej jako výpadek.

6. **Výběr oběti podle algoritmu:**

   - **FIFO (First-In First-Out):**
     Nahradí se stránka, která je v paměti **nejdéle** (nejstarší příchod).
     Implementace: udržuj frontu stránek v pořadí příchodu. Oběť = stránka na začátku fronty. Po náhradě přidej novou stránku na konec.

   - **LRU (Least Recently Used):**
     Nahradí se stránka, ke které se **nejdéle nepřistupovalo** (nejstarší poslední přístup).
     Implementace: při každém přístupu (hit i fault) si zaznamenej čas přístupu. Oběť = stránka s nejstarším časem posledního přístupu.

   - **Optimální (OPT):**
     Nahradí se stránka, ke které bude přistoupeno **nejpozději v budoucnu** (nebo vůbec).
     Implementace: podívej se dopředu na zbytek sekvence. Pro každou stránku v rámcích najdi, kdy se k ní příště přistoupí. Oběť = stránka s nejpozdějším dalším přístupem. Pokud se k stránce v budoucnu nepřistoupí vůbec, je to nejlepší oběť.

   - **Clock (Second Chance):**
     Stránky jsou v kruhové frontě s ručičkou. Každá má R bit.
     Postup při hledání oběti:
     ```text
     1. Podívej se na stránku pod ručičkou.
     2. Pokud R = 1: nastav R = 0, posuň ručičku o 1 vpřed, jdi na krok 1.
     3. Pokud R = 0: tato stránka je oběť. Nahraď ji, posuň ručičku vpřed.
     ```
     Při přístupu (hit) nastav R = 1 pro danou stránku.
     Při vložení nové stránky nastav R = 1 a umísti ji na místo ručičky.

   - **NRU (Not Recently Used):**
     Každá stránka má R bit (reference) a D bit (dirty/modified). OS je periodicky resetuje.
     Třídy: 0 = (R=0, D=0), 1 = (R=0, D=1), 2 = (R=1, D=0), 3 = (R=1, D=1).
     Oběť = stránka z **neprázdné třídy s nejnižším číslem**. V rámci třídy libovolná.

   - **Aging:**
     Každá stránka má n-bitový čítač C (inicializován na 0 nebo 11...1 dle varianty zadání).
     OS **periodicky** (každou periodu T):
     ```text
     1. Posun čítač C každé stránky o 1 bit doprava.
     2. Nastav MSB (nejvýznamnější bit) čítače na hodnotu R bitu dané stránky.
     3. Resetuj R bit na 0.
     ```
     Oběť = stránka s **nejmenší hodnotou čítače C** (nejméně „aktivní" v historii).

7. **Po každém přístupu aktualizuj záznamy** (R bit, čítač, pořadí ve frontě) podle algoritmu.

8. **Spočítej celkový počet výpadků** — je to součet všech zaznačených PAGE FAULTů.

9. **Zkontroluj výsledek** — první N přístupů k unikátním stránkám (kde N = počet rámců) jsou vždy výpadky (rámce se plní poprvé). Celkový počet výpadků nemůže být menší než u optimálního algoritmu.

---

## Vzorové zadání

!!! example "Zadání"
    **A) Stránkování.**
    Systém s virtuální pamětí: velikost stránky/rámce **16 384 B**, velikost virtuální adresy **36 bitů**, fyzické adresy **36 bitů**. TLB má **512 položek**. Běží **983 uživatelských procesů**. Systém používá **invertovanou** tabulku stránek.

    1. Kolik bitů má offset?
    2. Kolik bitů má číslo stránky (v logické adrese)?
    3. Kolik bitů má číslo rámce (ve fyzické adrese)?
    4. Kolik tabulek stránek si musí jádro pamatovat?
    5. Kolik řádek bude mít tabulka stránek?

    Vyberte pravdivá tvrzení (klasická tabulka vs. invertovaná):
    - Logická adresa obsahuje 22bitové číslo stránky.
    - Fyzická adresa obsahuje 14bitový offset.
    - Na řádce invertované tabulky je číslo rámce a present bit.
    - Na řádce TLB je číslo stránky, číslo rámce a modify/reference bit.
    - Větší stránky mohou zvýšit TLB hit ratio.

    **B) Náhrada stránek.**
    K dispozici **5 rámců** (a–e), na začátku prázdné. Ke stránkám se přistupuje v pořadí:
    `7, 0, 2, 0, 2, 6, 5, 5, 5, 1, 6, 7, 3, 6, 2, 7, 9`

    Kolik nastane výpadků stránky při **optimálním** algoritmu a jaký bude obsah rámců po posledním přístupu?

    *Stránkování: každý termín 2014–2025. Náhrada stránek: 2012, 2018, 2019, 2022.*

---

## Řešení vzorového zadání

??? success "Ukázat řešení"

    ### A) Stránkování — krok za krokem

    **Krok 1: Offset.**
    ```text
    offset_bitů = log2(16 384) = log2(2^14) = 14 bitů
    ```

    **Krok 2: Číslo stránky.**
    ```text
    page_bits = 36 − 14 = 22 bitů
    ```

    **Krok 3: Číslo rámce.**
    ```text
    frame_bits = 36 − 14 = 22 bitů
    ```
    (Virtuální a fyzická adresa jsou zde stejně dlouhé, takže vychází stejně — ale obecně se page_bits a frame_bits mohou lišit!)

    **Krok 4: Struktura adres.**
    ```text
    Virtuální adresa (36 b):  [ číslo stránky: 22 b | offset: 14 b ]
    Fyzická adresa   (36 b):  [ číslo rámce:   22 b | offset: 14 b ]
    ```

    **Krok 5: Počet tabulek.**
    Systém používá **invertovanou** tabulku → jádro udržuje **jednu tabulku pro celý systém**, bez ohledu na počet procesů (983 procesů na tom nic nemění).

    **Krok 6: Počet řádek.**
    Invertovaná tabulka má jednu řádku na každý fyzický rámec:
    ```text
    počet řádek = 2^frame_bits = 2^22 = 4 194 304 řádek
    ```

    **Krok 7: Multichoice.**

    | Tvrzení | Pravdivost | Odůvodnění |
    |---|---|---|
    | Logická adresa obsahuje 22bitové číslo stránky | **PRAVDA** | page_bits = 36 − 14 = 22 |
    | Fyzická adresa obsahuje 14bitový offset | **PRAVDA** | offset = log2(16384) = 14 |
    | Na řádce invertované tabulky je číslo rámce a present bit | **NEPRAVDA** | Invertovaná tabulka je indexována číslem rámce; řádka obsahuje číslo **stránky** + číslo procesu + P bit |
    | Na řádce TLB je číslo stránky, číslo rámce a modify/reference bit | **PRAVDA** | TLB cachuje překlad stránka → rámec + řídicí bity |
    | Větší stránky mohou zvýšit TLB hit ratio | **PRAVDA** | Větší stránka pokryje větší oblast adres jedinou TLB položkou |

    !!! note "Srovnání s klasickou tabulkou"
        Kdyby šlo o **jednoúrovňovou (klasickou)** tabulku stránek:
        - Počet řádek = `2^page_bits = 2^22 = 4 194 304` (zde stejně jako invertovaná, protože VA = FA).
        - Jádro by si muselo pamatovat **alespoň 983 tabulek** — jednu na každý proces.
        - Na řádce klasické tabulky je **číslo rámce** (ne stránky) + P, R, D bity.

    ---

    ### B) Náhrada stránek — Optimální algoritmus, krok za krokem

    Sekvence: `7, 0, 2, 0, 2, 6, 5, 5, 5, 1, 6, 7, 3, 6, 2, 7, 9`
    5 rámců, na začátku prázdné.

    Strategie Optimálního algoritmu: při výpadku vyber k vyřazení stránku, ke které bude přistoupeno nejpozději v budoucnu (nebo nikdy).

    **Přístupy 1–5: plnění prázdných rámců (vždy výpadek)**

    | Přístup | Stránka | Rámec a | Rámec b | Rámec c | Rámec d | Rámec e | Výpadek |
    |---|---|---|---|---|---|---|---|
    | 1 | 7 | **7** | — | — | — | — | F (1) |
    | 2 | 0 | 7 | **0** | — | — | — | F (2) |
    | 3 | 2 | 7 | 0 | **2** | — | — | F (3) |
    | 4 | 0 | 7 | 0 | 2 | — | — | hit |
    | 5 | 2 | 7 | 0 | 2 | — | — | hit |
    | 6 | 6 | 7 | 0 | 2 | **6** | — | F (4) |
    | 7 | 5 | 7 | 0 | 2 | 6 | **5** | F (5) |

    Rámce jsou nyní plné: `a=7, b=0, c=2, d=6, e=5`.

    **Přístup 8 (stránka 5):** 5 je v rámci e → **HIT**.

    **Přístup 9 (stránka 5):** 5 je v rámci e → **HIT**.

    **Přístup 10 (stránka 1):** 1 není v žádném rámci → PAGE FAULT (6).
    Podíváme se dopředu na zbytek sekvence: `6, 7, 3, 6, 2, 7, 9`
    Kdy se příště přistoupí k jednotlivým stránkám v rámcích?
    ```text
    stránka 7 → přístup č. 12  (pozice "7" v: 6,7,3,6,2,7,9)
    stránka 0 → NIKDY (0 se v zbytku nevyskytuje) ← nejlepší oběť
    stránka 2 → přístup č. 15
    stránka 6 → přístup č. 11
    stránka 5 → NIKDY (5 se v zbytku nevyskytuje) ← také dobrá oběť
    ```
    Nejlepší oběť: stránka **0** (nebo 5 — obě se v budoucnu nevyskytují; vybereme b=0 jako první volný v abecedním pořadí nahrazovaných kandidátů, ale v praxi vybíráme „nikdy" před „nejpozději"). Nahradíme rámec b=0 → b=1.

    Rámce: `a=7, b=1, c=2, d=6, e=5`.

    **Přístup 11 (stránka 6):** 6 je v rámci d → **HIT**.

    **Přístup 12 (stránka 7):** 7 je v rámci a → **HIT**.

    **Přístup 13 (stránka 3):** 3 není v žádném rámci → PAGE FAULT (7).
    Zbytek sekvence: `6, 2, 7, 9`
    ```text
    stránka 7 → přístup č. 16
    stránka 1 → NIKDY ← nejlepší oběť
    stránka 2 → přístup č. 15
    stránka 6 → přístup č. 14
    stránka 5 → NIKDY ← stejně dobrá
    ```
    Oběť: stránka **5** v rámci e (nebo 1 v rámci b — obě „nikdy"; vezmeme e=5).
    Nahradíme e=5 → e=3.

    Rámce: `a=7, b=1, c=2, d=6, e=3`.

    **Přístup 14 (stránka 6):** 6 je v rámci d → **HIT**.

    **Přístup 15 (stránka 2):** 2 je v rámci c → **HIT**.

    **Přístup 16 (stránka 7):** 7 je v rámci a → **HIT**.

    **Přístup 17 (stránka 9):** 9 není v žádném rámci → PAGE FAULT (8).
    Zbytek sekvence: prázdný (poslední přístup).
    Všechny stránky v rámcích jsou „nikdy" (konec sekvence). Vybereme libovolnou; konvencí nahradíme stránku **1** v rámci b.
    Rámce: `a=7, b=9, c=2, d=6, e=3`.

    **Výsledek:**

    ```text
    přístup  stránka   a   b   c   d   e   výpadek?
    1        7         7   —   —   —   —   F (1)
    2        0         7   0   —   —   —   F (2)
    3        2         7   0   2   —   —   F (3)
    4        0         7   0   2   —   —   hit
    5        2         7   0   2   —   —   hit
    6        6         7   0   2   6   —   F (4)
    7        5         7   0   2   6   5   F (5)
    8        5         7   0   2   6   5   hit
    9        5         7   0   2   6   5   hit
    10       1         7   1   2   6   5   F (6)  ← oběť: 0 (nikdy se nevrátí)
    11       6         7   1   2   6   5   hit
    12       7         7   1   2   6   5   hit
    13       3         7   1   2   6   3   F (7)  ← oběť: 5 (nikdy se nevrátí)
    14       6         7   1   2   6   3   hit
    15       2         7   1   2   6   3   hit
    16       7         7   1   2   6   3   hit
    17       9         7   9   2   6   3   F (8)  ← oběť: 1 (konec sekvence)
    ```

    **Celkový počet výpadků: 8.**

    Obsah rámců po posledním přístupu: **a=7, b=9, c=2, d=6, e=3**.

---

## Další procvičení

### Varianta 1 — stránkovací tabulky (jiné parametry)

!!! example "Zadání"
    Systém: velikost stránky **8 192 B** (8 KiB), virtuální adresa **32 bitů**, fyzická adresa **30 bitů**. Běží **256 procesů**. Systém používá **jednoúrovňovou** tabulku stránek.

    1. Kolik bitů má offset?
    2. Kolik bitů má číslo stránky?
    3. Kolik bitů má číslo rámce?
    4. Kolik tabulek si pamatuje jádro?
    5. Kolik řádek má jedna tabulka?

??? success "Ukázat řešení"
    **Krok 1:** `offset = log2(8192) = log2(2^13) = 13 bitů`

    **Krok 2:** `page_bits = 32 − 13 = 19 bitů`

    **Krok 3:** `frame_bits = 30 − 13 = 17 bitů`

    **Krok 4:** Jednoúrovňová tabulka → jádro udržuje **jednu tabulku na každý proces** → celkem **256 tabulek** (minimálně).

    **Krok 5:** Počet řádek jedné tabulky = `2^page_bits = 2^19 = 524 288 řádek`.

    Struktura adres:
    ```text
    Virtuální adresa (32 b):  [ číslo stránky: 19 b | offset: 13 b ]
    Fyzická adresa   (30 b):  [ číslo rámce:   17 b | offset: 13 b ]
    ```

    Pozoruj: page_bits (19) ≠ frame_bits (17) — fyzická paměť je menší než virtuální adresní prostor. To je běžné.

---

### Varianta 2 — náhrada stránek (FIFO vs. LRU)

!!! example "Zadání"
    K dispozici **3 rámce** (a, b, c), na začátku prázdné. Referenční sekvence:
    `2, 3, 2, 1, 5, 2, 4, 5, 3, 2, 5, 2`

    Spočítejte počet výpadků pro algoritmy **FIFO** a **LRU**.

??? success "Ukázat řešení"

    **FIFO (3 rámce):**
    Udržujeme frontu pořadí příchodu: nejstarší = první v řadě pro vyřazení.

    ```text
    přístup  stránka   a   b   c   fronta (nejstarší→nejnovější)   výpadek?
    1        2         2   —   —   [2]                               F (1)
    2        3         2   3   —   [2, 3]                            F (2)
    3        2         2   3   —   [2, 3]                            hit
    4        1         2   3   1   [2, 3, 1]                         F (3)
    5        5         5   3   1   [3, 1, 5]  ← oběť: 2             F (4)
    6        2         5   2   1   [1, 5, 2]  ← oběť: 3             F (5)
    7        4         5   2   4   [5, 2, 4]  ← oběť: 1             F (6)
    8        5         5   2   4   [5, 2, 4]                         hit
    9        3         3   2   4   [2, 4, 3]  ← oběť: 5             F (7)
    10       2         3   2   4   [2, 4, 3]                         hit
    11       5         3   5   4   [4, 3, 5]  ← oběť: 2             F (8)
    12       2         3   5   2   [3, 5, 2]  ← oběť: 4             F (9)
    ```

    **FIFO: 9 výpadků.**

    **LRU (3 rámce):**
    Při každém přístupu (hit i fault) si zaznamenáme čas. Oběť = stránka s nejstarším posledním přístupem.

    ```text
    přístup  stránka   a(čas) b(čas) c(čas)   oběť    výpadek?
    1        2         2(1)   —      —                   F (1)
    2        3         2(1)   3(2)   —                   F (2)
    3        2         2(3)   3(2)   —                   hit (aktualizuj čas 2)
    4        1         2(3)   3(2)   1(4)                F (3)
    5        5         2(3)   5(5)   1(4)     ← oběť: 3 (čas 2)   F (4)
    6        2         2(6)   5(5)   1(4)                hit
    7        4         2(6)   5(5)   4(7)     ← oběť: 1 (čas 4)   F (5)
    8        5         2(6)   5(8)   4(7)                hit
    9        3         2(6)   3(9)   4(7)     ← oběť: 5 (čas 5... wait: 5 naposledy přístup 8) ← oběť: 2 (čas 6)   F (6)
    ```

    !!! warning "Pozor na pořadí časů u LRU"
        Po přístupu č. 9 (stránka 3):
        Rámce: a=2 (naposledy přístup č. 6), b=5 (č. 8), c=4 (č. 7).
        Oběť = nejstarší poslední přístup = stránka **2** (čas 6). Nahradíme a=3.

    ```text
    9        3         3(9)   5(8)   4(7)     ← oběť: 2 (čas 6)   F (6)
    10       2         3(9)   5(8)   2(10)    ← oběť: 4 (čas 7)   F (7)
    11       5         3(9)   5(11)  2(10)                hit
    12       2         3(9)   5(11)  2(12)                hit
    ```

    **LRU: 7 výpadků** (méně než FIFO díky využití informace o nedávnosti přístupu).

    Srovnání:

    | Algoritmus | Výpadky | Poznámka |
    |---|---|---|
    | Optimální | 6 | dolní mez, nelze implementovat |
    | LRU | 7 | nejlepší reálná aproximace optimálního |
    | Clock | 8 | střední, modifikovaný FIFO |
    | FIFO | 9 | nejjednodušší, ale nejhorší výsledky |

---

## Varianty a chytáky

- **Velikost stránky musí být mocnina 2** — jen tehdy dává `log2` celé číslo pro offset. Pokud dostaneš hodnotu, která mocninou 2 není, přepočítej (je to chyba zadání nebo past).
- **page_bits ≠ frame_bits** — fyzická adresa může být kratší než virtuální (fyzická paměť < VAS); pak je frame_bits < page_bits a invertovaná tabulka bude mít méně řádek než jednoúrovňová klasická.
- **Rušivé údaje v zadání** — počet procesů je pro invertovanou tabulku rušivý (stále jen jedna tabulka); alokovaná paměť procesu je rušivá pro počet řádek (závisí na délce adresy, ne na využití).
- **Výpočet řádek vždy z délky adresy, ne z RAM** — i když systém má 1 GB RAM, jednoúrovňová ST na 36bitové adrese má `2^22` řádek (z délky adresy).
- **TLB hit ratio** — větší stránky → méně TLB missů (jedna položka pokrývá více adres). Více procesů → více TLB shootdownů, ale velikost TLB se nemění.
- **Při shodě oběti** u FIFO/LRU/Clock vyber rámec s nejnižším označením (a před b před c...); zadání to občas explicitně uvádí.
- **Přístupy 5,5 a 5,5,5** v sekvenci jsou hitten — je důležité aktualizovat metadata (LRU čas, R bit u Clock/NRU) i při hitu.
- **NRU třídí stránky periodicky** — R bit se resetuje v čase i×T ze zadání. Při výpočtu sleduj, kdy přesně se resetuje, jinak špatně přiřadíš třídu.
- **Aging** — pokud zadání neupřesní počáteční hodnotu čítače, předpokládej 0. MSB se nastaví na R, pak shift doprava (nebo opačně — čti zadání).

---

## Časté chyby

1. **Záměna čísla stránky a čísla rámce v adresách.** Virtuální adresa = stránka + offset. Fyzická adresa = rámec + offset. Nikdy naopak.

2. **Počet řádek invertované tabulky = počet procesů.** Špatně. Invertovaná tabulka má `2^frame_bits` řádek — jednu na fyzický rámec. Počet procesů je irelevantní.

3. **Počet tabulek u jednoúrovňové = 1.** Špatně. Jednoúrovňová = jedna tabulka na každý proces. Invertovaná = jedna tabulka pro celý systém.

4. **Záměna log2 a log10.** Offset = `log2(velikost_stránky)`, ne `log10`. Stránka 4 096 B = 2^12 → offset = 12 bitů.

5. **Přeskočení aktualizace metadat při hitu.** U LRU musíš aktualizovat čas přístupu i při hitu (jinak špatně určíš oběť příště). U Clock musíš nastavit R = 1 při hitu.

6. **Špatná volba oběti u optimálního algoritmu.** Vždy se díváš na zbytek sekvence *od aktuálního přístupu dál*. Stránka, která se v budoucnu vůbec neobjeví, je nejlepší oběť (vyber ji jako první).

7. **Záměna FIFO a LRU** — FIFO sleduje čas **příchodu** do rámce; LRU sleduje čas **posledního přístupu**. Stránka může být v rámci dlouho (FIFO by ji vyhodila), ale přistupovalo se k ní nedávno (LRU by ji nechala).

8. **Počítat výpadky i při hitu** — hit = stránka je v rámci = žádný výpadek, jen aktualizace metadat.

---

## Související

- [Skripta: Správa paměti](../../skripta/06-pamet.md) — kompletní teorie stránkování, algoritmů a správy haldy
- [Teoretické otázky (true/false)](../teorie-truefalse.md) — procvič vlastnosti tabulek a algoritmů v testovém formátu
