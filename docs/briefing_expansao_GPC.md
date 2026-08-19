# Briefing — Expansão do Gerador de Plano de Estudos para o GPC

**Curso alvo:** GPC — Gestão da Pecuária de Corte
**Público:** equipe responsável pelo conteúdo/coordenação do GPC
**Objetivo:** reunir os materiais necessários para que o gerador de Plano de Estudos, hoje rodando no GPL (Gestão na Pecuária Leiteira), passe a atender também os alunos do GPC.

---

## 1. Contexto em 1 minuto

Hoje o fluxo do GPL funciona assim:

```
Aluno responde a pesquisa      →   CS exporta o CSV      →   Ferramenta casa as 3 dores
de início de curso (HubSpot)       do HubSpot                com os módulos do curso
                                                                      ↓
                                                    Plano de Estudos personalizado (PDF)
                                                    com link direto de cada módulo no AVA
```

A ferramenta **não inventa conteúdo e não decide a ordem**. Ela executa uma tabela de correspondência que a área de conteúdo define — e monta a trilha na ordem de prioridade que o próprio aluno indicou na pesquisa:

> "Se o aluno disse que a dor dele é **X**, o módulo que resolve isso é **Y**, que fica no link **Z**, tem **N** videoaulas e **T** horas."

Portanto, o que precisamos de vocês é essa tabela — completa, com a redação final e os links definitivos.

**O que já está pronto e será reaproveitado (vocês não precisam se preocupar):** o design do plano, o layout do PDF, o aplicativo do CS, o leitor do CSV do HubSpot e toda a lógica de montagem.

**O que é específico do GPC e depende de vocês:** as dores, os módulos, os links, os dados de cada módulo e o texto da pesquisa.

---

## 2. Os 5 entregáveis

| # | Entregável | Formato | Prioridade |
|---|---|---|---|
| A | **Matriz Dor → Módulo** (o coração do projeto) | Planilha (modelo em anexo) | 🔴 Bloqueia tudo |
| B | **Texto final da pesquisa do GPC** | Documento | 🔴 Bloqueia tudo |
| C | **CSV de teste exportado do HubSpot** | Arquivo `.csv` | 🟡 Após B |
| D | **Textos fixos e contato do CS** | Documento curto | 🟢 Pode vir depois |
| E | **2 planos "gabarito"** feitos à mão para validação | Documento | 🟢 Fase final |

---

### 🔴 Entregável A — Matriz Dor → Módulo

**O que é:** uma linha para cada dor que o aluno pode escolher na pesquisa, ligada ao módulo que resolve aquela dor.

**Formato:** planilha, uma linha por dor. Use o modelo `docs/modelos/modelo_matriz_dores_GPC.csv` (abre no Excel/Google Sheets).

**Colunas obrigatórias:**

| Coluna | O que preencher | Exemplo (GPL — para se espelhar) |
|---|---|---|
| `id` | Apelido curto, sem espaço nem acento. Só uso interno. | `gestao_financeira` |
| `dor_pesquisa` | **Texto EXATO** da opção como vai aparecer na pesquisa do HubSpot. | `Organizar os gastos, saber o custo do litro de leite para atuar no aumento do lucro.` |
| `dor_exibicao` | Como essa dor aparecerá impressa no card do plano do aluno. Pode ser uma versão mais enxuta. | `Organizar os gastos, saber o custo do litro de leite para atuar no aumento do lucro` |
| `dor_curta` | Rótulo de 2–5 palavras, usado nas telas internas do CS. | `Gestão financeira e custos` |
| `modulo` | Nome oficial do módulo, **idêntico ao que está no AVA**. | `Gestão financeira e econômica` |
| `link` | URL completa do módulo no Instructure. Link definitivo, não de rascunho. | `https://rehagro.instructure.com/courses/2859` |
| `qtd_videoaulas` | Número de videoaulas do módulo. Só o número. | `31` |
| `tempo_total` | Duração total de aula gravada. | `4h` |
| `programacao` | Ritmo de estudo sugerido. | `4 semanas (1h por semana – 8 videoaulas por semana)` |
| `atividades` | Atividades do módulo, com indicação do que é obrigatório. | `Teste seu conhecimento (obrigatório para a aprovação) e Atividade prática (extra)` |

**Regras que não podem ser quebradas:**

1. **Uma dor → exatamente um módulo.** Se duas dores levarem ao mesmo módulo, o aluno pode receber o mesmo módulo duas vezes no plano. Se uma dor precisar de dois módulos, precisamos conversar antes — a ferramenta hoje não faz isso.
2. **Toda dor listada na pesquisa precisa estar na matriz.** Se o aluno escolher uma opção que não está aqui, ela simplesmente não vira módulo no plano dele — o plano sai incompleto.
3. **A redação de `dor_pesquisa` tem que ser caractere por caractere igual à opção do HubSpot.** É por esse texto que a ferramenta reconhece a escolha do aluno. Vírgula a mais, "e" trocado por "ou", singular/plural — qualquer diferença quebra o casamento. (Acento e ponto final a ferramenta tolera; o resto não.)
4. **Nada de link provisório.** Se o módulo ainda não está publicado no AVA, marque a linha como "pendente" e nos avise — mas não coloque um link temporário, porque ele vai chegar ao aluno.

**Quantas dores?** No GPL são 9 dores para 9 módulos. Para o GPC, o ideal é ficar entre **8 e 12**. Menos que isso deixa a personalização fraca; mais que isso deixa a pesquisa cansativa.

**Critério de aceite:** planilha 100% preenchida, sem células vazias, com todos os links abrindo o módulo correto no AVA.

---

### 🔴 Entregável B — Texto final da pesquisa do GPC

**O que é:** o questionário que o aluno do GPC responde no início do curso, e que hoje é aplicado via HubSpot Survey.

A pesquisa tem duas partes:

**B.1 — Perguntas de contexto (precisam ser adaptadas para o corte)**

No GPL as perguntas são: volume de produção diária (litros/dia), número de animais em lactação e média de produção por vaca. **No corte esses indicadores não fazem sentido.** Vocês precisam definir os equivalentes. Sugestões para vocês avaliarem — a decisão é da área:

- Sistema de produção (cria / recria / engorda / ciclo completo / confinamento)
- Número de matrizes ou de cabeças
- Arrobas produzidas por ano / arrobas por hectare/ano
- Ganho médio diário, taxa de desmame, idade ao abate

Estas perguntas **não** entram na lógica do plano — elas servem para o CS conhecer o aluno. Então há liberdade total aqui: definam o que for útil.

**Mantenham estas perguntas como estão** (a ferramenta as usa): nome do matriculado, código da matrícula, nome do curso, e-mail, perfil ("Dono/Sócio, Consultor, Gerente..."), formação, "o que faria você dizer que valeu a pena" e "qual sua meta".

**B.2 — As perguntas de prioridade (esta parte é crítica)**

São elas que geram o plano. **Repliquem exatamente o modelo que o GPL já usa hoje:**

> *"Por último, queremos saber os 3 pontos mais importantes para você melhorar na sua fazenda nos próximos meses, em ordem de prioridade."*
>
> **Qual a primeira prioridade?** · **Qual a segunda prioridade?** · **Qual a terceira prioridade?**

- **Três perguntas separadas**, cada uma com **resposta única** (lista suspensa) e a **lista completa** de dores.
- As três são **obrigatórias** e o aluno **não pode repetir** a mesma opção ("Selecione uma opção diferente").
- As opções devem ser **exatamente** os textos da coluna `dor_pesquisa` da matriz do Entregável A.

**Por que esse formato:** a ordem que o aluno escolhe é a ordem em que os módulos aparecem no plano — a 1ª prioridade vira o 1º módulo da trilha. Não é detalhe de formulário: é o ranqueamento do aluno virando sequência de estudo. Uma pergunta de múltipla escolha ("marque até 3") não serve, porque devolve as opções na ordem da tela, e não na ordem de urgência do aluno.

**Critério de aceite:** documento com o texto final de todas as perguntas e opções, aprovado internamente, pronto para ser montado no HubSpot.

---

### 🟡 Entregável C — CSV de teste exportado do HubSpot

**O que é:** depois de a pesquisa do GPC estar montada no HubSpot, precisamos de um **CSV real exportado**, com pelo menos **5 respostas** (podem ser respostas de teste preenchidas pela própria equipe).

**Por que é indispensável:** a ferramenta localiza cada informação pelo nome da coluna do CSV. Sem ver o arquivo real, não temos como garantir que ela vai ler o export do GPC corretamente. É a única forma de validar antes de o primeiro aluno receber um plano.

**Como preparar as 5 respostas de teste:** variem as escolhas de propósito — uma escolhendo as 3 primeiras dores da lista, outra as 3 últimas, e pelo menos **uma com o ranqueamento fora da ordem da lista** (ex.: 1ª prioridade = última dor da lista). Essa última é a que prova que o plano está saindo na ordem do aluno, e não na ordem do formulário.

**Critério de aceite:** arquivo `.csv` exportado direto do HubSpot, sem edição manual (não abrir e salvar pelo Excel — isso altera o arquivo).

---

### 🟢 Entregável D — Textos fixos e contato

Itens curtos, mas necessários para o plano ficar completo:

| Item | O que precisamos | Como é no GPL |
|---|---|---|
| Nome do curso | Nome exato como deve aparecer impresso no plano | `GPC - Gestão da Pecuária de Corte` |
| Módulo de boas-vindas | Link do módulo de abertura do GPC no AVA (ele entra no início de todo plano, antes das 3 prioridades) | `https://rehagro.instructure.com/courses/2850` |
| Descrição do boas-vindas | Uma frase | "Para iniciar, veja como funciona o curso e os critérios que garantem sua aprovação." |
| WhatsApp do CS | Número do time que atende o GPC (se for diferente do time do leite) | (31) 99147-6763 |
| Mensagem de encerramento | Frase final do plano | "Conte com a gente sempre que precisar — pra você aproveitar ao máximo o curso e levar o resultado para sua fazenda. 🌱" |

---

### 🟢 Entregável E — 2 planos "gabarito"

**O que é:** peguem 2 das respostas de teste do Entregável C e montem à mão, num documento, como o plano daquele aluno **deveria** sair: quais 3 módulos, em que ordem, com quais links.

**Por que:** é o nosso teste de aceite. Comparamos o plano gerado pela ferramenta com o gabarito de vocês. Se bater, está aprovado para uso com alunos reais.

---

## 3. Ordem de execução

| Etapa | O que acontece | Responsável | Depende de |
|---|---|---|---|
| 1 | Definir a lista de dores do GPC e casar com os módulos | Área de conteúdo GPC | — |
| 2 | Levantar dados de cada módulo (link, nº de aulas, tempo, atividades) | Área de conteúdo GPC | Etapa 1 |
| 3 | Entregar a **matriz preenchida** (Entregável A) | Área de conteúdo GPC | Etapas 1 e 2 |
| 4 | Replicar no GPC o formato de prioridades do GPL (3 perguntas ranqueadas, resposta única, sem repetir opção) | Área + CS | — |
| 5 | Fechar o texto da pesquisa (Entregável B) | Área + CS | Etapas 3 e 4 |
| 6 | Montar a pesquisa no HubSpot | CS / Marketing | Etapa 5 |
| 7 | Preencher 5 respostas de teste e exportar o CSV (Entregável C) | CS | Etapa 6 |
| 8 | Configurar a ferramenta para o GPC | Time do projeto | Etapas 3 e 7 |
| 9 | Validar contra os gabaritos (Entregável E) e liberar | Área + CS | Etapa 8 |

---

## 4. Checklist de entrega

Antes de mandar os materiais, confiram:

- [ ] Toda dor da matriz tem um módulo, e todo módulo tem link definitivo que abre corretamente
- [ ] Nenhuma célula da planilha ficou em branco
- [ ] Os textos das opções da pesquisa são idênticos aos da coluna `dor_pesquisa`
- [ ] Nenhuma dor da pesquisa ficou de fora da matriz
- [ ] Nenhum módulo aparece em duas dores diferentes
- [ ] As 3 perguntas de prioridade são de resposta única, obrigatórias e não deixam repetir a mesma opção
- [ ] O CSV de teste foi exportado do HubSpot sem passar pelo Excel
- [ ] Os 2 gabaritos estão prontos

---

## 5. Pontos que precisam de decisão da área

Estas questões não travam o início do trabalho, mas precisam de resposta antes da entrega final:

1. **Número de módulos no plano:** o plano do GPC continua entregando 3 módulos, ou o curso pede um número diferente?
2. **Trilhas por perfil:** o GPC tem trilhas diferentes por sistema de produção (cria × engorda × ciclo completo)? Se sim, um mesmo texto de dor pode precisar apontar para módulos diferentes conforme o perfil do aluno — isso muda o desenho da ferramenta e precisa ser sinalizado agora.
3. **Módulos obrigatórios:** além do boas-vindas, existe algum módulo que deve entrar no plano de todo aluno do GPC?
4. **Dores sem módulo:** existe alguma dor relevante do produtor de corte que o GPC ainda não cobre? Se sim, ela deve ficar fora da pesquisa (para não frustrar o aluno).

---

## 6. Anexo — Exemplo real, linha completa do GPL

Para servir de referência de nível de detalhe esperado:

```
id              : gestao_financeira
dor_pesquisa    : Organizar os gastos, saber o custo do litro de leite para atuar no aumento do lucro.
dor_exibicao    : Organizar os gastos, saber o custo do litro de leite para atuar no aumento do lucro
dor_curta       : Gestão financeira e custos
modulo          : Gestão financeira e econômica
link            : https://rehagro.instructure.com/courses/2859
qtd_videoaulas  : 31
tempo_total     : 4h
programacao     : 4 semanas (1h por semana – 8 videoaulas por semana)
atividades      : Teste seu conhecimento (obrigatório para a aprovação) e Atividade prática (extra)
```

E é assim que essa linha chega ao aluno, dentro do card do plano:

```
┌──────────────────────────────────────────────────────────────┐
│  1        1ª Prioridade                                      │
│                                                              │
│  Gestão financeira e econômica                    ← modulo   │
│  Organizar os gastos, saber o custo do litro                 │
│  de leite para atuar no aumento do lucro     ← dor_exibicao  │
│                                                              │
│  [ Acessar módulo ]                                ← link    │
│                                                              │
│  Materiais de aula                                           │
│  31 videoaulas          ~4h de aula gravada                  │
│  Atividades: Teste seu conhecimento (obrigatório para a      │
│              aprovação) e Atividade prática (extra)          │
│  Programação: 4 semanas (1h por semana – 8 videoaulas)       │
└──────────────────────────────────────────────────────────────┘
```

---

**Dúvidas sobre este documento:** falar com o time do projeto de Plano de Estudos antes de preencher — meia hora de alinhamento no começo economiza retrabalho na matriz inteira.
