"""
CS Rehagro — Gerador de Plano de Aula a partir do CSV do HubSpot Survey.

Duas telas (uso interno do time CS), no design Rehagro:
    1. Login (senha CS)
    2. Gerador: upload do CSV → seleção do aluno → geração do plano
       - PDF automático (Chromium headless) quando disponível;
       - fallback: download do HTML (o CS salva como PDF pelo navegador).
"""
import os
import sys

import streamlit as st
import streamlit.components.v1 as components

sys.path.insert(0, os.path.dirname(__file__))
from core.hubspot_csv import parse_hubspot_csv
from core.dados_plano import montar_dados
from core.render_plano import render_html, gerar_pdf
from core.styles import BRAND_CSS, masthead_html, step_html, card_prioridade_html
from config import CS_PASSWORD

st.set_page_config(
    page_title="Gerador de Plano de Aula · Rehagro",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="collapsed",
)
st.markdown(BRAND_CSS, unsafe_allow_html=True)


def _slug(nome: str) -> str:
    return "".join(c if c.isalnum() else "_" for c in (nome or "aluno")).strip("_")


# ──────────────────────────────────────────────────────────────────────────
#  TELA 1 — LOGIN
# ──────────────────────────────────────────────────────────────────────────
def tela_login():
    col = st.columns([1, 2, 1])[1]
    with col:
        st.markdown(masthead_html(com_logo=False), unsafe_allow_html=True)
        st.write("")
        with st.form("login_form"):
            senha = st.text_input(
                "Senha de acesso", type="password",
                placeholder="Digite a senha do time CS",
            )
            entrar = st.form_submit_button("Entrar  →", use_container_width=True)
            st.caption("🔒 Acesso restrito à equipe de Customer Success.")

        if entrar:
            if senha == CS_PASSWORD and CS_PASSWORD != "":
                st.session_state.cs_auth = True
                st.rerun()
            elif CS_PASSWORD == "":
                st.error("Senha CS não configurada (defina CS_PASSWORD nos secrets).")
            else:
                st.error("Senha incorreta.")


# ──────────────────────────────────────────────────────────────────────────
#  TELA 2 — GERADOR
# ──────────────────────────────────────────────────────────────────────────
def tela_gerador():
    st.markdown(
        masthead_html("Suba o CSV do HubSpot, escolha o aluno e gere o plano no design Rehagro."),
        unsafe_allow_html=True,
    )
    st.write("")

    # ── Etapa 1 — CSV ─────────────────────────────────────────────────────
    st.markdown(step_html(1, "Arquivo CSV exportado do HubSpot Survey"), unsafe_allow_html=True)
    arquivo = st.file_uploader(
        "CSV", type=["csv"], label_visibility="collapsed",
        help="Exporte as respostas da pesquisa de início de curso no HubSpot e suba aqui.",
    )

    if not arquivo:
        st.stop()

    try:
        alunos = parse_hubspot_csv(arquivo.getvalue())
    except Exception as e:
        st.error(f"Não consegui ler o CSV: {e}")
        st.stop()

    if not alunos:
        st.warning("O CSV foi lido, mas nenhum aluno foi encontrado. Confira o arquivo.")
        st.stop()

    st.success(f"{len(alunos)} aluno(s) carregado(s) do CSV.")
    st.divider()

    # ── Etapa 2 — Aluno ───────────────────────────────────────────────────
    st.markdown(step_html(2, "Selecione o aluno"), unsafe_allow_html=True)
    idx = st.selectbox(
        "Aluno", range(len(alunos)), label_visibility="collapsed",
        format_func=lambda i: (
            f"{i + 1}. {alunos[i].get('nome') or 'Sem nome'}"
            f"{'  ·  ' + alunos[i]['curso'] if alunos[i].get('curso') else ''}"
        ),
    )
    aluno = alunos[idx]
    modulos = aluno.get("modulos", [])

    if not modulos:
        st.error("Nenhuma das 3 prioridades casou com a lista de dores. "
                 "Confira o texto das opções no HubSpot vs. o mapeamento.")
    else:
        cols = st.columns(len(modulos), gap="medium")
        for i, (c, m) in enumerate(zip(cols, modulos), start=1):
            c.markdown(
                card_prioridade_html(i, m["modulo"], m.get("aulas"), m.get("tempo")),
                unsafe_allow_html=True,
            )

    if aluno.get("dores_nao_reconhecidas"):
        st.warning(
            "Trechos do campo de prioridades que **não** casaram com nenhuma dor:\n\n"
            + "\n".join(f"- {s}" for s in aluno["dores_nao_reconhecidas"])
        )

    st.divider()

    # ── Etapa 3 — Gerar ───────────────────────────────────────────────────
    st.markdown(step_html(3, "Gere e envie o plano"), unsafe_allow_html=True)

    html = render_html(montar_dados(aluno))
    nome_base = f"Plano_de_Aula_{_slug(aluno.get('nome'))}"

    b1, b2 = st.columns([1.6, 1], gap="medium")
    with b1:
        gerar = st.button("📄  Gerar PDF do plano", type="primary",
                          use_container_width=True, disabled=not modulos)
    with b2:
        st.download_button(
            "⬇  Baixar HTML (salvar como PDF)",
            data=html.encode("utf-8"),
            file_name=f"{nome_base}.html",
            mime="text/html",
            use_container_width=True,
            disabled=not modulos,
            help="Abra o arquivo e use Ctrl+P → 'Salvar como PDF' (layout A4 já configurado).",
        )

    if gerar:
        with st.spinner("Gerando o PDF..."):
            pdf = gerar_pdf(html)
        if pdf:
            st.download_button(
                "✅ Baixar Plano de Aula (PDF)",
                data=pdf,
                file_name=f"{nome_base}.pdf",
                mime="application/pdf",
                type="primary",
                use_container_width=True,
            )
        else:
            st.info(
                "A geração automática de PDF não está disponível neste ambiente "
                "(sem Chromium no servidor). Use o botão **Baixar HTML** e, no arquivo "
                "aberto, faça **Ctrl+P → Salvar como PDF** — o layout A4 já está pronto."
            )

    if modulos:
        with st.expander("👁  Pré-visualizar o plano"):
            components.html(html, height=900, scrolling=True)


# ──────────────────────────────────────────────────────────────────────────
if "cs_auth" not in st.session_state:
    st.session_state.cs_auth = False

if not st.session_state.cs_auth:
    tela_login()
else:
    tela_gerador()
