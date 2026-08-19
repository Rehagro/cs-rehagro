# Gerador de PDF — Plano de Estudos (a partir de um Word)

Ferramenta reutilizável para produzir o **PDF do Plano de Estudos** (design hi-fi
Rehagro) a partir dos dados de um aluno — normalmente vindos de um `.docx` como
`Plano de aula - arquivo 2 (1).docx`. Diferente do fluxo do app (CSV do HubSpot,
3 dores), aqui o número de módulos é livre (ex.: 9/10).

Reaproveita o motor visual do projeto (`core.render_plano._FONT_FACE_CSS` e
`_logo_data_uri`), então o PDF sai **idêntico ao design** e **self-contained**
(fontes Poppins/Mulish e logo embutidas em base64 — não depende de internet).

## Arquivos
- `gerar_plano.py` — edite o bloco **DADOS DO ALUNO** e rode. Já vem preenchido com o exemplo do **Ruan** (9 módulos).
- `plano.html.j2` — template do plano (cópia do design, com: selo "Módulo N", sem subtítulo por módulo, prazo de acesso opcional no hero, WhatsApp opcional no rodapé).
- `saida/` — onde caem os arquivos gerados (`.pdf`, `.html`, `preview.png`).

## Como usar
1. **Extrair o Word** (nome do aluno = título; e por módulo: link, aulas, tempo, atividades, programação):
   ```python
   import docx
   doc = docx.Document(r"CAMINHO\Plano de aula - arquivo X.docx")
   for p in doc.paragraphs:
       if p.text.strip():
           print(p.text)
   ```
   > O `course_id` do link é o número final da URL `.../courses/<ID>`.
2. **Editar `gerar_plano.py`**: `NOME`, `CURSO`, `DATA_GERACAO` (hoje), `PRAZO_ACESSO`
   (do Word; use `""` para ocultar), a lista `MODULOS` (na ordem desejada) e, se
   quiser, `ENCERRAMENTO["whatsapp_url"]`.
3. **Gerar**:
   ```powershell
   cd "<projeto>\tools\gerador_plano_pdf"
   python gerar_plano.py
   ```
   Saída em `saida\Plano de Estudos - <Nome>.pdf`.

## Convenções (definidas com o CS)
- Selo do card: **"Módulo N"** (não "Prioridade") quando há vários módulos.
- Subtítulo por módulo: **removido** por padrão.
- Texto inicial: padrão do `Plano de aula - Mensagem de envio.docx`.
- Hero: curso + "Gerado em [hoje]" + "Acesso até [prazo]".
- `tempo_aula` ganha `~` automático; `programacao` sem o "Se programe para assistir esse conteúdo em".

## Notas
- **N módulos → mais páginas** (9 módulos ≈ 4 páginas A4). Cards não cortam entre páginas (`break-inside: avoid`).
- Se o PDF estiver **aberto** no visualizador, o Windows bloqueia a regravação — o script cai para `(v2)`/`(v3)`. Melhor fechar antes de rodar.
- Precisa do Chromium do Playwright: `python -m playwright install chromium` (uma vez).
- Verificar links/páginas do PDF: `pypdf` (`len(reader.pages)` e anotações `/URI`).
