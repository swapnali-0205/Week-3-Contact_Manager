import unittest
from contacts_manager import validate_name, validate_phone, validate_email


class TestContactValidation(unittest.TestCase):

    def test_name(self):
        self.assertTrue(validate_name("John Doe"))
        self.assertFalse(validate_name("J1"))

    def test_phone(self):
        self.assertTrue(validate_phone("+1234567890"))
        self.assertFalse(validate_phone("123-abc"))

    def test_email(self):
        self.assertTrue(validate_email("test@example.com"))
        self.assertFalse(validate_email("test@com"))


if __name__ == "__main__":
    unittest.main()
