"""
Desafios praticos com a crypto_lib.

COMO USAR:
  1. Resolva cada desafio escrevendo o codigo no lugar indicado.
  2. Guarde o resultado na variavel R1, R2, ... conforme pedido.
  3. Rode:  python desafios.py
     Ele diz quais voce acertou.

Deixe como None os que ainda nao resolveu.
"""

from crypto_lib import CryptoMath

# ---------------------------------------------------------------
# 1) AQUECIMENTO - MDC e MMC
#    Calcule o MDC e o MMC de 1071 e 462.
#    R1 = (mdc, mmc)   <- uma tupla com os dois
# ---------------------------------------------------------------
R1 = None


# ---------------------------------------------------------------
# 2) EUCLIDES ESTENDIDO
#    Ache inteiros x e y que satisfacam:  240*x + 46*y = mdc(240, 46)
#    R2 = (mdc, x, y)
# ---------------------------------------------------------------
R2 = None


# ---------------------------------------------------------------
# 3) INVERSO MULTIPLICATIVO
#    Ache o inverso de 17 modulo 43.
#    (deve valer: 17 * R3 % 43 == 1)
#    R3 = numero
# ---------------------------------------------------------------
R3 = None


# ---------------------------------------------------------------
# 4) EXPONENCIACAO MODULAR
#    Calcule 7^222 mod 11.
#    Dica: NAO faca 7**222 % 11 na mao - use exponenciacao_modular.
#    R4 = numero
# ---------------------------------------------------------------
R4 = None


# ---------------------------------------------------------------
# 5) PRIMALIDADE (pegadinha)
#    561 e um numero de Carmichael: ele ENGANA o teste de Fermat,
#    fingindo ser primo. O Miller-Rabin da lib cai nessa?
#    R5 = CryptoMath.eh_primo(561)      <- True ou False
#    Depois descubra os 3 fatores primos de 561 (todos < 20).
#    R5_fatores = (a, b, c) em ordem crescente
# ---------------------------------------------------------------
R5 = None
R5_fatores = None


# ---------------------------------------------------------------
# 6) TEOREMA DE EULER
#    Calcule phi(36). Depois verifique o Teorema de Euler:
#    para 'a' coprimo com n, vale  a^phi(n) mod n == 1.
#    Teste com a = 5, n = 36.
#    R6 = (phi_de_36, resultado_de_5^phi mod 36)
# ---------------------------------------------------------------
R6 = None


# ---------------------------------------------------------------
# 7) TEOREMA CHINES DO RESTO  (problema de Sun Tzu, seculo III)
#    "Um exercito tem menos de 105 soldados. Em filas de 3 sobram 2,
#     em filas de 5 sobram 3, em filas de 7 sobram 2. Quantos sao?"
#    R7 = numero de soldados
# ---------------------------------------------------------------
R7 = None


# ---------------------------------------------------------------
# 8) DESAFIO FINAL - quebrar um RSA fraco
#    Voce interceptou esta mensagem cifrada:
#        chave publica: n = 11413, e = 3
#        texto cifrado: c = 10345
#    O n e pequeno demais: da pra fatorar. Passos:
#      a) ache p e q tais que p*q = 11413 (teste divisores e use eh_primo)
#      b) phi = (p-1)*(q-1)
#      c) d = inverso de e modulo phi
#      d) mensagem = c^d mod n
#    R8 = mensagem original (um numero)
# ---------------------------------------------------------------
R8 = None


# ===============================================================
#  DAQUI PRA BAIXO E O CORRETOR - nao precisa mexer
# ===============================================================
def _corrigir():
    gabarito = [
        ("1  MDC e MMC",            R1,          (21, 23562)),
        ("2  Euclides estendido",   R2,          (2, -9, 47)),
        ("3  Inverso multiplicativo", R3,        38),
        ("4  Exponenciacao modular", R4,         5),
        ("5  eh_primo(561)",        R5,          False),
        ("5b fatores de 561",       R5_fatores,  (3, 11, 17)),
        ("6  Teorema de Euler",     R6,          (12, 1)),
        ("7  Teorema Chines",       R7,          23),
        ("8  RSA quebrado",         R8,          1234),
    ]
    acertos = pendentes = 0
    print("=" * 46)
    for nome, resposta, esperado in gabarito:
        if resposta is None:
            print(f"  -  {nome:<26} (nao resolvido)")
            pendentes += 1
        elif resposta == esperado:
            print(f"  OK {nome:<26} {resposta}")
            acertos += 1
        else:
            print(f"  X  {nome:<26} seu: {resposta}")
    total = len(gabarito)
    print("=" * 46)
    print(f"  {acertos}/{total} corretos, {pendentes} nao resolvidos")


if __name__ == "__main__":
    _corrigir()
