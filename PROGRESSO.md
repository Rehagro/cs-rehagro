# Progresso e próximos passos — CS Rehagro

Último marco: **Deploy da correção das dores + ficha do módulo de Sistemas de produção preenchida em 2026-08-20.**

## 📚 Sistemas de produção ganhou aulas e tempo — 2026-08-20

O card de **Sistemas de produção e visão estratégica do negócio leite** saía no plano com `—` em *videoaulas* e *de aula gravada*: era o único módulo sem esses dados no "Plano de aula - arquivo 2.docx", e `core/mapeamento.py` refletia isso com `aulas: None, tempo: None`. O material foi atualizado pela área de conteúdo e os valores entraram: **16 videoaulas, ~2,5h**.

**Ainda pendente no material:** a linha de *Programação* desse módulo continua incompleta no arquivo ("assistir esse conteúdo em ___ semanas (1h por semana – ___ videoaulas por semana)"). Enquanto a área não fechar o número de semanas, `programacao` fica `None` e o card imprime `—` nessa linha — os outros 8 módulos têm a frase completa. Não foi preenchido por dedução de propósito: é texto que vai impresso para o aluno.

## 🚀 Deploy: a correção das dores só foi ao ar em 2026-08-20

Os commits de 19/08 (prioridades ranqueadas + diagnóstico na tela) ficaram um dia **só na máquina local** (`main` 3 commits à frente de `origin/main`). Como o Streamlit Cloud roda o `origin/main`, o app publicado seguia com o parser antigo e um CSV do formato novo entrava e saía com 0 módulos — o mesmo sintoma que a correção resolvia. **Regra:** ajuste no gerador só está entregue depois do `git push`; antes de investigar o parser, conferir `git status -sb`.

## 🐛 Gerador voltou a casar as dores — 2026-08-19

O formulário de início de curso migrou para `gpl.rehagro.com.br/pesquisa-onboarding` e o export mudou em dois pontos que **zeravam o plano** (o CSV entrava, o aluno aparecia, e a trilha saía com 0 módulos — botão de gerar desabilitado):

1. **As 3 prioridades agora vêm em 3 colunas** ("Qual a primeira/segunda/terceira prioridade?"). O parser procurava uma única coluna com "3 pontos mais importantes", que não existe mais → campo vazio.
2. **A redação das opções mudou.** 3 das 9 dores (`sistemas_producao`, `gestao_financeira`, `indicadores_rebanho`) tinham texto incompatível com o do formulário, e o casamento é por substring.

**Correções:**
- `core/mapeamento.py`: cada dor ganhou `variantes` — outras redações aceitas para a mesma dor. `match_dores` percorre canônica + variantes, e o novo `match_dor_unica()` casa o valor de uma coluna de prioridade. Mudança de redação no formulário agora é aditiva, não destrutiva.
- `core/hubspot_csv.py`: `_casar_prioridades()` lê as 3 colunas ranqueadas (e ignora repetição da mesma opção); cai para o campo combinado antigo se elas não existirem. Cabeçalhos com HTML (`<strong>`, `<span style=...>`) não atrapalham, porque a busca é por substring normalizada. Também mapeia `qtd_animais_lactacao` (nome interno da propriedade) para `animais`.

**Ganho de produto:** a ordem das colunas é o ranqueamento real do aluno, então **a 1ª prioridade dele é o 1º módulo do plano** — a ressalva antiga ("a ordem do CSV não é o ranking") deixou de valer.

**Decisão (2026-08-19):** a opção *"Reduzir perdas no processo da ensilagem e desensilagem"* **sai da pesquisa no HubSpot** — era a única dor da lista sem módulo correspondente, e quem a escolhesse receberia um plano com 2 módulos. Nada muda no código (ela nunca esteve em `DORES`); a lista do formulário passa a ter 9 opções, uma para cada módulo. A regra vale como princípio: **dor sem módulo não entra na pesquisa.**

**Pendência com a área de conteúdo:**
- O mapeamento de *"Planejar a necessidade de forragem do rebanho, calculando os indicadores..."* → **Indicadores reprodutivos e Evolução de rebanho** foi deduzido pela posição na lista; confirmar se não é *Planejamento forrageiro e manejo alimentar*.

## 🚦 Diagnóstico do CSV na tela — 2026-08-19

Antes, um CSV incompleto ou com redação divergente só aparecia como "0 módulos" e botão desabilitado — sem dizer o que estava errado. Agora `core/validacao.py` diagnostica o arquivo e o aluno, e a tela explica o problema:

- **Etapa 1 (arquivo):** colunas de prioridade ausentes, `Nome do matriculado`/`Nome do curso` vazios, respostas que não casaram com nenhum módulo (com contagem por texto) e quantos alunos ficaram sem trilha ou com menos de 3 módulos. Um expander lista as **colunas reconhecidas** (`chave ← cabeçalho`), que é o que revela na hora um export em formato novo.
- **Etapa 2 (aluno):** bloqueios e avisos do aluno selecionado; o download só habilita se o plano puder sair correto.
- **Convenção:** vermelho = não dá para gerar; amarelo = gera, mas confira. Divergência de redação é amarelo (o plano sai mais curto); aluno sem nenhum módulo é vermelho.
- Quando a redação diverge, a mensagem já diz o conserto: acrescentar o texto novo em `variantes`, em `core/mapeamento.py`.

## 📄 Briefing de expansão para o GPC — 2026-08-19

`docs/briefing_expansao_GPC.md` + `docs/modelos/modelo_matriz_dores_GPC.csv`: o que a área do GPC (Gestão da Pecuária de Corte) precisa entregar para a ferramenta atender o curso — matriz dor→módulo, texto da pesquisa, CSV de teste, textos fixos e gabaritos de validação.

---

### Histórico anterior — Último marco: **Reestilização da UI do app (2 telas no design Rehagro) em 2026-06-26.**

## ✂️ Removido o "Gerar PDF" do servidor — 2026-06-26

O botão "Gerar PDF do plano" (Playwright/Chromium) foi **removido**: no Streamlit Cloud o Chromium não existe, então ele sempre caía no fallback (confuso). Agora o fluxo é só **Baixar plano (HTML) → Ctrl+P → Salvar como PDF**, com uma caixa de orientação passo a passo na etapa 3. O botão de download virou a ação primária (verde). `playwright` foi tirado do `requirements.txt` (deploy mais leve). `core/render_plano.py` mantém só o `render_html`; `gerar_pdf`/`pdf_disponivel` seguem no arquivo (sem uso, degradam sem playwright).

## 🖥️ Redesign da UI do app — 2026-06-26 (handoff design_handoff_gerador_ui)

As 2 telas do app (login + gerador) foram reestilizadas na identidade do plano (verde-floresta/dourado, Poppins/Mulish), mantendo toda a lógica de CSV/PDF.

- `.streamlit/config.toml`: tema forest `#0F4630` / cream `#F2EEE4`.
- `core/styles.py`: reescrito — `BRAND_CSS` (CSS de marca p/ widgets nativos via data-testid) + helpers `masthead_html`, `step_html`, `card_prioridade_html`. Fontes via `@import` Google.
- `app.py`: 2 telas — **login** (masthead + form card branco + botão dourado; o `<form>` é o card e o submit dourado é estilizado via `div[data-testid="stForm"] button`) e **gerador** (masthead band com logo + 3 etapas numeradas: upload CSV, seleção do aluno com 3 cards de prioridade, gerar PDF/baixar HTML/pré-visualizar).
- Validado com screenshots (Playwright) das 2 telas vs. protótipo — fiel.
- Botão dourado: evitamos o hack do wrapper `.gold-btn` (não embrulha o widget de forma confiável); usamos o escopo do form (único form do app).

---

### Histórico anterior — Último marco: **Redesign profissional: saída agora é PDF (HTML/Jinja2/Chromium) em 2026-06-26.**

## 🎨 Redesign para PDF (handoff de design) — 2026-06-26

Depois de migrar para o fluxo HubSpot → .docx (ver seção abaixo), o `.docx` foi **aposentado** em favor de um design profissional hi-fi (handoff feito no Canva, entregue em `design_handoff_plano_de_aula/`).

**Decisões (confirmadas com o usuário):**
- Saída passa a ser **PDF** (substitui o link do .docx no AVA/e-mail). `.docx` descontinuado.
- Render: **dados → HTML (Jinja2) → PDF (Chromium headless via Playwright)**. WeasyPrint NÃO serve (sem flex/grid).
- Como o app roda no **Streamlit Cloud** (vários CS) e Chromium lá é arriscado: **tentar PDF no servidor, com fallback** para o CS baixar o HTML e salvar como PDF no navegador (CSS A4 já pronto).
- Plano **auto-gerado é final** (sem passo de edição manual).
- Fontes **Poppins + Mulish** (Google Fonts, livres) → fim do impasse Myriad/licença. Trabalho de embedding .docx (`font_embed.py`) foi descartado.

**Arquivos:**
- Novos: `templates/plano_de_aula.html.j2`, `core/dados_plano.py`, `core/render_plano.py`, `assets/rehagro-logo-white.png` / `rehagro-logo-color.png`.
- Removidos: `core/gerador_plano.py`, `core/font_embed.py` (.docx).
- `requirements.txt`: troca python-docx/pandas por `jinja2` + `playwright`.

**Validado:** CSV real → 3 módulos casados → PDF pixel-perfect ao protótipo (hero, badges, painéis de materiais, encerramento). Chromium OK em local.

**Ajuste v2 (2026-06-26):** o handoff foi recalibrado (espaçamentos/fontes compactos) para o PDF caber em **2 páginas A4** (antes 3). Só o template (`templates/plano_de_aula.html.j2`) e a pasta de referência mudaram — dados/contrato/código de render iguais. Quebra: pág.1 = capa+intro+boas-vindas+módulo 1; pág.2 = módulos 2 e 3 + encerramento. Meta de 2 páginas vale p/ ~3 módulos; com muitos módulos pode passar (aceitável).

---

### Histórico anterior — Último marco: **Reestruturação para fluxo HubSpot → .docx em 2026-06-26.**

## 🔄 Reestruturação 2026-06-26 (mudança de uso da ferramenta)

A pesquisa de início de curso saiu do formulário próprio e passou a ser feita no **HubSpot Survey**. A ferramenta deixou de coletar respostas e virou um **gerador**: recebe o CSV do HubSpot, casa as 3 prioridades com os módulos e gera o plano em `.docx`.

**O que mudou:**
- ❌ Removidos: formulário público, banco SQLite (`core/database.py`), Dashboard, Turmas e a pasta `pages/`.
- ✅ `app.py` virou página única: login CS → upload CSV → escolher aluno → revisar → baixar `.docx`.
- ✅ Novo `core/hubspot_csv.py`: desfaz o **duplo-encoding** do CSV (2 passadas) e mapeia colunas por palavra-chave.
- ✅ `core/mapeamento.py`: textos das 9 dores atualizados para o **`DOR DO ALUNO v2.docx`** + `match_dores()` (casamento por texto normalizado, porque as dores têm vírgula interna e não dá pra `split(",")`).
- ✅ Identidade visual nova: fonte **Myriad Pro**, verde `#015641`, dourado `#cdaf69`, verde secundário `#87a851`. Aplicada no `.docx` e na UI.

**Cuidado conhecido:** no HubSpot a pergunta das prioridades é multi-seleção, então a ordem do CSV é a ordem das opções, **não** o ranking de urgência do aluno. A trilha é montada na ordem em que aparece no CSV (sinalizado na tela). Se precisar ranquear, adicionar reordenação manual antes do download.

---

### Histórico anterior — Último marco: **Ajustes pós-lançamento (mobile, dores, plano de aula) em 2026-05-18.**

## ✅ O que está pronto

### Funcionalidades
- **Formulário público** (4 etapas): identificação com CPF auto-formatado, contexto produtivo, objetivos, 3 prioridades ranqueadas
- **Painel CS** (com senha): lista de respostas com filtros, revisão do plano, download `.docx`
- **Dashboard CS**: métricas, gráficos plotly com rótulos de dados
- **Gestão de Turmas**: CRUD completo, só 1 turma ativa por vez, gera link público parametrizado (`?turma=XXX`)

### Gerador de `.docx`
- Logo verde Rehagro no topo
- Hyperlinks reais (clicáveis) para os módulos no Instructure
- Estrutura: Boas-vindas → 1ª → 2ª → 3ª prioridade
- Texto de abertura e encerramento conforme briefing

### Identidade visual
- Verde Rehagro (`#1C3829`), dourado (`#C9A84C`), creme (`#F0EBE0`)
- Sidebar customizada, toggle dourado
- Header full-width com logo Rehagro

### Deploy
- Repo público: https://github.com/Rehagro/cs-rehagro
- Streamlit Cloud: deployado (URL a confirmar no painel)
- Senha CS via `st.secrets` (não vai pro código)

## ⚠️ Pendências críticas para uso em produção

### 1. Banco persistente
SQLite local é **efêmero** no Streamlit Cloud — toda reinicialização do app (deploy, sleep, manutenção) apaga tudo. Antes de coletar respostas reais, migrar para:
- **Supabase** (Postgres free tier, recomendado pela curva de aprendizado baixa)
- **Neon** (Postgres serverless free)
- **Google Sheets** (mais simples, mas limita gráficos complexos)

Arquivos afetados: `core/database.py` (todas as funções), `requirements.txt` (adicionar `psycopg2-binary` ou `supabase-py`).

### 2. Senha em produção ✅ resolvido em 2026-05-18
Configurada em **Streamlit Cloud → Settings → Secrets** como `CS_PASSWORD = "rehagro"`. Para trocar: editar lá + reboot manual do app (o Streamlit não recarrega secrets automaticamente sempre — em alguns casos exige reboot via "Manage app → Reboot app").

### 3. Link de "Boas-vindas" ✅ resolvido em 2026-05-18
`MODULO_BOASVINDAS["link"]` agora aponta para `https://rehagro.instructure.com/courses/2850` (extraído do `Plano de aula - Mensagem de envio.docx`), renderizado como hyperlink clicável no `.docx` gerado.

## 🚀 Ideias para próximas iterações

- **Edição manual do plano antes de baixar**: CS pode trocar/reordenar módulos sugeridos para um aluno específico
- **Envio automático**: integrar com e-mail (SendGrid/AWS SES) ou WhatsApp Business API para mandar o `.docx` direto pro aluno
- **Tela "Quem ainda não respondeu"**: cruzar lista de matriculados com respostas recebidas, pra CS dar follow-up
- **Personalização da mensagem**: usar campos `valeu_a_pena` e `meta_fazenda` no texto do `.docx` (citar nome da fazenda, meta declarada)
- **Multilíngue**: hoje só PT-BR, mas turmas internacionais podem precisar de EN/ES
- **Múltiplas turmas ativas simultâneas**: hoje só 1, mas pode crescer

## 🐛 Bugs conhecidos / cuidados

- **ImportError ao adicionar funções no `database.py`**: Streamlit cacheia o módulo. Solução: kill do processo, `rm -rf __pycache__ core/__pycache__ pages/__pycache__`, restart.
- **CSS do Streamlit muda entre versões**: o seletor do botão de expand da sidebar é específico da 1.57 (`stExpandSidebarButton`). Em upgrades, validar visualmente.
- **`pip` não está no PATH no Windows do usuário**: usar `python -m pip install ...`.

## 📚 Aprendizados de UX/mobile (2026-05-18)

### `st.selectbox` com texto longo NÃO funciona bem no mobile
O Streamlit usa BaseWeb (Uber) por baixo do `st.selectbox`. Características que aprendemos na marra:
1. **Trunca com `...`** quando o texto da opção não cabe na largura (típico em mobile).
2. **Virtualiza a lista do dropdown** com `position: absolute` e `top: Npx` baseado em altura fixa. Forçar `white-space: normal` via CSS faz cada `<li>` ficar com altura variável, mas o `top` continua fixo → **opções sobrepostas**.
3. **Forçar `position: relative` no `<ul role="listbox">` e `max-height: 60vh`** parece arrumar a sobreposição, mas **quebra o scroll de listas longas** (ex: select de Estado com 27 UFs vira "infinito" e sem como rolar).

**Conclusão prática:** quando as opções têm texto longo (ex: dores do aluno, com 80–150 caracteres), **trocar `st.selectbox` por `st.radio`**. O radio renderiza nativamente sem dropdown, mostra todas as opções inline com texto completo wrappado, e funciona em qualquer tela. Foi o que fizemos na etapa 4 do `pages/1_Formulario.py`.

**Quando manter selectbox:** quando as opções são curtas (UF, cargo, status etc.) — sem necessidade de wrap.

### Cache do Streamlit Cloud
- `Ctrl+Shift+R` no browser limpa cache do **navegador**, mas **não força** o servidor do Streamlit Cloud a recarregar o código. Após `git push`, o webhook pode demorar (já vimos 5–10 min) ou não disparar.
- **Solução robusta:** Manage app (no painel do app) → ⋮ → **Reboot app**. Aguardar "Running".
- Para testar mudanças no celular sem cache, **abrir em aba anônima** elimina cache local de uma vez.

## 🗂 Estrutura do projeto

```
cs_rehagro/
├── app.py                    # Entry point → redireciona pro formulário
├── config.py                 # Config + lê CS_PASSWORD do secrets
├── requirements.txt
├── README.md
├── PROGRESSO.md              # Este arquivo
├── .gitignore
├── .streamlit/
│   ├── config.toml           # Tema Rehagro
│   ├── secrets.toml          # GITIGNORED — senha CS
│   └── secrets.toml.example  # Template público
├── assets/
│   ├── logo_rehagro.png
│   ├── logo_rehagro_branca.png    # header do app
│   └── logo_rehagro_verde.png     # .docx gerado
├── core/
│   ├── database.py           # SQLite (respostas + turmas)
│   ├── mapeamento.py         # Dor → Módulo + URL Instructure
│   ├── gerador_plano.py      # python-docx com hyperlinks
│   └── styles.py             # CSS Rehagro
└── pages/
    ├── 1_Formulario.py       # público
    ├── 2_Plano_de_Aula.py    # CS
    ├── 3_Dashboard.py        # CS
    └── 4_Turmas.py           # CS
```

## 🔧 Rodar localmente

```powershell
cd "C:\Users\rasaf\Desktop\CS\CS\Projeto - Plano de Aula\cs_rehagro\cs_rehagro"
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Depois acessa http://localhost:8501.

**Importante**: o `.streamlit/secrets.toml` local já tem a senha. Em produção, configurar em **Streamlit Cloud → Settings → Secrets**.

## 📝 Histórico (resumo)

| Data | Marco |
|---|---|
| 2026-05-15 | Pesquisa inicial dos arquivos do briefing → descoberta que o app já estava 100% implementado em prévia do Claude.ai |
| 2026-05-15 | Ciclo grande de ajustes visuais: logo branca chapada, header full-width, sidebar funcional, CPF auto-formatado, gráficos com rótulos |
| 2026-05-15 | Criada página de gestão de turmas (4ª página) + banco de turmas |
| 2026-05-15 | URLs reais do Instructure inseridas no mapeamento, hyperlinks clicáveis no .docx |
| 2026-05-15 | Logo verde Rehagro embutida no `.docx` gerado |
| 2026-05-15 | Primeiro commit + push pro GitHub Rehagro/cs-rehagro |
| 2026-05-15 | Deploy no Streamlit Cloud (faltou configurar secrets no primeiro deploy) |
| 2026-05-18 | `CS_PASSWORD` configurado em Secrets (`rehagro`); reboot do app necessário pra propagar |
| 2026-05-18 | Confirmado que reboot do app no Cloud apaga o SQLite — 1 rodada de respostas perdida; mitigação postergada (Supabase free esgotado, considerar Turso/Neon) |
| 2026-05-18 | 4 dores atualizadas no `mapeamento.py` conforme novo `DOR DO ALUNO.docx` |
| 2026-05-18 | Plano de aula `.docx` alinhado ao `Plano de aula - arquivo 2.docx`: subtítulo "Materiais de aula:", labels "Tempo de aula gravada aproximado", "Atividades para realizar", "Programação: Se programe para assistir esse conteúdo em..." |
| 2026-05-18 | Link real do módulo Boas-vindas (`/courses/2850`) adicionado em `MODULO_BOASVINDAS` |
| 2026-05-18 | Texto de orientação das prioridades reescrito conforme briefing CS |
| 2026-05-18 | **Mobile fix:** trocados os 3 `st.selectbox` da etapa 4 por `st.radio` — selectbox do BaseWeb não tinha solução CSS robusta pra wrap de opção longa sem quebrar virtualização (ver seção Aprendizados) |
