"""
Rehagro · Gerador de Plano de Aula — APP DE REFERÊNCIA (Streamlit)

Mostra COMO estruturar e estilizar as duas telas (login + gerador) no
design Rehagro. É um guia de implementação, não um produto final:
- A lógica de CSV / geração de PDF deve usar o seu código atual.
- O foco aqui é o layout e a aplicação do CSS de marca (styles.css).

Componentes "ricos" (masthead, cards de prioridade, banners, títulos de
etapa) são desenhados em HTML puro via st.markdown(unsafe_allow_html=True),
porque os widgets nativos do Streamlit não alcançam esse nível de controle.
Widgets funcionais (file_uploader, selectbox, text_input, button, expander)
são nativos e recebem o tema via styles.css.

Rodar:  streamlit run app_example.py
Requer: a pasta .streamlit/config.toml e o styles.css ao lado deste arquivo.
"""
import base64
from pathlib import Path
import streamlit as st

BASE = Path(__file__).parent
ASSETS = BASE.parent / "assets"
SENHA_CS = "rehagro"  # troque pela sua senha / variável de ambiente


# ----------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------
def inject_css():
    css = (BASE / "styles.css").read_text(encoding="utf-8")
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


def logo_data_uri(nome: str) -> str:
    png = (ASSETS / nome).read_bytes()
    return f"data:image/png;base64,{base64.b64encode(png).decode()}"


def masthead(subtitulo: str = "", com_logo: bool = True):
    """Faixa verde com underline dourado (capa do app)."""
    logo = (
        f'<img src="{logo_data_uri("rehagro-logo-white.png")}" '
        f'style="height:30px;width:auto;flex:none;">'
        if com_logo else ""
    )
    sub = (
        f'<div style="font-size:13px;color:rgba(255,255,255,.78);margin-top:6px;">{subtitulo}</div>'
        if subtitulo else ""
    )
    st.markdown(f"""
    <div style="position:relative;overflow:hidden;border-radius:16px;
         border-bottom:3px solid #C49A45;
         background:linear-gradient(135deg,#0F4630 0%,#0A2C1E 100%);
         padding:24px 30px;display:flex;align-items:center;justify-content:space-between;gap:24px;">
      <div>
        <div style="font-family:'Poppins';font-size:11px;font-weight:600;letter-spacing:.22em;
             text-transform:uppercase;color:#E0C06A;">Rehagro · Customer Success</div>
        <div style="font-family:'Poppins';font-size:26px;font-weight:700;color:#fff;margin-top:6px;">
             Gerador de Plano de Aula</div>
        {sub}
      </div>
      {logo}
    </div>
    """, unsafe_allow_html=True)


def step(n: int, titulo: str):
    st.markdown(
        f'<div class="step"><span class="n">{n}</span><span class="t">{titulo}</span></div>',
        unsafe_allow_html=True,
    )


def card_prioridade(num: int, modulo: dict) -> str:
    return f"""
    <div style="background:#fff;border:1px solid #E7E1D3;border-radius:14px;padding:16px 17px;
         box-shadow:0 2px 8px rgba(15,70,48,.04);">
      <div style="display:flex;align-items:center;gap:10px;margin-bottom:11px;">
        <span style="width:30px;height:30px;border-radius:50%;
             background:linear-gradient(135deg,#E6C977,#C49A45);color:#fff;font-family:'Poppins';
             font-weight:700;font-size:14px;display:flex;align-items:center;justify-content:center;
             box-shadow:0 3px 8px rgba(196,154,69,.3);">{num}</span>
        <span style="font-family:'Poppins';font-size:9.5px;font-weight:600;letter-spacing:.1em;
             text-transform:uppercase;color:#9A7626;background:#FBF3DE;padding:3px 9px;
             border-radius:999px;">{num}ª Prioridade</span>
      </div>
      <div style="font-family:'Poppins';font-weight:600;font-size:15px;color:#0F4630;
           line-height:1.25;min-height:38px;">{modulo['titulo']}</div>
      <div style="margin-top:11px;padding-top:11px;border-top:1px solid #F0EBDE;
           color:#5A6B61;font-size:12.5px;">
        {modulo['qtd_aulas']} aulas · {modulo['tempo_aula']}
      </div>
    </div>
    """


# ----------------------------------------------------------------------
# TELA 1 — LOGIN
# ----------------------------------------------------------------------
def tela_login():
    col = st.columns([1, 2, 1])[1]  # coluna central ~520px
    with col:
        masthead(com_logo=False)
        st.write("")
        with st.container(border=True):
            senha = st.text_input("Senha de acesso", type="password",
                                  placeholder="Digite a senha do time CS")
            st.markdown('<div class="gold-btn">', unsafe_allow_html=True)
            entrar = st.button("Entrar  →", use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
            st.caption("🔒 Acesso restrito à equipe de Customer Success.")
        if entrar:
            if senha == SENHA_CS:
                st.session_state["auth"] = True
                st.rerun()
            else:
                st.error("Senha incorreta.")


# ----------------------------------------------------------------------
# TELA 2 — GERADOR
# ----------------------------------------------------------------------
def tela_gerador():
    masthead("Suba o CSV do HubSpot, escolha o aluno e gere o plano no design Rehagro.")
    st.write("")

    # STEP 1 — CSV
    step(1, "Arquivo CSV exportado do HubSpot Survey")
    arquivo = st.file_uploader("CSV", type=["csv"], label_visibility="collapsed")
    alunos = []
    if arquivo is not None:
        alunos = carregar_alunos(arquivo)   # << sua lógica atual
        st.success(f"{len(alunos)} aluno(s) carregado(s) do CSV.")

    st.divider()

    if alunos:
        # STEP 2 — ALUNO
        step(2, "Selecione o aluno")
        idx = st.selectbox(
            "Aluno", range(len(alunos)), label_visibility="collapsed",
            format_func=lambda i: f"{i+1}. {alunos[i]['nome']} · {alunos[i]['curso']}",
        )
        aluno = alunos[idx]

        # cards de prioridade (3 colunas)
        cols = st.columns(3, gap="medium")
        for i, (c, m) in enumerate(zip(cols, aluno["modulos"]), start=1):
            c.markdown(card_prioridade(i, m), unsafe_allow_html=True)

        st.divider()

        # STEP 3 — GERAR
        step(3, "Gere e envie o plano")
        b1, b2 = st.columns([1.6, 1], gap="medium")
        if b1.button("📄  Gerar PDF do plano", type="primary", use_container_width=True):
            gerar_pdf(aluno)                # << reaproveita o template Jinja2 do plano de aula
        b2.download_button("⬇  Baixar HTML (salvar como PDF)",
                           data=render_html(aluno), file_name="plano_de_aula.html",
                           use_container_width=True)

        with st.expander("👁  Pré-visualizar o plano"):
            st.components.v1.html(render_html(aluno), height=900, scrolling=True)


# ----------------------------------------------------------------------
# Stubs — substitua pela sua implementação real
# ----------------------------------------------------------------------
def carregar_alunos(arquivo):  # -> list[dict]
    raise NotImplementedError("use seu parser de CSV atual")

def render_html(aluno) -> str:  # usa o template do handoff do PLANO DE AULA
    raise NotImplementedError("renderize com plano_de_aula.html.j2")

def gerar_pdf(aluno):           # Playwright/Chromium (ver render.py do plano de aula)
    raise NotImplementedError


# ----------------------------------------------------------------------
def main():
    st.set_page_config(page_title="Gerador de Plano de Aula · Rehagro",
                       page_icon="🌱", layout="wide")
    inject_css()
    if not st.session_state.get("auth"):
        tela_login()
    else:
        tela_gerador()


if __name__ == "__main__":
    main()
