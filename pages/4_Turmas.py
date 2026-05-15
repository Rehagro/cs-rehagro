"""
Página 4 — Gestão de Turmas (acesso CS)
CS cria, edita, ativa e gera link público do formulário por turma
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import re
import streamlit as st
from core.database import (
    inicializar_banco, listar_turmas, get_turma_ativa,
    criar_turma, ativar_turma, atualizar_turma_nome, deletar_turma,
)
from core.styles import BASE_CSS, section_tag_html, header_html
from config import CS_PASSWORD

st.set_page_config(
    page_title="Turmas — CS Rehagro",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

inicializar_banco()
st.markdown(BASE_CSS, unsafe_allow_html=True)

# ── Autenticação ──────────────────────────────────────────────────────────
if not st.session_state.get("cs_auth"):
    st.warning("⚠️ Acesso restrito. Faça login na página **Plano de Aula**.")
    st.stop()

# ── Header ────────────────────────────────────────────────────────────────
st.markdown(header_html(
    "Gestão de Turmas",
    subtitulo="Crie, edite e ative turmas — gere o link público do formulário",
), unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────
#  CRIAR NOVA TURMA
# ─────────────────────────────────────────────────────────────────────────
st.markdown(section_tag_html("Cadastrar nova turma"), unsafe_allow_html=True)

with st.form("nova_turma"):
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        novo_id = st.text_input(
            "ID da turma *",
            placeholder="GPL-T19",
            help="Identificador curto (sem espaços). Ex: GPL-T19, GPL-T20",
        )
    with col2:
        novo_nome = st.text_input(
            "Nome da turma *",
            placeholder="Gestão na Pecuária Leiteira · Turma 19",
        )
    with col3:
        ativar_agora = st.checkbox("Tornar ativa", value=True,
                                   help="Desativa as demais")

    criar = st.form_submit_button("➕ Criar turma", type="primary",
                                  use_container_width=True)

    if criar:
        erros = []
        if not novo_id.strip():
            erros.append("ID é obrigatório.")
        elif not re.match(r"^[A-Za-z0-9_\-]+$", novo_id.strip()):
            erros.append("ID só pode ter letras, números, hífen e underline.")
        if not novo_nome.strip():
            erros.append("Nome é obrigatório.")

        if not erros:
            ok = criar_turma(novo_id.strip(), novo_nome.strip(), ativar=ativar_agora)
            if ok:
                st.success(f"✅ Turma **{novo_id}** criada com sucesso.")
                st.rerun()
            else:
                st.error(f"❌ Já existe uma turma com ID **{novo_id}**.")
        else:
            for e in erros:
                st.error(e)

st.divider()

# ─────────────────────────────────────────────────────────────────────────
#  LISTAR TURMAS
# ─────────────────────────────────────────────────────────────────────────
turmas = listar_turmas()
ativa  = get_turma_ativa()

st.markdown(section_tag_html(f"{len(turmas)} turma(s) cadastrada(s)"), unsafe_allow_html=True)

if not turmas:
    st.info("Nenhuma turma cadastrada ainda.")
    st.stop()

# Cabeçalho da tabela
cols_h = st.columns([2, 3, 1, 1, 1, 2])
for c, h in zip(cols_h, ["ID", "Nome", "Respostas", "Status", "Criada", "Ação"]):
    c.markdown(
        f"<small style='color:#6B6B5E; font-weight:600; "
        f"text-transform:uppercase; letter-spacing:1px;'>{h}</small>",
        unsafe_allow_html=True,
    )

for t in turmas:
    cols = st.columns([2, 3, 1, 1, 1, 2])
    with cols[0]:
        st.markdown(f"**{t['turma_id']}**")
    with cols[1]:
        # Permite editar o nome inline
        edit_key = f"edit_{t['turma_id']}"
        if st.session_state.get(edit_key):
            novo = st.text_input("Nome", value=t["turma_nome"],
                                 key=f"in_{t['turma_id']}",
                                 label_visibility="collapsed")
            cb1, cb2 = st.columns(2)
            with cb1:
                if st.button("Salvar", key=f"save_{t['turma_id']}", type="primary"):
                    atualizar_turma_nome(t["turma_id"], novo.strip())
                    st.session_state[edit_key] = False
                    st.rerun()
            with cb2:
                if st.button("Cancelar", key=f"cancel_{t['turma_id']}"):
                    st.session_state[edit_key] = False
                    st.rerun()
        else:
            st.markdown(t["turma_nome"])
    with cols[2]:
        st.markdown(f"<span style='color:#6B6B5E'>{t['qtd_respostas']}</span>",
                    unsafe_allow_html=True)
    with cols[3]:
        if t["ativa"]:
            st.markdown(
                "<span style='background:#1C3829; color:#C9A84C; "
                "padding:3px 10px; border-radius:12px; font-size:11px; "
                "font-weight:700; text-transform:uppercase; letter-spacing:1px;'>"
                "● Ativa</span>",
                unsafe_allow_html=True,
            )
        else:
            st.markdown("<span style='color:#aaa; font-size:12px;'>inativa</span>",
                        unsafe_allow_html=True)
    with cols[4]:
        criada = (t.get("criada_em") or "")[:10]
        st.markdown(f"<small style='color:#6B6B5E'>{criada}</small>",
                    unsafe_allow_html=True)
    with cols[5]:
        a1, a2, a3 = st.columns(3)
        with a1:
            if not t["ativa"]:
                if st.button("Ativar", key=f"ativar_{t['turma_id']}",
                             use_container_width=True):
                    ativar_turma(t["turma_id"])
                    st.rerun()
        with a2:
            if st.button("✎", key=f"edit_btn_{t['turma_id']}",
                         help="Editar nome",
                         use_container_width=True):
                st.session_state[edit_key] = True
                st.rerun()
        with a3:
            if t["qtd_respostas"] == 0:
                if st.button("🗑", key=f"del_{t['turma_id']}",
                             help="Remover (sem respostas)",
                             use_container_width=True):
                    ok, msg = deletar_turma(t["turma_id"])
                    if ok:
                        st.success(msg)
                        st.rerun()
                    else:
                        st.error(msg)

    st.markdown(
        "<hr style='margin:6px 0; border:none; border-top:0.5px solid #D8D3C8'>",
        unsafe_allow_html=True,
    )

st.divider()

# ─────────────────────────────────────────────────────────────────────────
#  LINK PÚBLICO DO FORMULÁRIO
# ─────────────────────────────────────────────────────────────────────────
st.markdown(section_tag_html("Link público do formulário"), unsafe_allow_html=True)

st.markdown(
    "<div class='rh-warning'>Compartilhe o link com os alunos da turma. "
    "Você pode usar o link sem parâmetro (cai sempre na turma ativa) ou "
    "com parâmetro <code>?turma=ID</code> pra direcionar pra uma turma específica.</div>",
    unsafe_allow_html=True,
)

# Detecta base URL (em produção, isso vem do request; em local mostramos placeholder)
base_url = st.text_input(
    "Base URL do app (apenas pra gerar os links abaixo)",
    value="http://localhost:8501",
    help="Quando estiver em produção, troque pelo domínio real (ex: https://cs.rehagro.com.br)",
)

if ativa:
    st.markdown(f"**Link para a turma ATIVA ({ativa['turma_id']})**")
    link_ativa = f"{base_url.rstrip('/')}/Formulario"
    st.code(link_ativa, language=None)

st.markdown("**Links por turma (com parâmetro)**")
for t in turmas:
    link = f"{base_url.rstrip('/')}/Formulario?turma={t['turma_id']}"
    st.markdown(f"- **{t['turma_id']}** — {t['turma_nome']}")
    st.code(link, language=None)
