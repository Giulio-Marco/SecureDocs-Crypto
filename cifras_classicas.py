"""
Biblioteca de Cifras Clássicas - SecureDocs Missão 2

Cifras implementadas:
- César
- Substituição monoalfabética
- Afim
- Vigenère
- Hill
- Transposição colunar
- Cifra de fluxo (keystream via LCG + XOR)

Usa CryptoMath (Missão 1) para inverso modular, MDC e coprimalidade.
Alfabeto: A-Z (m = 26). Texto é convertido para maiúsculas e sem acentos.
"""

import unicodedata
from typing import List
from crypto_lib import CryptoMath

ALFABETO = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
M = len(ALFABETO)  # 26


# ---------------------------------------------------------------- utilitários
def normalizar(texto: str) -> str:
    """Remove acentos e converte para maiúsculas (mantém espaços/pontuação)."""
    sem_acento = unicodedata.normalize("NFD", texto)
    sem_acento = "".join(c for c in sem_acento if unicodedata.category(c) != "Mn")
    return sem_acento.upper()


def somente_letras(texto: str) -> str:
    """Normaliza e remove tudo que não é A-Z."""
    return "".join(c for c in normalizar(texto) if c in ALFABETO)


def _idx(c: str) -> int:
    return ord(c) - ord("A")


def _chr(i: int) -> str:
    return chr(i % M + ord("A"))


class CifrasClassicas:

    # ------------------------------------------------------------- César
    @staticmethod
    def cesar_cifrar(texto: str, k: int) -> str:
        """C = (P + k) mod 26"""
        return "".join(_chr(_idx(c) + k) if c in ALFABETO else c
                       for c in normalizar(texto))

    @staticmethod
    def cesar_decifrar(texto: str, k: int) -> str:
        """P = (C - k) mod 26"""
        return CifrasClassicas.cesar_cifrar(texto, -k)

    # ------------------------------------------------------- Substituição
    @staticmethod
    def _validar_chave_substituicao(chave: str) -> str:
        chave = normalizar(chave)
        if len(chave) != M or set(chave) != set(ALFABETO):
            raise ValueError("Chave deve ser uma permutação das 26 letras.")
        return chave

    @staticmethod
    def substituicao_cifrar(texto: str, chave: str) -> str:
        """Cada letra i do alfabeto é trocada por chave[i]."""
        chave = CifrasClassicas._validar_chave_substituicao(chave)
        tabela = str.maketrans(ALFABETO, chave)
        return normalizar(texto).translate(tabela)

    @staticmethod
    def substituicao_decifrar(texto: str, chave: str) -> str:
        """Aplica a permutação inversa."""
        chave = CifrasClassicas._validar_chave_substituicao(chave)
        tabela = str.maketrans(chave, ALFABETO)
        return normalizar(texto).translate(tabela)

    # -------------------------------------------------------------- Afim
    @staticmethod
    def _validar_a(a: int) -> None:
        if not CryptoMath.saoCoprimo(a, M):
            raise ValueError(f"'a' = {a} não é coprimo com {M}; cifra não inversível.")

    @staticmethod
    def afim_cifrar(texto: str, a: int, b: int) -> str:
        """C = (a·P + b) mod 26, com mdc(a, 26) = 1"""
        CifrasClassicas._validar_a(a)
        return "".join(_chr(a * _idx(c) + b) if c in ALFABETO else c
                       for c in normalizar(texto))

    @staticmethod
    def afim_decifrar(texto: str, a: int, b: int) -> str:
        """P = a⁻¹·(C - b) mod 26"""
        CifrasClassicas._validar_a(a)
        a_inv = CryptoMath.inverso_multi(a, M)
        return "".join(_chr(a_inv * (_idx(c) - b)) if c in ALFABETO else c
                       for c in normalizar(texto))

    # ---------------------------------------------------------- Vigenère
    @staticmethod
    def _vigenere(texto: str, chave: str, sinal: int) -> str:
        chave = somente_letras(chave)
        if not chave:
            raise ValueError("Chave deve conter ao menos uma letra.")
        saida, j = [], 0
        for c in normalizar(texto):
            if c in ALFABETO:
                k = _idx(chave[j % len(chave)])
                saida.append(_chr(_idx(c) + sinal * k))
                j += 1  # só avança a chave em letras
            else:
                saida.append(c)
        return "".join(saida)

    @staticmethod
    def vigenere_cifrar(texto: str, chave: str) -> str:
        """C_i = (P_i + K_(i mod |K|)) mod 26"""
        return CifrasClassicas._vigenere(texto, chave, +1)

    @staticmethod
    def vigenere_decifrar(texto: str, chave: str) -> str:
        """P_i = (C_i - K_(i mod |K|)) mod 26"""
        return CifrasClassicas._vigenere(texto, chave, -1)

    # -------------------------------------------------------------- Hill
    @staticmethod
    def _det(mat: List[List[int]]) -> int:
        """Determinante por expansão de cofatores (matrizes pequenas)."""
        n = len(mat)
        if n == 1:
            return mat[0][0]
        if n == 2:
            return mat[0][0] * mat[1][1] - mat[0][1] * mat[1][0]
        return sum((-1) ** j * mat[0][j] * CifrasClassicas._det(
            [linha[:j] + linha[j + 1:] for linha in mat[1:]]) for j in range(n))

    @staticmethod
    def _matriz_inversa_mod(mat: List[List[int]], m: int = M) -> List[List[int]]:
        """K⁻¹ = det(K)⁻¹ · adj(K) mod m"""
        n = len(mat)
        det = CifrasClassicas._det(mat) % m
        if not CryptoMath.saoCoprimo(det, m):
            raise ValueError(f"det(K) = {det} não é coprimo com {m}; matriz não inversível.")
        det_inv = CryptoMath.inverso_multi(det, m)
        if n == 1:
            return [[det_inv]]
        # adj(K)[i][j] = cofator(j, i)
        adj = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                menor = [linha[:j] + linha[j + 1:] for k, linha in enumerate(mat) if k != i]
                adj[j][i] = (-1) ** (i + j) * CifrasClassicas._det(menor)
        return [[(det_inv * adj[i][j]) % m for j in range(n)] for i in range(n)]

    @staticmethod
    def _hill_aplicar(texto: str, mat: List[List[int]]) -> str:
        n = len(mat)
        saida = []
        for b in range(0, len(texto), n):
            bloco = [_idx(c) for c in texto[b:b + n]]
            for i in range(n):
                saida.append(_chr(sum(mat[i][j] * bloco[j] for j in range(n))))
        return "".join(saida)

    @staticmethod
    def hill_cifrar(texto: str, chave: List[List[int]], preenchimento: str = "X") -> str:
        """C = K·P mod 26 (blocos de n letras). Remove não-letras e completa com 'X'."""
        CifrasClassicas._matriz_inversa_mod(chave)  # valida a chave
        n = len(chave)
        texto = somente_letras(texto)
        if len(texto) % n:
            texto += preenchimento * (n - len(texto) % n)
        return CifrasClassicas._hill_aplicar(texto, chave)

    @staticmethod
    def hill_decifrar(texto: str, chave: List[List[int]]) -> str:
        """P = K⁻¹·C mod 26"""
        inv = CifrasClassicas._matriz_inversa_mod(chave)
        return CifrasClassicas._hill_aplicar(somente_letras(texto), inv)

    # ------------------------------------------------ Transposição colunar
    @staticmethod
    def _ordem_colunas(chave: str) -> List[int]:
        """Índices das colunas na ordem alfabética da chave (estável p/ repetidas)."""
        chave = normalizar(chave)
        return sorted(range(len(chave)), key=lambda i: (chave[i], i))

    @staticmethod
    def transposicao_cifrar(texto: str, chave: str, preenchimento: str = "X") -> str:
        """Escreve em linhas de |chave| colunas, lê colunas na ordem alfabética da chave."""
        n = len(chave)
        texto = normalizar(texto)
        if len(texto) % n:
            texto += preenchimento * (n - len(texto) % n)
        linhas = [texto[i:i + n] for i in range(0, len(texto), n)]
        return "".join("".join(l[c] for l in linhas)
                       for c in CifrasClassicas._ordem_colunas(chave))

    @staticmethod
    def transposicao_decifrar(texto: str, chave: str) -> str:
        """Reconstrói as colunas na ordem da chave e lê por linhas."""
        n = len(chave)
        n_linhas = len(texto) // n
        colunas = [""] * n
        for pos, c in enumerate(CifrasClassicas._ordem_colunas(chave)):
            colunas[c] = texto[pos * n_linhas:(pos + 1) * n_linhas]
        return "".join(colunas[c][r] for r in range(n_linhas) for c in range(n))

    # -------------------------------------------------- Cifra de fluxo
    @staticmethod
    def gerar_keystream(semente: int, tamanho: int,
                        a: int = 1103515245, c: int = 12345, m: int = 2 ** 31) -> bytes:
        """
        Gerador congruencial linear: X_(n+1) = (a·X_n + c) mod m.
        Retorna 'tamanho' bytes (byte = bits 16..23 de X_n).
        Obs.: LCG é previsível — uso apenas educacional.
        """
        x = semente % m
        saida = bytearray()
        for _ in range(tamanho):
            x = (a * x + c) % m
            saida.append((x >> 16) & 0xFF)
        return bytes(saida)

    @staticmethod
    def fluxo_cifrar(texto: str, semente: int) -> str:
        """C_i = P_i XOR K_i. Retorna hexadecimal."""
        dados = texto.encode("utf-8")
        ks = CifrasClassicas.gerar_keystream(semente, len(dados))
        return bytes(p ^ k for p, k in zip(dados, ks)).hex().upper()

    @staticmethod
    def fluxo_decifrar(cifrado_hex: str, semente: int) -> str:
        """P_i = C_i XOR K_i (XOR é sua própria inversa)."""
        dados = bytes.fromhex(cifrado_hex)
        ks = CifrasClassicas.gerar_keystream(semente, len(dados))
        return bytes(c ^ k for c, k in zip(dados, ks)).decode("utf-8")


# ------------------------------------------------------------------- demo
if __name__ == "__main__":
    msg = "TRANSFERIR DOCUMENTO PARA SERVIDOR CENTRAL"
    C = CifrasClassicas
    sub_key = "QWERTYUIOPASDFGHJKLZXCVBNM"
    hill_key = [[3, 3], [2, 5]]

    casos = [
        ("César (k=3)", C.cesar_cifrar(msg, 3), lambda x: C.cesar_decifrar(x, 3)),
        ("Substituição", C.substituicao_cifrar(msg, sub_key),
         lambda x: C.substituicao_decifrar(x, sub_key)),
        ("Afim (a=5,b=8)", C.afim_cifrar(msg, 5, 8), lambda x: C.afim_decifrar(x, 5, 8)),
        ("Vigenère (CHAVE)", C.vigenere_cifrar(msg, "CHAVE"),
         lambda x: C.vigenere_decifrar(x, "CHAVE")),
        ("Hill [[3,3],[2,5]]", C.hill_cifrar(msg, hill_key),
         lambda x: C.hill_decifrar(x, hill_key)),
        ("Transposição (ZEBRA)", C.transposicao_cifrar(msg, "ZEBRA"),
         lambda x: C.transposicao_decifrar(x, "ZEBRA")),
        ("Fluxo (semente=42)", C.fluxo_cifrar(msg, 42), lambda x: C.fluxo_decifrar(x, 42)),
    ]

    print(f"Texto claro: {msg}\n")
    for nome, cifrado, decifra in casos:
        print(f"{nome}\n  Cifrado:  {cifrado}\n  Decifrado: {decifra(cifrado)}\n")
