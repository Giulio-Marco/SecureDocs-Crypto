# SecureDocs - Missão 1: Precisamos de Matemática

## 📋 Descrição

Esta é uma biblioteca Python que implementa os algoritmos matemáticos fundamentais necessários para sistemas de criptografia. O projeto foi desenvolvido como resposta à **Missão 1** do desafio SecureDocs.

## 📚 Algoritmos Implementados

### 1. **Aritmética Modular**
- **Inverso Multiplicativo**: Calcula o inverso multiplicativo de um número em módulo
- **Exponenciação Modular**: Realiza exponenciação eficiente em módulo (usa algoritmo de exponenciação rápida)

### 2. **MDC e Algoritmo de Euclides**
- **Máximo Divisor Comum (GCD)**: Implementação do algoritmo de Euclides
- **Algoritmo Estendido de Euclides**: Encontra x, y tal que a*x + b*y = gcd(a,b)

### 3. **Números Primos**
- **Teste de Primalidade**: Implementação do Teste de Miller-Rabin (probabilístico)
- **Geração de Primos**: Encontra números primos aleatórios com n bits

### 4. **Função φ de Euler (Totient)**
- **Totient Genérico**: Calcula φ(n) para qualquer número
- **Totient para p*q**: Otimizado para quando n é produto de dois primos

### 5. **Teorema Chinês do Resto**
- Resolve sistemas de congruências módulo coprimos
- Essencial para muitos algoritmos criptográficos

### 6. **Utilitários**
- Verificação de coprimalidade
- Cálculo de Mínimo Múltiplo Comum (MMC)

## 🚀 Instalação e Uso

### Executar a biblioteca com exemplos

```bash
python crypto_lib.py
```

Isto executará uma demonstração com exemplos de cada algoritmo.

### Executar os testes

```bash
python test_crypto_lib.py
```

Isto executará a suite completa de testes unitários validando toda a implementação.

## 📖 Exemplos de Uso

```python
from crypto_lib import CryptoMath

# MDC
mdc = CryptoMath.gcd(48, 18)  # Resultado: 6

# Algoritmo Estendido de Euclides
gcd, x, y = CryptoMath.extended_gcd(10, 6)
# Resultado: gcd=2, x=2, y=-3
# Verificação: 10*2 + 6*(-3) = 2

# Inverso Multiplicativo
inv = CryptoMath.mod_inverse(3, 11)  # Resultado: 4
# Verificação: (3 * 4) % 11 = 1

# Exponenciação Modular
result = CryptoMath.mod_exp(2, 10, 1000)  # Resultado: 24

# Teste de Primalidade
is_prime = CryptoMath.is_prime(17)  # Resultado: True

# Função φ de Euler
phi = CryptoMath.euler_totient(12)  # Resultado: 4
phi_pq = CryptoMath.euler_totient_pq(5, 7)  # Resultado: 24

# Teorema Chinês do Resto
x = CryptoMath.chinese_remainder_theorem([2, 3, 2], [3, 5, 7])
# Encontra x tal que: x≡2(mod 3), x≡3(mod 5), x≡2(mod 7)

# Verificar coprimalidade
coprime = CryptoMath.are_coprime(15, 28)  # Resultado: True

# MMC
lcm = CryptoMath.lcm(12, 18)  # Resultado: 36
```

## 🏗️ Estrutura do Projeto

```
Trabalho-Criptografia/
├── crypto_lib.py           # Biblioteca principal com todos os algoritmos
├── test_crypto_lib.py      # Suite de testes unitários
├── README.md               # Este arquivo
└── DOCUMENTACAO.md         # Documentação técnica detalhada
```

## 📊 Detalhes Técnicos

### Exponenciação Modular
Implementa o algoritmo de "Binary Exponentiation" para calcular (base^exp) % mod de forma eficiente:
- Complexidade: O(log exp)
- Essencial para criptografia RSA

### Teste de Primalidade Miller-Rabin
Teste probabilístico que:
- Tem probabilidade de erro < 4^(-k) onde k é o número de rodadas
- Usa 40 rodadas por padrão (confiabilidade muito alta)
- Muito mais eficiente que testes determinísticos para números grandes

### Teorema Chinês do Resto
Resolve sistemas de congruências lineares:
- Requer que os módulos sejam coprimos entre si
- Tempo: O(n³) onde n é número de congruências
- Fundamental em RSA e protocolo Shamir

## ✅ Testes

A suite de testes cobre:
- 50+ casos de teste
- Todos os algoritmos implementados
- Casos extremos e valores conhecidos
- Validação de congruências

Para ver o resultado dos testes:
```bash
python -m unittest test_crypto_lib -v
```

## 🎯 Próximas Missões

Este projeto é a base para as próximas missões do SecureDocs:
- Missão 2: Criptografia Simétrica
- Missão 3: Criptografia Assimétrica (RSA)
- Missão 4: Funções Hash e Assinatura Digital
- E muito mais...

## 📝 Notas Importantes

1. **Miller-Rabin é probabilístico**: Para números críticos, execute múltiplas vezes
2. **Módulos devem ser coprimos**: No Teorema Chinês do Resto, verifique gcd
3. **Overflow não é problema**: Python suporta inteiros arbitrários
4. **Segurança**: Esta é uma implementação educacional, não use em produção

## 👥 Autores

Desenvolvido como projeto acadêmico para a disciplina de Criptografia.

## 📄 Licença

Projeto acadêmico.
