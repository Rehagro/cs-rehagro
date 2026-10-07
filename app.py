"""
CS Rehagro — Gerador de Plano de Aula a partir do CSV do HubSpot Survey.

Duas telas (uso interno do time CS), no design Rehagro:
    1. Login (senha CS)
    2. Gerador, em duas abas:
       - Plano inicial: plataforma do aluno → upload do CSV → seleção do
         aluno → plano com as 3 prioridades;
       - Plano complementar: plataforma → aluno → o CS escolhe e ordena os
         demais módulos → plano com a sequência dele.
       Em ambas o CS baixa o HTML e salva como PDF pelo navegador.
"""
import os
import sys

import streamlit as st
import streamlit.components.v1 as components

sys.path.insert(0, os.path.dirname(__file__))
from core.hubspot_csv import colunas_reconhecidas, parse_hubspot_csv
from core.dados_plano import montar_dados, montar_dados_complementar
from core.render_plano import render_html
from core.mapeamento import DORES, PLATAFORMAS, get_plataforma, link_boas_vindas
from core.styles import (
    BRAND_CSS,
    aviso_plataforma_html,
    card_prioridade_html,
    masthead_html,
    step_html,
)
from core.validacao import diagnosticar_aluno, diagnosticar_arquivo
from config import CS_PASSWORD

st.set_page_config(
    page_title="Gerador de Plano de Estudos · Rehagro",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="collapsed",
)
st.markdown(BRAND_CSS, unsafe_allow_html=True)


def _slug(nome: str) -> str:
    return "".join(c if c.isalnum() else "_" for c in (nome or "aluno")).strip("_")


def _mostrar_diagnostico(diag: dict) -> None:
    """Resumo do que o sistema achou (e não achou) no CSV, antes de gerar nada."""
    for msg in diag["bloqueios"]:
        st.error(msg)
    for msg in diag["avisos"]:
        st.warning(msg)

    if not diag["bloqueios"] and not diag["avisos"]:
        st.success(
            f"{diag['total']} aluno(s) carregado(s) — todos os dados necessários "
            "para o plano vieram no arquivo."
        )
    else:
        st.caption(f"{diag['total']} aluno(s) lidos do arquivo.")

    tem_problema = bool(diag["bloqueios"] or diag["avisos"])
    rotulo = "🔎 Detalhar o que está inconsistente" if tem_problema else "🔎 Ver o que o sistema encontrou no arquivo"

    with st.expander(rotulo, expanded=bool(diag["bloqueios"])):
        if diag["dores_divergentes"]:
            st.markdown("**Respostas de prioridade que não casaram com nenhum módulo**")
            for texto, qtd in diag["dores_divergentes"]:
                st.markdown(f"- “{texto}” — {qtd} aluno(s)")
            st.info(
                "Se a redação da opção mudou no HubSpot, acrescente o texto novo em "
                "`variantes`, na dor correspondente de `core/mapeamento.py`. A redação "
                "antiga continua valendo — nenhuma turma anterior quebra."
            )

        if diag["alunos_sem_trilha"]:
            st.markdown("**Alunos cujas respostas não casaram com nenhum módulo**")
            st.markdown("\n".join(f"- {n}" for n in diag["alunos_sem_trilha"]))

        if diag.get("alunos_sem_resposta"):
            st.markdown("**Alunos que não responderam as prioridades**")
            st.markdown("\n".join(f"- {n}" for n in diag["alunos_sem_resposta"]))

        if diag["alunos_incompletos"]:
            st.markdown("**Alunos com menos de 3 módulos**")
            st.markdown("\n".join(f"- {n} — {q} módulo(s)" for n, q in diag["alunos_incompletos"]))

        for msg in diag["info"]:
            st.caption(msg)

        st.markdown("**Colunas reconhecidas no CSV**")
        st.markdown(
            "\n".join(f"- `{c}` ← {h}" for c, h in diag["colunas"].items())
            or "- _nenhuma coluna reconhecida_"
        )



def _como_salvar_pdf(rotulo_botao: str) -> None:
    """Passo a passo de HTML → PDF (o Cloud não tem Chromium para gerar direto)."""
    st.markdown(
        f"""
        <div style="background:#FBFAF6; border:1px solid #E7E1D3; border-left:4px solid #C49A45;
             border-radius:12px; padding:14px 18px; margin-top:6px;">
          <div style="font-family:'Poppins',sans-serif; font-weight:600; font-size:13px;
               color:#0F4630; margin-bottom:8px;">📄 Como salvar o plano em PDF</div>
          <ol style="margin:0; padding-left:18px; color:#5A6B61; font-size:13px; line-height:1.75;">
            <li>Clique em <strong style="color:#0F4630;">{rotulo_botao}</strong>
                (baixa um arquivo <code>.html</code>).</li>
            <li>Abra o arquivo baixado — ele abre no seu navegador.</li>
            <li>Pressione <strong style="color:#0F4630;">Ctrl + P</strong>
                (no Mac, <strong style="color:#0F4630;">⌘ + P</strong>).</li>
            <li>Em <em>Destino / Impressora</em>, escolha
                <strong style="color:#0F4630;">Salvar como PDF</strong>.</li>
            <li>Clique em <strong style="color:#0F4630;">Salvar</strong>.
                Esse PDF é o que você envia ao aluno. ✅</li>
          </ol>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _escolher_plataforma(key: str) -> str:
    st.markdown(step_html(1, "Plataforma em que o aluno acessa as aulas"), unsafe_allow_html=True)
    plataforma = st.radio(
        "Plataforma",
        options=[p["id"] for p in PLATAFORMAS],
        captions=[p["descricao"] for p in PLATAFORMAS],
        format_func=lambda pid: get_plataforma(pid)["rotulo"],
        horizontal=True,
        label_visibility="collapsed",
        key=key,
    )
    st.caption(
        "Na dúvida, confira no Instructure por qual turma o aluno está matriculado — "
        "um link da plataforma errada abre uma página sem acesso para ele."
    )
    return plataforma


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
        masthead_html(
            "Gere o plano inicial (3 prioridades do CSV do HubSpot) ou o plano "
            "complementar (demais módulos, na ordem que você definir) no design Rehagro."
        ),
        unsafe_allow_html=True,
    )
    st.write("")

    aba_ini, aba_comp = st.tabs(
        ["🎯  Plano inicial — 3 prioridades", "🧭  Plano complementar — demais módulos"]
    )
    # Cada aba é uma função que só *retorna* quando falta algo: um st.stop()
    # numa aba interromperia a renderização da outra.
    with aba_ini:
        aba_inicial()
    with aba_comp:
        aba_complementar()


def aba_inicial():
    # ── Etapa 1 — Plataforma ──────────────────────────────────────────────
    # Os módulos existem em duas turmas do AVA (ids diferentes). Quem se
    # matriculou antes da republicação só acessa pela Videoteca; quem entrou
    # depois, pelo Studio. O plano precisa sair com os links certos.
    plataforma = _escolher_plataforma("plataforma")
    info_plataforma = get_plataforma(plataforma)
    st.divider()

    # ── Etapa 2 — CSV ─────────────────────────────────────────────────────
    st.markdown(step_html(2, "Arquivo CSV exportado do HubSpot Survey"), unsafe_allow_html=True)
    arquivo = st.file_uploader(
        "CSV", type=["csv"], label_visibility="collapsed",
        help="Exporte as respostas da pesquisa de início de curso no HubSpot e suba aqui.",
    )

    if not arquivo:
        return

    try:
        alunos = parse_hubspot_csv(arquivo.getvalue())
    except Exception as e:
        st.error(f"Não consegui ler o CSV: {e}")
        return

    if not alunos:
        st.warning("O CSV foi lido, mas nenhum aluno foi encontrado. Confira o arquivo.")
        return

    diag = diagnosticar_arquivo(alunos, colunas_reconhecidas(arquivo.getvalue()))
    _mostrar_diagnostico(diag)
    st.divider()

    # ── Etapa 3 — Aluno ───────────────────────────────────────────────────
    st.markdown(step_html(3, "Selecione o aluno"), unsafe_allow_html=True)
    idx = st.selectbox(
        "Aluno", range(len(alunos)), label_visibility="collapsed",
        format_func=lambda i: (
            f"{i + 1}. {alunos[i].get('nome') or 'Sem nome'}"
            f"{'  ·  ' + alunos[i]['curso'] if alunos[i].get('curso') else ''}"
        ),
    )
    aluno = alunos[idx]
    modulos = aluno.get("modulos", [])

    if modulos:
        cols = st.columns(len(modulos), gap="medium")
        for i, (c, m) in enumerate(zip(cols, modulos), start=1):
            c.markdown(
                card_prioridade_html(i, m["modulo"], m.get("aulas"), m.get("tempo")),
                unsafe_allow_html=True,
            )

    bloqueios_aluno, avisos_aluno = diagnosticar_aluno(aluno)
    if bloqueios_aluno:
        st.error(
            "**Não dá para gerar o plano deste aluno:**\n\n"
            + "\n".join(f"- {b}" for b in bloqueios_aluno)
        )
    if avisos_aluno:
        st.warning(
            "**Atenção neste aluno:**\n\n" + "\n".join(f"- {a}" for a in avisos_aluno)
        )

    st.divider()

    # ── Etapa 4 — Baixar e enviar ─────────────────────────────────────────
    st.markdown(step_html(4, "Baixe o plano e envie ao aluno"), unsafe_allow_html=True)
    st.markdown(
        aviso_plataforma_html(
            info_plataforma["rotulo"],
            info_plataforma["resumo"],
            link_boas_vindas(plataforma),
        ),
        unsafe_allow_html=True,
    )

    pode_gerar = bool(modulos) and not bloqueios_aluno
    html = render_html(montar_dados(aluno, plataforma=plataforma)) if pode_gerar else ""
    # A plataforma entra no nome do arquivo: se o mesmo aluno for gerado nas
    # duas, um download não sobrescreve o outro na pasta do CS.
    nome_base = (
        f"Plano_de_Estudos_{_slug(aluno.get('nome'))}_{_slug(info_plataforma['rotulo'])}"
    )

    st.download_button(
        "⬇  Baixar plano de estudos",
        data=html.encode("utf-8"),
        file_name=f"{nome_base}.html",
        mime="text/html",
        use_container_width=True,
        disabled=not pode_gerar,
    )
    _como_salvar_pdf("Baixar plano de estudos")

    if pode_gerar:
        with st.expander("👁  Pré-visualizar o plano"):
            components.html(html, height=900, scrolling=True)


# O plano inicial leva 3 dos 9 módulos; o complementar, no máximo os outros 6.
_COMP_POSICOES = len(DORES) - 3


def _limpar_posicoes_comp():
    for i in range(_COMP_POSICOES):
        st.session_state[f"comp_pos_{i}"] = "—"


def aba_complementar():
    """Plano com os módulos que ficaram fora das 3 prioridades, para o aluno que
    pede o curso completo. O CS escolhe quais entram e em que ordem (calendário
    das aulas ao vivo ou o que ele conhece da realidade do aluno)."""
    st.caption(
        "Para o aluno que pediu o plano completo: escolha os módulos que faltam e a "
        "ordem em que ele deve assistir. O PDF sai com o mesmo visual do plano inicial."
    )

    # ── Etapa 1 — Plataforma ──────────────────────────────────────────────
    plataforma = _escolher_plataforma("plataforma_comp")
    info_plataforma = get_plataforma(plataforma)
    st.divider()

    # ── Etapa 2 — Aluno ───────────────────────────────────────────────────
    st.markdown(step_html(2, "Aluno"), unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    nome = c1.text_input("Nome do aluno", key="comp_nome").strip()
    curso = c2.text_input("Curso", key="comp_curso").strip()
    st.divider()

    # ── Etapa 3 — Módulos e sequência ─────────────────────────────────────
    # O gerador não sabe quais módulos foram no plano inicial (o aluno é
    # digitado, não vem do CSV) — quem confere é o CS, antes de escolher a ordem.
    st.markdown(step_html(3, "Módulos e sequência"), unsafe_allow_html=True)
    st.warning(
        "**Antes de escolher a ordem, confira quais 3 módulos já foram enviados no plano "
        "inicial deste aluno** e deixe-os de fora: o plano complementar deve trazer "
        "só os módulos que ele ainda não recebeu."
    )
    st.caption(
        f"Escolha o módulo de cada posição (1º = o primeiro a assistir), até "
        f"{_COMP_POSICOES}. Para trocar, escolha outro módulo na posição; para tirar, "
        "volte para **—**; para reordenar, troque os módulos de posição."
    )
    # Uma caixa por posição, em vez de uma posição por módulo: o plano tem no
    # máximo 6 (os 9 do curso menos os 3 do plano inicial) e cada caixa pode
    # ser trocada ou zerada a qualquer momento.
    fora = "—"
    por_nome = {d["modulo"]: d for d in DORES}
    opcoes = [fora, *por_nome]
    st.button("Limpar escolhas", key="comp_limpar", on_click=_limpar_posicoes_comp)
    cols = st.columns(3, gap="medium")
    escolhas = [
        cols[i % 3].selectbox(f"{i + 1}º módulo", opcoes, key=f"comp_pos_{i}")
        for i in range(_COMP_POSICOES)
    ]

    nomes = [e for e in escolhas if e != fora]
    repetidos = sorted({n for n in nomes if nomes.count(n) > 1})
    # Posição vazia no meio não deixa buraco: a sequência só segue a ordem
    # das caixas preenchidas.
    sequencia = [por_nome[n] for n in nomes]

    bloqueios = []
    if not nome:
        bloqueios.append("Falta o nome do aluno.")
    if not sequencia:
        bloqueios.append("Nenhum módulo escolhido.")
    if repetidos:
        bloqueios.append(
            "Módulo repetido: " + "; ".join(repetidos)
            + ". Cada módulo entra em uma posição só."
        )
    avisos = []
    if not curso:
        avisos.append("Curso em branco — a capa do plano sai sem o nome do curso.")

    if sequencia and not repetidos:
        por_linha = 3
        for i in range(0, len(sequencia), por_linha):
            cols = st.columns(por_linha, gap="medium")
            for c, (n, d) in zip(cols, enumerate(sequencia[i:i + por_linha], start=i + 1)):
                c.markdown(
                    card_prioridade_html(
                        n, d["modulo"], d.get("aulas"), d.get("tempo"),
                        rotulo=f"{n}º da sequência",
                    ),
                    unsafe_allow_html=True,
                )
            st.write("")

    if bloqueios:
        st.error(
            "**Ainda não dá para gerar o plano:**\n\n"
            + "\n".join(f"- {b}" for b in bloqueios)
        )
    if avisos:
        st.warning("**Atenção:**\n\n" + "\n".join(f"- {a}" for a in avisos))
    st.divider()

    # ── Etapa 4 — Baixar e enviar ─────────────────────────────────────────
    st.markdown(
        step_html(4, "Baixe o plano complementar e envie ao aluno"), unsafe_allow_html=True
    )
    st.markdown(
        aviso_plataforma_html(
            info_plataforma["rotulo"],
            info_plataforma["resumo"],
            link_boas_vindas(plataforma),
        ),
        unsafe_allow_html=True,
    )

    pode_gerar = not bloqueios
    # "Curso completo" muda o encerramento. A orientação do CS é incluir todos
    # os módulos fora das 3 prioridades; com isso, os dois planos juntos cobrem
    # o curso inteiro.
    curso_completo = len(sequencia) >= _COMP_POSICOES
    html = render_html(
        montar_dados_complementar(
            nome, curso, sequencia,
            plataforma=plataforma,
            curso_completo=curso_completo,
        )
    ) if pode_gerar else ""
    nome_base = f"Plano_Complementar_{_slug(nome)}_{_slug(info_plataforma['rotulo'])}"

    st.download_button(
        "⬇  Baixar plano complementar",
        data=html.encode("utf-8"),
        file_name=f"{nome_base}.html",
        mime="text/html",
        use_container_width=True,
        disabled=not pode_gerar,
        key="comp_download",
    )
    _como_salvar_pdf("Baixar plano complementar")

    if pode_gerar:
        with st.expander("👁  Pré-visualizar o plano complementar"):
            components.html(html, height=900, scrolling=True)


# ──────────────────────────────────────────────────────────────────────────
if "cs_auth" not in st.session_state:
    st.session_state.cs_auth = False

if not st.session_state.cs_auth:
    tela_login()
else:
    tela_gerador()
