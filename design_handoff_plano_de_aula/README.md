# Handoff: Plano de Aula Personalizado — Rehagro

## Visão geral
Este pacote especifica o **documento "Plano de Aula Personalizado"** gerado para cada
aluno de capacitação do Rehagro. A ferramenta recebe dados de entrada (nome do aluno,
curso, módulos recomendados na ordem de prioridade, métricas de cada módulo) e deve
produzir um documento com a identidade visual do Rehagro, que sai em PDF e é enviado
ao aluno pelo time de Customer Success (CS).

O objetivo deste handoff é que o documento gerado pela ferramenta saia **exatamente**
como o protótipo aprovado, de forma automatizada e a partir de dados variáveis.

---

## Sobre os arquivos deste pacote
Os arquivos aqui são **referências de design feitas em HTML** — protótipos que mostram
o visual e a estrutura pretendidos, **não** código de produção a ser copiado cru.
A tarefa é **reproduzir este design no ambiente do seu projeto**, usando os padrões e
bibliotecas que você já adota (ou escolhendo a melhor stack, se ainda não houver uma).

Conteúdo do pacote:

| Caminho | O que é |
|---|---|
| `reference/Plano de Aula.dc.html` | Protótipo visual original (referência de aparência). Abra no navegador para ver o alvo. |
| `template/plano_de_aula.html.j2` | **Template de produção** em HTML + Jinja2, com placeholders e loop de módulos. É o ponto de partida recomendado. |
| `template/dados_exemplo.json` | Modelo de dados de entrada (o "contrato" que a ferramenta deve preencher). |
| `template/render.py` | Script de referência: dados → Jinja2 → HTML → PDF (Playwright/Chromium). |
| `assets/rehagro-logo-white.png` | Logo Rehagro em branco (para o fundo verde do cabeçalho). |
| `assets/rehagro-logo.png` | Logo Rehagro colorido (verde, fundo transparente) — para usos sobre fundo claro. |

---

## Fidelidade
**Alta fidelidade (hi-fi).** Cores, tipografia, espaçamentos e raios são finais.
Reproduza pixel a pixel. Todos os valores exatos estão na seção **Design Tokens**.

---

## ⚠️ Restrição de paginação: o PDF DEVE caber em 2 páginas A4
Uma implementação anterior gerou **3 páginas** por excesso de espaçamento vertical.
O template e os tokens deste pacote já foram **recalibrados** para caber em **2 páginas A4**
(com os 3 módulos de exemplo). Não reintroduza paddings/margens maiores nem aumente as
fontes — isso estoura para 3 páginas.

**Como a paginação foi validada (largura/altura reais de impressão A4 @96dpi):**
- Coluna de conteúdo impressa: `794px − 2×0.5in(48px) = 698px` de largura.
- Altura útil por página: `1123px − 2×0.38in(36.5px) = ~1050px` (as bandas de margem
  superior/inferior vêm do `thead`/`tfoot` repetidos).
- Altura total renderizada do conteúdo: **~1832px ≈ 1,74 páginas.**
- Com `break-inside: avoid` nos cards, a quebra cai naturalmente assim:
  - **Página 1:** Hero + Intro + Boas-vindas + Módulo 1.
  - **Página 2:** Módulo 2 + Módulo 3 + Encerramento.

**Se o seu conteúdo for maior (mais módulos, textos mais longos) e voltar a 3 páginas:**
1. Confirme que está usando os valores compactos desta versão (não os da versão anterior).
2. Reduza primeiro os espaços entre blocos (margens das seções, `margin-bottom` dos cards
   de 13px), depois os paddings internos dos cards/painéis — nunca as fontes abaixo dos
   valores aqui (legibilidade impressa).
3. Última opção, se houver muitos módulos: aceitar 3 páginas é melhor do que espremer a
   ponto de prejudicar leitura. A meta de 2 páginas vale para ~3 módulos.

---

## Recomendação de arquitetura (IMPORTANTE — leia antes de implementar)
O documento original era gerado como **.docx** e depois convertido manualmente em PDF
pelo CS. Recomendamos **abandonar o .docx** por dois motivos:

1. O `.docx` não reproduz fielmente flexbox/grid/gradientes/raios deste design — o
   resultado fica diferente do protótipo.
2. A conversão manual Word → PDF é um passo extra e fonte de inconsistência.

**Pipeline recomendado:** `dados → template HTML (Jinja2/Handlebars/etc.) → PDF via
Chromium headless`. Isso garante saída idêntica ao protótipo, sem intervenção manual.

- **Python:** Jinja2 + **Playwright** (`page.pdf(...)`) ou `pyppeteer`. Veja `render.py`.
  ⚠️ **Não use WeasyPrint/xhtml2pdf** — eles não suportam flexbox nem CSS grid e quebram este layout.
- **Node:** Handlebars/EJS + **Puppeteer** (`page.pdf(...)`).
- Sempre renderizar com `print_background: true` e `format: A4`, margens `0`
  (as margens internas já estão no CSS `@media print`).
- Esperar o carregamento das fontes do Google antes de gerar o PDF
  (`wait_until="networkidle"`), ou embutir as fontes localmente (ver **Assets**).

### "Esse botão pode substituir o link do arquivo de Word?"
Sim. Como o documento passa a ser HTML/PDF nativo, o fluxo pode ser:
- **Opção A (recomendada):** a ferramenta gera o **PDF** e o botão no AVA/e-mail aponta
  para o download do PDF — substituindo completamente o link do arquivo `.docx`.
- **Opção B:** a ferramenta publica o plano como **página HTML** (mesmo template, sem o
  CSS de impressão) e o botão abre essa página; o aluno pode imprimir/salvar em PDF pelo
  próprio navegador (o `@media print` já cuida do layout A4).
- **Opção C:** botão "Baixar plano de aula (PDF)" que dispara a geração sob demanda.

Em todos os casos, o botão substitui o link do `.docx`. **Observação:** a imagem enviada
("CL GPL – Boas-vindas") parece ser um banner de curso e não mostra o botão em si — se
houver um botão específico do AVA que você quer substituir, me mande o print dele para eu
detalhar o estado/CSS exato.

---

## Modelo de dados (contrato de entrada)
Estrutura que a ferramenta deve produzir e passar ao template (ver `dados_exemplo.json`):

```jsonc
{
  "data_geracao": "26/06/2026",          // string já formatada (dd/mm/aaaa)
  "aluno":  { "nome": "Douglas Brandão" },
  "curso":  { "nome": "Curso de teste" },

  "boas_vindas": {                        // bloco fixo "Para começar"
    "titulo": "Boas-vindas",
    "descricao": "Para iniciar, veja como funciona o curso ...",
    "url": "https://rehagro.instructure.com/courses/2850"
  },

  "modulos": [                            // 1..N — a numeração e "Nª Prioridade" são automáticas (loop.index)
    {
      "titulo": "Manejo da cultura do milho",
      "descricao": "Em seguida, veja o módulo ...",
      "url": "https://rehagro.instructure.com/courses/2856",
      "qtd_aulas": "16",                  // string ou int; exibido como número grande
      "tempo_aula": "~3h",                // string livre (ex.: "~3h", "~3,5h")
      "atividades": "Teste seu conhecimento (necessário para certificação) e Atividade prática (extra).",
      "programacao": "3 semanas — 1h por semana (5 videoaulas por semana)."
    }
    // ... mais módulos
  ],

  "encerramento": {
    "mensagem": "Nos acione a qualquer momento que precisar! ...",
    "equipe": "Equipe Customer Success",
    "organizacao": "Rehagro"
  }
}
```

**Notas sobre o loop de módulos:**
- O número do badge (1, 2, 3…) e o rótulo "1ª Prioridade / 2ª Prioridade…" são gerados
  automaticamente pelo índice do loop — **não** venham nos dados. O template suporta
  qualquer quantidade de módulos (1, 2, 4, 5…).
- `atividades` e `programacao` são frases completas; o template só prefixa o rótulo em
  negrito ("Atividades:", "Programação:"). Se quiser destacar os trechos "(necessário
  para certificação)" / "(extra)" em cinza como no protótipo, envolva-os em `<span
  style="color:#6A776E">…</span>` no backend, ou trate como HTML seguro (o template de
  exemplo escapa HTML por padrão — ajuste com `| safe` se for enviar marcação).

---

## Telas / Views
Documento de **página única e contínua** (flui em quantas páginas A4 forem necessárias).
De cima para baixo:

### 1. Hero / Capa
- **Layout:** seção full-width, `border-radius: 20px`, `padding: 34px 36px 32px`,
  `position: relative; overflow: hidden`.
- **Fundo:** `linear-gradient(135deg, #0F4630 0%, #0C3624 45%, #071E15 100%)`.
- **Ornamentos:** 2 SVGs decorativos (círculos/anéis) — anéis dourados (`#C49A45`) no
  canto superior direito e um anel verde (`#1E7A45`) no inferior esquerdo, com opacidade
  reduzida. São puramente decorativos (`aria-hidden`).
- **Topo:** logo Rehagro branco (`height: 26px`, à esquerda) + pílula "CUSTOMER SUCCESS"
  (à direita): borda `1px rgba(224,192,106,.45)`, texto `#E0C06A`, Poppins 10.5px, 600,
  `letter-spacing: .16em`, uppercase, `border-radius: 999px`, `padding: 6px 12px`.
- **Bloco título** (`margin-top: 30px`):
  - Eyebrow: "PLANO DE AULA PERSONALIZADO" — Poppins 12px, 600, `letter-spacing: .22em`,
    uppercase, cor `#E0C06A`.
  - H1: **nome do aluno** — Poppins 700, 38px, `line-height: 1.05`, `#fff`,
    `letter-spacing: -.01em`, `margin: 10px 0 0`.
  - Meta (`margin-top: 18px`, cor `rgba(255,255,255,.78)`, 13px, 500): ícone +
    `{{ curso.nome }}` · separador "•" (`opacity:.4`) · ícone calendário +
    "Gerado em {{ data_geracao }}". Ícones com `stroke: #E0C06A`.

### 2. Parágrafo de introdução
- `font-size: 15.5px; line-height: 1.7; color: #33433A; margin: 30px 2px 6px`.
- Abre com o nome do aluno em `<strong style="color:#0F4630">`. Texto fixo de saudação.

### 3. Section header "Para começar"
- Linha flex: H2 (Poppins 13px, 600, `letter-spacing: .18em`, uppercase, `#0F4630`) +
  régua que ocupa o resto (`height: 2px`, `linear-gradient(90deg, #C49A45 0%, #E7EBE6 100%)`).
- **Welcome card:** borda `1px #E2EAE4`, `border-radius: 16px`, `padding: 24px 26px`,
  fundo `linear-gradient(180deg,#FBFAF4 0%,#FFFFFF 60%)`.
  - Ícone à esquerda: quadrado 52×52, `border-radius: 14px`,
    `linear-gradient(135deg,#1E7A45,#0F4630)`, ícone "play/curso" branco, sombra
    `0 4px 12px rgba(15,70,48,.25)`.
  - Conteúdo: eyebrow "INÍCIO" (`#C49A45`), H3 título (Poppins 600, 20px, `#0F4630`),
    descrição (14.5px, `#445349`).
  - **Botão primário** "Acessar módulo": fundo `#0F4630`, texto branco, Poppins 500 13px,
    `padding: 10px 16px`, `border-radius: 10px`, ícone seta `↗` em `#E0C06A`. `href` = URL.

### 4. Section header "Sua trilha personalizada" + lista de módulos
- Mesmo padrão de header. Abaixo, linha auxiliar (13.5px, `#6A776E`).
- **Module card** (repete por módulo): borda `1px #E2EAE4`, `border-radius: 18px`,
  `overflow: hidden`, `margin-bottom: 22px`, sombra `0 2px 10px rgba(15,70,48,.05)`.
  - **Header do card** (`padding: 20px 24px`, fundo `linear-gradient(180deg,#F4F8F4,#FFFFFF)`):
    - Badge circular 54×54, `linear-gradient(135deg,#E6C977,#C49A45)`, número Poppins 700
      22px branco, sombra `0 4px 12px rgba(196,154,69,.35)`.
    - Pílula "Nª PRIORIDADE": Poppins 10px 600, `letter-spacing: .12em`, uppercase, texto
      `#9A7626`, fundo `#FBF3DE`, `border-radius: 999px`, `padding: 4px 10px`.
    - H3 título do módulo: Poppins 600, 20px, `#0F4630`, `line-height: 1.2`.
  - **Corpo do card** (`padding: 4px 24px 24px`):
    - Descrição (14.5px, `#445349`).
    - **Botão secundário** "Acessar módulo": outline `1.5px #1E7A45`, texto `#0F4630`,
      Poppins 500 13px, `padding: 9px 15px`, `border-radius: 10px`, seta em `#1E7A45`.
    - **Painel "Materiais de aula"** (fundo `#F3F7F3`, `border-radius: 14px`,
      `padding: 18px 20px`):
      - Eyebrow "MATERIAIS DE AULA" (`#1E7A45`, Poppins 10.5px 600).
      - **Grid 2 colunas** (`gap: 12px`) de tiles brancas (borda `1px #E2EAE4`,
        `border-radius: 12px`, `padding: 13px 15px`, flex com ícone):
        - Tile 1: ícone "vídeo" (`#C49A45`) + número grande (Poppins 700 20px `#0F4630`)
          = `qtd_aulas` + legenda "videoaulas" (11.5px `#6A776E`).
        - Tile 2: ícone "relógio" + `tempo_aula` + legenda "de aula gravada".
      - **Linha "Atividades:"** — ícone "check/clipboard" (`#1E7A45`) + texto 13.5px
        `#445349`, rótulo em `<strong #0F4630>`. Separador `border-top: 1px #E2EAE4`.
      - **Linha "Programação:"** — ícone "calendário" + texto. Mesmo separador.

### 5. Card de encerramento
- `border-radius: 18px`, `overflow: hidden`, fundo `linear-gradient(135deg,#0F4630,#0A2C1E)`,
  `padding: 28px 30px`, `margin-top: 34px`. Anel dourado decorativo no canto inferior direito.
- Mensagem (15px, `line-height: 1.7`, `#EAF1EC`, `max-width: 560px`).
- Assinatura (após `border-top: 1px rgba(255,255,255,.14)`): avatar circular "CS" 42×42
  (gradiente dourado, texto `#0F4630`) + nome da equipe (Poppins 600 14px branco) +
  organização (12.5px `#A9C2B2`).

---

## Interações & comportamento
Documento estático/impresso — não há estados interativos além de **links** (`<a href>`)
nos botões "Acessar módulo", que devem apontar para as URLs dos cursos. Em PDF, os links
permanecem clicáveis (Chromium/Puppeteer preservam hyperlinks). Não há hover/animação.

### Comportamento de impressão (já implementado no CSS)
- `@page { size: A4; margin: 0 }`.
- O `<table class="doc-frame">` com `thead`/`tfoot` vazios cria a margem superior/inferior
  que se repete em cada página (0.5in). Margens laterais via `.doc { padding: 0 0.55in }`
  no `@media print`.
- `print-color-adjust: exact` força a impressão dos fundos coloridos.
- `break-inside: avoid` nos cards (`.module-card`, `.welcome-card`, `.closing-card`,
  `.hero`) evita que um card seja cortado entre duas páginas.

---

## Design Tokens

### Cores
| Token | Hex | Uso |
|---|---|---|
| Verde floresta | `#0F4630` | Títulos, botão primário, base dos gradientes escuros |
| Verde escuro 2 | `#0C3624` / `#0A2C1E` / `#071E15` | Paradas dos gradientes do hero/encerramento |
| Verde Rehagro | `#1E7A45` | Outlines, eyebrows de painel, ícones de info |
| Dourado | `#C49A45` | Badges, ícones de métrica, réguas, anéis |
| Dourado claro | `#E0C06A` / `#E6C977` | Eyebrow do hero, topo dos gradientes dourados |
| Dourado texto | `#9A7626` | Texto da pílula de prioridade |
| Tinta (corpo) | `#1B2B22` | Cor de texto base |
| Texto parágrafo | `#33433A` / `#445349` | Parágrafos |
| Texto suave | `#6A776E` | Legendas, observações |
| Linha/hairline | `#E2EAE4` | Bordas de cards e tiles |
| Creme | `#FBFAF4` / `#FBF3DE` | Fundo do welcome card / pílula de prioridade |
| Verde claro (painel) | `#F3F7F3` / `#F4F8F4` | Fundo do painel de materiais / header do card |
| Fundo da página | `#E7EBE6` | Fundo cinza-esverdeado (só em tela; impressão = branco) |
| Branco | `#FFFFFF` | Superfície do documento e tiles |
| Texto sobre verde | `#EAF1EC` / `#A9C2B2` | Mensagem e subtítulo do encerramento |

### Tipografia (escala COMPACTA — versão de 2 páginas)
- **Display/Títulos:** `Poppins` (500, 600, 700) — Google Fonts.
- **Corpo:** `Mulish` (400, 500, 600, 700) — Google Fonts.
- Import: `https://fonts.googleapis.com/css2?family=Poppins:wght@500;600;700&family=Mulish:wght@400;500;600;700&display=swap`
- H1 (nome do aluno) **31px**/1.05; H3 (títulos de card) **17px**; corpo/descrições
  **13–13.5px**/1.55–1.6; texto das métricas e info **12.5px**; legendas **11px**;
  números de métrica **18px/700**; eyebrows **9.5–12px** uppercase com
  `letter-spacing` 0.12–0.2em. **Não reduzir abaixo destes valores** (legibilidade impressa).

### Raios (versão compacta)
Tiles `10px` · botões `9px` · welcome card `14px` · module/closing card `15px` ·
hero `18px` · pílulas/badges/avatar `999px`/círculo · ícone do welcome `12px`.

### Sombras
- Documento (tela): `0 10px 40px rgba(14,58,41,.14)` (removida na impressão).
- Module card: `0 2px 10px rgba(15,70,48,.05)`.
- Badge dourado: `0 4px 12px rgba(196,154,69,.35)`.
- Ícone welcome: `0 4px 12px rgba(15,70,48,.25)`.

### Espaçamento (referências)
Valores da **versão compacta de 2 páginas** (use exatamente estes):
- Padding do documento: `32px 42px 36px` (tela) / `0 0.5in` (impressão).
- Bandas de margem por página (thead/tfoot): `0.38in`.
- Hero: `24px 30px 22px`. Intro: `margin 18px 2px 4px`.
- Section headers: `margin 22–24px 0 6–12px`. Welcome card: `16px 20px`.
- Module card: `margin-bottom 13px` (último `6px`). Module header: `13px 18px`.
  Corpo do card: `2px 18px 16px`.
- Painel de materiais: `14px 16px`. Gap do grid de tiles: `10px`. Tiles: `10px 13px`.
- Linhas de info (Atividades/Programação): `padding 8px 0`.
- Encerramento: `margin-top 16px`, `padding 20px 24px`.

> Estes números foram calibrados para fechar em **~1832px de altura ≈ 2 páginas A4**.
> A versão anterior (mais espaçada) gerava 3 páginas.

---

## Ícones
Todos são **SVG inline, traço (`stroke`), 24×24 viewBox**, sem dependência externa
(estilo Lucide/Feather). Reaproveite os SVGs do template:
- **Hero — curso:** livro aberto. **Hero — data:** calendário.
- **Welcome:** "play/curso". **Botões:** seta diagonal `↗` (arrow-up-right).
- **Métrica aulas:** câmera/vídeo. **Métrica tempo:** relógio.
- **Atividades:** clipboard com check. **Programação:** calendário.
Cores de traço conforme contexto (`#E0C06A` no hero, `#C49A45` nas métricas, `#1E7A45`
nas linhas de info, `#fff` no ícone do welcome).

---

## Assets
| Arquivo | Origem | Uso |
|---|---|---|
| `assets/rehagro-logo-white.png` | Logo extraído do .docx original e recolorido em branco | Cabeçalho (fundo verde) |
| `assets/rehagro-logo.png` | Logo extraído do .docx original (verde, fundo transparente) | Usos sobre fundo claro |

Recomendações:
- Para PDF 100% self-contained, **embuta o logo como data URI** (base64) — ver
  `inline_logo()` em `render.py`.
- Idem para as fontes: em produção, considere baixar Poppins/Mulish e servir via
  `@font-face` local, evitando dependência de rede na hora de gerar o PDF.
- Se tiver versões vetoriais (SVG) oficiais do logo Rehagro, prefira-as.

---

## Arquivos de referência no projeto de design
- Protótipo aprovado: `reference/Plano de Aula.dc.html` (abra no navegador).
- Template de produção: `template/plano_de_aula.html.j2`.
- Contrato de dados: `template/dados_exemplo.json`.
- Script de geração de PDF: `template/render.py`.
