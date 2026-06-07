# Tarefas e Fases — Angra Lyrics

Roadmap completo para conclusão do projeto. Todas as tarefas serão executadas pela **IA (Cursor Agent)** sob sua orientação.

**Documentos relacionados:** [README.md](README.md) · [docs/DOCUMENTACAO_TECNICA.md](docs/DOCUMENTACAO_TECNICA.md)

**Legenda:** ⬜ pendente · 🟡 em progresso · ✅ concluído

---

## Critério de conclusão do projeto

O projeto estará **concluído** quando:

- [x] Os **10 álbuns de estúdio** tiverem `album.yaml` completo e todas as faixas em YAML
- [x] **100%** das faixas vocais com letra conferida, tradução 1:1 e referências
- [x] **100%** das faixas instrumentais com resumo e contexto
- [x] python scripts/validate.py passando sem erros
- [x] Site em site/ gerado e navegável (home → álbum → faixa)
- [x] Site publicado e acessível no **GitHub Pages**
- [x] Tabela de status do README atualizada com tudo ✅.

---

## Resumo de progresso

| Fase | Descrição | Status |
|------|-----------|--------|
| 0 | Fundação (infraestrutura) | ✅ |
| 1 | Piloto — Angels Cry | ✅ |
| 2 | Discografia (9 álbuns restantes) | ✅ |
| 3 | Refinamento do site | ✅ |
| 4 | Publicação e entrega final | ✅ |
| 5 | Extras (opcional) | ⬜ |

| Métrica | Total | Concluído |
|---------|-------|-----------|
| Álbuns | 10 | 10 |
| Faixas | 106 | 106 |
| Páginas HTML (aprox.) | ~117 | ~117 |

---

## Fase 0 — Fundação

Infraestrutura do repositório, pipeline de build e esqueleto do site.

### Documentação

- [x] README.md
- [x] docs/DOCUMENTACAO_TECNICA.md
- [x] TAREFAS.md (este arquivo)

### Estrutura de pastas

- [x] Criar `albums/` com subpastas dos 10 álbuns
- [x] Criar `albums/{slug}/assets/` em cada álbum
- [x] Criar `albums/{slug}/tracks/` em cada álbum
- [x] Criar `scripts/templates/` (Jinja2)
- [x] Criar `site/` (gerado pelo build; pode ter `.gitkeep` inicial)

### Templates e configuração

- [x] `templates/album.template.yaml`
- [x] `templates/track.template.yaml`
- [x] `scripts/build_config.yaml` (`base_path`, `site_title`, etc.)
- [x] `requirements.txt` (PyYAML, Jinja2, jsonschema)

### Scripts

- [x] `scripts/validate.py` — regras R01–R08
- [x] `scripts/build.py` — lê YAML, renderiza HTML, copia assets
- [x] Testar build com conteúdo vazio ou mock

### Site — esqueleto visual

- [x] `scripts/templates/base.html`
- [x] `scripts/templates/index.html`
- [x] `scripts/templates/album.html`
- [x] `scripts/templates/track.html`
- [x] `site/css/style.css` — tema escuro, tipografia legível
- [x] `site/js/main.js` — navegação básica

---

## Fase 1 — Piloto: Angels Cry (1993)

Validar pipeline completo com o primeiro álbum antes de escalar.

**Slug:** `01-angels-cry` · **Faixas:** 10 · **Idiomas:** EN / PT

### Álbum

- [x] Pesquisar história, gravação, conceito e recepção
- [x] Redigir `album.yaml` completo
- [x] Obter/documentar capa em `assets/cover.jpg` (ou URL em `sources.md`)
- [x] Criar `assets/sources.md`

### Faixas

- [x] 01 — Unfinished Allegro *(instrumental)*
- [x] 02 — Carry On
- [x] 03 — Time
- [x] 04 — Angels Cry
- [x] 05 — Stand Away
- [x] 06 — Never Understand
- [x] 07 — Wuthering Heights *(cover — Kate Bush)*
- [x] 08 — Streets of Tomorrow
- [x] 09 — Evil Warning
- [x] 10 — Lasting Child

### Entrega da fase

- [x] `validate.py` OK
- [x] `build.py` gera páginas do álbum no site
- [ ] Revisão visual local (`python -m http.server`)
- [x] Atualizar status no README

**Critério de aceite:** álbum 100% navegável no site com traduções e pesquisa.

---

## Fase 2 — Discografia completa

Produzir álbum a álbum na ordem abaixo. Para **cada álbum**, repetir:

1. Pesquisa do álbum → `album.yaml`
2. Pesquisa faixa a faixa → `tracks/*.yaml`
3. Assets e `sources.md`
4. `validate.py` + `build.py`
5. Atualizar README e este arquivo

---

### 2.1 — Rebirth (2001)

**Slug:** `04-rebirth` · **Faixas:** 10 · **Idioma:** EN

- [x] `album.yaml` + assets
- [x] 01 — In Excelsis *(instrumental)*
- [x] 02 — Nova Era
- [x] 03 — Millennium Sun
- [x] 04 — Acid Rain
- [x] 05 — Heroes of Sand
- [x] 06 — Unholy Wars
- [x] 07 — Rebirth
- [x] 08 — Judgement Day
- [x] 09 — Running Alone
- [x] 10 — Visions Prelude
- [x] Rebuild site + atualizar status

---

### 2.2 — Fireworks (1998)

**Slug:** `03-fireworks` · **Faixas:** 10 · **Idioma:** EN / PT (*Lisbon* em português)

- [x] `album.yaml` + assets
- [x] 01 — Wings of Reality
- [x] 02 — Petrified Eyes
- [x] 03 — Lisbon
- [x] 04 — Metal Icarus
- [x] 05 — Paradise
- [x] 06 — Mystery Machine
- [x] 07 — Fireworks
- [x] 08 — Extreme Dream
- [x] 09 — Gentle Change
- [x] 10 — Speed
- [x] Rebuild site + atualizar status

---

### 2.3 — Holy Land (1996)

**Slug:** `02-holy-land` · **Faixas:** 10 · **Idioma:** EN / PT · **Conceito:** descoberta do Brasil

- [x] `album.yaml` + assets
- [x] 01 — Crossing *(instrumental)*
- [x] 02 — Nothing to Say
- [x] 03 — Silence and Distance
- [x] 04 — Carolina IV
- [x] 05 — Holy Land
- [x] 06 — The Shaman
- [x] 07 — Make Believe
- [x] 08 — Z.I.T.O.
- [x] 09 — Deep Blue
- [x] 10 — Lullaby for Lucifer
- [x] Rebuild site + atualizar status

---

### 2.4 — Temple of Shadows (2004)

**Slug:** `05-temple-of-shadows` · **Faixas:** 13 · **Idioma:** EN · **Conceito:** caçador de sombras / Temple of Hate

- [x] `album.yaml` + assets
- [x] 01 — Deus Le Volt! *(intro)*
- [x] 02 — Spread Your Fire
- [x] 03 — Angels and Demons
- [x] 04 — Waiting Silence
- [x] 05 — Wishing Well
- [x] 06 — The Temple of Hate
- [x] 07 — The Shadow Hunter
- [x] 08 — No Pain for the Dead
- [x] 09 — Winds of Destination
- [x] 10 — Sprouts of Time
- [x] 11 — Morning Star
- [x] 12 — Late Redemption *(feat. Milton Nascimento)*
- [x] 13 — Gate XIII *(outro)*
- [x] Rebuild site + atualizar status

---

### 2.5 — Aurora Consurgens (2006)

**Slug:** `06-aurora-consurgens` · **Faixas:** 10 · **Idioma:** EN · **Tema:** saúde mental

- [x] `album.yaml` + assets
- [x] 01 — The Course of Nature
- [x] 02 — The Voice Commanding You
- [x] 03 — Ego Painted Grey
- [x] 04 — Breaking Ties
- [x] 05 — Salvation: Suicide
- [x] 06 — Window to Nowhere
- [x] 07 — So Near, So Far
- [x] 08 — Passing By
- [x] 09 — Scream Your Heart Out
- [x] 10 — Abandoned Fate
- [x] Rebuild site + atualizar status

---

### 2.6 — Aqua (2010)

**Slug:** `07-aqua` · **Faixas:** 10 · **Idioma:** EN / LA (*Viderunt te Aquæ*)

- [x] `album.yaml` + assets
- [x] 01 — Viderunt te Aquæ *(instrumental — latim)*
- [x] 02 — Arising Thunder
- [x] 03 — Awake from Darkness
- [x] 04 — Lease of Life
- [x] 05 — The Rage of the Waters
- [x] 06 — Spirit of the Air
- [x] 07 — Hollow
- [x] 08 — A Monster in Her Eyes
- [x] 09 — Weakness of a Man
- [x] 10 — Ashes
- [x] Rebuild site + atualizar status

---

### 2.7 — Secret Garden (2014)

**Slug:** `08-secret-garden` · **Faixas:** 10 · **Idioma:** EN

- [x] `album.yaml` + assets
- [x] 01 — Newborn Me
- [x] 02 — Black Hearted Soul
- [x] 03 — Final Light
- [x] 04 — Storm of Emotions
- [x] 05 — Violet Sky
- [x] 06 — Secret Garden
- [x] 07 — Upper Levels
- [x] 08 — Crushing Room
- [x] 09 — Perfect Symmetry
- [x] 10 — Silent Call
- [x] Rebuild site + atualizar status

---

### 2.8 — ØMNI (2018)

**Slug:** `09-omni` · **Faixas:** 11 · **Idioma:** EN / PT

- [x] `album.yaml` + assets
- [x] 01 — Light of Transcendence
- [x] 02 — Travelers of Time
- [x] 03 — Black Widow's Web
- [x] 04 — Insania
- [x] 05 — The Bottom of My Soul
- [x] 06 — War Horns
- [x] 07 — Caveman
- [x] 08 — Magic Mirror
- [x] 09 — Always More
- [x] 10 — ØMNI – Silence Inside
- [x] 11 — ØMNI – Infinite Nothing
- [x] Rebuild site + atualizar status

---

### 2.9 — Cycles of Pain (2023)

**Slug:** `10-cycles-of-pain` · **Faixas:** 12 · **Idioma:** EN / PT (*Vida Seca*)

- [x] `album.yaml` + assets
- [x] 01 — Cyclus Doloris *(instrumental)*
- [x] 02 — Ride into the Storm
- [x] 03 — Dead Man on Display
- [x] 04 — Tide of Changes – Part I
- [x] 05 — Tide of Changes – Part II
- [x] 06 — Vida Seca
- [x] 07 — Gods of the World
- [x] 08 — Cycles of Pain
- [x] 09 — Faithless Sanctuary
- [x] 10 — Here in the Now
- [x] 11 — Generation Warriors
- [x] 12 — Tears of Blood
- [x] Rebuild site + atualizar status

---

## Fase 3 — Refinamento do site

Melhorias de UX após a discografia principal estar no ar.

### Funcionalidades

- [x] Toggle **Original / Tradução / Ambos** na página de faixa
- [x] Busca client-side (`site/search-index.json` + JS)
- [x] Navegação entre faixas (anterior / próxima)
- [x] Breadcrumb consistente (Home → Álbum → Faixa)

### Visual e acessibilidade

- [x] Layout responsivo (mobile)
- [x] Contraste e legibilidade das letras revisados
- [x] Meta tags Open Graph (título, descrição, capa por álbum)
- [x] Favicon e identidade visual do site

### Qualidade

- [x] Testar todos os links internos
- [x] Testar caminhos com `base_path` do GitHub Pages
- [x] Rebuild final completo

---

## Fase 4 — Publicação (GitHub Pages)

### Repositório

- [x] Criar repositório no GitHub (`angra_lyrics`)
- [x] Push inicial com conteúdo + site gerado
- [x] Configurar **Settings → Pages → branch `main`, pasta `/site`**
- [x] Verificar URL pública funcionando

### Entrega final

- [x] README com tabela de status 100% ✅
- [x] TAREFAS.md com todas as fases marcadas
- [x] Site acessível e navegável de ponta a ponta
- [x] Informar URL final ao usuário

---

## Fase 5 — Extras (opcional)

Fora do escopo principal; executar somente se solicitado.

- [ ] EP *Evil Warning* (1994)
- [ ] EP *Freedom Call* (1996)
- [ ] EP *Hunters and Prey* (2002)
- [ ] Demo *Reaching Horizons* (1992)
- [ ] Faixas bônus de edições regionais (ex.: *Queen of the Night*)
- [ ] Domínio customizado no GitHub Pages
- [ ] PWA / modo offline

---

## Checklist por faixa (padrão IA)

Cada faixa vocal segue este fluxo interno:

- [ ] Coletar fontes (booklet, Metal Archives, entrevistas, Genius)
- [ ] Transcrever/conferir letra com áudio ou fonte oficial
- [ ] Dividir em seções (Verse, Chorus, Bridge…)
- [ ] Traduzir linha a linha (regra 1:1)
- [ ] Redigir `research.summary`
- [ ] Redigir `research.context`
- [ ] Preencher `research.references`
- [ ] Marcar `metadata.status: complete`

Faixas **instrumentais** substituem letra/tradução por `instrumental_description` + resumo/contexto.

---

## Checklist por álbum (padrão IA)

- [ ] Pesquisar contexto histórico e gravacão
- [ ] Montar `lineup` e `tracklist` oficiais
- [ ] Redigir `history.summary`, `recording`, `concept`, `reception`
- [ ] Documentar capa e imagens em `assets/`
- [ ] Produzir todas as faixas em `tracks/`
- [ ] Validar → build → atualizar README e TAREFAS

---

## Ordem de execução recomendada

```
Fase 0 (infra)
    ↓
Fase 1 (Angels Cry — piloto)
    ↓
Fase 2.1 → 2.9 (demais álbuns)
    ↓
Fase 3 (refinamento site)
    ↓
Fase 4 (GitHub Pages — ENTREGA)
    ↓
Fase 5 (opcional)
```

---

## Estimativa

| Escopo | Sessões IA (aprox.) |
|--------|---------------------|
| Fase 0 — infraestrutura | 1–2 |
| Fase 1 — Angels Cry | 1–2 |
| Fase 2 — 9 álbuns restantes | 12–20 |
| Fase 3 — refinamento site | 1 |
| Fase 4 — deploy | 1 |
| **Total** | **16–26 sessões** |

---

*Última atualização: 2026-06-06 — Fase 4 (GitHub Pages) concluída — https://bjscatena.github.io/angra_lyrics/*
