# ─────────────────────────────────────────
#  Configuração global — CS Rehagro GPL
# ─────────────────────────────────────────
import os

# Senha de acesso ao painel CS — lida de .streamlit/secrets.toml (gitignored)
# Em dev local: criar arquivo .streamlit/secrets.toml com:
#     CS_PASSWORD = "sua-senha"
# Em produção (Streamlit Cloud): definir no painel "Settings → Secrets"
try:
    import streamlit as st
    CS_PASSWORD = st.secrets.get("CS_PASSWORD", "")
except Exception:
    CS_PASSWORD = ""

# ── Identidade visual (2026-06-26) ─────────
RH_GREEN  = "#015641"   # verde principal
RH_GOLD   = "#cdaf69"   # dourado
RH_GREEN2 = "#87a851"   # verde secundário
RH_CREAM  = "#F4F1E9"   # fundo claro
RH_WHITE  = "#FFFFFF"
RH_MUTED  = "#6B6B5E"
RH_FONT   = "Myriad Pro"

# Caminhos
BASE_DIR   = os.path.dirname(__file__)
LOGO_PATH  = os.path.join(BASE_DIR, "assets", "logo_rehagro.png")
