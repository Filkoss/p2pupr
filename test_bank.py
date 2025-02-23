import unittest
from bank import Bank, get_db_connection


class TestBank(unittest.TestCase):

    def setUp(self):
        """Inicializuje testovací instance banky."""
        self.bank = Bank("192.168.68.100")
        self.connection = get_db_connection()

    def test_create_account(self):
        """Test vytvoření účtu."""
        response = self.bank.create_account()
        self.assertTrue(response.startswith("AC"), "Chyba: Účet nebyl správně vytvořen.")

    def test_deposit(self):
        """Test vkladu na účet."""
        acc_id = 10001  # Nahraď platným číslem účtu pro testování
        response = self.bank.deposit(acc_id, 500)
        self.assertTrue(response.startswith("AD"), "Chyba: Vklad se neprovedl správně.")

    def test_withdraw(self):
        """Test výběru z účtu."""
        acc_id = 10001  # Nahraď platným číslem účtu pro testování
        response = self.bank.withdraw(acc_id, 300)
        self.assertTrue(response.startswith("AW"), "Chyba: Výběr se neprovedl správně.")

    def test_get_balance(self):
        """Test získání zůstatku."""
        acc_id = 10001  # Nahraď platným číslem účtu pro testování
        response = self.bank.get_balance(acc_id)
        self.assertTrue(response.startswith("AB"), "Chyba: Zůstatek nebyl správně načten.")

    def test_remove_account(self):
        """Test odstranění účtu."""
        acc_id = 10001  # Nahraď platným číslem účtu pro testování
        response = self.bank.remove_account(acc_id)
        self.assertTrue(response.startswith("AR") or response.startswith("ER"), "Chyba: Účet nebyl správně smazán.")

if __name__ == "__main__":
    unittest.main()
