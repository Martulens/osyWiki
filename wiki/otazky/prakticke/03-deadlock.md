# Deadlock

Úloha na Bankéřův algoritmus patří mezi nejjistěji se opakující typy na zkoušce BI-OSY. Dostanete tabulku s maximálními požadavky a již přidělenými prostředky, vektorem volných prostředků a vaším úkolem je rozhodnout, zda je systém v **bezpečném stavu**, a pokud ano, uvést bezpečné pořadí uspokojení vláken.

??? abstract "Obsah stránky"

    [TOC]

---

## Co tento typ úlohy prověřuje

- Zda rozumíte pojmu **bezpečný stav** a umíte ho algoritmicky ověřit.
- Zda dokážete sestavit matici **Need = Max − Allocation** a správně pracovat s vektorem **Work**.
- Zda znáte **Coffmanovy podmínky** a víte, jak se vztahují k bezpečnému stavu (a proč bezpečný stav neznamená, že podmínky nejsou splněny).
- Zda umíte číst a interpretovat **alokační graf** (cyklus = uváznutí, jen u jednoinstancových prostředků je to nutná i postačující podmínka).

---

## Co potřebuješ znát

### Coffmanovy podmínky

Aby mohlo dojít k deadlocku, musí být **všechny čtyři podmínky splněny současně**:

| Podmínka | Anglicky | Popis |
|---|---|---|
| Vzájemné vyloučení | Mutual exclusion | Prostředek je v daný okamžik přidělen nejvýše jednomu vláknu |
| Neodnímatelnost | No preemption | Přidělený prostředek nelze vláknu násilně odebrat |
| Drž a čekej | Hold and wait | Vlákno drží část prostředků a zároveň čeká na další |
| Kruhové čekání | Circular wait | Existuje cyklus vláken, kde každé čeká na prostředek držený dalším |

!!! tip "Klíčový poznatek"
    Porušení **jediné** podmínky postačuje k tomu, aby deadlock principiálně nemohl nastat. Strategie prevence (deadlock prevention) se snaží trvale porušit jednu z prvních tří podmínek — nejpraktičtější je porušení kruhového čekání vzestupným číslováním prostředků.

### Bezpečný stav

**Bezpečný stav** je takový stav systému, ze kterého existuje alespoň jedna posloupnost přidělování prostředků, která zaručí postupné uspokojení potřeb **všech** vláken bez uváznutí.

**Nebezpečný stav** neznamená okamžitý deadlock — pouze říká, že taková bezpečná posloupnost neexistuje a deadlock *může* nastat.

### Vzorce a datové struktury

```text
Need[i] = Max[i] - Allocation[i]    (pro každé vlákno i a každý typ prostředku)

Work    = Available                  (inicializace; Work se v průběhu mění)
Finish  = [false, false, ..., false] (pro každé vlákno)
```

Kde:
- **Max** — maximální počet prostředků každého typu, které vlákno může celkem potřebovat
- **Allocation** — počet prostředků každého typu aktuálně přidělených vláknu
- **Need** — kolik prostředků vlákno ještě maximálně potřebuje
- **Available** — počet volných prostředků každého typu (vstup)
- **Work** — pracovní kopie Available, která se zvětšuje po uspokojení každého vlákna

Odkaz na teorii: [Skripta: Uváznutí](../../skripta/04-deadlock.md)

---

## Postup řešení krok za krokem

Toto je **těžiště celého tématu**. Naučte se postup nazpaměť — u zkoušky ho budete provádět mechanicky krok za krokem.

### Krok 1: Zkontroluj, co je zadáno

Zadání může uvádět:
- přímo tabulku **Need** (není třeba nic počítat), nebo
- tabulky **Max** a **Allocation** zvlášť (musíš spočítat Need), nebo
- smíšenou formu (Max a Alloc v jedné tabulce — nejčastější případ).

Vždy si přečti hlavičky sloupců. Přeskočení tohoto kroku způsobuje nejčastější chyby.

### Krok 2: Sestav matici Need

Pro každé vlákno `i` a každý typ prostředku `r`:

```text
Need[i][r] = Max[i][r] - Allocation[i][r]
```

Proveď výpočet systematicky řádek po řádku. Zkontroluj, že všechny hodnoty jsou nezáporné — pokud by Need vyšlo záporné, je tabulka chybně zadána nebo špatně přečtena.

### Krok 3: Inicializuj Work a Finish

```text
Work   = Available          (zkopíruj vektor volných prostředků)
Finish = [false, ..., false] (jedno false pro každé vlákno)
```

Work si piš jako vektor v závorce, například `Work = (0, 1, 7, 0)` pro 4 typy prostředků.

### Krok 4: Hledej kandidáta — vlákno, které lze uspokojit

Projdi **všechna neuspokojená vlákna** (kde `Finish[i] = false`) a hledej takové, pro které platí:

```text
Need[i] <= Work     (porovnání po složkách — každá složka Need musí být <= odpovídající složka Work)
```

Například pro vlákno s `Need = (0, 0, 4, 0)` a `Work = (0, 1, 7, 0)`:
- složka R0: 0 <= 0 ✓
- složka R1: 0 <= 1 ✓
- složka R2: 4 <= 7 ✓
- složka R3: 0 <= 0 ✓
- Podmínka splněna — vlákno **lze uspokojit**.

Pokud žádné takové vlákno neexistuje, přejdi na Krok 6.

### Krok 5: Uspokojení vlákna — aktualizuj Work a Finish

Jakmile najdeš vlákno `i` splňující podmínku z Kroku 4:

1. Zaznamenej ho do **bezpečné posloupnosti** (přidej na konec).
2. Nastav `Finish[i] = true`.
3. Aktualizuj Work — vlákno doběhne a uvolní všechny své prostředky:

```text
Work = Work + Allocation[i]
```

4. Vrať se na **Krok 4** a hledej dalšího kandidáta.

!!! note "Proč se přidává Allocation, ne Need?"
    Vlákno, které bylo uspokojeno, nejprve dostane zbývající potřebné prostředky (Need), provede svou práci a pak **uvolní vše, co drží** — tedy celý řádek Allocation. Proto přičítáme Allocation, ne Need.

### Krok 6: Vyhodnoť výsledek

Po skončení hlavní smyčky zkontroluj pole Finish:

- **Všechna `Finish[i] = true`** → systém je v **bezpečném stavu**. Zaznamenaná posloupnost je bezpečná.
- **Aspoň jedno `Finish[i] = false`** → systém je v **nebezpečném stavu**. Vlákna s `Finish = false` jsou potenciálně uvázlá.

### Krok 7: Coffmanovy podmínky a bezpečný stav (multichoice)

Toto je **nejčastější past** v multichoice otázkách:

!!! warning "Bezpečný stav NEZNAMENÁ, že Coffmanovy podmínky nejsou splněny"
    Coffmanovy podmínky jsou **nutné** podmínky deadlocku, nikoli nutné podmínky nebezpečného stavu. V bezpečném stavu mohou být všechny čtyři podmínky splněny — bezpečnost zaručuje existence bezpečné posloupnosti, ne porušení podmínek.

    Správné tvrzení: *„Systém je v bezpečném stavu, protože existuje bezpečná posloupnost T1, T3, T0..."*
    Špatné tvrzení: *„Systém je v bezpečném stavu, protože aspoň jedna Coffmanova podmínka není splněna."*

### Krok 8: Alokační graf

Alokační graf je orientovaný graf se dvěma typy uzlů:
- **Obdélník** = prostředek (tečky uvnitř = instance)
- **Kružnice** = vlákno

Hrany:
- prostředek → vlákno: vlákno **drží** prostředek
- vlákno → prostředek: vlákno **čeká** na prostředek

**Cyklus v grafu = deadlock** — ale pozor:
- U prostředků s **jednou instancí**: cyklus je nutná i **postačující** podmínka deadlocku.
- U prostředků s **více instancemi**: cyklus je nutná, ale **ne postačující** podmínka — musíš použít Bankéřův algoritmus.

### Krok 9: Ověření konkrétního pořadí (typická multichoice otázka)

Zadání může nabídnout několik pořadí a ptát se, která jsou bezpečná. Pro každé nabídnuté pořadí:

1. Nastav `Work = Available`.
2. Procházej vlákna v daném pořadí.
3. Pro každé vlákno ověř, zda `Need[i] <= Work`.
4. Pokud ano: `Work += Allocation[i]`, pokračuj.
5. Pokud ne: **toto pořadí není bezpečné** (i když systém může být v bezpečném stavu — jen tímto pořadím nelze projít).

### Krok 10: Tipuješ-li pořadí, začni od vláken s nejmenším Need

Pokud hledáš bezpečnou posloupnost od nuly, pomůže tato heuristika:
- Seřaď vlákna podle součtu Need (vzestupně).
- Zkus začít od vlákna, jehož Need je po složkách nejmenší — to je nejlepší kandidát na první v pořadí.
- Neexistuje ale zaručeně jedno bezpečné pořadí — jich může být více; hledej libovolné.

---

## Vzorové zadání

!!! example "Zadání"
    V systému jsou 4 typy prostředků R0–R3 a 5 vláken T0–T4. Jsou zadány celkové požadavky (Max) a již přidělené prostředky (Allocation):

    | Vlákno | Max R0 | Max R1 | Max R2 | Max R3 | Alloc R0 | Alloc R1 | Alloc R2 | Alloc R3 |
    |---|---|---|---|---|---|---|---|---|
    | T0 | 1 | 2 | 6 | 5 | 0 | 1 | 0 | 1 |
    | T1 | 1 | 0 | 6 | 6 | 1 | 0 | 2 | 6 |
    | T2 | 2 | 2 | 4 | 5 | 2 | 1 | 1 | 2 |
    | T3 | 0 | 1 | 8 | 0 | 0 | 0 | 0 | 0 |
    | T4 | 2 | 1 | 0 | 5 | 0 | 0 | 0 | 1 |

    Volné prostředky (Available): R0=0, R1=1, R2=7, R3=0.

    **Otázky:**

    1. Je systém v bezpečném stavu? Pokud ano, uveďte bezpečné pořadí uspokojení.
    2. Vyberte pravdivá tvrzení:
        - (a) Systém je v bezpečném stavu, protože aspoň jedna Coffmanova podmínka není splněna.
        - (b) Systém je v bezpečném stavu, protože existuje bezpečná posloupnost.
        - (c) Systém je v nebezpečném stavu, protože v alokačním grafu existuje cyklus.
        - (d) Systém je v bezpečném stavu, protože v alokačním grafu závislostí není cyklus.

    *Tento typ zadání se opakuje prakticky v každém termínu: 2011, 2014, 2015, 2018, 2023, 2025.*

---

## Řešení vzorového zadání

??? success "Ukázat řešení"

    ### Krok 1: Sestav matici Need = Max - Allocation

    | Vlákno | Need R0 | Need R1 | Need R2 | Need R3 |
    |---|---|---|---|---|
    | T0 | 1-0=**1** | 2-1=**1** | 6-0=**6** | 5-1=**4** |
    | T1 | 1-1=**0** | 0-0=**0** | 6-2=**4** | 6-6=**0** |
    | T2 | 2-2=**0** | 2-1=**1** | 4-1=**3** | 5-2=**3** |
    | T3 | 0-0=**0** | 1-0=**1** | 8-0=**8** | 0-0=**0** |
    | T4 | 2-0=**2** | 1-0=**1** | 0-0=**0** | 5-1=**4** |

    Přehledná tabulka Need:

    | Vlákno | Need R0 | Need R1 | Need R2 | Need R3 |
    |---|---|---|---|---|
    | T0 | 1 | 1 | 6 | 4 |
    | T1 | 0 | 0 | 4 | 0 |
    | T2 | 0 | 1 | 3 | 3 |
    | T3 | 0 | 1 | 8 | 0 |
    | T4 | 2 | 1 | 0 | 4 |

    ### Krok 2: Inicializace

    ```text
    Work   = Available = (0, 1, 7, 0)
    Finish = [false, false, false, false, false]
    Bezpecna posloupnost = []
    ```

    ### Krok 3: První průchod — hledáme vlákno s Need <= Work

    `Work = (0, 1, 7, 0)` — projdeme všechna vlákna:

    | Vlákno | Need | Work | Need <= Work? |
    |---|---|---|---|
    | T0 | (1,1,6,4) | (0,1,7,0) | R0: 1<=0? **NE** — nevyhovuje |
    | T1 | (0,0,4,0) | (0,1,7,0) | 0<=0, 0<=1, 4<=7, 0<=0 — **ANO** |
    | T2 | (0,1,3,3) | (0,1,7,0) | 0<=0, 1<=1, 3<=7, 3<=0? **NE** |
    | T3 | (0,1,8,0) | (0,1,7,0) | 0<=0, 1<=1, 8<=7? **NE** |
    | T4 | (2,1,0,4) | (0,1,7,0) | 2<=0? **NE** |

    **T1 vyhovuje.** Uspokojíme T1:

    ```text
    Finish[T1] = true
    Work = Work + Allocation[T1] = (0,1,7,0) + (1,0,2,6) = (1, 1, 9, 6)
    Bezpecna posloupnost = [T1]
    ```

    ### Krok 4: Druhý průchod — Work = (1, 1, 9, 6)

    | Vlákno | Need | Work | Need <= Work? |
    |---|---|---|---|
    | T0 | (1,1,6,4) | (1,1,9,6) | 1<=1, 1<=1, 6<=9, 4<=6 — **ANO** |
    | T2 | (0,1,3,3) | (1,1,9,6) | 0<=1, 1<=1, 3<=9, 3<=6 — **ANO** |
    | T3 | (0,1,8,0) | (1,1,9,6) | 0<=1, 1<=1, 8<=9, 0<=6 — **ANO** |
    | T4 | (2,1,0,4) | (1,1,9,6) | 2<=1? **NE** |

    Více vláken vyhovuje — zvolíme první, které splní podmínku (nebo libovolné). Zvolíme **T0**:

    ```text
    Finish[T0] = true
    Work = (1,1,9,6) + Allocation[T0] = (1,1,9,6) + (0,1,0,1) = (1, 2, 9, 7)
    Bezpecna posloupnost = [T1, T0]
    ```

    ### Krok 5: Třetí průchod — Work = (1, 2, 9, 7)

    Zbývají: T2, T3, T4.

    | Vlákno | Need | Work | Need <= Work? |
    |---|---|---|---|
    | T2 | (0,1,3,3) | (1,2,9,7) | 0<=1, 1<=2, 3<=9, 3<=7 — **ANO** |
    | T3 | (0,1,8,0) | (1,2,9,7) | 0<=1, 1<=2, 8<=9, 0<=7 — **ANO** |
    | T4 | (2,1,0,4) | (1,2,9,7) | 2<=1? **NE** |

    Zvolíme **T3** (má nulovou alokaci — uvolní nakonec to, co drží, což je nic; ale postup je správný):

    ```text
    Finish[T3] = true
    Work = (1,2,9,7) + Allocation[T3] = (1,2,9,7) + (0,0,0,0) = (1, 2, 9, 7)
    Bezpecna posloupnost = [T1, T0, T3]
    ```

    ### Krok 6: Čtvrtý průchod — Work = (1, 2, 9, 7)

    Zbývají: T2, T4.

    | Vlákno | Need | Work | Need <= Work? |
    |---|---|---|---|
    | T2 | (0,1,3,3) | (1,2,9,7) | **ANO** |
    | T4 | (2,1,0,4) | (1,2,9,7) | 2<=1? **NE** |

    Uspokojíme **T2**:

    ```text
    Finish[T2] = true
    Work = (1,2,9,7) + Allocation[T2] = (1,2,9,7) + (2,1,1,2) = (3, 3, 10, 9)
    Bezpecna posloupnost = [T1, T0, T3, T2]
    ```

    ### Krok 7: Pátý průchod — Work = (3, 3, 10, 9)

    Zbývá: T4.

    | Vlákno | Need | Work | Need <= Work? |
    |---|---|---|---|
    | T4 | (2,1,0,4) | (3,3,10,9) | 2<=3, 1<=3, 0<=10, 4<=9 — **ANO** |

    ```text
    Finish[T4] = true
    Work = (3,3,10,9) + Allocation[T4] = (3,3,10,9) + (0,0,0,1) = (3, 3, 10, 10)
    Bezpecna posloupnost = [T1, T0, T3, T2, T4]
    ```

    ### Výsledek

    Všechna `Finish[i] = true`. **Systém je v bezpečném stavu.**

    Bezpečné pořadí: **T1 → T0 → T3 → T2 → T4**

    (Také platné: T1 → T0 → T2 → T3 → T4 a další variace — bezpečných pořadí bývá více.)

    ### Odpovědi na multichoice otázky

    - **(a) „Bezpečný stav, protože aspoň jedna Coffmanova podmínka není splněna."** — **NEPRAVDA.** Všechny čtyři Coffmanovy podmínky mohou být splněny i v bezpečném stavu. Bezpečnost zaručuje existence bezpečné posloupnosti, ne porušení podmínek.
    - **(b) „Bezpečný stav, protože existuje bezpečná posloupnost."** — **PRAVDA.** Toto je přesná definice bezpečného stavu.
    - **(c) „Nebezpečný stav, protože v alokačním grafu existuje cyklus."** — **NEPRAVDA.** Systém je v bezpečném stavu; navíc u prostředků s více instancemi samotný cyklus nestačí k potvrzení deadlocku.
    - **(d) „Bezpečný stav, protože v alokačním grafu není cyklus."** — u jednoinstancových prostředků by to bylo dostatečné odůvodnění; u víceinstancových prostředků (jako zde) je správnější odůvodnění přes existenci bezpečné posloupnosti.

    !!! warning "Častá chyba v odůvodnění"
        U **víceinstancových** prostředků (jako v tomto zadání) absence cyklu
        v alokačním grafu **nestačí** k prokázání bezpečnosti — a naopak přítomnost
        cyklu nemusí znamenat deadlock. Cyklus v grafu je nutnou podmínkou deadlocku
        jen u **jednoinstancových** prostředků. U víceinstancových prostředků vždy
        odůvodňuj bezpečnost přes existenci bezpečné posloupnosti (Bankéřův algoritmus).

---

## Další procvičení

### Varianta A — systém se 3 prostředky

!!! example "Zadání A"
    Systém: vlákna T1–T4, prostředky R1–R3. Matice Max a Allocation:

    | Vlákno | Max R1 | Max R2 | Max R3 | Alloc R1 | Alloc R2 | Alloc R3 |
    |---|---|---|---|---|---|---|
    | T1 | 3 | 2 | 6 | 1 | 0 | 0 |
    | T2 | 6 | 1 | 3 | 6 | 1 | 2 |
    | T3 | 3 | 1 | 4 | 2 | 1 | 1 |
    | T4 | 4 | 2 | 2 | 0 | 0 | 2 |

    Existující prostředky: E = (9, 3, 6). Volné: F = (0, 1, 1).

    Je systém v bezpečném stavu? Uveďte bezpečné pořadí.

??? success "Ukázat řešení A"
    **Need = Max - Allocation:**

    | Vlákno | Need R1 | Need R2 | Need R3 |
    |---|---|---|---|
    | T1 | 2 | 2 | 6 |
    | T2 | 0 | 0 | 1 |
    | T3 | 1 | 0 | 3 |
    | T4 | 4 | 2 | 0 |

    **Work = (0, 1, 1)**

    **Průchod 1:** Hledáme Need <= (0,1,1):
    - T1: (2,2,6) — R1: 2<=0? NE
    - T2: (0,0,1) — 0<=0, 0<=1, 1<=1 — **ANO**

    Work += Alloc[T2] = (0,1,1) + (6,1,2) = **(6, 2, 3)** | Posloupnost: [T2]

    **Průchod 2:** Work = (6,2,3):
    - T1: (2,2,6) — 2<=6, 2<=2, 6<=3? NE
    - T3: (1,0,3) — 1<=6, 0<=2, 3<=3 — **ANO**

    Work += (2,1,1) = **(8, 3, 4)** | Posloupnost: [T2, T3]

    **Průchod 3:** Work = (8,3,4):
    - T4: (4,2,0) — 4<=8, 2<=3, 0<=4 — **ANO**

    Work += (0,0,2) = **(8, 3, 6)** | Posloupnost: [T2, T3, T4]

    **Průchod 4:** Work = (8,3,6):
    - T1: (2,2,6) — 2<=8, 2<=3, 6<=6 — **ANO**

    Posloupnost: **[T2, T3, T4, T1]**

    Všichni Finish = true. **Systém je v bezpečném stavu.** Bezpečné pořadí: **T2 → T3 → T4 → T1**.

---

### Varianta B — nebezpečný stav

!!! example "Zadání B"
    Systém: vlákna T0–T4, prostředky R0–R3. Matice Need (přímo zadána):

    | Vlákno | Need R0 | Need R1 | Need R2 | Need R3 | Alloc R0 | Alloc R1 | Alloc R2 | Alloc R3 |
    |---|---|---|---|---|---|---|---|---|
    | T0 | 6 | 2 | 2 | 4 | 1 | 0 | 0 | 0 |
    | T1 | 4 | 2 | 0 | 2 | 1 | 0 | 0 | 2 |
    | T2 | 0 | 2 | 2 | 1 | 0 | 0 | 0 | 0 |
    | T3 | 5 | 2 | 0 | 5 | 1 | 1 | 0 | 0 |
    | T4 | 2 | 1 | 4 | 0 | 0 | 0 | 3 | 0 |

    Volné: R0=5, R1=4, R2=2, R3=4.

    Je systém v bezpečném stavu? Ověřte pořadí T1, T2, T0, T4, T3.

??? success "Ukázat řešení B"
    **Work = (5, 4, 2, 4)**

    **Průchod 1:**
    - T0: Need (6,2,2,4) — 6<=5? NE
    - T1: Need (4,2,0,2) — 4<=5, 2<=4, 0<=2, 2<=4 — **ANO**

    Work += (1,0,0,2) = **(6, 4, 2, 6)** | Posloupnost: [T1]

    **Průchod 2:** Work = (6,4,2,6):
    - T0: (6,2,2,4) — 6<=6, 2<=4, 2<=2, 4<=6 — **ANO**

    Work += (1,0,0,0) = **(7, 4, 2, 6)** | Posloupnost: [T1, T0]

    **Průchod 3:** Work = (7,4,2,6):
    - T2: (0,2,2,1) — **ANO**

    Work += (0,0,0,0) = **(7, 4, 2, 6)** | Posloupnost: [T1, T0, T2]

    **Průchod 4:** Work = (7,4,2,6):
    - T3: (5,2,0,5) — 5<=7, 2<=4, 0<=2, 5<=6 — **ANO**

    Work += (1,1,0,0) = **(8, 5, 2, 6)** | Posloupnost: [T1, T0, T2, T3]

    **Průchod 5:** Work = (8,5,2,6):
    - T4: (2,1,4,0) — 2<=8, 1<=5, 4<=2? NE

    Konec smyčky — T4 zůstává s `Finish = false`.

    **Systém je v nebezpečném stavu.** T4 nemůže být uspokojeno.

    **Ověření pořadí T1, T2, T0, T4, T3:** Totéž by selhalo na T4 — pořadí T1, T2, T0, T4, T3 **není bezpečné**.

    Poznámka: existuje jiné pořadí T1, T0, T2, T3, kde T4 stále selže — žádné bezpečné pořadí zahrnující T4 neexistuje. Systém je v nebezpečném stavu.

---

## Varianty a chytáky

- **Need zadáno přímo vs. Max+Allocation zvlášť** — přečti hlavičky tabulky. Záměna způsobí špatnou matici Need a celý výsledek bude chybný.
- **Několik bezpečných pořadí** — stačí najít jedno. Algoritmus přijme libovolné vlákno splňující `Need <= Work`, takže pořadí nemusí být jednoznačné.
- **Nebezpečný stav ≠ okamžitý deadlock** — v nebezpečném stavu deadlock *může* nastat (záleží na dalším průběhu přidělování); neznamená, že *musí* nastat.
- **T3 s nulovou alokací** (jako ve vzorovém zadání) — uspokojení T3 nic nepřidá do Work, ale Finish[T3] se nastaví na true. To je v pořádku — vlákno, které nic nedrží, může být vždy uspokojeno hned, jakmile jeho Need <= Work.
- **Multichoice: ověření nabídnutého pořadí** — proveď Bankéřův algoritmus s daným pořadím krok za krokem. Pokud v libovolném kroku `Need[i] > Work`, pořadí je špatné. Neplést si „pořadí není bezpečné" s „systém je v nebezpečném stavu".
- **Cyklus v alokačním grafu** — u víceinstancových prostředků samo o sobě nic neprokáže. Odpovědi tvrdící „cyklus → deadlock" jsou u víceinstancových prostředků nepravdivé.
- **„Porušení Coffmanových podmínek by zabránilo deadlocku"** — technicky pravda jako obecné tvrzení, ale **nesouvisí s bezpečností konkrétního stavu**. Tvrzení „systém je v nebezpečném stavu, ale porušením Coffmanových podmínek by se dalo zabránit deadlocku" je zavádějící — prevence porušením podmínek je statická designová technika, ne vlastnost konkrétního stavu.

---

## Časté chyby

1. **Záměna Need a Max** — do podmínky `Need[i] <= Work` dosazuji Max místo Need. Zkontroluj výpočet Need = Max - Allocation.
2. **Záměna Allocation a Need při aktualizaci Work** — po uspokojení vlákna přičítám Need místo Allocation. Správně: `Work += Allocation[i]`.
3. **Porovnávání vektoru špatně** — stačí jediná složka, kde `Need > Work`, a vlákno nevyhovuje. Porovnání musí platit **po každé složce** zvlášť.
4. **Předpoklad, že bezpečné pořadí je jediné** — bezpečných pořadí může být více; zadání chce jedno libovolné.
5. **Tvrzení „bezpečný stav = Coffmanovy podmínky nejsou splněny"** — typická past v multichoice; viz Krok 7.
6. **Zapomenutí na vlákno s nulovou alokací** — vlákno, které nic nedrží, je validní kandidát a jeho „uspokojení" Work nezmění; ale musíš ho přesto zahrnout do průchodu.
7. **Počítání „celkových" místo „zbývajících" potřeb** — Need je to, co vlákno ještě potřebuje, ne celkové Max.

---

## Související

- [Skripta: Uváznutí (deadlock)](../../skripta/04-deadlock.md) — teorie Coffmanových podmínek, alokační graf, strategie prevence a Bankéřův algoritmus s formálním popisem
- [Teoretické otázky (True/False)](../teorie-truefalse.md) — procvičení tvrzení o bezpečném stavu, Coffmanových podmínkách a alokačním grafu
