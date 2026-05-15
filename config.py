# ─────────────────────────────────────────
#  Configuração global — CS Rehagro GPL
# ─────────────────────────────────────────
import os

# Turma padrão (popula o banco no primeiro run; depois é gerenciada via página "Turmas")
TURMA_ID   = "GPL-T18"
TURMA_NOME = "Gestão na Pecuária Leiteira · Turma 18"

# Senha de acesso ao painel CS — lida de .streamlit/secrets.toml (gitignored)
# Em dev local: criar arquivo .streamlit/secrets.toml com:
#     CS_PASSWORD = "sua-senha"
# Em produção (Streamlit Cloud): definir no painel "Settings → Secrets"
try:
    import streamlit as st
    CS_PASSWORD = st.secrets.get("CS_PASSWORD", "")
except Exception:
    CS_PASSWORD = ""

# Identidade visual
RH_GREEN = "#1C3829"
RH_GOLD  = "#C9A84C"
RH_CREAM = "#F0EBE0"
RH_WHITE = "#FFFFFF"
RH_MUTED = "#6B6B5E"

# Caminhos
BASE_DIR   = os.path.dirname(__file__)
DB_PATH    = os.path.join(BASE_DIR, "data", "respostas.db")
LOGO_PATH  = os.path.join(BASE_DIR, "assets", "logo_rehagro.png")
