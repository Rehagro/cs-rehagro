# CS Rehagro — Gerador de Plano de Aula (HubSpot → .docx)

Aplicação Streamlit interna do time de Customer Success da Rehagro (curso GPL — Gestão na Pecuária Leiteira).

A pesquisa de início de curso passou a ser feita no **HubSpot Survey**. Esta ferramenta recebe o **CSV exportado do HubSpot**, lê as 3 prioridades escolhidas pelo aluno (pergunta *"escolha os 3 pontos mais importantes…"*) e gera um **plano de aula personalizado em `.docx`** com a identidade visual Rehagro e links diretos para os módulos no Instructure.

## Fluxo (uso interno CS)

1. **Login** com a senha do time CS.
2. **Upload** do CSV exportado do HubSpot Survey.
3. **Seleção** do aluno (o CSV pode trazer a turma inteira).
4. **Revisão** da trilha (3 dores → 3 módulos) e dos dados do aluno.
5. **Download** do plano em `.docx` (o CS valida e converte para PDF depois).

## Identidade visual

- Fonte **Myriad Pro** (com fallback Segoe UI/Arial)
- Verde `#015641` · Dourado `#cdaf69` · Verde secundário `#87a851`
- Logo Rehagro (verde) embutida no `.docx`

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
3. Em **Settings → Secrets**, defina `CS_PASSWORD`.

## Estrutura

```
.
├── app.py                       # App de página única: login → upload CSV → escolher aluno → baixar .docx
├── config.py                    # Senha CS + paleta/identidade
├── requirements.txt
├── .streamlit/
│   ├── config.toml              # Tema visual
│   └── secrets.toml             # Senha CS (gitignored)
├── assets/                      # Logos
└── core/
    ├── hubspot_csv.py           # Parser do CSV do HubSpot (desfaz duplo-encoding) + casamento das dores
    ├── mapeamento.py            # Dor → Módulo + URL Instructure + matcher por texto
    ├── gerador_plano.py         # Geração do .docx (Myriad Pro + cores Rehagro)
    └── styles.py                # CSS Rehagro
```

## Notas sobre o CSV do HubSpot

- O export costuma vir **duplo-encodado** (linha inteira entre aspas, aspas internas duplicadas). O parser detecta e desfaz isso em 2 passadas.
- O campo das 3 prioridades junta as opções por vírgula, mas **algumas dores têm vírgula interna** → o casamento é por **texto normalizado** (sem acento/pontuação), não por `split(",")`.
- Se o texto das opções mudar no HubSpot, atualize os textos em `core/mapeamento.py` (`DORES[*]["dor"]`). Trechos não reconhecidos aparecem como aviso na tela.
