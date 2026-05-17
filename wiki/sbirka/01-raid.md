# RAID

??? abstract "Obsah stránky"

    [TOC]

---

## Úloha 1 — RAID 1, 22 × 450 GiB (Seagate Savvio 10K.6)

!!! example "Zadání"
    Předpokládejte následující konfiguraci diskového pole:

    - Typ disků: Seagate Savvio 10K.6 (SAS, 6 Gib/s)
    - Počet a velikost disků: 22 x 450 GiB
    - Rychlost disku: 10000 rpm, 340 MiB/s
    - Spolehlivost disků: 1172000 h MTBF
    - Typ diskového pole: RAID 1
    - Řadič: 1x, pracuje s rychlostí 1700 MiB/s, k tomuto řadiči jsou přímo připojené všechny disky
    - Připojení pole: Ethernet 10GBASE-T (10 Gibit/s) x 1 rozhraní

    1. Jakou bude mít takové pole kapacitu (v GiB)? (odpověď celé nebo desetinné číslo)
    2. Jakou rychlostí bude v ideálním případě možné z pole sekvenčně číst (v MiB/s)? Odpověď má povolenou toleranci 1%. (odpověď celé nebo desetinné číslo)
    3. Jakou rychlostí bude v ideálním případě možné na pole sekvenčně zapisovat (v MiB/s)? Odpověď má povolenou toleranci 1%. (odpověď celé nebo desetinné číslo)
    4. Kolik disků může určitě vypadnout, aniž dojde ke ztrátě dat? Uvažujte nejhorší možný scénář výpadků. (odpověď celé nebo desetinné číslo)
    5. Jaká je pravděpodobnost (v procentech), že během 32 měsíců nedojde ke ztrátě dat (předpokládáme, že během této doby v poli nic nevyměňujeme)? Odpověď má povolenou toleranci 1%. Při výpočtu uvažujte, že rok má 365 dní a každý měsíc je právě 1/12 roku. (odpověď celé nebo desetinné číslo)
    6. Kolik sekund bude trvat obnova dat po výpadku a obnově jednoho disku? Předpokládáme, že diskové pole slouží k streamování videa, tedy požadavky jednotlivých uživatelů jsou sekvenční čtení velkého objemu dat, ale jednotlivý uživatelé požadují data umístěná na různých místech diskového pole. Průměrná zátěž uživatelů představuje datový tok 20 MiB/s. Pokud obnovu nelze provést, ponechte pole prázdné. Odpověď má povolenou toleranci 1%. (odpověď celé nebo desetinné číslo)

??? success "Řešení"

    **1. Kapacita**

    Použitím RAID 1 ukládáme data dvakrát, jednou samotná data a jednou redundantní kopii navíc. Proto máme jenom polovinu místa, které máme fyzicky dostupné.

    ```text
    (22 * 450) / 2 = 4950 GiB
    ```

    **2. Rychlost sekvenčního čtení**

    Můžeme číst z obou zrcadel zároveň, tedy dvojnásobkem rychlosti jednoho disku. Je třeba dát si pozor, aby daná hodnota nebyla limitovaná rychlostí řadiče či některého z rozhraní.

    ```text
    disky:     340 * 2 = 680 MiB/s
    řadič:     1700 MiB/s
    připojení: 10 Gibit/s = 10 * 1000 / 8 = 1250 MiB/s

    minimum = 680 MiB/s
    ```

    Výsledek: **680 MiB/s**

    **3. Rychlost sekvenčního zápisu**

    Zapisujeme paralelně na obě zrcadla, takže rychlost zápisu dosáhne maximálně rychlost jednoho disku. Opět je třeba zkontrolovat, jestli řadič zvládne dvojnásobek této rychlosti.

    ```text
    disky (zápis): 340 MiB/s (zapisuje se na obě zrcadla, ale rychlost = rychlost 1 disku)
    řadič:         1700 MiB/s (skrz řadič tečou 2 * 340 = 680 MiB/s – v pořádku)
    připojení:     1250 MiB/s

    výsledek = 340 MiB/s
    ```

    Výsledek: **340 MiB/s**

    **4. Tolerance výpadku**

    V nejhorším případě se může stát, že nám vypadnou dva disky, na kterých jsou stejná data, resp. původní data a jejich duplikát. V tomto případě data nemáme jak obnovit, tedy jediný možný výpadek kdy máme zaručenou obnovu je případ kdy selže jenom jeden disk.

    Výsledek: **1 disk**

    **5. Pravděpodobnost bez ztráty dat za 32 měsíců**

    Po nastudování přednášky zjistíme vzorec pro pravděpodobnost, že disk bude fungovat správně v době t. Doplníme hodnoty ze zadání a máme téměř celé řešení. Ještě třeba vzít v potaz, že máme 11 párů disků a vždy chceme, aby alespoň jeden z každého páru přežil.

    ```text
    R(t) = e^(-t / MTBF)

    (1 - (1 - R(t))^2)^11

    t = 32 * 24 * (365/12) hodin

    (1 - (1 - e^(-(32*24*(365/12)) / 1172000))^2)^11 = 99.572 %
    ```

    Výsledek: **99.572 %**

    **6. Doba obnovy jednoho disku**

    Běžná zapisovací rychlost pole je 340 MiB/s, ale uživatelé nám vezmou 20 MiB/s. Kapacita jednoho disku je 450 GiB, tedy 450 * 2^10 MiB.

    ```text
    efektivní rychlost = 340 - 20 = 320 MiB/s

    (450 * 1024) / 320 = 1440 s
    ```

    Výsledek: **1440 s**

---

## Úloha 2 — RAID 1, 14 × 1500 GiB (Seagate Barracuda 7200.4)

!!! example "Zadání"
    Předpokládejte následující konfiguraci diskového pole:

    - Typ disků: Seagate Barracuda 7200.4 (SATA, 3 Gib/s)
    - Počet a velikost disků: 14 x 1500 GiB
    - Rychlost disku: 7200 rpm, 110 MiB/s
    - Spolehlivost disků: 822000 h MTBF
    - Typ diskového pole: RAID 1
    - Řadič: 1x, pracuje s rychlostí 330 MiB/s, k tomuto řadiči jsou přímo připojené všechny disky
    - Připojení pole: Ethernet 1 Gibit/s x 1 rozhraní

    1. Jakou bude mít takové pole kapacitu (v GiB)? (odpověď celé nebo desetinné číslo)
    2. Jakou rychlostí bude v ideálním případě možné z pole sekvenčně číst (v MiB/s)? Odpověď má povolenou toleranci 1%. (odpověď celé nebo desetinné číslo)
    3. Jakou rychlostí bude v ideálním případě možné na pole sekvenčně zapisovat (v MiB/s)? Odpověď má povolenou toleranci 1%. (odpověď celé nebo desetinné číslo)
    4. Kolik disků může určitě vypadnout, aniž dojde ke ztrátě dat? Uvažujte nejhorší možný scénář výpadků. (odpověď celé nebo desetinné číslo)
    5. Jaká je pravděpodobnost (v procentech), že během 43 měsíců nedojde ke ztrátě dat (předpokládáme, že během této doby v poli nic nevyměňujeme)? Odpověď má povolenou toleranci 1%. Při výpočtu uvažujte, že rok má 365 dní a každý měsíc je právě 1/12 roku. (odpověď celé nebo desetinné číslo)
    6. Kolik sekund bude trvat obnova dat po výpadku a obnově jednoho disku? Předpokládáme, že diskové pole slouží k streamování videa, tedy požadavky jednotlivých uživatelů jsou sekvenční čtení velkého objemu dat, ale jednotlivý uživatelé požadují data umístěná na různých místech diskového pole. Průměrná zátěž uživatelů představuje datový tok 30 MiB/s. Pokud obnovu nelze provést, ponechte pole prázdné. Odpověď má povolenou toleranci 1%. (odpověď celé nebo desetinné číslo)

??? success "Řešení"

    **1. Kapacita**

    ```text
    (14 * 1500) / 2 = 10500 GiB
    ```

    Výsledek: **10500 GiB**

    **2. Rychlost sekvenčního čtení**

    ```text
    disky:     110 * 2 = 220 MiB/s
    řadič:     330 MiB/s
    připojení: 1 Gibit/s = 1000/8 = 125 MiB/s

    minimum = 125 MiB/s  (limitováno Ethernetem; 1 Gibit = 128 MiB)
    ```

    Výsledek: **128 MiB/s** (limitováno Ethernetem, 1 Gibit = 128 MiB)

    !!! note
        Sbírka uvádí výsledek 128 MiB/s s poznámkou „1 Gibit = 128 MiB" (používá binární konvenci: 1 Gb/s = 2^30 bit/s / 8 / 2^20 = 128 MiB/s).

    **3. Rychlost sekvenčního zápisu**

    ```text
    disky (zápis): 110 MiB/s
    řadič:         330 MiB/s
    připojení:     128 MiB/s

    minimum = 110 MiB/s
    ```

    Výsledek: **110 MiB/s**

    **4. Tolerance výpadku**

    Výsledek: **1 disk**

    **5. Pravděpodobnost bez ztráty dat za 43 měsíců**

    Máme 7 párů disků, vždy chceme, aby alespoň jeden z každého páru přežil.

    ```text
    t = 43 * 24 * (365/12) h

    R(t) = e^(-t / 822000)

    (1 - (1 - R(t))^2)^7 = 99.021 %
    ```

    Výsledek: **99.021 %**

    **6. Doba obnovy jednoho disku**

    ```text
    efektivní rychlost = 110 - 30 = 80 MiB/s

    (1500 * 1024) / 80 = 19200 s
    ```

    Výsledek: **19200 s**

---

## Úloha 3 — RAID 01, 18 × 3000 GiB (Seagate Barracuda 7200.4)

!!! example "Zadání"
    Předpokládejte následující konfiguraci diskového pole:

    - Typ disků: Seagate Barracuda 7200.4 (SATA, 1.5 Gib/s)
    - Počet a velikost disků: 18 x 3000 GiB
    - Rychlost disku: 7200 rpm, 120 MiB/s
    - Spolehlivost disků: 713000 h MTBF
    - Typ diskového pole: RAID 01
    - Řadič: 1x, pracuje s rychlostí 360 MiB/s, k tomuto řadiči jsou přímo připojené všechny disky
    - Připojení pole: Fibre Channel 800 (800MiB/s) x 4 rozhraní

    1. Jakou bude mít takové pole kapacitu (v GiB)? (odpověď celé nebo desetinné číslo)
    2. Jakou rychlostí bude v ideálním případě možné z pole sekvenčně číst (v MiB/s)? Odpověď má povolenou toleranci 1%. (odpověď celé nebo desetinné číslo)
    3. Jakou rychlostí bude v ideálním případě možné na pole sekvenčně zapisovat (v MiB/s)? Odpověď má povolenou toleranci 1%. (odpověď celé nebo desetinné číslo)
    4. Kolik disků může určitě vypadnout, aniž dojde ke ztrátě dat? Uvažujte nejhorší možný scénář výpadků. (odpověď celé nebo desetinné číslo)
    5. Jaká je pravděpodobnost (v procentech), že během 25 měsíců nedojde ke ztrátě dat (předpokládáme, že během této doby v poli nic nevyměňujeme)? Odpověď má povolenou toleranci 1%. Při výpočtu uvažujte, že rok má 365 dní a každý měsíc je právě 1/12 roku. (odpověď celé nebo desetinné číslo)
    6. Kolik sekund bude trvat obnova dat po výpadku a obnově jednoho disku? Předpokládáme, že diskové pole slouží k streamování videa, tedy požadavky jednotlivých uživatelů jsou sekvenční čtení velkého objemu dat, ale jednotlivý uživatelé požadují data umístěná na různých místech diskového pole. Průměrná zátěž uživatelů představuje datový tok 10 MiB/s. Pokud obnovu nelze provést, ponechte pole prázdné. Odpověď má povolenou toleranci 1%. (odpověď celé nebo desetinné číslo)

??? success "Řešení"

    **1. Kapacita**

    Stejně jako použitím RAID 1, tak i použitím RAID 01 ukládáme data dvakrát, jednou samotná data a jednou redundantní kopii navíc. Proto máme jenom polovinu místa, které máme fyzicky dostupné.

    ```text
    (18 * 3000) / 2 = 27000 GiB
    ```

    Výsledek: **27000 GiB**

    **2. Rychlost sekvenčního čtení**

    Pod každým zrcadlem je RAID 0, takže můžeme číst ze všech jeho devíti disků najednou. Rychlost čtení z jednoho zrcadla je tedy až 9 * 120 = 1080 MiB/s. Navíc můžeme číst z obou zrcadel paralelně, tedy celkem až 2 * 1080 = 2160 MiB/s. Zde je potřeba si všimnout, že jsme limitováni rychlostí řadiče.

    ```text
    disky:     18 * 120 = 2160 MiB/s
    řadič:     360 MiB/s
    připojení: 4 * 800 = 3200 MiB/s

    minimum = 360 MiB/s
    ```

    Výsledek: **360 MiB/s**

    **3. Rychlost sekvenčního zápisu**

    Z předchozí otázky už víme, že nám rychlost omezuje řadič. Na rozdíl od čtení je třeba data zapsat dvakrát.

    ```text
    360 / 2 = 180 MiB/s
    ```

    Výsledek: **180 MiB/s**

    **4. Tolerance výpadku**

    RAID 0 sám o sobě nemá žádnou odolnost vůči výpadku disku. Pokud nám v obou zrcadlech vypadne nějaký disk, data jsou nenávratně ztracena. Tedy jediný možný výpadek (kdy máme zaručenou obnovu) je případ, kdy selže jenom jeden disk.

    Výsledek: **1 disk**

    **5. Pravděpodobnost bez ztráty dat za 25 měsíců**

    RAID 01 má 2 zrcadla, každé po 9 discích. Pole přežije, pokud alespoň jedno zrcadlo přežije celé (všech jeho 9 disků musí fungovat). Pravděpodobnost, že jedno zrcadlo přežije = R(t)^9. Pravděpodobnost, že alespoň jedno ze dvou zrcadel přežije = 1 - (1 - R(t)^9)^2.

    ```text
    R(t) = e^(-t / MTBF)

    t = 25 * 24 * (365/12) h

    1 - (1 - (e^(-(25*24*(365/12)) / 713000))^9)^2 = 95.766 %
    ```

    Výsledek: **95.766 %**

    !!! note "Diagram výpočtu spolehlivosti RAID 01"
        ```text
        R(t) = e^(-t / MTBF)

                              přežije jedno
                              zrcadlo
                           ___________
                          /           \
        1 - (  1 -     R(t)^9        )^2
              \_________________________/
               obě zrcadla se poškodí
        ```

    **6. Doba obnovy jednoho disku**

    Při obnově se čte z partnerského zrcadla (9 disků, RAID 0). Maximální průtok jednoho zrcadla při čtení je 9 * 120 = 1080 MiB/s, ale jsme limitováni řadičem: 360 MiB/s. Data se zapisují na nový disk přes stejný řadič. Zápis zabere polovinu kapacity řadiče (zároveň se čte), tedy efektivní rychlost zápisu = 360 / 2 = 175 MiB/s. Uživatelská zátěž 10 MiB/s se odečítá.

    ```text
    efektivní rychlost = 360/2 - 10 = 175 - 10 = 165 MiB/s
    kapacita 1 zrcadla = 9 * 3000 * 1024 MiB

    (9 * 3000 * 1024) / (360/2 - 10) = 157988.57 s
    ```

    Výsledek: **157988.57 s**

    !!! note
        Sbírka uvádí výpočet jako `(9 * 3000 * 1024) / (350/2) = 157988.57 s`, kde 350 = 360 - 10 (uživatelská zátěž se odečítá od kapacity řadiče před půlením).

---

## Úloha 4 — RAID 6, 14 × 1500 GiB (WD RE SAS)

!!! example "Zadání"
    Předpokládejte následující konfiguraci diskového pole:

    - Typ disků: WD RE SAS (SAS, 12 Gib/s)
    - Počet a velikost disků: 14 x 1500 GiB
    - Rychlost disku: 7200 rpm, 150 MiB/s
    - Spolehlivost disků: 720000 h MTBF
    - Typ diskového pole: RAID 6
    - Řadič: 1x, pracuje s rychlostí 270 MiB/s, k tomuto řadiči jsou přímo připojené všechny disky
    - Připojení pole: FibreChannel 1600 (1600 MiB/s) x 2 rozhraní

    1. Jakou bude mít takové pole kapacitu (v GiB)? (odpověď desetinné číslo)
    2. Jakou rychlostí bude v ideálním případě možné z pole sekvenčně číst (v MiB/s)? Odpověď má povolenou toleranci 1%. (odpověď desetinné číslo)
    3. Jakou rychlostí bude v ideálním případě možné na pole sekvenčně zapisovat (v MiB/s)? Odpověď má povolenou toleranci 1%. (odpověď desetinné číslo)
    4. Kolik disků může určitě vypadnout, aniž dojde ke ztrátě dat? Uvažujte nejhorší možný scénář výpadků. (odpověď desetinné číslo)
    5. Jaká je pravděpodobnost (v procentech), že během 37 měsíců nedojde ke ztrátě dat (předpokládáme, že během této doby v poli nic nevyměňujeme)? Odpověď má povolenou toleranci 1%. (odpověď desetinné číslo)
    6. Kolik sekund bude trvat obnova dat při obnově jednoho disku za předpokladu, že uživatel diskové pole trvale zatěžuje požadavky průměrně 10 MiB/s? Pokud obnovu nelze provést, ponechte pole prázdné. Odpověď má povolenou toleranci 1%. (odpověď desetinné číslo)

??? success "Řešení"

    **1. Kapacita**

    Při použití RAID 6 se nám kromě dat ukládají dva paritní součty. Tyto součty jsou sice na různých discích, ale v důsledku zaberou kapacitu o objemu právě dvou disků. Pro n disků, kde nejmenší má kapacitu S_min, se kapacita spočítá jako (n − 2) × S_min.

    ```text
    (14 - 2) * 1500 = 12 * 1500 = 18000 GiB
    ```

    Výsledek: **18000 GiB**

    **2. Rychlost sekvenčního čtení**

    Ze dvou disků nečteme, protože je na nich paritní součet. Rychlost nám tedy vychází na 12 × 150 MiB/s, ale jsme limitováni řadičem.

    ```text
    disky:     12 * 150 = 1800 MiB/s  (ze 14 disků čte 12, 2 mají paritu)
    řadič:     270 MiB/s
    připojení: 2 * 1600 = 3200 MiB/s

    minimum = 270 MiB/s
    ```

    Výsledek: **270 MiB/s**

    **3. Rychlost sekvenčního zápisu**

    Jak víme z předchozí úlohy, rychlost je limitovaná rychlostí řadiče. Na rozdíl od případu čtení musíme do toku dat započítat i zápis paritního součtu. V tomto případě nám zápis paritního součtu zabere 2 části ze 14.

    ```text
    (12/14) * 270 MiB/s = 231.43 MiB/s
    ```

    Výsledek: **231.43 MiB/s**

    **4. Tolerance výpadku**

    Pro RAID 6 obecně platí odolnosti výpadku vůči dvěma diskům. Buď nám zůstanou všechna data, nebo alespoň jedna parita.

    Výsledek: **2 disky**

    **5. Pravděpodobnost bez ztráty dat za 37 měsíců**

    RAID 6 přežije výpadek libovolných 2 disků. Pravděpodobnost bez ztráty dat = pravděpodobnost, že selže 0 nebo 1 nebo 2 disky.

    ```text
    R(t) = e^(-t / MTBF)

    t = 37 * 24 * (365/12) h

    R(t) = e^(-(37*24*(365/12)) / 720000) = 96.31 %

    P = R(t)^14 + 14 * R(t)^13 * (1 - R(t)) + C(14,2) * R(t)^12 * (1 - R(t))^2
      = 98.66 %
    ```

    Výsledek: **98.66 %**

    **6. Doba obnovy jednoho disku**

    Na obnovu potřebujeme číst z 12 disků, z každého 1500 * 1024 MiB. Na jeden disk zapisujeme 1500 * 1024 MiB. Rychlost je omezená řadičem 270 - 10 = 260 MiB/s.

    ```text
    efektivní rychlost = 270 - 10 = 260 MiB/s

    (1500 * 1024) / (260/13) = (1500 * 1024) / 20 = 76800 s
    ```

    !!! note
        Sbírka uvádí výpočet: `(1500×1024) / (260/13) = 76800 s`. Při rebuildu RAID 6 se čte z 13 zbývajících disků a zapisuje 1, takže efektivní rychlost zápisu = (260 MiB/s) / 13 * 1 ≈ 20 MiB/s.

    Výsledek: **76800 s**

---

## Úloha 5 — RAID 10, 18 × 750 GiB (Seagate Savvio 10K.6)

!!! example "Zadání"
    Předpokládejte následující konfiguraci diskového pole:

    - Typ disků: Seagate Savvio 10K.6 (SAS, 6 Gib/s)
    - Počet a velikost disků: 18 x 750 GiB
    - Rychlost disku: 10000 rpm, 330 MiB/s
    - Spolehlivost disků: 1520000 h MTBF
    - Typ diskového pole: RAID 10 (mirror then strip)
    - Řadič: 1x, pracuje s rychlostí 270 MiB/s, k tomuto řadiči jsou přímo připojené všechny disky
    - Připojení pole: FibreChannel 1600 (1600 MiB/s) x 2 rozhraní

    1. Jakou bude mít takové pole kapacitu (v GiB)? (odpověď celé nebo desetinné číslo)
    2. Jakou rychlostí bude v ideálním případě možné z pole sekvenčně číst (v MiB/s)? Odpověď má povolenou toleranci 1%. (odpověď celé nebo desetinné číslo)
    3. Jakou rychlostí bude v ideálním případě možné na pole sekvenčně zapisovat (v MiB/s)? Odpověď má povolenou toleranci 1%. (odpověď celé nebo desetinné číslo)
    4. Kolik disků může určitě vypadnout, aniž dojde ke ztrátě dat? Uvažujte nejhorší možný scénář výpadků. (odpověď celé nebo desetinné číslo)
    5. Jaká je pravděpodobnost (v procentech), že během 45 měsíců nedojde ke ztrátě dat (předpokládáme, že během této doby v poli nic nevyměňujeme)? Odpověď má povolenou toleranci 1%. Při výpočtu uvažujte, že rok má 365 dní a každý měsíc je právě 1/12 roku. (odpověď celé nebo desetinné číslo)
    6. Kolik sekund bude trvat obnova dat po výpadku a obnově jednoho disku? Předpokládáme, že diskové pole slouží k streamování videa, tedy požadavky jednotlivých uživatelů jsou sekvenční čtení velkého objemu dat, ale jednotlivý uživatelé požadují data umístěná na různých místech diskového pole. Průměrná zátěž uživatelů představuje datový tok 20 MiB/s. Pokud obnovu nelze provést, ponechte pole prázdné. Odpověď má povolenou toleranci 1%. (odpověď celé nebo desetinné číslo)

??? success "Řešení"

    **1. Kapacita**

    Mirroring nám sebere polovinu fyzické kapacity všech disků, striping nám nesebere nic.

    ```text
    9 * 750 = 6750 GiB  (zůstane kapacita 9 disků, tedy 9 * 750 GiB)
    ```

    Výsledek: **6750 GiB**

    **2. Rychlost sekvenčního čtení**

    Mirroring umožňuje číst z obou zrcadel zároveň a striping čte z každého z devíti disků najednou, tedy teoreticky by bylo možné z pole číst rychlostí 18 * 330 MiB/s = 5940 MiB/s, tato rychlost je však limitována řadičem.

    ```text
    disky:     18 * 330 = 5940 MiB/s
    řadič:     270 MiB/s
    připojení: 2 * 1600 = 3200 MiB/s

    minimum = 270 MiB/s
    ```

    Výsledek: **270 MiB/s**

    **3. Rychlost sekvenčního zápisu**

    Maximální průtok řadičem je 270 MiB/s.

    ```text
    270 / 2 = 135 MiB/s
    ```

    Výsledek: **135 MiB/s**

    **4. Tolerance výpadku**

    V nejhorším případě nám vypadne v obou zrcadlech stejný disk, data pak nemáme jak obnovit. Pro případ jednoho disku stačí obnovit data z druhého zrcadla.

    Výsledek: **1 disk**

    **5. Pravděpodobnost bez ztráty dat za 45 měsíců**

    RAID 10 má 9 zrcadlených párů. Pole přežije, pokud v každém páru přežije alespoň jeden disk.

    ```text
    R(t) = e^(-t / MTBF) = e^(-(45*24*(365/12)) / 1520000)

    (1 - (1 - R(t))^2)^9 = 99.59 %
    ```

    !!! note "Diagram výpočtu spolehlivosti RAID 10"
        ```text
        R(t) = e^(-t / MTBF) = e^(-(45*24*(365/12)) / 1520000)

                      alespoň jeden
                      ze dvou přežije
                   ___________________
                  /                   \
        (         1 - (1 - R(t))^2    )^9
          \_________________________________/
           v každém z párů přežije
           alespoň jeden disk
        ```

    Výsledek: **99.59 %**

    **6. Doba obnovy jednoho disku**

    Disky jsou párované, po výpadku jednoho disku musíme data obnovit z druhého z páru. Maximální rychlost jednoho disku je 330 MiB/s. Máme 9 dvojic disků, mezi které se rozloží vytížení uživatelů. Na jednu dvojici tak připadne 20/9 MiB/s. Data je možné souběžně číst a zapisovat, tedy nám stačí spočítat, za jak dlouho se přenese 750 GiB touto rychlostí.

    ```text
    efektivní rychlost = 330 - 20/9 MiB/s

    (750 * 1024) / (330 - 20/9) = 2343.05 s
    ```

    Výsledek: **2343.05 s**

---

## Úloha 6 — RAID 10, 14 × 3000 GiB (Seagate Barracuda 7200.14)

!!! example "Zadání"
    Předpokládejte následující konfiguraci diskového pole:

    - Typ disků: Seagate Barracuda 7200.14 (SATA, 3 Gib/s)
    - Počet a velikost disků: 14 x 3000 GiB
    - Rychlost disku: 7200 rpm, 110 MiB/s
    - Spolehlivost disků: 765000 h MTBF
    - Typ diskového pole: RAID 10 (mirror than strip)
    - Řadič: 1x, pracuje s rychlostí 330 MiB/s, k tomuto řadiči jsou přímo připojené všechny disky
    - Připojení pole: Ethernet 10GBASE-T (10 Gibit/s) x 3 rozhraní

    1. Jakou bude mít takové pole kapacitu (v GiB)? (odpověď celé nebo desetinné číslo)
    2. Jakou rychlostí bude v ideálním případě možné z pole sekvenčně číst (v MiB/s)? Odpověď má povolenou toleranci 1%. (odpověď celé nebo desetinné číslo)
    3. Jakou rychlostí bude v ideálním případě možné na pole sekvenčně zapisovat (v MiB/s)? Odpověď má povolenou toleranci 1%. (odpověď celé nebo desetinné číslo)
    4. Kolik disků může určitě vypadnout, aniž dojde ke ztrátě dat? Uvažujte nejhorší možný scénář výpadků. (odpověď celé nebo desetinné číslo)
    5. Jaká je pravděpodobnost (v procentech), že během 40 měsíců nedojde ke ztrátě dat (předpokládáme, že během této doby v poli nic nevyměňujeme)? Odpověď má povolenou toleranci 1%. Při výpočtu uvažujte, že rok má 365 dní a každý měsíc je právě 1/12 roku. (odpověď celé nebo desetinné číslo)
    6. Kolik sekund bude trvat obnova dat po výpadku a obnově jednoho disku? Předpokládáme, že diskové pole slouží k streamování videa, tedy požadavky jednotlivých uživatelů jsou sekvenční čtení velkého objemu dat, ale jednotlivý uživatelé požadují data umístěná na různých místech diskového pole. Průměrná zátěž uživatelů představuje datový tok 20 MiB/s. Pokud obnovu nelze provést, ponechte pole prázdné. Odpověď má povolenou toleranci 1%. (odpověď celé nebo desetinné číslo)

??? success "Řešení"

    **1. Kapacita**

    ```text
    (14 / 2) * 3000 = 7 * 3000 = 21000 GiB
    ```

    Výsledek: **21000 GiB**

    **2. Rychlost sekvenčního čtení**

    ```text
    disky:     14 * 110 = 1540 MiB/s
    řadič:     330 MiB/s
    připojení: 3 * (10 * 1000 / 8) = 3 * 1250 = 3750 MiB/s

    minimum = 330 MiB/s  (omezené řadičem)
    ```

    Výsledek: **330 MiB/s**, omezené řadičem

    **3. Rychlost sekvenčního zápisu**

    ```text
    330 / 2 = 165 MiB/s  (omezené řadičem)
    ```

    Výsledek: **165 MiB/s**, omezené řadičem

    **4. Tolerance výpadku**

    Výsledek: **1 disk**

    **5. Pravděpodobnost bez ztráty dat za 40 měsíců**

    RAID 10 má 7 zrcadlených párů.

    ```text
    R(40 měsíců) = e^(-(40*24*(365/12)) / 765000) = 96.25 %

    (1 - (1 - R(t))^2)^7 = 99.02 %
    ```

    Výsledek: **99.02 %**

    **6. Doba obnovy jednoho disku**

    ```text
    efektivní rychlost páru = 110 - 20/7 MiB/s

    (3000 * 1024) / (110 - 20/7) = 28672.7 s
    ```

    Výsledek: **28672.7 s**
