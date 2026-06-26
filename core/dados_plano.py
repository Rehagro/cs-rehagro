"""
Transforma o registro do aluno (vindo de core.hubspot_csv) no contrato de
dados que o template do plano de aula espera (ver design_handoff_plano_de_aula
/template/dados_exemplo.json).
"""
from datetime import datetime
from urllib.parse import quote

from core.mapeamento import MODULO_BOASVINDAS

# WhatsApp do time de Sucesso do Cliente (formato internacional, só dígitos).
# Abre a conversa já com uma mensagem pronta que o aluno só envia.
_WHATSAPP_NUMERO = "5531991476763"
_WHATSAPP_MENSAGEM = (
    "Olá! Sou aluno do curso e gostaria de falar com a "
    "Equipe de Sucesso do Cliente do Rehagro."
)
_WHATSAPP_URL = f"https://wa.me/{_WHATSAPP_NUMERO}?text={quote(_WHATSAPP_MENSAGEM)}"

# Descrição de cada módulo conforme a posição na trilha (1ª, 2ª, 3ª…).
_INTROS = [
    "Responde ao desafio que você apontou como mais urgente. Por isso vem primeiro.",
    "Ao concluir o módulo anterior, siga para o segundo desafio que você indicou.",
    "Fecha sua trilha com o terceiro ponto que você destacou.",
]
_INTRO_EXTRA = "Continue sua trilha com este módulo."

_BOAS_VINDAS_DESC = (
    "Comece por aqui: veja como o curso funciona e o que garante sua aprovação "
    "(a entrega das atividades)."
)

_ENCERRAMENTO = {
    "mensagem": (
        "Conte com a gente sempre que precisar — pra você tirar o máximo do curso "
        "e levar resultado pra sua fazenda. 🌱"
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


def _modulo_para_template(dor: dict, indice: int) -> dict:
    return {
        "titulo": dor.get("modulo", "—"),
        "descricao": _INTROS[indice] if indice < len(_INTROS) else _INTRO_EXTRA,
        "url": dor.get("link", ""),
        "qtd_aulas": str(dor["aulas"]) if dor.get("aulas") else "—",
        "tempo_aula": _fmt_tempo(dor.get("tempo")),
        "atividades": dor.get("atividades") or "—",
        "programacao": dor.get("programacao") or "—",
    }


def montar_dados(registro: dict, data_geracao: str | None = None) -> dict:
    """
    registro: dict de core.hubspot_csv.parse_hubspot_csv (tem 'nome', 'curso',
              'modulos' = lista de dores casadas).
    Retorna o dict pronto para o template Jinja2.
    """
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
            "url": MODULO_BOASVINDAS.get("link", ""),
        },
        "modulos": [_modulo_para_template(d, i) for i, d in enumerate(modulos)],
        "encerramento": dict(_ENCERRAMENTO),
    }
