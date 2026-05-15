"""
Página 2 — Gerador de Plano de Aula (acesso CS)
CS seleciona aluno, revisa e baixa o .docx
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import streamlit as st
from core.database    import inicializar_banco, listar_respostas, buscar_resposta, marcar_plano_gerado
from core.mapeamento  import get_dor_por_id, DORES
from core.gerador_plano import gerar_plano_docx
from core.styles      import BASE_CSS, section_tag_html
from config           import CS_PASSWORD, TURMA_ID, TURMA_NOME, RH_GREEN, RH_GOLD

st.set_page_config(
    page_title="Plano de Aula — CS Rehagro",
    page_icon="📋",
    layout="wide",
)

inicializar_banco()

# CSS base + sidebar visível para CS
CSS_CS = BASE_CSS.replace(
    "section[data-testid=\"stSidebar\"] { display: none; }",
    ""
)
st.markdown(CSS_CS, unsafe_allow_html=True)

# ── Autenticação ──────────────────────────────────────────────────────────
if "cs_auth" not in st.session_state:
    st.session_state.cs_auth = False

if not st.session_state.cs_auth:
    st.markdown(f"""
    <div style="max-width:400px; margin: 80px auto;">
        <div style="background:#1C3829; border-radius:12px; padding:32px; text-align:center;">
            <div style="font-size:11px; letter-spacing:2px; color:#C9A84C;
                        text-transform:uppercase; margin-bottom:8px;">
                Rehagro · Customer Success
            </div>
            <div style="font-size:22px; font-weight:800; color:#C9A84C;
                        text-transform:uppercase; letter-spacing:1px;">
                Acesso Restrito
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
                if senha == CS_PASSWORD:
                    st.session_state.cs_auth = True
                    st.rerun()
                else:
                    st.error("Senha incorreta.")
    st.stop()

# ─────────────────────────────────────────────────────────────────────────
#  PAINEL GERADOR DE PLANO
# ─────────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="rh-header">
    <div>
        <div class="rh-header-tag">Rehagro · Customer Success</div>
        <div class="rh-header-title">Gerador de Plano de Aula</div>
        <div class="rh-header-sub">Selecione o aluno, revise e baixe o .docx personalizado</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Filtros ───────────────────────────────────────────────────────────────
col_f1, col_f2 = st.columns([2, 1])
with col_f1:
    busca = st.text_input("🔍 Buscar por nome ou CPF", placeholder="Ex: João Silva ou 000.000.000-00")
with col_f2:
    filtro_status = st.selectbox("Status do plano",
                                  ["Todos", "Aguardando geração", "Plano gerado"])

respostas = listar_respostas()

# Aplicar filtros
if busca:
    busca_l = busca.lower().strip()
    respostas = [
        r for r in respostas
        if busca_l in (r.get("nome") or "").lower()
        or busca_l in (r.get("cpf") or "")
    ]
if filtro_status == "Aguardando geração":
    respostas = [r for r in respostas if not r.get("plano_gerado")]
elif filtro_status == "Plano gerado":
    respostas = [r for r in respostas if r.get("plano_gerado")]

st.divider()

if not respostas:
    st.info("Nenhuma resposta encontrada com os filtros aplicados.")
    st.stop()

# ── Lista de alunos ───────────────────────────────────────────────────────
st.markdown(section_tag_html(f"{len(respostas)} respostas encontradas"), unsafe_allow_html=True)

cols_header = st.columns([3, 2, 2, 2, 1])
for c, h in zip(cols_header, ["Nome", "Turma", "Data", "Status", "Ação"]):
    c.markdown(f"<small style='color:#6B6B5E; font-weight:600; "
               f"text-transform:uppercase; letter-spacing:1px;'>{h}</small>",
               unsafe_allow_html=True)

for r in respostas:
    cols = st.columns([3, 2, 2, 2, 1])
    with cols[0]:
        st.markdown(f"**{r.get('nome', '—')}**  \n"
                    f"<small style='color:#6B6B5E'>CPF: {r.get('cpf','—')}</small>",
                    unsafe_allow_html=True)
    with cols[1]:
        st.markdown(f"<small>{r.get('turma_id','—')}</small>", unsafe_allow_html=True)
    with cols[2]:
        criado = (r.get("criado_em") or "")[:16]
        st.markdown(f"<small>{criado}</small>", unsafe_allow_html=True)
    with cols[3]:
        if r.get("plano_gerado"):
            st.markdown("✅ <small style='color:#1C3829'>Gerado</small>",
                        unsafe_allow_html=True)
        else:
            st.markdown("⏳ <small style='color:#C9A84C'>Pendente</small>",
                        unsafe_allow_html=True)
    with cols[4]:
        if st.button("Ver →", key=f"ver_{r['id']}"):
            st.session_state["aluno_selecionado"] = r["id"]

    st.markdown("<hr style='margin:6px 0; border:none; "
                "border-top:0.5px solid #D8D3C8'>", unsafe_allow_html=True)

# ── Painel de revisão e geração ───────────────────────────────────────────
if "aluno_selecionado" in st.session_state:
    r = buscar_resposta(st.session_state["aluno_selecionado"])
    if not r:
        st.error("Resposta não encontrada.")
        st.stop()

    st.divider()
    st.markdown(section_tag_html(f"Revisão do plano — {r.get('nome','—')}"),
                unsafe_allow_html=True)

    col_info, col_plan = st.columns([1, 2])

    with col_info:
        st.markdown("**Dados do aluno**")
        info_items = [
            ("Turma",      r.get("turma_id","—")),
            ("Cidade",     f"{r.get('cidade','—')} / {r.get('estado','—')}"),
            ("Cargo",      r.get("cargo","—")),
            ("Produção",   f"{r.get('producao_litros_dia') or 'N/A'} L/dia"),
            ("Animais",    f"{r.get('animais_lactacao') or 'N/A'} vacas"),
            ("Média/vaca", f"{r.get('media_vaca_dia') or 'N/A'} L/vaca/dia"),
            ("Respondido em", (r.get("criado_em") or "")[:16]),
        ]
        for label, val in info_items:
            st.markdown(
                f"<div style='display:flex; justify-content:space-between; "
                f"font-size:13px; padding:6px 0; "
                f"border-bottom:0.5px solid #D8D3C8;'>"
                f"<span style='color:#6B6B5E'>{label}</span>"
                f"<span style='font-weight:500'>{val}</span></div>",
                unsafe_allow_html=True,
            )

        st.markdown("<br>**Objetivos declarados**", unsafe_allow_html=True)
        st.markdown(
            f"<div style='background:#FBF6ED; border-left:3px solid #C9A84C; "
            f"border-radius:0 8px 8px 0; padding:12px; font-size:13px; "
            f"margin-bottom:8px; color:#1A1A1A;'>"
            f"<strong>Valeu a pena se:</strong><br>{r.get('valeu_a_pena','—')}</div>",
            unsafe_allow_html=True,
        )
        st.markdown(
            f"<div style='background:#EAF0EC; border-left:3px solid #1C3829; "
            f"border-radius:0 8px 8px 0; padding:12px; font-size:13px; color:#1A1A1A;'>"
            f"<strong>Meta:</strong><br>{r.get('meta_fazenda','—')}</div>",
            unsafe_allow_html=True,
        )

    with col_plan:
        st.markdown("**Trilha personalizada gerada**")

        dores_ids = [r.get("prioridade_1"), r.get("prioridade_2"), r.get("prioridade_3")]
        badges    = ["🥇 1ª prioridade", "🥈 2ª prioridade", "🥉 3ª prioridade"]
        cores     = ["#FBF6ED", "#F5F1E8", "#F0EDE4"]

        for i, dor_id in enumerate(dores_ids):
            mod = get_dor_por_id(dor_id) if dor_id else None
            if mod:
                st.markdown(f"""
                <div style="background:{cores[i]}; border:0.5px solid #D8D3C8;
                            border-left:4px solid #C9A84C; border-radius:0 8px 8px 0;
                            padding:14px 16px; margin-bottom:10px;">
                    <div style="font-size:11px; font-weight:700; letter-spacing:1.5px;
                                color:#C9A84C; text-transform:uppercase; margin-bottom:4px;">
                        {badges[i]}
                    </div>
                    <div style="font-size:14px; font-weight:600; color:#1C3829; margin-bottom:2px;">
                        {mod['modulo']}
                    </div>
                    <div style="font-size:12px; color:#6B6B5E;">
                        {mod['dor']}
                    </div>
                    {"<div style='font-size:11px; color:#888; margin-top:4px;'>" +
                     str(mod.get('aulas','?')) + " aulas · " + str(mod.get('tempo','?')) + " · " +
                     str(mod.get('programacao','')) + "</div>" if mod.get('aulas') else ""}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(
                    f"<div style='color:#aaa; font-size:13px; padding:8px;'>"
                    f"{badges[i]}: não preenchido</div>",
                    unsafe_allow_html=True,
                )

        st.markdown("<br>", unsafe_allow_html=True)

        # Botão de download
        try:
            docx_bytes = gerar_plano_docx(r)
            nome_arquivo = f"Plano_de_Aula_{r.get('nome','aluno').replace(' ','_')}.docx"
            st.download_button(
                label="⬇️ Baixar Plano de Aula (.docx)",
                data=docx_bytes,
                file_name=nome_arquivo,
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                type="primary",
                use_container_width=True,
                on_click=lambda: marcar_plano_gerado(r["id"]),
            )
            if r.get("plano_gerado"):
                gerado_em = (r.get("plano_gerado_em") or "")[:16]
                st.caption(f"✅ Plano já foi gerado em {gerado_em}")
        except Exception as e:
            st.error(f"Erro ao gerar o plano: {e}")
