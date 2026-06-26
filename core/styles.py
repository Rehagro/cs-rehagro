"""
Rehagro · Gerador de Plano de Aula — CSS de marca + helpers de UI (Streamlit).

Estratégia (do handoff design_handoff_gerador_ui):
  1. Tema base em .streamlit/config.toml.
  2. CSS de marca injetado uma vez (BRAND_CSS) — refina widgets nativos por data-testid.
  3. Blocos "ricos" (masthead, etapas, cards de prioridade) desenhados em HTML
     puro via st.markdown, usando os helpers abaixo.
"""
import base64
import os

_ASSETS = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets")
_LOGO_WHITE = os.path.join(_ASSETS, "rehagro-logo-white.png")


def logo_white_data_uri() -> str:
    if not os.path.exists(_LOGO_WHITE):
        return ""
    with open(_LOGO_WHITE, "rb") as f:
        return f"data:image/png;base64,{base64.b64encode(f.read()).decode('ascii')}"


# Anel dourado decorativo (canto do masthead)
_RING = (
    '<svg viewBox="0 0 200 200" aria-hidden="true" style="position:absolute;'
    'top:-70px;right:-40px;width:190px;height:190px;opacity:.5;">'
    '<circle cx="100" cy="100" r="80" fill="none" stroke="#C49A45" stroke-width="2"></circle>'
    '<circle cx="100" cy="100" r="60" fill="none" stroke="#C49A45" stroke-width="1" opacity=".5"></circle>'
    '</svg>'
)


BRAND_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@500;600;700&family=Mulish:wght@400;500;600;700&display=swap');

:root{
  --forest:#0F4630; --forest2:#0A2C1E; --bar:#0B3B2B;
  --green:#1E7A45;  --gold:#C49A45;   --gold-2:#E6C977; --gold-soft:#FBF3DE;
  --cream:#F2EEE4;  --ink:#1B2B22;    --muted:#5A6B61;  --muted-2:#8A8270;
  --line:#E7E1D3;   --line-input:#E2DED1;
}

/* ---- base / fontes ---- */
html, body, [class*="css"]{ font-family:'Mulish', system-ui, sans-serif; color:var(--ink); }
.stApp{ background:var(--cream); }
h1,h2,h3,h4,h5{ font-family:'Poppins', sans-serif; }

/* esconder chrome do Streamlit */
#MainMenu, footer { visibility:hidden; }
[data-testid="stToolbarActions"],
[data-testid="stAppDeployButton"],
[data-testid="stMainMenu"],
[data-testid="stDecoration"],
[data-testid="stStatusWidget"] { display:none !important; }
section[data-testid="stSidebar"] { display:none; }

/* barra superior fina verde (substitui o header padrão do Streamlit) */
header[data-testid="stHeader"]{
  background:linear-gradient(90deg,var(--bar),#0E4632) !important;
  height:60px;
}

/* largura/respiro do conteúdo (padding-top folga a barra verde de 60px) */
.block-container{ max-width:1120px; padding-top:80px !important; padding-bottom:48px !important; }

/* ---- TÍTULOS DE ETAPA (.step via st.markdown) ---- */
.step{ display:flex; align-items:center; gap:11px; margin:0 0 13px; }
.step .n{ width:24px; height:24px; border-radius:50%; border:1.5px solid var(--gold);
  color:#9A7626; font-family:'Poppins'; font-weight:700; font-size:12px;
  display:flex; align-items:center; justify-content:center; flex:none; }
.step .t{ font-family:'Poppins'; font-size:12px; font-weight:600; letter-spacing:.1em;
  text-transform:uppercase; color:var(--muted); }

/* ---- INPUT DE TEXTO / SENHA ---- */
[data-testid="stTextInput"] input{
  height:46px; border:1.5px solid var(--line-input) !important; border-radius:11px !important;
  background:#FBFAF6 !important; font-size:14px;
}
[data-testid="stTextInput"] input:focus{ border-color:var(--gold) !important;
  box-shadow:0 0 0 3px rgba(196,154,69,.18) !important; }
[data-testid="stTextInput"] label, [data-testid="stSelectbox"] label{
  font-family:'Poppins'; font-weight:600; font-size:12.5px; color:var(--muted) !important;
}

/* ---- SELECTBOX (selecione o aluno) ---- */
[data-testid="stSelectbox"] div[data-baseweb="select"] > div{
  border:1.5px solid var(--line-input) !important; border-radius:11px !important;
  background:#fff !important; min-height:48px; padding:4px 6px;
}

/* ---- FILE UPLOADER ---- */
[data-testid="stFileUploader"] section{
  border:1.5px dashed #C9C2B0 !important; border-radius:14px !important;
  background:#fff !important; padding:18px;
}
[data-testid="stFileUploader"] section:hover{ border-color:var(--gold) !important; }
[data-testid="stFileUploaderDropzoneInstructions"] *{ color:var(--muted) !important; }

/* ---- BOTÕES ---- */
/* primário (type="primary") + download (ação principal): verde floresta */
.stButton > button[kind="primary"],
[data-testid="stDownloadButton"] > button{
  background:var(--forest) !important; color:#fff !important; border:none !important;
  border-radius:12px !important; height:52px; font-family:'Poppins'; font-weight:600;
  font-size:14.5px; box-shadow:0 6px 16px rgba(15,70,48,.22);
}
.stButton > button[kind="primary"]:hover,
[data-testid="stDownloadButton"] > button:hover{ background:#0c3a28 !important; color:#fff !important; }
/* secundário: outline */
.stButton > button[kind="secondary"]{
  background:#fff !important; color:var(--forest) !important;
  border:1.5px solid #C9C2B0 !important; border-radius:12px !important; height:52px;
  font-family:'Poppins'; font-weight:600; font-size:13.5px;
}
/* botão dourado: o submit do formulário de login (único form do app) */
div[data-testid="stForm"] button{
  background:linear-gradient(135deg,var(--gold-2),var(--gold)) !important;
  color:var(--forest) !important; border:none !important; border-radius:11px !important;
  height:48px; font-family:'Poppins'; font-weight:600; font-size:14.5px;
  box-shadow:0 4px 12px rgba(196,154,69,.3);
}
/* o formulário de login é o card branco */
div[data-testid="stForm"]{ background:#fff !important; border:1px solid var(--line) !important;
  border-radius:16px !important; padding:24px 26px !important;
  box-shadow:0 8px 30px rgba(0,0,0,.06); }

/* ---- ALERTA DE SUCESSO (st.success) ---- */
[data-testid="stAlert"]{
  background:#E7F1E8 !important; border:1px solid #C3E0C8 !important;
  border-radius:12px !important; color:var(--forest) !important;
}

/* ---- EXPANDER (pré-visualizar o plano) ---- */
[data-testid="stExpander"]{ border:1px solid var(--line) !important; border-radius:12px !important;
  background:#fff !important; }
[data-testid="stExpander"] summary{ font-family:'Poppins'; font-weight:500; color:var(--forest); }

/* divisória mais suave */
[data-testid="stDivider"] hr, hr{ border-color:var(--line) !important; }
</style>
"""


def masthead_html(subtitulo: str = "", com_logo: bool = True, titulo: str = "Gerador de Plano de Aula") -> str:
    """Faixa verde com underline dourado (capa do app)."""
    logo = ""
    if com_logo:
        uri = logo_white_data_uri()
        if uri:
            logo = f'<img src="{uri}" alt="Rehagro" style="height:30px;width:auto;flex:none;position:relative;">'
    sub = (
        f'<div style="font-size:13px;color:rgba(255,255,255,.80);margin-top:6px;max-width:560px;">{subtitulo}</div>'
        if subtitulo else ""
    )
    return f"""
    <div style="position:relative;overflow:hidden;border-radius:16px;
         border-bottom:3px solid #C49A45;
         background:linear-gradient(135deg,#0F4630 0%,#0A2C1E 100%);
         padding:24px 30px;display:flex;align-items:center;justify-content:space-between;gap:24px;">
      {_RING}
      <div style="position:relative;">
        <div style="font-family:'Poppins';font-size:11px;font-weight:600;letter-spacing:.22em;
             text-transform:uppercase;color:#E0C06A;">Rehagro · Customer Success</div>
        <div style="font-family:'Poppins';font-size:26px;font-weight:700;color:#fff;margin-top:6px;line-height:1.1;">
             {titulo}</div>
        {sub}
      </div>
      {logo}
    </div>
    """


def step_html(n: int, titulo: str) -> str:
    return f'<div class="step"><span class="n">{n}</span><span class="t">{titulo}</span></div>'


def card_prioridade_html(num: int, titulo: str, aulas, tempo: str) -> str:
    aulas_txt = aulas if aulas not in (None, "") else "?"
    tempo_txt = tempo if tempo else "?"
    return f"""
    <div style="background:#fff;border:1px solid #E7E1D3;border-radius:14px;padding:16px 17px;
         box-shadow:0 2px 8px rgba(15,70,48,.04);height:100%;">
      <div style="display:flex;align-items:center;gap:10px;margin-bottom:11px;">
        <span style="width:30px;height:30px;border-radius:50%;flex:none;
             background:linear-gradient(135deg,#E6C977,#C49A45);color:#fff;font-family:'Poppins';
             font-weight:700;font-size:14px;display:flex;align-items:center;justify-content:center;
             box-shadow:0 3px 8px rgba(196,154,69,.3);">{num}</span>
        <span style="font-family:'Poppins';font-size:9.5px;font-weight:600;letter-spacing:.1em;
             text-transform:uppercase;color:#9A7626;background:#FBF3DE;padding:3px 9px;
             border-radius:999px;">{num}ª Prioridade</span>
      </div>
      <div style="font-family:'Poppins';font-weight:600;font-size:15px;color:#0F4630;
           line-height:1.25;min-height:38px;">{titulo}</div>
      <div style="margin-top:11px;padding-top:11px;border-top:1px solid #F0EBDE;
           color:#5A6B61;font-size:12.5px;">
        {aulas_txt} aulas · ~{tempo_txt}
      </div>
    </div>
    """
