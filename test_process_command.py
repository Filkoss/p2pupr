import unittest
from bank import Bank
from process_command import process_command

class TestProcessCommand(unittest.TestCase):

    def setUp(self):
        """Inicializuje testovací bankovní instanci."""
        self.bank = Bank("192.168.68.100")

    def test_command_bc(self):
        """Test příkazu BC."""
        response = process_command("BC", self.bank)
        self.assertTrue(response.startswith("BC"), "Chyba: Příkaz BC nefunguje správně.")

    def test_command_ac(self):
        """Test příkazu AC."""
        response = process_command("AC", self.bank)
        self.assertTrue(response.startswith("AC"), "Chyba: Příkaz AC nefunguje správně.")

    def test_command_bn(self):
        """Test příkazu BN."""
        response = process_command("BN", self.bank)
        self.assertTrue(response.startswith("BN"), "Chyba: Příkaz BN nefunguje správně.")

    def test_command_invalid(self):
        """Test neplatného příkazu."""
        response = process_command("XYZ", self.bank)
        self.assertEqual(response, "ER Neplatný příkaz", "Chyba: Neplatný příkaz nebyl správně odmítnut.")

if __name__ == "__main__":
    unittest.main()
