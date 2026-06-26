# Handoff: Gerador de Plano de Aula (UI) — Rehagro

## Visão geral
Reestilização da **ferramenta interna do time de Customer Success** que gera os planos de
aula dos alunos. São **duas telas** — login e gerador — agora alinhadas à identidade visual
do documento de Plano de Aula (verde-floresta + dourado, Poppins/Mulish, cards modernos).

A ferramenta é um app **Streamlit (Python)**. Este pacote mostra como aplicar o design
Rehagro sobre os componentes do Streamlit, mantendo a lógica de CSV/geração de PDF já
existente.

> **Relação com o outro handoff:** o documento gerado por esta ferramenta é especificado
> em `design_handoff_plano_de_aula/` (template Jinja2 + `render.py`). Reutilize aquele
> template para o botão "Gerar PDF" e o "Pré-visualizar".

---

## Sobre os arquivos deste pacote
Os arquivos são **referências de design** — recrie no app Streamlit real usando os padrões
do seu código. Conteúdo:

| Caminho | O que é |
|---|---|
| `reference/Gerador UI.dc.html` | Protótipo visual das 2 telas (abra no navegador — modo canvas, role/zoom para ver ambas). |
| `streamlit/.streamlit/config.toml` | Tema base do Streamlit (cores/fontes da marca). |
| `streamlit/styles.css` | CSS de marca para injetar no app (estiliza widgets nativos + classes utilitárias). |
| `streamlit/app_example.py` | App de referência: estrutura das 2 telas e como renderizar cada bloco. |
| `assets/rehagro-logo-white.png` | Logo branco (faixa verde). |
| `assets/rehagro-logo.png` | Logo colorido (fundo claro). |

---

## Fidelidade
**Alta fidelidade (hi-fi).** Cores, tipografia, espaçamentos e raios são finais. Valores
exatos em **Design Tokens**. Onde o Streamlit não permitir controle fino, prefira desenhar
o bloco em **HTML via `st.markdown(..., unsafe_allow_html=True)`** (ver `app_example.py`).

---

## Estratégia de implementação no Streamlit (importante)
O Streamlit gera nomes de classe instáveis e tem widgets de aparência fixa. Combine 3 camadas:

1. **Tema** (`.streamlit/config.toml`): define `primaryColor`, `backgroundColor`,
   `secondaryBackgroundColor`, `textColor`. Resolve 70% da base. (As fontes Poppins/Mulish
   **não** entram pelo tema — vêm via `@import` no `styles.css`.)
2. **CSS injetado** (`styles.css`): refina os widgets **nativos** (input, selectbox,
   file_uploader, button, expander, alert) por `data-testid` (seletores estáveis) e a barra
   superior (`header[data-testid="stHeader"]`).
3. **HTML puro via `st.markdown`** para os blocos "ricos" que o Streamlit não desenha:
   **masthead**, **cards de prioridade**, **títulos de etapa (1/2/3)** e, se quiser, o banner
   de sucesso. Helpers prontos no `app_example.py` (`masthead()`, `step()`, `card_prioridade()`).

**Limitações conhecidas / dicas:**
- Botão dourado (login "Entrar"): o Streamlit só tem `primary`/`secondary`. Envolva o botão
  em `<div class="gold-btn">…</div>` e estilize via CSS (já incluso), ou use um
  `st.form_submit_button` com a mesma classe wrapper.
- Para o **botão de download** use `st.download_button` (o "Baixar HTML"); para **gerar PDF**
  use `st.button` + Playwright/Chromium (ver `render.py` do outro handoff).
- A **pré-visualização** usa `st.components.v1.html(render_html(aluno), height=900)`.
- Esconder chrome do Streamlit: `footer{visibility:hidden}` (no CSS) e, se quiser ocultar o
  menu/"Manage app" para o CS, rode com `--client.toolbarMode=minimal`.
- Centralizar a coluna de login: `st.columns([1,2,1])` e use a do meio.

---

## Telas / Views

### Tela 1 — Login
- **Layout:** barra verde superior (60px) + coluna central (~520px) com respiro vertical.
- **Masthead card:** retângulo `border-radius:16px`, `border-bottom:3px solid #C49A45`,
  fundo `linear-gradient(135deg,#0F4630,#0A2C1E)`, `padding:30px 34px 28px`, centralizado.
  Anel dourado decorativo no canto. Eyebrow "REHAGRO · CUSTOMER SUCCESS" (`#E0C06A`, Poppins
  11px, `letter-spacing:.22em`) + título "Gerador de Plano de Aula" (Poppins 700, ~25px, `#fff`).
- **Form card:** branco, `border:1px #E7E1D3`, `border-radius:16px`, `padding:28px 30px`.
  - Label "Senha de acesso" (Poppins 12px 600, `#5A6B61`).
  - Campo de senha: altura 46px, `border:1.5px #E2DED1`, `border-radius:11px`, fundo `#FBFAF6`,
    ícone de cadeado à esquerda; placeholder itálico "Digite a senha do time CS". Botão "olho"
    (toggle) 46×46 quadrado ao lado.
  - **Botão "Entrar →":** full-width, altura 48px, gradiente dourado
    `linear-gradient(135deg,#E6C977,#C49A45)`, texto `#0F4630` (Poppins 600), seta. Sombra
    `0 4px 12px rgba(196,154,69,.3)`.
  - Nota: "🔒 Acesso restrito à equipe de Customer Success." (12.5px, `#8A8270`).
- **Estados:** senha incorreta → `st.error`. Sucesso → `st.session_state["auth"]=True; st.rerun()`.

### Tela 2 — Gerador
- **Barra superior** verde (60px) + **masthead band** (mesma faixa, agora full-width do
  conteúdo, com a subdescrição "Suba o CSV do HubSpot, escolha o aluno e gere o plano no
  design Rehagro." e o **logo branco** à direita).
- Conteúdo em **3 etapas numeradas** (badge circular com borda dourada + label uppercase):

  **Etapa 1 — Arquivo CSV exportado do HubSpot Survey** (com ícone de ajuda "?" à direita)
  - Card de arquivo carregado: tile verde (`#0F4630`) com ícone de CSV (traço dourado),
    nome do arquivo (Poppins 600, `#0F4630`) + tamanho/estado (`#8A8270`), botão "×" remover
    (vermelho suave), divisor, botão "＋ Trocar arquivo" (tracejado).
  - **Banner de sucesso:** fundo `#E7F1E8`, borda `#C3E0C8`, `border-radius:12px`, check em
    círculo verde (`#1E7A45`) + "N aluno(s) carregado(s) do CSV." (`#0F4630`, 600).

  **Etapa 2 — Selecione o aluno**
  - **Dropdown:** branco, `border:1.5px #E2DED1`, `border-radius:11px`, avatar circular com
    iniciais (gradiente dourado) + "**Nome** · Curso" + chevron.
  - **3 cards de prioridade** (grid 1fr 1fr 1fr, `gap:14px`): badge circular dourado com o
    número, pílula "Nª PRIORIDADE" (`#9A7626` sobre `#FBF3DE`), título do módulo (Poppins 600
    15px `#0F4630`), e rodapé com métricas "N aulas · ~Xh" (ícones de vídeo/relógio dourados,
    separados por `border-top:1px #F0EBDE`).

  **Etapa 3 — Gere e envie o plano**
  - **Botão primário** "📄 Gerar PDF do plano": verde `#0F4630`, branco, altura 52px,
    `border-radius:12px`, sombra `0 6px 16px rgba(15,70,48,.22)`, ~1.6× de largura.
  - **Botão secundário** "⬇ Baixar HTML (salvar como PDF)": branco, `border:1.5px #C9C2B0`,
    texto `#0F4630`.
  - **Linha "Pré-visualizar o plano":** card branco com chevron + ícone de olho + label
    (expander que abre a pré-visualização HTML do plano).

---

## Design Tokens (idênticos ao documento de Plano de Aula)

### Cores
| Token | Hex | Uso |
|---|---|---|
| Verde floresta | `#0F4630` | Títulos, botão primário, masthead, tile de arquivo |
| Verde escuro 2 | `#0A2C1E` | Parada final do gradiente do masthead |
| Verde da barra | `#0B3B2B` → `#0E4632` | Barra superior |
| Verde Rehagro | `#1E7A45` | Check de sucesso, ícones de ação positiva |
| Dourado | `#C49A45` | Underline, badges, métricas, foco de input |
| Dourado claro | `#E0C06A` / `#E6C977` | Eyebrow, topo dos gradientes dourados |
| Dourado texto | `#9A7626` | Texto das pílulas/etapas |
| Creme (fundo) | `#F2EEE4` | Fundo da página |
| Branco | `#FFFFFF` | Cards, inputs |
| Tinta | `#1B2B22` | Texto base |
| Muted | `#5A6B61` | Labels |
| Muted 2 | `#8A8270` | Texto auxiliar/placeholder |
| Linha | `#E7E1D3` / `#E2DED1` / `#F0EBDE` | Bordas de card / input / divisória interna |
| Creme pílula | `#FBF3DE` | Fundo das pílulas de prioridade |
| Sucesso | bg `#E7F1E8` · borda `#C3E0C8` | Banner "aluno carregado" |
| Input bg | `#FBFAF6` | Fundo de campos de texto |

### Tipografia
- **Títulos/labels:** `Poppins` (500/600/700). **Corpo:** `Mulish` (400–700).
- Import: `https://fonts.googleapis.com/css2?family=Poppins:wght@500;600;700&family=Mulish:wght@400;500;600;700&display=swap`
- Masthead título 25–26px/700; títulos de card 15px/600; labels de etapa 12px/600 uppercase
  `letter-spacing:.1em`; corpo/inputs 14px; auxiliares 12.5px.

### Raios / sombras
- Raios: barra 0 · masthead/cards 14–16px · inputs/botões 11–12px · pílulas/avatares 999px.
- Sombras: card de tela `0 8px 30px rgba(0,0,0,.12)`; botão primário
  `0 6px 16px rgba(15,70,48,.22)`; botão dourado `0 4px 12px rgba(196,154,69,.3)`;
  cards internos `0 2px 8px rgba(15,70,48,.04)`.

### Espaçamento
Barra 60px · masthead `padding:24px 30px` · conteúdo `padding:26px 28px` ·
gap dos cards de prioridade 14px · divisórias entre etapas `margin:24px 0`.

---

## Ícones
SVG inline traço (estilo Lucide/Feather), 24×24 viewBox. Usados: cadeado (senha), olho
(toggle/preview), seta (entrar), arquivo/CSV, "＋" (trocar), "×" (remover), check (sucesso),
chevron-down (dropdown), vídeo + relógio (métricas), documento (gerar PDF), download (baixar),
chevron-right + "?" (ajuda). Reaproveite os SVGs do `reference/Gerador UI.dc.html`.

---

## Arquivos de referência
- Protótipo: `reference/Gerador UI.dc.html`
- Tema: `streamlit/.streamlit/config.toml`
- CSS de marca: `streamlit/styles.css`
- App de referência: `streamlit/app_example.py`
- Documento gerado (template/PDF): ver o pacote `design_handoff_plano_de_aula/`.
