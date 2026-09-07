"""
Exemplo prático de uso da crypto_lib.

Este arquivo está NA MESMA PASTA que crypto_lib.py.
Basta rodar:  python exemplo_uso.py
"""

# ---------------------------------------------------------------
# 3 formas de importar (escolha UMA — aqui uso a forma 1)
# ---------------------------------------------------------------
# 1) importa a classe direto  -> CryptoMath.mdc(48, 18)
from crypto_lib import CryptoMath

# 2) importa o módulo inteiro -> crypto_lib.CryptoMath.mdc(48, 18)
# import crypto_lib

# 3) importa com apelido      -> cm.CryptoMath.mdc(48, 18)
# import crypto_lib as cm


print("=== 1. Chamando as funções direto na classe ===")
# Todos os métodos são @staticmethod: NÃO precisa criar objeto.
# Errado:  m = CryptoMath(); m.mdc(...)   <- funciona, mas é desnecessário
# Certo:   CryptoMath.mdc(...)
print("MDC(48, 18)      =", CryptoMath.mdc(48, 18))
print("MMC(12, 18)      =", CryptoMath.mmc(12, 18))
print("15 e 28 coprimos?", CryptoMath.sao_coprimos(15, 28))


print("\n=== 2. Guardando o retorno em variáveis ===")
resultado = CryptoMath.exponenciacao_modular(2, 10, 1000)   # (2^10) % 1000
print("exponenciacao_modular(2, 10, 1000) =", resultado)

# mdc_estendido devolve uma TUPLA de 3 valores -> desempacote em 3 variáveis
mdc, x, y = CryptoMath.mdc_estendido(10, 6)
print(f"mdc_estendido(10, 6) -> mdc={mdc}, x={x}, y={y}")
print(f"confere: 10*{x} + 6*{y} = {10*x + 6*y}")


print("\n=== 3. Funções que podem dar erro (use try/except) ===")
try:
    print("inverso_modular(3, 11) =", CryptoMath.inverso_modular(3, 11))
    print("inverso_modular(4, 8)  =", CryptoMath.inverso_modular(4, 8))  # não existe
except ValueError as e:
    print("Erro capturado:", e)


print("\n=== 4. Usando as funções em um loop ===")
for n in [17, 19, 97, 100, 121]:
    print(f"  {n:>4} é primo? {CryptoMath.eh_primo(n)}")


print("\n=== 5. Juntando tudo: um RSA de brinquedo ===")
# Passo 1: dois primos
p = CryptoMath.gerar_primo(16)
q = CryptoMath.gerar_primo(16)
while p == q:
    q = CryptoMath.gerar_primo(16)
print(f"p = {p}")
print(f"q = {q}")

# Passo 2: n e phi(n)
n = p * q
phi = CryptoMath.totiente_euler_pq(p, q)      # (p-1)*(q-1)
print(f"n   = p*q  = {n}")
print(f"phi = (p-1)*(q-1) = {phi}")

# Passo 3: expoente público e — precisa ser coprimo com phi
e = 65537
while not CryptoMath.sao_coprimos(e, phi):
    e += 2
print(f"chave publica  (e, n) = ({e}, {n})")

# Passo 4: expoente privado d = inverso de e mod phi
d = CryptoMath.inverso_modular(e, phi)
print(f"chave privada  (d, n) = ({d}, {n})")

# Passo 5: cifrar e decifrar
mensagem = 42
cifrado = CryptoMath.exponenciacao_modular(mensagem, e, n)   # c = m^e mod n
decifrado = CryptoMath.exponenciacao_modular(cifrado, d, n)  # m = c^d mod n
print(f"mensagem  = {mensagem}")
print(f"cifrado   = {cifrado}")
print(f"decifrado = {decifrado}  -> {'OK' if decifrado == mensagem else 'FALHOU'}")


print("\n=== 6. Teorema Chinês do Resto (listas como parâmetro) ===")
restos  = [2, 3, 2]
modulos = [3, 5, 7]
x = CryptoMath.teorema_chines_resto(restos, modulos)
print(f"x = {x}   (x%3={x%3}, x%5={x%5}, x%7={x%7})")
