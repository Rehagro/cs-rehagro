# ─────────────────────────────────────────
#  Mapeamento: Dor do aluno → Módulo GPL
# ─────────────────────────────────────────

DORES = [
    {
        "id": "sistemas_producao",
        "dor": "Definir o melhor sistema de produção, instalações e raças mais adequados para a minha realidade.",
        "dor_curta": "Sistema de produção e instalações",
        "modulo": "Sistemas de produção e visão estratégica do negócio leite",
        "link": "https://rehagro.instructure.com/courses/2852",
        "aulas": None,
        "tempo": None,
        "programacao": None,
        "atividades": "Teste seu conhecimento (necessário para certificação) e Atividade prática (extra)",
    },
    {
        "id": "eficiencia_produtiva",
        "dor": "Reduzir doenças pós-parto, estabelecer melhores estratégias para emprenhar vacas rapidamente.",
        "dor_curta": "Reprodução e eficiência produtiva",
        "modulo": "Estratégias para eficiência produtiva",
        "link": "https://rehagro.instructure.com/courses/2854",
        "aulas": 21,
        "tempo": "3,5h",
        "programacao": "3 semanas (1h por semana – 7 videoaulas por semana)",
        "atividades": "Teste seu conhecimento (necessário para certificação) e Atividade prática (extra)",
    },
    {
        "id": "gestao_financeira",
        "dor": "Organizar os gastos, saber o custo do litro de leite e buscar o aumento do lucro na fazenda.",
        "dor_curta": "Gestão financeira e custos",
        "modulo": "Gestão financeira e econômica",
        "link": "https://rehagro.instructure.com/courses/2859",
        "aulas": 31,
        "tempo": "4h",
        "programacao": "4 semanas (1h por semana – 8 videoaulas por semana)",
        "atividades": "Teste seu conhecimento (necessário para certificação) e Atividade prática (extra)",
    },
    {
        "id": "sanidade_bezerras",
        "dor": "Reduzir doenças e mortalidade e definir protocolos para tratamento das bezerras.",
        "dor_curta": "Sanidade de bezerras e novilhas",
        "modulo": "Sanidade de bezerras e novilhas",
        "link": "https://rehagro.instructure.com/courses/2855",
        "aulas": 21,
        "tempo": "2,5h",
        "programacao": "3 semanas (1h por semana – 7 videoaulas por semana)",
        "atividades": "Teste seu conhecimento (necessário para certificação) e Atividade prática (extra)",
    },
    {
        "id": "criacao_bezerras",
        "dor": "Melhorar o ganho de peso e definir plano alimentar das bezerras nas diferentes fases da vida.",
        "dor_curta": "Criação e alimentação de bezerras",
        "modulo": "Criação de bezerras e novilhas",
        "link": "https://rehagro.instructure.com/courses/2851",
        "aulas": 18,
        "tempo": "3h",
        "programacao": "3 semanas (1h por semana – 6 videoaulas por semana)",
        "atividades": "Teste seu conhecimento (necessário para certificação) e Atividade prática (extra)",
    },
    {
        "id": "qualidade_leite",
        "dor": "Reduzir gasto com medicamento de mastite, reduzir CCS e CBT do leite do tanque.",
        "dor_curta": "Qualidade do leite e mastite",
        "modulo": "Produção de leite de qualidade",
        "link": "https://rehagro.instructure.com/courses/2858",
        "aulas": 35,
        "tempo": "3,5h",
        "programacao": "4 semanas (1h por semana – 9 videoaulas por semana)",
        "atividades": "Teste seu conhecimento (necessário para certificação) e Atividade prática (extra)",
    },
    {
        "id": "indicadores_rebanho",
        "dor": "Planejar a necessidade de forrageira, calcular indicadores e identificar oportunidades no manejo.",
        "dor_curta": "Indicadores reprodutivos e evolução do rebanho",
        "modulo": "Indicadores reprodutivos e Evolução de rebanho",
        "link": "https://rehagro.instructure.com/courses/2853",
        "aulas": 20,
        "tempo": "3h",
        "programacao": "3 semanas (1h por semana – 7 videoaulas por semana)",
        "atividades": "Teste seu conhecimento (necessário para certificação) e Atividade prática (extra)",
    },
    {
        "id": "manejo_milho",
        "dor": "Produzir silagem de milho ou sorgo de qualidade e em quantidade adequada para o rebanho.",
        "dor_curta": "Silagem de milho e sorgo",
        "modulo": "Manejo da cultura do milho",
        "link": "https://rehagro.instructure.com/courses/2856",
        "aulas": 16,
        "tempo": "3h",
        "programacao": "3 semanas (1h por semana – 5 videoaulas por semana)",
        "atividades": "Teste seu conhecimento (necessário para certificação) e Atividade prática (extra)",
    },
    {
        "id": "manejo_alimentar",
        "dor": "Estruturar manejo alimentar para otimizar a produção de leite e monitorar os resultados. Reduzir perdas no processo da ensilagem e desensilagem.",
        "dor_curta": "Manejo alimentar e planejamento forrageiro",
        "modulo": "Planejamento forrageiro e manejo alimentar",
        "link": "https://rehagro.instructure.com/courses/2857",
        "aulas": 28,
        "tempo": "3,5h",
        "programacao": "4 semanas (1h por semana – 7 videoaulas por semana)",
        "atividades": "Teste seu conhecimento (necessário para certificação) e Atividade prática (extra)",
    },
]

# Módulo de boas-vindas (sempre incluído no início do plano)
MODULO_BOASVINDAS = {
    "modulo": "Boas-vindas",
    "link": "https://rehagro.instructure.com/courses/2850",
    "aulas": None,
    "tempo": None,
    "programacao": None,
    "atividades": None,
}


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
