"""
Biblioteca de Algoritmos Criptográficos

Implementação de operações matemáticas fundamentais para criptografia:
- Aritmética modular
- Algoritmo de Euclides
- Algoritmo Estendido de Euclides
- Inverso Multiplicativo
- Exponenciação Modular
- Números Primos
- Função φ de Euler (Totient)
- Teorema Chinês do Resto
"""

import random
from typing import Tuple

class CryptoMath:

    @staticmethod
    def mdc_euclides(a: int, b: int) -> int:
        """
        Args:
            a: Primeiro número
            b: Segundo número
        Returns:
            MDC de a e b
        """
        a, b = abs(a), abs(b)
        while b != 0:
            a, b = b, a % b
        return a

    @staticmethod
    def mdc_euclidesEstendido(a: int, b: int) -> Tuple[int, int, int]:
        """
        Retorna (mdc_euclides, x, y) tal que: a * x + b * y = mdc_euclides(a, b)
        Args:
            a: Primeiro número
            b: Segundo número
        Returns:
            Tupla (mdc_euclides, x, y) onde mdc_euclides = mdc(a,b) e a * x + b * y = mdc_euclides
        """
        if b == 0:
            return a, 1, 0

        mdc_euclides, x1, y1 = CryptoMath.mdc_euclidesEstendido(b, a % b)
        x = y1
        y = x1 - (a // b) * y1

        return mdc_euclides, x, y

    @staticmethod
    def inverso_multi(a: int, m: int) -> int:
        """
        Retorna x tal que (a * x) % m = 1
        Args:
            a: Número para o qual encontrar o inverso
            m: Módulo
        Returns:
            Inverso multiplicativo de a módulo m
        Exceções:
            ValueError: Se o inverso não existe (mdc_euclides(a,m) != 1)
        """
        mdc_euclides, x, _ = CryptoMath.mdc_euclidesEstendido(a, m)

        if mdc_euclides != 1:
            raise ValueError(f"Inverso multiplicativo não existe para {a} mod {m}")

        return x % m

    @staticmethod
    def exp_mod(base: int, exp: int, mod: int) -> int:
        """
        Usa algoritmo de exponenciação rápida (binary exponentiation).
        Args:
            base: Base da exponenciação
            exp: Expoente
            mod: Módulo
        Returns:
            (base^exp) % mod
        """
        result = 1
        base = base % mod

        while exp > 0:
            if exp % 2 == 1:
                result = (result * base) % mod
            exp = exp >> 1
            base = (base * base) % mod

        return result

    @staticmethod
    def ehPrimo(n: int, k: int = 40) -> bool:
        """
        Testa se um número é primo usando Teste de Miller-Rabin.
        Probabilístico com probabilidade de erro < 4^(-k)
        Args:
            n: Número a testar
            k: Número de rodadas (quanto maior, mais confiável)
        Returns:
            True se primo, False de não primo
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

        for _ in range(k):
            a = random.randint(2, n - 2)
            x = CryptoMath.exp_mod(a, d, n)

            if x == 1 or x == n - 1:
                continue

            for _ in range(r - 1):
                x = CryptoMath.exp_mod(x, 2, n)
                if x == n - 1:
                    break
            else:
                return False

        return True

    @staticmethod
    def acharPrimo(bits: int) -> int:
        """
        Args:
            bits: Número de bits desejados
        Returns:
            Um número primo com aproximadamente 'bits' bits
        """
        while True:
            n = random.getrandbits(bits)
            n |= (1 << bits - 1) | 1  # Garante que tem 'bits' bits e é ímpar
            if CryptoMath.ehPrimo(n):
                return n

    @staticmethod
    def euler_totiente(n: int) -> int:
        """
        Conta quantos inteiros positivos <= n são coprimos com n.
        Para primos p: φ(p) = p - 1
        Para p*q (primos): φ(p*q) = (p-1)*(q-1)
        Args:
            n: Número para calcular φ(n)
        Returns:
            φ(n)
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
    def euler_totiente_pq(p: int, q: int) -> int:
        """
        Calcula φ(n) quando n = p*q (p e q primos distintos).
        Otimizado: φ(p*q) = (p-1)*(q-1)
        Args:
            p: Primeiro número primo
            q: Segundo número primo
        Returns:
            φ(p*q) = (p-1)*(q-1)
        """
        return (p - 1) * (q - 1)

    @staticmethod
    def chines_resto(restos: list, modulos: list) -> int:
        """
        Encontra x tal que:
            x ≡ restos[0] (mod modulos[0])
            x ≡ restos[1] (mod modulos[1])
            ...
        Requer que modulos sejam coprimos entre si.
        Args:
            restos: Lista de restos
            modulos: Lista de módulos (devem ser coprimos)
        Returns:
            x tal que satisfaz todos os sistema de congruências
        Exceções:
            ValueError: Se modulos não são coprimos
        """
        if len(restos) != len(modulos):
            raise ValueError("Tamanho de restos e modulos devem ser iguais")

        # Verifica se modulos são coprimos
        for i in range(len(modulos)):
            for j in range(i + 1, len(modulos)):
                if CryptoMath.mdc_euclides(modulos[i], modulos[j]) != 1:
                    raise ValueError(f"Módulos {modulos[i]} e {modulos[j]} não são coprimos")
        
        M = 1
        for m in modulos:
            M *= m
        
        x = 0
        for i in range(len(restos)):
            Mi = M // modulos[i]
            yi = CryptoMath.inverso_multi(Mi, modulos[i])
            x += restos[i] * Mi * yi
        
        return x % M

    @staticmethod
    def saoCoprimo(a: int, b: int) -> bool:
        """
        Args:
            a: Primeiro número
            b: Segundo número
        Returns:
            True se são coprimos, False caso contrário
        """
        return CryptoMath.mdc_euclides(a, b) == 1

    @staticmethod
    def mmc(a: int, b: int) -> int:
        """
        Args:
            a: Primeiro número
            b: Segundo número
        Returns:
            MMC de a e b
        """
        return abs(a * b) // CryptoMath.mdc_euclides(a, b)

def executar_menu_interativo() -> None:
    while True:
        print("\n=== Calculadora de Criptografia ===")
        print("1 - Algoritmo de Euclides (classico)")
        print("2 - Algoritmo Estendido de Euclides")
        print("3 - Aritmetica modular")
        print("4 - Teorema Chines do Resto")
        print("5 - Verificar se e primo")
        print("6 - Funcao de Euler phi(n)")
        print("7 - MMC")
        print("0 - Sair")

        opcao = input("Escolha uma opção: ").strip()

        try:
            if opcao == "1":
                primeiro = int(input("Digite o primeiro numero: "))
                segundo = int(input("Digite o segundo numero: "))
                print(f"Resultado: MDC({primeiro}, {segundo}) = "
                      f"{CryptoMath.mdc_euclides(primeiro, segundo)}")
            elif opcao == "2":
                primeiro = int(input("Digite o primeiro numero: "))
                segundo = int(input("Digite o segundo numero: "))
                mdc_euclides, x, y = CryptoMath.mdc_euclidesEstendido(primeiro, segundo)
                print(f"Resultado: MDC({primeiro}, {segundo}) = {mdc_euclides}")
                print(f"Coeficientes: x = {x}, y = {y} "
                      f"(verificacao: {primeiro}*{x} + {segundo}*{y} = {mdc_euclides})")
            elif opcao == "3":
                print("1 - Soma")
                print("2 - Subtracao")
                print("3 - Multiplicacao")
                print("4 - Exponenciacao")
                print("5 - Inverso multiplicativo")
                sub_opcao = input("Escolha uma operacao: ").strip()
                modulo = int(input("Digite o modulo: "))

                if modulo <= 0:
                    raise ValueError("O modulo deve ser maior que zero")

                if sub_opcao in {"1", "2", "3"}:
                    primeiro = int(input("Digite o primeiro numero: "))
                    segundo = int(input("Digite o segundo numero: "))
                    operacoes = {
                        "1": ("+", (primeiro + segundo) % modulo),
                        "2": ("-", (primeiro - segundo) % modulo),
                        "3": ("*", (primeiro * segundo) % modulo),
                    }
                    simbolo, resultado = operacoes[sub_opcao]
                    print(f"Resultado: ({primeiro} {simbolo} {segundo}) mod {modulo} = {resultado}")
                elif sub_opcao == "4":
                    base = int(input("Digite a base: "))
                    expoente = int(input("Digite o expoente: "))
                    resultado = CryptoMath.exp_mod(base, expoente, modulo)
                    print(f"Resultado: ({base}^{expoente}) mod {modulo} = {resultado}")
                elif sub_opcao == "5":
                    numero = int(input("Digite o numero: "))
                    resultado = CryptoMath.inverso_multi(numero, modulo)
                    print(f"Resultado: o inverso de {numero} mod {modulo} e {resultado}")
                else:
                    print("Opcao invalida. Escolha uma operacao do menu.")
            elif opcao == "4":
                restos = list(map(int, input("Digite os restos (separados por espaco): ").split()))
                modulos = list(map(int, input("Digite os modulos (separados por espaco): ").split()))
                resultado = CryptoMath.chines_resto(restos, modulos)
                modulo_total = 1
                for modulo in modulos:
                    modulo_total *= modulo
                print(f"Resultado: x = {resultado} (mod {modulo_total})")
            elif opcao == "5":
                numero = int(input("Digite o número: "))
                resultado = "é primo" if CryptoMath.ehPrimo(numero) else "não é primo"
                print(f"Resultado: {numero} {resultado}.")
            elif opcao == "6":
                numero = int(input("Digite n: "))
                print(f"Resultado: φ({numero}) = {CryptoMath.euler_totiente(numero)}")
            elif opcao == "7":
                primeiro = int(input("Digite o primeiro número: "))
                segundo = int(input("Digite o segundo número: "))
                print(f"Resultado: MMC({primeiro}, {segundo}) = "
                      f"{CryptoMath.mmc(primeiro, segundo)}")
            elif opcao == "0":
                print("Até mais!")
                break
            else:
                print("Opção inválida. Escolha um número do menu.")
        except ValueError as erro:
            print(f"Valor inválido: {erro}")


if __name__ == "__main__":
    executar_menu_interativo()
