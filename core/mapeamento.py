# ─────────────────────────────────────────
#  Mapeamento: Dor do aluno → Módulo GPL
#  - "dor": texto que CASA com o CSV do HubSpot (redação do "DOR DO ALUNO
#    v2.docx"). NÃO alterar sem alinhar com o HubSpot Survey, senão o
#    casamento quebra.
#  - "variantes": outras redações da MESMA dor que já circularam/circulam no
#    formulário. O casamento aceita "dor" ou qualquer variante, então mudar a
#    redação no HubSpot não derruba o gerador — basta acrescentar aqui.
#  - "dor_exibicao": texto MOSTRADO no card do plano (redação oficial do
#    "Plano de aula - arquivo 3 CEIGPL.docx").
#  - "links": o MESMO módulo em cada plataforma do AVA (ver PLATAFORMAS
#    abaixo). O plano sai com o link da plataforma escolhida no gerador.
# ─────────────────────────────────────────
import unicodedata

# ─────────────────────────────────────────
#  Plataformas do AVA (Instructure)
#  Os 10 módulos do GPL foram republicados: cada um existe hoje em duas
#  turmas, com course_id diferente. Quem se matriculou antes da republicação
#  continua com acesso apenas pela turma antiga (Videoteca), e quem entrou
#  depois só enxerga a nova (Studio) — por isso o plano precisa sair com os
#  links da plataforma de cada aluno.
#  Ordem desta lista = ordem dos botões no gerador; a primeira é o padrão.
# ─────────────────────────────────────────
PLATAFORMAS = [
    {
        "id": "studio",
        "rotulo": "Studio",
        "descricao": "Alunos que entraram depois da republicação dos módulos",
        "resumo": "turmas atuais (courses/31xx)",
    },
    {
        "id": "videoteca",
        "rotulo": "Videoteca",
        "descricao": "Alunos que já estavam matriculados antes da republicação",
        "resumo": "turmas antigas (courses/28xx)",
    },
]

PLATAFORMA_PADRAO = PLATAFORMAS[0]["id"]

_BASE_AVA = "https://rehagro.instructure.com/courses"


def _url(course_id: str) -> str:
    return f"{_BASE_AVA}/{course_id}"


DORES = [
    {
        "id": "sistemas_producao",
        "variantes": [
            "Definir o melhor sistema de produção, instalações e raças mais adequados para a minha realidade.",
        ],
        "dor": "Definir o melhor sistema de produção, instalações e raças para a minha realidade.",
        "dor_exibicao": "Definir o melhor sistema de produção, instalações e raças para a minha realidade",
        "dor_curta": "Sistema de produção e instalações",
        "modulo": "Sistemas de produção e visão estratégica do negócio leite",
        "links": {
            "studio": _url("3142"),
            "videoteca": _url("2852"),
        },
        "aulas": 16,
        "tempo": "2,5h",
        "programacao": "3 semanas (1h por semana – 5 videoaulas por semana)",
        "atividades": "Teste seu conhecimento (obrigatório para a aprovação) e Atividade prática (extra)",
    },
    {
        "id": "eficiencia_produtiva",
        "variantes": [
            "Reduzir doenças pós-parto, estabelecer melhores estratégias para emprenhar vacas rapidamente.",
        ],
        "dor": "Reduzir doenças pós-parto, estabelecer estratégias para emprenhar vacas rapidamente.",
        "dor_exibicao": "Reduzir doenças pós-parto, estabelecer estratégias para emprenhar vacas rapidamente",
        "dor_curta": "Reprodução e eficiência produtiva",
        "modulo": "Estratégias para eficiência produtiva",
        "links": {
            "studio": _url("3135"),
            "videoteca": _url("2854"),
        },
        "aulas": 21,
        "tempo": "3,5h",
        "programacao": "3 semanas (1h por semana – 7 videoaulas por semana)",
        "atividades": "Teste seu conhecimento (obrigatório para a aprovação) e Atividade prática (extra)",
    },
    {
        "id": "gestao_financeira",
        "variantes": [
            "Organizar os gastos da fazenda, saber o custo do litro de leite e buscar oportunidades para reduzir custos.",
        ],
        "dor": "Organizar os gastos, saber o custo do litro de leite para atuar no aumento do lucro.",
        "dor_exibicao": "Organizar os gastos, saber o custo do litro de leite para atuar no aumento do lucro",
        "dor_curta": "Gestão financeira e custos",
        "modulo": "Gestão financeira e econômica",
        "links": {
            "studio": _url("3136"),
            "videoteca": _url("2859"),
        },
        "aulas": 31,
        "tempo": "4h",
        "programacao": "4 semanas (1h por semana – 8 videoaulas por semana)",
        "atividades": "Teste seu conhecimento (obrigatório para a aprovação) e Atividade prática (extra)",
    },
    {
        "id": "sanidade_bezerras",
        "variantes": [
            "Reduzir a ocorrência de doenças e mortalidade e definir protocolos para tratamento de doenças das bezerras.",
        ],
        "dor": "Reduzir doenças e mortalidade das bezerras e definir protocolos de tratamento.",
        "dor_exibicao": "Reduzir doenças e mortalidade das bezerras e definir protocolos de tratamento",
        "dor_curta": "Sanidade de bezerras e novilhas",
        "modulo": "Sanidade de bezerras e novilhas",
        "links": {
            "studio": _url("3141"),
            "videoteca": _url("2855"),
        },
        "aulas": 21,
        "tempo": "2,5h",
        "programacao": "3 semanas (1h por semana – 7 videoaulas por semana)",
        "atividades": "Teste seu conhecimento (obrigatório para a aprovação) e Atividade prática (extra)",
    },
    {
        "id": "criacao_bezerras",
        "variantes": [
            "Melhorar o ganho de peso das bezerras, definir plano alimentar das bezerras nas diferentes fases da vida.",
        ],
        "dor": "Melhorar o ganho de peso e definir alimentação das bezerras nas diferentes categorias.",
        "dor_exibicao": "Melhorar o ganho de peso e definir alimentação das bezerras nas diferentes categorias",
        "dor_curta": "Criação e alimentação de bezerras",
        "modulo": "Criação de bezerras e novilhas",
        "links": {
            "studio": _url("3134"),
            "videoteca": _url("2851"),
        },
        "aulas": 18,
        "tempo": "3h",
        "programacao": "3 semanas (1h por semana – 6 videoaulas por semana)",
        "atividades": "Teste seu conhecimento (obrigatório para a aprovação) e Atividade prática (extra)",
    },
    {
        "id": "qualidade_leite",
        "variantes": [
            "Reduzir gasto com medicamento de mastite, reduzir CCS e CBT do leite do tanque.",
        ],
        "dor": "Reduzir gasto com medicamento de mastite, reduzir CCS e CBT do leite do tanque.",
        "dor_exibicao": "Reduzir gastos com medicamento de mastite, reduzir CCS e CBT do leite do tanque",
        "dor_curta": "Qualidade do leite e mastite",
        "modulo": "Produção de leite de qualidade",
        "links": {
            "studio": _url("3140"),
            "videoteca": _url("2858"),
        },
        "aulas": 35,
        "tempo": "3,5h",
        "programacao": "4 semanas (1h por semana – 9 videoaulas por semana)",
        "atividades": "Teste seu conhecimento (obrigatório para a aprovação) e Atividade prática (extra)",
    },
    {
        "id": "indicadores_rebanho",
        "variantes": [
            "Planejar a necessidade de forragem do rebanho, calculando os indicadores e identificando oportunidades de manejo.",
        ],
        "dor": "Saber a quantidade de animais do próximo ano e quanto de forragem preciso produzir.",
        "dor_exibicao": "Saber a quantidade de animais no próximo ano e quanto de forragem preciso produzir",
        "dor_curta": "Indicadores reprodutivos e evolução do rebanho",
        "modulo": "Indicadores reprodutivos e Evolução de rebanho",
        "links": {
            "studio": _url("3137"),
            "videoteca": _url("2853"),
        },
        "aulas": 20,
        "tempo": "3h",
        "programacao": "3 semanas (1h por semana – 7 videoaulas por semana)",
        "atividades": "Teste seu conhecimento (obrigatório para a aprovação) e Atividade prática (extra)",
    },
    {
        "id": "manejo_milho",
        "variantes": [
            "Produzir silagem de milho ou sorgo de qualidade e em quantidade adequada para o rebanho.",
        ],
        "dor": "Produzir silagem de milho ou sorgo de qualidade e em quantidade adequada para o rebanho.",
        "dor_exibicao": "Produzir silagem de milho ou sorgo de qualidade e em quantidade adequada para o rebanho",
        "dor_curta": "Silagem de milho e sorgo",
        "modulo": "Manejo da cultura do milho",
        "links": {
            "studio": _url("3138"),
            "videoteca": _url("2856"),
        },
        "aulas": 16,
        "tempo": "3h",
        "programacao": "3 semanas (1h por semana – 5 videoaulas por semana)",
        "atividades": "Teste seu conhecimento (obrigatório para a aprovação) e Atividade prática (extra)",
    },
    {
        "id": "manejo_alimentar",
        "variantes": [
            "Estruturar manejo alimentar para otimizar a produção de leite e monitorar os resultados.",
        ],
        "dor": "Estruturar manejo alimentar para otimizar a produção de leite.",
        "dor_exibicao": "Estruturar manejo alimentar para otimizar produção de leite",
        "dor_curta": "Manejo alimentar e planejamento forrageiro",
        "modulo": "Planejamento forrageiro e manejo alimentar",
        "links": {
            "studio": _url("3139"),
            "videoteca": _url("2857"),
        },
        "aulas": 28,
        "tempo": "3,5h",
        "programacao": "4 semanas (1h por semana – 7 videoaulas por semana)",
        "atividades": "Teste seu conhecimento (obrigatório para a aprovação) e Atividade prática (extra)",
    },
]

# Módulo de boas-vindas (sempre incluído no início do plano)
MODULO_BOASVINDAS = {
    "modulo": "Boas-vindas",
    "links": {
        "studio": _url("3133"),
        "videoteca": _url("2850"),
    },
    "aulas": None,
    "tempo": None,
    "programacao": None,
    "atividades": None,
}


# ─────────────────────────────────────────
#  Resolução de link por plataforma
# ─────────────────────────────────────────
def plataforma_valida(plataforma: str | None) -> str:
    """Devolve o id de plataforma pedido, ou o padrão se vier vazio/desconhecido."""
    ids = [p["id"] for p in PLATAFORMAS]
    return plataforma if plataforma in ids else PLATAFORMA_PADRAO


def get_plataforma(plataforma: str | None) -> dict:
    alvo = plataforma_valida(plataforma)
    return next(p for p in PLATAFORMAS if p["id"] == alvo)


def link_modulo(modulo: dict, plataforma: str | None = None) -> str:
    """Link do módulo (dor ou boas-vindas) na plataforma pedida.

    Cai para o link da plataforma padrão se o módulo ainda não tiver o par
    cadastrado — melhor um link válido da turma nova do que string vazia.
    """
    links = modulo.get("links") or {}
    return links.get(plataforma_valida(plataforma)) or links.get(PLATAFORMA_PADRAO, "")


def link_boas_vindas(plataforma: str | None = None) -> str:
    return link_modulo(MODULO_BOASVINDAS, plataforma)


def get_dor_por_id(dor_id: str) -> dict | None:
    for d in DORES:
        if d["id"] == dor_id:
            return d
    return None


def get_lista_dores() -> list[str]:
    """Retorna lista de textos completos das dores (para exibir no formulário)."""
    return [d["dor"] for d in DORES]


def get_lista_dores_curtas() -> list[str]:
    return [d["dor_curta"] for d in DORES]


def dor_texto_para_id(texto: str) -> str | None:
    for d in DORES:
        if d["dor"] == texto:
            return d["id"]
    return None


# ─────────────────────────────────────────
#  Casamento de texto (CSV do HubSpot → dor)
# ─────────────────────────────────────────
def _textos_casaveis(dor: dict) -> list[str]:
    """Todas as redações aceitas para a mesma dor (canônica + variantes)."""
    return [dor["dor"], *dor.get("variantes", [])]


def normalizar(texto: str) -> str:
    """Minúsculas, sem acentos, sem pontuação, espaços colapsados.

    Usado para casar o texto que vem do HubSpot (que pode variar pontuação,
    ex.: ponto final faltando) contra o texto canônico das dores.
    """
    if not texto:
        return ""
    texto = unicodedata.normalize("NFKD", texto)
    texto = "".join(c for c in texto if not unicodedata.combining(c))
    texto = texto.lower()
    texto = "".join(c if c.isalnum() else " " for c in texto)
    return " ".join(texto.split())


def match_dores(prioridades_texto: str) -> tuple[list[dict], list[str]]:
    """Casa as dores escolhidas dentro do campo das 3 prioridades.

    O HubSpot junta as opções escolhidas por vírgula, mas algumas dores têm
    vírgula interna — então não dá pra dividir por vírgula. Aqui procuramos
    cada dor canônica (normalizada) como substring do campo normalizado e
    retornamos as encontradas na ordem em que aparecem no texto.

    Retorna (dores_encontradas, trechos_nao_reconhecidos).
    """
    alvo = normalizar(prioridades_texto)
    if not alvo:
        return [], []

    encontradas = []
    cobertura = []  # (inicio, fim) dos trechos casados, p/ achar sobras
    for d in DORES:
        for texto in _textos_casaveis(d):
            agulha = normalizar(texto)
            pos = alvo.find(agulha)
            if pos != -1:
                encontradas.append((pos, d))
                cobertura.append((pos, pos + len(agulha)))
                break

    encontradas.sort(key=lambda x: x[0])
    dores = [d for _, d in encontradas]

    # Detecta trechos não cobertos (possíveis opções novas/divergentes)
    nao_reconhecidos = []
    if len(dores) < 3:
        restante = alvo
        for _, d in encontradas:
            for texto in _textos_casaveis(d):
                restante = restante.replace(normalizar(texto), " | ")
        sobras = [s.strip() for s in restante.split("|") if len(s.strip()) > 8]
        nao_reconhecidos = sobras

    return dores, nao_reconhecidos


def match_dor_unica(texto: str) -> dict | None:
    """Casa o valor de UMA coluna de prioridade (1ª/2ª/3ª) com a dor.

    Usado no formato ranqueado do formulário, em que cada prioridade vem na
    própria coluna — aqui a ordem do plano é a ordem das colunas, ou seja, o
    ranqueamento que o aluno de fato fez.
    """
    alvo = normalizar(texto)
    if not alvo:
        return None
    for d in DORES:
        for candidato in _textos_casaveis(d):
            if normalizar(candidato) in alvo:
                return d
    return None
