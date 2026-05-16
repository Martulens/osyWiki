# Souborové systémy

Úlohy na souborové systémy se zaměřují na dvě oblasti: **výpočty kapacit** (maximální velikost souboru v UFS, velikost FAT tabulky, srovnání správy volného prostoru) a **sledování operací nad FS** (kolik i-nodů a datových bloků se při `cp`/`mv`/`ln`/`rm` přečte nebo zapíše). Obě oblasti jsou pravidelnou součástí každého zkouškového termínu.

??? abstract "Obsah stránky"

    [TOC]

---

## Co tento typ úlohy prověřuje

- Porozumění struktuře i-nodu v UFS — přímé a nepřímé ukazatele, počet odkazů v bloku.
- Schopnost vypočítat maximální velikost souboru a souborového systému z daných parametrů.
- Porozumění struktuře FAT — kolik místa zabírá FAT tabulka, jak velký soubor může FAT adresovat.
- Srovnání bitové mapy a zřetězeného seznamu pro správu volného prostoru.
- Schopnost trasovat operace `cp`, `mv`, `ln`, `rm` a spočítat přesný počet přečtených a zapsaných i-nodů a datových bloků, včetně alokací.

---

## Co potřebuješ znát

### UFS — vzorce

**Počet odkazů v jednom bloku (R):**

```text
R = velikost_bloku_v_B * 8 / bity_odkazu
```

Příklad: blok 8 KiB, odkaz 64bitový → R = 8192 * 8 / 64 = 1024

**Celkový počet adresovatelných datových bloků:**

```text
12 + R + R^2 + R^3
```

- 12 přímých odkazů přímo v i-nodu
- R odkazů přes jednonásobný nepřímý blok
- R^2 odkazů přes dvojnásobný nepřímý blok (blok s R ukazateli na bloky s R ukazateli)
- R^3 odkazů přes trojnásobný nepřímý blok

**Maximální velikost souboru:**

```text
max_velikost = (12 + R + R^2 + R^3) * velikost_bloku
```

**Maximální velikost souborového systému:**

```text
max_FS = 2^(bity_adresy) * velikost_bloku
```

(Omezeno délkou adresy, ne i-nodem — souborový systém může mít více souborů.)

### FAT — vzorce

**Maximální velikost souboru (v FAT):**

```text
max_soubor_FAT = 2^(bity_adresy) * velikost_clusteru
```

**Počet clusterů v oblasti:**

```text
pocet_clusteru = kapacita_oblasti / velikost_clusteru
```

**Velikost FAT tabulky:**

```text
velikost_FAT = pocet_clusteru * ceil(bity_adresy / 8)
```

Adresa se zaokrouhluje na celé bajty (28 bitů → 4 B, 12 bitů → 2 B).

### Volné objekty FS

| Struktura | Paměť | Kdy je výhodná |
|---|---|---|
| Bitmapa | B bitů (1 bit / blok) | Skoro vždy; rychlé bitové operace |
| Zřetězený seznam | F * D bitů (adresa na volný blok) | Pokud je F * D < B |

Podmínka, kdy je zřetězený seznam menší než bitmapa: **F * D < B**

- B = celkový počet bloků FS
- F = počet volných bloků
- D = počet bitů adresy jednoho bloku

### FS operace — přehled

| Operace | I-nody ke čtení | I-nody k zápisu | Datové bloky ke čtení | Datové bloky k zápisu | Alokace |
|---|---|---|---|---|---|
| `mv` (stejný FS) | cesta zdroj + cesta cíl + soubor | zdrojový adresář + cílový adresář | obsah všech adresářů cesty | obsah zdrojového + cílového adresáře | žádná |
| `mv` (jiný FS) | stejné jako `cp` + `rm` | stejné jako `cp` + `rm` | data souboru | data souboru | ano (cíl), uvolnění (zdroj) |
| `ln` (hard link) | cesta cíle + soubor | soubor (++čítač) + cílový adresář | obsah adresářů cesty cíle | obsah cílového adresáře | žádná |
| `ln -s` (symlink) | cesta cíle | nový i-node linku + cílový adresář | obsah adresářů cesty cíle | datový blok linku (cílová cesta) + obsah cílového adresáře | 1 i-node + 1 datový blok |
| `rm` | celá cesta + soubor | zdrojový adresář + i-node souboru | obsah všech adresářů cesty | obsah zdrojového adresáře | uvolnění i-nodu + bloků |
| `cp` | cesty obou + zdroj | nový i-node + cílový adresář | obsah adresářů + data zdroje | data cíle + obsah cílového adresáře | 1 i-node + datové bloky |

[Skripta: Datová úložiště a souborové systémy](../../skripta/07-souborove-systemy.md)

---

## Postup řešení krok za krokem

### A. Výpočet kapacit UFS

1. **Přečti zadání:** zapiš si velikost bloku (v bajtech), délku odkazu (v bitech) a počet přímých a nepřímých odkazů v i-nodu.

2. **Spočítej R — počet odkazů v jednom bloku:**

   ```text
   R = velikost_bloku_v_B * 8 / bity_odkazu
   ```

   Příklad: blok 8 KiB = 8192 B, odkaz 64 b → R = 8192 * 8 / 64 = 65536 / 64 = **1024**

3. **Zkontroluj, zda R je celé číslo.** Pokud ne, zkontroluj jednotky (B vs. KiB).

4. **Spočítej příspěvky jednotlivých úrovní:**
   - Přímé: 12 bloků (standardně)
   - Jednonásobný nepřímý: R bloků (1 blok s R ukazateli → R datových bloků)
   - Dvojnásobný nepřímý: R^2 bloků (1 blok → R bloků → R^2 datových bloků)
   - Trojnásobný nepřímý: R^3 bloků

5. **Sečti celkový počet adresovatelných bloků:**

   ```text
   N_bloků = 12 + R + R^2 + R^3
   ```

6. **Vypočítej maximální velikost souboru:**

   ```text
   max_soubor = N_bloků * velikost_bloku
   ```

   Výsledek převeď na vhodnou jednotku (TiB, GiB...).

7. **Pokud se ptají na maximální velikost FS** (ne souboru): maximální počet bloků v FS je omezen délkou adresy, nikoliv strukturou i-nodu. Max bloků = 2^(bity_adresy), max velikost FS = 2^(bity_adresy) * velikost_bloku.

8. **Zkontroluj, zda R^3 >> 12 + R + R^2.** Při velkém R dominuje trojnásobný nepřímý odkaz, ostatní jsou zanedbatelné. Přesné číslo ale vždy spočítej.

### B. Výpočet kapacit FAT

1. **Přečti zadání:** zapiš si velikost clusteru a počet bitů adresy.

2. **Maximální velikost souboru:**

   ```text
   max_soubor_FAT = 2^(bity_adresy) * velikost_clusteru
   ```

   Příklad: 28 b adresa, cluster 16 KiB → 2^28 * 2^14 B = 2^42 B = 4 TiB

3. **Pokud se ptají na velikost FAT tabulky pro danou oblast:**
   - Spočítej počet clusterů: kapacita_oblasti / velikost_clusteru
   - Zaokrouhli délku adresy na celé bajty: ceil(bity_adresy / 8)
   - Velikost FAT = počet_clusterů * bajty_na_adresu

4. **Pozor na zaokrouhlení adresy:** 28 b → 4 B (ne 3,5 B). 12 b → 2 B. Vždy ceil.

5. **FAT32 omezení:** přestože adresa FAT32 má 32 b, fakticky se používá jen 28 b (4 b jsou rezervovány). Pokud zadání říká 28 b, je to FAT32 v reálném světě.

### C. Srovnání volného prostoru (bitmapa vs. seznam)

1. **Bitmapa:** každý blok FS má 1 bit → celkem B bitů.

2. **Zřetězený seznam:** každý **volný** blok drží adresu dalšího volného bloku → celkem F * D bitů, kde F je počet volných bloků a D je délka adresy v bitech.

3. **Podmínka, kdy je seznam menší:**

   ```text
   F * D < B
   ```

   Přičemž B a D jsou z parametrů FS, F závisí na obsazenosti.

4. **Interpretace:** zřetězený seznam je výhodný, pokud je disk **téměř plný** (F je malé). Pokud je disk téměř prázdný (F blízké B), bitmapa je menší.

### D. Trasování FS operací

Tato část je nejpracnější a vyžaduje systematický přístup.

**Příprava:**

1. **Nakresli si obě cesty** (zdroj i cíl) jako seznam komponent oddělených `/`. Každá komponenta je buď adresář, nebo soubor.
2. **Zkontroluj konfiguraci:** je FS s `atime` nebo `noatime`? FAT32 atime ignoruje vždy. `noatime` znamená, že čtení souboru/adresáře **nezapisuje** i-node (čas přístupu se neaktualizuje).
3. **Přečti, co je v paměti:** zadání obvykle říká, co je předem načteno (superblock, i-node kořene, nebo nic). To, co je načteno, se nepočítá do operací čtení.

**Obecné pravidlo pro procházení cesty (platí pro všechny operace):**

Pro každý adresář v cestě (od kořene po předposlední komponentu):
- Načti i-node tohoto adresáře (pokud ještě není v paměti)
- Načti datový blok (obsah) tohoto adresáře (prohledání záznamu s názvem dalšího prvku)

Pro terminální prvek (soubor nebo cílový adresář):
- Načti jeho i-node

**mv v rámci téhož FS (krok za krokem):**

1. Projdi celou **zdrojovou cestu** (všechny adresáře + i-node souboru) — čtení i-nodů a datových bloků adresářů.
2. Projdi celou **cílovou cestu** (všechny adresáře). Pokud se `/` nebo jiný adresář opakuje, nepočítej znovu (je v paměti). Cílový soubor (přesouvaný) **se nečte** — přepisuje se záznam.
3. **Zapiš:** datový blok a i-node zdrojového adresáře (odebrání záznamu, aktualizace mtime). Datový blok a i-node cílového adresáře (přidání záznamu, mtime).
4. **Alokace: žádná.** mv v rámci téhož FS je jen přepojení odkazu v adresáři — i-node souboru se nemění (jen dereference), datové bloky souboru se nedotýkají.
5. **Pozor na noatime:** pokud je FS s `noatime`, čtení adresářů nezapisuje jejich i-node (čas přístupu se nemění → i-node se nezapisuje jen kvůli čtení).

**ln (hard link, krok za krokem):**

1. Projdi **zdrojovou cestu** — načti i-nody a datové bloky adresářů, načti i-node souboru.
2. Projdi **cílovou cestu** (adresáře) — načti i-nody a datové bloky adresářů.
3. **Zapiš:** i-node souboru (inkrementace čítače pevných linků). Datový blok a i-node cílového adresáře (přidání záznamu).
4. **Alokace:** žádná (hard link nealokuje nový i-node, jen zvyšuje čítač existujícího).

**ln -s (symbolický link, krok za krokem):**

1. Projdi **cílovou cestu** (adresáře kde bude link) — načti i-nody a datové bloky adresářů.
2. **Zdrojová cesta se nečte** — symbolický link se nestará o to, zda cíl existuje.
3. **Zapiš:** nový i-node pro link (alokace). Datový blok linku (cílová cesta jako řetězec) — pokud ji FS nezapíše přímo do i-nodu. Datový blok a i-node cílového adresáře (přidání záznamu).
4. **Alokace:** 1 i-node + (obvykle) 1 datový blok.

**rm (krok za krokem):**

1. Projdi **celou cestu** — načti i-nody a datové bloky adresářů, načti i-node souboru.
2. **Zapiš:** datový blok a i-node posledního adresáře (odebrání záznamu, mtime). I-node souboru (dekrementace čítače; pokud = 0, uvolni).
3. **Uvolnění:** i-node souboru + všechny datové bloky souboru + bloky s nepřímými ukazateli. Každé uvolnění se počítá zvlášť.
4. U velkého souboru pamatuj, že se uvolňují i bloky **s ukazateli** (jednonásobný, dvojnásobný, trojnásobný nepřímý blok), nejen datové bloky.

**cp (krok za krokem):**

1. Projdi **zdrojovou cestu** — načti i-nody a datové bloky adresářů, načti i-node zdrojového souboru.
2. Načti **datové bloky zdrojového souboru** (všechna data).
3. Projdi **cílovou cestu** (adresáře) — načti i-nody a datové bloky adresářů.
4. **Zapiš:** nový i-node pro kopii (alokace). Datové bloky kopie (alokace + zápis). Datový blok a i-node cílového adresáře (přidání záznamu).
5. **Alokace:** 1 i-node + počet datových bloků souboru.

---

## Vzorové zadání

!!! example "Zadání"
    **A) UFS.** UFS pracuje s i-nody, které mají 12 přímých odkazů a po jednom jednonásobném, dvojnásobném a trojnásobném nepřímém odkazu. Velikost datového bloku 8 KiB, odkazy na blok jsou 64bitové. Jaká je maximální velikost souboru?

    **B) FAT.** FAT pracuje s clustery 16 KiB, odkaz na cluster je 28bitový. (1) Jaká je maximální velikost souboru? (2) Jaká je velikost FAT tabulky pro oblast 32 GiB?

    **C) Volné objekty.** FS má B datových bloků, z toho F volných, adresa bloku D bitů. Za jaké podmínky zabírá zřetězený seznam volných bloků méně paměti než bitmapa?

    **D) FS operace.** UFS, blok 16 KiB, připojeno s `noatime`. Provede se:

    ```text
    mv /usr/boot/lib/local/dev/php.ini /var/boot/src/home/include/test.cpp
    ```

    Přesun je v rámci téhož UFS. Kolik i-nodů a datových bloků se načte/zapíše? Kolik alokací/uvolnění?

    *UFS: 2010, 2011, 2014, 2019. FAT: 2011, 2012. Volné objekty: 2010, 2011. FS operace: každý termín od 2014.*

---

## Řešení vzorového zadání

??? success "Ukázat řešení"

    ### A) UFS — maximální velikost souboru

    **Krok 1: Spočítej R**

    ```text
    R = 8192 B * 8 / 64 = 65536 / 64 = 1024
    ```

    **Krok 2: Příspěvky jednotlivých úrovní**

    ```text
    přímé:                   12
    jednonásobný nepřímý:  1024                           =       1 024
    dvojnásobný nepřímý:   1024^2                         =   1 048 576
    trojnásobný nepřímý:   1024^3                         = 1 073 741 824
                           ———————————————————————————————
    celkem bloků:                                         = 1 074 791 436
    ```

    **Krok 3: Maximální velikost souboru**

    ```text
    1 074 791 436 * 8192 B = 8 804 505 763 ...B ≈ 8.8 TiB
    ```

    Dominantní složka je trojnásobný nepřímý odkaz (1024^3 = 1,07 × 10^9 bloků), ostatní jsou zanedbatelné.

    ### B) FAT

    **Krok 1: Maximální velikost souboru**

    ```text
    2^28 * 16 KiB = 2^28 * 2^14 B = 2^42 B = 4 TiB
    ```

    **Krok 2: Velikost FAT tabulky pro oblast 32 GiB**

    Počet clusterů:
    ```text
    32 GiB / 16 KiB = 2^35 B / 2^14 B = 2^21 clusterů
    ```

    Bajty na adresu (28 b → zaokrouhlení):
    ```text
    ceil(28 / 8) = ceil(3,5) = 4 B
    ```

    Velikost FAT:
    ```text
    2^21 * 4 B = 2^23 B = 8 MiB
    ```

    ### C) Volné objekty

    - Bitmapa: **B bitů** (jeden bit na každý blok, bez ohledu na obsazenost)
    - Zřetězený seznam: **F * D bitů** (každý volný blok drží D-bitovou adresu dalšího)

    Zřetězený seznam je menší, pokud: **F * D < B**

    Například: B = 10^9 bloků, D = 32 b → seznam je menší pokud F < B / D = 10^9 / 32 ≈ 3,1 × 10^7 volných bloků. Tj. disk musí být obsazený z více než 96,9 %.

    ### D) FS operace — `mv` v rámci téhož UFS (noatime)

    **Příprava:** Rozpiš obě cesty:

    ```text
    zdroj:  /  usr  boot  lib  local  dev  php.ini
    cíl:    /  var  boot  src  home  include  test.cpp  (test.cpp se tvoří)
    ```

    `noatime` — čtení adresářů nezapisuje jejich i-node.

    **Načtené i-nody (čtení):**

    Procházíme zdrojovou cestu a cílovou cestu. Kořen `/` je společný — počítáme jen jednou. Boot adresář se na obou cestách jmenuje stejně, ale jde o **různé adresáře** (mají odlišného rodiče), takže se počítají zvlášť.

    | Adresář/soubor | Patří do |
    |---|---|
    | / (kořen) | obě cesty — 1× |
    | usr | zdrojová cesta |
    | boot (pod usr) | zdrojová cesta |
    | lib | zdrojová cesta |
    | local | zdrojová cesta |
    | dev | zdrojová cesta |
    | php.ini (i-node souboru) | zdrojová cesta |
    | var | cílová cesta |
    | boot (pod var) | cílová cesta |
    | src | cílová cesta |
    | home | cílová cesta |
    | include | cílová cesta |

    Celkem: **11 načtených i-nodů**

    **Načtené datové bloky (obsah adresářů):**

    Pro každý adresář v obou cestách se čte jeho obsah (prohledávání záznamu). Soubor `php.ini` se nečte (mv v rámci FS data nekopíruje).

    | Datový blok adresáře | Patří do |
    |---|---|
    | obsah / | společný — 1× |
    | obsah usr | zdrojová cesta |
    | obsah boot (pod usr) | zdrojová cesta |
    | obsah lib | zdrojová cesta |
    | obsah local | zdrojová cesta |
    | obsah dev | zdrojová cesta |
    | obsah var | cílová cesta |
    | obsah boot (pod var) | cílová cesta |
    | obsah src | cílová cesta |
    | obsah home | cílová cesta |
    | obsah include | cílová cesta |

    Celkem: **11 načtených datových bloků**

    **Zapsané i-nody:**

    - i-node `dev` (mtime — odebrání záznamu pro php.ini)
    - i-node `include` (mtime — přidání záznamu pro test.cpp)

    Celkem: **2 zapsané i-nody**

    **Zapsané datové bloky:**

    - obsah `dev` (odebrání záznamu php.ini)
    - obsah `include` (přidání záznamu test.cpp)

    Celkem: **2 zapsané datové bloky**

    **Alokace a uvolnění:**

    `mv` v rámci téhož FS přesouvá jen záznam v adresáři. I-node souboru a jeho datové bloky zůstávají nedotčeny. **0 alokací, 0 uvolnění.**

    !!! note "mv na jiný FS"
        Kdyby `/usr` a `/var` byly na různých FS (různé diskové oddíly), `mv` by se choval jako `cp` + `rm`. Kopírovaly by se **všechny datové bloky souboru php.ini**, alokoval by se nový i-node + datové bloky na cílovém FS, a zdrojový i-node + datové bloky by se uvolnily. Počet operací by byl řádově vyšší.

---

## Další procvičení

### Varianta 1: UFS s menším blokem a FAT

!!! example "Zadání"
    **A) UFS.** I-node má 12 přímých odkazů, jednonásobný, dvojnásobný a trojnásobný nepřímý. Velikost bloku 4 KiB, odkaz 32bitový. Jaká je maximální velikost souboru?

    **B) FAT.** Cluster 4 KiB, adresa 32bitová (fakticky 28bitová jako FAT32). (1) Max velikost souboru? (2) Velikost FAT tabulky pro oblast 2 TiB?

??? success "Ukázat řešení"
    **A) UFS, blok 4 KiB, odkaz 32 b:**

    ```text
    R = 4096 * 8 / 32 = 32768 / 32 = 1024
    N_bloků = 12 + 1024 + 1024^2 + 1024^3 = 1 074 791 436
    max_soubor = 1 074 791 436 * 4096 B = 4 TiB (přibližně)
    ```

    Přesně: 1 074 791 436 * 4096 = 4 402 341 969 920 B ≈ 4,004 TiB

    !!! warning "Pozor na velikost odkazu"
        Odkaz 32bitový s blokem 4 KiB a odkaz 64bitový s blokem 8 KiB dávají stejné R = 1024. Výsledný počet bloků je stejný, ale maximální velikost souboru je 2× menší (blok je 2× menší). Nezaměňuj R se samotnou velikostí souboru — vždy dosaď správnou velikost bloku.

    **B) FAT32 (28bitová adresa), cluster 4 KiB:**

    Max soubor:
    ```text
    2^28 * 4 KiB = 2^28 * 2^12 B = 2^40 B = 1 TiB
    ```

    Velikost FAT pro oblast 2 TiB:
    ```text
    počet clusterů = 2 TiB / 4 KiB = 2^41 / 2^12 = 2^29 clusterů
    ceil(28/8) = 4 B na adresu
    velikost FAT = 2^29 * 4 B = 2^31 B = 2 GiB
    ```

    FAT tabulka 2 GiB se ale do RAM vejde jen obtížně — proto FAT32 obvykle limituje velikost oblasti na 2 TiB.

### Varianta 2: FS operace — hard link

!!! example "Zadání"
    UFS, blok 4 KiB, `noatime`. V paměti je načten pouze superblock. Provede se:

    ```text
    ln /usr/src/games/src/https.conf /var/log/etc/bin/etc/doc/libpcre.so
    ```

    Kolik i-nodů se načte? Kolik zapíše? Kolik datových bloků se načte? Kolik zapíše? Kolik alokací?

??? success "Ukázat řešení"
    Zdrojová cesta: `/` `usr` `src` `games` `src` (jiný než první src!) `https.conf`
    Cílová cesta: `/` `var` `log` `etc` `bin` `etc` (jiný!) `doc` `libpcre.so` (nový hard link)

    **Hard link nevyžaduje přístup ke zdrojovému souboru jako k datům** — musíme jen načíst jeho i-node a inkrementovat čítač linků.

    **Načtené i-nody:**

    Zdrojová cesta (adresáře + soubor):
    - / (kořen), usr, src, games, src, https.conf = 6 i-nodů

    Cílová cesta (adresáře, bez /):
    - var, log, etc, bin, etc, doc = 6 i-nodů

    Celkem: **12 načtených i-nodů**

    **Načtené datové bloky (obsah adresářů):**

    Zdrojová cesta: /, usr, src, games, src = 5 datových bloků
    Cílová cesta (bez /): var, log, etc, bin, etc, doc = 6 datových bloků

    Celkem: **11 načtených datových bloků**

    **Zapsané i-nody:**

    - i-node `https.conf` (inkrementace čítače pevných linků, mtime)
    - i-node `doc` (mtime — přidání záznamu libpcre.so)

    Celkem: **2 zapsané i-nody**

    **Zapsané datové bloky:**

    - obsah adresáře `doc` (přidání záznamu libpcre.so)

    Celkem: **1 zapsaný datový blok**

    **Alokace:**

    Hard link nealokuje žádný nový i-node ani datový blok. **0 alokací.**

---

## Varianty a chytáky

- **mv v rámci téhož FS vs. mezi různými FS.** Zkontroluj mountpoint obou cest. Pokud jsou na různých diskových oddílech (jiných FS), `mv` = `cp` + `rm` s miliony operací u velkého souboru.
- **noatime vs. atime.** Při `atime` každé čtení adresáře aktualizuje jeho i-node → přibývají zápisy i-nodů adresářů na celé cestě. Při `noatime` se i-node adresáře zapisuje jen při skutečné modifikaci obsahu.
- **FAT32 atime.** FAT32 čas přístupu vůbec nepoužívá — atime/noatime parametry nemají vliv.
- **`/` se počítá jednou.** Kořenový adresář je sdílen oběma cestami — jeho i-node a datový blok se načtou jen jednou i když je na obou cestách.
- **Stejné jméno adresáře ≠ stejný adresář.** `/usr/boot` a `/var/boot` jsou různé adresáře s různými i-nody i datovými bloky — počítají se zvlášť.
- **Zaokrouhlení FAT adresy.** 28 b → 4 B (ne 3,5 B). 12 b → 2 B. Vždy ceil(bity/8).
- **hard link vs. symbolický link.** Hard link: žádný nový i-node, jen ++čítač na existujícím. Symbolický link: nový i-node + datový blok s cílovou cestou. Hard link nelze přes hranice FS; symbolický lze.
- **rm velkého souboru.** Uvolňují se nejen datové bloky s daty, ale i bloky s nepřímými ukazateli (jednonásobný = 1 blok, dvojnásobný = 1+R bloků, trojnásobný = 1+R+R^2 bloků). Každé uvolnění se počítá zvlášť.
- **i-node má 128 B.** Pokud zadání ptá na počet i-nodů v bloku nebo na velikost tabulky i-nodů.
- **Počet odkazů v bloku závisí na velikosti bloku i délce adresy.** R = B_blok * 8 / b_odkaz. Změna délky adresy ze 32 b na 64 b sníží R na polovinu (při stejném bloku).

---

## Časté chyby

- **Záměna R a počtu bloků.** R je počet odkazů v jednom blokovém záznamu, ne počet adresovatelných bloků.
- **Zapomínání na bloky s ukazateli.** Při výpočtu max velikosti souboru se NEZAPOČÍTÁVAJÍ bloky s nepřímými ukazateli — ty jsou metadata. Velikost souboru = N_datových_bloků * velikost_bloku.
- **Špatná jednotka odkazu.** Pokud je odkaz 64bitový, R = blok_B * 8 / 64. Pokud chybně použiješ 32, dostaneš 2× větší R a špatný výsledek.
- **mv vs. cp při výpočtu operací.** mv v rámci FS nekopíruje data → 0 čtení datových bloků souboru, 0 alokací. cp vždy kopíruje → N čtení + N zápisů + alokace.
- **Počítání adresy FAT jako celých bajtů.** 28 b adresy → 4 B, ne 3,5 B. Vždy ceil.
- **Zapomínání na i-node souboru při mv.** I-node souboru se načte (musíme ověřit, že jde o soubor a získat metadata), ale nezapisuje se (mv v rámci FS mění jen záznamy v adresářích).
- **Nepočítání i-nodu cílového adresáře při zápisu.** Přidání záznamu do adresáře = zápis datového bloku adresáře + zápis i-nodu adresáře (mtime). Obojí.
- **Záměna noatime a FAT.** noatime platí jen pro FS, kde se atime normálně používá (UFS, ext). FAT atime nepoužívá vůbec bez ohledu na parametry připojení.

---

## Související

- [Skripta: Datová úložiště a souborové systémy](../../skripta/07-souborove-systemy.md)
- [Teoretické otázky (true/false)](../teorie-truefalse.md)
- [Praktické příklady — přehled všech typů úloh](index.md)
