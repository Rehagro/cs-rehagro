"""
CS Rehagro — Gerador de Plano de Aula a partir do CSV do HubSpot Survey.

Fluxo (uso interno do time CS):
    1. Login (senha CS)
    2. Upload do CSV exportado do HubSpot Survey
    3. Seleção do aluno
    4. Revisão da trilha (3 dores → 3 módulos) + dados do aluno
    5. Download do plano de aula em .docx (identidade visual Rehagro)
"""
import os
import sys

import streamlit as st

sys.path.insert(0, os.path.dirname(__file__))
from core.hubspot_csv import parse_hubspot_csv
from core.gerador_plano import gerar_plano_docx
from core.mapeamento import get_dor_por_id
from core.styles import BASE_CSS, header_html, section_tag_html
from config import CS_PASSWORD

st.set_page_config(
    page_title="Plano de Aula — CS Rehagro",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# CSS base (esconde a sidebar — app de página única)
CSS = BASE_CSS.replace(
    "</style>",
    "section[data-testid=\"stSidebar\"] { display: none; }</style>",
)
st.markdown(CSS, unsafe_allow_html=True)

# ── Autenticação ──────────────────────────────────────────────────────────
if "cs_auth" not in st.session_state:
    st.session_state.cs_auth = False

if not st.session_state.cs_auth:
    st.markdown("""
    <div style="max-width:420px; margin: 70px auto 24px;">
        <div style="background:#015641; border-radius:14px; padding:34px; text-align:center;
                    border-bottom:4px solid #cdaf69;">
            <div style="font-size:11px; letter-spacing:2px; color:#cdaf69;
                        text-transform:uppercase; margin-bottom:8px;">
                Rehagro · Customer Success
            </div>
            <div style="font-size:22px; font-weight:800; color:#cdaf69;
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
        "Suba o CSV do HubSpot, escolha o aluno e baixe o plano em .docx",
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

st.divider()

# ── Revisão ───────────────────────────────────────────────────────────────
col_info, col_plan = st.columns([1, 2])

with col_info:
    st.markdown("**Dados do aluno**")
    info_items = [
        ("Curso",      aluno.get("curso", "—")),
        ("Perfil",     aluno.get("perfil", "—")),
        ("Formação",   aluno.get("formacao", "—")),
        ("Produção",   aluno.get("producao", "—")),
        ("Animais",    aluno.get("animais", "—")),
        ("Média/vaca", aluno.get("media_vaca", "—")),
        ("E-mail",     aluno.get("email", "—")),
    ]
    for label, val in info_items:
        st.markdown(
            f"<div style='display:flex; justify-content:space-between; gap:12px; "
            f"font-size:13px; padding:6px 0; "
            f"border-bottom:0.5px solid #D8D3C8;'>"
            f"<span style='color:#6B6B5E'>{label}</span>"
            f"<span style='font-weight:500; text-align:right'>{val or '—'}</span></div>",
            unsafe_allow_html=True,
        )

    st.markdown("<br>**Respostas abertas**", unsafe_allow_html=True)
    st.markdown(
        f"<div style='background:#FBF6ED; border-left:3px solid #cdaf69; "
        f"border-radius:0 8px 8px 0; padding:12px; font-size:13px; "
        f"margin-bottom:8px; color:#1A1A1A;'>"
        f"<strong>Para valer a pena, preciso aprender:</strong><br>"
        f"{aluno.get('valeu_a_pena') or '—'}</div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        f"<div style='background:#EAF0EC; border-left:3px solid #015641; "
        f"border-radius:0 8px 8px 0; padding:12px; font-size:13px; color:#1A1A1A;'>"
        f"<strong>Meta em 5 anos:</strong><br>{aluno.get('meta') or '—'}</div>",
        unsafe_allow_html=True,
    )

with col_plan:
    st.markdown("**Trilha personalizada** "
                "<span style='color:#6B6B5E; font-size:12px;'>(na ordem em que aparece no HubSpot)</span>",
                unsafe_allow_html=True)

    modulos = aluno.get("modulos", [])
    badges = ["1ª prioridade", "2ª prioridade", "3ª prioridade"]

    if not modulos:
        st.error("Nenhuma das 3 prioridades casou com a lista de dores. "
                 "Confira o texto das opções no HubSpot vs. o mapeamento.")
    for i, mod in enumerate(modulos):
        st.markdown(f"""
        <div style="background:#FBF6ED; border:0.5px solid #D8D3C8;
                    border-left:4px solid #cdaf69; border-radius:0 8px 8px 0;
                    padding:14px 16px; margin-bottom:10px;">
            <div style="font-size:11px; font-weight:700; letter-spacing:1.5px;
                        color:#cdaf69; text-transform:uppercase; margin-bottom:4px;">
                {badges[i] if i < 3 else f'{i+1}ª'}
            </div>
            <div style="font-size:14px; font-weight:600; color:#015641; margin-bottom:2px;">
                {mod['modulo']}
            </div>
            <div style="font-size:12px; color:#6B6B5E;">{mod['dor']}</div>
            {"<div style='font-size:11px; color:#888; margin-top:4px;'>" +
             str(mod.get('aulas') or '?') + " aulas · " + str(mod.get('tempo') or '?') +
             (" · " + str(mod.get('programacao')) if mod.get('programacao') else '') +
             "</div>" if mod.get('aulas') else ""}
        </div>
        """, unsafe_allow_html=True)

    if aluno.get("dores_nao_reconhecidas"):
        st.warning(
            "Trechos do campo de prioridades que **não** casaram com nenhuma dor:\n\n"
            + "\n".join(f"- {s}" for s in aluno["dores_nao_reconhecidas"])
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Download ──────────────────────────────────────────────────────────
    try:
        docx_bytes = gerar_plano_docx(aluno)
        nome_arq = f"Plano_de_Aula_{(aluno.get('nome') or 'aluno').replace(' ', '_')}.docx"
        st.download_button(
            label="⬇️ Baixar Plano de Aula (.docx)",
            data=docx_bytes,
            file_name=nome_arq,
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            type="primary",
            use_container_width=True,
            disabled=not modulos,
        )
    except Exception as e:
        st.error(f"Erro ao gerar o plano: {e}")
