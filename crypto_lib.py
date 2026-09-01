"""
Biblioteca de Algoritmos Criptográficos
SecureDocs - Missão 1: Precisamos de matemática

Implementação de operações matemáticas fundamentais para criptografia:
- Aritmética modular
- MDC (Máximo Divisor Comum)
- Algoritmo de Euclides
- Algoritmo Estendido de Euclides
- Inverso Multiplicativo
- Números Primos
- Função φ de Euler (Totient)
- Exponenciação Modular
- Teorema Chinês do Resto
"""

import random
from typing import Tuple


class CryptoMath:
    """Classe contendo operações matemáticas para criptografia."""

    # ============== MDC e Algoritmo de Euclides ==============
    
    @staticmethod
    def gcd(a: int, b: int) -> int:
        """
        Calcula o Máximo Divisor Comum (MDC) usando Algoritmo de Euclides.
        
        Args:
            a: Primeiro número
            b: Segundo número
            
        Returns:
            MDC de a e b
            
        Exemplo:
            >>> CryptoMath.gcd(48, 18)
            6
        """
        a, b = abs(a), abs(b)
        while b != 0:
            a, b = b, a % b
        return a

    @staticmethod
    def extended_gcd(a: int, b: int) -> Tuple[int, int, int]:
        """
        Algoritmo Estendido de Euclides.
        Retorna (gcd, x, y) tal que: a*x + b*y = gcd(a, b)
        
        Args:
            a: Primeiro número
            b: Segundo número
            
        Returns:
            Tupla (gcd, x, y) onde gcd = mdc(a,b) e a*x + b*y = gcd
            
        Exemplo:
            >>> gcd, x, y = CryptoMath.extended_gcd(10, 6)
            >>> gcd
            2
            >>> 10*x + 6*y == gcd
            True
        """
        if b == 0:
            return a, 1, 0
        
        gcd, x1, y1 = CryptoMath.extended_gcd(b, a % b)
        x = y1
        y = x1 - (a // b) * y1
        
        return gcd, x, y

    # ============== Aritmética Modular ==============

    @staticmethod
    def mod_inverse(a: int, m: int) -> int:
        """
        Calcula o inverso multiplicativo de a módulo m.
        Retorna x tal que (a * x) % m = 1
        
        Args:
            a: Número para o qual encontrar o inverso
            m: Módulo
            
        Returns:
            Inverso multiplicativo de a módulo m
            
        Raises:
            ValueError: Se o inverso não existe (gcd(a,m) != 1)
            
        Exemplo:
            >>> CryptoMath.mod_inverse(3, 11)
            4
            >>> (3 * 4) % 11
            1
        """
        gcd, x, _ = CryptoMath.extended_gcd(a, m)
        
        if gcd != 1:
            raise ValueError(f"Inverso multiplicativo não existe para {a} mod {m}")
        
        return x % m

    @staticmethod
    def mod_exp(base: int, exp: int, mod: int) -> int:
        """
        Calcula (base^exp) % mod de forma eficiente usando exponenciação modular.
        Usa algoritmo de exponenciação rápida (binary exponentiation).
        
        Args:
            base: Base da exponenciação
            exp: Expoente
            mod: Módulo
            
        Returns:
            (base^exp) % mod
            
        Exemplo:
            >>> CryptoMath.mod_exp(2, 10, 1000)
            24
            >>> (2**10) % 1000
            24
        """
        result = 1
        base = base % mod
        
        while exp > 0:
            if exp % 2 == 1:
                result = (result * base) % mod
            exp = exp >> 1
            base = (base * base) % mod
        
        return result

    # ============== Números Primos ==============

    @staticmethod
    def is_prime(n: int, k: int = 40) -> bool:
        """
        Testa se um número é primo usando Teste de Miller-Rabin.
        Probabilístico com probabilidade de erro < 4^(-k)
        
        Args:
            n: Número a testar
            k: Número de rodadas (quanto maior, mais confiável)
            
        Returns:
            True se provavelmente primo, False se composição
            
        Exemplo:
            >>> CryptoMath.is_prime(17)
            True
            >>> CryptoMath.is_prime(16)
            False
        """
        if n < 2:
            return False
        if n == 2 or n == 3:
            return True
        if n % 2 == 0:
            return False
        
        # Escreve n-1 como 2^r * d
        r = 0
        d = n - 1
        while d % 2 == 0:
            r += 1
            d //= 2
        
        # Testa k vezes
        for _ in range(k):
            a = random.randint(2, n - 2)
            x = CryptoMath.mod_exp(a, d, n)
            
            if x == 1 or x == n - 1:
                continue
            
            for _ in range(r - 1):
                x = CryptoMath.mod_exp(x, 2, n)
                if x == n - 1:
                    break
            else:
                return False
        
        return True

    @staticmethod
    def find_prime(bits: int) -> int:
        """
        Encontra um número primo aleatório com o número especificado de bits.
        
        Args:
            bits: Número de bits desejados
            
        Returns:
            Um número primo com aproximadamente 'bits' bits
            
        Exemplo:
            >>> prime = CryptoMath.find_prime(16)
            >>> CryptoMath.is_prime(prime)
            True
        """
        while True:
            n = random.getrandbits(bits)
            n |= (1 << bits - 1) | 1  # Garante que tem 'bits' bits e é ímpar
            if CryptoMath.is_prime(n):
                return n

    # ============== Função de Euler (Totient) ==============

    @staticmethod
    def euler_totient(n: int) -> int:
        """
        Calcula φ(n) - Função Totiente de Euler.
        Conta quantos inteiros positivos <= n são coprimos com n.
        
        Para primos p: φ(p) = p - 1
        Para p*q (primos): φ(p*q) = (p-1)*(q-1)
        
        Args:
            n: Número para calcular φ(n)
            
        Returns:
            φ(n)
            
        Exemplo:
            >>> CryptoMath.euler_totient(12)
            4
            >>> CryptoMath.euler_totient(7)
            6
        """
        result = n
        p = 2
        
        while p * p <= n:
            if n % p == 0:
                while n % p == 0:
                    n //= p
                result -= result // p
            p += 1
        
        if n > 1:
            result -= result // n
        
        return result

    @staticmethod
    def euler_totient_pq(p: int, q: int) -> int:
        """
        Calcula φ(n) quando n = p*q (p e q primos distintos).
        Otimizado: φ(p*q) = (p-1)*(q-1)
        
        Args:
            p: Primeiro número primo
            q: Segundo número primo
            
        Returns:
            φ(p*q) = (p-1)*(q-1)
            
        Exemplo:
            >>> CryptoMath.euler_totient_pq(5, 7)
            24
        """
        return (p - 1) * (q - 1)

    # ============== Teorema Chinês do Resto ==============

    @staticmethod
    def chinese_remainder_theorem(remainders: list, moduli: list) -> int:
        """
        Resolve sistema de congruências usando Teorema Chinês do Resto.
        Encontra x tal que:
            x ≡ remainders[0] (mod moduli[0])
            x ≡ remainders[1] (mod moduli[1])
            ...
        
        Requer que moduli sejam coprimos entre si.
        
        Args:
            remainders: Lista de restos
            moduli: Lista de módulos (devem ser coprimos)
            
        Returns:
            x tal que satisfaz todos os sistema de congruências
            
        Raises:
            ValueError: Se moduli não são coprimos
            
        Exemplo:
            >>> x = CryptoMath.chinese_remainder_theorem([2, 3, 2], [3, 5, 7])
            >>> x % 3 == 2 and x % 5 == 3 and x % 7 == 2
            True
        """
        if len(remainders) != len(moduli):
            raise ValueError("Tamanho de remainders e moduli devem ser iguais")
        
        # Verifica se moduli são coprimos
        for i in range(len(moduli)):
            for j in range(i + 1, len(moduli)):
                if CryptoMath.gcd(moduli[i], moduli[j]) != 1:
                    raise ValueError(f"Módulos {moduli[i]} e {moduli[j]} não são coprimos")
        
        M = 1
        for m in moduli:
            M *= m
        
        x = 0
        for i in range(len(remainders)):
            Mi = M // moduli[i]
            yi = CryptoMath.mod_inverse(Mi, moduli[i])
            x += remainders[i] * Mi * yi
        
        return x % M

    # ============== Utilitários ==============

    @staticmethod
    def are_coprime(a: int, b: int) -> bool:
        """
        Verifica se dois números são coprimos (mdc = 1).
        
        Args:
            a: Primeiro número
            b: Segundo número
            
        Returns:
            True se são coprimos, False caso contrário
        """
        return CryptoMath.gcd(a, b) == 1

    @staticmethod
    def lcm(a: int, b: int) -> int:
        """
        Calcula o Mínimo Múltiplo Comum (MMC).
        
        Args:
            a: Primeiro número
            b: Segundo número
            
        Returns:
            MMC de a e b
        """
        return abs(a * b) // CryptoMath.gcd(a, b)


if __name__ == "__main__":
    print("=" * 60)
    print("BIBLIOTECA DE CRIPTOGRAFIA - MISSÃO 1")
    print("=" * 60)
    
    # Exemplos de uso
    print("\n1. MDC e Algoritmo de Euclides")
    print(f"   MDC(48, 18) = {CryptoMath.gcd(48, 18)}")
    
    print("\n2. Algoritmo Estendido de Euclides")
    gcd, x, y = CryptoMath.extended_gcd(10, 6)
    print(f"   gcd, x, y = extended_gcd(10, 6)")
    print(f"   Resultado: gcd={gcd}, x={x}, y={y}")
    print(f"   Verificação: 10*{x} + 6*{y} = {10*x + 6*y}")
    
    print("\n3. Inverso Multiplicativo")
    inv = CryptoMath.mod_inverse(3, 11)
    print(f"   Inverso de 3 mod 11 = {inv}")
    print(f"   Verificação: (3 * {inv}) % 11 = {(3 * inv) % 11}")
    
    print("\n4. Exponenciação Modular")
    result = CryptoMath.mod_exp(2, 10, 1000)
    print(f"   (2^10) % 1000 = {result}")
    
    print("\n5. Testes de Primalidade")
    test_numbers = [17, 19, 97, 100, 121]
    for num in test_numbers:
        print(f"   {num} é primo? {CryptoMath.is_prime(num)}")
    
    print("\n6. Função φ de Euler (Totient)")
    print(f"   φ(12) = {CryptoMath.euler_totient(12)}")
    print(f"   φ(7) = {CryptoMath.euler_totient(7)}")
    print(f"   φ(5*7) = {CryptoMath.euler_totient_pq(5, 7)}")
    
    print("\n7. Coprimalidade")
    print(f"   MDC(15, 28) = {CryptoMath.gcd(15, 28)}")
    print(f"   15 e 28 são coprimos? {CryptoMath.are_coprime(15, 28)}")
    
    print("\n8. Mínimo Múltiplo Comum (MMC)")
    print(f"   MMC(12, 18) = {CryptoMath.lcm(12, 18)}")
    
    print("\n9. Teorema Chinês do Resto")
    x = CryptoMath.chinese_remainder_theorem([2, 3, 2], [3, 5, 7])
    print(f"   Solução para x≡2(mod 3), x≡3(mod 5), x≡2(mod 7)")
    print(f"   x = {x}")
    print(f"   Verificação: {x}%3={x%3}, {x}%5={x%5}, {x}%7={x%7}")
    
    print("\n" + "=" * 60)
