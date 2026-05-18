"""
Página 1 — Pesquisa de Início de Jornada
Acesso público: aluno responde o questionário
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import streamlit as st
from core.database  import (
    inicializar_banco, salvar_resposta, cpf_ja_respondeu,
    get_turma_ativa, get_turma,
)
from core.mapeamento import get_lista_dores
from core.styles    import BASE_CSS, header_html, progress_html, section_tag_html
from config         import TURMA_ID, TURMA_NOME

st.set_page_config(
    page_title="Pesquisa de Início de Jornada — Rehagro GPL",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

inicializar_banco()
st.markdown(BASE_CSS, unsafe_allow_html=True)

# ── Resolução da turma ───────────────────────────────────────────────────
# 1) Se vier ?turma=ID na URL → usa essa (se existir no banco)
# 2) Senão → usa a turma marcada como ativa no banco
# 3) Fallback → config.py
params      = st.query_params
turma_param = params.get("turma")

if turma_param:
    t = get_turma(turma_param)
else:
    t = get_turma_ativa()

if t:
    turma_id   = t["turma_id"]
    turma_nome = t["turma_nome"]
else:
    turma_id   = TURMA_ID
    turma_nome = TURMA_NOME

# ── Estado da sessão ──────────────────────────────────────────────────────
defaults = {
    "etapa": 1,
    "nome": "", "cpf": "", "cidade": "", "estado": "",
    "producao": None, "na_producao": False,
    "animais": None,  "na_animais": False,
    "media": None,    "na_media": False,
    "cargo": "", "formacao": "",
    "valeu_a_pena": "", "meta": "",
    "p1": "", "p2": "", "p3": "",
    "enviado": False,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

DORES = get_lista_dores()
ESTADOS_BR = [
    "", "AC","AL","AP","AM","BA","CE","DF","ES","GO",
    "MA","MT","MS","MG","PA","PB","PR","PE","PI","RJ",
    "RN","RS","RO","RR","SC","SP","SE","TO",
]
CARGOS    = ["", "Dono / Sócio", "Consultor / Prestador de serviço",
             "Gerente", "Colaborador", "Sucessor"]
FORMACOES = [
    "", "Ensino fundamental completo/incompleto",
    "Ensino médio completo/incompleto",
    "Ensino superior completo/incompleto",
    "Pós-Graduação / Mestrado / Doutorado",
]

def _limpar_cpf(cpf: str) -> str:
    return "".join(c for c in cpf if c.isdigit())

def _validar_cpf_formato(cpf: str) -> bool:
    return len(_limpar_cpf(cpf)) == 11

def _formatar_cpf(cpf: str) -> str:
    raw = _limpar_cpf(cpf)[:11]
    if len(raw) <= 3:
        return raw
    if len(raw) <= 6:
        return f"{raw[:3]}.{raw[3:]}"
    if len(raw) <= 9:
        return f"{raw[:3]}.{raw[3:6]}.{raw[6:]}"
    return f"{raw[:3]}.{raw[3:6]}.{raw[6:9]}-{raw[9:]}"

def _aplicar_mascara_cpf():
    """Callback: aplica máscara 000.000.000-00 ao campo CPF."""
    st.session_state.cpf_input = _formatar_cpf(st.session_state.cpf_input)

# ─────────────────────────────────────────────────────────────────────────
#  TELA DE AGRADECIMENTO
# ─────────────────────────────────────────────────────────────────────────
if st.session_state.enviado:
    st.markdown(header_html(
        "Pesquisa de Início de Jornada",
        subtitulo="GPL Online",
    ), unsafe_allow_html=True)

    st.markdown("""
    <div class="rh-thanks">
        <div class="rh-thanks-icon">✅</div>
        <div class="rh-thanks-title">Recebemos suas respostas!</div>
        <div class="rh-thanks-sub">
            Obrigado por dedicar alguns minutos para compartilhar seus desafios
            com a gente.<br><br>
            Nosso time de <strong>Customer Success</strong> vai usar essas informações
            para criar o seu plano de aula personalizado. Você receberá em breve pelo
            WhatsApp ou e-mail.<br><br>
            Bons estudos e bom proveito do curso! 🌿
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ─────────────────────────────────────────────────────────────────────────
#  HEADER
# ─────────────────────────────────────────────────────────────────────────
st.markdown(header_html(
    "Pesquisa de Início de Jornada",
    subtitulo="GPL Online · Responda em menos de 5 minutos",
), unsafe_allow_html=True)

with st.container():
    col_l, col_form, col_r = st.columns([1, 4, 1])
    with col_form:
        etapa = st.session_state.etapa

        # ── Progress ───────────────────────────────────────────────────────
        pct    = {1: 15, 2: 45, 3: 75, 4: 95}.get(etapa, 15)
        labels = {
            1: "Bloco 1 de 4 — Identificação",
            2: "Bloco 2 de 4 — Contexto produtivo",
            3: "Bloco 3 de 4 — Objetivos",
            4: "Bloco 4 de 4 — Prioridades",
        }
        st.markdown(progress_html(pct, labels.get(etapa, "")), unsafe_allow_html=True)

        # ══════════════════════════════════════════════════════════════════
        #  ETAPA 1 — Identificação
        # ══════════════════════════════════════════════════════════════════
        if etapa == 1:
            st.markdown(section_tag_html("Identificação"), unsafe_allow_html=True)

            # Pré-preencher o campo CPF formatado (uma vez por sessão)
            if "cpf_input" not in st.session_state:
                st.session_state.cpf_input = (
                    _formatar_cpf(st.session_state.cpf) if st.session_state.cpf else ""
                )

            nome = st.text_input("Nome completo *", value=st.session_state.nome,
                                 placeholder="Ex: João da Silva")
            cpf  = st.text_input(
                "CPF *",
                key="cpf_input",
                placeholder="000.000.000-00",
                on_change=_aplicar_mascara_cpf,
                help="Digite os números — pontos e traço são aplicados automaticamente",
                max_chars=14,
            )
            col1, col2 = st.columns(2)
            with col1:
                cidade = st.text_input("Cidade *", value=st.session_state.cidade)
            with col2:
                estado = st.selectbox("Estado *", ESTADOS_BR,
                                      index=ESTADOS_BR.index(st.session_state.estado)
                                      if st.session_state.estado in ESTADOS_BR else 0)

            avancar = st.button("Próximo →", type="primary",
                                use_container_width=True, key="btn_etapa1")

            if avancar:
                erros = []
                if not nome.strip():       erros.append("Nome é obrigatório.")
                if not cpf.strip():        erros.append("CPF é obrigatório.")
                elif not _validar_cpf_formato(cpf):
                    erros.append("CPF inválido — deve ter 11 dígitos.")
                if not cidade.strip():     erros.append("Cidade é obrigatória.")
                if not estado:             erros.append("Selecione o estado.")

                if not erros:
                    cpf_limpo = _limpar_cpf(cpf)
                    if cpf_ja_respondeu(cpf_limpo, turma_id):
                        st.warning(
                            "⚠️ Este CPF já respondeu a pesquisa para esta turma. "
                            "Se achar que houve um erro, fale com o CS."
                        )
                    else:
                        st.session_state.nome   = nome.strip()
                        st.session_state.cpf    = cpf_limpo
                        st.session_state.cidade = cidade.strip()
                        st.session_state.estado = estado
                        st.session_state.etapa  = 2
                        st.rerun()
                else:
                    for e in erros:
                        st.error(e)

        # ══════════════════════════════════════════════════════════════════
        #  ETAPA 2 — Contexto produtivo
        # ══════════════════════════════════════════════════════════════════
        elif etapa == 2:
            st.markdown(section_tag_html("Contexto produtivo"), unsafe_allow_html=True)

            with st.form("form_prod"):
                st.markdown("**1. Volume de produção diária (litros/dia)**")
                st.caption("Média dos últimos 6 meses. Digite apenas números.")
                na_prod = st.checkbox("Não se aplica (não sou produtor)",
                                      value=st.session_state.na_producao,
                                      key="cb_prod")
                producao = None
                if not na_prod:
                    producao = st.number_input("Litros/dia", min_value=0.0,
                                               value=float(st.session_state.producao or 0),
                                               step=10.0, format="%.0f",
                                               label_visibility="collapsed")

                st.divider()
                st.markdown("**2. Número médio de animais em lactação**")
                st.caption("Média dos últimos 6 meses.")
                na_anim = st.checkbox("Não se aplica",
                                      value=st.session_state.na_animais, key="cb_anim")
                animais = None
                if not na_anim:
                    animais = st.number_input("Animais em lactação", min_value=0.0,
                                              value=float(st.session_state.animais or 0),
                                              step=1.0, format="%.0f",
                                              label_visibility="collapsed")

                st.divider()
                st.markdown("**3. Média de produção por vaca (litros/vaca/dia)**")
                na_med = st.checkbox("Não se aplica",
                                     value=st.session_state.na_media, key="cb_med")
                media = None
                if not na_med:
                    media = st.number_input("Litros/vaca/dia", min_value=0.0,
                                            value=float(st.session_state.media or 0),
                                            step=0.5, format="%.1f",
                                            label_visibility="collapsed")

                st.divider()
                cargo    = st.selectbox("4. Qual é o seu papel na propriedade? *",
                                        CARGOS,
                                        index=CARGOS.index(st.session_state.cargo)
                                        if st.session_state.cargo in CARGOS else 0)
                formacao = st.selectbox("5. Qual é a sua formação? *",
                                        FORMACOES,
                                        index=FORMACOES.index(st.session_state.formacao)
                                        if st.session_state.formacao in FORMACOES else 0)

                col_v, col_a = st.columns(2)
                with col_v:
                    voltar  = st.form_submit_button("← Voltar", type="secondary")
                with col_a:
                    avancar = st.form_submit_button("Próximo →", type="primary",
                                                    use_container_width=True)

                if voltar:
                    st.session_state.etapa = 1; st.rerun()

                if avancar:
                    erros = []
                    if not cargo:    erros.append("Selecione seu papel na propriedade.")
                    if not formacao: erros.append("Selecione sua formação.")

                    if not erros:
                        st.session_state.na_producao = na_prod
                        st.session_state.producao    = producao
                        st.session_state.na_animais  = na_anim
                        st.session_state.animais     = animais
                        st.session_state.na_media    = na_med
                        st.session_state.media       = media
                        st.session_state.cargo       = cargo
                        st.session_state.formacao    = formacao
                        st.session_state.etapa       = 3
                        st.rerun()
                    else:
                        for e in erros: st.error(e)

        # ══════════════════════════════════════════════════════════════════
        #  ETAPA 3 — Objetivos
        # ══════════════════════════════════════════════════════════════════
        elif etapa == 3:
            st.markdown(section_tag_html("Seus objetivos com o curso"), unsafe_allow_html=True)

            with st.form("form_obj"):
                st.markdown("**6. Ao final deste curso, o que faria você dizer que 'valeu a pena'?**")
                valeu = st.text_area(
                    "Resposta", value=st.session_state.valeu_a_pena,
                    placeholder="Descreva com suas palavras o que seria um resultado significativo para você...",
                    height=100, label_visibility="collapsed"
                )

                st.divider()
                st.markdown("**7. Pensando na sua fazenda hoje, para onde você gostaria de chegar nos próximos anos?**")
                st.caption("Pode mencionar produção total, média das vacas, número de vacas — o que for mais claro para você.")
                meta = st.text_area(
                    "Meta", value=st.session_state.meta,
                    placeholder="Ex: Quero chegar a 5.000 litros/dia com 100 vacas em lactação...",
                    height=100, label_visibility="collapsed"
                )

                col_v, col_a = st.columns(2)
                with col_v:
                    voltar  = st.form_submit_button("← Voltar", type="secondary")
                with col_a:
                    avancar = st.form_submit_button("Próximo →", type="primary",
                                                    use_container_width=True)

                if voltar:
                    st.session_state.etapa = 2; st.rerun()

                if avancar:
                    erros = []
                    if not valeu.strip(): erros.append("Conte o que faria valer a pena (questão 6).")
                    if not meta.strip():  erros.append("Descreva sua meta (questão 7).")

                    if not erros:
                        st.session_state.valeu_a_pena = valeu.strip()
                        st.session_state.meta         = meta.strip()
                        st.session_state.etapa        = 4
                        st.rerun()
                    else:
                        for e in erros: st.error(e)

        # ══════════════════════════════════════════════════════════════════
        #  ETAPA 4 — Prioridades (ranqueadas)
        # ══════════════════════════════════════════════════════════════════
        elif etapa == 4:
            st.markdown(section_tag_html("Suas 3 principais prioridades"), unsafe_allow_html=True)

            st.markdown(
                '<div class="rh-warning">Escolha as <strong>3 prioridades</strong>, '
                'em ordem de importância, que você considera mais urgentes para serem '
                'melhoradas/trabalhadas na(s) propriedade(s) que atua/irá atuar. '
                'Cada dor só pode aparecer uma vez.</div>',
                unsafe_allow_html=True,
            )

            with st.form("form_prio"):
                opcoes_base = ["— Selecione —"] + DORES

                p1 = st.selectbox(
                    "🥇 1ª prioridade — mais urgente hoje na sua fazenda",
                    opcoes_base,
                    index=opcoes_base.index(st.session_state.p1)
                    if st.session_state.p1 in opcoes_base else 0,
                )
                p2 = st.selectbox(
                    "🥈 2ª prioridade",
                    opcoes_base,
                    index=opcoes_base.index(st.session_state.p2)
                    if st.session_state.p2 in opcoes_base else 0,
                )
                p3 = st.selectbox(
                    "🥉 3ª prioridade",
                    opcoes_base,
                    index=opcoes_base.index(st.session_state.p3)
                    if st.session_state.p3 in opcoes_base else 0,
                )

                st.divider()
                st.markdown(
                    "<small style='color:#6B6B5E'>Ao clicar em <strong>Enviar</strong>, "
                    "suas respostas serão registradas e não poderão ser alteradas.</small>",
                    unsafe_allow_html=True,
                )

                col_v, col_a = st.columns(2)
                with col_v:
                    voltar = st.form_submit_button("← Voltar", type="secondary")
                with col_a:
                    enviar = st.form_submit_button("Enviar pesquisa ✓", type="primary",
                                                   use_container_width=True)

                if voltar:
                    st.session_state.etapa = 3; st.rerun()

                if enviar:
                    erros = []
                    selecionadas = [p1, p2, p3]

                    for i, p in enumerate(selecionadas, 1):
                        if p == "— Selecione —":
                            erros.append(f"Selecione a {i}ª prioridade.")

                    sel_validas = [p for p in selecionadas if p != "— Selecione —"]
                    if len(sel_validas) != len(set(sel_validas)):
                        erros.append("As 3 prioridades devem ser diferentes entre si.")

                    if not erros:
                        from core.mapeamento import dor_texto_para_id
                        dados = {
                            "turma_id":   turma_id,
                            "turma_nome": turma_nome,
                            "nome":       st.session_state.nome,
                            "cpf":        st.session_state.cpf,
                            "cidade":     st.session_state.cidade,
                            "estado":     st.session_state.estado,
                            "producao_litros_dia":    st.session_state.producao,
                            "nao_se_aplica_producao": int(st.session_state.na_producao),
                            "animais_lactacao":       st.session_state.animais,
                            "nao_se_aplica_animais":  int(st.session_state.na_animais),
                            "media_vaca_dia":         st.session_state.media,
                            "nao_se_aplica_media":    int(st.session_state.na_media),
                            "cargo":      st.session_state.cargo,
                            "formacao":   st.session_state.formacao,
                            "valeu_a_pena": st.session_state.valeu_a_pena,
                            "meta_fazenda": st.session_state.meta,
                            "prioridade_1": dor_texto_para_id(p1),
                            "prioridade_2": dor_texto_para_id(p2),
                            "prioridade_3": dor_texto_para_id(p3),
                        }
                        salvar_resposta(dados)
                        st.session_state.p1 = p1
                        st.session_state.p2 = p2
                        st.session_state.p3 = p3
                        st.session_state.enviado = True
                        st.rerun()
                    else:
                        for e in erros: st.error(e)
