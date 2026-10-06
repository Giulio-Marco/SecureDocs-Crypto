# Resumo – Criptografia Clássica (Missão 2)

## Conceitos básicos

Criptografia é transformar uma mensagem para que só quem tem a chave consiga lê-la.

**Histórico.** As primeiras cifras surgiram na Antiguidade para uso militar e diplomático, como a de César em Roma. No século IX, o árabe Al-Kindi descreveu a análise de frequência, que quebra cifras de substituição simples. Isso levou às cifras polialfabéticas (Vigenère, século XVI) e, no século XX, às máquinas de rotor (Enigma) e à criptografia moderna baseada em matemática e computadores.

**Texto claro** (*plaintext*): a mensagem original, legível. Ex.: `TRANSFERIR DOCUMENTO`.

**Texto cifrado** (*ciphertext*): a mensagem após a transformação, ilegível sem a chave. Ex.: `WUDQVIHULU GRFXPHQWR` (César, k = 3).

**Cifragem**: o processo de transformar texto claro em texto cifrado usando um algoritmo e uma chave.

**Decifragem**: o processo inverso, que recupera o texto claro a partir do texto cifrado e da chave.

**Chave criptográfica**: o valor secreto que configura o algoritmo. O mesmo algoritmo com chaves diferentes produz textos cifrados diferentes. Ex.: na César, a chave é o deslocamento k.

**Criptoanálise**: o estudo de como quebrar uma cifra, ou seja, recuperar o texto claro ou a chave sem conhecê-la. As técnicas básicas são a força bruta e a análise de frequência.

**Princípio de Kerckhoffs** (1883): um sistema criptográfico deve continuar seguro mesmo que tudo sobre ele seja público, exceto a chave. A segurança tem que estar na chave, não no segredo do algoritmo.

## Algoritmos estudados

As cifras clássicas se dividem em duas famílias: **substituição** (troca as letras por outras) e **transposição** (mantém as letras, muda a posição). As letras são tratadas como números de 0 (A) a 25 (Z), e as contas são feitas módulo 26.

| Cifra | Família | Chave | Ideia | Nº de chaves |
| --- | --- | --- | --- | --- |
| César | Substituição monoalfabética | Inteiro k | Toda letra anda k casas: C = (P + k) mod 26 | 25 |
| Substituição | Substituição monoalfabética | Alfabeto embaralhado (26 letras) | Cada letra é trocada pela da tabela | 26! ≈ 4 × 10²⁶ |
| Afim | Substituição monoalfabética | Inteiros a e b, com mdc(a, 26) = 1 | C = (a·P + b) mod 26; decifra com o inverso de a | 312 (12 × 26) |
| Vigenère | Substituição polialfabética | Palavra | Uma César diferente por letra, seguindo a palavra-chave repetida | 26ᵐ (m = tamanho da palavra) |
| Hill | Substituição poligráfica | Matriz n × n com mdc(det, 26) = 1 | Blocos de n letras multiplicados pela matriz: C = K·P mod 26 | 157.248 (matriz 2 × 2) |
| Transposição colunar | Transposição | Palavra | Texto escrito em linhas, lido por colunas na ordem alfabética da chave | n! (n = nº de colunas) |
| Fluxo | Cifra de fluxo | Semente do gerador | Gera uma sequência pseudoaleatória (keystream) e faz XOR com o texto | 2³¹ (LCG usado) |

**Monoalfabética**: uma letra vira sempre a mesma letra. **Polialfabética**: a mesma letra pode virar letras diferentes conforme a posição. **Poligráfica**: cifra blocos de letras de uma vez.

Na biblioteca do grupo, Afim e Hill usam a `crypto_lib.py` da Missão 1: `saoCoprimo` valida a chave e `inverso_multi` calcula o inverso modular usado na decifragem.

## Fragilidades: força bruta e análise de frequência

Todas as cifras clássicas são quebráveis hoje, por um de dois caminhos.

**Força bruta**: testar todas as chaves possíveis até o texto fazer sentido. Funciona quando há poucas chaves: a César tem 25 e a Afim tem 312, o que um computador testa em milissegundos.

**Análise de frequência**: em português, algumas letras aparecem muito mais que outras (A, E e O são as mais comuns). Nas cifras monoalfabéticas, a letra mais frequente do texto cifrado provavelmente corresponde a A ou E. Por isso a Substituição, mesmo com 26! chaves, cai sem força bruta.

| Cifra | Como é quebrada |
| --- | --- |
| César | Força bruta (25 tentativas) ou frequência |
| Substituição | Análise de frequência de letras, pares e trios |
| Afim | Força bruta (312 tentativas) ou frequência: duas letras identificadas dão a e b |
| Vigenère | Descobre-se o tamanho da chave (método de Kasiski, índice de coincidência); depois, frequência em cada posição, como m Césares |
| Hill | Ataque de texto claro conhecido: com alguns pares texto claro/cifrado, a matriz sai por álgebra linear |
| Transposição | As frequências das letras não mudam, o que denuncia a transposição; depois, testa-se a ordem das colunas |
| Fluxo (LCG) | O gerador é previsível: poucos bytes conhecidos revelam o estado. Reusar a semente permite C₁ ⊕ C₂ = P₁ ⊕ P₂ |

## Por que esconder o algoritmo não é suficiente?

Porque o algoritmo acaba sendo descoberto, e a cifra precisa continuar segura quando isso acontecer. É o que diz o princípio de Kerckhoffs.

- **O algoritmo vaza.** Ele está no software instalado em vários computadores, pode ser obtido por engenharia reversa, por um funcionário ou por um invasor que acesse o servidor do SecureDocs.
- **Trocar um algoritmo é caro; trocar uma chave é barato.** Se o segredo é o algoritmo e ele vaza, o sistema inteiro precisa ser refeito. Se o segredo é a chave, basta gerar outra.
- **A criptoanálise não depende de conhecer o algoritmo.** A análise de frequência quebra uma substituição observando só os padrões do texto cifrado, sem saber qual cifra foi usada.
- **Algoritmo público é algoritmo testado.** Algoritmos abertos são atacados por muitos especialistas; os que resistem são confiáveis. Um algoritmo secreto nunca passou por esse teste.

Conclusão para o SecureDocs: a segurança deve vir de algoritmos públicos e bem estudados, com chaves secretas e grandes demais para força bruta. As cifras clássicas não atendem a isso e servem apenas como base para as próximas missões.
