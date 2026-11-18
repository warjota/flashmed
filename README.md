# FlashMed

Gerenciador de flashcards do Anki para estudar para a residência médica.

O FlashMed pega cards prontos, como os exportados de cursinhos, e cuida de três coisas:
- **limpa:** tira duplicados, cards fáceis demais e cards de baixo rendimento;
- **corrige e reescreve:** deixa cada card objetivo, no estilo do estudante;
- **completa:** cria cards novos onde falta conteúdo que cai em prova.

Cada decisão de excluir, manter ou criar se baseia em três fontes:
1. **peso do tema** numa planilha de prioridades;
2. **incidência real nas bancas-alvo**;
3. **julgamento clínico**, que perde quando o dado de prova diz o contrário.

> Este repositório guarda só o **projeto**: ferramentas, método, exemplos e templates.
> Baralhos, CSVs e material de terceiros ficam fora do git (veja `.gitignore`).

## Como funciona

```
CSV (frente;verso)  ─┐
                     ├─► decisões por card (ferramentas/decks/<tema>.py)
planilha de pesos  ──┤        │
incidência bancas  ──┘        ▼
                     build_csv_deck.py ─► <tema>.apkg  (excluídos não entram)
                              │
                              ├─► changelog.py ─► ALTERACOES_<tema>.md + <tema>_revisao.csv
                              └─► testar_importacao.py (numa cópia da coleção)
```

1. **Entrada:** o CSV do conteúdo (`frente;verso`) e, se houver, questões relacionadas.
2. **Pesquisa:** o peso do tema, o que mais cai nas bancas-alvo e as pegadinhas.
3. **Meta de cards:** ~100 cards por 1% de peso do tema, mínimo 10, ajuste de ±30%.
4. **Decisões:** cada linha do CSV vira uma de três:
   - **E**: editar, manter ou corrigir;
   - **X**: excluir, sempre com motivo;
   - **NOVOS**: cards de lacuna.
5. **Montagem:** o `.apkg` sai pronto para importar, com tags de rastreio:
   - `limpa::editado` e `limpa::corrigido`;
   - `fonte::medway` e `fonte::claude`;
   - `lacuna`;
   - `incidencia::<banca>`.
6. **Revisão:** o changelog mostra o antes e depois de cada card.

O método completo, com regras de redação, critérios de exclusão e formatação, está em [GUIA_FLASHCARDS_RESIDENCIA.md](GUIA_FLASHCARDS_RESIDENCIA.md). Os dados de incidência por banca estão em [dados/INCIDENCIA_BANCAS.md](dados/INCIDENCIA_BANCAS.md).

## Ferramentas

| Script | O que faz |
|---|---|
| `build_csv_deck.py` | Monta um deck novo a partir de um CSV e de um arquivo de decisões |
| `changelog.py` | Gera o changelog (.md) e a planilha de revisão (.csv) |
| `testar_importacao.py` | Importa o .apkg numa cópia da coleção e mostra o que mudaria |
| `dump.py` | Exporta todos os cards de uma coleção para JSON |
| `dups.py` | Acha duplicados por similaridade (TF-IDF) |
| `autoclean.py` | Limpeza automática: separa resposta e explicação, preenche lacunas (cloze) |
| `prioridades.py` | Cruza a planilha de pesos com os decks e gera a meta de cards por deck |
| `build_pilot.py` | Limpa um deck que já existe na coleção (usado no piloto de Diabetes) |

## Instalação

```bash
python -m venv .venv
.venv/Scripts/pip install -r requirements.txt   # Windows (Linux/macOS: .venv/bin/pip)
```

O `.apkg` moderno guarda a coleção em `collection.anki21b`, que é sqlite comprimido com zstd. As ferramentas usam o pacote `anki` do pip para ler e gravar.

## Uso: deck novo a partir de um CSV

```bash
cp exemplos/decisoes_exemplo.py ferramentas/decks/meu_tema.py   # preencher as decisões
python ferramentas/build_csv_deck.py ferramentas/decks/meu_tema.py entrada/meu_tema.csv col.db novos/Meu_Tema.apkg rows.json
python ferramentas/changelog.py rows.json novos/Meu_Tema_revisao.csv novos/ALTERACOES_Meu_Tema.md "Baralho::Tema"
python ferramentas/testar_importacao.py col.db novos/Meu_Tema.apkg "Baralho::Tema"
```

`col.db` é a coleção do usuário, extraída de um `.apkg`/`.colpkg` exportado do Anki. Ela é usada para o deck novo herdar o tipo de nota "Básico" (Frente / Verso / Comentário).

## Templates

- `templates/fluxograma.html`: fluxograma em HTML para cards de protocolo, testado no modo claro e no noturno do Anki.

## Próximos passos possíveis

- Virar uma **skill** do Claude Code, com o fluxo "manda o CSV → recebe o .apkg + changelog".
- Virar um **app**, com interface para revisar as decisões card a card antes de gerar o pacote.
