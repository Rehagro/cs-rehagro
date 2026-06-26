"""
Parser do CSV exportado pelo HubSpot Survey (pesquisa de início de curso).

Particularidades tratadas aqui:
  1. O export costuma vir DUPLO-ENCODADO: a linha inteira é um único campo
     entre aspas, com as aspas internas duplicadas. Detectamos isso e fazemos
     o parse em 2 passadas.
  2. O campo das 3 prioridades junta as opções por vírgula, mas algumas dores
     têm vírgula interna — o casamento é feito por texto em core.mapeamento.
"""
import csv
import io

from core.mapeamento import match_dores

# Cada coluna do HubSpot é identificada por uma palavra-chave (normalizada,
# minúscula) presente no cabeçalho — resiliente a pequenas mudanças de texto.
_COLUNAS = [
    ("matriculado",                 "nome"),       # "Nome do matriculado"
    ("codigo da matricula",         "codigo"),
    ("nome do curso",               "curso"),
    ("encaixa melhor",              "perfil"),
    ("formacao",                    "formacao"),
    ("volume de",                   "producao"),
    ("numero medio de animais",     "animais"),
    ("media de producao por vaca",  "media_vaca"),
    ("valer a pena",                "valeu_a_pena"),
    ("daqui a 5 anos",              "meta"),
    ("3 pontos mais importantes",   "prioridades"),
    ("contact email",              "email"),
]


def _strip_acentos(texto: str) -> str:
    import unicodedata
    texto = unicodedata.normalize("NFKD", texto or "")
    return "".join(c for c in texto if not unicodedata.combining(c)).lower().strip()


def _decode(raw) -> str:
    if isinstance(raw, str):
        return raw
    for enc in ("utf-8-sig", "utf-8", "latin-1"):
        try:
            return raw.decode(enc)
        except UnicodeDecodeError:
            continue
    return raw.decode("utf-8", errors="replace")


def _linhas(text: str) -> list[list[str]]:
    """Retorna as linhas já desfazendo o duplo-encoding, se houver."""
    outer = [r for r in csv.reader(io.StringIO(text)) if r and any(c.strip() for c in r)]
    if not outer:
        return []

    # Duplo-encodado: cabeçalho colapsa em 1 coluna que ainda contém vírgulas.
    if len(outer[0]) == 1 and "," in outer[0][0]:
        linhas = []
        for r in outer:
            linhas.append(next(csv.reader(io.StringIO(r[0]))))
        return linhas

    return outer


def _mapear_cabecalho(header: list[str]) -> dict[int, str]:
    """Índice da coluna → chave interna."""
    idx_para_chave = {}
    for i, col in enumerate(header):
        col_norm = _strip_acentos(col)
        for chave_busca, chave_interna in _COLUNAS:
            if chave_busca in col_norm and i not in idx_para_chave:
                # 'matriculado' tem prioridade sobre o "Nome" simples
                if chave_interna not in idx_para_chave.values():
                    idx_para_chave[i] = chave_interna
                break
    return idx_para_chave


def parse_hubspot_csv(raw) -> list[dict]:
    """
    Lê o CSV (bytes ou str) e retorna uma lista de alunos. Cada aluno é um dict:
        nome, curso, perfil, formacao, producao, animais, media_vaca,
        valeu_a_pena, meta, email, prioridades (texto cru),
        modulos        -> lista de dicts de dor casados (ordem do CSV)
        prioridade_1/2/3 -> ids das dores (para o gerador de plano)
        dores_nao_reconhecidas -> trechos do campo que não casaram
    """
    text = _decode(raw)
    linhas = _linhas(text)
    if len(linhas) < 2:
        return []

    header = linhas[0]
    idx_para_chave = _mapear_cabecalho(header)

    alunos = []
    for linha in linhas[1:]:
        registro = {chave: "" for _, chave in _COLUNAS}
        for i, valor in enumerate(linha):
            chave = idx_para_chave.get(i)
            if chave:
                registro[chave] = (valor or "").strip()

        # Fallback de nome: se "Nome do matriculado" veio vazio, usa col 0.
        if not registro.get("nome") and linha:
            registro["nome"] = (linha[0] or "").strip()

        modulos, sobras = match_dores(registro.get("prioridades", ""))
        registro["modulos"] = modulos
        registro["dores_nao_reconhecidas"] = sobras
        for n in range(3):
            registro[f"prioridade_{n + 1}"] = modulos[n]["id"] if n < len(modulos) else None

        # Compatibilidade com o gerador de plano (espera 'turma_nome')
        registro["turma_nome"] = registro.get("curso", "")

        alunos.append(registro)

    return alunos
