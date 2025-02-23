import re
from bank import log_transaction, get_time, get_db_connection

ip_pattern = r"^(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)$"
MAX_AMOUNT = 9223372036854775807

def send_request_to_bank(bank_ip, data):
    """Mock: Síťová komunikace není implementována."""
    return f"ER Chyba při odesílání P2P transakce: Síťová komunikace není implementována."

def process_command(data, bank):
    if not data.strip():
        return "ER Prázdný příkaz"

    parts = data.split()
    command = parts[0].upper()

    # ---------------------------------------------------------------
    # Příkazy, které mají jen jedno slovo (BC, AC, BA, BN)
    # ---------------------------------------------------------------
    if command == "BC":
        # BC bez parametrů je OK, cokoliv navíc chyba
        if len(parts) == 1:
            return f"BC {bank.ip_address}"
        else:
            return "ER Příkaz BC nevyžaduje žádné parametry."

    if command == "AC":
        # AC bez parametrů je OK, cokoliv navíc chyba
        if len(parts) == 1:
            return bank.create_account()
        else:
            return "ER Příkaz AC nevyžaduje žádné parametry."

    if command == "BA":
        # BA bez parametrů je OK, cokoliv navíc chyba
        if len(parts) == 1:
            return bank.total_amount()
        else:
            return "ER Příkaz BA nevyžaduje žádné parametry."

    if command == "BN":
        # BN bez parametrů je OK, cokoliv navíc chyba
        if len(parts) == 1:
            return bank.num_clients()
        else:
            return "ER Příkaz BN nevyžaduje žádné parametry."

    # ---------------------------------------------------------------
    # AD / AW (vklad / výběr) - 3 argumenty: "AD 12345/127.0.0.1 500"
    # ---------------------------------------------------------------
    if command in ("AD", "AW") and len(parts) == 3:
        account_ip = parts[1]
        amount_str = parts[2]
        errors = []

        # 1) Rozdělit účet a IP
        if "/" not in account_ip:
            errors.append("chybí lomítko mezi číslem účtu a IP")
        else:
            acc_number_str, bank_ip = account_ip.split("/", 1)

            # a) Syntaktická validace čísla účtu
            if not (acc_number_str.isdigit() and 10000 <= int(acc_number_str) <= 99999):
                errors.append("číslo účtu není v rozsahu 10000-99999")
            else:
                # Ověření existence účtu v DB
                acc_number = int(acc_number_str)
                conn = get_db_connection()
                with conn.cursor() as cursor:
                    cursor.execute("SELECT id FROM accounts WHERE id = %s", (acc_number,))
                    row = cursor.fetchone()
                    if not row:
                        errors.append("účet neexistuje")

            # b) Validace IP adresy
            if not re.fullmatch(ip_pattern, bank_ip or ""):
                errors.append("IP adresa je nesprávná")
            else:
                if bank_ip != bank.ip_address:
                    errors.append("IP adresa neodpovídá této bance")

        # 2) Validace částky
        if not re.fullmatch(r"[1-9]\d*", amount_str):
            errors.append("částka musí být celé kladné číslo bez +, - a nesmí začínat nulou")
        else:
            amount = int(amount_str)
            if amount > MAX_AMOUNT:
                errors.append("částka překračuje 64bitový limit")

        # 3) Pokud máme chyby, vrátíme je naráz
        if errors:
            return "ER " + " a ".join(errors) + "."

        # 4) Vše OK -> vklad nebo výběr
        if command == "AD":
            return bank.deposit(int(acc_number_str), amount)
        else:
            return bank.withdraw(int(acc_number_str), amount)

    # ---------------------------------------------------------------
    # AB (Balance) - 2 argumenty: "AB 12345/127.0.0.1"
    # ---------------------------------------------------------------
    if command == "AB" and len(parts) == 2:
        account_ip = parts[1]
        errors = []

        if "/" not in account_ip:
            errors.append("chybí lomítko mezi účtem a IP")
        else:
            acc_number_str, bank_ip = account_ip.split("/", 1)

            if not (acc_number_str.isdigit() and 10000 <= int(acc_number_str) <= 99999):
                errors.append("číslo účtu není v rozsahu 10000-99999")
            else:
                acc_number = int(acc_number_str)
                conn = get_db_connection()
                with conn.cursor() as cursor:
                    cursor.execute("SELECT id FROM accounts WHERE id = %s", (acc_number,))
                    row = cursor.fetchone()
                    if not row:
                        errors.append("účet neexistuje")

            if not re.fullmatch(ip_pattern, bank_ip or ""):
                errors.append("IP adresa je nesprávná")
            else:
                if bank_ip != bank.ip_address:
                    errors.append("IP adresa neodpovídá této bance")

        if errors:
            return "ER " + " a ".join(errors) + "."

        return bank.get_balance(acc_number)

    # ---------------------------------------------------------------
    # AR (Remove account) - 2 argumenty: "AR 12345/127.0.0.1"
    # ---------------------------------------------------------------
    if command == "AR" and len(parts) == 2:
        account_ip = parts[1]
        errors = []

        if "/" not in account_ip:
            errors.append("chybí lomítko mezi účtem a IP")
        else:
            acc_number_str, bank_ip = account_ip.split("/", 1)

            if not (acc_number_str.isdigit() and 10000 <= int(acc_number_str) <= 99999):
                errors.append("číslo účtu není v rozsahu 10000-99999")
            else:
                acc_number = int(acc_number_str)
                conn = get_db_connection()
                with conn.cursor() as cursor:
                    cursor.execute("SELECT id FROM accounts WHERE id = %s", (acc_number,))
                    row = cursor.fetchone()
                    if not row:
                        errors.append("účet neexistuje")

            if not re.fullmatch(ip_pattern, bank_ip or ""):
                errors.append("IP adresa je nesprávná")
            else:
                if bank_ip != bank.ip_address:
                    errors.append("IP adresa neodpovídá této bance")

        if errors:
            return "ER " + " a ".join(errors) + "."

        return bank.remove_account(acc_number)

    # ---------------------------------------------------------------
    # Příkaz není platný
    # ---------------------------------------------------------------
    return "ER Neplatný příkaz"
