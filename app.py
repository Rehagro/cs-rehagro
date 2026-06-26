"""
CS Rehagro — Gerador de Plano de Aula a partir do CSV do HubSpot Survey.

Fluxo (uso interno do time CS):
    1. Login (senha CS)
    2. Upload do CSV exportado do HubSpot Survey
    3. Seleção do aluno
    4. Geração do plano de aula no design Rehagro:
       - PDF automático (Chromium headless) quando disponível;
       - fallback: download do HTML (o CS salva como PDF pelo navegador, Ctrl+P).
"""
import os
import sys

import streamlit as st
import streamlit.components.v1 as components

sys.path.insert(0, os.path.dirname(__file__))
from core.hubspot_csv import parse_hubspot_csv
from core.dados_plano import montar_dados
from core.render_plano import render_html, gerar_pdf
from core.styles import BASE_CSS, header_html, section_tag_html
from config import CS_PASSWORD

st.set_page_config(
    page_title="Plano de Aula — CS Rehagro",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed",
)

CSS = BASE_CSS.replace(
    "</style>",
    "section[data-testid=\"stSidebar\"] { display: none; }</style>",
)
st.markdown(CSS, unsafe_allow_html=True)


def _slug(nome: str) -> str:
    return "".join(c if c.isalnum() else "_" for c in (nome or "aluno")).strip("_")


# ── Autenticação ──────────────────────────────────────────────────────────
if "cs_auth" not in st.session_state:
    st.session_state.cs_auth = False

if not st.session_state.cs_auth:
    st.markdown("""
    <div style="max-width:420px; margin: 70px auto 24px;">
        <div style="background:#0F4630; border-radius:14px; padding:34px; text-align:center;
                    border-bottom:4px solid #C49A45;">
            <div style="font-size:11px; letter-spacing:2px; color:#E0C06A;
                        text-transform:uppercase; margin-bottom:8px;">
                Rehagro · Customer Success
            </div>
            <div style="font-size:22px; font-weight:800; color:#E0C06A;
                        text-transform:uppercase; letter-spacing:1px;">
                Gerador de Plano de Aula
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    with st.form("login_form"):
        col_c = st.columns([1, 2, 1])
        with col_c[1]:
            senha = st.text_input("Senha de acesso", type="password",
                                  placeholder="Digite a senha do time CS")
            entrar = st.form_submit_button("Entrar →", type="primary",
                                           use_container_width=True)
            if entrar:
                if senha == CS_PASSWORD and CS_PASSWORD != "":
                    st.session_state.cs_auth = True
                    st.rerun()
                elif CS_PASSWORD == "":
                    st.error("Senha CS não configurada (defina CS_PASSWORD nos secrets).")
                else:
                    st.error("Senha incorreta.")
    st.stop()

# ─────────────────────────────────────────────────────────────────────────
#  PAINEL
# ─────────────────────────────────────────────────────────────────────────
st.markdown(
    header_html(
        "Gerador de Plano de Aula",
        "Suba o CSV do HubSpot, escolha o aluno e gere o plano no design Rehagro",
    ),
    unsafe_allow_html=True,
)

# ── Upload do CSV ─────────────────────────────────────────────────────────
arquivo = st.file_uploader(
    "Arquivo CSV exportado do HubSpot Survey",
    type=["csv"],
    help="Exporte as respostas da pesquisa de início de curso no HubSpot e suba aqui.",
)

if not arquivo:
    st.info("Suba o CSV do HubSpot para começar.")
    st.stop()

try:
    alunos = parse_hubspot_csv(arquivo.getvalue())
except Exception as e:
    st.error(f"Não consegui ler o CSV: {e}")
    st.stop()

if not alunos:
    st.warning("O CSV foi lido, mas nenhum aluno foi encontrado. Confira o arquivo.")
    st.stop()

st.success(f"✅ {len(alunos)} aluno(s) carregado(s) do CSV.")
st.divider()

# ── Seleção do aluno ──────────────────────────────────────────────────────
st.markdown(section_tag_html("Selecione o aluno"), unsafe_allow_html=True)

opcoes = {
    f"{i + 1}. {a.get('nome') or 'Sem nome'}"
    f"{'  ·  ' + a['curso'] if a.get('curso') else ''}": i
    for i, a in enumerate(alunos)
}
escolha = st.selectbox("Aluno", list(opcoes.keys()), label_visibility="collapsed")
aluno = alunos[opcoes[escolha]]

# ── Resumo da trilha casada ───────────────────────────────────────────────
modulos = aluno.get("modulos", [])
if not modulos:
    st.error("Nenhuma das 3 prioridades casou com a lista de dores. "
             "Confira o texto das opções no HubSpot vs. o mapeamento.")
else:
    cols = st.columns(len(modulos))
    for i, (col, m) in enumerate(zip(cols, modulos)):
        with col:
            st.markdown(
                f"<div style='border:0.5px solid #E2EAE4; border-left:4px solid #C49A45; "
                f"border-radius:0 8px 8px 0; padding:12px 14px; background:#FBFAF4;'>"
                f"<div style='font-size:10px; font-weight:700; letter-spacing:1px; "
                f"color:#9A7626; text-transform:uppercase;'>{i + 1}ª prioridade</div>"
                f"<div style='font-size:14px; font-weight:600; color:#0F4630; margin-top:3px;'>"
                f"{m['modulo']}</div>"
                f"<div style='font-size:11px; color:#6A776E; margin-top:3px;'>"
                f"{m.get('aulas') or '?'} aulas · ~{m.get('tempo') or '?'}</div></div>",
                unsafe_allow_html=True,
            )

if aluno.get("dores_nao_reconhecidas"):
    st.warning(
        "Trechos do campo de prioridades que **não** casaram com nenhuma dor:\n\n"
        + "\n".join(f"- {s}" for s in aluno["dores_nao_reconhecidas"])
    )

st.divider()

# ── Geração do plano ──────────────────────────────────────────────────────
dados = montar_dados(aluno)
html = render_html(dados)
nome_base = f"Plano_de_Aula_{_slug(aluno.get('nome'))}"

col_a, col_b = st.columns([1, 1])

with col_a:
    gerar = st.button("📄 Gerar PDF do plano", type="primary",
                      use_container_width=True, disabled=not modulos)

with col_b:
    st.download_button(
        "⬇️ Baixar HTML (salvar como PDF no navegador)",
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
            "(sem Chromium no servidor). Use o botão **Baixar HTML** ao lado e, "
            "no arquivo aberto, faça **Ctrl+P → Salvar como PDF** — o layout A4 já "
            "está pronto e sai idêntico."
        )

# ── Pré-visualização ──────────────────────────────────────────────────────
if modulos:
    with st.expander("👁️ Pré-visualizar o plano"):
        components.html(html, height=900, scrolling=True)
