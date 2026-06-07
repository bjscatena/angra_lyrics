# Angra Lyrics — Levantamento Artístico

Projeto pessoal de documentação e pesquisa sobre a discografia da banda brasileira **Angra**. O objetivo é reunir, de forma organizada e aprofundada, as letras originais, traduções frase a frase, resumos interpretativos e o contexto histórico de cada faixa — além da história e do material visual de cada álbum.

**Entrega final:** um site HTML estático publicável no **GitHub Pages**, gerado a partir do conteúdo pesquisado e estruturado neste repositório.

## Objetivo

Construir um acervo consultável — em YAML no repositório e em HTML na web — que funcione como referência artística e cultural da obra da Angra, permitindo:

- Ler cada música na **língua original** com **tradução alinhada linha a linha**
- Entender o **significado** e a **intenção** de cada composição
- Situar cada faixa no **contexto do álbum**, da carreira da banda e do cenário do power/progressive metal
- Conhecer a **história de gravação**, conceito e arte de cada release
- Navegar tudo isso em um **site estático** hospedado gratuitamente no GitHub Pages

## Modelo de trabalho

Este **não é um projeto open source de contribuição**. É um levantamento pessoal produzido sob sua orientação, com a **IA (Cursor Agent) executando**:

- Pesquisa de fontes (encartes, entrevistas, bases confiáveis)
- Transcrição e conferência de letras
- Tradução linha a linha
- Redação de resumos, contexto e história dos álbuns
- Montagem dos arquivos YAML
- Geração do site HTML e deploy no GitHub Pages

Seu papel: definir direção, revisar conteúdo quando quiser e publicar o repositório.

## Escopo

### Incluído (fase principal)

| Categoria | Itens |
|-----------|-------|
| Álbuns de estúdio | Angels Cry, Holy Land, Fireworks, Rebirth, Temple of Shadows, Aurora Consurgens, Aqua, Secret Garden, ØMNI, Cycles of Pain |
| Por álbum | Capa, fotos, ficha técnica, história do álbum |
| Por faixa | Letra original, tradução, resumo, contexto, referências |
| Site | HTML estático gerado automaticamente, pronto para GitHub Pages |

### Escopo futuro (opcional)

- EPs (*Evil Warning*, *Freedom Call*, *Hunters and Prey*, etc.)
- Demos (*Reaching Horizons*, *Acid Rain*)
- Singles e faixas bônus exclusivas de edições regionais

## Estrutura do repositório

```
angra_lyrics/
├── README.md
├── TAREFAS.md                    # roadmap e checklist completo
├── docs/
│   └── DOCUMENTACAO_TECNICA.md   # especificação completa
├── albums/                       # fonte da verdade (YAML + imagens)
│   ├── 01-angels-cry/
│   │   ├── album.yaml
│   │   ├── assets/
│   │   └── tracks/
│   └── ...
├── scripts/
│   ├── validate.py               # validação do conteúdo
│   └── build.py                  # gera o site estático
└── site/                         # saída do build → GitHub Pages
    ├── index.html
    ├── css/
    ├── js/
    └── albums/
```

- **`albums/`** — conteúdo editorial em YAML (pesquisado e redigido pela IA)
- **`scripts/build.py`** — lê os YAML e gera HTML em `site/`
- **`site/`** — artefato publicável; GitHub Pages aponta para esta pasta

Detalhes de schema, build e deploy estão em [`docs/DOCUMENTACAO_TECNICA.md`](docs/DOCUMENTACAO_TECNICA.md).

## Formato do conteúdo

### Álbum (`album.yaml`)

Informações editoriais, elenco na gravação, conceito geral, linha do tempo de produção e caminhos para as imagens em `assets/`.

### Faixa (`tracks/*.yaml`)

- Metadados (título, autores, idioma, duração)
- Letra original dividida em **blocos** (verso, refrão, ponte…)
- Cada linha com sua **tradução correspondente**
- Seções de **resumo** e **contexto**
- **Referências** das fontes consultadas na pesquisa

Exemplo simplificado:

```yaml
title: "Carry On"
language: en
lyrics:
  - section: "Verse 1"
    lines:
      - original: "It's time to go, the sun is rising"
        translation: "É hora de ir, o sol está nascendo"
research:
  summary: |
    Faixa de abertura que estabelece o tom épico do álbum...
  context: |
    Composta durante as sessões de Angels Cry, reflete...
```

## Idiomas das letras

A Angra alterna **português**, **inglês** e, pontualmente, **latim** e **italiano**. A regra do projeto:

| Idioma original | Tradução alvo |
|-----------------|---------------|
| Inglês | Português (BR) |
| Português | Inglês |
| Latim / Italiano | Português (BR) + nota etimológica quando relevante |

Instrumentais não possuem bloco de letra, mas incluem resumo e contexto.

## Metodologia de pesquisa (executada pela IA)

1. **Fonte primária da letra** — encarte oficial, site da banda, entrevistas dos compositores
2. **Conferência cruzada** — ao menos uma fonte secundária confiável (Metal Kingdom, Genius, entrevistas)
3. **Contexto** — notas de álbum, making-of, entrevistas, críticas contemporâneas
4. **Registro** — toda afirmação não óbvia recebe referência em `research.references`

## Publicação no GitHub Pages

Após o build, o site é servido a partir da pasta `site/`:

1. Repositório publicado no GitHub
2. **Settings → Pages → Build and deployment → Deploy from a branch**
3. Branch `main`, pasta `/site`
4. URL resultante: `https://<usuario>.github.io/angra_lyrics/`

O script de build já configura caminhos relativos compatíveis com subpath do GitHub Pages.

## Status do projeto

| Álbum | Metadados | Faixas | Pesquisa | Site |
|-------|-----------|--------|----------|------|
| Angels Cry (1993) | ✅ | ✅ | ✅ | ✅ |
| Holy Land (1996) | ✅ | ✅ | ✅ | ✅ |
| Fireworks (1998) | ✅ | ✅ | ✅ | ✅ |
| Rebirth (2001) | ✅ | ✅ | ✅ | ✅ |
| Temple of Shadows (2004) | ✅ | ✅ | ✅ | ✅ |
| Aurora Consurgens (2006) | ✅ | ✅ | ✅ | ✅ |
| Aqua (2010) | ✅ | ✅ | ✅ | ✅ |
| Secret Garden (2014) | ✅ | ✅ | ✅ | ✅ |
| ØMNI (2018) | ✅ | ✅ | ✅ | ✅ |
| Cycles of Pain (2023) | ✅ | ✅ | ✅ | ✅ |

Legenda: ⬜ pendente · 🟡 em progresso · ✅ concluído

## Licença e aviso legal

- **Letras**: propriedade dos compositores e editoras. Projeto de caráter **educacional e artístico**, sem fins comerciais.
- **Imagens de capa**: preferir URLs oficiais ou material documentado em `assets/sources.md`; evitar redistribuir artes protegidas sem autorização.
- **Conteúdo de pesquisa**: redação produzida no levantamento; uso pessoal e consulta pública via GitHub Pages.

## Referências úteis

- [Site oficial — Angra](https://angra.com.br/)
- [Angra — Wikipedia (EN)](https://en.wikipedia.org/wiki/Angra_(band))
- [Metal Kingdom — Angra](https://www.metalkingdom.net/band/angra-31)

---

*Projeto pessoal de levantamento artístico. Power metal made in Brazil.*
