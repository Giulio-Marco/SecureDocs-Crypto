"""
Testes unitários para a Biblioteca de Criptografia - crypto_lib.py
"""

import unittest
from crypto_lib import CryptoMath

class Teste_Euclides(unittest.TestCase):

    def teste_mdcEuclides_simples(self):
        self.assertEqual(CryptoMath.mdc_euclides(48, 18), 6)
        self.assertEqual(CryptoMath.mdc_euclides(100, 50), 50)
        self.assertEqual(CryptoMath.mdc_euclides(17, 19), 1)
    
    def teste_mdcEuclides_zero(self): # = 0
        self.assertEqual(CryptoMath.mdc_euclides(5, 0), 5)
        self.assertEqual(CryptoMath.mdc_euclides(0, 5), 5)
    
    def teste_mdcEuclides_negativo(self): # < 0
        self.assertEqual(CryptoMath.mdc_euclides(-48, 18), 6)
        self.assertEqual(CryptoMath.mdc_euclides(48, -18), 6)
    
    def teste_mdcEstendidoEuclides(self):
        mdc, x, y = CryptoMath.mdc_euclidesEstendido(10, 6)
        self.assertEqual(mdc, 2)
        self.assertEqual(10 * x + 6 * y, mdc)
    
    def teste_mdcEstendidoEuclides_coprimo(self): # mdc(a, b) == 1
        mdc, x, y = CryptoMath.mdc_euclidesEstendido(7, 5)
        self.assertEqual(mdc, 1)
        self.assertEqual(7 * x + 5 * y, 1)

class Teste_AritmeticaModular(unittest.TestCase):

    def teste_inversoMulti_simples(self):
        inv = CryptoMath.inverso_multi(3, 11)
        self.assertEqual((3 * inv) % 11, 1)
    
    def teste_inversoMulti_valores(self): # Vários valores
        casos_testes = [(3, 11), (7, 26), (5, 12), (2, 5)]
        for a, m in casos_testes:
            inv = CryptoMath.inverso_multi(a, m)
            self.assertEqual((a * inv) % m, 1)
    
    def teste_inverso_multi_naoExiste(self): # Inverso que não existe
        with self.assertRaises(ValueError):
            CryptoMath.inverso_multi(6, 9)  # mdc(6,9) = 3 --> 3 ≠ 1
    
    def teste_expMod_simples(self):
        # (2^10) % 1000 = 1024 % 1000 = 24
        self.assertEqual(CryptoMath.exp_mod(2, 10, 1000), 24)
    
    def teste_expMod_grande(self): # Com grandes valores
        resultado = CryptoMath.exp_mod(123456789, 987654321, 10**9 + 7)
        self.assertIsInstance(resultado, int)
        self.assertGreaterEqual(resultado, 0)
        self.assertLess(resultado, 10**9 + 7)
    
    def teste_expMod_pow(self): # Verifica exp_mod contra pow built-in
        casos = [(2, 10, 1000), (3, 5, 7), (5, 3, 11)]
        for base, exp, mod in casos:
            self.assertEqual(
                CryptoMath.exp_mod(base, exp, mod),
                pow(base, exp, mod)
            )

class Teste_Primo(unittest.TestCase):

    def teste_ehPrimo_pequeno(self): # Pequenos valores
        primos = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31]
        for p in primos:
            self.assertTrue(CryptoMath.ehPrimo(p), f"{p} deveria ser primo")
    
    def teste_ehPrimo_composto(self): # Número composto
        composto = [4, 6, 8, 9, 10, 12, 15, 20, 21, 25]
        for c in composto:
            self.assertFalse(CryptoMath.ehPrimo(c), f"{c} não deveria ser primo")
    
    def teste_ehPrimo_extremo(self): # Extremo
        self.assertFalse(CryptoMath.ehPrimo(0))
        self.assertFalse(CryptoMath.ehPrimo(1))
        self.assertTrue(CryptoMath.ehPrimo(2))
    
    def teste_acharPrimo(self):
        for bits in [8, 16, 32]:
            primo = CryptoMath.acharPrimo(bits)
            self.assertTrue(CryptoMath.ehPrimo(primo))
            # Verifica se tem aproximadamente 'bits' bits
            self.assertGreaterEqual(primo.bit_length(), bits - 1)
            self.assertLessEqual(primo.bit_length(), bits + 1)

class Teste_EulerTotiente(unittest.TestCase):
    
    def teste_eulerTotiente_primo(self):
        primos = [5, 7, 11, 13]
        for p in primos:
            self.assertEqual(CryptoMath.euler_totiente(p), p - 1)
    
    def teste_eulerTotiente_conhecido(self):
        casos_testes = [
            (1, 1),
            (12, 4),   # φ(12) = φ(4*3) = 4
            (20, 8),   # φ(20) = φ(4*5) = 8
            (30, 8),   # φ(30) = φ(2*3*5) = 8
        ]
        for n, possivel in casos_testes:
            self.assertEqual(CryptoMath.euler_totiente(n), possivel)
    
    def teste_eulerTotiente_pq(self):
        casos = [(5, 7), (3, 11), (13, 17)]
        for p, q in casos:
            possivel = (p - 1) * (q - 1)
            self.assertEqual(CryptoMath.euler_totiente_pq(p, q), possivel)
            # Verifica consistência com euler_totiente
            self.assertEqual(
                CryptoMath.euler_totiente(p * q),
                CryptoMath.euler_totiente_pq(p, q)
            )

class Teste_ChinesResto(unittest.TestCase):

    def teste_chinesResto_simples(self):
        restos = [2, 3, 2]
        modulos = [3, 5, 7]
        x = CryptoMath.chines_resto(restos, modulos)
        
        # Verifica se a solução satisfaz todas as congruências
        self.assertEqual(x % 3, 2)
        self.assertEqual(x % 5, 3)
        self.assertEqual(x % 7, 2)
    
    def teste_chinesResto_duasEq(self):
        x = CryptoMath.chines_resto([1, 2], [3, 5])
        self.assertEqual(x % 3, 1)
        self.assertEqual(x % 5, 2)
    
    def teste_chinesPrimo_naoCoprimo(self):
        with self.assertRaises(ValueError):
            CryptoMath.chines_resto([1, 2], [4, 6])  # mdc(4,6) = 2
    
    def teste_chinesPrimo_difTam(self): # Listas de diferentes tamanhos
        with self.assertRaises(ValueError):
            CryptoMath.chines_resto([1, 2, 3], [5, 7])

class Teste_Utils(unittest.TestCase):

    def teste_saoCoprimos_true(self): # Coprimos
        self.assertTrue(CryptoMath.saoCoprimo(7, 11))
        self.assertTrue(CryptoMath.saoCoprimo(15, 28))
    
    def teste_saoCoprimos_false(self): # Não coprimos
        self.assertFalse(CryptoMath.saoCoprimo(6, 9))
        self.assertFalse(CryptoMath.saoCoprimo(12, 18))
    
    def teste_mmc_simples(self):
        self.assertEqual(CryptoMath.mmc(12, 18), 36)
        self.assertEqual(CryptoMath.mmc(7, 5), 35)
        self.assertEqual(CryptoMath.mmc(4, 6), 12)


if __name__ == '__main__':
    unittest.main(verbosity=2)
