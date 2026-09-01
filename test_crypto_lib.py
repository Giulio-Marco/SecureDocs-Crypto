"""
Testes unitários para a Biblioteca de Criptografia
SecureDocs - Missão 1

Valida a implementação de todos os algoritmos matemáticos.
"""

import unittest
from crypto_lib import CryptoMath


class TestMDCAndEuclides(unittest.TestCase):
    """Testes para MDC e Algoritmo de Euclides."""
    
    def test_gcd_basic(self):
        """Testa MDC com casos básicos."""
        self.assertEqual(CryptoMath.gcd(48, 18), 6)
        self.assertEqual(CryptoMath.gcd(100, 50), 50)
        self.assertEqual(CryptoMath.gcd(17, 19), 1)
    
    def test_gcd_with_zero(self):
        """Testa MDC com zero."""
        self.assertEqual(CryptoMath.gcd(5, 0), 5)
        self.assertEqual(CryptoMath.gcd(0, 5), 5)
    
    def test_gcd_negative(self):
        """Testa MDC com números negativos."""
        self.assertEqual(CryptoMath.gcd(-48, 18), 6)
        self.assertEqual(CryptoMath.gcd(48, -18), 6)
    
    def test_extended_gcd(self):
        """Testa Algoritmo Estendido de Euclides."""
        gcd, x, y = CryptoMath.extended_gcd(10, 6)
        self.assertEqual(gcd, 2)
        self.assertEqual(10*x + 6*y, gcd)
    
    def test_extended_gcd_coprime(self):
        """Testa extended_gcd com números coprimos."""
        gcd, x, y = CryptoMath.extended_gcd(7, 5)
        self.assertEqual(gcd, 1)
        self.assertEqual(7*x + 5*y, 1)


class TestModularArithmetic(unittest.TestCase):
    """Testes para aritmética modular."""
    
    def test_mod_inverse_basic(self):
        """Testa inverso multiplicativo básico."""
        inv = CryptoMath.mod_inverse(3, 11)
        self.assertEqual((3 * inv) % 11, 1)
    
    def test_mod_inverse_various(self):
        """Testa inverso multiplicativo com vários valores."""
        test_cases = [(3, 11), (7, 26), (5, 12), (2, 5)]
        for a, m in test_cases:
            inv = CryptoMath.mod_inverse(a, m)
            self.assertEqual((a * inv) % m, 1)
    
    def test_mod_inverse_not_exists(self):
        """Testa quando inverso não existe."""
        with self.assertRaises(ValueError):
            CryptoMath.mod_inverse(6, 9)  # gcd(6,9) = 3 ≠ 1
    
    def test_mod_exp_basic(self):
        """Testa exponenciação modular."""
        # (2^10) % 1000 = 1024 % 1000 = 24
        self.assertEqual(CryptoMath.mod_exp(2, 10, 1000), 24)
    
    def test_mod_exp_large(self):
        """Testa exponenciação modular com números grandes."""
        # Verifica que funciona eficientemente com números grandes
        result = CryptoMath.mod_exp(123456789, 987654321, 10**9 + 7)
        self.assertIsInstance(result, int)
        self.assertGreaterEqual(result, 0)
        self.assertLess(result, 10**9 + 7)
    
    def test_mod_exp_against_pow(self):
        """Verifica mod_exp contra pow built-in."""
        cases = [(2, 10, 1000), (3, 5, 7), (5, 3, 11)]
        for base, exp, mod in cases:
            self.assertEqual(
                CryptoMath.mod_exp(base, exp, mod),
                pow(base, exp, mod)
            )


class TestPrimes(unittest.TestCase):
    """Testes para testes de primalidade."""
    
    def test_is_prime_small_primes(self):
        """Testa números primos pequenos."""
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31]
        for p in primes:
            self.assertTrue(CryptoMath.is_prime(p), f"{p} deveria ser primo")
    
    def test_is_prime_composites(self):
        """Testa números compostos."""
        composites = [4, 6, 8, 9, 10, 12, 15, 20, 21, 25]
        for c in composites:
            self.assertFalse(CryptoMath.is_prime(c), f"{c} não deveria ser primo")
    
    def test_is_prime_edge_cases(self):
        """Testa casos extremos."""
        self.assertFalse(CryptoMath.is_prime(0))
        self.assertFalse(CryptoMath.is_prime(1))
        self.assertTrue(CryptoMath.is_prime(2))
    
    def test_find_prime(self):
        """Testa geração de números primos."""
        for bits in [8, 16, 32]:
            prime = CryptoMath.find_prime(bits)
            self.assertTrue(CryptoMath.is_prime(prime))
            # Verifica se tem aproximadamente 'bits' bits
            self.assertGreaterEqual(prime.bit_length(), bits - 1)
            self.assertLessEqual(prime.bit_length(), bits + 1)


class TestEulerTotient(unittest.TestCase):
    """Testes para a Função φ de Euler."""
    
    def test_euler_totient_prime(self):
        """Testa φ(p) = p-1 para primo p."""
        primes = [5, 7, 11, 13]
        for p in primes:
            self.assertEqual(CryptoMath.euler_totient(p), p - 1)
    
    def test_euler_totient_known_values(self):
        """Testa φ com valores conhecidos."""
        test_cases = [
            (1, 1),
            (12, 4),   # φ(12) = φ(4*3) = 4
            (20, 8),   # φ(20) = φ(4*5) = 8
            (30, 8),   # φ(30) = φ(2*3*5) = 8
        ]
        for n, expected in test_cases:
            self.assertEqual(CryptoMath.euler_totient(n), expected)
    
    def test_euler_totient_pq(self):
        """Testa φ(p*q) para primos p, q."""
        cases = [(5, 7), (3, 11), (13, 17)]
        for p, q in cases:
            expected = (p - 1) * (q - 1)
            self.assertEqual(CryptoMath.euler_totient_pq(p, q), expected)
            # Verifica consistência com euler_totient
            self.assertEqual(
                CryptoMath.euler_totient(p * q),
                CryptoMath.euler_totient_pq(p, q)
            )


class TestChineseRemainderTheorem(unittest.TestCase):
    """Testes para Teorema Chinês do Resto."""
    
    def test_crt_basic(self):
        """Testa CRT com caso simples."""
        remainders = [2, 3, 2]
        moduli = [3, 5, 7]
        x = CryptoMath.chinese_remainder_theorem(remainders, moduli)
        
        # Verifica se a solução satisfaz todas as congruências
        self.assertEqual(x % 3, 2)
        self.assertEqual(x % 5, 3)
        self.assertEqual(x % 7, 2)
    
    def test_crt_two_equations(self):
        """Testa CRT com duas congruências."""
        x = CryptoMath.chinese_remainder_theorem([1, 2], [3, 5])
        self.assertEqual(x % 3, 1)
        self.assertEqual(x % 5, 2)
    
    def test_crt_non_coprime_raises(self):
        """Testa que CRT lança erro para módulos não coprimos."""
        with self.assertRaises(ValueError):
            CryptoMath.chinese_remainder_theorem([1, 2], [4, 6])  # gcd(4,6)=2
    
    def test_crt_different_sizes(self):
        """Testa CRT com diferentes tamanhos de listas."""
        with self.assertRaises(ValueError):
            CryptoMath.chinese_remainder_theorem([1, 2, 3], [5, 7])


class TestUtilities(unittest.TestCase):
    """Testes para funções utilitárias."""
    
    def test_are_coprime_true(self):
        """Testa números coprimos."""
        self.assertTrue(CryptoMath.are_coprime(7, 11))
        self.assertTrue(CryptoMath.are_coprime(15, 28))
    
    def test_are_coprime_false(self):
        """Testa números não coprimos."""
        self.assertFalse(CryptoMath.are_coprime(6, 9))
        self.assertFalse(CryptoMath.are_coprime(12, 18))
    
    def test_lcm_basic(self):
        """Testa cálculo do MMC."""
        self.assertEqual(CryptoMath.lcm(12, 18), 36)
        self.assertEqual(CryptoMath.lcm(7, 5), 35)
        self.assertEqual(CryptoMath.lcm(4, 6), 12)


if __name__ == '__main__':
    # Executa todos os testes com verbosidade
    unittest.main(verbosity=2)
