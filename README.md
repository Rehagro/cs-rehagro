# CS Rehagro — Gerador de Plano de Aula (HubSpot → PDF)

Aplicação Streamlit interna do time de Customer Success da Rehagro (curso GPL — Gestão na Pecuária Leiteira).

A pesquisa de início de curso é feita no **HubSpot Survey**. Esta ferramenta recebe o **CSV exportado do HubSpot**, lê as 3 prioridades escolhidas pelo aluno e gera um **plano de aula personalizado** no design profissional Rehagro, com links diretos para os módulos no Instructure.

## Fluxo (uso interno CS)

1. **Login** com a senha do time CS.
2. **Upload** do CSV exportado do HubSpot Survey.
3. **Seleção** do aluno (o CSV pode trazer a turma inteira).
4. **Baixar o plano** (arquivo HTML, design Rehagro) → o CS abre e salva como PDF pelo navegador (`Ctrl + P → Salvar como PDF`; o layout A4 já está pronto).

> O HTML é **self-contained** (fontes e logo embutidos) e o PDF gerado pelo navegador sai idêntico ao design. Esse PDF substitui o antigo `.docx` — vai direto pro aluno (link/anexo no AVA/e-mail). Há um **Pré-visualizar** na própria tela.

## Design / identidade

- Layout hi-fi vindo do handoff de design (`design_handoff_plano_de_aula/`); UI do app em `design_handoff_gerador_ui/`.
- Fontes **Poppins** (títulos) + **Mulish** (corpo) — Google Fonts, livres (OFL), embutidas no documento.
- Paleta: verde floresta `#0F4630`, verde Rehagro `#1E7A45`, dourado `#C49A45` / `#E0C06A`.

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

> O app **não gera PDF no servidor** (não depende de Chromium/Playwright). Ele entrega o **HTML** do plano e o CS salva como PDF pelo navegador (`Ctrl + P → Salvar como PDF`). Isso mantém o deploy leve e funciona em qualquer ambiente.

## Estrutura

```
.
├── app.py                       # 2 telas: login → (upload CSV → escolher aluno → baixar plano)
├── config.py                    # Senha CS + paleta
├── requirements.txt
├── templates/
│   └── plano_de_aula.html.j2    # Template do plano (design hi-fi, Jinja2)
├── assets/                      # Logos + fontes (Poppins/Mulish, OFL)
├── core/
│   ├── hubspot_csv.py           # Parser do CSV do HubSpot (desfaz duplo-encoding) + casamento das dores
│   ├── mapeamento.py            # Dor → Módulo + URL Instructure + matcher por texto
│   ├── dados_plano.py           # registro CSV → contrato de dados do template
│   ├── render_plano.py          # Jinja2 → HTML (fontes/logo embutidos)
│   └── styles.py                # CSS de marca da UI Streamlit + helpers das telas
├── design_handoff_plano_de_aula/  # Pacote de design do PDF (referência)
└── design_handoff_gerador_ui/     # Pacote de design da UI do app (referência)
```

## Notas sobre o CSV do HubSpot

- O export costuma vir **duplo-encodado** (linha inteira entre aspas, aspas internas duplicadas). O parser detecta e desfaz isso em 2 passadas.
- O campo das 3 prioridades junta as opções por vírgula, mas **algumas dores têm vírgula interna** → o casamento é por **texto normalizado**, não por `split(",")`.
- A ordem dos módulos no plano segue a ordem do CSV (no HubSpot a pergunta é multi-seleção, não ranqueada). Se o texto das opções mudar, atualize `core/mapeamento.py`.
