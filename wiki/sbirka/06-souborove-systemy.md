# Systémy souborů – i-node

??? abstract "Obsah stránky"

    [TOC]

---

## Společná konfigurace systémů souborů

Na UNIXovém systému máme připojeny následující systémy souborů:

| Bod připojení | Disk      | Typ systému souborů | Parametry připojení  |
|---------------|-----------|---------------------|----------------------|
| /             | /dev/sda1 | UFS                 | read/write, noatime  |
| /home         | /dev/sda2 | UFS                 | read/write, noatime  |
| /fat1         | /dev/sdb1 | FAT32               | read/write           |
| /fat2         | /dev/sdc1 | FAT32               | read/write           |

- Parametr **atime** znamená, že se u souborů/adresářů aktualizuje čas přístupu při každém přístupu.
- Parametr **noatime** znamená, že se u souborů/adresářů neaktualizuje čas přístupu.
- Systém souborů FAT32 nepoužívá informaci o přístupu, tedy atribut atime/noatime není použit.
- Při výpočtu používáme jednotky KiB, MiB, …, platí: 1 KiB = 1024 B, 1 MiB = 1024 KiB, …

---

## Úloha 1 — cp, UFS blok 2 KiB, 32bitové odkazy

!!! example "Zadání"
    Systém souborů UFS pracuje s i-nody, které mají 12 odkazů přímých a po jednom jednonásobném, dvojnásobném a trojnásobném nepřímém odkazu na datové bloky. Velikost datového bloku je 2 KiB, odkazy na datový blok jsou 32-bitové. Atributy i-nodu jsou: typ souboru, velikost souboru, čítač pevných linků, přístupová práva, vlastník a skupina, čas modifikace, čas přístupu, symbolický link se vždy zapisuje do datového bloku. Informace o volných objektech UFS (i-nodech a blocích) jsou uložené v bitové mapě na disku, která se při připojení systému souborů načetla do paměti.

    Systém souborů FAT32 pracuje s datovými bloky (clustery) o velikosti 2 KiB a odkazy na clustery jsou 32-bitové.

    Předpokládejte, že obsah adresáře nepřesáhne velikost bloku 2 KiB. Dále předpokládejte, že v paměti jsou načtené pouze **superbloky/boot sektory** jednotlivých připojených disků. Dále pro jednoduchost předpokládáme, že operace uspějí (cesty existují, soubory lze číst/zapisovat, je dostatek místa, všimněte si, že operace provádíme pod uživatelem root, tedy nemáme omezená na přístupová práva). Pro zpracovávaný soubor víte, že zobrazení by vypadalo takto:

    ```
    # ll /var/include/dev/share/boot/boot
    ...
    -rw-rw-rw- 1 root root 309788851 Feb 4 12:57 ntpd.conf
    ...
    ```

    V takové konfiguraci se provede následující příkaz shellu:

    ```
    # cp /var/include/dev/share/boot/boot/ntpd.conf /home/log/boot/games/ld.so.conf
    ```

    Uvažujte pouze efekt tohoto příkazu (tedy neuvažujte režii spojenou s vlastním natažením tohoto příkazu do paměti).

    1. Kolik i-nodů se musí načíst? (celé desítkové číslo)
    2. Kolik i-nodů se musí zapsat? (celé desítkové číslo)
    3. Kolik datových bloků se musí načíst? (celé desítkové číslo)
    4. Kolik datových bloků se musí zapsat? (celé desítkové číslo)
    5. Kolik operací alokování/uvolňování bloků a i-nodů musí být provedeno? Každou operaci alokace/uvolnění bloku/i-node započtěte zvlášť.

??? success "Řešení"

    ### 1. Kolik i-nodů se musí načíst?

    Procházíme zdrojovou cestu (všechny adresáře + i-node souboru) a cílovou cestu (adresáře). Kořen `/` je společný — počítáme jej jednou. Adresář `/home` je na jiném disku (sda2), ale stále UFS s noatime.

    ```
    R i-node /
    R content /
    R i-node /var
    R content /var
    R i-node /var/include
    R content /var/include
    R i-node /var/include/dev
    R content /var/include/dev
    R i-node /var/include/dev/share
    R content /var/include/dev/share
    R i-node /var/include/dev/share/boot
    R content /var/include/dev/share/boot
    R i-node /var/include/dev/share/boot/boot
    R content /var/include/dev/share/boot/boot
    R i-node /var/include/dev/share/boot/boot/ntpd.conf
    R i-node /home
    R content /home
    R i-node /home/log
    R content /home/log
    R i-node /home/log/boot
    R content /home/log/boot
    R i-node /home/log/boot/games
    R content /home/log/boot/games
    Alloc /dev/sda2 i-node for /home/log/boot/games/ld.so.conf
    W i-node /home/log/boot/games/ld.so.conf
    ```

    **Musí se načíst 12 i-nodů.**

    ### 2. Kolik i-nodů se musí zapsat?

    Jeden i-node se přepíše kvůli aktualizaci hodnoty mtime adresáře **games** a jeden se vytvoří za soubor **ld.so.conf**.

    ```
    W i-node /home/log/boot/games/ld.so.conf
    W i-node /home/log/boot/games  (mtime)
    ```

    **Musí se zapsat 2 i-nody.**

    ### 3. Kolik datových bloků se musí načíst?

    Nejprve si musíme spočítat, kolik datových bloků načteme pro nalezení adresářů z argumentu příkazu `cp`. Za první složku načteme 7 datových bloků:

    ```
    R content /
    R content /var
    R content /var/include
    R content /var/include/dev
    R content /var/include/dev/share
    R content /var/include/dev/share/boot
    R content /var/include/dev/share/boot/boot
    ```

    Za druhou načteme 4 bloky:

    ```
    R content /home
    R content /home/log
    R content /home/log/boot
    R content /home/log/boot/games
    ```

    Zde je důležité si všimnout, že druhá posloupnost nezačíná kořenovou složkou `/`, ale složkou `/home`. To je proto, že daný datový blok si pamatujeme a nenačítáme ho dvakrát.

    Dalším krokem je výpočet počtu přímých adres, které se vejdou do jednoho nepřímého odkazu. Velikost datového bloku převedeme na bity:

    ```
    2 KiB = 2 * 2^10 B = 2^11 B = 8 * 2^11 b = 2^3 * 2^11 b = 2^14 b
    ```

    Odkazy na clustery mají 32 bitů, do jednoho bloku se nám jich tedy vejde 2^14 / 32 = 2^14 / 2^5 = 2^9. Víme, že celková velikost souboru je 309788851 B, a z toho jsme schopni spočítat, že soubor zabere ceil(309788851 B / 2 KiB) = ceil(309788851 / 2^11) = 151265 bloků o velikosti 2 KiB.

    Nyní je potřeba spočítat, kolik potřebujeme použít nepřímých bloků. I-node obsahuje 12 přímých odkazů na datové bloky, ty použijeme jako první. Zbývá nám tedy zapsat 151265 - 12 = 151253 datových bloků. Jak jsme si již spočítali, jeden nepřímý odkaz první úrovně dokáže pojmout 2^9 přímých odkazů, použijeme jej tedy a nyní nám zbývá zapsat 151253 - 2^9 = 150741 datových bloků. Na jejich zapsání využijeme jeden nepřímý odkaz druhé úrovně; analogicky jako v předchozím případě tento odkaz může adresovat 2^9 nepřímých odkazů první úrovně. Nyní je třeba zjistit, kolik z nich musíme reálně využít. To spočítáme následovně: ceil(150741 / 2^9) = 295. Prvních 294 zaplníme úplně, takže nám zbývá 150741 - 294 * 2^9 = 213 datových bloků, které se nám vejdou do posledního 295. nepřímého odkazu první úrovně.

    Pro zjištění celkového počtu datových bloků je potřeba sečíst samotná data souboru, datové bloky použité pro nepřímou adresaci a datové bloky načtené při procházení adresářů (R content na adresářích):

    ```
    151265 + 1 + 1 + 295 + 4 + 7 = 151573
    ```

    **Musí se načíst 151573 datových bloků.**

    ### 4. Kolik datových bloků se musí zapsat?

    Už víme, že soubor zabere ceil(309788851 / 2^11) = 151265 bloků o velikosti 2 KiB. Také navíc víme, že za nepřímou adresaci musíme zapsat 1 + 1 + 295 = 297 bloků. Další zápis vypotřebujeme na aktualizaci obsahu složky **games**.

    ```
    W content /home/log/boot/games
    W content /home/log/boot/games/ld.so.conf  (151265 file data + 297 indirect addr blocks)
    ```

    ```
    151265 + 297 + 1 = 151563
    ```

    **Musí se zapsat 151563 datových bloků.**

    ### 5. Kolik operací alokování/uvolňování bloků a i-nodů musí být provedeno?

    Za vytvoření souboru **ld.so.conf** se musí alokovat jeden i-node a jak už víme, ještě musíme alokovat 151562 datových bloků (151265 dat + 297 nepřímých adresovacích bloků).

    ```
    Alloc /dev/sda2 i-node for /home/log/boot/games/ld.so.conf
    Alloc /dev/sda2 blocks  (151265 file data + 297 indirect addr blocks)
    ```

    ```
    151265 + 297 + 1 = 151563
    ```

    **Musí být provedeno 151563 operací.**

---

## Úloha 2 — cp, UFS blok 16 KiB, 64bitové odkazy

!!! example "Zadání"
    Systém souborů UFS pracuje s i-nody, které mají 12 odkazů přímých a po jednom jednonásobném, dvojnásobném a trojnásobném nepřímém odkazu na datové bloky. Velikost datového bloku je 16 KiB, odkazy na datový blok jsou 64-bitové. Atributy i-nodu jsou: typ souboru, velikost souboru, čítač pevných linků, přístupová práva, vlastník a skupina, čas modifikace, čas přístupu, symbolický link se vždy zapisuje do datového bloku. Informace o volných objektech UFS (i-nodech a blocích) jsou uložené v bitové mapě na disku, která se při připojení systému souborů načetla do paměti.

    Systém souborů FAT32 pracuje s datovými bloky (clustery) o velikosti 16 KiB a odkazy na clustery jsou 64-bitové.

    Předpokládejte, že obsah adresáře nepřesáhne velikost bloku 16 KiB. Dále předpokládejte, že v paměti jsou načtené pouze **superbloky/boot sektory** jednotlivých připojených disků. Pro zpracovávaný soubor víte, že zobrazení by vypadalo takto:

    ```
    # ll /var/share/etc/doc/share/local
    ...
    -rw-rw-rw- 1 root root 33869614059 Jul 28 05:21 run.sh
    ...
    ```

    V takové konfiguraci se provede následující příkaz shellu:

    ```
    # cp /var/share/etc/doc/share/local/run.sh /home/share/log/doc/libxml2.so.6
    ```

    Uvažujte pouze efekt tohoto příkazu (tedy neuvažujte režii spojenou s vlastním natažením tohoto příkazu do paměti).

    1. Kolik i-nodů se musí načíst? (celé desítkové číslo)
    2. Kolik i-nodů se musí zapsat? (celé desítkové číslo)
    3. Kolik datových bloků se musí načíst? (celé desítkové číslo)
    4. Kolik datových bloků se musí zapsat? (celé desítkové číslo)
    5. Kolik operací alokování/uvolňování bloků a i-nodů musí být provedeno? Každou operaci alokace/uvolnění bloku/i-node započtěte zvlášť.

??? success "Řešení"

    ### 1. Kolik i-nodů se musí načíst?

    ```
    R i-node /
    R i-node /var
    R i-node /var/share
    R i-node /var/share/etc
    R i-node /var/share/etc/doc
    R i-node /var/share/etc/doc/share
    R i-node /var/share/etc/doc/share/local
    R i-node /var/share/etc/doc/share/local/run.sh
    R i-node /home
    R i-node /home/share
    R i-node /home/share/log
    R i-node /home/share/log/doc
    ```

    **Musí se načíst 12 i-nodů.**

    ### 2. Kolik i-nodů se musí zapsat?

    ```
    W i-node /home/share/log/doc/libxml2.so.6
    W i-node /home/share/log/doc  (mtime)
    ```

    **Musí se zapsat 2 i-nody.**

    ### 3. Kolik datových bloků se musí načíst?

    Za první složku načteme 7 datových bloků a za druhou 4 datové bloky.

    ```
    R content /
    R content /var
    R content /var/share
    R content /var/share/etc
    R content /var/share/etc/doc
    R content /var/share/etc/doc/share
    R content /var/share/etc/doc/share/local
    ```

    ```
    R content /home
    R content /home/share
    R content /home/share/log
    R content /home/share/log/doc
    ```

    Velikost datového bloku převedeme na bity:

    ```
    16 KiB = 2^4 * 2^10 B = 2^14 B = 8 * 2^14 b = 2^3 * 2^14 b = 2^17 b
    ```

    Odkazy na clustery mají 64 bitů, do jednoho bloku se nám jich tedy vejde 2^17 / 64 = 2^17 / 2^6 = 2^11. Víme, že celková velikost souboru je 33869614059 B, a z toho jsme schopni spočítat, že soubor zabere ceil(33869614059 / 2^14) = 2067238 bloků o velikosti 16 KiB.

    I-node obsahuje 12 přímých odkazů na datové bloky, ty použijeme jako první. Zbývá nám tedy zapsat 2067238 - 12 = 2067226 datových bloků. Jeden nepřímý odkaz první úrovně dokáže pojmout 2^11 přímých odkazů, použijeme jej tedy a nyní nám zbývá zapsat 2067226 - 2^11 = 2065178 datových bloků. Jeden nepřímý odkaz druhé úrovně může adresovat 2^11 nepřímých odkazů první úrovně. Nyní je třeba zjistit, kolik z nich musíme reálně využít: ceil(2065178 / 2^11) = 1009.

    ```
    2067238 + 1 + 1 + 1009 + 4 + 7 = 2068260
    ```

    **Musí se načíst 2068260 datových bloků.**

    ### 4. Kolik datových bloků se musí zapsat?

    Už víme, že soubor zabere 2067238 bloků o velikosti 16 KiB. Také navíc víme, že za nepřímou adresaci musíme zapsat 1011 bloků. Další zápis vypotřebujeme na aktualizaci obsahu složky **doc**.

    ```
    2067238 + 1011 + 1 = 2068250
    ```

    **Musí se zapsat 2068250 datových bloků.**

    ### 5. Kolik operací alokování/uvolňování bloků a i-nodů musí být provedeno?

    ```
    2067238 + 1011 + 1 = 2068250
    ```

    **Musí být provedeno 2068250 operací.**

---

## Úloha 3 — mv v rámci jednoho FS, UFS blok 2 KiB, 64bitové odkazy

!!! example "Zadání"
    Systém souborů UFS pracuje s i-nody, které mají 12 odkazů přímých a po jednom jednonásobném, dvojnásobném a trojnásobném nepřímém odkazu na datové bloky. Velikost datového bloku je 2 KiB, odkazy na datový blok jsou 64-bitové. Atributy i-nodu jsou: typ souboru, velikost souboru, čítač pevných linků, přístupová práva, vlastník a skupina, čas modifikace, čas přístupu, symbolický link se vždy zapisuje do datového bloku. Informace o volných objektech UFS (i-nodech a blocích) jsou uložené v bitové mapě na disku, která se při připojení systému souborů načetla do paměti.

    Systém souborů FAT32 pracuje s datovými bloky (clustery) o velikosti 2 KiB a odkazy na clustery jsou 64-bitové.

    Předpokládejte, že obsah adresáře nepřesáhne velikost bloku 2 KiB. Dále předpokládejte, že v paměti jsou načtené pouze **superbloky/boot sektory** jednotlivých připojených disků. Pro zpracovávaný soubor víte, že zobrazení by vypadalo takto:

    ```
    # ll /usr/log/games/dev/src
    ...
    -rw-rw-rw- 1 root root 3395426 Jun 15 04:49 index.php
    ...
    ```

    V takové konfiguraci se provede následující příkaz shellu:

    ```
    # mv /usr/log/games/dev/src/index.php /var/local/games/home/index.html
    ```

    Uvažujte pouze efekt tohoto příkazu (tedy neuvažujte režii spojenou s vlastním natažením tohoto příkazu do paměti).

    1. Kolik i-nodů se musí načíst? (celé desítkové číslo)
    2. Kolik i-nodů se musí zapsat? (celé desítkové číslo)
    3. Kolik datových bloků se musí načíst? (celé desítkové číslo)
    4. Kolik datových bloků se musí zapsat? (celé desítkové číslo)
    5. Kolik operací alokování/uvolňování bloků a i-nodů musí být provedeno? Každou operaci alokace/uvolnění bloku/i-node započtěte zvlášť.

??? success "Řešení"

    Jedná se o přesun v rámci jednoho systému souborů (obě cesty leží na sda1, UFS, noatime), proto stačí jen přepsat záznamy v adresářích — data souboru se nekopírují.

    ### 1. Kolik i-nodů se musí načíst?

    ```
    R i-node /
    R content /
    R i-node /usr
    R content /usr
    R i-node /usr/log
    R content /usr/log
    R i-node /usr/log/games
    R content /usr/log/games
    R i-node /usr/log/games/dev
    R content /usr/log/games/dev
    R i-node /usr/log/games/dev/src
    R content /usr/log/games/dev/src
    remember /usr/log/games/dev/src/index.php i-node number
    R i-node /var
    R content /var
    R i-node /var/local
    R content /var/local
    R i-node /var/local/games
    R content /var/local/games
    R i-node /var/local/games/home
    R content /var/local/games/home
    W content /var/local/games/home
    W i-node /var/local/games/home  (mtime)
    W content /usr/log/games/dev/src
    W i-node /usr/log/games/dev/src  (mtime)
    ```

    **Musí se načíst 10 i-nodů.**

    ### 2. Kolik i-nodů se musí zapsat?

    Jeden i-node se přepíše kvůli aktualizaci hodnoty mtime adresáře **home** a druhý se přepíše kvůli aktualizaci hodnoty mtime adresáře **src**.

    ```
    W i-node /var/local/games/home  (mtime)
    W i-node /usr/log/games/dev/src  (mtime)
    ```

    **Musí se zapsat 2 i-nody.**

    ### 3. Kolik datových bloků se musí načíst?

    Musíme si spočítat, kolik datových bloků načteme pro nalezení adresářů z argumentu příkazu `mv`. Za první složku načteme 6 datových bloků:

    ```
    R content /
    R content /usr
    R content /usr/log
    R content /usr/log/games
    R content /usr/log/games/dev
    R content /usr/log/games/dev/src
    ```

    Za druhou načteme 4 bloky:

    ```
    R content /var
    R content /var/local
    R content /var/local/games
    R content /var/local/games/home
    ```

    Na rozdíl od předešlého příkladu (příkaz `cp`), už žádné další datové bloky nenačítáme. Při použití příkazu `mv` jenom změníme adresář, ve kterém se soubor nachází.

    **Musí se načíst 10 datových bloků.**

    ### 4. Kolik datových bloků se musí zapsat?

    Stačí zapsat 2 datové bloky, které drží informaci o obsahu adresáře. V prvním adresáři **/home** musíme soubor odebrat ze seznamu a v druhém **/src** musíme soubor do seznamu přidat.

    ```
    W content /var/local/games/home
    W content /usr/log/games/dev/src
    ```

    **Musí se načíst 2 datové bloky.**

    ### 5. Kolik operací alokování/uvolňování bloků a i-nodů musí být provedeno?

    Při provedení příkazu `mv` v rámci jednoho adresáře nepotřebujeme vykonat žádné další alokování/uvolňování bloků ani i-nodů, jelikož se jedná pouze o přesun reference na již existující i-node.

    **Nemusí být provedené žádné operace.**

---

## Úloha 4 — mv mezi různými FS, UFS blok 16 KiB, 64bitové odkazy

!!! example "Zadání"
    Systém souborů UFS pracuje s i-nody, které mají 12 odkazů přímých a po jednom jednonásobném, dvojnásobném a trojnásobném nepřímém odkazu na datové bloky. Velikost datového bloku je 16 KiB, odkazy na datový blok jsou 64-bitové. Atributy i-nodu jsou: typ souboru, velikost souboru, čítač pevných linků, přístupová práva, vlastník a skupina, čas modifikace, čas přístupu, symbolický link se vždy zapisuje do datového bloku. Informace o volných objektech UFS (i-nodech a blocích) jsou uložené v bitové mapě na disku, která se při připojení systému souborů načetla do paměti.

    Systém souborů FAT pracuje s datovými bloky (clustery) o velikosti 8 KiB a odkazy na clustery jsou 64-bitové.

    Pro zpracovávaný soubor víte, že zobrazení by vypadalo takto:

    ```
    # ll /var/games/etc/share/share/boot
    ...
    -rw-rw-rw- 1 root root 3395426 Jun 15 04:49 ld.so.conf
    ...
    ```

    V takové konfiguraci se provede následující příkaz shellu:

    ```
    # mv /var/games/etc/share/share/boot/ld.so.conf
       /home/doc/share/local/src/libsml2.so.6
    ```

    Uvažujte pouze efekt tohoto příkazu (tedy neuvažujte režii spojenou s vlastním natažením tohoto příkazu do paměti).

    1. Kolik i-nodů se musí načíst? (celé desítkové číslo)
    2. Kolik i-nodů se musí zapsat? (celé desítkové číslo)
    3. Kolik datových bloků se musí načíst? (celé desítkové číslo)
    4. Kolik datových bloků se musí zapsat? (celé desítkové číslo)
    5. Kolik operací alokování/uvolňování bloků a i-nodů musí být provedeno? Každou operaci alokace/uvolnění bloku/i-node započtěte zvlášť.

??? success "Řešení"

    Na rozdíl od předešlého příkladu se jedná o přesouvání souboru v různých systémech souborů a proto je potřeba překopírovat i i-node (i data) za soubor.

    ### 1. Kolik i-nodů se musí načíst?

    ```
    R i-node /
    R i-node /var
    R i-node /var/games
    R i-node /var/games/etc
    R i-node /var/games/etc/share
    R i-node /var/games/etc/share/share
    R i-node /var/games/etc/share/share/boot
    R i-node /var/games/etc/share/share/boot/ld.so.conf
    R i-node /home
    R i-node /home/doc
    R i-node /home/doc/share
    R i-node /home/doc/share/local
    R i-node /home/doc/share/local/src
    ```

    **Musí se načíst 13 i-nodů.**

    ### 2. Kolik i-nodů se musí zapsat?

    Jeden i-node se přepíše kvůli aktualizaci hodnoty mtime adresáře **/boot**, druhý se přepíše kvůli aktualizaci hodnoty mtime adresáře **/src** a už zbývá jen vytvořit i-node na systému souborů **/home**.

    ```
    W i-node /var/games/etc/share/share/boot  (mtime)
    W i-node /home/doc/share/local/src  (mtime)
    W i-node /home/doc/share/local/src/libsml2.so.6
    ```

    **Musí se zapsat 3 i-nody.**

    ### 3. Kolik datových bloků se musí načíst?

    Za načtení obou cest celkem 12 bloků (7 + 5).

    Načítáme obsah souboru, začneme 12 přímo adresovanými bloky, zbývá nám načíst 3395426 B - 12 * 16 KiB = 3198818 B. Načteme první nepřímo adresovaný blok, dostaneme dostupných 16 KiB / 64 bit = 2048 adres. Z nich nám pro načtení zbývajících 3198818 B stačí ceil(3198818 B / 16 KiB) = 196.

    ```
    12 + 12 + 1 + 196 = 221
    ```

    **Musí se načíst 221 datových bloků.**

    ### 4. Kolik datových bloků se musí zapsat?

    Počet zapsaných bloků za soubor je stejný jako za čtení, poté nám stačí pro oba adresáře změnit jejich obsah (jeden datový blok odebrání, druhý datový blok přidání souboru).

    ```
    2 + 12 + 1 + 196 = 211
    ```

    **Musí se zapsat 211 datových bloků.**

    ### 5. Kolik operací alokování/uvolňování bloků a i-nodů musí být provedeno?

    Jednu sadu datových bloků na prvním disku je třeba celou uvolnit, stejný počet alokovat na druhém disku. Zbývá smazat původní i-node a alokovat nový. Operace změny obsahu adresářů nevyžadují alokaci ani dealokaci.

    ```
    2 * (12 + 1 + 196) + 2 = 420
    ```

    **Musí se provést 420 operací.**

---

## Úloha 5 — ln -s (symbolický link), UFS blok 8 KiB, 64bitové odkazy

!!! example "Zadání"
    Systém souborů UFS pracuje s i-nody, které mají 12 odkazů přímých a po jednom jednonásobném, dvojnásobném a trojnásobném nepřímém odkazu na datové bloky. Velikost datového bloku je 8 KiB, odkazy na datový blok jsou 64-bitové. Atributy i-nodu jsou: typ souboru, velikost souboru, čítač pevných linků, přístupová práva, vlastník a skupina, čas modifikace, čas přístupu, symbolický link se vždy zapisuje do datového bloku. Informace o volných objektech UFS (i-nodech a blocích) jsou uložené v bitové mapě na disku, která se při připojení systému souborů načetla do paměti.

    Systém souborů FAT32 pracuje s datovými bloky (clustery) o velikosti 8 KiB a odkazy na clustery jsou 64-bitové.

    Předpokládejte, že obsah adresáře nepřesáhne velikost bloku 8 KiB. Dále předpokládejte, že v paměti jsou načtené pouze **superbloky/boot sektory** jednotlivých připojených disků. Pro zpracovávaný soubor víte, že zobrazení by vypadalo takto:

    ```
    # ll /home/pavel/2018/osy/cl
    ...
    -rw-rw-rw- 1 root root 56375076079 Aug 12 03:31 f.pdf
    ...
    ```

    V takové konfiguraci se provede následující příkaz shellu:

    ```
    # ln -s /home/pavel/2018/osy/cl/f.pdf /home/pavel/f.link
    ```

    Uvažujte pouze efekt tohoto příkazu (tedy neuvažujte režii spojenou s vlastním natažením tohoto příkazu do paměti).

    1. Kolik i-nodů se musí načíst? (celé desítkové číslo)
    2. Kolik i-nodů se musí zapsat? (celé desítkové číslo)
    3. Kolik datových bloků se musí načíst? (celé desítkové číslo)
    4. Kolik datových bloků se musí zapsat? (celé desítkové číslo)
    5. Kolik operací alokování/uvolňování bloků a i-nodů musí být provedeno? Každou operaci alokace/uvolnění bloku/i-node započtěte zvlášť.

??? success "Řešení"

    ### 1. Kolik i-nodů se musí načíst?

    Pro vytvoření soft-linku v rámci jednoho filesystému nám stačí přečíst cestu, kde bude výsledný odkaz vytvořen. Na rozdíl od hard-linku se vůbec nemusí číst cíl odkazu.

    ```
    R i-node /
    R i-node /home
    R i-node /home/pavel
    ```

    **Musí se načíst 3 i-nody.**

    ### 2. Kolik i-nodů se musí zapsat?

    Jeden na vytvoření i-nodu pro odkaz f.link a další na upravení mtime ve složce pavel.

    ```
    W i-node /home/pavel/f.link
    W i-node /home/pavel  (mtime)
    ```

    **Musí se zapsat 2 i-nody.**

    ### 3. Kolik datových bloků se musí načíst?

    Pro vytvoření symbolického linku nám stačí se dostat do správného adresáře a zde zapsat soubor. Pro čtení datových bloků tedy:

    ```
    R content /
    R content /home
    R content /home/pavel
    ```

    **Musí se načíst 3 datové bloky.**

    ### 4. Kolik datových bloků se musí zapsat?

    ```
    W content /home/pavel
    W content /home/pavel/f.link  (link to /home/pavel/2018/osy/cl/f.pdf)
    ```

    **Musí se zapsat 2 datové bloky.**

    ### 5. Kolik operací alokování/uvolňování bloků a i-nodů musí být provedeno?

    Musí se provést 2 alokace. Celkem 1 i-node a 1 datový blok pro f.link.

    **Musí se provést 2 alokace.**

---

## Úloha 6 — ln -s (symbolický link), UFS blok 16 KiB, 64bitové odkazy

!!! example "Zadání"
    Systém souborů UFS pracuje s i-nody, které mají 12 odkazů přímých a po jednom jednonásobném, dvojnásobném a trojnásobném nepřímém odkazu na datové bloky. Velikost datového bloku je 16 KiB, odkazy na datový blok jsou 64-bitové. Atributy i-nodu jsou: typ souboru, velikost souboru, čítač pevných linků, přístupová práva, vlastník a skupina, čas modifikace, čas přístupu, symbolický link se vždy zapisuje do datového bloku. Informace o volných objektech UFS (i-nodech a blocích) jsou uložené v bitové mapě na disku, která se při připojení systému souborů načetla do paměti.

    Systém souborů FAT32 pracuje s datovými bloky (clustery) o velikosti 16 KiB a odkazy na clustery jsou 64-bitové.

    Předpokládejte, že obsah adresáře nepřesáhne velikost bloku 16 KiB. Dále předpokládejte, že v paměti jsou načtené pouze **superbloky/boot sektory** jednotlivých připojených disků. Pro zpracovávaný soubor víte, že zobrazení by vypadalo takto:

    ```
    # ll /usr/etc/etc/home/games
    ...
    -rw-rw-rw- 1 root root 48039878 Sep 14 21:57 test.cpp
    ...
    ```

    V takové konfiguraci se provede následující příkaz shellu:

    ```
    # ln -s /usr/etc/etc/home/games/test.cpp /var/home/src/lib/src/doc/index.php
    ```

    Uvažujte pouze efekt tohoto příkazu (tedy neuvažujte režii spojenou s vlastním natažením tohoto příkazu do paměti).

    1. Kolik i-nodů se musí načíst? (celé desítkové číslo)
    2. Kolik i-nodů se musí zapsat? (celé desítkové číslo)
    3. Kolik datových bloků se musí načíst? (celé desítkové číslo)
    4. Kolik datových bloků se musí zapsat? (celé desítkové číslo)
    5. Kolik operací alokování/uvolňování bloků a i-nodů musí být provedeno? Každou operaci alokace/uvolnění bloku/i-node započtěte zvlášť.

??? success "Řešení"

    ### 1. Kolik i-nodů se musí načíst?

    Pro symbolický link čteme pouze cestu, kde bude link vytvořen — zdrojová cesta se nečte.

    ```
    R i-node /
    R i-node /var
    R i-node /var/home
    R i-node /var/home/src
    R i-node /var/home/src/lib
    R i-node /var/home/src/lib/src
    R i-node /var/home/src/lib/src/doc
    ```

    **Musí se načíst 7 i-nodů.**

    ### 2. Kolik i-nodů se musí zapsat?

    ```
    W i-node /var/home/src/lib/src/doc/index.php
    W i-node /var/home/src/lib/src/doc  (mtime)
    ```

    **Musí se zapsat 2 i-nody.**

    ### 3. Kolik datových bloků se musí načíst?

    ```
    R content /
    R content /var
    R content /var/home
    R content /var/home/src
    R content /var/home/src/lib
    R content /var/home/src/lib/src
    R content /var/home/src/lib/src/doc
    ```

    **Musí se načíst 7 datových bloků.**

    ### 4. Kolik datových bloků se musí zapsat?

    ```
    W content /var/home/src/lib/src/doc
    W content /var/home/src/lib/src/doc/index.php
    ```

    **Musí se načíst 2 datové bloky.**

    ### 5. Kolik operací alokování/uvolňování bloků a i-nodů musí být provedeno?

    Musí se provést 2 alokace. Celkem 1 i-node a 1 datový blok pro index.php.

    **Musí se provést 2 alokace.**
