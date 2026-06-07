# Documentação Técnica — Angra Lyrics

Este documento descreve **como** o projeto será estruturado, produzido pela IA, validado e publicado como site estático no GitHub Pages.

---

## 1. Visão geral da arquitetura

Pipeline em três camadas: **conteúdo** (YAML) → **build** (Python) → **site** (HTML estático no GitHub Pages).

```
┌─────────────────────────────────────────────────────────┐
│              Camada de conteúdo (fonte)                  │
│  albums/{slug}/album.yaml + tracks/*.yaml + assets/     │
│  Pesquisa, letras, traduções — produzido pela IA        │
└──────────────────────────┬──────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────┐
│              Camada de build (scripts/)                 │
│  validate.py  →  conferência de schema e integridade    │
│  build.py     →  gera HTML/CSS/JS em site/             │
└──────────────────────────┬──────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────┐
│           Camada de publicação (site/)                  │
│  HTML estático · caminhos relativos · GitHub Pages      │
└─────────────────────────────────────────────────────────┘
```

**Princípios:**

- **YAML como fonte da verdade** — o site é sempre regenerado; nunca editar HTML manualmente
- **Um arquivo por faixa** — organização clara e build incremental por álbum
- **Metadados tipados** — campos fixos garantem consistência entre os 10 álbuns
- **Separação conteúdo/apresentação** — trocar layout do site sem reescrever pesquisa
- **Rastreabilidade** — referências obrigatórias em afirmações factuais
- **Projeto solo** — toda produção editorial feita pela IA sob sua orientação; sem fluxo de PR/contribuição externa

---

## 2. Modelo de trabalho: IA como produtora

### 2.1 Papéis

| Papel | Responsabilidade |
|-------|------------------|
| **Você** | Direção do projeto, revisão opcional, publicação no GitHub |
| **IA (Cursor Agent)** | Pesquisa, redação, YAML, imagens/links, build e deploy |

### 2.2 Ciclo por álbum

```
Solicitação  →  Pesquisa web  →  YAML (album + tracks)  →  validate.py
     →  build.py  →  site/ atualizado  →  status no README
```

A IA executa cada etapa de forma autônoma, consultando fontes reais (web, encartes referenciados, bases de metadados). Você pode pedir um álbum por vez ou a discografia inteira em sequência.

### 2.3 Ordem de produção sugerida

1. **Angels Cry** — piloto (10 faixas, mix PT/EN, marco histórico)
2. Rebirth → Fireworks → Holy Land
3. Temple of Shadows → Aurora Consurgens
4. Aqua → Secret Garden → ØMNI → Cycles of Pain

Após cada álbum concluído: validar, buildar site, atualizar tabela de status.

---

## 3. Convenções de nomenclatura

### 3.1 Slugs de álbum

Padrão: `{ordem}-{nome-kebab-case}`

| Álbum | Slug |
|-------|------|
| Angels Cry | `01-angels-cry` |
| Holy Land | `02-holy-land` |
| Fireworks | `03-fireworks` |
| Rebirth | `04-rebirth` |
| Temple of Shadows | `05-temple-of-shadows` |
| Aurora Consurgens | `06-aurora-consurgens` |
| Aqua | `07-aqua` |
| Secret Garden | `08-secret-garden` |
| ØMNI | `09-omni` |
| Cycles of Pain | `10-cycles-of-pain` |

Caracteres especiais (Ø, acentos) são normalizados no slug; o título oficial permanece no campo `title`.

### 3.2 Slugs de faixa

Padrão: `{ordem}-{titulo-kebab-case}.yaml`

Exemplos: `01-carry-on.yaml`, `04-angels-and-demons.yaml`

### 3.3 Imagens (`assets/`)

| Arquivo | Descrição |
|---------|-----------|
| `cover.jpg` | Capa principal (mín. 800×800 px) |
| `back.jpg` | Contracapa (opcional) |
| `booklet-*.jpg` | Páginas do encarte |
| `band-*.jpg` | Fotos promocionais do período |
| `sources.md` | Origem e licença de cada imagem |

Quando não houver scan próprio, a IA documenta URL externa em `sources.md` e o build pode referenciar a imagem remotamente ou copiar para `site/assets/`.

---

## 4. Schema: `album.yaml`

```yaml
id: "01-angels-cry"
title: "Angels Cry"
type: "studio"
release:
  date: "1993-10-01"
  label: "Eldorado"
  countries: ["Brazil", "Japan", "Europe"]

lineup:
  - name: "Andre Matos"
    role: "vocals"
  - name: "Rafael Bittencourt"
    role: "guitars, backing vocals"

tracklist:
  - number: 1
    file: "01-carry-on.yaml"
    title: "Carry On"
    duration: "4:27"
    instrumental: false

history:
  summary: |
    Parágrafo introdutório: conceito, momento na carreira, recepção.
  recording: |
    Estúdios, produtores, curiosidades.
  concept: |
    Fio condutor temático.
  reception: |
    Crítica, charts, legado.
  references:
    - title: "Entrevista com Rafael Bittencourt (1994)"
      url: "https://..."
      type: "interview"

assets:
  cover: "assets/cover.jpg"
  gallery:
    - "assets/booklet-01.jpg"
```

**Campos obrigatórios:** `id`, `title`, `type`, `release.date`, `tracklist`, `history.summary`, `assets.cover`

---

## 5. Schema: faixa (`tracks/*.yaml`)

```yaml
id: "01-angels-cry-01-carry-on"
album_id: "01-angels-cry"
track_number: 1
title: "Carry On"
title_alternate:
  - "União das Almas"
language: "en"
authors:
  - "Rafael Bittencourt"
  - "Andre Matos"
duration: "4:27"

lyrics:
  - section: "Verse 1"
    lines:
      - original: "It's time to go, the sun is rising"
        translation: "É hora de ir, o sol está nascendo"
        notes: ""

research:
  summary: |
    Do que a música trata, tom, papel no álbum.
  themes:
    - "superação"
  context: |
    Circunstâncias de composição, relação com outras faixas.
  interpretation: |
    Análise interpretativa (claramente marcada como tal).
  references:
    - title: "Metal Kingdom — Angels Cry"
      url: "https://..."
      type: "database"
      accessed: "2026-06-06"

metadata:
  status: "complete"          # draft | complete
  last_updated: "2026-06-06"
```

**Campos obrigatórios (com vocal):** `id`, `album_id`, `track_number`, `title`, `language`, `lyrics`, `research.summary`, `research.context`

**Instrumentais:** `instrumental: true`, `instrumental_description`, sem bloco `lyrics`.

---

## 6. Regras de tradução linha a linha

### 6.1 Correspondência 1:1

Cada linha em `lines` tem `original` + `translation` no mesmo objeto. A IA não agrega duas linhas originais em uma tradução.

### 6.2 Idioma alvo

| `language` | Tradução em |
|------------|-------------|
| `en` | Português (BR) |
| `pt` | Inglês |
| `la` | Português (BR) + `notes` etimológicas |
| `it` | Português (BR) |
| `instrumental` | N/A |

### 6.3 Qualidade

- Fidelidade sobre rima forçada
- Conferência com fontes oficiais; transcrições online só como apoio
- Double entendres e citações em `notes`

---

## 7. Metodologia de pesquisa (IA)

### 7.1 Por faixa — 5 etapas

```
Coleta de fontes  →  Letra oficial  →  Tradução  →  Resumo + contexto  →  Validação
```

| Prioridade | Fonte |
|------------|-------|
| 1 | Encarte / booklet oficial |
| 2 | Site oficial, redes da banda |
| 3 | Entrevistas dos compositores |
| 4 | Metal Kingdom, Discogs, Wikipedia |
| 5 | Genius, Dark Lyrics (conferir sempre) |

### 7.2 Por álbum

1. Contexto pré-gravação e lineup
2. Processo criativo e estúdios
3. Identidade visual (capa, arte)
4. Lançamento por região
5. Legado e reedições

---

## 8. Site estático — especificação

### 8.1 Objetivo

Site HTML puro (sem backend), gerado por `scripts/build.py`, hospedado no **GitHub Pages** a partir da pasta `site/`.

### 8.2 Estrutura de páginas geradas

```
site/
├── index.html                          # home: grid dos 10 álbuns
├── css/
│   └── style.css                       # tema escuro, tipografia legível
├── js/
│   └── main.js                         # navegação, toggle tradução
├── assets/
│   └── covers/                         # capas copiadas do build
└── albums/
    ├── 01-angels-cry/
    │   ├── index.html                  # história do álbum, galeria, tracklist
    │   └── carry-on.html               # letra + tradução + pesquisa
    └── ...
```

### 8.3 Páginas e conteúdo

| Página | Conteúdo |
|--------|----------|
| **Home** | Grid com capas, ano, link para cada álbum |
| **Álbum** | Capa, ficha técnica, elenco, história (`history.*`), galeria, lista de faixas |
| **Faixa** | Título, autores, duração; letra original e tradução lado a lado (ou toggle); resumo, contexto, temas, referências |

### 8.4 Layout da página de faixa

```
┌─────────────────────────────────────────────────────┐
│  ← Angels Cry · Faixa 1                             │
│  Carry On                                           │
│  Rafael Bittencourt, Andre Matos · 4:27             │
├─────────────────────────────────────────────────────┤
│  [ Original ] [ Tradução ] [ Ambos ]   ← toggle     │
├──────────────────────┬──────────────────────────────┤
│  Verse 1             │  É hora de ir...             │
│  It's time to go...  │  (alinhado linha a linha)    │
├──────────────────────┴──────────────────────────────┤
│  Sobre a música                                     │
│  (research.summary)                                 │
├─────────────────────────────────────────────────────┤
│  Contexto                                           │
│  (research.context)                                 │
├─────────────────────────────────────────────────────┤
│  Referências                                        │
│  (links das fontes)                                 │
└─────────────────────────────────────────────────────┘
```

### 8.5 Stack do site

| Componente | Escolha | Motivo |
|------------|---------|--------|
| HTML | Gerado por Python | Zero dependência de runtime no GitHub Pages |
| CSS | Arquivo único customizado | Visual temático (metal/escuro), sem framework pesado |
| JS | Vanilla mínimo | Toggle de idioma, menu mobile |
| Build | Python 3.11+ + Jinja2 | Templates HTML reutilizáveis |
| Deploy | GitHub Pages (`/site`) | Gratuito, HTTPS, integrado ao repo |

**Sem** Node.js, React ou banco de dados — o site deve funcionar abrindo os arquivos localmente ou via GitHub Pages.

### 8.6 Compatibilidade com GitHub Pages (subpath)

Repositórios de projeto usam URL `https://<user>.github.io/<repo>/`. O build deve:

- Usar caminhos relativos (`../css/style.css`) ou prefixo configurável `BASE_PATH`
- Gerar links internos com prefixo `/angra_lyrics/` quando necessário
- Copiar assets para dentro de `site/assets/`

Configuração em `scripts/build_config.yaml`:

```yaml
base_path: "/angra_lyrics"    # vazio "" para user.github.io root
output_dir: "site"
site_title: "Angra Lyrics"
```

### 8.7 Templates Jinja2 (em `scripts/templates/`)

```
scripts/templates/
├── base.html           # layout comum (nav, footer)
├── index.html          # home
├── album.html          # página do álbum
└── track.html          # página da faixa
```

`build.py` carrega YAML de `albums/`, renderiza templates, escreve em `site/`.

---

## 9. Scripts

### 9.1 `scripts/validate.py`

Valida integridade antes do build. Falha (`exit 1`) quando:

| Regra | Descrição |
|-------|-----------|
| R01 | Campo obrigatório ausente |
| R02 | `tracklist[].file` inexistente |
| R03 | Faixa vocal sem tradução |
| R04 | `album_id` ≠ pasta pai |
| R05 | `track_number` duplicado |
| R06 | Instrumental com bloco `lyrics` |
| R07 | `assets.cover` ausente |
| R08 | Data inválida |

### 9.2 `scripts/build.py`

```
python scripts/build.py
```

1. Executa validação (ou `--skip-validate` para preview)
2. Lê todos os `album.yaml` e `tracks/*.yaml`
3. Copia imagens para `site/assets/`
4. Renderiza templates Jinja2
5. Gera `site/index.html` + páginas por álbum/faixa
6. Escreve `site/search-index.json` (opcional, para busca client-side futura)

### 9.3 Dependências Python

```
# requirements.txt
PyYAML>=6.0
Jinja2>=3.1
jsonschema>=4.0
```

---

## 10. GitHub Pages — deploy

### 10.1 Configuração no repositório

1. Push do repositório para GitHub
2. **Settings → Pages**
3. Source: **Deploy from a branch**
4. Branch: `main`, folder: **`/site`**
5. Save — site disponível em ~1 minuto

### 10.2 Fluxo de atualização

Sempre que a IA concluir um álbum ou revisar conteúdo:

```bash
python scripts/validate.py
python scripts/build.py
git add albums/ site/
git commit -m "feat(angels-cry): complete album content and rebuild site"
git push
```

GitHub Pages republica automaticamente após o push.

### 10.3 Preview local

```bash
python scripts/build.py
python -m http.server 8080 --directory site
# Abrir http://localhost:8080
```

---

## 11. Fases de implementação

### Fase 0 — Fundação

- [x] README e documentação técnica
- [x] Templates YAML de referência
- [x] Estrutura de pastas dos 10 álbuns
- [x] `scripts/validate.py` e `scripts/build.py` (esqueleto)
- [x] Templates Jinja2 e CSS base do site

### Fase 1 — Piloto: Angels Cry

- [ ] `album.yaml` + 10 faixas completas (IA pesquisa e redige)
- [ ] Assets de capa documentados
- [ ] Site gerado com álbum navegável
- [ ] Deploy de teste no GitHub Pages

**Critério de aceite:** 100% das faixas vocais com tradução 1:1, referências, site funcional.

### Fase 2 — Discografia completa

Produzir álbum a álbum (IA), rebuild do site a cada entrega, atualizar status no README.

### Fase 3 — Refinamento do site

- Busca client-side (`search-index.json`)
- Toggle original/tradução/ambos
- Responsivo mobile
- Meta tags Open Graph para compartilhamento

### Fase 4 — Extras (opcional)

- EPs e demos
- PWA offline
- Domínio customizado no GitHub Pages

---

## 12. Riscos e mitigações

| Risco | Mitigação |
|-------|-----------|
| Letras incorretas online | IA confere múltiplas fontes + referências |
| Direitos autorais (letras) | Projeto educacional; sem monetização; créditos aos compositores |
| Imagens protegidas | URLs externas ou documentação em `sources.md` |
| Alucinação da IA em fatos | Referências obrigatórias; marcar incertezas em `notes` |
| Escopo infinito | 10 álbuns de estúdio como escopo fechado |
| GitHub Pages subpath quebrado | `base_path` no build config |

---

## 13. Estimativa de esforço (sessões IA)

Por faixa vocal: ~1 sessão de pesquisa + redação.

| Escopo | Estimativa |
|--------|------------|
| 1 álbum (~10 faixas) | 1–3 sessões de chat |
| Discografia completa (~115 faixas) | 15–25 sessões |
| Site + build pipeline | 1–2 sessões |

Você pode acelerar pedindo álbum inteiro por mensagem ou ir faixa a faixa.

---

## 14. Próximos passos

1. Criar estrutura de pastas e templates YAML
2. Implementar `validate.py` e `build.py` com layout base
3. IA produz **Angels Cry** completo (pesquisa + YAML + site)
4. Publicar no GitHub Pages

---

## Apêndice A — Seções de letra

`Intro`, `Verse`, `Verse 2`, `Pre-Chorus`, `Chorus`, `Bridge`, `Solo`, `Interlude`, `Outro`, `Recitative`, `Spoken`, `Refrain`

## Apêndice B — Tipos de referência

`booklet`, `interview`, `article`, `video`, `lyrics`, `database`, `book`, `social`

## Apêndice C — Discografia

| # | Álbum | Ano | Faixas (aprox.) | Idioma predominante |
|---|-------|-----|-----------------|---------------------|
| 1 | Angels Cry | 1993 | 10 | EN / PT |
| 2 | Holy Land | 1996 | 14 | EN / PT |
| 3 | Fireworks | 1998 | 11 | EN |
| 4 | Rebirth | 2001 | 11 | EN |
| 5 | Temple of Shadows | 2004 | 11 | EN |
| 6 | Aurora Consurgens | 2006 | 13 | EN / PT |
| 7 | Aqua | 2010 | 11 | EN |
| 8 | Secret Garden | 2014 | 10 | EN |
| 9 | ØMNI | 2018 | 12 | EN / PT |
| 10 | Cycles of Pain | 2023 | 11 | EN |

---

*Versão 1.1 — 2026-06-06*
