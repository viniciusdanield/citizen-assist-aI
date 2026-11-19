# FIAP - Faculdade de Informática e Administração Paulista

<p align="center">
<a href="https://www.fiap.com.br/">
  <img src="https://upload.wikimedia.org/wikipedia/commons/d/d4/Fiap-logo-novo.jpg"
       alt="FIAP - Faculdade de Informática e Administração Paulista"
       width="40%">
</a>
</p>

# Citizen Assist AI

## [Grupo 13]

## 👨‍🎓 Integrantes:

- <a href="https://www.linkedin.com/in/viniciusdanield/">Vinícius Daniel de Borba - RM 572091</a>
- <a href="https://www.linkedin.com/in/vitorarafe/">Vitor de Araujo Ferreira - RM 572838</a>
- <a href="https://www.linkedin.com/in/anacfmafra/">Ana Carolina Freire Mafra - RM 573650</a>
- <a href="https://linkedin.com/in/SEU-PERFIL">Daniel Guimarães Barreto - RM 573425</a>
- <a href="https://linkedin.com/in/SEU-PERFIL">Paulo Henrique da Silva Gola - RM 572992</a>

## 👩‍🏫 Professores:

### Tutor(a)

- <a href="https://www.linkedin.com/in/andretritiack/">[André Tritiack]</a>

### Coordenador(a)

- <a href="https://www.linkedin.com/in/andregodoichiovato/">André Godoi Chiovato</a>

## 📜 Descrição

O **Citizen Assist AI** é um assistente digital de texto, desenvolvido em Python, que ajuda cidadãos a encontrar orientações sobre documentos, serviços e temas comunitários.

O sistema consulta uma base de conhecimento estruturada em JSON, identifica informações relacionadas à pergunta do usuário e apresenta orientações em linguagem simples, acompanhadas da fonte consultada e da data de verificação.

Quando não encontra informações suficientes, o assistente informa essa limitação, evitando inventar orientações ou apresentar respostas sem respaldo na base de conhecimento.

> ⚠️ **Aviso:** este projeto é um protótipo acadêmico. Ele não é um canal oficial de nenhum órgão público e não substitui a consulta às fontes oficiais.

### Problema, público beneficiado e temas abordados

Muitas pessoas encontram informações dispersas, termos difíceis ou instruções incompletas ao procurar orientações sobre serviços do cotidiano. Isso torna a busca lenta, confusa e sujeita a interpretações incorretas.

- **Público beneficiado:** cidadãos que precisam de orientações simples e com fontes indicadas sobre direitos do trabalhador, direitos do consumidor, cuidados com o meio ambiente, educação e trânsito.
- **Temas abordados:** trabalho, consumidor, meio ambiente, educação e trânsito.

### Organização da base de conhecimento

As orientações ficam no arquivo `data/base_conhecimento.json`, estruturado como uma lista de registros. Cada registro é um dicionário com os seguintes campos:

| Campo | Descrição |
|---|---|
| `id` | Identificador único do registro (ex.: `TRAB-001`) |
| `tema` | Tema da orientação (ex.: `trabalho`) |
| `palavras_chave` | Lista de palavras e expressões utilizadas na busca |
| `orientacao` | Orientação resumida em linguagem simples |
| `referencia` | Link da fonte consultada |
| `data_verificacao` | Data em que a informação foi conferida na fonte |

Exemplo de registro:

```json
{
  "id": "TRAB-003",
  "tema": "trabalho",
  "palavras_chave": [
    "recurso",
    "recurso seguro desemprego",
    "seguro desemprego negado",
    "indeferido"
  ],
  "orientacao": "Se o pedido de seguro-desemprego for negado, é possível pedir revisão por meio de um recurso administrativo ao Ministério do Trabalho e Emprego.",
  "referencia": "https://www.gov.br/pt-br/servicos/cadastrar-recurso-relativo-ao-seguro-desemprego",
  "data_verificacao": "2026-11-19"
}
```

- **Quantidade de registros:** 25 registros, distribuídos em 5 temas, com 5 orientações por tema.
- **Origem das informações:** páginas oficiais do Governo Federal, portais de serviços públicos, órgãos estaduais e instituições responsáveis pelos serviços abordados. Cada registro possui seu próprio link de referência e data de verificação.
- **Validação:** ao iniciar, o programa verifica se o arquivo existe, se não está vazio e se os registros possuem os campos obrigatórios preenchidos.
- **Manutenção:** novos registros podem ser acrescentados ou corrigidos diretamente no JSON, sem necessidade de alterar o código principal.

### Estruturas de dados e estratégia de busca

O sistema utiliza estruturas de dados e técnicas de comparação textual para localizar orientações relacionadas às perguntas dos usuários.

- **Estruturas utilizadas:** lista de dicionários para armazenar os registros, dicionários para organizar o grafo de temas relacionados e conjuntos (`set`) para auxiliar na comparação das palavras.
- **Preparação da pergunta:** o texto é convertido para letras minúsculas, normalizado para remover acentos e pontuação e dividido em palavras. Palavras comuns, como "de", "um" e "para", são ignoradas. O sistema também realiza tratamento de variações simples, como plural e singular.
- **Comparação:** as palavras-chave são comparadas com os termos presentes na pergunta. Uma expressão pode ser reconhecida quando todas as suas palavras aparecem no texto, mesmo que não estejam necessariamente em sequência. Expressões mais específicas recebem maior pontuação do que palavras isoladas.
- **Seleção de resultados:** o sistema utiliza a pontuação para identificar os registros mais relacionados à pergunta. Quando existem múltiplas correspondências relevantes, a aplicação trata a situação como ambígua e apresenta possibilidades relacionadas.
- **Pontuação mínima:** uma correspondência positiva é suficiente para considerar que existe um resultado. Quando nenhuma palavra-chave corresponde, o sistema informa que não encontrou orientação confiável na base.
- **Temas relacionados (grafo simples):** cada tema possui conexões com outros assuntos. Ao final das consultas, o sistema pode sugerir temas relacionados para dar continuidade à navegação.

Exemplo do grafo de temas relacionados:

```python
RELACIONADOS = {
    "trabalho":      ["consumidor", "meio_ambiente", "educacao", "transito"],
    "consumidor":    ["trabalho", "meio_ambiente", "transito"],
    "meio_ambiente": ["consumidor", "trabalho", "educacao"],
    "educacao":      ["trabalho", "meio_ambiente"],
    "transito":      ["consumidor", "trabalho"],
}
```

As relações são utilizadas para recomendar outros assuntos disponíveis na base de conhecimento, permitindo que o cidadão explore diferentes temas.

### Regras de resposta, modelos de prompt e tratamento das limitações

O assistente utiliza estruturas condicionais e operações lógicas para tratar perguntas válidas, resultados encontrados, ambiguidades e situações sem orientação disponível.

Foram definidos dois modelos de resposta, que podem ser alternados pela opção correspondente no menu principal:

- **Modelo A (curto):** apresenta a orientação de forma objetiva e resumida, acompanhada da fonte consultada e de um lembrete para confirmar as informações no canal oficial. É voltado à rapidez e facilidade de leitura.
- **Modelo B (detalhado):** apresenta o tema, a orientação, a fonte consultada, a data de verificação e um aviso explícito de que o assistente não é um canal oficial. É voltado à transparência e ao fornecimento de contexto adicional.

**Comparação dos modelos:**

O Modelo A prioriza a objetividade e permite que o usuário encontre rapidamente a informação principal. O Modelo B oferece mais contexto, apresenta a data de verificação e reforça a natureza não oficial do projeto.

Os dois modelos utilizam as mesmas informações da base de conhecimento. A diferença está na organização e na quantidade de detalhes apresentados ao usuário.

**Tratamento de limitações:**

- **Entrada vazia:** o sistema informa que nenhuma pergunta foi digitada e retorna ao fluxo de interação.
- **Opção inexistente ou texto no lugar de número:** o sistema apresenta uma mensagem de erro e solicita uma nova escolha.
- **Pergunta ambígua:** o sistema identifica múltiplas correspondências relevantes e apresenta as possibilidades relacionadas.
- **Pergunta sem correspondência:** o sistema informa que não encontrou orientação suficiente, não inventa informações e sugere temas disponíveis.
- **Base de conhecimento inválida ou indisponível:** o programa verifica problemas no carregamento e na estrutura dos dados, evitando utilizar registros inválidos.

### Plano de testes, indicadores e resultados

A validação do sistema foi realizada por meio de testes automatizados, utilizando o arquivo `data/perguntas_teste.json` e o script `src/testes.py`.

**Perguntas de teste:**

Foram definidos 29 cenários, distribuídos da seguinte forma:

| Tipo de teste | Quantidade |
|---|---:|
| Perguntas diretas | 16 |
| Perguntas reformuladas | 8 |
| Perguntas fora dos temas | 2 |
| Situações de limite | 3 |
| **Total** | **29** |

As situações de limite contemplam entrada vazia, consulta ambígua e ausência de resposta confiável.

**Registro dos resultados:**

O script automatizado compara a resposta esperada com a classificação obtida pelo sistema, registrando:

- Pergunta realizada;
- Tipo de cenário;
- Resultado esperado;
- Resultado obtido;
- Classificação de acerto ou erro;
- Tempo de consulta em milissegundos.

Os resultados são armazenados automaticamente em `data/resultados_testes.json`.

**Resultados obtidos na execução final:**

| Indicador | Resultado |
|---|---:|
| Perguntas testadas | 29 |
| Acertos | 29 |
| Erros | 0 |
| Taxa de acerto | **100%** |
| Tempo médio de consulta | **1,1671 ms** |

**Cálculo da taxa de acerto:**

`29 ÷ 29 × 100 = 100%`

**Tempo médio de consulta:**

A média registrada foi de aproximadamente 1,1671 milissegundos por pergunta. Esse tempo considera o processamento de busca e classificação, não o tempo total de interação de uma pessoa com o assistente.

**Interpretação dos indicadores:**

O sistema apresentou o comportamento esperado em todos os 29 cenários definidos, incluindo perguntas diretas, reformuladas e situações de limite.

Durante a validação, foi identificada uma ambiguidade entre os registros de consulta de multas e contestação de multas de trânsito. O problema foi solucionado por meio do refinamento das palavras-chave do registro `TRAN-002`, sem necessidade de modificar o algoritmo principal de busca.

Após o ajuste, a execução final apresentou 29 acertos e nenhum erro.

Os resultados indicam que a estratégia de busca atende aos cenários definidos pela equipe, considerando o tamanho e o conteúdo atual da base de conhecimento.

### Simulação de teste de usabilidade

Foi elaborada uma simulação de avaliação de usabilidade considerando o perfil de uma pessoa com conhecimentos básicos em tecnologia e sem participação no desenvolvimento do projeto.

Foram consideradas seis tarefas: consultar os temas disponíveis, realizar uma pergunta sobre seguro-desemprego, enviar uma entrada vazia, consultar um assunto fora do escopo, navegar entre temas relacionados e alternar entre os modelos de resposta.

Na simulação, todas as tarefas foram consideradas concluídas. As observações indicaram que a navegação por menus e a apresentação das orientações são compreensíveis, embora a leitura das opções possa exigir atenção de usuários menos familiarizados com sistemas textuais.

Como possíveis melhorias, foram identificadas a simplificação das opções de navegação e a apresentação ainda mais clara das mensagens de orientação.

**Limitação:** estes resultados são simulados e não representam uma avaliação realizada com um participante real.

**Melhorias possíveis:**

1. Ampliar o vocabulário de palavras-chave e expressões utilizadas pelos cidadãos, aumentando a capacidade de reconhecer diferentes formas de formular uma pergunta.
2. Aprimorar a identificação de sinônimos e variações linguísticas, reduzindo ambiguidades e aumentando a flexibilidade da busca.

**Limitações da avaliação:**

A avaliação foi realizada com um conjunto de 29 perguntas previamente definidas pela equipe. Por isso, a taxa de acerto de 100% representa o desempenho nesses cenários específicos e não garante precisão equivalente para todas as possíveis perguntas de usuários reais.

Além disso, o tempo registrado mede somente a busca e a classificação, não considerando o tempo de leitura ou navegação do usuário. A quantidade de registros também é limitada, e as informações da base precisam ser revisadas periodicamente, pois serviços e regras públicas podem sofrer alterações.

### Exemplos de uso

**Consulta com resposta encontrada (Modelo B)**

```text
Pergunta: como pedir o seguro-desemprego

Resposta:

Assistente de orientação cidadã (informação não oficial)

Tema: trabalho

Orientação:
O seguro-desemprego é um benefício para quem foi dispensado sem justa causa. O pedido pode ser feito pelo portal de serviços do governo, pelo aplicativo da Carteira de Trabalho Digital, pelo telefone 158 ou presencialmente, e a liberação pode ser acompanhada no gov.br ou no aplicativo.

Fonte consultada:
https://www.gov.br/pt-br/servicos/solicitar-o-seguro-desemprego

Verificado em: 2026-11-19

Atenção:
As regras podem mudar. Confirme no site oficial antes de agir. Este assistente não é um canal oficial de órgãos públicos.
```

**Entrada vazia**

```text
Digite sua pergunta:

Você não digitou nada.
```

**Pergunta sem correspondência na base**

```text
Pergunta: como tirar o rg

Resposta:
Não encontrei uma orientação sobre isso na base.

Tente outras palavras ou escolha um dos temas disponíveis:
trabalho, consumidor, meio_ambiente, educacao ou transito.
```

### Cuidados com clareza, acessibilidade, privacidade e informação não oficial

- **Clareza:** as orientações são escritas em linguagem simples, com mensagens objetivas e informações organizadas.
- **Acessibilidade:** interface textual com menu numerado e mensagens compreensíveis, sem dependência de elementos visuais.
- **Privacidade:** o sistema não solicita nem armazena dados pessoais dos cidadãos.
- **Informação não oficial:** o assistente não se apresenta como canal de órgãos públicos, apresenta a fonte consultada e recomenda a confirmação das informações nos canais oficiais.

## 📁 Estrutura de pastas

Abaixo encontra-se a descrição da organização da raiz do projeto e a finalidade de cada diretório e arquivo:

- **`data/`** Armazena a base de conhecimento (`base_conhecimento.json`), as perguntas de teste (`perguntas_teste.json`) e o registro dos resultados dos testes (`resultados_testes.json`).
- **`docs/`** Centraliza a documentação do projeto, incluindo o registro de uso de IA (`uso_ia.md`) e possíveis imagens utilizadas no README.
- **`notebooks/`** Diretório destinado aos notebooks e materiais auxiliares de desenvolvimento e experimentação.
- **`src/`** Contém o código-fonte em Python. O arquivo principal é `sistema.py` e os testes automatizados ficam em `testes.py`.
- **`README.md`** Guia principal de introdução, configuração e contextualização do projeto.

## 📎 Links e Observações

### 🔗 Links do Projeto

- **Repositório GitHub:** [https://github.com/viniciusdanield/citizen-assist-aI.git]
- **Vídeo de apresentação no YouTube:** [COLAR AQUI O LINK DO VÍDEO] — demonstração do funcionamento do sistema (vídeo não listado).

### 🧠 Decisões Técnicas

- **JSON como base de conhecimento:** formato simples, legível e fácil de editar, permitindo acrescentar ou corrigir orientações sem modificar o código principal.
- **Listas e dicionários:** organizam os registros e permitem recuperar informações por identificador, tema ou palavras-chave.
- **Conjuntos (`set`):** auxiliam na comparação dos termos e na identificação de correspondências.
- **Busca por palavras-chave com pontuação:** estratégia simples de explicar, implementar e testar, adequada ao tamanho atual da base.
- **Grafo simples de temas relacionados:** permite navegar entre assuntos ligados após cada resposta.
- **Separação entre dados e código:** facilita a manutenção e atualização da base de conhecimento.
- **Sem APIs externas ou modelos de IA em tempo de execução:** as respostas são construídas a partir dos registros locais da base de conhecimento, evitando a geração de orientações sem fonte cadastrada.

### 📢 Observações Gerais

- **Participação na Competição:** [YES] Sim, aceitamos participar
- **Outras observações gerais (opcional):** o uso de inteligência artificial durante o desenvolvimento está documentado em `docs/uso_ia.md`.

## 🔧 Como executar o código

### Pré-requisitos

- Python 3.8 ou superior instalado.
- Não há dependências externas. O projeto utiliza recursos da biblioteca padrão do Python.

### Passo a passo

**1. Baixe o repositório:**

```bash
git clone [https://github.com/viniciusdanield/citizen-assist-aI.git]
```

**2. Entre na pasta do projeto:**

```bash
cd citizen-assist-aI
```

**3. Execute o sistema:**

```bash
python src/sistema.py
```

**4. (Opcional) Execute os testes automatizados:**

```bash
python src/testes.py
```

Ao executar os testes, o programa apresenta os resultados no terminal e atualiza o arquivo `data/resultados_testes.json`.

## 🏁 Conclusões, limitações e melhorias

**Conclusões:**

O Citizen Assist AI foi desenvolvido para facilitar o acesso a orientações sobre serviços e temas do cotidiano, utilizando uma base de conhecimento estruturada e uma interface textual simples.

O sistema permite consultar informações por meio de perguntas ou navegação por temas, apresenta fontes de referência, disponibiliza dois modelos de resposta e trata situações em que não encontra informações suficientes.

Na execução final dos testes automatizados, o sistema alcançou 100% de acerto nos 29 cenários avaliados, com tempo médio de consulta de 1,1671 ms.

**Limitações:**

- Base de conhecimento limitada a 25 registros e 5 temas.
- Busca baseada em palavras-chave, sem compreensão semântica completa das perguntas.
- Possibilidade de ambiguidades quando diferentes registros apresentam termos semelhantes.
- Informações públicas sujeitas a alterações, exigindo revisão periódica das fontes.
- Avaliação limitada ao conjunto de perguntas definido pela equipe.

**Possibilidades de melhoria:**

- Ampliar a base de conhecimento com novos serviços, orientações e temas.
- Adicionar sinônimos e expressões utilizadas no cotidiano.
- Aprimorar o tratamento de perguntas ambíguas.
- Realizar testes com mais usuários para avaliar clareza, facilidade de uso e eficiência.
- Implementar mecanismos adicionais de atualização e verificação das fontes.

---

## 📋 Licença

<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1"><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1">

<p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/">
<a property="dct:title" rel="cc:attributionURL" href="https://github.com/fiap-tutoria/FIAP-PORTFOLIO-AI">TEMPLATE - FIAP PORTFÓLIO AI</a> por
<a rel="cc:attributionURL dct:creator" property="cc:attributionName" href="https://fiap.com.br">FIAP</a>
está licenciado sob
<a href="http://creativecommons.org/licenses/by/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">Attribution 4.0 International</a>.
</p>