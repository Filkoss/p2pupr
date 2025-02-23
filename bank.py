import os
import random
import pymysql
from datetime import datetime
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME
from bank_account import BankAccount

LOG_FILE = "bank.log"


class Bank:
    def __init__(self, ip_address):
        self.ip_address = ip_address

    def create_account(self):
        """Vytvoří nový účet s číslem v rozmezí 10000 - 99999 a uloží ho do databáze."""
        try:
            connection = get_db_connection()
            with connection.cursor() as cursor:
                while True:
                    acc_number = random.randint(10000, 99999)
                    cursor.execute("SELECT id FROM accounts WHERE id = %s", (acc_number,))
                    if not cursor.fetchone():
                        cursor.execute("INSERT INTO accounts (id, balance) VALUES (%s, 0)", (acc_number,))
                        connection.commit()
                        break

            log_transaction(f"[{get_time()}] Vytvořen účet {acc_number} s bankou {self.ip_address}")
            return f"AC {acc_number}/{self.ip_address}"

        except Exception as e:
            return f"ER Chyba při vytváření účtu: {str(e)}"

    def deposit(self, account_number, amount):
        if not isinstance(amount, int) or amount <= 0 or amount > 9223372036854775807:
            return "ER Částka musí být celé kladné číslo v rozsahu 1 až 9223372036854775807."

        try:
            connection = get_db_connection()
            with connection.cursor() as cursor:
                cursor.execute("SELECT balance FROM accounts WHERE id = %s", (account_number,))
                row = cursor.fetchone()
                if not row:
                    return "ER Účet neexistuje"

                new_balance = row["balance"] + amount
                cursor.execute("UPDATE accounts SET balance = %s WHERE id = %s", (new_balance, account_number))
                connection.commit()

            log_transaction(f"[{get_time()}] Vklad {amount} na účet {account_number}")
            return f"AD {amount} na účet {account_number}"

        except Exception as e:
            return f"ER Chyba při vkladu: {str(e)}"

    def withdraw(self, account_number, amount):
        if not isinstance(amount, int) or amount <= 0 or amount > 9223372036854775807:
            return "ER Částka musí být celé kladné číslo v rozsahu 1 až 9223372036854775807."

        try:
            connection = get_db_connection()
            with connection.cursor() as cursor:
                cursor.execute("SELECT balance FROM accounts WHERE id = %s", (account_number,))
                row = cursor.fetchone()
                if not row:
                    return "ER Účet neexistuje"

                if row["balance"] < amount:
                    return "ER Nedostatek prostředků na účtu."

                new_balance = row["balance"] - amount
                cursor.execute("UPDATE accounts SET balance = %s WHERE id = %s", (new_balance, account_number))
                connection.commit()

            log_transaction(f"[{get_time()}] Výběr {amount} z účtu {account_number}")
            return f"AW {amount} z účtu {account_number}"

        except Exception as e:
            return f"ER Chyba při výběru: {str(e)}"

    def get_balance(self, account_number):
        """Vrátí zůstatek účtu ve správném formátu."""
        try:
            connection = get_db_connection()
            with connection.cursor() as cursor:
                cursor.execute("SELECT balance FROM accounts WHERE id = %s", (account_number,))
                row = cursor.fetchone()
                if not row:
                    return "ER Účet neexistuje"
                return f"AB OK {int(row['balance'])}"  # Oprava návratové hodnoty pro testy

        except Exception as e:
            return f"ER Chyba při získávání zůstatku: {str(e)}"

    def remove_account(self, account_number):
        """Odstraní účet z databáze a ověří, že byl skutečně smazán."""
        try:
            connection = get_db_connection()
            with connection.cursor() as cursor:
                # Zkontrolujeme, zda účet existuje
                cursor.execute("SELECT balance FROM accounts WHERE id = %s", (account_number,))
                row = cursor.fetchone()
                if not row:
                    return "ER Účet neexistuje"

                if row["balance"] != 0:
                    return "ER Nelze smazat bankovní účet na kterém jsou finance."

                # Smazání účtu
                cursor.execute("DELETE FROM accounts WHERE id = %s", (account_number,))
                connection.commit()

            log_transaction(f"[{get_time()}] Účet {account_number} byl odstraněn")

            # Ověříme, že účet už opravdu neexistuje
            with connection.cursor() as cursor:
                cursor.execute("SELECT id FROM accounts WHERE id = %s", (account_number,))
                if not cursor.fetchone():
                    return f"AR Účet {account_number} odstraněn. Nyní už neexistuje."
                else:
                    return "ER Chyba: Účet se nepodařilo odstranit."

        except Exception as e:
            return f"ER Chyba při mazání účtu: {str(e)}"

    def total_amount(self):
        """Vrátí celkový součet financí ve všech účtech."""
        try:
            connection = get_db_connection()
            with connection.cursor() as cursor:
                cursor.execute("SELECT SUM(balance) AS total FROM accounts")
                row = cursor.fetchone()
                return f"BA {int(row['total'])}" if row and row['total'] is not None else "BA 0"

        except Exception as e:
            return f"ER Chyba při získávání celkového zůstatku: {str(e)}"

    def num_clients(self):
        """Vrátí počet klientů (účtů)."""
        try:
            connection = get_db_connection()
            with connection.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) AS count FROM accounts")
                row = cursor.fetchone()
                return f"BN {row['count']}" if row else "BN 0"

        except Exception as e:
            return f"ER Chyba při získávání počtu klientů: {str(e)}"


def get_time():
    """Vrátí aktuální čas ve formátu YYYY-MM-DD HH:MM:SS."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def log_transaction(message):
    """Zapíše zprávu do souboru bank.log s časovou značkou."""
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"{message}\n")


def get_db_connection():
    """Vrátí připojení k databázi."""
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        cursorclass=pymysql.cursors.DictCursor
    )
