# Como Executar a Biblioteca e Testes

## 🚀 Executar a Biblioteca com Exemplos

Execute no PowerShell:

```powershell
cd "c:\Users\giuli\OneDrive\Documents\Trabalho-Criptografia"
python crypto_lib.py
```

**Saída esperada**:
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
