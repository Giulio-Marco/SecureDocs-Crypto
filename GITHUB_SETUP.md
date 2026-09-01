# Guia: Como Criar o Repositório no GitHub e Adicionar Colaboradores

## ✅ O que foi feito

A biblioteca de criptografia foi criada e o repositório Git local foi inicializado com o primeiro commit!

### Arquivos criados:
- ✅ `crypto_lib.py` - Biblioteca com todos os algoritmos
- ✅ `test_crypto_lib.py` - Suite de testes unitários
- ✅ `README.md` - Documentação do projeto
- ✅ `DOCUMENTACAO.md` - Documentação técnica detalhada
- ✅ `.gitignore` - Configuração para Git
- ✅ `LICENSE` - Licença MIT
- ✅ `pyproject.toml` - Configuração Python

### Status do Git local:
- ✅ Repositório inicializado
- ✅ Configuração de usuário: "SecureDocs Team"
- ✅ Primeiro commit realizado

---

## 📝 Próximas Etapas: Criar Repositório no GitHub

### Informações do Repositório Solicitado:
- **Nome**: `SecureDocs - Criptografia - Trabalho` (ou simplificar para `SecureDocs-Crypto`)
- **Visibilidade**: Privado
- **Colaboradores a adicionar**:
  - enzo.simon.luz10@gmail.com
  - FelipeDeSousa06

---

## 🚀 Passo 1: Criar o Repositório no GitHub

### Opção A: Via Website (Recomendado se não tiver GitHub CLI)

1. Acesse [github.com](https://github.com) e faça login
2. Clique no `+` no topo direito e selecione **"New repository"**
3. Preencha os dados:
   - **Repository name**: `SecureDocs-Crypto` (sem espaços)
   - **Description**: "Biblioteca de algoritmos criptográficos - Missão 1 SecureDocs"
   - **Visibility**: Marque **Private**
   - **Initialize repository**: NÃO marque nenhuma opção (já temos conteúdo)
4. Clique em **Create repository**

### Opção B: Via GitHub CLI (se instalar)

```powershell
# Instalar GitHub CLI (uma vez)
choco install gh

# Depois fazer login
gh auth login

# Criar o repositório
gh repo create SecureDocs-Crypto `
  --private `
  --source=. `
  --remote=origin `
  --push
```

---

## 🔗 Passo 2: Conectar o Repositório Local ao Remoto

Após criar no GitHub, execute os comandos no PowerShell:

```powershell
# Navegar até a pasta do projeto
cd "c:\Users\giuli\OneDrive\Documents\Trabalho-Criptografia"

# Adicionar o repositório remoto (substitua USUARIO pelo seu username)
git remote add origin https://github.com/USUARIO/SecureDocs-Crypto.git

# Alterar a branch padrão para main (opcional, mas recomendado)
git branch -M main

# Fazer push do código para o GitHub
git push -u origin main
```

**Substitua `USUARIO` pelo seu nome de usuário do GitHub!**

---

## 👥 Passo 3: Adicionar Colaboradores

### Via Website:

1. Acesse seu repositório no GitHub
2. Clique em **Settings** → **Collaborators** (ou **Manage access**)
3. Clique em **Add people** ou **Invite collaborators**
4. Digite o email ou username do colaborador:
   - `enzo.simon.luz10@gmail.com` ou username no GitHub
   - `FelipeDeSousa06`
5. Clique em **Add** para enviar o convite
6. O colaborador receberá um email e poderá aceitar o acesso

### Via GitHub CLI:

```powershell
# Adicionar primeiro colaborador
gh repo add-collaborators SecureDocs-Crypto `
  --permission push `
  enzo.simon.luz10

# Adicionar segundo colaborador
gh repo add-collaborators SecureDocs-Crypto `
  --permission push `
  FelipeDeSousa06
```

**Nota**: Os usernames precisam corresponder aos perfis do GitHub. Se não funcionar, use os emails.

---

## 🔐 Níveis de Acesso

Ao adicionar colaboradores, escolha o nível de permissão:

| Nível | Permissões |
|-------|-----------|
| **Pull** | Apenas ler e fazer fork |
| **Push** | Ler e fazer commits (recomendado para grupo) |
| **Admin** | Controle total do repositório |

Para um trabalho em grupo, use **Push** para ambos.

---

## 📡 Após Configurar o Remoto

### Para sincronizar mudanças:

```powershell
# Fazer commit local
git add .
git commit -m "Sua mensagem de commit"

# Enviar para GitHub
git push

# Buscar atualizações do remoto
git pull
```

### Seus colaboradores podem:

```powershell
# Clonar o repositório
git clone https://github.com/USUARIO/SecureDocs-Crypto.git

# Trabalhar e fazer commits
git add .
git commit -m "Sua mudança"

# Enviar mudanças
git push
```

---

## ✨ Checklist de Conclusão

- [ ] Repositório criado no GitHub
- [ ] Código enviado (git push)
- [ ] Colaborador 1 adicionado e confirmado
- [ ] Colaborador 2 adicionado e confirmado
- [ ] Ambos os colaboradores conseguem fazer pull/push
- [ ] Arquivo CONTRIBUINDO.md criado (opcional)

---

## 🆘 Troubleshooting

### "fatal: remote origin already exists"
```powershell
git remote remove origin
git remote add origin https://github.com/USUARIO/SecureDocs-Crypto.git
```

### "Permission denied (publickey)"
```powershell
# Configure suas credenciais SSH ou use HTTPS
git config --global user.email "seu.email@github.com"
git config --global user.name "Seu Nome"
```

### Colaborador não recebeu convite
- Verifique se o email/username está correto
- Peça que o colaborador verifique a pasta de spam
- Use o GitHub CLI com o username correto

---

## 📚 Próximas Missões

Após concluir a Missão 1, o repositório será a base para:
- **Missão 2**: Criptografia Simétrica (AES, DES)
- **Missão 3**: Criptografia Assimétrica (RSA)
- **Missão 4**: Funções Hash e Assinatura Digital

Cada missão adicionará novos arquivos e funcionalidades ao mesmo repositório.

---

## 💡 Dicas Importantes

1. **Faça commits frequentes** - Não acumule mudanças
2. **Use mensagens descritivas** - "Implementar algoritmo X" é melhor que "fix"
3. **Puxe antes de empurrar** - `git pull` antes de `git push`
4. **Crie branches para features** - Para trabalhos paralelos
5. **Revise código** - Use Pull Requests para análise

---

**Última atualização**: Setembro 2026
**Versão**: 1.0
