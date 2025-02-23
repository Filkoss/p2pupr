import mysql.connector
from mysql.connector import Error
import config


def connect():
    """Připojí se k databázi a vrátí spojení."""
    try:
        conn = mysql.connector.connect(
            host=config.DB_HOST,
            user=config.DB_USER,
            password=config.DB_PASSWORD,
            database=config.DB_NAME
        )
        if conn.is_connected():
            print("✅ Připojeno k databázi")
            return conn
    except Error as e:
        print(f"❌ Chyba při připojení k MySQL: {e}")
        return None

def create_account():
    """Vytvoří nový bankovní účet a vrátí ID účtu."""
    conn = connect()
    if conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO accounts (balance) VALUES (0.00)")
        conn.commit()
        account_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return account_id

def get_balance(account_id):
    """Vrátí zůstatek účtu podle ID."""
    conn = connect()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT balance FROM accounts WHERE id = %s", (account_id,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        if result:
            return result[0]
        else:
            return None

def deposit(account_id, amount):
    """Přidá částku na účet."""
    conn = connect()
    if conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE accounts SET balance = balance + %s WHERE id = %s", (amount, account_id))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    return False

def withdraw(account_id, amount):
    """Odebere částku z účtu, pokud je dostatek peněz."""
    balance = get_balance(account_id)
    if balance is not None and balance >= amount:
        conn = connect()
        if conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE accounts SET balance = balance - %s WHERE id = %s", (amount, account_id))
            conn.commit()
            cursor.close()
            conn.close()
            return True
    return False
