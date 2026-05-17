# Plánování vláken

??? abstract "Obsah stránky"

    [TOC]

---

Předpokládáme následující systém (platí pro všechny úlohy, pokud není uvedeno jinak):

- Procesor(y): 1 × Intel® Core^TM^ i5-3330 (počet jader na procesor: 4)
- Počet vláken na jádro: 1 (tedy celkem vláken na procesor: 4)
- Architektura: SMP/UMA (desktop)

Na systému je nainstalovaný 64-bitový operační systém, který používá pro plánování uživatelských procesů **statickou prioritu** (vyšší hodnota znamená vyšší prioritu). Jádro/procesor se přiděluje jednotlivým vláknům maximálně na dobu 10 ms a režii přepínání kontextu zanedbáváme.

Dále předpokládáme:

- plánovač se snaží prodloužit životnost CPU tím, že udržuje rovnoměrnou teplotu všech jader, tedy výpočetní zátěž rovnoměrně rozkládá na jednotlivé jádra
- u každého procesu je uvedena statická priorita, počet vláken, která provádějí výpočet, a **celková doba výpočtu (doba výpočtu procesu, pokud by běžel sekvenčně na jednom nezatíženém jádru)**. Pokud je výpočet v procesu realizován pomocí více vláken na dostatečném počtu jader, pak předpokládáme lineární zrychlení výpočtu, a režii na vytváření a synchronizaci vláken zanedbáváme.

---

## Úloha 1 — 4 jádra, background load 20 %, 6 procesů

!!! example "Zadání"

    Předpokládáme systém:

    - Procesor(y): 1 × Intel® Core^TM^ i5-3330 (počet jader na procesor: 4)
    - Počet vláken na jádro: 1 (tedy celkem vláken na procesor: 4)
    - Architektura: SMP/UMA (desktop)
    - Paměť: 4 GiB DDR3

    Na systému je nainstalovaný 64-bitový operační systém, který používá pro plánování uživatelských procesů statickou prioritu (vyšší hodnota znamená vyšší prioritu). Jádro/procesor se přiděluje jednotlivým vláknům maximálně na dobu 10 ms a režii přepínání kontextu zanedbáváme. Dále předpokládáme:

    - **jádro a ostatní procesy (kromě P0,...,P5) zatěžují procesor z 20 %**
    - plánovač se snaží prodloužit životnost CPU tím, že udržuje rovnoměrnou teplotu všech jader, tedy výpočetní zátěž rovnoměrně rozkládá na jednotlivé jádra
    - pro každého běžného uživatele je nastaven limit, který dovolí uživateli spustit maximálně 704 vláken, po dosažení limitu budou funkce vytvářející nová vlákna vracet chybu
    - všichni běžní uživatelé z následující tabulky spustí své procesy v čase T0
    - u každého procesu je uvedena statická priorita, počet vláken, která provádějí výpočet, a celková doba výpočtu (doba výpočtu procesu, pokud by běžel sekvenčně na jednom nezatíženém jádru). Pokud je výpočet v procesu realizován pomocí více vláken na dostatečném počtu jader, pak předpokládáme lineární zrychlení výpočtu, a režii na vytváření a synchronizaci vláken zanedbáváme.

    | Uživatel | Proces | Priorita | Počet vláken | Celková doba výpočtu [sec] |
    | -------- | ------ | -------- | ------------ | -------------------------- |
    | xvagner  | P0     | 48       | 3            | 162                        |
    | zdarekj  | P1     | 13       | 2            | 180                        |
    | trdlicka | P2     | 13       | 2            | 72                         |
    | trdlicka | P3     | 48       | 4            | 72                         |
    | xvagner  | P4     | 13       | 3            | 135                        |
    | soch     | P5     | 13       | 2            | 72                         |

    1. Za kolik sekund po T0 se ukončí proces P2? (Výsledek zadejte i s desetinnou částí, je tolerovaná malá odchylka.)
    2. Za kolik sekund po T0 se fakticky začne zpracovávat proces P2? (Výsledek zadejte i s desetinnou částí, je tolerovaná malá odchylka.)
    3. Za kolik sekund po T0 se ukončí poslední proces? (Výsledek zadejte i s desetinnou částí, je tolerovaná malá odchylka.)

??? success "Řešení"

    ### Úprava dob výpočtu (background load 20 %)

    Využíváme jenom 80 % (resp. 4/5) procesoru. Všechny hodnoty v posledním sloupci vynásobíme 5/4 (převrácenou hodnotou). Dále ve výpočtu budeme používat tyto hodnoty:

    | Proces | Celková doba výpočtu [sec] |
    | ------ | -------------------------- |
    | P0     | 202,5                      |
    | P1     | 225                        |
    | P2     | 90                         |
    | P3     | 90                         |
    | P4     | 168,75                     |
    | P5     | 90                         |

    ### Fáze 1

    P3 se bude střídat s P0, mají stejnou prioritu.
    Jako první doběhne P3 po (90/4) * (7/4) = 39.375 s.

    ```
    Výpočet běží na 4 vláknech, za 39.375 s reálného času paralelně vlákna
    udělala práci za 4 * 39.375 = 157.5 s.
    P0 tedy stihlo zpracovat 157.5 - 90 = 67.5 s.
    P0 tak zbývá 202.5 - 67.5 = 135 s.
    ```

    > P3 doběhne v čase **T0 + 39.375 s**.

    ### Fáze 2

    P0 si sebere tři jádra pro sebe, má největší prioritu. Ostatní nedokončené procesy se budou dělit o jedno zbývající jádro, mají stejnou prioritu.

    P0 doběhne po 135/3 = 45 s.
    Nacházíme se v čase 39.375 + 45 = 84.375 s.

    Na čtvrtém jádře se střídalo 9 vláken, každé běželo 45/9 = 5 s.

    - P1 stihlo vykonat 2 * 5 = 10 s, zůstává 215 s
    - P2 stihlo vykonat 2 * 5 = 10 s, zůstává 80 s
    - P4 stihlo vykonat 3 * 5 = 15 s, zůstává 153.75 s
    - P5 stihlo vykonat 2 * 5 = 10 s, zůstává 80 s

    > P0 doběhne v čase **T0 + 84.375 s**.

    > **Odpověď na otázku 2:** P2 fakticky začne zpracovávat v čase **T0 + 39.375 s** (kdy se uvolní jádra po P3 a P2 dostane přístup k výkonu).

    ### Fáze 3

    Všechny procesy P1, P2, P4, P5 mají stejnou prioritu, budou se střídat na 4 jádrech.

    P2 i P5 zbývá 80 s, doběhnou jako první po (80 * 2) / 4 = 90 s.

    Nacházíme se v čase 39.375 + 45 + 90 = 174.375 s.

    Na těchto 4 jádrech za 90 s proběhlo 360 s výpočetního času.

    ```
    P4 za tu dobu uběhlo 360 * (3/9) = 120 s. Zbývá mu 153.75 - 120 = 33.75 s.
    P1 za tu dobu uběhlo 360 * (2/9) = 80 s. Zbývá mu 215 - 80 = 135 s.
    ```

    > P2 a P5 doběhnou v čase **T0 + 174.375 s**.

    > **Odpověď na otázku 1:** Proces P2 se ukončí v čase **T0 + 174.375 s**.

    ### Fáze 4

    P1, P4 se budou střídat na všech jádrech.

    Jako první doběhne P4 po (33.75 * 5) / 4 = 14.0625 s.

    Nacházíme se v čase 39.375 + 45 + 90 + 14.0625 = 188.4375 s.

    Na 4 jádrech za tu dobu proběhlo 4 * 14.0625 = 56.25 s výpočetního času.

    ```
    P1 stihlo vykonat 56.25 * (2/5) = 22.5 s, zůstává 135 - 22.5 = 112.5 s
    ```

    > P4 doběhne v čase **T0 + 188.4375 s**.

    ### Fáze 5

    P1 poběží na dvou jádrech, doběhne po 112.5 / 2 = 56.25 s.

    Nacházíme se v čase 39.375 + 45 + 90 + 14.0625 + 56.25 = 244.6575 s.

    > P1 doběhne v čase **T0 + 244.6575 s**.

    ### Shrnutí odpovědí

    | Otázka | Odpověď |
    | ------ | ------- |
    | 1. Za kolik sekund po T0 se ukončí P2? | **174.375 s** |
    | 2. Za kolik sekund po T0 se fakticky začne zpracovávat P2? | **39.375 s** |
    | 3. Za kolik sekund po T0 se ukončí poslední proces? | **244.6575 s** |

---

## Úloha 2 — 4 jádra, background load 75 %, 6 procesů

!!! example "Zadání"

    Předpokládáme systém:

    - Procesor(y): 1 × Intel® Core^TM^ i5-3330 (počet jader na procesor: 4)
    - Počet vláken na jádro: 1 (tedy celkem vláken na procesor: 4)
    - Architektura: SMP/UMA (desktop)
    - Paměť: 8 GiB DDR3

    Na systému je nainstalovaný 64-bitový operační systém, který používá pro plánování uživatelských procesů statickou prioritu (vyšší hodnota znamená vyšší prioritu). Jádro/procesor se přiděluje jednotlivým vláknům maximálně na dobu 10 ms a režii přepínání kontextu zanedbáváme. Dále předpokládáme:

    - **jádro a ostatní procesy (kromě P0,...,P5) zatěžují procesor z 75 %**
    - plánovač se snaží prodloužit životnost CPU tím, že udržuje rovnoměrnou teplotu všech jader, tedy výpočetní zátěž rovnoměrně rozkládá na jednotlivé jádra
    - pro každého běžného uživatele je nastaven limit, který dovolí uživateli spustit maximálně 512 vláken, po dosažení limitu budou funkce vytvářející nová vlákna vracet chybu
    - všichni běžní uživatelé z následující tabulky spustí své procesy v čase T0
    - u každého procesu je uvedena statická priorita, počet vláken, která provádějí výpočet, a celková doba výpočtu (doba výpočtu procesu, pokud by běžel sekvenčně na jednom nezatíženém jádru). Pokud je výpočet v procesu realizován pomocí více vláken na dostatečném počtu jader, pak předpokládáme lineární zrychlení výpočtu, a režii na vytváření a synchronizaci vláken zanedbáváme.

    | Uživatel | Proces | Priorita | Počet vláken | Celková doba výpočtu [sec] |
    | -------- | ------ | -------- | ------------ | -------------------------- |
    | xvagner  | P0     | 69       | 3            | 216                        |
    | trdlicka | P1     | 33       | 2            | 108                        |
    | soch     | P2     | 84       | 2            | 90                         |
    | trdlicka | P3     | 17       | 1            | 63                         |
    | zdarekj  | P4     | 69       | 1            | 72                         |
    | soch     | P5     | 33       | 3            | 135                        |

    1. Za kolik sekund po T0 se ukončí proces P4? (Výsledek zadejte i s desetinnou částí, je tolerovaná malá odchylka.)
    2. Za kolik sekund po T0 se fakticky začne zpracovávat proces P5? (Výsledek zadejte i s desetinnou částí, je tolerovaná malá odchylka.)
    3. Za kolik sekund po T0 se ukončí poslední proces? (Výsledek zadejte i s desetinnou částí, je tolerovaná malá odchylka.)

??? success "Řešení"

    ### Úprava dob výpočtu (background load 75 %)

    Využíváme jenom 25 % (resp. 1/4) procesoru. Všechny hodnoty v posledním sloupci vynásobíme 4/1 = 4 (převrácenou hodnotou). Dále ve výpočtu budeme používat tyto hodnoty:

    | Proces | Celková doba výpočtu [sec] |
    | ------ | -------------------------- |
    | P0     | 864                        |
    | P1     | 432                        |
    | P2     | 360                        |
    | P3     | 252                        |
    | P4     | 288                        |
    | P5     | 540                        |

    ### Fáze 1

    P2 poběží na 2 jádrech, na zbývajících dvou se budou střídat procesy P0, P4.

    Jako první doběhne P2 po 360/2 = 180 s.

    Dohromady se spočítalo 180 * 2 = 360 s výpočetního času na zbývajících dvou jádrech s procesy P0, P4.

    ```
    Z toho P0 stihlo s třemi vlákny vykonat (3/4) * 360 = 270 s, zůstává mu
    tak 864 - 270 = 594 s.
    Z toho P4 stihlo s jedním vláknem vykonat (1/4) * 360 = 90 s, zůstává
    mu tak 288 - 90 = 198 s.
    ```

    > P2 doběhne v čase **T0 + 180 s**.

    ### Fáze 2

    P0, P4 se budou střídat na všech jádrech, obě doběhnou po 198 s.

    Nacházíme se v čase 180 + 198 = 378 s.

    > P0 a P4 doběhnou v čase **T0 + 378 s**.

    > **Odpověď na otázku 1:** Proces P4 se ukončí v čase **T0 + 378 s**.

    > **Odpověď na otázku 2:** Proces P5 fakticky začne zpracovávat v čase **T0 + 378 s** (kdy se uvolní jádra po P0 a P4 a P5 dostane přístup k výkonu).

    ### Fáze 3

    P1, P5 se budou střídat na všech jádrech.

    Jako první doběhne P5 po (540 * 5) / 4 = 225 s.

    Nacházíme se v čase 180 + 198 + 225 = 603 s.

    ```
    P1 stihlo na dvou vláknech z pěti vykonat 225 * 4 * (2/5) = 360 s, zůstává 72 s.
    ```

    > P5 doběhne v čase **T0 + 603 s**.

    ### Fáze 4

    P1, P3 se budou střídat na 3 jádrech.

    P1 doběhne po 36 s, P3 doběhne po 252 s.

    Nacházíme se v čase 180 + 198 + 225 + 252 = 855 s.

    > P1 doběhne v čase **T0 + 639 s** (603 + 36).
    > P3 doběhne v čase **T0 + 855 s** jako poslední.

    ### Shrnutí odpovědí

    | Otázka | Odpověď |
    | ------ | ------- |
    | 1. Za kolik sekund po T0 se ukončí P4? | **378 s** |
    | 2. Za kolik sekund po T0 se fakticky začne zpracovávat P5? | **378 s** |
    | 3. Za kolik sekund po T0 se ukončí poslední proces? | **855 s** |

---

## Úloha 3 — 4 jádra, bez background load, 6 procesů

!!! example "Zadání"

    Předpokládáme systém:

    - Procesor(y): 1 × Intel® Core^TM^ i5-3330 (počet jader na procesor: 4)
    - Počet vláken na jádro: 1 (tedy celkem vláken na procesor: 4)
    - Architektura: SMP/UMA (desktop)
    - Paměť: 4 GiB DDR3

    Na systému je nainstalovaný 32-bitový operační systém, který používá pro plánování uživatelských procesů statickou prioritu (vyšší hodnota znamená vyšší prioritu). Jádro/procesor se přiděluje jednotlivým vláknům maximálně na dobu 50 ms a režii přepínání kontextu zanedbáváme. Dále předpokládáme:

    - **jádro a ostatní procesy (kromě P0,...,P5) procesor nezatěžují**
    - plánovač se snaží prodloužit životnost CPU tím, že udržuje rovnoměrnou teplotu všech jader, tedy výpočetní zátěž rovnoměrně rozkládá na jednotlivé jádra
    - pro každého běžného uživatele je nastaven limit, který dovolí uživateli spustit maximálně 384 vláken, po dosažení limitu budou funkce vytvářející nová vlákna vracet chybu
    - všichni běžní uživatelé z následující tabulky spustí své procesy v čase T0
    - u každého procesu je uvedena statická priorita, počet vláken, která provádějí výpočet, a celková doba výpočtu (doba výpočtu procesu, pokud by běžel sekvenčně na jednom nezatíženém jádru). Pokud je výpočet v procesu realizován pomocí více vláken na dostatečném počtu jader, pak předpokládáme lineární zrychlení výpočtu, a režii na vytváření a synchronizaci vláken zanedbáváme.

    | Uživatel | Proces | Priorita | Počet vláken | Celková doba výpočtu [sec] |
    | -------- | ------ | -------- | ------------ | -------------------------- |
    | zahradn  | P0     | 33       | 4            | 360                        |
    | trdlicka | P1     | 58       | 1            | 54                         |
    | zahradn  | P2     | 22       | 1            | 27                         |
    | zahradn  | P3     | 22       | 1            | 54                         |
    | zdarekj  | P4     | 22       | 2            | 36                         |
    | xvagner  | P5     | 22       | 4            | 72                         |

    1. Za kolik sekund po T0 se ukončí proces P0? (Výsledek zadejte i s desetinnou částí, je tolerovaná malá odchylka.)
    2. Za kolik sekund po T0 se fakticky začne zpracovávat proces P4? (Výsledek zadejte i s desetinnou částí, je tolerovaná malá odchylka.)
    3. Za kolik sekund po T0 se ukončí poslední proces? (Výsledek zadejte i s desetinnou částí, je tolerovaná malá odchylka.)

??? success "Řešení"

    Bez background load — doby výpočtu se nijak neupravují.

    ### Fáze 1

    P1 poběží na 1 jádru, na zbývajících třech bude běžet P0.

    Jako první doběhne P1 po 54 s.

    Na zbývajících třech jádrech se střídala 4 vlákna P0, celkem vykonala 54 * 3 = 162 s výpočetního času.

    ```
    P0 tak zbývá 360 - 162 = 198 s.
    ```

    > P1 doběhne v čase **T0 + 54 s**.

    ### Fáze 2

    P0 poběží na všech jádrech, doběhne po 198/4 = 49.5 s.

    Nacházíme se v čase 54 + 49.5 = 103.5 s.

    > P0 doběhne v čase **T0 + 103.5 s**.

    > **Odpověď na otázku 1:** Proces P0 se ukončí v čase **T0 + 103.5 s**.

    > **Odpověď na otázku 2:** Proces P4 fakticky začne zpracovávat v čase **T0 + 103.5 s** (kdy se uvolní jádra po P0 a procesy P2, P3, P4, P5 s nižší prioritou dostanou přístup k výkonu).

    ### Fáze 3

    Všechny procesy P2, P3, P4, P5 mají stejnou prioritu, budou se střídat na 4 jádrech.

    P4, P5 doběhnou jako první po 36 s.

    Na 4 jádrech za tu dobu proběhlo 4 * 36 = 144 s výpočetního času.

    ```
    P2 zůstává 9 s, P3 zůstává 36 s.
    ```

    Nacházíme se v čase 54 + 49.5 + 36 = 139.5 s.

    > P4 a P5 doběhnou v čase **T0 + 139.5 s**.

    ### Fáze 4

    P2 doběhne po 9 s, P3 doběhne po 36 s.

    Nacházíme se v čase 54 + 49.5 + 36 + 36 = 175.5 s.

    > P2 doběhne v čase **T0 + 148.5 s** (139.5 + 9).
    > P3 doběhne v čase **T0 + 175.5 s** jako poslední.

    ### Shrnutí odpovědí

    | Otázka | Odpověď |
    | ------ | ------- |
    | 1. Za kolik sekund po T0 se ukončí P0? | **103.5 s** |
    | 2. Za kolik sekund po T0 se fakticky začne zpracovávat P4? | **103.5 s** |
    | 3. Za kolik sekund po T0 se ukončí poslední proces? | **175.5 s** |
