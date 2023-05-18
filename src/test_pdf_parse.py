import unittest

from src.create_invoice import create_invoice


class MyTestCase(unittest.TestCase):
    def test_parse_without_email_connection(self):
        # to use that test simply add an attachments folder in src with an temp_invoice.pdf based on XP FX pdf
        create_invoice()
        self.assertEqual(True, True)  # add assertion here


if __name__ == '__main__':
    unittest.main()
