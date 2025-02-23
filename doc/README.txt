# Dokumentace k aplikaci P2P Banka

## Jak spustit aplikaci

1. Instalace závislostí
   Nejprve se ujistěte, že máte nainstalovaný Python 3.12 nebo novější a pip pro instalaci závislostí.

   Spusťte terminál v kořenovém adresáři projektu a použijte následující příkaz pro instalaci požadovaných balíčků:

   pip install -r requirements.txt

   2. Spuštění aplikace

    Pro spuštění bankovní aplikace použijte následující příkaz v terminálu: python run_server.py
    Aplikace začne naslouchat na portu definovaném v souboru config.py a přijímat příkazy od klientů.
    A otevřete si MYSQL Workbench, (pro uchování účtů a jejich transakcí)

   3. Ovládání aplikace: Aplikace naslouchá na TCP/IP portu 65525 až 65535. Klienti mohou posílat příkazy ve formátu textu (UTF-8) a aplikace bude odpovídat na tyto příkazy podle jejich typu.

    Příklady příkazů:

    BC: Získání kódu banky (IP adresa serveru)
    AC: Vytvoření nového bankovního účtu
    AD [amount]: Vklad na účet
    AW [amount]: Výběr z účtu


   4. Použité zdroje:

    https://stackoverflow.com/questions/23267305/python-sockets-peer-to-peer

   5. Seznam znovu použitých zdrojů z předchozích projektů

   Modul pro práci s databází: Využité kódy pro připojení k MySQL databázi a práci s SQL dotazy byly převzaty a upraveny z předchozích projektů

   Logování a transakce: Logovací systém, který zaznamenává všechny operace provedené v aplikaci, byl částečně inspirován předchozím projektem, kde byla implementována podobná funkcionalita.





