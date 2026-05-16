# Disky a RAID

Dva typy úloh z jedné oblasti: **disk I/O** — kolik milisekund trvá přečíst soubor s ohledem na mechaniku HDD — a **RAID** — kapacita, přenosové rychlosti, tolerance výpadků, spolehlivost a doba obnovy diskového pole. Oba typy se na zkoušce objevují souběžně nebo každý samostatně.

??? abstract "Obsah stránky"

    [TOC]

---

## Co tento typ úlohy prověřuje

- Pochopení mechaniky HDD: seek, rotační zpoždění, přenosová rychlost sektoru.
- Rozdíl mezi **sekvenčním** a **náhodným** přístupem k souboru.
- Výpočet kapacity, čtecích/zápisových rychlostí a tolerance výpadku pro různé úrovně RAID.
- Výpočet spolehlivosti pole pomocí vzorce `R(t) = exp(-t / MTBF)` a binomického rozvoje.
- Odhad doby rebuildu pole po výpadku disku.
- Identifikace úzkého hrdla v řetězu: disk × počet, řadič, síťové připojení.

---

## Co potřebuješ znát

### Vzorce pro disk I/O

```text
Doba jedné otáčky [ms]   = 60 000 / rpm
Průměrné rotační zpoždění = otáčka / 2
Doba čtení 1 sektoru     = otáčka / počet_sektorů_na_stopě (nebo cylindru)
Počet sektorů souboru    = velikost_souboru / velikost_sektoru

Náhodné rozmístění:
  čas = A * (seek + otáčka/2 + otáčka/sektorů_na_stopě)
  kde A = počet sektorů souboru

Sekvenční rozmístění (sousední cylindry):
  čas = seek_první_cylindr + rotace_první_stopa + přenos_první_stopy
        + (počet_dalších_stop * (seek_sousední + rotace + přenos_stopy))
```

### Tabulka RAID (N disků velikosti S)

| RAID | Kapacita | Čtení (ideál) | Zápis (ideál) | Tolerance výpadku (nejhorší) |
|---|---|---|---|---|
| 0 (striping) | N × S | N × disk | N × disk | 0 |
| 1 (zrcadlení, pár) | S | 2 × disk | disk | 1 (z páru přežije 1) |
| 5 | (N−1) × S | N × disk | ~N × disk | 1 |
| 6 | (N−2) × S | N × disk | ~N × disk | 2 |
| 10 (mirror+stripe) | (N/2) × S | N × disk | (N/2) × disk | 1 (pesimisticky) |
| 01 (stripe+mirror) | (N/2) × S | N × disk | (N/2) × disk | 1 (pesimisticky) |

Skutečná rychlost = **minimum** přes celý řetěz: (disky × počet), řadič, síťové rozhraní (součet rozhraní).

### Vzorce pro spolehlivost

```text
Spolehlivost jednoho disku:  R = exp(-t / MTBF)
  t v hodinách, MTBF v hodinách

Přepočet času:  t = měsíce * (365 * 24 / 12)  [h]

RAID 0  (musí přežít všechny):     P = R^N
RAID 5  (stačí N-1 z N):           P = R^N + N * R^(N-1) * (1-R)
RAID 6  (stačí N-2 z N):           P = R^N + N*R^(N-1)*(1-R) + C(N,2)*R^(N-2)*(1-R)^2
RAID 10 (P párů, každý pár OK):    P = (1 - (1-R)^2)^P
  kde P = počet zrcadlených párů = N/2

Doba rebuildu = kapacita_jednoho_disku / efektivní_rychlost_zápisu
efektivní_rychlost = rychlost_disku - uživatelská_zátěž
```

[Skripta: Datová úložiště a souborové systémy](../../skripta/07-souborove-systemy.md)

---

## Postup řešení krok za krokem

### A) Disk I/O — přečti soubor

**Krok 1 — Spočítej dobu jedné otáčky.**

```text
otáčka [ms] = 60 000 / rpm
```

Příklad: 10 000 rpm → otáčka = 60 000 / 10 000 = **6 ms**.

**Krok 2 — Spočítej průměrné rotační zpoždění.**

```text
rotační zpoždění = otáčka / 2
```

Příklad: 6 ms / 2 = **3 ms**. Toto je průměr — na začátku každého přístupu musíme čekat, než se správný sektor otočí pod hlavičku; v průměru to je polovina otáčky.

**Krok 3 — Spočítej dobu čtení jednoho sektoru.**

```text
přenos_sektoru [ms] = otáčka / počet_sektorů_na_stopě (cylindru)
```

Příklad: 6 ms / 8192 sektorů ≈ **0.000732 ms** (velmi malé číslo — přenos samotných dat trvá kratičce).

**Krok 4 — Spočítej počet sektorů souboru.**

```text
A = velikost_souboru [B] / velikost_sektoru [B]
```

Příklad: 7 819 264 B / 4096 B = **1909 sektorů**. Výsledek musí být celé číslo — pokud ne, zaokrouhli nahoru (`ceil`).

**Krok 5 — Rozlišuj: náhodné nebo sekvenční rozmístění?**

Zadání vždy explicitně říká, jde-li o „náhodně rozmístěné sektory" nebo „sektory uložené sekvenčně (na sousedních cylindrech/stopách)". Toto zásadně ovlivňuje výpočet.

**Krok 6a — Náhodné rozmístění (každý sektor = nový přístup na disk).**

```text
čas_celkem = A * (seek + rotační_zpoždění + přenos_sektoru)
```

Každý ze `A` sektorů stojí plný seek (hlavičky se přesunou přes celý disk), plné rotační zpoždění, pak přenos dat. Výsledek bývá řádově sekundy i pro malé soubory.

Příklad:
```text
1909 * (9 + 3 + 6/8192)
= 1909 * (9 + 3 + 0.000732...)
= 1909 * 12.000732...
≈ 22 909.4 ms
```

**Krok 6b — Sekvenční rozmístění (stopy za sebou).**

```text
Počet stop (cylindrů) = ceil(A / sektorů_na_stopě)

První stopa:    seek_průměrný + rotační_zpoždění + přenos_celé_stopy
Každá další:    seek_sousední  + rotační_zpoždění + přenos_celé_stopy

přenos_celé_stopy [ms] = otáčka
```

Výsledek je typicky desítky až stovky ms — řádově stovky až tisíckrát rychlejší než náhodný přístup.

**Krok 7 — Zkontroluj jednotky.** Seek a rotace jsou v ms, přenos sektoru také v ms — finální výsledek v ms. Převod na sekundy jen pokud zadání požaduje.

---

### B) RAID — kapacita, rychlost, spolehlivost, rebuild

**Krok 1 — Identifikuj typ RAID a počet disků.**

Přečti zadání pozorně: RAID 01 = nejprve striping, pak mirroring (opak RAID 10). U kombinovaných typů 10 a 01 je kapacita stejná, ale odolnost a výkon se mohou lišit.

**Krok 2 — Spočítej kapacitu pole.**

Použij tabulku výše. U RAID 10/01 s N disky: `kapacita = (N/2) * S`, kde S je velikost jednoho disku.

Příklad (RAID 01, 12 × 1500 GiB): kapacita = (12/2) × 1500 = **9000 GiB**.

**Krok 3 — Urči rychlost čtení.**

Rychlost se počítá jako minimum ze tří složek:

```text
1. disky: rychlost_jednoho_disku * počet_disků_čtoucích_paralelně
2. řadič: propustnost řadiče [MiB/s]
3. připojení: součet_všech_rozhraní * rychlost_jednoho_rozhraní [MiB/s]
```

Výsledek = min(1, 2, 3).

U RAID s mirrorem: při čtení mohou číst všechny disky (i ze záložní kopie), proto se použije plný počet disků. U RAID 0/5/6: čtou všechny disky.

**Krok 4 — Urči rychlost zápisu.**

Zápis je komplikovanější — data musí být zapsána na více míst:

- RAID 1/10/01: data se zapíší 2× (na obě kopie zrcadla). Skrz řadič tedy tečou 2× tolik dat → `rychlost_zápisu = propustnost_řadiče / 2`.
- RAID 5: musí se přepočítat parita → efektivní rychlost zápisu je nižší než čtení.
- RAID 0: zápis stejný jako čtení.

Znovu vezmi minimum přes celý řetěz.

**Krok 5 — Urči toleranci výpadku.**

Otázka zní „kolik disků může určitě vypadnout v nejhorším scénáři". Nejhorší scénář = výpadky jsou vždy co nejhorší pro daný typ:

- RAID 10/01: stačí, aby vypadl 1 disk z každého mirroru ve stejné skupině → garantovaně přežije **1 disk**.
- RAID 5: garantovaně přežije **1 disk**.
- RAID 6: garantovaně přežije **2 disky**.
- RAID 0: přežije **0 disků**.

**Krok 6 — Spočítej spolehlivost pole za dané období.**

```text
a) Převeď čas na hodiny:
   t = měsíce * (365 * 24 / 12)   [h]
   Nebo: t = roky * 365 * 24       [h]

b) Spočítej spolehlivost jednoho disku:
   R = exp(-t / MTBF)

c) Dosaď do vzorce pro daný typ RAID:
   RAID 0:  P = R^N
   RAID 5:  P = R^N + N * R^(N-1) * (1-R)
   RAID 6:  P = R^N + N*R^(N-1)*(1-R) + C(N,2)*R^(N-2)*(1-R)^2
   RAID 10 (P párů): P = (1 - (1-R)^2)^P
```

Výsledek vynásob 100 pro procenta.

**Krok 7 — Spočítej dobu rebuildu.**

```text
efektivní_rychlost_zápisu = rychlost_disku - uživatelská_zátěž  [MiB/s]
doba_rebuildu = kapacita_disku [MiB] / efektivní_rychlost_zápisu  [s]

Kapacita: 1 GiB = 1024 MiB, 1 TiB = 1024 GiB = 1048576 MiB
```

Při rebuildu: data se čtou z partnera (RAID 1) nebo z ostatních disků (RAID 5: N−1 disků), pak se zapisují na nový disk. Uživatelská zátěž odečte od dostupné rychlosti.

!!! warning "Pozor u RAID 5 — efektivní rychlost zápisu při rebuildu"
    U RAID 5 se při rebuildu čte ze všech N−1 zbývajících disků a zapisuje se 1 disk nový. V ustáleném stavu je poměr čtení:zápis = (N−1):1. Pokud je propustnost řadiče omezující, efektivní rychlost zápisu = propustnost_řadiče / N (čtení tvoří (N−1)/N provozu, zápis 1/N).

    Příklad (RAID 5, 10 disků, propustnost 250 MiB/s, bez uživatelské zátěže):
    ```text
    zápis = 250 / 10 = 25 MiB/s
    rebuild 1 TiB: 1 * 1024 * 1024 MiB / 25 MiB/s = 41943 s ≈ 11.6 h
    ```

**Krok 8 — Zkontroluj: nepominul jsi žádný článek řetězu?**

Zejména síťové připojení — zadání uvádí „Fibre Channel 800 MiB/s × 4 rozhraní" → součet = 3200 MiB/s. Nebo „Ethernet 1000BASE-T × 2" → 2 × 125 MiB/s = 250 MiB/s. Vždy přepočítej Gbit/s na MiB/s: 1 Gbit/s ≈ 125 MiB/s.

---

## Vzorové zadání

!!! example "Zadání"
    **A) Disk.** Pevný disk: velikost sektoru 4096 B, průměrný počet sektorů na cylindr 8192, rychlost 10 000 rpm, průměrná doba vystavení hlaviček 9 ms. Jak dlouho bude trvat přečíst soubor o velikosti 7 819 264 B, pokud je uložen na **náhodně rozmístěných sektorech**?

    **B) RAID.** Diskové pole: 12 × 1500 GiB, disky 7200 rpm / 280 MiB/s, MTBF 765 000 h. Typ pole: **RAID 01** (nejprve striping, pak mirroring). Řadič 1120 MiB/s, připojení Fibre Channel 800 MiB/s × 4 rozhraní.

    1. Kapacita pole (GiB)?
    2. Rychlost sekvenčního čtení (MiB/s)?
    3. Rychlost sekvenčního zápisu (MiB/s)?
    4. Kolik disků určitě může vypadnout bez ztráty dat (nejhorší scénář)?
    5. Pravděpodobnost (%), že během 45 měsíců nedojde ke ztrátě dat?
    6. Doba obnovy jednoho disku při uživatelské zátěži 30 MiB/s?

    *Disk I/O: termíny 2010–2012, 2019, 2023. RAID: každý termín od 2014.*

---

## Řešení vzorového zadání

??? success "Ukázat řešení"

    ### A) Disk — náhodné sektory

    **Krok 1 — Otáčka:**
    ```text
    otáčka = 60 000 / 10 000 = 6 ms
    ```

    **Krok 2 — Rotační zpoždění:**
    ```text
    rotační zpoždění = 6 / 2 = 3 ms
    ```

    **Krok 3 — Přenos 1 sektoru:**
    ```text
    přenos = 6 / 8192 ≈ 0.000732 ms
    ```

    **Krok 4 — Počet sektorů:**
    ```text
    A = 7 819 264 / 4096 = 1909 sektorů  (celé číslo, žádné zaokrouhlování)
    ```

    **Krok 5 — Celkový čas:**
    ```text
    čas = 1909 * (9 + 3 + 0.000732)
        = 1909 * 12.000732
        ≈ 22 909.4 ms
        ≈ 22.9 s
    ```

    ---

    ### B) RAID 01, 12 × 1500 GiB

    **1. Kapacita**

    RAID 01 = nejprve striping (skupiny), pak mirroring (zrcadlení skupin). Polovina disků je záložní kopie.
    ```text
    kapacita = (12 / 2) * 1500 = 6 * 1500 = 9000 GiB
    ```

    **2. Čtení**

    Identifikujeme všechny články řetězu:
    ```text
    disky:      12 * 280 = 3360 MiB/s  (všechny disky čtou paralelně)
    řadič:      1120 MiB/s
    připojení:  4 * 800 = 3200 MiB/s
    ```
    Minimum = **řadič 1120 MiB/s** → rychlost čtení = **1120 MiB/s**.

    **3. Zápis**

    RAID 01 zapisuje data 2× (na obě zrcadlené skupiny). Skrz řadič proteče dvojnásobek dat:
    ```text
    efektivní rychlost zápisu = 1120 / 2 = 560 MiB/s
    ```
    Zkontroluj ostatní články:
    ```text
    disky (zápis): 6 * 280 = 1680 MiB/s  (zapisuje jen jedna polovina)
    připojení:     3200 MiB/s
    ```
    Minimum je stále řadič (1120 MiB/s skrz, tedy 560 MiB/s efektivně).
    Rychlost zápisu = **560 MiB/s**.

    **4. Tolerance výpadku**

    RAID 01 = stripe + mirror. V nejhorším scénáři vypadne jeden disk z každé skupiny na odpovídajících pozicích — celá skupina je nedostupná a zrcadlo je zničeno. Garantovaně přežije výpadek **1 disku**.

    !!! note "Optimistický vs. pesimistický odhad"
        Pesimisticky (nejhorší scénář): 1 disk. Optimisticky (výpadky v různých skupinách): až 6 disků. Zadání se ptá na nejhorší scénář → **1 disk**.

    **5. Spolehlivost za 45 měsíců**

    ```text
    Krok a — čas na hodiny:
      t = 45 * (365 * 24 / 12) = 45 * 730 = 32 850 h

    Krok b — spolehlivost jednoho disku:
      R = exp(-32 850 / 765 000)
        = exp(-0.042941...)
        ≈ 0.95797

    Krok c — RAID 01 má 6 zrcadlených párů (12 disků / 2):
      P = (1 - (1-R)^2)^6
        = (1 - (1 - 0.95797)^2)^6
        = (1 - (0.04203)^2)^6
        = (1 - 0.001766...)^6
        = (0.998234...)^6
        ≈ 0.98944...
        ≈ 98.94 %
    ```

    Pravděpodobnost bez ztráty dat ≈ **98.94 %** (přesnou hodnotu dopočítej kalkulačkou — povolená tolerance 1 ‰).

    **6. Doba obnovy**

    Při obnově se čte z partnerské skupiny zrcadla a zapisuje na nový disk. Omezujícím faktorem je rychlost disku snížená o uživatelskou zátěž:
    ```text
    efektivní rychlost = 280 - 30 = 250 MiB/s

    kapacita disku = 1500 GiB = 1500 * 1024 MiB = 1 536 000 MiB

    doba = 1 536 000 / 250 = 6144 s ≈ 1.71 h
    ```

---

## Další procvičení

### Varianta 1 — Disk I/O, sekvenční čtení

!!! example "Zadání"
    Disk: velikost sektoru 512 B, 320 sektorů na stopu, 7200 rpm, průměrný seek 10 ms, seek na sousední stopu 1 ms. Jak dlouho trvá přečíst soubor s 2560 sektory uloženými **sekvenčně na sousedních stopách**?

??? success "Ukázat řešení"
    **Krok 1 — Otáčka:**
    ```text
    otáčka = 60 000 / 7200 ≈ 8.333 ms
    ```

    **Krok 2 — Rotační zpoždění:**
    ```text
    rotace = 8.333 / 2 ≈ 4.167 ms
    ```

    **Krok 3 — Přenos celé stopy:**
    ```text
    přenos_stopy = otáčka = 8.333 ms  (přeneseme všechny sektory na stopě)
    ```

    **Krok 4 — Počet stop:**
    ```text
    stopy = 2560 / 320 = 8 stop
    ```

    **Krok 5 — Celkový čas:**
    ```text
    První stopa:  10 (seek) + 4.167 (rotace) + 8.333 (přenos) = 22.5 ms
    Každá další:   1 (seek) + 4.167 (rotace) + 8.333 (přenos) = 13.5 ms

    celkem = 22.5 + 7 * 13.5 = 22.5 + 94.5 = 117 ms
    ```

    **Srovnání:** náhodné čtení stejného počtu sektorů by trvalo 2560 × (10 + 4.167 + 8.333/320) = 2560 × 14.193 ≈ 36 333 ms ≈ 36 s — tedy přibližně **310× déle**.

---

### Varianta 2 — RAID 5, spolehlivost a rebuild

!!! example "Zadání"
    Diskové pole: 8 × 1500 GiB, disky 7200 rpm / 90 MiB/s, MTBF 829 000 h. Typ: **RAID JBOD** (concatenation, tj. RAID 0). Řadič 180 MiB/s, připojení Ethernet 1000BASE-T × 2 rozhraní (1 Gbit/s každé).

    1. Kapacita (GiB)?
    2. Rychlost sekvenčního čtení (MiB/s)?
    3. Kolik disků může vypadnout (nejhorší scénář)?
    4. Pravděpodobnost bez ztráty dat za 43 měsíců?
    5. Doba obnovy jednoho disku při zátěži 30 MiB/s (pokud je možná)?

??? success "Ukázat řešení"
    **1. Kapacita:** RAID 0 (JBOD) = 8 × 1500 = **12 000 GiB**.

    **2. Čtení:**
    ```text
    disky:      8 * 90 = 720 MiB/s
    řadič:      180 MiB/s
    připojení:  2 * 125 = 250 MiB/s  (1 Gbit/s = 125 MiB/s)
    ```
    Minimum = **řadič 180 MiB/s** → rychlost čtení = **180 MiB/s**.

    **3. Tolerance výpadku:** RAID 0 (JBOD) — výpadek 1 disku = ztráta dat → **0 disků**.

    **4. Spolehlivost za 43 měsíců:**
    ```text
    t = 43 * 730 = 31 390 h
    R = exp(-31 390 / 829 000) = exp(-0.037864...) ≈ 0.96285
    RAID 0: P = R^8 = (0.96285)^8 ≈ 0.7405 ≈ 74.05 %
    ```

    **5. Obnova:** RAID 0 nemá redundanci — po výpadku disku jsou data **ztracena**, obnova není možná.

---

## Varianty a chytáky

- **Rušivé parametry:** zadání obsahuje spoustu číslic — kapacita disku u disk-I/O úloh, typ rozhraní SATA, rpm u RAID bez výpočtu seek. Mnoho z nich pro konkrétní otázku nepotřebuješ. Přečti otázku a vyber pouze relevantní veličiny.

- **Rychlost = vždy minimum přes celý řetěz.** Nezapomeň přepočítat síťové rozhraní: `Gbit/s → MiB/s = Gbit/s * 1000 / 8` (nebo přibližně `* 125`). Více rozhraní se sčítá.

- **Zápis na zrcadlo / s paritou.** RAID 1/10/01 zapisuje 2× → přes řadič tečou 2× data → efektivní rychlost = propustnost_řadiče / 2. RAID 5/6 musí navíc generovat paritu — odhad efektivní rychlosti je složitější (závisí na implementaci).

- **RAID 10 vs. RAID 01 — rozdíl!** RAID 10 = nejprve zrcadlení párů, pak striping přes páry (odolnější). RAID 01 = nejprve striping skupin, pak zrcadlení skupin (méně odolný — stačí vypadnout po jednom disku z každé skupiny). Na zkoušce rozlišuj přesně.

- **Nejhorší vs. optimistický scénář výpadku.** RAID 10/01 pesimisticky = 1 disk. Optimisticky (všechny výpadky v různých párech) = N/2 disků. Otázka se typicky ptá na nejhorší scénář.

- **Rok = 365 dní, měsíc = 1/12 roku** (explicitně ve většině zadání). Nepočítej měsíc jako 30 dní, pokud zadání říká jinak.

- **Rebuild RAID 5 a poměr čtení:zápis.** Při rebuildu RAID 5 se čte z N−1 disků a zapisuje 1. Propustnost sběrnice/řadiče se dělí v poměru (N−1):1 mezi čtení a zápis → efektivní rychlost zápisu = propustnost / N. Nezaměňuj s RAID 1, kde se pouze čte ze zrcadla a zapisuje.

- **Přepočet kapacity pro rebuild.** 1 GiB = 1024 MiB, 1 TiB = 1024 GiB = 1 048 576 MiB. Výsledek v sekundách — případně převeď na hodiny.

---

## Časté chyby

- **Zapomenutí na článek řetězu.** Nejčastěji se přehlédne síťové připojení (nebo počet rozhraní). Vždy vyjmenuj všechny tři složky: disky, řadič, připojení.

- **Zápis = čtení u RAID s mirrorem.** Chybný předpoklad, že zápis je stejně rychlý jako čtení u RAID 01/10. Data se zapisují dvakrát, efektivní rychlost je tedy poloviční (při řadiči jako bottlenecku).

- **Záměna rpm za sektorů/stopě.** Zadání uvádí obojí — nezaměňuj. `otáčka = 60 000 / rpm`, přenos sektoru = `otáčka / sektorů_na_stopě`.

- **Pesimistický vs. optimistický výpadek.** Typická chyba u RAID 10: uvést 5 disků (optimistický odhad) místo 1 disku (pesimistický).

- **Spolehlivost jednoho disku vs. pole.** R(t) = spolehlivost jednoho disku. Spolehlivost pole závisí na typu RAID — vždy dosaď do správného vzorce.

- **Měsíce → hodiny.** `t = 45 * (365 * 24 / 12) = 45 * 730`. Chyba: použití 30 dní/měsíc nebo zapomenutí na převod.

- **Disk I/O: přenos sektoru je zanedbatelný** oproti seeku a rotaci. Přesto ho počítej — u náhodného přístupu se přičítá ke každému sektoru a u tisíců sektorů se projeví.

- **JBOD ≠ RAID 0 striping (pro výkon, ale ano pro spolehlivost).** JBOD (concatenation) a RAID 0 (striping) mají stejnou kapacitu a toleranci výpadku (0), ale JBOD čte sekvenčně z jednoho disku, striping čte paralelně. U výpočtu rychlosti je nutné vědět, co zadání míní.

---

## Související

- [Skripta: Datová úložiště a souborové systémy](../../skripta/07-souborove-systemy.md)
- [Teoretické otázky — true/false](../teorie-truefalse.md)
- [Zpět na přehled praktických příkladů](index.md)
