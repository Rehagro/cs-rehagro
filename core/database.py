import sqlite3
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from config import DB_PATH, TURMA_ID, TURMA_NOME


def _conn():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    return sqlite3.connect(DB_PATH, check_same_thread=False)


def inicializar_banco():
    with _conn() as con:
        # ── Tabela de turmas ────────────────────────────────────
        con.execute("""
        CREATE TABLE IF NOT EXISTS turmas (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            turma_id    TEXT UNIQUE NOT NULL,
            turma_nome  TEXT NOT NULL,
            ativa       INTEGER DEFAULT 0,
            criada_em   TEXT DEFAULT (datetime('now','localtime'))
        )
        """)
        # Popula turma padrão se vazio
        existe = con.execute("SELECT COUNT(*) FROM turmas").fetchone()[0]
        if existe == 0:
            con.execute(
                "INSERT INTO turmas (turma_id, turma_nome, ativa) VALUES (?, ?, 1)",
                (TURMA_ID, TURMA_NOME),
            )

        # ── Tabela de respostas ─────────────────────────────────
        con.execute("""
        CREATE TABLE IF NOT EXISTS respostas (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            turma_id        TEXT    NOT NULL,
            turma_nome      TEXT    NOT NULL,
            criado_em       TEXT    DEFAULT (datetime('now','localtime')),

            -- Identificação
            nome            TEXT,
            cpf             TEXT,
            cidade          TEXT,
            estado          TEXT,

            -- Bloco 1: Contexto produtivo
            producao_litros_dia     REAL,
            nao_se_aplica_producao  INTEGER DEFAULT 0,
            animais_lactacao        REAL,
            nao_se_aplica_animais   INTEGER DEFAULT 0,
            media_vaca_dia          REAL,
            nao_se_aplica_media     INTEGER DEFAULT 0,
            cargo                   TEXT,
            formacao                TEXT,

            -- Bloco 2: Objetivos
            valeu_a_pena    TEXT,
            meta_fazenda    TEXT,

            -- Bloco 3: Prioridades (dores ranqueadas)
            prioridade_1    TEXT,
            prioridade_2    TEXT,
            prioridade_3    TEXT,

            -- Plano gerado
            plano_gerado    INTEGER DEFAULT 0,
            plano_gerado_em TEXT
        )
        """)


def salvar_resposta(dados: dict) -> int:
    with _conn() as con:
        cur = con.execute("""
        INSERT INTO respostas (
            turma_id, turma_nome,
            nome, cpf, cidade, estado,
            producao_litros_dia, nao_se_aplica_producao,
            animais_lactacao, nao_se_aplica_animais,
            media_vaca_dia, nao_se_aplica_media,
            cargo, formacao,
            valeu_a_pena, meta_fazenda,
            prioridade_1, prioridade_2, prioridade_3
        ) VALUES (
            :turma_id, :turma_nome,
            :nome, :cpf, :cidade, :estado,
            :producao_litros_dia, :nao_se_aplica_producao,
            :animais_lactacao, :nao_se_aplica_animais,
            :media_vaca_dia, :nao_se_aplica_media,
            :cargo, :formacao,
            :valeu_a_pena, :meta_fazenda,
            :prioridade_1, :prioridade_2, :prioridade_3
        )
        """, dados)
        return cur.lastrowid


def listar_respostas(turma_id: str | None = None) -> list[dict]:
    with _conn() as con:
        con.row_factory = sqlite3.Row
        if turma_id:
            rows = con.execute(
                "SELECT * FROM respostas WHERE turma_id = ? ORDER BY criado_em DESC",
                (turma_id,)
            ).fetchall()
        else:
            rows = con.execute(
                "SELECT * FROM respostas ORDER BY criado_em DESC"
            ).fetchall()
        return [dict(r) for r in rows]


def buscar_resposta(resposta_id: int) -> dict | None:
    with _conn() as con:
        con.row_factory = sqlite3.Row
        row = con.execute(
            "SELECT * FROM respostas WHERE id = ?", (resposta_id,)
        ).fetchone()
        return dict(row) if row else None


def marcar_plano_gerado(resposta_id: int):
    with _conn() as con:
        con.execute("""
        UPDATE respostas
        SET plano_gerado = 1,
            plano_gerado_em = datetime('now','localtime')
        WHERE id = ?
        """, (resposta_id,))


def cpf_ja_respondeu(cpf: str, turma_id: str) -> bool:
    cpf_limpo = "".join(c for c in cpf if c.isdigit())
    with _conn() as con:
        row = con.execute(
            "SELECT id FROM respostas WHERE cpf = ? AND turma_id = ?",
            (cpf_limpo, turma_id)
        ).fetchone()
        return row is not None


# ═════════════════════════════════════════════════════════════════════════
#  GESTÃO DE TURMAS
# ═════════════════════════════════════════════════════════════════════════

def listar_turmas() -> list[dict]:
    """Retorna todas as turmas + contagem de respostas."""
    with _conn() as con:
        con.row_factory = sqlite3.Row
        rows = con.execute("""
            SELECT t.*,
                   (SELECT COUNT(*) FROM respostas r
                    WHERE r.turma_id = t.turma_id) AS qtd_respostas
            FROM turmas t
            ORDER BY t.ativa DESC, t.criada_em DESC
        """).fetchall()
        return [dict(r) for r in rows]


def get_turma_ativa() -> dict | None:
    """Retorna a turma marcada como ativa (ou None)."""
    with _conn() as con:
        con.row_factory = sqlite3.Row
        row = con.execute(
            "SELECT * FROM turmas WHERE ativa = 1 LIMIT 1"
        ).fetchone()
        return dict(row) if row else None


def get_turma(turma_id: str) -> dict | None:
    with _conn() as con:
        con.row_factory = sqlite3.Row
        row = con.execute(
            "SELECT * FROM turmas WHERE turma_id = ?", (turma_id,)
        ).fetchone()
        return dict(row) if row else None


def criar_turma(turma_id: str, turma_nome: str, ativar: bool = False) -> bool:
    """Cria turma nova. Se ativar=True, marca como ativa (desativa outras)."""
    with _conn() as con:
        try:
            con.execute(
                "INSERT INTO turmas (turma_id, turma_nome, ativa) VALUES (?, ?, 0)",
                (turma_id, turma_nome),
            )
        except sqlite3.IntegrityError:
            return False
    if ativar:
        ativar_turma(turma_id)
    return True


def ativar_turma(turma_id: str):
    """Marca uma turma como ativa — desativa todas as outras."""
    with _conn() as con:
        con.execute("UPDATE turmas SET ativa = 0")
        con.execute("UPDATE turmas SET ativa = 1 WHERE turma_id = ?", (turma_id,))


def atualizar_turma_nome(turma_id: str, novo_nome: str):
    with _conn() as con:
        con.execute(
            "UPDATE turmas SET turma_nome = ? WHERE turma_id = ?",
            (novo_nome, turma_id),
        )
        con.execute(
            "UPDATE respostas SET turma_nome = ? WHERE turma_id = ?",
            (novo_nome, turma_id),
        )


def deletar_turma(turma_id: str) -> tuple[bool, str]:
    """Deleta turma. Bloqueia se houver respostas vinculadas."""
    with _conn() as con:
        qtd = con.execute(
            "SELECT COUNT(*) FROM respostas WHERE turma_id = ?", (turma_id,)
        ).fetchone()[0]
        if qtd > 0:
            return False, f"Não é possível remover — {qtd} resposta(s) vinculadas."
        con.execute("DELETE FROM turmas WHERE turma_id = ?", (turma_id,))
        return True, "Turma removida."
