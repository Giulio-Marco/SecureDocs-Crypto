# Documentação Técnica - Algoritmos Criptográficos

## 📌 Índice

1. [Aritmética Modular](#aritmética-modular)
2. [MDC e Algoritmo de Euclides](#mdc-e-algoritmo-de-euclides)
3. [Números Primos](#números-primos)
4. [Função φ de Euler](#função-φ-de-euler-totient)
5. [Teorema Chinês do Resto](#teorema-chinês-do-resto)
6. [Análise de Complexidade](#análise-de-complexidade)

---

## Aritmética Modular

### Conceito
A aritmética modular trabalha com restos de divisão. Se a ≡ b (mod m), significa que m divide (a - b).

### Inverso Multiplicativo

**Definição**: O inverso multiplicativo de `a` módulo `m` é um número `x` tal que:
```
(a * x) ≡ 1 (mod m)
```

**Quando existe**:
- Existe se e somente se gcd(a, m) = 1 (a e m são coprimos)
- Se gcd(a, m) ≠ 1, não existe inverso

**Algoritmo**:
Usa o Algoritmo Estendido de Euclides para encontrar x, y tal que:
```
a*x + m*y = gcd(a, m)
```
Se gcd(a, m) = 1, então `x` é o inverso de `a` mod `m`.

**Exemplo**:
```
Inverso de 3 módulo 11:
3 * 4 ≡ 12 ≡ 1 (mod 11)
Portanto, inv = 4
```

**Aplicações em Criptografia**:
- Algoritmo RSA (decodificação)
- Cifra Affine
- Cálculos em corpos finitos

---

### Exponenciação Modular

**Definição**: Calcular (base^exp) mod m de forma eficiente.

**Problema**: Calcular 2^1000000 mod 1000000007 é inviável diretamente.

**Solução**: Algoritmo de Binary Exponentiation
```
1. Converter exp para binário
2. Usar a propriedade: (a*b) mod m = ((a mod m) * (b mod m)) mod m
3. Processar bits do expoente da direita para esquerda
```

**Pseudocódigo**:
```
mod_exp(base, exp, mod):
    result = 1
    base = base % mod
    while exp > 0:
        if exp é ímpar:
            result = (result * base) % mod
        exp = exp >> 1  (divide por 2)
        base = (base * base) % mod
    return result
```

**Complexidade**: O(log exp)

**Exemplo**:
```
(2^10) % 1000:
- 10 em binário: 1010
- Processa cada bit: resultado = 24
```

**Aplicações em Criptografia**:
- RSA: (mensagem^chave) mod n
- Diffie-Hellman
- Qualquer sistema que use exponenciação

---

## MDC e Algoritmo de Euclides

### Máximo Divisor Comum (MDC/GCD)

**Definição**: O maior número que divide ambos a e b.

**Algoritmo de Euclides**:
```
gcd(a, b):
    while b ≠ 0:
        temp = b
        b = a mod b
        a = temp
    return a
```

**Propriedade Principal**:
```
gcd(a, b) = gcd(b, a mod b)
```

**Exemplo**:
```
gcd(48, 18):
48 = 18 * 2 + 12
18 = 12 * 1 + 6
12 = 6 * 2 + 0
Portanto, gcd = 6
```

**Complexidade**: O(log(min(a, b)))

---

### Algoritmo Estendido de Euclides

**Objetivo**: Encontrar x, y inteiros tal que:
```
a*x + b*y = gcd(a, b)
```

**Pseudocódigo Recursivo**:
```
extended_gcd(a, b):
    if b = 0:
        return (a, 1, 0)
    else:
        (gcd, x1, y1) = extended_gcd(b, a mod b)
        x = y1
        y = x1 - (a // b) * y1
        return (gcd, x, y)
```

**Exemplo**:
```
extended_gcd(10, 6):
Retorna: gcd=2, x=2, y=-3
Verificação: 10*2 + 6*(-3) = 20 - 18 = 2 ✓
```

**Aplicações em Criptografia**:
- Calcular inversos multiplicativos
- Algoritmo de Euclides estendido para corpos finitos

---

## Números Primos

### Conceito
Um número primo p é aquele divisível apenas por 1 e por ele mesmo.
- Primos pequenos: 2, 3, 5, 7, 11, 13, 17, 19, 23, 29...
- Fundamentais em criptografia (RSA usa primos grandes)

### Teste de Primalidade Miller-Rabin

**Tipo**: Teste probabilístico (não determinístico)

**Complexidade**: O(k log³ n) onde k é número de rodadas

**Algoritmo**:
```
1. Escrever n-1 = 2^r * d (onde d é ímpar)
2. Repetir k vezes:
   a. Escolher a aleatório em [2, n-2]
   b. Calcular x = a^d mod n
   c. Se x = 1 ou x = n-1, continuar para próxima rodada
   d. Para cada i de 1 a r-1:
      - x = x^2 mod n
      - Se x = n-1, sair e continuar próxima rodada
   e. Se não encontrou n-1, n é composto, retorna False
3. Se passou em todas as k rodadas, provavelmente primo
```

**Probabilidade de Erro**:
- Probabilidade de falso positivo: ≤ 4^(-k)
- Com k=40 (padrão): erro ≤ 2^(-80) (negligenciável)

**Vantagem sobre testes determinísticos**:
- Muito mais rápido para números muito grandes
- Confiável na prática

---

### Geração de Números Primos

**Algoritmo**:
```
1. Gerar número aleatório com n bits
2. Garantir que é ímpar (bit menos significativo = 1)
3. Testar com Miller-Rabin
4. Se não for primo, tentar próximo número ímpar
5. Repetir até encontrar primo
```

**Aplicações**:
- RSA: precisa de dois primos grandes (2048+ bits)
- Diffie-Hellman: escolher primo grande
- Criptografia baseada em curvas elípticas

---

## Função φ de Euler (Totient)

### Definição
φ(n) = número de inteiros positivos ≤ n que são coprimos com n.

**Exemplos**:
```
φ(1) = 1         (apenas 1)
φ(6) = 2         (1, 5 são coprimos com 6)
φ(7) = 6         (1,2,3,4,5,6 são coprimos com 7)
φ(12) = 4        (1,5,7,11 são coprimos com 12)
```

### Propriedades Importantes

**Para número primo p**:
```
φ(p) = p - 1
```

**Para potência de primo p^k**:
```
φ(p^k) = p^k - p^(k-1) = p^(k-1) * (p - 1)
```

**Para produtos de coprimos**:
```
Se gcd(m, n) = 1, então φ(m*n) = φ(m) * φ(n)
```

**Para n = p * q (p, q primos distintos)**:
```
φ(p*q) = (p-1) * (q-1)
```

### Cálculo Geral

**Algoritmo**:
```
1. Fatorizar n = p1^k1 * p2^k2 * ... * pr^kr
2. φ(n) = n * (1 - 1/p1) * (1 - 1/p2) * ... * (1 - 1/pr)
```

**Exemplo**:
```
φ(12) = φ(2² * 3) = 12 * (1 - 1/2) * (1 - 1/3) 
      = 12 * 1/2 * 2/3 = 4 ✓
```

### Aplicações em Criptografia

- **RSA**: φ(n) = (p-1)*(q-1) é usado para calcular chave privada
- **Teorema de Euler**: a^φ(n) ≡ 1 (mod n) se gcd(a,n)=1
- **Pequeno Teorema de Fermat**: p^(p-1) ≡ 1 (mod p) para primo p

---

## Teorema Chinês do Resto (TCR)

### Problema
Resolver um sistema de congruências simultâneas:
```
x ≡ a₁ (mod m₁)
x ≡ a₂ (mod m₂)
...
x ≡ aₖ (mod mₖ)
```

### Condição de Existência
- Solução existe se e somente se os módulos m₁, m₂, ..., mₖ são **coprimos entre si**
- Ou seja: gcd(mᵢ, mⱼ) = 1 para todo i ≠ j

### Algoritmo (Construção)

```
1. Calcular M = m₁ * m₂ * ... * mₖ
2. Para cada i:
   a. Calcular Mᵢ = M / mᵢ
   b. Calcular yᵢ = inverso de Mᵢ módulo mᵢ
      (yᵢ tal que Mᵢ * yᵢ ≡ 1 (mod mᵢ))
3. Solução: x = Σ(aᵢ * Mᵢ * yᵢ) mod M
```

### Exemplo Completo

```
Resolver:
x ≡ 2 (mod 3)
x ≡ 3 (mod 5)
x ≡ 2 (mod 7)

M = 3 * 5 * 7 = 105

Para i=1: M₁ = 105/3 = 35, y₁ = inv(35, 3) = inv(2, 3) = 2
Para i=2: M₂ = 105/5 = 21, y₂ = inv(21, 5) = inv(1, 5) = 1
Para i=3: M₃ = 105/7 = 15, y₃ = inv(15, 7) = inv(1, 7) = 1

x = (2*35*2 + 3*21*1 + 2*15*1) mod 105
  = (140 + 63 + 30) mod 105
  = 233 mod 105
  = 23

Verificação:
23 % 3 = 2 ✓
23 % 5 = 3 ✓
23 % 7 = 2 ✓
```

### Aplicações em Criptografia

- **RSA com TCR**: Acelera decodificação usando TCR para cálculos mod p e mod q
- **Shamir Secret Sharing**: Reconstruir segredo de compartilhamentos
- **Protocolo de Distribuição de Chaves**
- **Corpos Finitos**: Operações em GF(p^n)

---

## Análise de Complexidade

| Algoritmo | Complexidade | Observações |
|-----------|--------------|------------|
| GCD | O(log min(a,b)) | Muito eficiente |
| Extended GCD | O(log min(a,b)) | Mesmo que GCD |
| Inverso Modular | O(log m) | Usa Extended GCD |
| Mod Exponentiation | O(log exp * log² mod) | Essencial para criptografia |
| Miller-Rabin (k rodadas) | O(k log³ n) | Probabilístico, rápido |
| Euler Totient | O(√n) | Fatorização é cara |
| TCR (k congruências) | O(k³) | Dominado por inversas |

---

## Considerações de Segurança

### ✅ O que fazer:

1. **Use números primos grandes** (2048+ bits para RSA)
2. **Verifique coprimalidade** antes de usar TCR
3. **Use Miller-Rabin com k≥40** para testes de primalidade
4. **Gere aleatoriamente** números primos (não reutilize)
5. **Valide entradas** (verifique divisões por zero, módulos válidos)

### ⚠️ Riscos:

1. **Números primos fracos**: Devem ser grandes e aleatórios
2. **Reutilização de chaves**: Cada sessão deve usar novos primos
3. **Side-channel attacks**: Tempo de execução pode vazar informações
4. **Implementação**: Esta é educacional, não use em produção

---

## Referências Bibliográficas

1. **"Introduction to Cryptography with Coding Theory"** - Trappe & Washington
2. **"Handbook of Applied Cryptography"** - Menezes, Oorschot, Vanstone
3. **"Elementary Number Theory"** - Rosen
4. **"Cryptography and Network Security"** - Stallings

---

**Última atualização**: Setembro 2026
**Versão**: 1.0
