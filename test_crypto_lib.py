"""
Testes unitários para a Biblioteca de Criptografia
SecureDocs - Missão 1

Valida a implementação de todos os algoritmos matemáticos.
"""

import unittest
from crypto_lib import CryptoMath


class TestMDCAndEuclides(unittest.TestCase):
    """Testes para MDC e Algoritmo de Euclides."""
    
    def test_mdc_basic(self):
        """Testa MDC com casos básicos."""
        self.assertEqual(CryptoMath.mdc(48, 18), 6)
        self.assertEqual(CryptoMath.mdc(100, 50), 50)
        self.assertEqual(CryptoMath.mdc(17, 19), 1)
    
    def test_mdc_with_zero(self):
        """Testa MDC com zero."""
        self.assertEqual(CryptoMath.mdc(5, 0), 5)
        self.assertEqual(CryptoMath.mdc(0, 5), 5)
    
    def test_mdc_negative(self):
        """Testa MDC com números negativos."""
        self.assertEqual(CryptoMath.mdc(-48, 18), 6)
        self.assertEqual(CryptoMath.mdc(48, -18), 6)
    
    def test_mdc_estendido(self):
        """Testa Algoritmo Estendido de Euclides."""
        mdc, x, y = CryptoMath.mdc_estendido(10, 6)
        self.assertEqual(mdc, 2)
        self.assertEqual(10*x + 6*y, mdc)
    
    def test_mdc_estendido_coprime(self):
        """Testa mdc_estendido com números coprimos."""
        mdc, x, y = CryptoMath.mdc_estendido(7, 5)
        self.assertEqual(mdc, 1)
        self.assertEqual(7*x + 5*y, 1)


class TestModularArithmetic(unittest.TestCase):
    """Testes para aritmética modular."""
    
    def test_inverso_modular_basic(self):
        """Testa inverso multiplicativo básico."""
        inv = CryptoMath.inverso_modular(3, 11)
        self.assertEqual((3 * inv) % 11, 1)
    
    def test_inverso_modular_various(self):
        """Testa inverso multiplicativo com vários valores."""
        test_cases = [(3, 11), (7, 26), (5, 12), (2, 5)]
        for a, m in test_cases:
            inv = CryptoMath.inverso_modular(a, m)
            self.assertEqual((a * inv) % m, 1)
    
    def test_inverso_modular_not_exists(self):
        """Testa quando inverso não existe."""
        with self.assertRaises(ValueError):
            CryptoMath.inverso_modular(6, 9)  # mdc(6,9) = 3 ≠ 1
    
    def test_exponenciacao_modular_basic(self):
        """Testa exponenciação modular."""
        # (2^10) % 1000 = 1024 % 1000 = 24
        self.assertEqual(CryptoMath.exponenciacao_modular(2, 10, 1000), 24)
    
    def test_exponenciacao_modular_large(self):
        """Testa exponenciação modular com números grandes."""
        # Verifica que funciona eficientemente com números grandes
        result = CryptoMath.exponenciacao_modular(123456789, 987654321, 10**9 + 7)
        self.assertIsInstance(result, int)
        self.assertGreaterEqual(result, 0)
        self.assertLess(result, 10**9 + 7)
    
    def test_exponenciacao_modular_against_pow(self):
        """Verifica exponenciacao_modular contra pow built-in."""
        cases = [(2, 10, 1000), (3, 5, 7), (5, 3, 11)]
        for base, exp, mod in cases:
            self.assertEqual(
                CryptoMath.exponenciacao_modular(base, exp, mod),
                pow(base, exp, mod)
            )


class TestPrimes(unittest.TestCase):
    """Testes para testes de primalidade."""
    
    def test_eh_primo_small_primes(self):
        """Testa números primos pequenos."""
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31]
        for p in primes:
            self.assertTrue(CryptoMath.eh_primo(p), f"{p} deveria ser primo")
    
    def test_eh_primo_composites(self):
        """Testa números compostos."""
        composites = [4, 6, 8, 9, 10, 12, 15, 20, 21, 25]
        for c in composites:
            self.assertFalse(CryptoMath.eh_primo(c), f"{c} não deveria ser primo")
    
    def test_eh_primo_edge_cases(self):
        """Testa casos extremos."""
        self.assertFalse(CryptoMath.eh_primo(0))
        self.assertFalse(CryptoMath.eh_primo(1))
        self.assertTrue(CryptoMath.eh_primo(2))
    
    def test_gerar_primo(self):
        """Testa geração de números primos."""
        for bits in [8, 16, 32]:
            prime = CryptoMath.gerar_primo(bits)
            self.assertTrue(CryptoMath.eh_primo(prime))
            # Verifica se tem aproximadamente 'bits' bits
            self.assertGreaterEqual(prime.bit_length(), bits - 1)
            self.assertLessEqual(prime.bit_length(), bits + 1)


class TestEulerTotient(unittest.TestCase):
    """Testes para a Função φ de Euler."""
    
    def test_totiente_euler_prime(self):
        """Testa φ(p) = p-1 para primo p."""
        primes = [5, 7, 11, 13]
        for p in primes:
            self.assertEqual(CryptoMath.totiente_euler(p), p - 1)
    
    def test_totiente_euler_known_values(self):
        """Testa φ com valores conhecidos."""
        test_cases = [
            (1, 1),
            (12, 4),   # φ(12) = φ(4*3) = 4
            (20, 8),   # φ(20) = φ(4*5) = 8
            (30, 8),   # φ(30) = φ(2*3*5) = 8
        ]
        for n, expected in test_cases:
            self.assertEqual(CryptoMath.totiente_euler(n), expected)
    
    def test_totiente_euler_pq(self):
        """Testa φ(p*q) para primos p, q."""
        cases = [(5, 7), (3, 11), (13, 17)]
        for p, q in cases:
            expected = (p - 1) * (q - 1)
            self.assertEqual(CryptoMath.totiente_euler_pq(p, q), expected)
            # Verifica consistência com totiente_euler
            self.assertEqual(
                CryptoMath.totiente_euler(p * q),
                CryptoMath.totiente_euler_pq(p, q)
            )


class TestChineseRemainderTheorem(unittest.TestCase):
    """Testes para Teorema Chinês do Resto."""
    
    def test_crt_basic(self):
        """Testa CRT com caso simples."""
        remainders = [2, 3, 2]
        moduli = [3, 5, 7]
        x = CryptoMath.teorema_chines_resto(remainders, moduli)
        
        # Verifica se a solução satisfaz todas as congruências
        self.assertEqual(x % 3, 2)
        self.assertEqual(x % 5, 3)
        self.assertEqual(x % 7, 2)
    
    def test_crt_two_equations(self):
        """Testa CRT com duas congruências."""
        x = CryptoMath.teorema_chines_resto([1, 2], [3, 5])
        self.assertEqual(x % 3, 1)
        self.assertEqual(x % 5, 2)
    
    def test_crt_non_coprime_raises(self):
        """Testa que CRT lança erro para módulos não coprimos."""
        with self.assertRaises(ValueError):
            CryptoMath.teorema_chines_resto([1, 2], [4, 6])  # mdc(4,6)=2
    
    def test_crt_different_sizes(self):
        """Testa CRT com diferentes tamanhos de listas."""
        with self.assertRaises(ValueError):
            CryptoMath.teorema_chines_resto([1, 2, 3], [5, 7])


class TestUtilities(unittest.TestCase):
    """Testes para funções utilitárias."""
    
    def test_sao_coprimos_true(self):
        """Testa números coprimos."""
        self.assertTrue(CryptoMath.sao_coprimos(7, 11))
        self.assertTrue(CryptoMath.sao_coprimos(15, 28))
    
    def test_sao_coprimos_false(self):
        """Testa números não coprimos."""
        self.assertFalse(CryptoMath.sao_coprimos(6, 9))
        self.assertFalse(CryptoMath.sao_coprimos(12, 18))
    
    def test_mmc_basic(self):
        """Testa cálculo do MMC."""
        self.assertEqual(CryptoMath.mmc(12, 18), 36)
        self.assertEqual(CryptoMath.mmc(7, 5), 35)
        self.assertEqual(CryptoMath.mmc(4, 6), 12)


if __name__ == '__main__':
    # Executa todos os testes com verbosidade
    unittest.main(verbosity=2)
