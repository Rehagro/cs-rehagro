"""
Render do Plano de Aula: dados -> HTML (Jinja2) -> PDF (Chromium headless).

- `render_html(dados)` sempre funciona (sem dependência de browser).
- `gerar_pdf(html)` tenta Playwright/Chromium; se indisponível (ex.: Streamlit
  Cloud sem browser), retorna None e o app cai no fluxo de "salvar pelo navegador".
"""
import base64
import os

from jinja2 import Environment, FileSystemLoader, select_autoescape

_BASE_DIR = os.path.dirname(os.path.dirname(__file__))
_TEMPLATES_DIR = os.path.join(_BASE_DIR, "templates")
_ASSETS_DIR = os.path.join(_BASE_DIR, "assets")
_FONTS_DIR = os.path.join(_ASSETS_DIR, "fonts")
_LOGO_WHITE = os.path.join(_ASSETS_DIR, "rehagro-logo-white.png")

# Fontes embutidas no documento (Poppins/Mulish — Google Fonts, OFL). Embutir
# em base64 deixa o PDF/HTML self-contained: sem depender de rede/Google na hora
# de gerar (gera sempre com o visual correto). Mulish é variável (400–700).
_FONTES = [
    ("Poppins", "500", "Poppins-Medium.ttf"),
    ("Poppins", "600", "Poppins-SemiBold.ttf"),
    ("Poppins", "700", "Poppins-Bold.ttf"),
    ("Mulish", "400 700", "Mulish[wght].ttf"),
]

_env = Environment(
    loader=FileSystemLoader(_TEMPLATES_DIR),
    autoescape=select_autoescape(["html", "xml", "j2"]),
)


def _font_faces_css() -> str:
    """Monta um <style> com @font-face base64 para cada fonte disponível."""
    regras = ["<style>"]
    for familia, peso, arquivo in _FONTES:
        caminho = os.path.join(_FONTS_DIR, arquivo)
        if not os.path.exists(caminho):
            continue
        with open(caminho, "rb") as f:
            b64 = base64.b64encode(f.read()).decode("ascii")
        regras.append(
            f"@font-face{{font-family:'{familia}';font-style:normal;"
            f"font-weight:{peso};font-display:swap;"
            f"src:url(data:font/ttf;base64,{b64}) format('truetype');}}"
        )
    regras.append("</style>")
    return "".join(regras)


# Construído uma única vez (os arquivos não mudam em runtime).
_FONT_FACE_CSS = _font_faces_css()


def _logo_data_uri() -> str:
    """Logo branco como data URI — PDF/HTML 100% self-contained."""
    if not os.path.exists(_LOGO_WHITE):
        return ""
    with open(_LOGO_WHITE, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("ascii")
    return f"data:image/png;base64,{b64}"


def render_html(dados: dict) -> str:
    tpl = _env.get_template("plano_de_aula.html.j2")
    contexto = dict(dados)
    contexto["logo_url"] = _logo_data_uri()
    contexto["font_face_css"] = _FONT_FACE_CSS
    return tpl.render(**contexto)


def gerar_pdf(html: str) -> bytes | None:
    """
    Gera o PDF a partir do HTML via Chromium headless. Retorna os bytes do PDF
    ou None se o Chromium não estiver disponível no ambiente.
    """
    try:
        from playwright.sync_api import sync_playwright
    except Exception:
        return None

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            try:
                page = browser.new_page()
                page.set_content(html, wait_until="networkidle")
                pdf = page.pdf(
                    format="A4",
                    print_background=True,
                    margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
                )
            finally:
                browser.close()
        return pdf
    except Exception:
        return None


def pdf_disponivel() -> bool:
    """Checa rapidamente se o Chromium do Playwright está instalado."""
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            path = p.chromium.executable_path
            return bool(path) and os.path.exists(path)
    except Exception:
        return False
