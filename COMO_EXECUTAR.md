# Como Executar a Biblioteca e Testes

## 🚀 Executar a Calculadora Interativa

Execute no PowerShell:

```powershell
cd "c:\Users\giuli\OneDrive\Documents\Trabalho-Criptografia"
python crypto_lib.py
```

O programa exibirá um menu. Digite o número da operação e, depois, os valores
solicitados. Por exemplo, para calcular o MDC de 48 e 18:

```text
Escolha uma opção: 1
Digite o primeiro número: 48
Digite o segundo número: 18
Resultado: MDC(48, 18) = 6
```

Escolha `0` para sair. As opções disponíveis são:
- `1`: Algoritmo de Euclides (classico)
- `2`: Algoritmo Estendido de Euclides
- `3`: Aritmetica modular (soma, subtracao, multiplicacao, exponenciacao e inverso)
- `4`: Teorema Chines do Resto
- `5`: Verificar se e primo
- `6`: Funcao de Euler
- `7`: MMC

Para usar a biblioteca sem o menu, importe `CryptoMath` em outro arquivo.

### Exemplos exibidos anteriormente

As operações também podem ser chamadas diretamente no código. A saída abaixo
representa o formato dos resultados:

```
============================================================
BIBLIOTECA DE CRIPTOGRAFIA - MISSÃO 1
============================================================

1. MDC e Algoritmo de Euclides
   MDC(48, 18) = 6

2. Algoritmo Estendido de Euclides
   gcd, x, y = extended_gcd(10, 6)
   Resultado: gcd=2, x=2, y=-3
   Verificação: 10*2 + 6*(-3) = 2

... (mais exemplos)
```

---

## 🧪 Executar os Testes

Execute no PowerShell:

```powershell
cd "c:\Users\giuli\OneDrive\Documents\Trabalho-Criptografia"
python -m pytest test_crypto_lib.py -v
```

Ou simplesmente:

```powershell
python test_crypto_lib.py
```

**Informações dos testes**:
- Total de testes: 50+
- Cobertura: Todos os algoritmos
- Tempo esperado: < 5 segundos

---

## 📦 Usar a Biblioteca em Outro Projeto

Se quiser usar a biblioteca em outro arquivo Python:

```python
# seu_arquivo.py
from crypto_lib import CryptoMath

# Exemplos de uso
mdc = CryptoMath.gcd(48, 18)
print(f"MDC(48, 18) = {mdc}")

# Teste de primalidade
if CryptoMath.is_prime(17):
    print("17 é primo!")

# Exponenciação modular eficiente
result = CryptoMath.mod_exp(2, 1000000, 10**9 + 7)
print(f"(2^1000000) mod 10^9+7 = {result}")
```

---

## 🔍 Verificar Instalação Python

Antes de executar, certifique-se que tem Python 3.8+:

```powershell
python --version
```

Esperado: `Python 3.8.x` ou superior

---

## ⚠️ Se Tiver Problemas

### Erro: "No module named 'crypto_lib'"
- Certifique-se de estar na pasta correta
- O arquivo `crypto_lib.py` precisa estar no mesmo diretório

### Erro: "Python não encontrado"
- Instale Python de [python.org](https://www.python.org)
- Adicione à PATH do Windows

### Testes com erro
- Execute: `python test_crypto_lib.py` (modo verbose)
- Verifique Python 3.8+

---

## 📊 Estrutura dos Testes

```
test_crypto_lib.py
├── TestMDCAndEuclides (5 testes)
├── TestModularArithmetic (6 testes)
├── TestPrimes (5 testes)
├── TestEulerTotient (5 testes)
├── TestChineseRemainderTheorem (4 testes)
└── TestUtilities (3 testes)
```

Cada classe testa um grupo de funções relacionadas.

---

## 🎓 Executar Apenas um Teste

```powershell
# Testar apenas MDC
python -m unittest test_crypto_lib.TestMDCAndEuclides -v

# Testar apenas números primos
python -m unittest test_crypto_lib.TestPrimes -v
```

---

## 📈 Próximas Etapas

1. ✅ Missão 1 completa
2. 📤 Enviar para GitHub (GITHUB_SETUP.md)
3. 👥 Adicionar colaboradores
4. 📝 Fazer commit: `git add . && git commit -m "Adicionar guias de execução"`
5. 📡 Fazer push: `git push`

---

**Versão**: 1.0
**Data**: Setembro 2026
