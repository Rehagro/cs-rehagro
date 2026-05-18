"""CSS da identidade visual Rehagro — injetado em todas as páginas."""
import base64
import os

_BASE_DIR = os.path.dirname(os.path.dirname(__file__))
_LOGO_BRANCA = os.path.join(_BASE_DIR, "assets", "logo_rehagro_branca.png")


def _logo_base64() -> str:
    if not os.path.exists(_LOGO_BRANCA):
        return ""
    with open(_LOGO_BRANCA, "rb") as f:
        return base64.b64encode(f.read()).decode()


BASE_CSS = """
<style>
/* ── Reset Streamlit ───────────────────────────────── */
#MainMenu, footer { visibility: hidden; }
[data-testid="stDecoration"] { display: none; }
[data-testid="stStatusWidget"] { display: none; }
[data-testid="stMainMenu"] { display: none !important; }

/* Esconde APENAS o botão Deploy e ações extras — preserva o stExpandSidebarButton */
[data-testid="stToolbarActions"] { display: none !important; }
[data-testid="stAppDeployButton"] { display: none !important; }

/* Header do Streamlit (contém o botão de toggle da sidebar) — visível e acima do conteúdo */
header[data-testid="stHeader"] {
    background: #1C3829 !important;
    height: 3rem !important;
    z-index: 100 !important;
    border-bottom: 1px solid #2A4F3A !important;
}
header[data-testid="stHeader"] [data-testid="stToolbar"] {
    background: transparent !important;
    padding: 6px 12px !important;
}

.block-container {
    padding: 3rem 2.5rem 2rem 2.5rem !important;
    max-width: 100% !important;
}

/* Header REHAGRO expande além do padding do block-container */
.rh-header {
    margin-left: -2.5rem !important;
    margin-right: -2.5rem !important;
    width: calc(100% + 5rem) !important;
}
.stApp { background: #F0EBE0; }

/* Sidebar com identidade Rehagro */
section[data-testid="stSidebar"] {
    background: #1C3829 !important;
    border-right: 1px solid #2A4F3A !important;
}
section[data-testid="stSidebar"] * {
    color: #F0EBE0 !important;
}
section[data-testid="stSidebar"] a {
    color: #F0EBE0 !important;
    font-weight: 500 !important;
    border-radius: 6px !important;
    transition: background 0.15s !important;
}
section[data-testid="stSidebar"] a:hover {
    background: rgba(201,168,76,0.12) !important;
    color: #C9A84C !important;
}
/* Botão de toggle (abrir/fechar sidebar) — sempre visível */
button[data-testid="stSidebarCollapseButton"],
button[data-testid="stExpandSidebarButton"] {
    color: #C9A84C !important;
    background: #1C3829 !important;
    border: 1px solid #C9A84C !important;
    border-radius: 6px !important;
    visibility: visible !important;
    opacity: 1 !important;
    z-index: 999999 !important;
}
button[data-testid="stExpandSidebarButton"] {
    /* Garante que o botão de expandir fique visível e acessível no canto */
    width: 40px !important;
    height: 40px !important;
}
button[data-testid="stExpandSidebarButton"] svg,
button[data-testid="stSidebarCollapseButton"] svg,
button[data-testid="stExpandSidebarButton"] span,
button[data-testid="stSidebarCollapseButton"] span,
button[data-testid="stExpandSidebarButton"] *,
button[data-testid="stSidebarCollapseButton"] * {
    fill: #C9A84C !important;
    color: #C9A84C !important;
}
button[data-testid="stExpandSidebarButton"]:hover,
button[data-testid="stSidebarCollapseButton"]:hover {
    background: #2A4F3A !important;
}

/* ── Header Rehagro ────────────────────────────────── */
.rh-header {
    background: #1C3829 !important;
    padding: 24px 40px 22px !important;
    display: flex !important;
    justify-content: space-between !important;
    align-items: center !important;
    margin-bottom: 32px !important;
    width: 100% !important;
    box-sizing: border-box !important;
    border-bottom: 3px solid #C9A84C !important;
}
.rh-header-left {
    flex: 1;
}
.rh-header-tag {
    font-size: 11px !important;
    letter-spacing: 2.5px !important;
    color: #C9A84C !important;
    text-transform: uppercase !important;
    font-weight: 600 !important;
    margin-bottom: 6px !important;
}
.rh-header-title {
    font-size: 26px !important;
    font-weight: 800 !important;
    color: #C9A84C !important;
    text-transform: uppercase !important;
    letter-spacing: 1.5px !important;
    line-height: 1.1 !important;
    margin-bottom: 4px !important;
}
.rh-header-sub {
    font-size: 13px !important;
    color: #9FB8A8 !important;
    font-weight: 400 !important;
}
.rh-header-logo {
    height: 46px;
    width: auto;
    opacity: 1;
    margin-left: 24px;
}

/* ── Conteúdo ──────────────────────────────────────── */
.rh-content {
    padding: 0 48px 48px;
    max-width: 980px;
    margin: 0 auto;
}
.rh-section-tag {
    font-size: 12px;
    letter-spacing: 2.5px;
    text-transform: uppercase;
    color: #C9A84C;
    font-weight: 700;
    margin-bottom: 18px;
    padding-bottom: 10px;
    border-bottom: 1px solid #D8D3C8;
}
.rh-section-tag::before { content: "— "; }

/* Container central do formulário */
.rh-form-wrap {
    max-width: 760px;
    margin: 0 auto;
    padding: 0 24px;
}

/* ── Cards ─────────────────────────────────────────── */
.rh-card {
    background: #FFFFFF;
    border: 0.5px solid #D8D3C8;
    border-radius: 12px;
    border-top: 3px solid #C9A84C;
    padding: 24px 28px;
    margin-bottom: 16px;
}
.rh-card-num {
    width: 30px; height: 30px;
    border-radius: 50%;
    background: #1C3829;
    color: white;
    font-size: 13px;
    font-weight: 700;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 10px;
}
.rh-card-label {
    font-size: 15px;
    font-weight: 600;
    color: #1A1A1A;
    margin-bottom: 4px;
}
.rh-card-hint {
    font-size: 13px;
    color: #6B6B5E;
    margin-bottom: 10px;
}

/* ── Progress bar ──────────────────────────────────── */
.rh-progress-wrap {
    margin-bottom: 28px;
}
.rh-progress-label {
    font-size: 13px;
    color: #6B6B5E;
    margin-bottom: 8px;
    letter-spacing: 1px;
    text-transform: uppercase;
    font-weight: 600;
}
.rh-progress-bar {
    background: #D8D3C8;
    height: 5px;
    border-radius: 3px;
    overflow: hidden;
}
.rh-progress-fill {
    background: #C9A84C;
    height: 100%;
    border-radius: 3px;
    transition: width 0.4s ease;
}

/* ── Botões ────────────────────────────────────────── */
div.stButton > button,
div.stFormSubmitButton > button,
div.stDownloadButton > button {
    border-radius: 8px !important;
    font-size: 15px !important;
    font-weight: 600 !important;
    letter-spacing: 0.5px !important;
    height: 48px !important;
    padding: 0 28px !important;
    transition: all 0.2s !important;
}
div.stButton > button[kind="primary"],
div.stFormSubmitButton > button[kind="primary"],
div.stDownloadButton > button[kind="primary"] {
    background: #1C3829 !important;
    color: white !important;
    border: none !important;
}
div.stButton > button[kind="primary"]:hover,
div.stFormSubmitButton > button[kind="primary"]:hover {
    background: #2A4F3A !important;
}
div.stButton > button[kind="secondary"],
div.stFormSubmitButton > button[kind="secondary"] {
    background: transparent !important;
    color: #6B6B5E !important;
    border: 0.5px solid #D8D3C8 !important;
}

/* ── Inputs Streamlit (FONTE MAIOR) ────────────────── */
div[data-testid="stTextInput"] input,
div[data-testid="stNumberInput"] input,
div[data-testid="stSelectbox"] select,
div[data-testid="stTextArea"] textarea,
div[data-baseweb="select"] > div {
    border-radius: 8px !important;
    border: 0.5px solid #D8D3C8 !important;
    background: #FAFAF8 !important;
    font-size: 15px !important;
    min-height: 44px !important;
}

/* Selectbox: permitir quebra de linha para opções longas (dor do aluno).
   Sem isso, no mobile o texto fica cortado por "..." e o aluno não enxerga
   a opção inteira nem no campo selecionado nem no dropdown.
   O BaseWeb aplica text-overflow:ellipsis nos descendentes do <li>, então
   precisamos forçar override em todos os filhos também. */

/* Campo selecionado (controle fechado) */
div[data-baseweb="select"] > div,
div[data-baseweb="select"] > div > div,
div[data-baseweb="select"] [data-baseweb="tag"],
div[data-baseweb="select"] input {
    height: auto !important;
    min-height: 44px !important;
    white-space: normal !important;
    word-break: break-word !important;
    overflow: visible !important;
    text-overflow: clip !important;
    line-height: 1.35 !important;
    padding-top: 8px !important;
    padding-bottom: 8px !important;
}

/* Dropdown aberto (popover renderiza fora do form, no body) — atinge
   também TODOS os descendentes da option, porque é num <div> interno
   que o BaseWeb coloca o ellipsis. */
div[data-baseweb="popover"] li,
div[data-baseweb="popover"] li *,
ul[role="listbox"] li,
ul[role="listbox"] li *,
li[role="option"],
li[role="option"] *,
div[role="option"],
div[role="option"] * {
    white-space: normal !important;
    word-break: break-word !important;
    overflow: visible !important;
    text-overflow: clip !important;
    max-height: none !important;
    height: auto !important;
    line-height: 1.4 !important;
}

/* O BaseWeb virtualiza a lista: cada <li> fica com position:absolute e
   top:0/40/80px. Como agora cada opção tem altura variável (texto longo
   quebra em N linhas), o posicionamento fixo causa sobreposição. Forçar
   flow natural: ul ganha altura automática, items voltam a ser relativos. */
ul[role="listbox"],
div[data-baseweb="popover"] ul,
div[data-baseweb="menu"] ul {
    position: relative !important;
    height: auto !important;
    max-height: 60vh !important;
    overflow-y: auto !important;
}
ul[role="listbox"] li,
ul[role="listbox"] > div,
li[role="option"],
div[role="option"] {
    position: relative !important;
    top: auto !important;
    left: auto !important;
    transform: none !important;
    padding-top: 10px !important;
    padding-bottom: 10px !important;
}
div[data-testid="stTextInput"] input:focus,
div[data-testid="stSelectbox"] select:focus,
div[data-testid="stTextArea"] textarea:focus {
    border-color: #C9A84C !important;
    box-shadow: 0 0 0 2px rgba(201,168,76,0.15) !important;
}

/* Labels MAIS legíveis */
div[data-testid="stTextInput"] label,
div[data-testid="stSelectbox"] label,
div[data-testid="stNumberInput"] label,
div[data-testid="stTextArea"] label,
div[data-testid="stCheckbox"] label,
.stMarkdown p {
    font-size: 15px !important;
    color: #1A1A1A !important;
}
div[data-testid="stTextInput"] label,
div[data-testid="stSelectbox"] label,
div[data-testid="stNumberInput"] label,
div[data-testid="stTextArea"] label {
    font-weight: 600 !important;
}

/* Captions */
div[data-testid="stCaptionContainer"],
.stCaption {
    font-size: 13px !important;
    color: #6B6B5E !important;
}

/* Markdown geral (NÃO aplicar a divs do header — ele tem suas próprias cores) */
.stMarkdown p, .stMarkdown li {
    font-size: 15px;
    line-height: 1.6;
    color: #1A1A1A;
}

/* ── Alert / Success ───────────────────────────────── */
.rh-success {
    background: #EAF0EC;
    border: 0.5px solid #1C3829;
    border-left: 4px solid #C9A84C;
    border-radius: 8px;
    padding: 18px 22px;
    margin-bottom: 18px;
    font-size: 15px;
    color: #1C3829;
}
.rh-warning {
    background: #FBF6ED;
    border: 0.5px solid #D8D3C8;
    border-left: 4px solid #C9A84C;
    border-radius: 8px;
    padding: 18px 22px;
    margin-bottom: 18px;
    font-size: 15px;
    color: #6B6B5E;
}

/* ── Tela de agradecimento ─────────────────────────── */
.rh-thanks {
    text-align: center;
    padding: 80px 40px;
    max-width: 600px;
    margin: 0 auto;
}
.rh-thanks-icon {
    font-size: 56px;
    margin-bottom: 18px;
}
.rh-thanks-title {
    font-size: 28px;
    font-weight: 800;
    color: #1C3829;
    margin-bottom: 10px;
    text-transform: uppercase;
    letter-spacing: 1px;
}
.rh-thanks-sub {
    font-size: 16px;
    color: #6B6B5E;
    line-height: 1.7;
}

/* ── Responsivo mobile ─────────────────────────────── */
@media (max-width: 768px) {
    .rh-header {
        padding: 24px 20px 20px;
        flex-direction: column;
        align-items: flex-start;
        gap: 16px;
    }
    .rh-header-logo { margin-left: 0; height: 44px; }
    .rh-header-title { font-size: 22px; }
    .rh-content { padding: 0 20px 32px; }
    .rh-form-wrap { padding: 0 8px; }
}
</style>
"""


def header_html(titulo: str, subtitulo: str = "",
                tag: str = "Rehagro · Customer Success") -> str:
    logo_b64 = _logo_base64()
    logo_img = (
        f'<img class="rh-header-logo" src="data:image/png;base64,{logo_b64}" alt="Rehagro">'
        if logo_b64 else ""
    )
    return f"""
    <div class="rh-header">
        <div class="rh-header-left">
            <div class="rh-header-tag">{tag}</div>
            <div class="rh-header-title">{titulo}</div>
            {"<div class='rh-header-sub'>" + subtitulo + "</div>" if subtitulo else ""}
        </div>
        {logo_img}
    </div>
    """


def progress_html(pct: int, label: str = "") -> str:
    return f"""
    <div class="rh-progress-wrap">
        {"<div class='rh-progress-label'>" + label + "</div>" if label else ""}
        <div class="rh-progress-bar">
            <div class="rh-progress-fill" style="width:{pct}%"></div>
        </div>
    </div>
    """


def card_html(num: int | str, label: str, hint: str = "", content: str = "") -> str:
    return f"""
    <div class="rh-card">
        <div class="rh-card-num">{num}</div>
        <div class="rh-card-label">{label}</div>
        {"<div class='rh-card-hint'>" + hint + "</div>" if hint else ""}
        {content}
    </div>
    """


def section_tag_html(text: str) -> str:
    return f'<div class="rh-section-tag">{text}</div>'
