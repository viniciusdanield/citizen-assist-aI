# FIAP - Faculdade de Informática e Administração Paulista
 
<p align="center">
<a href="https://www.fiap.com.br/">
  <img src="docs/imagens/logo-fiap.png" 
       alt="FIAP - Faculdade de Informática e Administração Paulista" 
       width="40%">
</a>
</p>
<br>
# Citizen Assist AI
 
## [Nome do grupo]
 
## 👨‍🎓 Integrantes: 
- <a href="https://linkedin.com/in/SEU-PERFIL">[Nome do integrante 1] - RM [00000]</a>
- <a href="https://linkedin.com/in/SEU-PERFIL">[Nome do integrante 2] - RM [00000]</a>
- <a href="https://linkedin.com/in/SEU-PERFIL">[Nome do integrante 3] - RM [00000]</a>
- <a href="https://linkedin.com/in/SEU-PERFIL">[Nome do integrante 4] - RM [00000]</a>
- <a href="https://linkedin.com/in/SEU-PERFIL">[Nome do integrante 5] - RM [00000]</a>
## 👩‍🏫 Professores:
 
### Tutor(a)
- <a href="https://linkedin.com/in/PERFIL-DO-TUTOR">[Nome do Tutor]</a>
  
### Coordenador(a)
- <a href="https://www.linkedin.com/in/andregodoichiovato/">André Godoi Chiovato</a>
## 📜 Descrição
 
O **Citizen Assist AI** é um assistente digital de texto, desenvolvido em Python, que ajuda cidadãos a encontrar orientações sobre documentos, serviços e temas comunitários. Ele consulta uma base de informações verificadas, apresenta a resposta junto com a fonte consultada e avisa com clareza quando não tem informação suficiente para orientar.
 
> ⚠️ **Aviso:** este projeto é um protótipo acadêmico. Ele **não é um canal oficial** de nenhum órgão público e não substitui a consulta às fontes oficiais.
 
### Problema, público beneficiado e temas abordados
 
Muitas pessoas encontram informações dispersas, termos difíceis ou instruções incompletas ao procurar orientações sobre serviços do cotidiano. Isso torna a busca lenta, confusa e sujeita a interpretações incorretas.
 
- **Público beneficiado:** [descrever, por exemplo: cidadãos que precisam de orientações simples sobre documentos e serviços].
- **Temas abordados:** [tema 1], [tema 2] e [tema 3].
### Organização da base de conhecimento
 
As orientações ficam no arquivo `data/base_conhecimento.json`, que é uma lista de registros. Cada registro é um dicionário com os campos obrigatórios:
 
| Campo | Descrição |
|---|---|
| `id` | Identificador único do registro (ex.: `DOC-001`) |
| `tema` | Tema da orientação (ex.: `documentos`) |
| `palavras_chave` | Lista de palavras usadas na busca |
| `orientacao` | Orientação resumida em linguagem simples |
| `referencia` | Link da fonte consultada |
| `data_verificacao` | Data em que a informação foi conferida na fonte |
 
Exemplo de registro:
 
```json
{
  "id": "DOC-001",
  "tema": "documentos",
  "palavras_chave": ["rg", "identidade", "segunda via"],
  "orientacao": "Texto resumido da orientação.",
  "referencia": "https://link-da-fonte-oficial",
  "data_verificacao": "2026-11-12"
}
```
 
- **Quantidade de registros:** [número] registros, distribuídos em [número] temas.
- **Origem das informações:** [descrever as fontes oficiais utilizadas].
- **Validação:** ao iniciar, o programa verifica se o arquivo existe, se não está vazio e se todos os registros possuem os campos obrigatórios preenchidos.
- **Manutenção:** novos registros podem ser acrescentados ou corrigidos editando apenas o JSON, sem alterar o código do programa.
### Estruturas de dados e estratégia de busca
 
- **Estruturas utilizadas:** lista de dicionários para os registros e dicionário para o grafo de temas relacionados.
- **Preparação da pergunta:** o texto é convertido para minúsculas, sem acentos e sem pontuação, e dividido em palavras.
- **Comparação:** para cada registro, conta-se quantas palavras-chave aparecem na pergunta. O registro com maior pontuação é o escolhido.
- **Várias correspondências (empate):** [descrever a regra decidida pelo grupo].
- **Pontuação mínima:** [descrever o mínimo para considerar que encontrou resposta].
- **Temas relacionados (grafo simples):** cada tema aponta para outros temas ligados a ele. Ao final de cada resposta, o sistema oferece esses temas como continuidade da consulta.
```python
relacionados = {
    "documentos": ["servicos", "direitos"],
    "servicos": ["documentos", "comunitario"],
    "direitos": ["documentos", "comunitario"],
    "comunitario": ["servicos", "direitos"],
}
```
 
[Ajustar o dicionário acima aos temas reais do grupo.]
 
### Regras de resposta, modelos de prompt e tratamento das limitações
 
O assistente usa condicionais e operações lógicas para tratar perguntas válidas, correspondências e ausência de orientação. Foram definidos dois modelos de resposta:
 
- **Modelo A (curto):** [papel do assistente, formato e obrigação de citar a fonte].
- **Modelo B (detalhado):** [papel do assistente, formato em passos, fonte, data de verificação e aviso de confirmação].
**Comparação:** [descrever o resultado da comparação nas mesmas perguntas e justificar qual modelo é mais claro e consistente].
 
**Tratamento de limitações:**
 
- Entrada vazia: o sistema pede que o usuário digite uma pergunta ou escolha um tema.
- Opção inexistente ou texto no lugar de número: o sistema avisa e mostra novamente as opções.
- Pergunta ambígua: o sistema informa a ambiguidade e sugere temas.
- Pergunta sem correspondência: o sistema informa que não há base suficiente, **não inventa orientações** e sugere outros temas.
### Plano de testes, indicadores e resultados
 
- **Perguntas de teste:** [número, mínimo 12], incluindo perguntas diretas, reformuladas, fora dos temas e três situações de limite (entrada vazia, consulta ambígua e ausência de resposta confiável). Arquivo: `data/perguntas_teste.json`.
- **Registro dos resultados:** resposta esperada, resposta obtida, acerto ou erro e tempo de consulta.
- **Taxa de acerto:** `acertos ÷ total × 100` = [resultado]%.
- **Tempo médio de consulta:** [resultado] segundos.
- **Teste de facilidade de uso:** [descrever o roteiro de tarefas, quem testou, dificuldades e resultados].
- **Interpretação dos indicadores:** [descrever].
- **Melhorias possíveis:** 1) [melhoria 1]; 2) [melhoria 2].
- **Limitações da avaliação:** [descrever].
### Exemplos de uso
 
**Consulta com resposta encontrada**
 
```
Pergunta: [exemplo de pergunta]
Resposta: [orientação resumida]
Fonte: [link]
Verificado em: [data]
Aviso: confirme as informações no canal oficial. Este assistente não é um canal oficial.
```
 
**Entrada vazia**
 
```
[mensagem exibida pelo sistema]
```
 
**Pergunta sem correspondência na base**
 
```
Pergunta: [exemplo fora dos temas]
Resposta: [aviso de que não há informação suficiente e sugestão de temas]
```
 
### Cuidados com clareza, acessibilidade, privacidade e informação não oficial
 
- **Clareza:** as orientações são escritas em linguagem simples, com mensagens objetivas.
- **Acessibilidade:** interface textual com menu numerado e mensagens compreensíveis, sem dependência de elementos visuais.
- **Privacidade:** o sistema **não solicita nem armazena dados pessoais**.
- **Informação não oficial:** o assistente não se apresenta como canal de órgãos públicos, sempre mostra a fonte consultada e recomenda a confirmação em canal oficial.
## 📁 Estrutura de pastas 
 
Abaixo encontra-se a descrição da organização da raiz do projeto e a finalidade de cada diretório e arquivo:
 
* **`data/`** Armazena a base de conhecimento (`base_conhecimento.json`) e as perguntas de teste (`perguntas_teste.json`).
* **`docs/`** Centraliza a documentação do projeto, incluindo o registro de uso de IA (`uso_ia.md`) e imagens usadas no README.
* **`src/`** Contém o código-fonte em Python. O arquivo principal é `sistema.py`.
* **`README.md`** Este ficheiro. Funciona como o guia principal de introdução, configuração e contextualização do projeto.
## 📎 Links e Observações
 
### 🔗 Links do Projeto
 
* **[Vídeo de apresentação no YouTube]**([COLAR AQUI O LINK DO VÍDEO]) - Demonstração do funcionamento do sistema (vídeo não listado).
### 🧠 Decisões Técnicas
 
> - **JSON como base de conhecimento:** formato simples, legível e fácil de editar, o que permite acrescentar ou corrigir orientações sem mexer no código.
> - **Listas e dicionários:** organizam os registros e permitem recuperar informações por identificador, tema ou palavras-chave.
> - **Busca por palavras-chave com pontuação:** simples de explicar e de testar, e adequada ao tamanho da base.
> - **Grafo simples de temas relacionados:** permite navegar entre assuntos ligados após cada resposta.
> - **Sem APIs externas ou modelos de IA:** as respostas vêm somente da base verificada, o que evita informações inventadas.
> - [Acrescentar outras decisões do grupo.]
 
### 📢 Observações Gerais
 
* **Participação na Competição:** [ ] Sim, aceitamos participar / [ ] Não vamos participar.
* *Outras observações gerais (opcional):* O uso de inteligência artificial no desenvolvimento está documentado em `docs/uso_ia.md`.
## 🔧 Como executar o código
 
**Pré-requisitos**
 
- Python 3.[versão utilizada] ou superior instalado.
- [Bibliotecas adicionais, se houver. Se usar apenas a biblioteca padrão, escrever: "Não há dependências externas."]
**Passo a passo**
 
1. Baixe o repositório:
```bash
   git clone [LINK DO REPOSITÓRIO]
```
2. Entre na pasta do projeto:
```bash
   cd [NOME-DO-REPOSITÓRIO]
```
3. Execute o sistema:
```bash
   python src/sistema.py
```
 
## 🏁 Conclusões, limitações e melhorias
 
- **Conclusões:** [descrever].
- **Limitações:** [descrever, por exemplo: base pequena, busca por palavras-chave sem entender sinônimos].
- **Possibilidades de melhoria:** [descrever].
---
 
## 📋 Licença
 
<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1"><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1"><p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/"><a property="dct:title" rel="cc:attributionURL" href="https://github.com/fiap-tutoria/FIAP-PORTFOLIO-AI">TEMPLATE - FIAP PORTFÓLIO AI</a> por <a rel="cc:attributionURL dct:creator" property="cc:attributionName" href="https://fiap.com.br">FIAP</a> está licenciado sobre <a href="http://creativecommons.org/licenses/by/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">Attribution 4.0 International</a>.</p>
