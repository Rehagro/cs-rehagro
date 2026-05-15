"""
Página 3 — Dashboard CS
Análises e gráficos das respostas da pesquisa
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from core.database   import inicializar_banco, listar_respostas
from core.mapeamento import DORES, get_dor_por_id
from core.styles     import BASE_CSS, section_tag_html
from config          import CS_PASSWORD, RH_GREEN, RH_GOLD

st.set_page_config(
    page_title="Dashboard CS — Rehagro GPL",
    page_icon="📊",
    layout="wide",
)

inicializar_banco()
CSS_CS = BASE_CSS.replace(
    'section[data-testid="stSidebar"] { display: none; }', ""
)
st.markdown(CSS_CS, unsafe_allow_html=True)

# ── Autenticação ──────────────────────────────────────────────────────────
if not st.session_state.get("cs_auth"):
    st.warning("⚠️ Acesso restrito. Faça login na página **Plano de Aula**.")
    st.stop()

# ── Carrega dados ─────────────────────────────────────────────────────────
respostas = listar_respostas()

st.markdown("""
<div class="rh-header">
    <div>
        <div class="rh-header-tag">Rehagro · Customer Success</div>
        <div class="rh-header-title">Dashboard — Pesquisa de Início</div>
        <div class="rh-header-sub">Análise das respostas coletadas por turma</div>
    </div>
</div>
""", unsafe_allow_html=True)

if not respostas:
    st.info("Nenhuma resposta registrada ainda.")
    st.stop()

df = pd.DataFrame(respostas)

# ── Filtro de turma ───────────────────────────────────────────────────────
turmas = ["Todas"] + sorted(df["turma_id"].dropna().unique().tolist())
col_t, col_gap = st.columns([2, 5])
with col_t:
    turma_sel = st.selectbox("Filtrar por turma", turmas)

if turma_sel != "Todas":
    df = df[df["turma_id"] == turma_sel]

if df.empty:
    st.info("Nenhuma resposta para a turma selecionada.")
    st.stop()

# ─────────────────────────────────────────────────────────────────────────
#  MÉTRICAS PRINCIPAIS
# ─────────────────────────────────────────────────────────────────────────
st.markdown(section_tag_html("Visão geral"), unsafe_allow_html=True)

col1, col2, col3, col4, col5 = st.columns(5)

total = len(df)
prod_valid = df[df["nao_se_aplica_producao"] == 0]["producao_litros_dia"].dropna()
media_prod  = prod_valid.mean() if len(prod_valid) > 0 else None
media_vaca_valid = df[df["nao_se_aplica_media"] == 0]["media_vaca_dia"].dropna()
media_vaca  = media_vaca_valid.mean() if len(media_vaca_valid) > 0 else None
planos_gerados = df["plano_gerado"].sum()

with col1:
    st.metric("Total de respostas", total)
with col2:
    st.metric("Média produção",
              f"{media_prod:,.0f} L/dia" if media_prod else "N/A")
with col3:
    st.metric("Média/vaca",
              f"{media_vaca:.1f} L/vaca/dia" if media_vaca else "N/A")
with col4:
    st.metric("Planos gerados", int(planos_gerados))
with col5:
    pct_planos = (int(planos_gerados) / total * 100) if total > 0 else 0
    st.metric("Cobertura CS", f"{pct_planos:.0f}%")

st.divider()

# ─────────────────────────────────────────────────────────────────────────
#  GRÁFICO 1 — % das dores (1ª prioridade)
# ─────────────────────────────────────────────────────────────────────────
st.markdown(section_tag_html("Dores mais urgentes — 1ª prioridade"), unsafe_allow_html=True)

dor_map = {d["id"]: d["dor_curta"] for d in DORES}

col_g1, col_g2 = st.columns([3, 2])

with col_g1:
    dores_1a = df["prioridade_1"].dropna().map(lambda x: dor_map.get(x, x))
    contagem_1a = dores_1a.value_counts().reset_index()
    contagem_1a.columns = ["Dor", "Qtd"]
    contagem_1a["Pct"] = (contagem_1a["Qtd"] / len(df) * 100).round(1)
    contagem_1a_sorted = contagem_1a.sort_values("Qtd")

    fig1 = px.bar(
        contagem_1a_sorted,
        x="Pct", y="Dor",
        orientation="h",
        text=contagem_1a_sorted.apply(
            lambda r: f"{int(r['Qtd'])} ({r['Pct']:.0f}%)", axis=1
        ),
        color_discrete_sequence=[RH_GOLD],
    )
    fig1.update_layout(
        plot_bgcolor="white", paper_bgcolor="white",
        margin=dict(l=10, r=40, t=10, b=10),
        xaxis_title="% dos respondentes",
        yaxis_title="",
        font=dict(family="sans-serif", size=12),
        height=380,
    )
    fig1.update_traces(
        textposition="outside",
        textfont=dict(size=12, color="#1C3829"),
        cliponaxis=False,
    )
    st.plotly_chart(fig1, use_container_width=True)

with col_g2:
    # Contagem combinada das 3 prioridades
    todas_dores = []
    for col in ["prioridade_1", "prioridade_2", "prioridade_3"]:
        todas_dores.extend(df[col].dropna().tolist())
    contagem_geral = pd.Series(todas_dores).map(lambda x: dor_map.get(x, x)).value_counts()

    fig2 = px.pie(
        values=contagem_geral.values,
        names=contagem_geral.index,
        color_discrete_sequence=[
            RH_GREEN, RH_GOLD, "#4A7C5E", "#D4B96C",
            "#2E5C44", "#E8C98C", "#6B9E7C", "#B8935A", "#3A6B50",
        ],
        hole=0.45,
    )
    fig2.update_layout(
        title="Todas as prioridades (1ª + 2ª + 3ª)",
        plot_bgcolor="white", paper_bgcolor="white",
        margin=dict(l=10, r=10, t=40, b=10),
        font=dict(family="sans-serif", size=11),
        legend=dict(font=dict(size=10)),
        height=380,
    )
    fig2.update_traces(
        textinfo="value+percent",
        textfont=dict(size=12, color="white"),
        textposition="inside",
        hovertemplate="<b>%{label}</b><br>Qtd: %{value}<br>%{percent}<extra></extra>",
    )
    st.plotly_chart(fig2, use_container_width=True)

st.divider()

# ─────────────────────────────────────────────────────────────────────────
#  GRÁFICO 2 — Distribuição de produção
# ─────────────────────────────────────────────────────────────────────────
st.markdown(section_tag_html("Perfil produtivo da turma"), unsafe_allow_html=True)

col_h1, col_h2, col_h3 = st.columns(3)

def _hist_com_rotulos(serie, nbins, cor, titulo, xaxis_title):
    fig = px.histogram(serie, nbins=nbins, color_discrete_sequence=[cor], title=titulo)
    fig.update_layout(
        plot_bgcolor="white", paper_bgcolor="white",
        xaxis_title=xaxis_title, yaxis_title="Nº de alunos",
        margin=dict(l=10, r=10, t=40, b=10),
        font=dict(family="sans-serif", size=11),
        height=300, bargap=0.08,
        showlegend=False,
    )
    fig.update_traces(
        texttemplate="%{y}",
        textposition="outside",
        textfont=dict(size=12, color="#1C3829"),
        cliponaxis=False,
    )
    return fig

with col_h1:
    prod_df = df[df["nao_se_aplica_producao"] == 0]["producao_litros_dia"].dropna()
    if len(prod_df) > 0:
        st.plotly_chart(
            _hist_com_rotulos(prod_df, 8, RH_GOLD,
                              "Produção diária (litros/dia)", "Litros/dia"),
            use_container_width=True,
        )
    else:
        st.info("Sem dados de produção")

with col_h2:
    anim_df = df[df["nao_se_aplica_animais"] == 0]["animais_lactacao"].dropna()
    if len(anim_df) > 0:
        st.plotly_chart(
            _hist_com_rotulos(anim_df, 6, RH_GREEN,
                              "Animais em lactação", "Nº de vacas"),
            use_container_width=True,
        )
    else:
        st.info("Sem dados de animais")

with col_h3:
    med_df = df[df["nao_se_aplica_media"] == 0]["media_vaca_dia"].dropna()
    if len(med_df) > 0:
        st.plotly_chart(
            _hist_com_rotulos(med_df, 6, "#4A7C5E",
                              "Média por vaca (L/vaca/dia)", "Litros/vaca/dia"),
            use_container_width=True,
        )
    else:
        st.info("Sem dados de média")

st.divider()

# ─────────────────────────────────────────────────────────────────────────
#  GRÁFICO 3 — Perfil da turma: cargo, formação, estado
# ─────────────────────────────────────────────────────────────────────────
st.markdown(section_tag_html("Perfil da turma"), unsafe_allow_html=True)

col_p1, col_p2, col_p3 = st.columns(3)

with col_p1:
    cargo_c = df["cargo"].dropna().value_counts()
    fig_cargo = px.pie(
        values=cargo_c.values, names=cargo_c.index,
        title="Cargo / papel",
        color_discrete_sequence=[RH_GREEN, RH_GOLD, "#4A7C5E", "#D4B96C", "#6B9E7C"],
        hole=0.4,
    )
    fig_cargo.update_layout(
        plot_bgcolor="white", paper_bgcolor="white",
        margin=dict(l=0, r=0, t=40, b=0),
        font=dict(family="sans-serif", size=11),
        legend=dict(font=dict(size=10)),
        height=300,
    )
    fig_cargo.update_traces(
        textinfo="value+percent",
        textfont=dict(size=11, color="white"),
        textposition="inside",
    )
    st.plotly_chart(fig_cargo, use_container_width=True)

with col_p2:
    form_c = df["formacao"].dropna().value_counts()
    form_labels = [f[:30] + "…" if len(f) > 30 else f for f in form_c.index]
    fig_form = px.bar(
        x=form_c.values, y=form_labels,
        orientation="h",
        title="Formação",
        text=form_c.values,
        color_discrete_sequence=[RH_GOLD],
    )
    fig_form.update_layout(
        plot_bgcolor="white", paper_bgcolor="white",
        margin=dict(l=0, r=30, t=40, b=0),
        xaxis_title="", yaxis_title="",
        font=dict(family="sans-serif", size=11),
        height=300,
    )
    fig_form.update_traces(
        textposition="outside",
        textfont=dict(size=12, color="#1C3829"),
        cliponaxis=False,
    )
    st.plotly_chart(fig_form, use_container_width=True)

with col_p3:
    estado_c = df["estado"].dropna().value_counts().head(8)
    fig_estado = px.bar(
        x=estado_c.values, y=estado_c.index,
        orientation="h",
        title="Estados (top 8)",
        text=estado_c.values,
        color_discrete_sequence=[RH_GREEN],
    )
    fig_estado.update_layout(
        plot_bgcolor="white", paper_bgcolor="white",
        margin=dict(l=0, r=30, t=40, b=0),
        xaxis_title="", yaxis_title="",
        font=dict(family="sans-serif", size=11),
        height=300,
    )
    fig_estado.update_traces(
        textposition="outside",
        textfont=dict(size=12, color="#1C3829"),
        cliponaxis=False,
    )
    st.plotly_chart(fig_estado, use_container_width=True)

st.divider()

# ─────────────────────────────────────────────────────────────────────────
#  TABELA — Respostas detalhadas
# ─────────────────────────────────────────────────────────────────────────
st.markdown(section_tag_html("Respostas detalhadas"), unsafe_allow_html=True)

df_exib = df[[
    "nome", "turma_id", "estado", "cargo",
    "producao_litros_dia", "animais_lactacao", "media_vaca_dia",
    "prioridade_1", "prioridade_2", "prioridade_3",
    "plano_gerado", "criado_em",
]].copy()

df_exib["prioridade_1"] = df_exib["prioridade_1"].map(lambda x: dor_map.get(x, x))
df_exib["prioridade_2"] = df_exib["prioridade_2"].map(lambda x: dor_map.get(x, x))
df_exib["prioridade_3"] = df_exib["prioridade_3"].map(lambda x: dor_map.get(x, x))
df_exib["plano_gerado"] = df_exib["plano_gerado"].map({0: "⏳", 1: "✅"})

df_exib.columns = [
    "Nome", "Turma", "Estado", "Cargo",
    "Prod. L/dia", "Animais", "Média/vaca",
    "1ª Prioridade", "2ª Prioridade", "3ª Prioridade",
    "Plano", "Respondido em",
]

st.dataframe(df_exib, use_container_width=True, hide_index=True)

# Exportar CSV
csv = df_exib.to_csv(index=False).encode("utf-8-sig")
st.download_button(
    "⬇️ Exportar CSV",
    data=csv,
    file_name=f"respostas_gpl_{turma_sel.replace(' ','_')}.csv",
    mime="text/csv",
)
