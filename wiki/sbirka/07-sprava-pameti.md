# Správa paměti – multichoice

??? abstract "Obsah stránky"

    [TOC]

---

## Sada 1 – jednoúrovňová tabulka, NRU (stránka 32768 B, VA 48 b, FA 40 b)

Systém používá virtuální paměť se stránkováním. Velikost stránky/rámce je 32768 B, velikost logické adresy je 48 bitů, velikost fyzické adresy je 40 bitů. Systém používá TLB o velikosti 256 položek (řádek). Na systému právě běží 454 uživatelských procesů. Každému uživatelskému procesu je alokováno pouze na nejnižších adresách 113377280 bytů pro kód a haldu a na nejvyšších adresách 7323648 bytů pro zásobník. Pro náhradu stránek se používá algoritmus NRU. Předpokládejme, že systém používá klasickou jednoúrovňovou tabulku stránek. Která z následujících tvrzení jsou pro tento systém s danou konfigurací pravdivá?

### Otázka 1 – logická adresa

!!! example "Zadání"
    Která tvrzení o logické adrese jsou pravdivá?

    - (a) Logická adresa obsahuje číslo rámce velikosti 50 bitů
    - (b) Logická adresa obsahuje offset 15 bitů
    - (c) Logická adresa obsahuje číslo stránky o velikosti 50 bitů
    - (d) Logická adresa obsahuje číslo stránky o velikosti 64 bitů

??? success "Řešení"
    **Správná odpověď: (b)**

    Velikost stránky je 32768 B, takže logická adresa obsahuje offset log2(32768) = 15 bitů.

    Logická adresa má 48 bitů celkem: offset = 15 bitů, číslo stránky = 48 − 15 = 33 bitů. Logická adresa nikdy neobsahuje číslo rámce (to je součást fyzické adresy).

---

### Otázka 2 – fyzická adresa

!!! example "Zadání"
    Která tvrzení o fyzické adrese jsou pravdivá?

    - (a) Fyzická adresa obsahuje číslo rámce velikosti 52 bitů
    - (b) Fyzická adresa obsahuje číslo stránky velikosti 50 bitů
    - (c) Fyzická adresa obsahuje offset velikosti 15 bitů
    - (d) Fyzická adresa obsahuje číslo rámce velikosti 35 bitů

??? success "Řešení"
    **Správná odpověď: (c)**

    Velikost rámce je 32768 B, takže fyzická adresa obsahuje offset log2(32768) = 15 bitů.

    Fyzická adresa má 40 bitů celkem: offset = 15 bitů, číslo rámce = 40 − 15 = 25 bitů. Fyzická adresa nikdy neobsahuje číslo stránky.

---

### Otázka 3 – vlastnosti offsetu

!!! example "Zadání"
    Která tvrzení o offsetu jsou pravdivá?

    - (a) Pro různě velké stránky je velikost offsetu různá
    - (b) Offset definuje pozici dat uvnitř rámce
    - (c) Při překladu adresy se offset používá jako index do klasické tabulky stránek
    - (d) Při překladu adresy hledáme číslo stránky, ve kterém je nahraný daný rámec

??? success "Řešení"
    **Správné odpovědi: (a) a (b)**

    - (a) PRAVDA – offset = log2(velikost stránky); různé velikosti stránek dávají různé offsety.
    - (b) PRAVDA – offset udává pozici bytu uvnitř stránky/rámce.
    - (c) NEPRAVDA – jako index do tabulky stránek se používá číslo stránky, nikoli offset.
    - (d) NEPRAVDA – při překladu hledáme číslo rámce, do kterého je stránka namapována (ne naopak).

---

### Otázka 4 – tabulky stránek v jádře

!!! example "Zadání"
    Která tvrzení o tom, kolik tabulek stránek si musí jádro pamatovat, jsou pravdivá?

    - (a) Jádro systému si musí pamatovat pouze tabulky, které nejsou v TLB
    - (b) Jádro systému si nemusí pamatovat žádnou tabulku, vše je uloženo v TLB
    - (c) Jádro systému si musí pamatovat aspoň 454 tabulek stránek
    - (d) Jádro systému si musí pamatovat pro každý proces právě jednu tabulku

??? success "Řešení"
    **Správné odpovědi: (c) a (d)**

    U klasické jednoúrovňové tabulky stránek jádro udržuje jednu tabulku na každý proces. Běží 454 procesů → jádro si musí pamatovat aspoň 454 tabulek. TLB je pouze cache pro urychlení překladu; plnohodnotné tabulky stránek musí existovat v paměti vždy.

---

### Otázka 5 – obsah řádky klasické tabulky stránek

!!! example "Zadání"
    Která tvrzení o obsahu řádky klasické tabulky stránek jsou pravdivá?

    - (a) Na řádce klasické tabulky stránek je uložené číslo stránky
    - (b) Na řádce klasické tabulky stránek je uložené číslo rámce
    - (c) Na řádce klasické tabulky stránek je uložený Modify bit
    - (d) Na řádce klasické tabulky stránek je uložený Reference bit

??? success "Řešení"
    **Správné odpovědi: (b), (c), (d)**

    Na řádce klasické tabulky stránek je uložené číslo rámce, do kterého se tato stránka namapovala, a kontrolní bity:

    - Present bit (P)
    - Reference bit (R)
    - Modify bit (M)
    - Přístupová práva
    - Cache disable/enabled

    Číslo stránky se na řádce klasické tabulky neukládá – index do tabulky přímo odpovídá číslu stránky.

---

### Otázka 6 – obsah řádky TLB

!!! example "Zadání"
    Která tvrzení o obsahu řádky TLB jsou pravdivá?

    - (a) Na řádce TLB je uložený Reference bit
    - (b) Na řádce TLB je uložený Modify bit
    - (c) Na řádce TLB je uložené číslo rámce
    - (d) Na řádce TLB je uložený offset

??? success "Řešení"
    **Správné odpovědi: (a), (b), (c)**

    Položka TLB obsahuje:

    - Valid bit
    - Číslo stránky
    - Číslo rámce
    - ASID (address space ID)
    - Kontrolní bity (Reference bit, Modify bit, přístupová práva…)

    Offset se do TLB neukládá – je součástí adresy, ale překlad stránka → rámec se provádí bez offsetu.

---

### Otázka 7 – TLB hit ratio a velikost stránek

!!! example "Zadání"
    Která tvrzení o TLB hit ratio a velikosti stránek jsou pravdivá?

    - (a) Cache hit ratio TLB se může zvýšit, pokud systém bude používat pro proces větší stránky
    - (b) Současné serverové a desktopové procesory umožňují používat různě velké stránky pro různé procesy
    - (c) Současné serverové a desktopové procesory umožňují aplikacím za běhu měnit velikost TLB podle potřeby
    - (d) Cache hit ratio TLB se může zvýšit, pokud systém bude používat pro proces menší stránky

??? success "Řešení"
    **Správné odpovědi: (a) a (b)**

    - (a) PRAVDA – větší stránka pokrývá více adres jedinou TLB položkou → více hitů.
    - (b) PRAVDA – moderní procesory (x86-64, ARM) podporují huge pages (2 MiB, 1 GiB) vedle standardních 4 KiB stránek; různé procesy (nebo různé oblasti paměti) mohou používat různé velikosti.
    - (c) NEPRAVDA – TLB je pevná hardwarová cache; aplikace ji nemohou za běhu zvětšovat.
    - (d) NEPRAVDA – menší stránky znamenají méně adres na položku → hit ratio spíše klesá.

---

### Otázka 8 – počet řádek tabulky stránek (sada 1)

!!! example "Zadání"
    Kolik řádek bude obsahovat tabulka stránek? (celé desítkové číslo)

??? success "Řešení"
    Bude obsahovat 2^(48−15) = 2^33 řádek.

    - offset = log2(32768) = 15 bitů
    - číslo stránky = 48 − 15 = 33 bitů
    - počet řádek jednoúrovňové tabulky = 2^33

---

## Sada 2 – invertovaná tabulka, Clock (stránka 65536 B, VA 64 b, FA 48 b)

Systém používá virtuální paměť se stránkováním. Velikost stránky/rámce je 65536 B, velikost logické adresy je 64 bitů, velikost fyzické adresy je 48 bitů. Systém používá TLB o velikosti 2048 položek (řádek). Na systému právě běží 417 uživatelských procesů. Každému procesu je alokováno pouze na nejnižších adresách 286785536 bytů pro kód a haldu a na nejvyšších adresách 56688640 bytů pro zásobník. Pro náhradu stránek se používá algoritmus Clock. Předpokládejme, že systém používá invertovanou tabulku stránek. Která z následujících tvrzení jsou pro tento systém a danou konfiguraci pravdivá?

### Otázka 9 – logická adresa (sada 2)

!!! example "Zadání"
    Která tvrzení o logické adrese jsou pravdivá?

    - (a) Logická adresa obsahuje číslo rámce velikosti 32 bitů
    - (b) Logická adresa obsahuje číslo rámce velikosti 48 bitů
    - (c) Logická adresa obsahuje číslo stránky velikosti 48 bitů
    - (d) Logická adresa obsahuje číslo stránky velikosti 64 bitů

??? success "Řešení"
    **Správná odpověď: (c)**

    - offset = log2(65536) = 16 bitů
    - číslo stránky = 64 − 16 = 48 bitů

    Logická adresa nikdy neobsahuje číslo rámce.

---

### Otázka 10 – fyzická adresa (sada 2)

!!! example "Zadání"
    Která tvrzení o fyzické adrese jsou pravdivá?

    - (a) Fyzická adresa obsahuje číslo rámce velikosti 48 bitů
    - (b) Fyzická adresa obsahuje offset velikosti 16 bitů
    - (c) Fyzická adresa obsahuje číslo stránky velikosti 32 bitů
    - (d) Fyzická adresa obsahuje číslo rámce velikosti 32 bitů

??? success "Řešení"
    **Správné odpovědi: (b) a (d)**

    - offset = log2(65536) = 16 bitů
    - číslo rámce = 48 − 16 = 32 bitů

    Fyzická adresa tedy obsahuje 16bitový offset a 32bitové číslo rámce.

---

### Otázka 11 – překlad adresy s invertovanou tabulkou

!!! example "Zadání"
    Která tvrzení o překladu adresy jsou pravdivá?

    - (a) Při překladu adresy lze použít rozptylovací funkci k urychlení překladu
    - (b) Při překladu adresy hledáme v tabulce řádku, ve které je záznam o daném rámci
    - (c) Při překladu adresy hledáme číslo rámce, do kterého se stránka nahrála
    - (d) Při překladu adresy se číslo rámce používá jako index do TLB

??? success "Řešení"
    **Správné odpovědi: (a) a (c)**

    - (a) PRAVDA – invertovaná tabulka je indexována číslem rámce, ale pro překlad ze stránky na rámec je třeba prohledat celou tabulku; hash funkce na číslo stránky tento proces urychluje.
    - (b) NEPRAVDA – invertovaná tabulka je sice indexována číslem rámce, ale hledáme řádku podle čísla stránky (ne rámce).
    - (c) PRAVDA – cílem překladu je najít číslo rámce, do kterého byla stránka nahrána.
    - (d) NEPRAVDA – do TLB se používá číslo stránky jako klíč, nikoli číslo rámce.

---

### Otázka 12 – tabulky stránek v jádře (sada 2, invertovaná)

!!! example "Zadání"
    Která tvrzení o tom, kolik tabulek stránek si musí jádro pamatovat, jsou pravdivá?

    - (a) Jádro systému si musí pamatovat pouze tabulky, které nejsou v TLB
    - (b) Jádro systému si nemusí pamatovat žádnou tabulku, vše je uloženo v TLB
    - (c) Jádro systému si musí pamatovat pro každý proces právě jednu tabulku
    - (d) Jádro systému si musí pamatovat aspoň 417 tabulek stránek

??? success "Řešení"
    **Žádná z nabízených možností není správná tak jak jsou formulovány — správné je, že jádro udržuje právě jednu invertovanou tabulku pro celý systém.**

    U invertované tabulky stránek existuje v systému pouze jedna tabulka, bez ohledu na počet procesů. Počet řádek odpovídá počtu fyzických rámců (2^32), nikoli počtu procesů. Možnosti (c) a (d) popisují chování jednoúrovňové tabulky, nikoli invertované. TLB (b) je pouze cache a tabulku nenahrazuje.

---

### Otázka 13 – obsah řádky invertované tabulky stránek

!!! example "Zadání"
    Která tvrzení o obsahu řádky invertované tabulky stránek jsou pravdivá?

    - (a) Na řádce invertované tabulky stránek je uložené číslo stránky
    - (b) Na řádce invertované tabulky stránek je uložené číslo procesu
    - (c) Na řádce invertované tabulky stránek je uložený Present bit
    - (d) Na řádce invertované tabulky stránek je uložený offset

??? success "Řešení"
    **Správné odpovědi: (a), (b), (c)**

    Řádka invertované tabulky stránek obsahuje:

    - Číslo stránky (identifikuje, která virtuální stránka je v tomto rámci)
    - Číslo procesu / PID (více procesů může mít stránku se stejným číslem)
    - Present bit (P)
    - Reference bit (R), Modify bit (M)
    - Index zřetězení (pro řešení kolizí při použití hash funkce)

    Offset se neukládá – je součástí adresy, ne tabulky.

---

### Otázka 14 – obsah řádky TLB (sada 2)

!!! example "Zadání"
    Která tvrzení o obsahu řádky TLB jsou pravdivá?

    - (a) Na řádce TLB je uložený Modify bit
    - (b) Na řádce TLB je uložené číslo rámce
    - (c) Na řádce TLB je uložený offset
    - (d) Na řádce TLB je uložený Reference bit

??? success "Řešení"
    **Správné odpovědi: (a), (b), (d)**

    Položka TLB obsahuje: Valid bit, číslo stránky, číslo rámce, ASID a kontrolní bity (Reference bit, Modify bit, přístupová práva). Offset se do TLB neukládá.

---

### Otázka 15 – TLB hit ratio a velikost stránek (sada 2)

!!! example "Zadání"
    Která tvrzení o TLB hit ratio a velikosti stránek jsou pravdivá?

    - (a) Cache hit ratio TLB se může zvýšit pokud systém bude používat pro proces větší stránky
    - (b) Současné serverové a desktopové procesory umožňují používat různě velké stránky pro různé procesy
    - (c) Současné serverové a desktopové procesory umožňují aplikacím za běhu měnit velikost TLB podle potřeby.
    - (d) Cache hit ratio TLB se může zvýšit pokud systém bude používat pro proces menší stránky

??? success "Řešení"
    **Správné odpovědi: (a) a (b)**

    Shodně se sadou 1: větší stránky zvyšují hit ratio; moderní HW podporuje různé velikosti stránek pro různé procesy/oblasti. TLB velikost je hardwarově pevná, aplikace ji nemůže měnit. Menší stránky hit ratio nesnižují efektivitu TLB, ale nesnižují ani nezvyšují – spíše snižují pokrytí na položku.

---

### Otázka 16 – počet řádek tabulky stránek (sada 2)

!!! example "Zadání"
    Kolik řádek bude obsahovat tabulka stránek? (celé desítkové číslo)

??? success "Řešení"
    Bude obsahovat 2^32 řádek.

    - offset = log2(65536) = 16 bitů
    - číslo rámce = 48 − 16 = 32 bitů
    - invertovaná tabulka má jednu řádku na každý fyzický rámec → počet řádek = 2^32

---

## Sada 3 – jednoúrovňová tabulka, Aging (stránka 4096 B, VA 32 b, FA 32 b)

Systém používá virtuální paměť se stránkováním. Velikost stránky/rámce je 4096 B, velikost logické adresy je 32 bitů, velikost fyzické adresy je 32 bitů. Systém používá TLB o velikosti 512 položek (řádek). Na systému právě běží 143 uživatelských procesů. Každému uživatelskému procesu je alokováno pouze na nejnižších adresách 8388600 bytů pro kód a haldu a na nejvyšších adresách 16777200 bytů pro zásobník. Pro náhradu stránek se používá algoritmus Aging. Předpokládejme, že systém používá klasickou jednoúrovňovou tabulku stránek. Která z následujících tvrzení jsou pro tento systém s danou konfigurací pravdivá?

### Otázka 17 – logická adresa (sada 3)

!!! example "Zadání"
    Která tvrzení o logické adrese jsou pravdivá?

    - (a) Logická adresa obsahuje číslo stránky velikosti 20 bitů
    - (b) Logická adresa obsahuje číslo rámce velikosti 20 bitů
    - (c) Logická adresa obsahuje offset velikosti 12 bitů
    - (d) Logická adresa obsahuje číslo rámce velikosti 21 bitů

??? success "Řešení"
    **Správné odpovědi: (a) a (c)**

    - offset = log2(4096) = 12 bitů
    - číslo stránky = 32 − 12 = 20 bitů

    Logická adresa neobsahuje číslo rámce (to je součást fyzické adresy).

---

### Otázka 18 – fyzická adresa (sada 3)

!!! example "Zadání"
    Která tvrzení o fyzické adrese jsou pravdivá?

    - (a) Fyzická adresa obsahuje číslo rámce velikosti 20 bitů
    - (b) Fyzická adresa obsahuje číslo stránky velikosti 20 bitů
    - (c) Fyzická adresa obsahuje číslo stránky velikosti 12 bitů
    - (d) Fyzická adresa obsahuje číslo rámce velikosti 12 bitů

??? success "Řešení"
    **Správná odpověď: (a)**

    - offset = log2(4096) = 12 bitů
    - číslo rámce = 32 − 12 = 20 bitů

    Fyzická adresa obsahuje 20bitové číslo rámce a 12bitový offset. Nikdy neobsahuje číslo stránky.

---

### Otázka 19 – překlad adresy s klasickou tabulkou (sada 3)

!!! example "Zadání"
    Která tvrzení o překladu adresy jsou pravdivá?

    - (a) Při překladu adresy se číslo stránky používá jako index do TLB
    - (b) Při překladu adresy se číslo rámce používá jako index do TLB
    - (c) Při překladu adresy hledáme číslo stránky, ve kterém je nahraný daný rámec
    - (d) Při překladu adresy se číslo stránky používá jako index do TLB

??? success "Řešení"
    **Správné odpovědi: (a) a (d)**

    Odpovědi (a) a (d) jsou identická tvrzení a obě jsou pravdivá. Při překladu adresy se číslo stránky používá jako index (klíč) pro vyhledání v TLB i v tabulce stránek. Číslo rámce je výsledkem překladu, nikoli vstupem. Hledáme číslo rámce, do kterého je stránka namapována – nikoli naopak.

---

### Otázka 20 – tabulky stránek v jádře (sada 3)

!!! example "Zadání"
    Která tvrzení o tom, kolik tabulek stránek si musí jádro pamatovat, jsou pravdivá?

    - (a) Jádro systému si musí pamatovat pro každý proces právě jednu tabulku
    - (b) Jádro systému si musí pamatovat jenom jednu tabulku stránek
    - (c) Jádro systému si nemusí pamatovat žádnou tabulku, vše je uloženo v TLB
    - (d) Jádro systému si musí pamatovat pouze tabulky, které nejsou v TLB

??? success "Řešení"
    **Správná odpověď: (a)**

    U klasické jednoúrovňové tabulky stránek jádro udržuje jednu tabulku na každý proces → pro 143 procesů aspoň 143 tabulek. TLB je pouze cache a plnohodnotné tabulky nenahrazuje. Možnost (b) popisuje invertovanou tabulku.

---

### Otázka 21 – obsah řádky invertované tabulky (sada 3, pozor na formulaci)

!!! example "Zadání"
    Která tvrzení o obsahu řádky invertované tabulky stránek jsou pravdivá?

    *(Poznámka: Ačkoli sada 3 používá klasickou tabulku, tato otázka se ptá na invertovanou – stejně jako v ostatních sadách.)*

    - (a) Na řádce invertované tabulky stránek je uložený offset
    - (b) Na řádce invertované tabulky stránek je uložený Modify bit
    - (c) Na řádce invertované tabulky stránek je uložený Present bit
    - (d) Na řádce invertované tabulky stránek je uložený Reference bit

??? success "Řešení"
    **Správné odpovědi: (b), (c), (d)**

    Řádka invertované tabulky obsahuje: číslo stránky, číslo procesu, Present bit (P), Reference bit (R), Modify bit (M) a index zřetězení. Offset se do tabulky neukládá.

---

### Otázka 22 – obsah řádky TLB (sada 3)

!!! example "Zadání"
    Která tvrzení o obsahu řádky TLB jsou pravdivá?

    - (a) Na řádce TLB je uložené číslo stránky
    - (b) Na řádce TLB je uložený offset
    - (c) Na řádce TLB je uložený Reference bit
    - (d) Na řádce TLB je uložený Modify bit

??? success "Řešení"
    **Správné odpovědi: (a), (c), (d)**

    Položka TLB obsahuje: Valid bit, číslo stránky, číslo rámce, ASID a kontrolní bity (Reference bit, Modify bit, přístupová práva). Offset se do TLB neukládá.

---

### Otázka 23 – TLB hit ratio a velikost stránek (sada 3)

!!! example "Zadání"
    Která tvrzení o TLB hit ratio a velikosti stránek jsou pravdivá?

    - (a) Cache hit ratio TLB se může zvýšit pokud systém bude používat pro proces větší stránky
    - (b) Cache hit ratio TLB se může zvýšit pokud systém bude používat pro proces menší stránky
    - (c) Současné serverové a desktopové procesory umožňují aplikacím za běhu měnit velikost TLB podle potřeby.
    - (d) Současné serverové a desktopové procesory umožňují používat různě velké stránky pro různé procesy

??? success "Řešení"
    **Správné odpovědi: (a) a (d)**

    Shodně se sadami 1 a 2: větší stránky zvyšují TLB hit ratio; moderní HW (x86-64, ARM) podporuje různě velké stránky pro různé procesy/oblasti paměti. Velikost TLB je fixní hardware parametr, aplikace ji za běhu měnit nemůže.

---

### Otázka 24 – počet řádek tabulky stránek (sada 3)

!!! example "Zadání"
    Kolik řádek bude obsahovat tabulka stránek? (celé desítkové číslo)

??? success "Řešení"
    Bude obsahovat 2^20 řádek.

    - offset = log2(4096) = 12 bitů
    - číslo stránky = 32 − 12 = 20 bitů
    - jednoúrovňová tabulka má jednu řádku na každou stránku VAS → počet řádek = 2^20 = 1 048 576
