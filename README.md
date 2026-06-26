# CS Rehagro — Gerador de Plano de Aula (HubSpot → PDF)

Aplicação Streamlit interna do time de Customer Success da Rehagro (curso GPL — Gestão na Pecuária Leiteira).

A pesquisa de início de curso é feita no **HubSpot Survey**. Esta ferramenta recebe o **CSV exportado do HubSpot**, lê as 3 prioridades escolhidas pelo aluno e gera um **plano de aula personalizado** no design profissional Rehagro (HTML → PDF), com links diretos para os módulos no Instructure.

## Fluxo (uso interno CS)

1. **Login** com a senha do time CS.
2. **Upload** do CSV exportado do HubSpot Survey.
3. **Seleção** do aluno (o CSV pode trazer a turma inteira).
4. **Geração** do plano no design Rehagro:
   - **PDF automático** (Chromium headless) quando disponível;
   - **Fallback:** download do HTML — o CS abre e salva como PDF pelo navegador (`Ctrl+P`, layout A4 já configurado).

O plano em PDF substitui o antigo `.docx` — vai direto pro aluno (link/anexo no AVA/e-mail).

## Design / identidade

- Layout hi-fi vindo do handoff de design (`design_handoff_plano_de_aula/`).
- Fontes **Poppins** (títulos) + **Mulish** (corpo) — Google Fonts, livres (OFL).
- Paleta: verde floresta `#0F4630`, verde Rehagro `#1E7A45`, dourado `#C49A45` / `#E0C06A`.
- Render fiel a flexbox/grid/gradientes via Chromium (NÃO usar WeasyPrint — quebra o layout).

## Rodar localmente

```bash
pip install -r requirements.txt
playwright install chromium      # necessário para o PDF automático
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

> **PDF no Cloud:** o build padrão do Streamlit Cloud **não roda** `playwright install chromium`, então a geração automática de PDF tende a ficar indisponível lá — nesse caso o app cai automaticamente no **fluxo de fallback** (baixar HTML e salvar como PDF pelo navegador). Para tentar habilitar PDF no servidor, seria preciso disponibilizar o Chromium no ambiente (ex.: `packages.txt` + estratégia de instalação do browser).

## Estrutura

```
.
├── app.py                       # Login → upload CSV → escolher aluno → gerar PDF/HTML
├── config.py                    # Senha CS + paleta
├── requirements.txt
├── templates/
│   └── plano_de_aula.html.j2    # Template do plano (design hi-fi, Jinja2)
├── assets/                      # Logos (rehagro-logo-white.png, etc.)
├── core/
│   ├── hubspot_csv.py           # Parser do CSV do HubSpot (desfaz duplo-encoding) + casamento das dores
│   ├── mapeamento.py            # Dor → Módulo + URL Instructure + matcher por texto
│   ├── dados_plano.py           # registro CSV → contrato de dados do template
│   ├── render_plano.py          # Jinja2 → HTML → PDF (Playwright, com fallback)
│   └── styles.py                # CSS da UI Streamlit
└── design_handoff_plano_de_aula/  # Pacote de design (referência): protótipo, tokens, assets
```

## Notas sobre o CSV do HubSpot

- O export costuma vir **duplo-encodado** (linha inteira entre aspas, aspas internas duplicadas). O parser detecta e desfaz isso em 2 passadas.
- O campo das 3 prioridades junta as opções por vírgula, mas **algumas dores têm vírgula interna** → o casamento é por **texto normalizado**, não por `split(",")`.
- A ordem dos módulos no plano segue a ordem do CSV (no HubSpot a pergunta é multi-seleção, não ranqueada). Se o texto das opções mudar, atualize `core/mapeamento.py`.
