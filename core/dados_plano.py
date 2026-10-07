"""
Transforma o registro do aluno (vindo de core.hubspot_csv) no contrato de
dados que o template do plano de aula espera (ver design_handoff_plano_de_aula
/template/dados_exemplo.json).
"""
from datetime import datetime
from urllib.parse import quote

from core.mapeamento import (
    MODULO_BOASVINDAS,
    PLATAFORMA_PADRAO,
    link_boas_vindas,
    link_modulo,
    plataforma_valida,
)

# WhatsApp do time de Sucesso do Cliente (formato internacional, só dígitos).
# Abre a conversa já com uma mensagem pronta que o aluno só envia.
_WHATSAPP_NUMERO = "5531991476763"
_WHATSAPP_MENSAGEM = (
    "Olá! Sou aluno do curso e gostaria de falar com a "
    "Equipe de Sucesso do Cliente do Rehagro."
)
_WHATSAPP_URL = f"https://wa.me/{_WHATSAPP_NUMERO}?text={quote(_WHATSAPP_MENSAGEM)}"

_BOAS_VINDAS_DESC = (
    "Para iniciar, veja como funciona o curso e os critérios que garantem sua aprovação."
)

_ENCERRAMENTO = {
    "mensagem": (
        "Conte com a gente sempre que precisar — pra você aproveitar ao máximo o curso "
        "e levar o resultado para sua fazenda. 🌱"
    ),
    "equipe": "Equipe de Sucesso do Cliente",
    "organizacao": "Rehagro",
    "whatsapp_url": _WHATSAPP_URL,
}


def _fmt_tempo(tempo) -> str:
    """Formata o tempo de aula como no design (ex.: '3,5h' -> '~3,5h')."""
    if not tempo:
        return "—"
    t = str(tempo).strip()
    return t if t.startswith("~") else f"~{t}"


def _modulo_para_template(dor: dict, plataforma: str) -> dict:
    return {
        "titulo": dor.get("modulo", "—"),
        # Subtítulo do card = a dor que o aluno apontou (redação de exibição do
        # arquivo 3; cai para "dor" se não houver versão de exibição).
        "descricao": dor.get("dor_exibicao") or dor.get("dor", ""),
        # O link muda conforme a plataforma em que o aluno tem acesso.
        "url": link_modulo(dor, plataforma),
        "qtd_aulas": str(dor["aulas"]) if dor.get("aulas") else "—",
        "tempo_aula": _fmt_tempo(dor.get("tempo")),
        "atividades": dor.get("atividades") or "—",
        "programacao": dor.get("programacao") or "—",
    }


def montar_dados(
    registro: dict,
    data_geracao: str | None = None,
    plataforma: str | None = PLATAFORMA_PADRAO,
) -> dict:
    """
    registro: dict de core.hubspot_csv.parse_hubspot_csv (tem 'nome', 'curso',
              'modulos' = lista de dores casadas).
    plataforma: 'studio' (turmas atuais) ou 'videoteca' (turmas antigas) —
              decide para qual turma do AVA os links do plano apontam.
    Retorna o dict pronto para o template Jinja2.
    """
    plataforma = plataforma_valida(plataforma)

    if data_geracao is None:
        data_geracao = datetime.now().strftime("%d/%m/%Y")

    modulos = registro.get("modulos", [])

    return {
        "data_geracao": data_geracao,
        "aluno": {"nome": registro.get("nome") or "Aluno"},
        "curso": {"nome": registro.get("curso") or ""},
        "boas_vindas": {
            "titulo": MODULO_BOASVINDAS.get("modulo", "Boas-vindas"),
            "descricao": _BOAS_VINDAS_DESC,
            "url": link_boas_vindas(plataforma),
        },
        "modulos": [_modulo_para_template(d, plataforma) for d in modulos],
        "encerramento": dict(_ENCERRAMENTO),
    }


# ──────────────────────────────────────────────────────────────────────────
#  Plano complementar — os módulos que ficaram fora das 3 prioridades, na
#  ordem que o CS define (calendário das aulas ao vivo ou o que ele conhece da
#  realidade do aluno). Mesmo template e mesmo visual; mudam os textos.
#  Os textos abaixo são a redação proposta — ajuste aqui, não no template.
# ──────────────────────────────────────────────────────────────────────────
_COMPLEMENTAR_TEXTOS = {
    "eyebrow": "Plano de Estudos Complementar",
    "intro": (
        "este é o seu plano de estudos complementar. Ele reúne os demais módulos do "
        "curso, além das 3 prioridades do seu primeiro plano, numa sequência montada "
        "pela nossa equipe a partir do calendário das aulas ao vivo e do que "
        "conhecemos da sua realidade."
    ),
    "intro_destaque": "Recomendamos que você assista os módulos na ordem abaixo.",
    "antes_titulo": "Antes de seguir",
    "antes_rotulo": "Seu primeiro plano",
    "antes_texto": (
        "Se ainda não concluiu os módulos do seu plano inicial, termine-os antes de "
        "começar esta sequência — eles são a base para o que vem a seguir."
    ),
    "trilha_titulo": "Sua sequência complementar",
}

_COMPLEMENTAR_ENCERRAMENTO_COMPLETO = (
    "Com esta sequência e o seu plano inicial, você percorre o curso completo. "
    "Conte com a gente sempre que precisar — pra você aproveitar ao máximo cada "
    "módulo e levar o resultado para sua fazenda. 🌱"
)


def _horas(tempo) -> float:
    """'2,5h' -> 2.5; vazio ou ilegível -> 0."""
    try:
        return float(str(tempo or "").strip().lstrip("~").rstrip("h").replace(",", "."))
    except ValueError:
        return 0.0


def _fmt_horas(h: float) -> str:
    return f"~{h:g}h".replace(".", ",")


def montar_dados_complementar(
    nome: str,
    curso: str,
    modulos: list[dict],
    plataforma: str | None = PLATAFORMA_PADRAO,
    modulos_anteriores: list[dict] | None = None,
    curso_completo: bool = False,
    data_geracao: str | None = None,
) -> dict:
    """
    modulos: dores de core.mapeamento.DORES já na ordem em que o aluno deve
             assistir.
    modulos_anteriores: as dores do primeiro plano (quando o aluno veio do
             CSV) — aparecem no bloco "Antes de seguir" só como referência.
    curso_completo: os dois planos juntos cobrem todos os módulos do curso;
             muda a mensagem de encerramento.
    """
    plataforma = plataforma_valida(plataforma)
    if data_geracao is None:
        data_geracao = datetime.now().strftime("%d/%m/%Y")

    total_aulas = sum(int(d.get("aulas") or 0) for d in modulos)
    total_horas = sum(_horas(d.get("tempo")) for d in modulos)
    qtd = len(modulos)
    resumo = (
        f"São {qtd} módulo{'s' if qtd != 1 else ''}, na ordem recomendada para você "
        f"assistir. Juntos, somam {total_aulas} videoaulas e "
        f"{_fmt_horas(total_horas)} de aula gravada."
    )

    encerramento = dict(_ENCERRAMENTO)
    if curso_completo:
        encerramento["mensagem"] = _COMPLEMENTAR_ENCERRAMENTO_COMPLETO

    return {
        "variante": "complementar",
        "textos": dict(_COMPLEMENTAR_TEXTOS, trilha_texto=resumo),
        "data_geracao": data_geracao,
        "aluno": {"nome": nome or "Aluno"},
        "curso": {"nome": curso or ""},
        "anteriores": [d.get("modulo", "") for d in (modulos_anteriores or [])],
        "modulos": [_modulo_para_template(d, plataforma) for d in modulos],
        "encerramento": encerramento,
    }
