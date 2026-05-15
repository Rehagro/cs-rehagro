# CS Rehagro — Pesquisa de Início de Jornada + Plano de Aula

Aplicação Streamlit para o time de Customer Success da Rehagro (curso GPL — Gestão na Pecuária Leiteira). Coleta respostas dos alunos via formulário público e gera planos de aula personalizados em `.docx` com links diretos para os módulos do Instructure.

## Páginas

- **Formulário** (público) — aluno responde 4 blocos: identificação, contexto produtivo, objetivos e 3 prioridades.
- **Plano de Aula** (CS) — lista respostas, revisa e baixa o `.docx` personalizado.
- **Dashboard** (CS) — métricas e gráficos da turma.
- **Turmas** (CS) — cria, edita, ativa turmas e gera o link público do formulário.

## Rodar localmente

```bash
pip install -r requirements.txt
```

Crie `.streamlit/secrets.toml` (use `.streamlit/secrets.toml.example` como base):

```toml
CS_PASSWORD = "sua-senha-aqui"
```

Inicie:

```bash
streamlit run app.py
```

## Deploy no Streamlit Cloud

1. Conecte o repo em [share.streamlit.io](https://share.streamlit.io)
2. Entrypoint: `app.py`
3. Em **Settings → Secrets**, cole:
   ```toml
   CS_PASSWORD = "sua-senha-aqui"
   ```

## Estrutura

```
.
├── app.py                       # Entry point (redireciona ao formulário)
├── config.py                    # Configurações globais
├── requirements.txt
├── .streamlit/
│   ├── config.toml              # Tema visual
│   └── secrets.toml             # Senha CS (gitignored)
├── assets/                      # Logos
├── core/
│   ├── database.py              # SQLite (respostas + turmas)
│   ├── mapeamento.py            # Dor → Módulo + URL Instructure
│   ├── gerador_plano.py         # Geração do .docx
│   └── styles.py                # CSS Rehagro
└── pages/
    ├── 1_Formulario.py
    ├── 2_Plano_de_Aula.py
    ├── 3_Dashboard.py
    └── 4_Turmas.py
```

## Notas

- O banco SQLite (`data/respostas.db`) é local e gitignored. Em Streamlit Cloud o storage é efêmero — considere migrar para Postgres/Supabase antes de uso em produção.
- A senha CS fica em `secrets.toml` (não commitado). Em produção, configure pelo painel do Streamlit Cloud.
