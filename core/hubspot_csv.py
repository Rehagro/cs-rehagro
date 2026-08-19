"""
Parser do CSV exportado pelo HubSpot Survey (pesquisa de início de curso).

Particularidades tratadas aqui:
  1. O export costuma vir DUPLO-ENCODADO: a linha inteira é um único campo
     entre aspas, com as aspas internas duplicadas. Detectamos isso e fazemos
     o parse em 2 passadas.
  2. As 3 prioridades podem vir em DOIS formatos:
       a) ranqueado (formulário atual): uma coluna por prioridade —
          "Qual a primeira/segunda/terceira prioridade?". A ordem das colunas
          É o ranqueamento do aluno e vira a ordem dos módulos no plano.
       b) combinado (formato antigo): uma única coluna com as opções juntas
          por vírgula. Como algumas dores têm vírgula interna, o casamento é
          por texto (core.mapeamento.match_dores), e a ordem é a da tela.
     O parser detecta o formato (a) e cai para o (b) se não achar as colunas.
  3. Os cabeçalhos podem vir com HTML (<strong>, <span style=...>) — as chaves
     de busca são procuradas dentro do texto normalizado, então isso não atrapalha.
"""
import csv
import io

from core.mapeamento import match_dor_unica, match_dores

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
    ("qtd_animais",                 "animais"),   # nome interno da propriedade
    ("media de producao por vaca",  "media_vaca"),
    ("valer a pena",                "valeu_a_pena"),
    ("daqui a 5 anos",              "meta"),
    ("3 pontos mais importantes",   "prioridades"),   # formato combinado (antigo)
    ("contact email",              "email"),
]

# Formato ranqueado: uma coluna por prioridade, na ordem escolhida pelo aluno.
_COLUNAS_RANQUEADAS = [
    ("primeira prioridade",  "prioridade_texto_1"),
    ("segunda prioridade",   "prioridade_texto_2"),
    ("terceira prioridade",  "prioridade_texto_3"),
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
        for chave_busca, chave_interna in _COLUNAS + _COLUNAS_RANQUEADAS:
            if chave_busca in col_norm and i not in idx_para_chave:
                # 'matriculado' tem prioridade sobre o "Nome" simples
                if chave_interna not in idx_para_chave.values():
                    idx_para_chave[i] = chave_interna
                break
    return idx_para_chave


def colunas_reconhecidas(raw) -> dict[str, str]:
    """chave interna -> cabeçalho como veio no arquivo (sem o HTML dos rótulos).

    Serve ao diagnóstico na tela: mostra ao CS o que o sistema achou no CSV e,
    por consequência, o que NÃO achou.
    """
    import re

    linhas = _linhas(_decode(raw))
    if not linhas:
        return {}
    header = linhas[0]
    limpo = lambda s: " ".join(re.sub(r"<[^>]+>", " ", s or "").split())
    return {chave: limpo(header[i]) for i, chave in _mapear_cabecalho(header).items()}


def _casar_prioridades(registro: dict) -> tuple[list[dict], list[str]]:
    """Resolve as 3 dores do aluno, em ordem, nos dois formatos de export.

    Ranqueado tem prioridade: se houver ao menos uma coluna de prioridade
    preenchida, a ordem das colunas (1ª → 3ª) é a ordem dos módulos no plano.
    Sem isso, cai para o campo combinado antigo.
    """
    textos = [registro.get(chave, "") for _, chave in _COLUNAS_RANQUEADAS]
    if not any(t.strip() for t in textos):
        return match_dores(registro.get("prioridades", ""))

    modulos, nao_reconhecidas = [], []
    for texto in textos:
        texto = (texto or "").strip()
        if not texto:
            continue
        dor = match_dor_unica(texto)
        if dor is None:
            nao_reconhecidas.append(texto)
        elif dor not in modulos:          # aluno repetiu a mesma opção
            modulos.append(dor)
    return modulos, nao_reconhecidas


def parse_hubspot_csv(raw) -> list[dict]:
    """
    Lê o CSV (bytes ou str) e retorna uma lista de alunos. Cada aluno é um dict:
        nome, curso, perfil, formacao, producao, animais, media_vaca,
        valeu_a_pena, meta, email, prioridades (texto cru),
        modulos        -> lista de dicts de dor casados, JÁ na ordem de
                          prioridade do aluno (1ª → 3ª) quando o export traz
                          as colunas ranqueadas
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
        registro = {chave: "" for _, chave in _COLUNAS + _COLUNAS_RANQUEADAS}
        for i, valor in enumerate(linha):
            chave = idx_para_chave.get(i)
            if chave:
                registro[chave] = (valor or "").strip()

        # Fallback de nome: se "Nome do matriculado" veio vazio, usa col 0.
        if not registro.get("nome") and linha:
            registro["nome"] = (linha[0] or "").strip()

        modulos, sobras = _casar_prioridades(registro)
        registro["modulos"] = modulos
        registro["dores_nao_reconhecidas"] = sobras
        for n in range(3):
            registro[f"prioridade_{n + 1}"] = modulos[n]["id"] if n < len(modulos) else None

        # Compatibilidade com o gerador de plano (espera 'turma_nome')
        registro["turma_nome"] = registro.get("curso", "")

        alunos.append(registro)

    return alunos
