# Plánování procesů

Úloha na plánování procesů se statickou prioritou: dostaneš tabulku procesů s prioritou, počtem vláken a celkovou dobou výpočtu a musíš zjistit, kdy jednotlivé procesy skončí, kdy fakticky začnou běžet a kdy doběhne úplně poslední proces.

??? abstract "Obsah stránky"

    [TOC]

---

## Co tento typ úlohy prověřuje

- Porozumění tomu, jak plánovač přiděluje hardwarová vlákna procesům podle priority.
- Schopnost poměrně rozdělit kapacitu vláken při shodné prioritě.
- Výpočet reálné doby běhu procesu při přidělení méně (nebo více) vláken, než proces vytvořil.
- Opakované přepočítávání stavu systému poté, co každý proces doběhne (tzv. fázový přístup).
- Zohlednění background load (zatížení procesoru jádrem / ostatními procesy).

Tento typ se ve zkoušce objevuje prakticky každý rok: 2011, 2014, 2018, 2019, 2023.

---

## Co potřebuješ znát

### Vzorce

```text
HW vláken celkem  = počet_procesorů × jader_na_procesor × vláken_na_jádro

doba_vlákna       = celková_doba_výpočtu / počet_vláken_procesu
                    (= doba, za kterou výpočet zvládne JEDNO vlákno)

real_time         = doba_vlákna × počet_vláken_procesu / přidělených_HW_vláken
                    (= jak dlouho proces reálně poběží při k přidělených vláknech)

Zkrácený zápis:   real_time = celková_doba / přidělených_HW_vláken

S background load X %:
  všechny vypočítané časy × (100 / (100 - X))
```

**Příklad:** Proces má 3 vlákna, celková doba 270 s.
- doba jednoho vlákna = 270 / 3 = **90 s**
- dostane-li 3 HW vlákna: real_time = 270 / 3 = **90 s**
- dostane-li 1 HW vlákno:  real_time = 270 / 1 = **270 s** (1 vlákno dělá práci 3)

### Klíčové principy

- **Vyšší číslo priority = vyšší priorita** (pokud zadání neurčí jinak).
- Plánovač přiděluje HW vlákna vždy nejprve procesu s nejvyšší prioritou (dostane tolik, kolik má vláken, max. tolik, kolik je dostupných).
- Při shodné prioritě a nedostatku HW vláken se dostupná vlákna rozdělí **poměrně** podle počtu vláken jednotlivých procesů.
- Plánovač přerozděluje vlákna vždy, když nějaký proces doběhne (uvolní vlákna).
- Výpočet probíhá ve **fázích** — každá fáze trvá do okamžiku, kdy první z běžících procesů dokončí práci.

### Odkaz na teorii

[Skripta: Plánování](../../skripta/05-planovani.md)

---

## Postup řešení krok za krokem

Níže je obecný postup, který funguje na všechny varianty této úlohy. Je rozepsán velmi podrobně — u zkoušky zvládneš po procvičení zkrátit, ale první kroky si vždy kresli.

### 1. Urči počet HW vláken

```text
HW = procesory × jádra_na_procesor × vlákna_na_jádro
```

Toto je **celková kapacita** plánovače — kolik procesů/vláken může zároveň vykonávat výpočet.

### 2. Vypočítej dobu jednoho vlákna pro každý proces

```text
doba_vlákna[P] = celková_doba[P] / počet_vláken[P]
```

Toto číslo ti říká, kolik práce (v sekundách) musí zvládnout jedno vlákno, aby celý výpočet procesu P byl dokončen. Zároveň platí: pokud procesu přidělíš přesně tolik HW vláken, kolik jich má, poběží právě `doba_vlákna` sekund.

### 3. Seřaď procesy podle priority sestupně

Vytvoř si tabulku seřazenou od nejvyšší po nejnižší prioritu. Při shodné prioritě je pořadí ve sloupci libovolné (obě skupiny se zpracovávají současně).

| Proces | Priorita | Vláken | Celková doba | Doba vlákna |
| ------ | -------- | ------ | ------------ | ----------- |
| ...    | ...      | ...    | ...          | ...         |

### 4. Přidel HW vlákna v první fázi (čas T0)

Prochází tabulku shora dolů (od nejvyšší priority):

- Procesu s nejvyšší prioritou přiřaď tolik HW vláken, kolik požaduje (tj. kolik má vláken), **nejvýše** tolik, kolik zbývá volných.
- Odečti přidělená vlákna od dostupného počtu.
- Pokračuj s dalším procesem v pořadí (nižší priorita).
- Pokud při přidělování dojdeš k **více procesům se stejnou prioritou** a zbývá méně vláken než by potřebovaly dohromady, rozděl dostupná vlákna **poměrně** (viz krok 5).
- Procesy, na které vlákna nevyjdou (nejnižší priority), **čekají** — nedostávají nic.

### 5. Poměrné dělení při shodné prioritě

Mají-li dva (nebo více) procesů stejnou prioritu a sdílejí `V` dostupných HW vláken:

```text
vlákna[Pi] = V × (počet_vláken[Pi] / součet_vláken_skupiny)
```

Toto je zlomkové číslo — **nemusí** vyjít celé. To je v pořádku; HW vlákno pak pracuje na více procesech střídavě (nebo jen zčásti) a výpočet doby odpovídá tomu zlomku výkonu.

**Příklad:** Procesy A (2 vlákna) a B (3 vlákna) sdílejí 1 HW vlákno.
- A dostane: 1 × (2/5) = 0.4 vlákna
- B dostane: 1 × (3/5) = 0.6 vlákna

### 6. Urči reálnou dobu běhu každého procesu v této fázi

Pro každý běžící proces spočítej, za jak dlouho by dokončil práci, kdyby měl přidělení po celou dobu fáze:

```text
real_time[P] = celková_zbývající_práce[P] / přidělených_vláken[P]
```

kde `celková_zbývající_práce[P]` je (zatím) celková doba výpočtu (v první fázi = původní `celková_doba`).

### 7. Najdi proces, který doběhne jako první

Ze všech aktuálně běžících procesů vyber ten s nejmenším `real_time`. Délka fáze = `real_time` tohoto procesu. Označme ji `delta`.

### 8. Zaznamenej čas ukončení a "odvedenou práci"

- Čas ukončení procesu, který doběhl: `T_aktuální + delta`.
- Pro **každý ostatní** běžící proces spočítej, kolik práce bylo za dobu `delta` odvedeno:

```text
odvedená_práce[P] = přidělená_vlákna[P] × delta
zbývající_práce[P] = zbývající_práce[P] - odvedená_práce[P]
```

Nebo ekvivalentně: zbývající real_time pro každý jiný proces se zkrátí o `delta` (protože všichni běželi stejnou dobu).

### 9. Uvolni vlákna dokončeného procesu a aktualizuj dostupná vlákna

Proces, který doběhl, uvolní svá HW vlákna. Nový počet dostupných vláken:

```text
dostupná_vlákna = dostupná_vlákna + vlákna_dokončeného_procesu
```

### 10. Přerozděl vlákna pro novou fázi

Opakuj kroky 4–9 se zbývajícími procesy a nově dostupnými vlákny.

Pozor: pokud se uvolní vlákna a čekající procesy (nižší priority) mohou nyní dostat přidělení, jsou aktivovány — ale teprve **od tohoto okamžiku** začínají fakticky běžet.

### 11. Zohledni background load (pokud je zadán)

Pokud zadání říká „jádro a ostatní procesy zatěžují CPU z X %":

- Efektivní výkon procesoru je jen `(100 - X) %`.
- Všechny vypočítané reálné časy (v sekundách) vynásob faktorem `100 / (100 - X)`.

```text
čas_s_bg_load = čas_bez_bg_load × (100 / (100 - X))
```

Příklad: výsledek 90 s při zatížení 68 %: `90 × (100 / 32) = 281.25 s`.

### 12. Opakuj, dokud nedoběhnou všechny procesy

Výsledkem je seznam: kdy doběhl každý proces a celkový čas od T0 do ukončení posledního procesu.

---

## Vzorové zadání

!!! example "Zadání"
    Systém: 4 procesory, každý má 1 jádro, 1 vlákno na jádro. OS používá **statickou prioritu** (vyšší hodnota = vyšší priorita). Jádro a ostatní procesy procesor nezatěžují. Všichni uživatelé spustí procesy v čase T0:

    | Proces | Statická priorita | Počet vláken | Celková doba výpočtu [s] |
    | ------ | ----------------- | ------------ | ------------------------ |
    | P0     | 0                 | 3            | 108                      |
    | P1     | 26                | 1            | 54                       |
    | P2     | 80                | 3            | 270                      |
    | P3     | 71                | 1            | 45                       |
    | P4     | 0                 | 4            | 72                       |
    | P5     | 26                | 2            | 72                       |

    1. Za kolik sekund po T0 se ukončí proces P2?
    2. Za kolik sekund po T0 se fakticky začne zpracovávat P1?
    3. Za kolik sekund po T0 se ukončí poslední proces?

    *Tento typ se objevil prakticky v každém termínu: 2011, 2014, 2018, 2019, 2023.*

---

## Řešení vzorového zadání

??? success "Ukázat řešení"

    ### Krok 1: Počet HW vláken

    ```text
    HW = 4 procesory × 1 jádro × 1 vlákno = 4 HW vlákna
    ```

    ### Krok 2: Tabulka seřazená podle priority (sestupně) a doby vlákna

    | Proces | Priorita | Vláken | Celková doba [s] | Doba vlákna [s] |
    | ------ | -------- | ------ | ---------------- | --------------- |
    | P2     | 80       | 3      | 270              | 90              |
    | P3     | 71       | 1      | 45               | 45              |
    | P1     | 26       | 1      | 54               | 54              |
    | P5     | 26       | 2      | 72               | 36              |
    | P0     | 0        | 3      | 108              | 36              |
    | P4     | 0        | 4      | 72               | 18              |

    ### Krok 3: Fáze 1 — přidělení vláken v T0

    Přidělujeme shora dolů z dostupných 4 HW vláken:

    - **P2 (priorita 80)** chce 3 vlákna → dostane **3**, zbývá 4 − 3 = 1.
    - **P3 (priorita 71)** chce 1 vlákno → dostane **1**, zbývá 1 − 1 = 0.
    - **P1, P5 (priorita 26)** → 0 dostupných vláken → **čekají**.
    - **P0, P4 (priorita 0)** → 0 dostupných vláken → **čekají**.

    Reálná doba běhu v této fázi:

    ```text
    P2: real_time = 270 / 3 = 90 s
    P3: real_time =  45 / 1 = 45 s
    ```

    Jako první doběhne **P3** za **45 s**.

    > **Odpověď na otázku 1:** P2 dostane celou dobu 3 vlákna, proto skončí za `270 / 3 = 90 s`.

    ### Krok 4: Fáze 2 — po ukončení P3 (T0 + 45 s)

    P3 uvolnil 1 HW vlákno → dostupná vlákna = 0 + 1 = **1**.

    Zbývající práce P2: běžel 45 s × 3 vlákna → odvedl 135 s práce → zbývá `270 − 135 = 135 s`.

    Přidělení:

    - **P2 (priorita 80)** stále běží se **3 vlákny** (ta mu nebyla odebrána).
    - Uvolněné 1 vlákno jde na nejbližší čekající procesy: **P1 a P5 (priorita 26)** — sdílejí 1 HW vlákno poměrně:
      - P1 má 1 vlákno, P5 má 2 vlákna → součet = 3.
      - P1 dostane: 1 × (1/3) ≈ 0.333 vlákna
      - P5 dostane: 1 × (2/3) ≈ 0.667 vlákna

    > **Odpověď na otázku 2:** P1 fakticky začne přijímat výpočetní výkon v čase **T0 + 45 s**.

    Reálná doba běhu v této fázi (od T0 + 45):

    ```text
    P2: real_time = 135 / 3 = 45 s   → doběhne v T0 + 45 + 45 = T0 + 90 s
    P1: real_time =  54 / (1/3) = 162 s
    P5: real_time =  72 / (2/3) = 108 s
    ```

    Jako první doběhne **P2** za **45 s** od začátku fáze.

    Za těchto 45 s každý z ostatních odvedl:

    ```text
    P1: odvedená práce = (1/3) × 45 = 15 s → zbývá 54 − 15 = 39 s
    P5: odvedená práce = (2/3) × 45 = 30 s → zbývá 72 − 30 = 42 s   (doba vlákna: 42/2 = 21 s)
    ```

    ### Krok 5: Fáze 3 — po ukončení P2 (T0 + 90 s)

    P2 uvolnil 3 HW vlákna → dostupná vlákna = 0 + 3 = **3** (plus P1 a P5 stále sdílejí to 1 původní → celkem 4 vlákna dostupná pro procesy priority 26 a níže, ale přidělujeme od nejvyšší priority).

    Přidělení:

    - **P1 + P5 (priorita 26)** dohromady chtějí 1 + 2 = 3 vláken → dostupná jsou 4, ale jejich součet je 3 → dostanou plně **3 vlákna** (P1 → 1, P5 → 2). Zbývá 4 − 3 = **1 vlákno**.
    - **P0 + P4 (priorita 0)** sdílejí zbylé **1 vlákno** poměrně: P0 má 3 vlákna, P4 má 4 → součet = 7.
      - P0 dostane: 1 × (3/7) vlákna
      - P4 dostane: 1 × (4/7) vlákna

    Reálná doba běhu v této fázi (od T0 + 90):

    ```text
    P1: real_time = 39 / 1 = 39 s
    P5: real_time = 42 / 2 = 21 s   → doběhne nejdříve
    P0: real_time = 108 / (3/7) = 252 s
    P4: real_time =  72 / (4/7) = 126 s
    ```

    Jako první doběhne **P5** za **21 s** od začátku fáze → v čase T0 + 111 s.

    Za těchto 21 s ostatní odvedli:

    ```text
    P1: odvedená práce = 1 × 21 = 21 s   → zbývá 39 − 21 = 18 s
    P0: odvedená práce = (3/7) × 21 = 9 s → zbývá 108 − 9 = 99 s
    P4: odvedená práce = (4/7) × 21 = 12 s → zbývá 72 − 12 = 60 s
    ```

    ### Krok 6: Fáze 4 — po ukončení P5 (T0 + 111 s)

    P5 uvolnil 2 HW vlákna → dostupná vlákna = 2.

    Přidělení:

    - **P1 (priorita 26)** chce 1 vlákno → dostane **1**. Zbývá 2 − 1 = **1**.
    - **P0 + P4 (priorita 0)** sdílejí zbylé **1 vlákno** poměrně (3:4):
      - P0: 1 × (3/7) vlákna
      - P4: 1 × (4/7) vlákna

    Reálná doba běhu (od T0 + 111):

    ```text
    P1: real_time = 18 / 1 = 18 s   → doběhne nejdříve
    P0: real_time = 99 / (3/7) = 231 s
    P4: real_time = 60 / (4/7) = 105 s
    ```

    Jako první doběhne **P1** za **18 s** → v čase T0 + 129 s.

    Za těchto 18 s ostatní odvedli:

    ```text
    P0: odvedená práce = (3/7) × 18 = 54/7 s  → zbývá 99 − 54/7 = (693 − 54)/7 = 639/7 s
    P4: odvedená práce = (4/7) × 18 = 72/7 s  → zbývá 60 − 72/7 = (420 − 72)/7 = 348/7 s

    Přepočet: 639/7 ≈ 91.286 s a 348/7 ≈ 49.714 s
    ```

    ### Krok 7: Fáze 5 — po ukončení P1 (T0 + 129 s)

    P1 uvolnil 1 HW vlákno → dostupná vlákna = 0 + 1 = 1, celkem pro P0 a P4: **4 HW vlákna**.

    Přidělení:

    - **P0 + P4 (priorita 0)** dohromady chtějí 3 + 4 = 7 vláken, ale dostupná jsou jen **4** → sdílejí poměrně (3:4):
      - P0 dostane: 4 × (3/7) = 12/7 vlákna
      - P4 dostane: 4 × (4/7) = 16/7 vlákna

    Reálná doba běhu (od T0 + 129):

    ```text
    P0: real_time = (639/7) / (12/7) = 639/12 = 53.25 s
    P4: real_time = (348/7) / (16/7) = 348/16 = 21.75 s   → doběhne nejdříve
    ```

    Jako první doběhne **P4** za **21.75 s** → v čase T0 + 129 + 21.75 = **T0 + 150.75 s**.

    Za těchto 21.75 s P0 odvedl:

    ```text
    P0: odvedená práce = (12/7) × 21.75 = 12 × 21.75 / 7 = 261/7 = 37.286 s
        zbývá: 639/7 − 261/7 = 378/7 = 54 s
    ```

    ### Krok 8: Fáze 6 — po ukončení P4 (T0 + 150.75 s)

    P4 uvolnil (16/7) vláken → dostupná vlákna pro P0 = **4** (všechna).

    P0 chce 3 vlákna → dostane **3**.

    ```text
    P0: real_time = 54 / 3 = 18 s → doběhne v T0 + 150.75 + 18 = T0 + 168.75 s
    ```

    !!! warning "Pozor na záludný krok"
        Výsledek je citlivý na to, jak přesně počítáš zbývající práci po fázích 4 a 5
        a odkdy dostávají vlákna procesy P0 a P4 (až od T0 + 90 s, kdy se uvolní tři
        vlákna — ne dřív). Když mezisoučty zaokrouhluješ nebo tento okamžik určíš
        špatně, dostaneš jiný, chybný čas. **Počítej se zlomky a nezaokrouhluj
        mezivýsledky** — zaokrouhli teprve finální čas. Průběh si vždy ověř na časové
        ose podle konkrétních čísel ze zadání.

    ### Shrnutí výsledků

    | Otázka | Odpověď |
    | ------ | ------- |
    | 1. Kdy se ukončí P2? | **T0 + 90 s** |
    | 2. Kdy fakticky začne P1? | **T0 + 45 s** |
    | 3. Kdy doběhne poslední? | **T0 + 168.75 s** (viz poznámka výše) |

    !!! warning "Background load"
        Kdyby zadání řeklo „jádro a ostatní procesy zatěžují procesor z 68 %", všechny výsledky se násobí `100 / (100 − 68) = 100 / 32 = 3.125`. Například: P2 doběhne za `90 × 3.125 = 281.25 s`.

---

## Další procvičení

### Varianta A — méně procesů, jiná konfigurace

!!! example "Zadání A"
    Systém: 2 procesory, každý 2 jádra, 1 vlákno na jádro (celkem 4 HW vlákna). Statická priorita (vyšší = lepší). Jádro nezatěžuje CPU. Všechny procesy spuštěny v T0:

    | Proces | Priorita | Vláken | Celková doba [s] |
    | ------ | -------- | ------ | ---------------- |
    | A      | 50       | 2      | 60               |
    | B      | 50       | 2      | 40               |
    | C      | 20       | 3      | 90               |

    1. Za kolik sekund doběhne proces B?
    2. Za kolik sekund doběhne poslední proces?

??? success "Řešení A"

    **HW vlákna:** 2 × 2 × 1 = **4**.

    **Doba vlákna:**

    ```text
    A: 60 / 2 = 30 s
    B: 40 / 2 = 20 s
    C: 90 / 3 = 30 s
    ```

    **Fáze 1 (T0):**

    - A + B (priorita 50) dohromady chtějí 2 + 2 = 4 vláken → dostupná 4 → dostanou plně.
      - A → 2 vlákna, B → 2 vlákna.
    - C (priorita 20) → zbývá 0 vláken → čeká.

    Reálné doby:

    ```text
    A: 60 / 2 = 30 s
    B: 40 / 2 = 20 s   → B doběhne jako první
    ```

    B doběhne po **20 s** → v čase **T0 + 20 s**.

    Za 20 s A odvedl: 2 × 20 = 40 s práce → zbývá 60 − 40 = **20 s**.

    **Fáze 2 (T0 + 20 s):**

    B uvolnil 2 HW vlákna → dostupná = 2.

    - **A (priorita 50)** běží dál (má stále 2 vlákna).
    - Dostupná 2 vlákna přidělíme C (priorita 20, nic jiného nečeká): C dostane **2 vlákna** (chce 3, ale dostane max 2).

    Reálné doby (od T0 + 20):

    ```text
    A: 20 / 2 = 10 s   → A doběhne jako první
    C: 90 / 2 = 45 s
    ```

    A doběhne po **10 s** → v čase T0 + 30 s.

    Za 10 s C odvedl: 2 × 10 = 20 s práce → zbývá 90 − 20 = **70 s**.

    **Fáze 3 (T0 + 30 s):**

    A uvolnil 2 HW vlákna → dostupná = 2. Celkem C má nyní 2 + 2 = **4 vlákna** (ale chce jen 3 → dostane **3**).

    ```text
    C: real_time = 70 / 3 ≈ 23.33 s → doběhne v T0 + 30 + 23.33 = T0 + 53.33 s
    ```

    **Výsledky:**

    | Otázka | Odpověď |
    | ------ | ------- |
    | 1. Kdy doběhne B? | **T0 + 20 s** |
    | 2. Kdy doběhne poslední? | **T0 + 53.33 s** |

---

### Varianta B — s background load

!!! example "Zadání B"
    Stejná konfigurace jako ve vzorovém zadání (4 HW vlákna), ale jádro a ostatní procesy zatěžují CPU z **25 %**. Procesy:

    | Proces | Priorita | Vláken | Celková doba [s] |
    | ------ | -------- | ------ | ---------------- |
    | X      | 10       | 2      | 80               |
    | Y      | 10       | 2      | 40               |
    | Z      | 5        | 2      | 60               |

    1. Za kolik sekund doběhne Y?
    2. Za kolik sekund doběhne poslední proces (s background load)?

??? success "Řešení B"

    **HW vlákna:** 4.

    **Bez background load nejprve:**

    Fáze 1 (T0): X a Y (priorita 10) sdílejí 4 vlákna → X dostane 2, Y dostane 2. Z čeká.

    ```text
    X: 80 / 2 = 40 s
    Y: 40 / 2 = 20 s   → Y doběhne první
    ```

    Y doběhne po **20 s**. Za tu dobu X odvedl 2 × 20 = 40 s → zbývá 80 − 40 = 40 s.

    Fáze 2 (T0 + 20 s): Y uvolnil 2 vlákna. X stále 2 vlákna; Z dostane uvolněná 2 vlákna.

    ```text
    X: 40 / 2 = 20 s   → X doběhne první
    Z: 60 / 2 = 30 s
    ```

    X doběhne po 20 s → T0 + 40 s. Za tu dobu Z odvedl 2 × 20 = 40 s → zbývá 60 − 40 = 20 s.

    Fáze 3 (T0 + 40 s): Z dostane všechna 4 vlákna, ale chce jen 2 → dostane **2**.

    ```text
    Z: 20 / 2 = 10 s → doběhne v T0 + 50 s
    ```

    Výsledky bez background load: Y = 20 s, poslední = 50 s.

    **S background load 25 %:**

    ```text
    faktor = 100 / (100 − 25) = 100 / 75 = 4/3 ≈ 1.333

    Y doběhne za: 20 × (4/3) = 80/3 ≈ 26.67 s
    Poslední za:  50 × (4/3) = 200/3 ≈ 66.67 s
    ```

    | Otázka | Odpověď |
    | ------ | ------- |
    | 1. Kdy doběhne Y (s BG load 25 %)? | **≈ 26.67 s** |
    | 2. Kdy doběhne poslední (s BG load 25 %)? | **≈ 66.67 s** |

---

## Varianty a chytáky

- **Round-robin / časové kvantum:** zadání může zmínit kvantum nebo přepínání kontextu — zpravidla se **zanedbává** (slouží jen jako popis strategie). Počítej, jako by každý proces běžel spojitě.
- **Různý výkon jader:** pokud mají jádra různý výkon, uprav vzorec `real_time` o koeficient výkonu. Pokud jsou všechna jádra stejně rychlá, výkon se nemění.
- **Procesy spuštěné v různých časech:** pokud nejsou všechny spuštěny v T0, nepřiděluj jim vlákna dříve, než jsou spuštěny. V okamžiku spuštění nového procesu přerozděluj.
- **Vlákna vs. procesy:** zadání někdy říká „vlákna procesu provádějí výpočet" — jedno vlákno procesu = jedno HW vlákno. Pokud proces má 3 vlákna, potřebuje 3 HW vlákna k lineárnímu zrychlení.
- **„Fakticky začne zpracovávat"** = okamžik, kdy proces poprvé dostane alespoň část HW vlákna (výpočetního výkonu). Procesy čekající bez přidělení ještě „nezačaly".
- **Lineární zrychlení je předpoklad:** ve skutečnosti platí Amdahlův zákon, ale zadání výslovně předpokládá lineární zrychlení — neřeš paralelní overhead.
- **Vícenásobné shodné priority s nedostatkem vláken:** poměrné dělení vede na zlomková čísla — pracuj s nimi jako zlomky, nezaokrouhluj průběžně.

---

## Časté chyby

1. **Zapomenutí na přerozdělení vláken** po ukončení procesu. Každé ukončení = nová fáze = znova přiděluj od nejvyšší priority.
2. **Záměna „celková doba" a „doba vlákna".** `celková_doba` je práce celého procesu (při 1 vláknu). `real_time = celková_doba / přidělená_vlákna` — NE `celková_doba × přidělená_vlákna`.
3. **Nespočítání odvedené práce pro ostatní procesy** po skončení fáze. Vždy odečti, co bylo hotovo.
4. **Ignorování čekajících procesů.** Procesy s nižší prioritou dostávají vlákna teprve po ukončení procesů s vyšší prioritou — dříve se neobjevují ve výpočtu.
5. **Background load zapomenout nebo aplikovat špatně.** Faktor `100 / (100 - X)` se násobí **výsledným časem**, ne přidělovanými vlákny.
6. **Zaokrouhlování mezivýsledků.** Zlomky (jako 3/7 vlákna) zachovávej v přesném tvaru po celou dobu výpočtu — zaokrouhluj až finální odpověď.
7. **Špatné poměrné dělení.** Poměr se počítá z **počtu vláken procesu**, ne z jeho doby výpočtu. A dělí se **dostupná HW vlákna**, ne celkový počet.

---

## Související

- [Skripta: Plánování procesů a vláken](../../skripta/05-planovani.md)
- [Teoretické otázky — True/False](../teorie-truefalse.md)
- [Zpět na přehled praktických příkladů](index.md)
