# -*- coding: utf-8 -*-
"""
Gerador de PDF do "Plano de Estudos" (design Rehagro) a partir de dados de um aluno.

Ferramenta reutilizável: cada aluno = um bloco DADOS -> um PDF. Reaproveita o
motor visual do projeto cs_rehagro (fontes Poppins/Mulish + logo embutidas em
base64), então o PDF sai visualmente idêntico ao design e 100% self-contained
(não depende de internet). Suporta N módulos (não só 3), links clicáveis em
cada card e prazo de acesso opcional no hero.

Como usar
---------
1. Extraia os dados do Word do aluno (ver README.md — snippet com python-docx).
2. Edite o bloco DADOS abaixo (nome, curso, datas, módulos).
3. Rode:  python gerar_plano.py
   Saída: ./saida/Plano de Estudos - <Nome>.pdf  (+ .html e preview.png)

Requisitos: jinja2, playwright (+ chromium instalado), fontes/logo do projeto.
"""
import os
import re
import sys

from jinja2 import Environment, FileSystemLoader, select_autoescape
from playwright.sync_api import sync_playwright

# --- Caminhos (portáteis: derivados da localização deste arquivo) ----------- #
AQUI = os.path.dirname(os.path.abspath(__file__))
# Este script mora em <projeto>/tools/gerador_plano_pdf/ -> projeto = 2 níveis acima.
PROJETO = os.path.abspath(os.path.join(AQUI, "..", ".."))
SAIDA_DIR = os.path.join(AQUI, "saida")

# Reaproveita as fontes/logo embutidas do projeto (visual idêntico ao app).
sys.path.insert(0, PROJETO)
from core.render_plano import _FONT_FACE_CSS, _logo_data_uri  # noqa: E402


def _url(course_id: str) -> str:
    return f"https://rehagro.instructure.com/courses/{course_id}"


# =========================================================================== #
# DADOS DO ALUNO  — EDITE ESTE BLOCO A CADA PLANO
# (exemplo real: Ruan, 9 módulos, extraído de "Plano de aula - arquivo 2 (1).docx")
# =========================================================================== #
NOME = "Ruan"
CURSO = "GPL — Gestão na Pecuária Leiteira"
DATA_GERACAO = "28/07/2026"          # data de hoje (dd/mm/aaaa)
PRAZO_ACESSO = "09/01/2027"          # deixe "" para não mostrar o prazo no hero

INTRO_TEXTO = (
    f'<strong style="color:#0F4630;">{NOME}</strong>, esse é o seu plano de aula '
    "personalizado. Nele você verá as orientações sobre a sequência de conteúdos "
    "para assistir nesses primeiros meses de curso, além de materiais complementares "
    "que podem te apoiar no seu dia a dia. "
    '<strong style="color:#0F4630;">Confira abaixo nossa recomendação:</strong>'
)

ATIV = "Teste seu conhecimento (necessário para certificação) e Atividade prática (extra)"

# (título, course_id, qtd_aulas, tempo, programação) — na ordem em que devem aparecer.
MODULOS = [
    ("Planejamento forrageiro e manejo alimentar", "2857", "28", "3,5h", "3 semanas (9 videoaulas por semana)"),
    ("Sistemas de produção e visão estratégica do negócio leite", "2852", "16", "2,5h", "2 semanas (8 videoaulas por semana)"),
    ("Gestão financeira e econômica", "2859", "31", "4h", "4 semanas (8 videoaulas por semana)"),
    ("Produção de leite de qualidade", "2858", "35", "3,5h", "4 semanas (9 videoaulas por semana)"),
    ("Indicadores reprodutivos e Evolução de rebanho", "2853", "20", "3h", "2 semanas (10 videoaulas por semana)"),
    ("Estratégias para eficiência produtiva", "2854", "21", "3,5h", "2 semanas (10 videoaulas por semana)"),
    ("Criação de bezerras e novilhas", "2851", "18", "3h", "2 semanas (9 videoaulas por semana)"),
    ("Sanidade de bezerras e novilhas", "2855", "21", "2,5h", "2 semanas (10 videoaulas por semana)"),
    ("Manejo da cultura do milho", "2856", "16", "3h", "2 semanas (8 videoaulas por semana)"),
]

BOAS_VINDAS = {
    "titulo": "Boas-vindas",
    "descricao": (
        "Para iniciar, veja como funciona o curso e os critérios de aprovação "
        "no nosso módulo de Boas-vindas."
    ),
    "url": _url("2850"),
}

ENCERRAMENTO = {
    "mensagem": (
        "Conte com a gente sempre que precisar — pra você aproveitar ao máximo o curso "
        "e levar o resultado para sua fazenda. 🌱"
    ),
    "equipe": "Equipe de Sucesso do Cliente",
    "organizacao": "Rehagro",
    # "whatsapp_url": "https://wa.me/5531991476763",  # descomente p/ mostrar o botão verde
}
# =========================================================================== #


def montar_dados() -> dict:
    return {
        "aluno": {"nome": NOME},
        "curso": {"nome": CURSO},
        "data_geracao": DATA_GERACAO,
        "prazo_acesso": PRAZO_ACESSO,
        "intro_texto": INTRO_TEXTO,
        "boas_vindas": BOAS_VINDAS,
        "modulos": [
            {
                "titulo": titulo,
                "url": _url(cid),
                "qtd_aulas": aulas,
                "tempo_aula": tempo if str(tempo).startswith("~") else f"~{tempo}",
                "atividades": ATIV,
                "programacao": prog,
            }
            for (titulo, cid, aulas, tempo, prog) in MODULOS
        ],
        "encerramento": ENCERRAMENTO,
    }


def render_html(dados: dict) -> str:
    env = Environment(
        loader=FileSystemLoader(AQUI),
        autoescape=select_autoescape(["html", "xml", "j2"]),
    )
    tpl = env.get_template("plano.html.j2")
    ctx = dict(dados)
    ctx["logo_url"] = _logo_data_uri()
    ctx["font_face_css"] = _FONT_FACE_CSS
    return tpl.render(**ctx)


def gerar_pdf(html: str, destino: str, preview_png: str) -> str:
    with sync_playwright() as p:
        browser = p.chromium.launch()
        try:
            page = browser.new_page()
            page.set_content(html, wait_until="networkidle")
            pdf_bytes = page.pdf(
                format="A4",
                print_background=True,
                margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
            )
            page.set_viewport_size({"width": 900, "height": 1400})
            page.screenshot(path=preview_png, full_page=True)
        finally:
            browser.close()

    # Se o destino estiver aberto/bloqueado no visualizador, cai p/ um nome alternativo.
    for candidato in (destino, destino.replace(".pdf", " (v2).pdf"),
                      destino.replace(".pdf", " (v3).pdf")):
        try:
            with open(candidato, "wb") as f:
                f.write(pdf_bytes)
            return candidato
        except PermissionError:
            continue
    raise PermissionError("Destino bloqueado (o PDF está aberto? feche e rode de novo).")


def main() -> None:
    os.makedirs(SAIDA_DIR, exist_ok=True)
    slug = re.sub(r"\s+", " ", NOME).strip()
    dados = montar_dados()
    html = render_html(dados)

    html_path = os.path.join(SAIDA_DIR, f"Plano de Estudos - {slug}.html")
    pdf_path = os.path.join(SAIDA_DIR, f"Plano de Estudos - {slug}.pdf")
    png_path = os.path.join(SAIDA_DIR, f"preview - {slug}.png")

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)
    destino = gerar_pdf(html, pdf_path, png_path)

    print("OK ->", destino)
    print("tamanho:", os.path.getsize(destino), "bytes")
    print("preview:", png_path)


if __name__ == "__main__":
    main()
