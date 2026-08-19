"""
Diagnóstico do CSV: diz ao CS, em português claro, o que falta no arquivo
para o plano ser gerado — antes de ele tentar gerar e receber um plano vazio.

Dois níveis:
  1. diagnosticar_arquivo() — o CSV como um todo (colunas que o sistema não
     achou, dores com redação divergente, alunos sem trilha).
  2. diagnosticar_aluno()   — o aluno selecionado, campo a campo.

Regra usada aqui: "bloqueio" é o que impede um plano correto de existir;
"aviso" é o que sai capenga mas ainda vale enviar.
"""
from collections import Counter

# Campos que aparecem impressos no plano do aluno.
_CAMPO_NOME = ("nome", "Nome do matriculado")
_CAMPO_CURSO = ("curso", "Nome do curso")

# Colunas ranqueadas (formato atual do formulário).
_COLS_PRIORIDADE = [
    ("prioridade_texto_1", "Qual a primeira prioridade?"),
    ("prioridade_texto_2", "Qual a segunda prioridade?"),
    ("prioridade_texto_3", "Qual a terceira prioridade?"),
]

# Campos de contexto: não entram no plano, mas o CS usa para conhecer o aluno.
_CAMPOS_CONTEXTO = [
    ("email", "E-mail"),
    ("codigo", "Código da matrícula"),
    ("perfil", "Perfil (dono/sócio, consultor…)"),
    ("formacao", "Formação"),
    ("producao", "Volume de produção"),
    ("animais", "Número de animais"),
    ("media_vaca", "Média por vaca"),
    ("valeu_a_pena", "O que faria valer a pena"),
    ("meta", "Meta para os próximos anos"),
]


def _vazio_para_todos(alunos: list[dict], chave: str) -> bool:
    return not any((a.get(chave) or "").strip() for a in alunos)


def diagnosticar_arquivo(alunos: list[dict], colunas: dict[str, str]) -> dict:
    """
    alunos:  saída de parse_hubspot_csv
    colunas: chave interna -> cabeçalho encontrado (hubspot_csv.colunas_reconhecidas)

    Retorna {'bloqueios': [...], 'avisos': [...], 'info': [...],
             'dores_divergentes': [(texto, qtd)], 'alunos_sem_trilha': [nomes],
             'alunos_incompletos': [(nome, qtd_modulos)], 'colunas': {...}}
    """
    total = len(alunos)
    bloqueios, avisos, info = [], [], []

    tem_ranqueadas = any(c in colunas for c, _ in _COLS_PRIORIDADE)
    tem_combinada = "prioridades" in colunas

    if not tem_ranqueadas and not tem_combinada:
        bloqueios.append(
            "**Nenhuma coluna de prioridade foi encontrada.** O plano é montado a partir "
            "das respostas de 1ª, 2ª e 3ª prioridade — sem elas não há trilha. "
            "Confira se a exportação incluiu as colunas "
            "*“Qual a primeira/segunda/terceira prioridade?”*."
        )
    elif tem_ranqueadas:
        faltando = [rot for c, rot in _COLS_PRIORIDADE if c not in colunas]
        if faltando:
            avisos.append(
                "O arquivo tem só parte das prioridades — não vieram: "
                + ", ".join(f"*{r}*" for r in faltando)
                + ". Os alunos vão receber um plano com menos módulos."
            )

    chave_nome, rotulo_nome = _CAMPO_NOME
    if _vazio_para_todos(alunos, chave_nome):
        bloqueios.append(
            f"**A coluna “{rotulo_nome}” não veio preenchida.** O nome do aluno é impresso "
            "na capa do plano e usado no nome do arquivo."
        )

    chave_curso, rotulo_curso = _CAMPO_CURSO
    if _vazio_para_todos(alunos, chave_curso):
        avisos.append(
            f"A coluna “{rotulo_curso}” não veio preenchida — a capa do plano sai sem o "
            "nome do curso. Dá para enviar assim, mas o ideal é corrigir a exportação."
        )

    ausentes_contexto = [rot for chave, rot in _CAMPOS_CONTEXTO if _vazio_para_todos(alunos, chave)]
    if ausentes_contexto:
        info.append(
            "Campos de contexto que não vieram no arquivo (não afetam o plano, "
            "só o que o CS enxerga aqui): " + ", ".join(ausentes_contexto) + "."
        )

    # Redações que não casaram com nenhuma dor — normalmente é o texto da opção
    # tendo mudado no formulário.
    divergentes = Counter()
    for a in alunos:
        for t in a.get("dores_nao_reconhecidas", []):
            divergentes[t.strip()] += 1

    # Vermelho fica reservado ao que impede gerar; a divergência de redação
    # gera plano (mais curto), então é aviso — e o caso fatal (aluno sem
    # nenhum módulo) já entra como bloqueio logo abaixo.
    if divergentes:
        avisos.append(
            f"**{len(divergentes)} resposta(s) de prioridade não casaram com nenhum módulo.** "
            "Quase sempre é o texto da opção tendo mudado no HubSpot. Quem escolheu essas "
            "opções recebe um plano com menos módulos — veja a lista no detalhamento abaixo."
        )

    sem_trilha = [a.get("nome") or "(sem nome)" for a in alunos if not a.get("modulos")]
    incompletos = [
        (a.get("nome") or "(sem nome)", len(a.get("modulos", [])))
        for a in alunos
        if 0 < len(a.get("modulos", [])) < 3
    ]

    if sem_trilha:
        bloqueios.append(
            f"**{len(sem_trilha)} de {total} aluno(s) ficaram sem nenhum módulo** — "
            "para esses, o plano não pode ser gerado."
        )
    if incompletos:
        avisos.append(
            f"{len(incompletos)} aluno(s) ficaram com menos de 3 módulos. "
            "O plano é gerado assim mesmo, com os módulos que casaram."
        )

    return {
        "bloqueios": bloqueios,
        "avisos": avisos,
        "info": info,
        "dores_divergentes": divergentes.most_common(),
        "alunos_sem_trilha": sem_trilha,
        "alunos_incompletos": incompletos,
        "colunas": colunas,
        "total": total,
    }


def diagnosticar_aluno(aluno: dict) -> tuple[list[str], list[str]]:
    """Retorna (bloqueios, avisos) do aluno selecionado."""
    bloqueios, avisos = [], []

    if not (aluno.get("nome") or "").strip():
        bloqueios.append("Sem **nome do matriculado** — o plano é nominal, não dá para gerar.")

    modulos = aluno.get("modulos", [])
    if not modulos:
        bloqueios.append(
            "**Nenhuma prioridade virou módulo.** Ou as respostas vieram vazias, ou o texto "
            "das opções no HubSpot está diferente do cadastrado no gerador."
        )
    elif len(modulos) < 3:
        avisos.append(
            f"Só **{len(modulos)} de 3** prioridades viraram módulo — o plano sai mais curto."
        )

    if not (aluno.get("curso") or "").strip():
        avisos.append("Sem **nome do curso** — a capa do plano fica sem essa linha.")

    for texto in aluno.get("dores_nao_reconhecidas", []):
        avisos.append(f"Resposta não reconhecida: “{texto}”")

    return bloqueios, avisos
