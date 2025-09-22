"""import unittest
from ex1_palindromo import is_palindrome

class TestPalindromo(unittest.TestCase):
    def test_frases_portugues(self):
        self.assertTrue(is_palindrome("A grama é amarga"))
        self.assertTrue(is_palindrome("Socorram-me, subi no ônibus em Marrocos"))
        self.assertTrue(is_palindrome("Anotaram a data da maratona"))

    def test_nao_palindromo(self):
        self.assertFalse(is_palindrome("saas"))
        self.assertFalse(is_palindrome("Python"))

    def test_edge_cases(self):
        self.assertTrue(is_palindrome(""))              # string vazia é palíndromo
        self.assertTrue(is_palindrome("!!!..."))        # só pontuação
        with self.assertRaises(ValueError):
            is_palindrome(None)

if __name__ == "__main__":
    unittest.main()

# python -m unittest -v test_ex1_palindromo.py
"""