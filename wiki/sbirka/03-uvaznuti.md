# Uváznutí

??? abstract "Obsah stránky"

    [TOC]

---

V systému existují následující typy prostředků: T0, ..., T3. Prostředky daného typu jsou rovnocenné, tzn. pokud proces požádá o prostředek typu Ti, kterého existuje v systému několik instancí, pak mu je jedno, která instance mu je přidělena. Prostředky jsou buď volné a nebo přidělené právě jednomu procesu. Prostředky jsou přidělovány jednotlivým procesům jádrem systému. Pouze proces, který má prostředek přidělen, ho může také následně uvolnit a uvolní ho při svém ukončení.

V systému běží následující procesy: P0, ..., P4. U každého procesu předem víme, které prostředky a v jakém počtu bude proces vyžadovat.

**Coffmanovy podmínky** — uváznutí nastane pouze pokud jsou splněny následující podmínky:

- **(a) Vzájemné vyloučení:** každý prostředek je buď přidělen právě jednomu vláknu a nebo je volný (prostředek nemůže být sdílen více vlákny)
- **(b) Podmínka neodnímatelnosti:** prostředek, který byl již přidělen nějakému vláknu, nemůže mu být násilím odebrán (musí být dobrovolně uvolněn daným vláknem)
- **(c) Podmínka „drž a čekej":** vlákno, které má již přiděleny nějaké prostředky, může žádat o další prostředky (vlákno může žádat o prostředky postupně)
- **(d) Podmínka kruhového čekání:** musí existovat smyčka dvou nebo více vláken, ve které každé vlákno čeká na prostředek přidelený dalšímu vláknu ve smyčce

První tři podmínky jsou nutné, ale ne dostačující => k uváznutí může dojít. Poslední podmínka představuje samotné uváznutí.

Pokud aspoň jedna z podmínek není splněna, nemůže dojít k uváznutí.

---

## Úloha 1 — Bankéřův algoritmus: nebezpečný stav, deadlock P0, P2, P3

!!! example "Zadání"
    V systému existují následující typy prostředků: T0, ..., T3. V systému běží procesy P0, ..., P4. V tomto okamžiku je již část prostředků přidělena jednotlivým procesům, viz následující tabulka:

    | Proces | Max T0 | Max T1 | Max T2 | Max T3 | Přiděleno T0 | Přiděleno T1 | Přiděleno T2 | Přiděleno T3 |
    |--------|--------|--------|--------|--------|--------------|--------------|--------------|--------------|
    | P0     | 5      | 5      | 4      | 4      | 1            | 0            | 2            | 2            |
    | P1     | 1      | 1      | 1      | 1      | 1            | 0            | 0            | 1            |
    | P2     | 4      | 4      | 6      | 4      | 3            | 3            | 0            | 1            |
    | P3     | 3      | 3      | 8      | 4      | 0            | 2            | 2            | 2            |
    | P4     | 1      | 0      | 0      | 1      | 1            | 0            | 0            | 1            |

    A část prostředků je ještě volná, viz následující tabulka:

    | Typ prostředku  | T0 | T1 | T2 | T3 |
    |-----------------|----|----|----|----|
    | Počet prostředků | 0  | 1  | 5  | 1  |

    **Otázky:**

    1. Která z následujících tvrzení jsou platná?
        - (a) Systém se nachází v "bezpečném" stavu, protože jednotlivé procesy můžeme uspokojit v následujícím pořadí P0, P4, P2, P1, P3.
        - (b) Systém se nachází v "bezpečném" stavu.
        - (c) Systém se nachází v "nebezpečném" stavu.
        - (d) Systém se nachází v "bezpečném" stavu, protože jednotlivé procesy můžeme uspokojit v následujícím pořadí P3, P2, P0, P1, P4.
        - (e) Systém se nachází v "nebezpečném" stavu, protože neexistuje posloupnost alokací prostředků chi = {chi_1, chi_2, ..., chi_j} taková, že v bodě chi_k, 1 <= k <= j budou alokovány všechny potřebné prostředky pro uspokojení procesu P3.

    2. Pro toto zadání dále vyberte pravdivá tvrzení:
        - (a) Systém se nachází v "nebezpečném" stavu, protože aspoň jedna Coffmanova podmínka není splněna.
        - (b) Systém se nachází v "nebezpečném" stavu, ale porušením Coffmanových podmínek by se dalo zabránit deadlocku.
        - (c) Systém se nachází v "bezpečném" stavu, přestože všechny Coffmanovy podmínky jsou splněné.
        - (d) Systém se nachází v "bezpečném" stavu, protože všechny Coffmanovy podmínky jsou splněné.
        - (e) Systém se nachází v "nebezpečném" stavu, protože aspoň jedna Coffmanova podmínka je splněná.

??? success "Řešení"
    **Krok 1: Sestav matici Potřebné = Požadované - Přidělené**

    ```
    Požadované        Již přidělené       Potřebné
       T0 T1 T2 T3      T0 T1 T2 T3        T0 T1 T2 T3
    P0 [ 5  5  4  4]  P0 [ 1  0  2  2]  P0 [ 4  5  2  2]
    P1 [ 1  1  1  1]  P1 [ 1  0  0  1]  P1 [ 0  1  1  0]
    P2 [ 4  4  6  4]  P2 [ 3  3  0  1]  P2 [ 1  1  6  3]
    P3 [ 3  3  8  4]  P3 [ 0  2  2  2]  P3 [ 3  1  6  2]
    P4 [ 1  0  0  1]  P4 [ 1  0  0  1]  P4 [ 0  0  0  0]
    ```

    | Proces | Potřeba T0 | Potřeba T1 | Potřeba T2 | Potřeba T3 |
    |--------|------------|------------|------------|------------|
    | P0     | 4          | 5          | 2          | 2          |
    | P1     | 0          | 1          | 1          | 0          |
    | P2     | 1          | 1          | 6          | 3          |
    | P3     | 3          | 1          | 6          | 2          |
    | P4     | 0          | 0          | 0          | 0          |

    **Krok 2: Inicializace**

    ```
    Volné = (0, 1, 5, 1)
    ```

    **Proces P4 je již uspokojen**, protože má přiděleny všechny potřebné prostředky (Potřeba = (0,0,0,0) <= (0,1,5,1)).

    Dostaneme zpět jeden prostředek typu T0 a jeden typu T3 a zůstávají nám:

    | Typ prostředku   | T0 | T1 | T2 | T3 |
    |------------------|----|----|----|----|
    | Počet prostředků | 1  | 1  | 5  | 2  |

    **Krok 3: Uspokojíme P1**

    V tento moment můžeme uspokojit pouze jeden proces P1, který ještě potřebuje jeden prostředek typu T1 a jeden typu T2. Podmínka Potřeba[P1] = (0,1,1,0) <= (1,1,5,2) je splněna.

    Dostaneme zpět jeden prostředek typu T0 a jeden typu T3 a zůstávají nám:

    | Typ prostředku   | T0 | T1 | T2 | T3 |
    |------------------|----|----|----|----|
    | Počet prostředků | 2  | 1  | 5  | 3  |

    **Krok 4: Výsledek**

    Na uspokojení procesů P0, P2 a P3 nemáme prostředky. Nastává **deadlock**.

    - P0: Potřeba (4,5,2,2) — T1: 5 > 1, nelze uspokojit
    - P2: Potřeba (1,1,6,3) — T2: 6 > 5, nelze uspokojit
    - P3: Potřeba (3,1,6,2) — T2: 6 > 5, nelze uspokojit

    Bezpečná posloupnost (částečná): **P4 -> P1**, poté nastane deadlock pro P0, P2, P3.

    **Odpovědi:**

    **Otázka 1:**
    - (a) NEPRAVDA — pořadí P0, P4, P2, P1, P3 není bezpečné (P0 nelze uspokojit jako první)
    - (b) NEPRAVDA — systém je v nebezpečném stavu
    - **(c) PRAVDA** — systém se nachází v nebezpečném stavu
    - (d) NEPRAVDA — toto pořadí není bezpečné
    - **(e) PRAVDA** — neexistuje bezpečná posloupnost zahrnující P3 (deadlock nastane pro P0, P2, P3)

    Tímto nebezpečným stavem je myšlen deadlock popsaný výše, vyjádřený v odpovědi (e).

    **Otázka 2:**
    - (a) NEPRAVDA — nebezpečný stav nesouvisí s nesplněním Coffmanových podmínek
    - **(b) PRAVDA** — systém je v nebezpečném stavu, ale porušením Coffmanových podmínek by se dalo zabránit deadlocku
    - (c) NEPRAVDA — systém není v bezpečném stavu
    - (d) NEPRAVDA — systém není v bezpečném stavu
    - (e) NEPRAVDA — splnění Coffmanových podmínek nezpůsobuje nebezpečný stav

---

## Úloha 2 — Bankéřův algoritmus: nebezpečný stav, deadlock P0, P2, P3

!!! example "Zadání"
    V systému existují typy prostředků T0, ..., T3 a procesy P0, ..., P4. V tomto okamžiku je již část prostředků přidělena jednotlivým procesům, viz následující tabulka:

    | Proces | Max T0 | Max T1 | Max T2 | Max T3 | Přiděleno T0 | Přiděleno T1 | Přiděleno T2 | Přiděleno T3 |
    |--------|--------|--------|--------|--------|--------------|--------------|--------------|--------------|
    | P0     | 1      | 3      | 4      | 8      | 0            | 0            | 0            | 4            |
    | P1     | 1      | 4      | 0      | 0      | 1            | 0            | 0            | 0            |
    | P2     | 0      | 2      | 2      | 8      | 0            | 2            | 2            | 0            |
    | P3     | 1      | 0      | 0      | 6      | 0            | 0            | 0            | 4            |
    | P4     | 1      | 0      | 0      | 1      | 0            | 0            | 0            | 0            |

    A část prostředků je ještě volná, viz následující tabulka:

    | Typ prostředku   | T0 | T1 | T2 | T3 |
    |------------------|----|----|----|----|
    | Počet prostředků | 1  | 5  | 3  | 1  |

    **Otázky:**

    1. Která z následujících tvrzení jsou platná?
        - (a) Systém se nachází v "bezpečném" stavu.
        - (b) Systém se nachází v "bezpečném" stavu, protože jednotlivé procesy můžeme uspokojit v následujícím pořadí P4, P1, P3, P2, P0.
        - (c) Systém se nachází v "nebezpečném" stavu, protože nemáme dostatečný počet prostředků, abychom uspokojili proces P2.
        - (d) Systém se nachází v "bezpečném" stavu, protože jednotlivé procesy můžeme uspokojit v následujícím pořadí P3, P1, P2, P0, P4.
        - (e) Systém se nachází v "nebezpečném" stavu.

    2. Pro toto zadání dále vyberte pravdivá tvrzení:
        - (a) Systém se nachází v "bezpečném" stavu, protože v alokačním grafu závislostí není cyklus.
        - (b) Systém se nachází v "nebezpečném" stavu, protože aspoň jedna Coffmanova podmínka je splněna.
        - (c) Systém se nachází v "bezpečném" stavu, protože všechny Coffmanovy podmínky jsou splněné.
        - (d) Systém se nachází v "nebezpečném" stavu, protože aspoň jedna Coffmanova podmínka není splněna.
        - (e) Systém se nachází v "nebezpečném" stavu, ale porušením Coffmanových podmínek by se dalo zabránit deadlocku.

??? success "Řešení"
    **Krok 1: Sestav matici Potřebné = Požadované - Přidělené**

    ```
    Požadované        Již přidělené       Potřebné
       T0 T1 T2 T3      T0 T1 T2 T3        T0 T1 T2 T3
    P0 [ 1  3  4  8]  P0 [ 0  0  0  4]  P0 [ 1  3  4  4]
    P1 [ 1  4  0  0]  P1 [ 1  0  0  0]  P1 [ 0  4  0  0]
    P2 [ 0  2  2  8]  P2 [ 0  2  2  0]  P2 [ 0  0  0  8]
    P3 [ 1  0  0  6]  P3 [ 0  0  0  4]  P3 [ 1  0  0  2]
    P4 [ 1  0  0  1]  P4 [ 0  0  0  0]  P4 [ 1  0  0  1]
    ```

    | Proces | Potřeba T0 | Potřeba T1 | Potřeba T2 | Potřeba T3 |
    |--------|------------|------------|------------|------------|
    | P0     | 1          | 3          | 4          | 4          |
    | P1     | 0          | 4          | 0          | 0          |
    | P2     | 0          | 0          | 0          | 8          |
    | P3     | 1          | 0          | 0          | 2          |
    | P4     | 1          | 0          | 0          | 1          |

    **Krok 2: Inicializace**

    ```
    Volné = (1, 5, 3, 1)
    ```

    **Krok 3: Uspokojíme P4**

    Potřeba[P4] = (1,0,0,1) <= (1,5,3,1) — ANO.

    Zůstávají nám (po vrácení alokace P4 = (0,0,0,0)):

    | Typ prostředku   | T0 | T1 | T2 | T3 |
    |------------------|----|----|----|----|
    | Počet prostředků | 1  | 5  | 3  | 1  |

    **Krok 4: Uspokojíme P1**

    Potřeba[P1] = (0,4,0,0) <= (1,5,3,1) — ANO.

    Dostaneme zpět jeden prostředek typu T0, zůstávají nám:

    | Typ prostředku   | T0 | T1 | T2 | T3 |
    |------------------|----|----|----|----|
    | Počet prostředků | 2  | 5  | 3  | 1  |

    **Krok 5: Výsledek**

    Na uspokojení procesů P0, P2 a P3 nemáme prostředky. Nastává **deadlock**.

    - P0: Potřeba (1,3,4,4) — T3: 4 > 1, nelze uspokojit
    - P2: Potřeba (0,0,0,8) — T3: 8 > 1, nelze uspokojit
    - P3: Potřeba (1,0,0,2) — T3: 2 > 1, nelze uspokojit

    Bezpečná posloupnost (částečná): **P4 -> P1**, poté nastane deadlock pro P0, P2, P3.

    **Odpovědi:**

    **Otázka 1:**
    - (a) NEPRAVDA — systém je v nebezpečném stavu
    - (b) NEPRAVDA — pořadí P4, P1, P3, P2, P0 není bezpečné (po P4 a P1 nelze uspokojit P3)
    - **(c) PRAVDA** — systém je v nebezpečném stavu, protože nemáme dostatečný počet prostředků T3 (P2 potřebuje 8, ale máme jen 1)
    - (d) NEPRAVDA — toto pořadí není bezpečné
    - **(e) PRAVDA** — systém se nachází v nebezpečném stavu

    **Otázka 2:**
    - (a) NEPRAVDA — absence cyklu v alokačním grafu nestačí pro víceinstancové prostředky
    - (b) NEPRAVDA — splnění Coffmanových podmínek není příčinou nebezpečného stavu
    - (c) NEPRAVDA — systém není v bezpečném stavu
    - (d) NEPRAVDA — nesplnění Coffmanových podmínek není příčinou nebezpečného stavu
    - **(e) PRAVDA** — systém je v nebezpečném stavu, ale porušením Coffmanových podmínek by se dalo zabránit deadlocku

---

## Úloha 3 — Bankéřův algoritmus: bezpečný stav, pořadí P3, P2, P1, P4, P0

!!! example "Zadání"
    V systému existují typy prostředků T0, ..., T3 a procesy P0, ..., P4. V tomto okamžiku je již část prostředků přidělena jednotlivým procesům, viz následující tabulka:

    | Proces | Max T0 | Max T1 | Max T2 | Max T3 | Přiděleno T0 | Přiděleno T1 | Přiděleno T2 | Přiděleno T3 |
    |--------|--------|--------|--------|--------|--------------|--------------|--------------|--------------|
    | P0     | 1      | 6      | 1      | 5      | 0            | 0            | 0            | 0            |
    | P1     | 1      | 0      | 0      | 0      | 0            | 0            | 0            | 0            |
    | P2     | 0      | 5      | 0      | 2      | 0            | 4            | 0            | 1            |
    | P3     | 1      | 2      | 0      | 2      | 0            | 2            | 0            | 1            |
    | P4     | 0      | 5      | 1      | 5      | 0            | 0            | 0            | 1            |

    A část prostředků je ještě volná, viz následující tabulka:

    | Typ prostředku   | T0 | T1 | T2 | T3 |
    |------------------|----|----|----|----|
    | Počet prostředků | 2  | 2  | 2  | 3  |

    **Otázky:**

    1. Která z následujících tvrzení jsou platná?
        - (a) Systém se nachází v "bezpečném" stavu.
        - (b) Systém se nachází v "nebezpečném" stavu.
        - (c) Systém se nachází v "bezpečném" stavu, protože jednotlivé procesy můžeme uspokojit v následujícím pořadí P4, P2, P3, P0, P1.
        - (d) Systém se nachází v "bezpečném" stavu, protože jednotlivé procesy můžeme uspokojit v následujícím pořadí P3, P2, P1, P4, P0.
        - (e) Systém se nachází v "nebezpečném" stavu, protože neexistuje posloupnost alokací prostředků chi = {chi_1, chi_2, ..., chi_j} taková, že v bodě chi_k, 1 <= k <= j budou alokovány všechny potřebné prostředky pro uspokojení procesu P4.

    2. Pro toto zadání dále vyberte pravdivá tvrzení:
        - (a) Systém se nachází v "bezpečném" stavu, přestože všechny Coffmanovy podmínky jsou splněné.
        - (b) Systém se nachází v "nebezpečném" stavu, ale porušením Coffmanových podmínek by se dalo zabránit deadlocku.
        - (c) Systém se nachází v "nebezpečném" stavu, protože aspoň jedna Coffmanova podmínka není splněna.
        - (d) Systém se nachází v "bezpečném" stavu, protože všechny Coffmanovy podmínky jsou splněné.
        - (e) Systém se nachází v "nebezpečném" stavu, protože aspoň jedna Coffmanova podmínka je splněna.

??? success "Řešení"
    **Krok 1: Sestav matici Potřebné = Požadované - Přidělené**

    ```
    Požadované        Již přidělené       Potřebné
       T0 T1 T2 T3      T0 T1 T2 T3        T0 T1 T2 T3
    P0 [ 1  6  1  5]  P0 [ 0  0  0  0]  P0 [ 1  6  1  5]
    P1 [ 1  0  0  0]  P1 [ 0  0  0  0]  P1 [ 1  0  0  0]
    P2 [ 0  5  0  2]  P2 [ 0  4  0  1]  P2 [ 0  1  0  1]
    P3 [ 1  2  0  2]  P3 [ 0  2  0  1]  P3 [ 1  0  0  1]
    P4 [ 0  5  1  5]  P4 [ 0  0  0  1]  P4 [ 0  5  1  4]
    ```

    | Proces | Potřeba T0 | Potřeba T1 | Potřeba T2 | Potřeba T3 |
    |--------|------------|------------|------------|------------|
    | P0     | 1          | 6          | 1          | 5          |
    | P1     | 1          | 0          | 0          | 0          |
    | P2     | 0          | 1          | 0          | 1          |
    | P3     | 1          | 0          | 0          | 1          |
    | P4     | 0          | 5          | 1          | 4          |

    **Krok 2: Inicializace**

    ```
    Volné = (2, 2, 2, 3)
    ```

    V tento moment můžeme uspokojit procesy P1, P2 nebo P3.

    **Krok 3: Uspokojíme P3**

    Potřeba[P3] = (1,0,0,1) <= (2,2,2,3) — ANO.

    Dostaneme zpět dva prostředky typu T1 a jeden prostředek typu T3. Zůstávají nám:

    | Typ prostředku   | T0 | T1 | T2 | T3 |
    |------------------|----|----|----|----|
    | Počet prostředků | 2  | 4  | 2  | 4  |

    **Krok 4: Uspokojíme P2**

    Potřeba[P2] = (0,1,0,1) <= (2,4,2,4) — ANO.

    Dostaneme zpět čtyři prostředky typu T1 a jeden prostředek typu T3. Zůstávají nám:

    | Typ prostředku   | T0 | T1 | T2 | T3 |
    |------------------|----|----|----|----|
    | Počet prostředků | 2  | 8  | 2  | 5  |

    **Krok 5: Uspokojíme všechny ostatní procesy**

    V tento moment můžeme uspokojit všechny ostatní procesy v libovolném pořadí.

    Například uspokojíme P1:
    - Potřeba[P1] = (1,0,0,0) <= (2,8,2,5) — ANO
    - Volné po P1: (2,8,2,5) + (0,0,0,0) = (2,8,2,5)

    Pak P4:
    - Potřeba[P4] = (0,5,1,4) <= (2,8,2,5) — ANO
    - Volné po P4: (2,8,2,5) + (0,0,0,1) = (2,8,2,6)

    Pak P0:
    - Potřeba[P0] = (1,6,1,5) <= (2,8,2,6) — ANO

    Bezpečné pořadí: **P3 -> P2 -> P1 -> P4 -> P0**

    Systém je v **bezpečném stavu**.

    **Odpovědi:**

    **Otázka 1:**
    - **(a) PRAVDA** — systém se nachází v bezpečném stavu
    - (b) NEPRAVDA — systém je v bezpečném stavu
    - (c) NEPRAVDA — pořadí P4, P2, P3, P0, P1 není bezpečné (P4 potřebuje (0,5,1,4), ale máme jen (2,2,2,3), T1: 5 > 2)
    - **(d) PRAVDA** — pořadí P3, P2, P1, P4, P0 je bezpečné (viz výše)
    - (e) NEPRAVDA — P4 lze uspokojit (po P3 a P2)

    **Otázka 2:**
    - **(a) PRAVDA** — systém je v bezpečném stavu, přestože všechny Coffmanovy podmínky jsou splněné
    - (b) NEPRAVDA — systém je v bezpečném stavu
    - (c) NEPRAVDA — systém je v bezpečném stavu
    - (d) NEPRAVDA — Coffmanovy podmínky jsou splněné, ale to není důvod bezpečnosti; bezpečnost plyne z existence bezpečné posloupnosti
    - (e) NEPRAVDA — systém je v bezpečném stavu
