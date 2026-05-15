# Progresso e próximos passos — CS Rehagro

Último marco: **MVP deployado no Streamlit Cloud em 2026-05-15.**

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

### 2. Senha em produção
O usuário esqueceu de configurar `CS_PASSWORD` em Secrets no primeiro deploy. Verificar se já foi corrigido em **Streamlit Cloud → Settings → Secrets**:
```toml
CS_PASSWORD = "valor-aqui"
```

### 3. Link de "Boas-vindas"
Em `core/mapeamento.py:108`, `MODULO_BOASVINDAS["link"]` ainda é placeholder (`CL GPL T1 - Boas-vindas`). Precisa da URL real do Instructure pra virar hyperlink clicável.

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
