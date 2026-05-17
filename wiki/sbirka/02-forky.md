# Forky

??? abstract "Obsah stránky"

    [TOC]

---

## Úloha 1 — fork() s &&: kolik výpisů „test"?

!!! example "Zadání"
    Kolik řetězců „test" se vytiskne?

    ```c
    if (fork() &&
            fork() &&
            fork() &&
            fork())
        printf("test\n");
    ```

??? success "Řešení"
    Systémové volání `fork()` způsobí, že z rodičovského procesu vznikne nový proces, který pokračuje v kódu na stejném místě, kde se oddělil od rodiče. Návratová hodnota funkce `fork()` v rodiči je PID potomka, a v potomku se vrátí nula. Pokaždé, když `fork()` vrátí nulu (tedy v child procesech), dojde k přerušení výpočtu podmínky, protože již nemůže být splněna.

    Strom procesů (operátor `&&` zkratuje při `= 0`):

    ```text
              P0
            =0 / \ ≠0
             P1   P0
               =0 / \ ≠0
                P2   P0
                  =0 / \ ≠0
                   P3   P0
                     =0 / \ ≠0
                      P4  test
    ```

    Každý potomek P1, P2, P3, P4 vznikne na větvi `= 0` (fork vrátí 0) a podmínka se přeruší — `printf` se nevykoná. Pouze původní proces P0 projde všemi čtyřmi `fork()` s nenulovými hodnotami (PID potomků) a vytiskne „test".

    **Vytiskne se 1 řetězec „test".**

---

## Úloha 2 — fork() s ||: kolik výpisů „test"?

!!! example "Zadání"
    Kolik řetězců „test" se vytiskne?

    ```c
    if (fork() ||
            fork() ||
            fork() ||
            fork())
        printf("test\n");
    ```

??? success "Řešení"
    Pokaždé když `fork()` vrátí nenulové PID, dojde k splnění podmínky a vytiskne se řetězec „test". Když `fork()` vrátí nulu (tedy v child procesech), podmínka ještě může být splněna, a tak výpočet pokračuje.

    Strom procesů (operátor `||` zkratuje při `≠ 0`):

    ```text
              P0
          ≠0 /  \ =0
          test   P1
             ≠0 /  \ =0
             test   P2
                ≠0 /  \ =0
                test   P3
                   ≠0 /  \ =0
                   test   P4
    ```

    Každý rodič projde větví `≠ 0` a ihned vytiskne „test". Potomci (na větvích `= 0`) pokračují do dalšího `fork()`. Původní P0 vytiskne „test" hned z prvního `fork()`. P1 vytiskne „test" z druhého. P2 z třetího. P3 z čtvrtého. P4 (potomek P3) se ocitne v podmínce, kde žádný `fork()` nezbývá — nevytiskne nic.

    **Vytisknou se 4 řetězce „test".**

---

## Úloha 3 — fork() s || (8 fork()): kolik výpisů „test"?

!!! example "Zadání"
    Kolik řetězců „test" se vytiskne?

    ```c
    if (fork() ||
            fork() ||
            fork() ||
            fork() ||
            fork() ||
            fork() ||
            fork() ||
            fork())
        printf("test\n");
    ```

??? success "Řešení"
    Stejný princip jako v předchozí úloze, nyní s osmi voláními `fork()`.

    Strom procesů:

    ```text
              P0
          ≠0 /  \ =0
          test   P1
             ≠0 /  \ =0
             test   P2
                ≠0 /  \ =0
                test   P3
                   ≠0 /  \ =0
                   test   P4
                      ≠0 /  \ =0
                      test   P5
                         ≠0 /  \ =0
                         test   P6
                            ≠0 /  \ =0
                            test   P7
                               ≠0 /  \ =0
                               test   P8
    ```

    Rodičovský proces na každé úrovni vytiskne „test" větví `≠ 0`. Potomek (větev `= 0`) pokračuje do dalšího `fork()`. Tímto způsobem vznikne 8 výpisů — po jednom za každý `fork()`, který vrátil nenulové PID.

    **Vytiskne se 8 řetězců „test".**

---

## Úloha 4 — fork() == fork() v cyklu (i < 5): kolik procesů vznikne?

!!! example "Zadání"
    Kolik procesů vznikne důsledkem spuštění následujícího kódu?

    ```c
    for( int i = 0; i < 5; i++ ){
      if( fork() == fork() )
        break;
    }
    ```

??? success "Řešení"
    V rámci jedné inkrementace proměnné `i` se provedou **dva forky**, které odpovídají dvěma hladinám stromu procesů. Při přechodu po zelené hraně (vlevo) zůstáváme v rámci stejného procesu, při přechodu vpravo vzniká nový child proces. V červených vrcholech stromu nastává `break`.

    Výraz `fork() == fork()` — levý `fork()` vrátí v rodiči PID potomka (≠ 0) a v potomkovi 0; pravý `fork()` se pak vyhodnotí v obou těchto procesech. Podmínka je splněna (`0 == 0`) jen v tom procesu, kde oba forky vrátily 0 — ten provede `break`.

    V grafu lze pozorovat, že **po každé druhé hladině stromu se počet procesů ztrojnásobí**. (Grafická ilustrace od čtvrté hladiny už není přesná a má jen znázornit větvení stromu.)

    ```text
    úroveň (po dvojici forků):  0    1    2    3    4    5
    počet procesů:              1    3    9   27   81  243
    ```

    **Celkově vznikne 1 + 3 + 9 + 27 + 81 + 243 = 364 nových procesů.**

---

## Úloha 5 — fork() == fork() v cyklu (i < 9): kolik procesů vznikne?

!!! example "Zadání"
    Kolik procesů vznikne důsledkem spuštění následujícího kódu?

    ```c
    for( int i = 0; i < 9; i++ ){
      if( fork() == fork() )
        break;
    }
    ```

??? success "Řešení"
    Stejný princip jako v předchozí úloze — v rámci jedné inkrementace proměnné `i` se provedou dva forky odpovídající dvěma hladinám stromu. Počet procesů se po každé druhé hladině ztrojnásobí.

    Součet pro cyklus `i < 9`:

    ```text
    1 + 3 + 9 + 27 + 81 + 243 + 729 + 2187 + 6561 + 19683 = 29524
    ```

    **Celkově vznikne 1 + 3 + 9 + 27 + 81 + 243 + 729 + 2187 + 6561 + 19683 = 29524 nových procesů.**
