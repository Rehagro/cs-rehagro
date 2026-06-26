"""
Renderiza o Plano de Aula Rehagro em PDF — fidelidade total ao design.

Pipeline: dados (dict/JSON) -> Jinja2 -> HTML -> Playwright (Chromium) -> PDF

Por que Playwright/Chromium e não WeasyPrint?
  O design usa flexbox, CSS grid, gradientes e radius. O Chromium headless
  renderiza tudo exatamente como o navegador (e como a pré-visualização que
  você aprovou). WeasyPrint NÃO suporta flex/grid e vai quebrar o layout.

Instalação:
    pip install jinja2 playwright
    playwright install chromium

Uso:
    python render.py dados_exemplo.json plano_de_aula.pdf
"""
import json
import sys
import base64
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from playwright.sync_api import sync_playwright

BASE = Path(__file__).parent
ASSETS = BASE.parent / "assets"


def inline_logo() -> str:
    """Converte o logo em data URI para o PDF ser 100% self-contained."""
    png = (ASSETS / "rehagro-logo-white.png").read_bytes()
    b64 = base64.b64encode(png).decode("ascii")
    return f"data:image/png;base64,{b64}"


def render_html(dados: dict) -> str:
    env = Environment(loader=FileSystemLoader(str(BASE)), autoescape=True)
    tpl = env.get_template("plano_de_aula.html.j2")
    dados = dict(dados)
    dados["logo_url"] = inline_logo()  # sobrescreve o caminho relativo
    return tpl.render(**dados)


def html_to_pdf(html: str, saida: Path) -> None:
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.set_content(html, wait_until="networkidle")  # espera as fontes do Google
        page.pdf(
            path=str(saida),
            format="A4",
            print_background=True,   # ESSENCIAL: imprime os fundos verdes/dourados
            margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
        )
        browser.close()


def main():
    dados_path = Path(sys.argv[1]) if len(sys.argv) > 1 else BASE / "dados_exemplo.json"
    saida = Path(sys.argv[2]) if len(sys.argv) > 2 else BASE / "plano_de_aula.pdf"
    dados = json.loads(dados_path.read_text(encoding="utf-8"))
    html = render_html(dados)
    # opcional: salvar o HTML intermediário para inspeção
    (saida.with_suffix(".html")).write_text(html, encoding="utf-8")
    html_to_pdf(html, saida)
    print(f"OK -> {saida}")


if __name__ == "__main__":
    main()
