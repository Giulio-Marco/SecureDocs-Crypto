# Como usar — Cifras Clássicas (Missão 2)

## Importação

```python
from cifras_classicas import CifrasClassicas as C
```

> O arquivo `cifras_classicas.py` precisa estar na mesma pasta que `crypto_lib.py`.

Todas as cifras seguem o mesmo padrão:

```python
cifrado   = C.<cifra>_cifrar(texto, chave)
decifrado = C.<cifra>_decifrar(cifrado, chave)
```

O texto é convertido automaticamente para **maiúsculas sem acento** (`"Ação"` → `"ACAO"`).

---

## 1. César

Desloca cada letra `k` posições no alfabeto.
**Chave:** um inteiro `k`.

```python
c = C.cesar_cifrar("ATAQUE AO AMANHECER", 3)
# 'DWDTXH DR DPDQKHFHU'

C.cesar_decifrar(c, 3)
# 'ATAQUE AO AMANHECER'
```

---

## 2. Substituição

Troca cada letra do alfabeto por outra, conforme uma tabela.
**Chave:** string com as 26 letras embaralhadas (cada letra aparece uma vez).

```
Alfabeto: ABCDEFGHIJKLMNOPQRSTUVWXYZ
Chave:    QWERTYUIOPASDFGHJKLZXCVBNM   →  A vira Q, B vira W, ...
```

```python
chave = "QWERTYUIOPASDFGHJKLZXCVBNM"

c = C.substituicao_cifrar("ATAQUE AO AMANHECER", chave)
# 'QZQJXT QG QDQFITETK'

C.substituicao_decifrar(c, chave)
# 'ATAQUE AO AMANHECER'
```

---

## 3. Afim

Fórmula: `C = (a·P + b) mod 26`.
**Chave:** dois inteiros `a` e `b`.

⚠️ `a` precisa ser coprimo com 26. Valores válidos: **1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25**.

```python
c = C.afim_cifrar("ATAQUE AO AMANHECER", 5, 8)
# 'IZIKEC IA IQIVRCSCP'

C.afim_decifrar(c, 5, 8)
# 'ATAQUE AO AMANHECER'

C.afim_cifrar("ATAQUE", 2, 1)
# ValueError: 'a' = 2 não é coprimo com 26; cifra não inversível.
```

---

## 4. Vigenère

César com um deslocamento diferente por letra, dado por uma palavra-chave que se repete.
**Chave:** uma palavra (ex.: `"CHAVE"`).

```python
c = C.vigenere_cifrar("ATAQUE AO AMANHECER", "CHAVE")
# 'CAALYG HO VQCUHZGGY'

C.vigenere_decifrar(c, "CHAVE")
# 'ATAQUE AO AMANHECER'
```

---

## 5. Hill

Divide o texto em blocos de `n` letras e multiplica cada bloco por uma matriz `n×n`.
**Chave:** matriz quadrada (lista de listas).

⚠️ O determinante da matriz precisa ser coprimo com 26.
⚠️ Espaços e pontuação são removidos. Se faltar letra no último bloco, completa com `X`.

```python
chave = [[3, 3],
         [2, 5]]

c = C.hill_cifrar("ATAQUE AO AMANHECER", chave)
# 'FRWCUIQSKINNHISYQT'

C.hill_decifrar(c, chave)
# 'ATAQUEAOAMANHECERX'

C.hill_cifrar("ATAQUE", [[2, 4], [1, 2]])
# ValueError: det(K) = 0 não é coprimo com 26; matriz não inversível.
```

---

## 6. Transposição colunar

Não troca as letras, só **muda a posição** delas. O texto é escrito em linhas sob a palavra-chave, e as colunas são lidas em ordem alfabética da chave.
**Chave:** uma palavra (ex.: `"ZEBRA"`).

```
Z E B R A        ordem de leitura: A(5) B(3) E(2) R(4) Z(1)
---------
A T A Q U
E   A O
A M A N H
E C E R X   ← completado com X
```

```python
c = C.transposicao_cifrar("ATAQUE AO AMANHECER", "ZEBRA")
# 'U HXAAAET MCQONRAEAE'

C.transposicao_decifrar(c, "ZEBRA")
# 'ATAQUE AO AMANHECERX'
```

---

## 7. Cifra de fluxo

Gera uma sequência pseudoaleatória de bytes (keystream) a partir de uma semente e faz `XOR` com o texto.
**Chave:** um inteiro (semente).
**Saída:** texto em hexadecimal.

```python
c = C.fluxo_cifrar("ATAQUE", 42)
# 'C8DDE4247500'

C.fluxo_decifrar(c, 42)
# 'ATAQUE'
```

Para ver a keystream gerada:

```python
C.gerar_keystream(42, 6).hex()
```

> Esta cifra **preserva acentos e minúsculas**, porque trabalha em bytes, não no alfabeto A-Z.

---

## Resumo rápido

| Cifra        | Chave                     | Restrição                  | Mantém espaços? |
|--------------|---------------------------|----------------------------|-----------------|
| César        | `int`                     | —                          | Sim             |
| Substituição | `str` com 26 letras       | permutação de A-Z          | Sim             |
| Afim         | `int a, int b`            | `mdc(a, 26) = 1`           | Sim             |
| Vigenère     | `str`                     | ao menos 1 letra           | Sim             |
| Hill         | matriz `n×n`              | `mdc(det, 26) = 1`         | Não (+ `X`)     |
| Transposição | `str`                     | —                          | Sim (+ `X`)     |
| Fluxo        | `int` (semente)           | —                          | Sim (hex)       |

## Rodar a demonstração

```bash
python cifras_classicas.py
```
