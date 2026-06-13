# Vytváření procesů a vláken

??? abstract "Obsah stránky"

    [TOC]

---

Předpokládejme následující systém:

- Procesor(y): 1 × Intel® Core™ 2 Duo Processor E8600 (počet jader na procesor: 2)
- Počet vláken na jádro: 1 (tedy celkem vláken na procesor: 2)
- Architektura: SMP/UMA (desktop)
- Paměť: 2 GiB DDR

Na systému je nainstalovaný operační systém SUSE Linux Enterprise Server (64b) a nastaveny následující limity:

- maximální velikost zásobníku každého procesu je nastavena na 8 MiB
- běžný uživatel smí spustit celkem maximálně 128 vláken (po dosažení tohoto limitu budou funkce vytvářející nová vlákna vracet chybu)

Program `/bin/sleep n` bude po spuštění `n` sekund ve stavu BLOCKED a potom se ukončí. Podobně funkce `sleep(n)` způsobí uspání volajícího procesu na `n` sekund. Dobu potřebnou na provedení ostatních systémových a knihovních volání zanedbejte. Předpokládejme, že běžný uživatel, kterému na systému běží pouze login shell, v čase T0 spustí přeloženou verzi následujícího programu `/home/user/prog`.

## Úloha 1 — Jednoduchý cyklus s fork() bez wait a exec

!!! example "Zadání"

    ```c
    ...
    int main()
    {
      char a[4797902];
      char *ptr_char = (char *) malloc (3700521);

      for (int i = 0; i < 3; i ++)
      {
            child_pid = fork();
            if (child_pid == 0)
            {
              sleep(10);
            }
      }
      free(ptr_char);
      return 0;
    }
    ```

    1. Kolik procesů se celkem vytvoří v důsledku spuštění následujícího příkazu?
       `$ /home/user/prog`
    2. Za kolik sekund po spuštění programu `/home/user/prog` doběhne poslední proces, který vznikl v důsledku provádění tohoto programu?
    3. Kolik procesů, které vznikly v důsledku spuštění programu `/home/user/prog`, poběží v čase T0 + 15 s?
    4. Kolik místa si bude alokovat na zásobníku každý proces provádějící `/home/user/prog` (zaokrouhlete na MiB nahoru)?
    5. Kolik místa si bude alokovat na haldě každý proces provádějící `/home/user/prog` (zaokrouhlete na MiB nahoru)?

??? success "Řešení"

    **1. Počet procesů**

    V každé iteraci cyklu se počet existujících procesů zdvojí (každý existující proces zavolá `fork()`). Potomek (`child_pid == 0`) provede `sleep(10)`, ale protože nemá `return` ani `exit`, po probuzení se vrátí do cyklu a v dalších iteracích také forkuje. Cyklus má 3 iterace (i = 0, 1, 2), tedy celkový počet procesů = 2^3 = 8.

    Strom procesů (hrany označeny návratovou hodnotou fork: != 0 = rodič, = 0 = potomek):

    ```text
                       P0
                    /      \
                !=0           =0
               P0             P3
             /    \         /    \
           !=0    =0      !=0    =0
            P0    P1       P3    P6
           /  \  /  \    /  \  /  \
         !=0 =0 !=0 =0 !=0 =0 !=0 =0
          P0  P2  P1  P4  P3  P5  P6  P7
    ```

    **8 procesů.**

    **2. Doba běhu**

    Procesy vzniklé v iteraci 2 (tj. v poslední iteraci) spí od okamžiku svého vzniku 10 sekund. Nejpozdější vznik nastane u potomka, jehož předkové spali v iteracích 0 a 1 — takový proces vznikne v čase T0+20 s a spí dalších 10 s → skončí v T0+30 s.

    Časová osa (časy vzniku uzlů stromu):

    ```text
                          P0
                      0s /    \ 10s
                       P0      P3
                   0s /  \ 10s   \ 10s / 20s
                    P0    P1      P3    P6
                0s/ \10s 10s/ \20s 10s/ \20s 20s/ \30s
                P0  P2   P1   P4   P3   P5   P6   P7
    ```

    **30 s.**

    **3. Procesy v čase T0 + 15 s**

    Procesy P4, P5, P6 čekají v čase 10–20 sekund (sleep(10) zahájený v T0+10).

    **3 procesy.**

    **4. Zásobník**

    Statická alokace: `char a[4797902];`

    ceil(4 797 902 / 1 048 576) = ceil(4,575...) = **5 MiB**

    **5. Halda**

    Dynamická alokace: `char *ptr_char = (char *) malloc (3700521);`

    ceil(3 700 521 / 1 048 576) = ceil(3,529...) = **4 MiB**

---

Předpokládejme následující systém:

- Procesor(y): 16 × Sparc64-X (počet jader na procesor: 16)
- Počet vláken na jádro: 2 (tedy celkem vláken na procesor: 32)
- Architektura: SMP/NUMA (server)
- Paměť: 512 GiB DDR3

Na systému je nainstalovaný operační systém Debian Wheezy 7.5 (64b) a nastaveny následující limity:

- maximální velikost zásobníku každého procesu je nastavena na 9 MiB
- běžný uživatel smí spustit celkem maximálně 112 vláken (po dosažení tohoto limitu budou funkce vytvářející nová vlákna vracet chybu)

Program `/bin/sleep n` bude po spuštění `n` sekund ve stavu BLOCKED a potom se ukončí. Podobně funkce `sleep(n)` způsobí uspání volajícího procesu na `n` sekund. Dobu potřebnou na provedení ostatních systémových a knihovních volání zanedbejte. Předpokládejme, že běžný uživatel, kterému na systému běží pouze login shell, v čase T0 spustí přeloženou verzi následujícího programu `/home/user/prog`.

## Úloha 2 — Cyklus s fork(), wait() a execlp()

!!! example "Zadání"

    ```c
    ...
    int main()
    {
      char a[1779061];
      char *ptr_char = (char *) malloc (7179004);

      for (int i = 0; i < 4; i ++)
      {
        pid_t child_pid = fork();
        if (child_pid == 0)
        {
          sleep(7);
        }
        else
        {
          int status;
          wait(&status);
          execlp("/bin/sleep", "sleep", "15", (char *) NULL);
          sleep(7);
        }
      }
      free(ptr_char);
      return 0;
    }
    ```

    1. Kolik procesů se celkem vytvoří v důsledku spuštění následujícího příkazu?
       `$ /home/user/prog`
    2. Za kolik sekund po spuštění programu `/home/user/prog` doběhne poslední proces, který vznikl v důsledku provádění tohoto programu?
    3. Kolik procesů, které vznikly v důsledku spuštění programu `/home/user/prog`, poběží v čase T0 + 45,977 s?
    4. Kolik místa si bude alokovat na zásobníku každý proces provádějící `/home/user/prog` (zaokrouhlete na MiB nahoru)?
    5. Kolik místa si bude alokovat na haldě každý proces provádějící `/home/user/prog` (zaokrouhlete na MiB nahoru)?

??? success "Řešení"

    **1. Počet procesů**

    Systémové volání `wait` způsobí, že proces před pokračováním čeká, až skončí nějaký z jeho synů. `execlp` způsobí nahrazení procesu voláním `/bin/sleep`, další řádky se nevykonají a proces končí. Jako důsledek bude proces P0 čekat na kaskádní dokončení všech ostatních procesů, přes postupné součty 7 + 15 + 7 + 15 ...

    Rodičovská větev (`else`): zavolá `wait()` a čeká na potomka. Jakmile potomek skončí, provede `execlp("/bin/sleep", "sleep", "15", ...)` — přemění se na `sleep 15` a skončí. Kód za `execlp` (ani `sleep(7)`, ani další iterace cyklu) se nevykoná. Proto každý rodič vytvoří právě jednoho přímého potomka a pak se přemění.

    Strom procesů je lineární řetězec:

    ```text
               P0
              /   \
            =0    !=0
            P1     P0
           /   \
         =0    !=0
         P2     P1
        /   \
      =0    !=0
      P3     P2
     /   \
    =0    !=0
    P4     P3
    ```

    **5 procesů.**

    **2. Doba běhu**

    Systémové volání `wait` způsobí, že proces čeká na dokončení potomka. `execlp` nahradí kód procesu voláním `/bin/sleep`, další řádky (ani `sleep(7)`, ani další iterace cyklu) se nevykonají a proces skončí. P0 proto bude kaskádně čekat na celý řetězec.

    Cyklus `i < 4` má 4 iterace (i = 0, 1, 2, 3). Díky `wait()` každý rodič čeká, než jeho potomek skutečně skončí, takže se procesy rodí postupně (sériově), ne paralelně. Nejhlubší potomek P4 vznikne v iteraci 3 (i=3) — nemá další iteraci, cyklus skončí a provede `return 0`. Procesy P0–P3 (4 procesy) provedou `execlp sleep 15` poté, co jejich potomek skončí.

    Časový řetězec (každá úroveň přidá 7 s sleep + 15 s jako sleep 15):

    ```text
    Proces | narozen v | sleep(7)  | wait vrátí | jako sleep 15 | konec
    -------|-----------|-----------|------------|---------------|------
    P4     | T0+21     | 21s - 28s | —          | —             | T0+28  (return 0)
    P3     | T0+14     | 14s - 21s | T0+28      | 28s - 43s     | T0+43
    P2     | T0+7      |  7s - 14s | T0+43      | 43s - 58s     | T0+58
    P1     | T0+0      |  0s -  7s | T0+58      | 58s - 73s     | T0+73
    P0     | T0+0      | —         | T0+73      | 73s - 88s     | T0+88
    ```

    Pozn.: P0 nespí sleep(7) — hned zavolá fork a pak wait (je v `else` větvi).

    Strom s časovými popisky dle sbírky (levé číslo = kdy potomek spí, pravé = kdy rodič doběhne):

    ```text
                         P0
                      7s /   \ 88s
                        P1    P0
                     7s /  \ 66s
                       P2    P1
                    7s /  \ 44s
                      P3    P2
                   7s /  \ 22s
                     P4    P3
    ```

    (Pravé číslo odpovídá době, za kterou daný rodičovský proces doběhne od vzniku svého potomka: 7 + 15 = 22 s, 2×(7+15) = 44 s, 3×(7+15) = 66 s, 4×(7+15) = 88 s.)

    **88 s.**

    **3. Procesy v čase T0 + 45,977 s**

    V čase T0+45,977 s:
    - P4 skončil v T0+28 s — již nežije.
    - P3 skončil v T0+43 s — již nežije.
    - P2 běží jako `sleep 15` (43–58 s) — stále žije.
    - P1 čeká ve `wait()` (vrátí se až v T0+58) — stále žije.
    - P0 čeká ve `wait()` (vrátí se až v T0+73) — stále žije.

    Procesy P0, P1, P2 čekají v čase 44–88 sekund, ostatní již stihly skončit.

    **3 procesy.**

    **4. Zásobník**

    `char a[1779061];`

    ceil(1 779 061 / 1 048 576) = ceil(1,696...) = **2 MiB**

    **5. Halda**

    `char *ptr_char = (char *) malloc (7179004);`

    7 179 004 bajtů ≈ 6,84 MiB → ceil = **7 MiB**

---

Předpokládejme následující systém:

- Procesor(y): 1 × Intel® Core™ 2 Duo Processor E8600 (počet jader na procesor: 2)
- Počet vláken na jádro: 1 (tedy celkem vláken na procesor: 2)
- Architektura: SMP/UMA (desktop)
- Paměť: 2 GiB DDR

Na systému je nainstalovaný operační systém Debian Wheezy 7.5 (64b) a nastaveny následující limity:

- maximální velikost zásobníku každého procesu je nastavena na 6 MiB
- běžný uživatel smí spustit celkem maximálně 112 vláken (po dosažení tohoto limitu budou funkce vytvářející nová vlákna vracet chybu)

Program `/bin/sleep n` bude po spuštění `n` sekund ve stavu BLOCKED a potom se ukončí. Podobně funkce `sleep(n)` způsobí uspání volajícího procesu na `n` sekund. Dobu potřebnou na provedení ostatních systémových a knihovních volání zanedbejte. Předpokládejme, že běžný uživatel, kterému na systému běží pouze login shell, v čase T0 spustí přeloženou verzi následujícího programu `/home/user/prog`.

## Úloha 3 — Jednoduchý cyklus bez wait a exec (varianta 2)

!!! example "Zadání"

    ```c
    ...
    int main()
    {
      char a[1775297];
      char *ptr_char = (char *) malloc (8233219);

      for (int i = 0; i < 4; i ++)
      {
        pid_t child_pid = fork();
        if (child_pid == 0)
        {
          sleep(7);
        }
      }
      free(ptr_char);
      return 0;
    }
    ```

    1. Kolik procesů se celkem vytvoří v důsledku spuštění následujícího příkazu?
       `$ /home/user/prog`
    2. Za kolik sekund po spuštění programu `/home/user/prog` doběhne poslední proces, který vznikl v důsledku provádění tohoto programu?
    3. Kolik procesů, které vznikly v důsledku spuštění programu `/home/user/prog`, poběží v čase T0 + 11,509 s?
    4. Kolik místa si bude alokovat na zásobníku každý proces provádějící `/home/user/prog` (zaokrouhlete na MiB nahoru)?
    5. Kolik místa si bude alokovat na haldě každý proces provádějící `/home/user/prog` (zaokrouhlete na MiB nahoru)?

??? success "Řešení"

    **1. Počet procesů**

    Cyklus má 4 iterace (i = 0, 1, 2, 3). Chybí `wait()` a `exec*()` v rodiči — rodič po `fork()` ihned pokračuje do další iterace. Potomek po `sleep(7)` také pokračuje do dalších iterací (bez `return`/`exit`). Počet procesů se v každé iteraci zdvojí:

    - Po iteraci 0: 2 procesy
    - Po iteraci 1: 4 procesy
    - Po iteraci 2: 8 procesů
    - Po iteraci 3: 16 procesů

    **16 procesů.**

    **2. Doba běhu**

    Nejpozdější potomek vznikne v iteraci 3 od předka, který spal v iteracích 0, 1, 2 (3 × 7 = 21 s čekání předka). Tento potomek vznikne v T0+21 s a spí 7 s → skončí v T0+28 s.

    **28 s.**

    **3. Procesy v čase T0 + 11,509 s**

    V čase T0+11,509 s platí:
    - Potomci vzniklí v iteraci 0 (narozeni v T0+0): spí 7 s → skončili v T0+7. Nežijí.
    - Potomci vzniklí v iteraci 1 od původního procesu (narozeni v T0+0): spí 7 s → skončili v T0+7. Nežijí.
    - Potomci vzniklí v iteraci 1 od potomka z iterace 0 (narozeni v T0+7, protože potomek z iter. 0 spal do T0+7): spí 7 s → skončí v T0+14. Stále žijí.
    - Potomci vzniklí v iteraci 2 od procesů, které neprošly sleep (narozeni v T0+0): spí do T0+7. Nežijí.
    - Potomci vzniklí v iteraci 2 od procesů, které prošly jedním sleep (narozeni kolem T0+7): spí do T0+14. Žijí.
    - Potomci vzniklí v iteraci 3 od procesů, které prošly dvěma sleep (narozeni kolem T0+14): ještě se ani nenarodili (T0+14 > T0+11,509). Neexistují.

    Přesný počet dle sbírky: **6 procesů.**

    **4. Zásobník**

    `char a[1775297];`

    ceil(1 775 297 / 1 048 576) = ceil(1,693...) = **2 MiB**

    **5. Halda**

    `char *ptr_char = (char *) malloc (8233219);`

    ceil(8 233 219 / 1 048 576) = ceil(7,851...) = **8 MiB**
