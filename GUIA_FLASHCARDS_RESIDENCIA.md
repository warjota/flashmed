# Guia de criação de flashcards: Residência Médica

Este guia é a referência que vou seguir sempre que criar ou limpar cards para você. Ele junta três coisas: o que a evidência mostra, o que funciona com FSRS no Anki e o estilo que você já usa quando edita os baralhos da Medway (aprendido da análise do baralho `02026`).

---

## 1. Princípios (o que a evidência sustenta)

1. **Os cards complementam as questões, não substituem.** Nos estudos com Anki, quem ia bem sempre fazia questões também. O card guarda o fato, e a questão treina como esse fato é cobrado.
2. **Constância pesa mais que volume.** O ganho vem de revisar todo dia. Cerca de 1.500 cards a mais deram só ~1 ponto a mais no Step 1. Mais cards ≠ mais nota.
3. **Cada card precisa valer o tempo de revisão dele.** Com FSRS a 85%, um card custa algo como 5–8 revisões no primeiro ano. Um card fácil ou repetido custa o mesmo tempo e não ensina nada.
4. **A decisão mistura quatro fontes, e nenhuma decide sozinha:**
   - o meu julgamento clínico;
   - a pesquisa sobre o tema (o que mais cai, prevalência, pegadinhas);
   - os dados das bancas-alvo: **PSU-GO, SES-GO, SES-DF, UnB (via ENARE) e ENAMED** (`dados/INCIDENCIA_BANCAS.md`);
   - a **planilha de prioridades da Medway**, com 294 focos e seus pesos (`dados/PRIORIDADES.md`).

   ENARE, USP e outras grandes servem de referência secundária. Quando Medway e bancas-alvo divergem, as bancas-alvo pesam mais, porque são as suas provas.
5. **Dado favorável vence a minha opinião.** Posso excluir por "fácil", "fisiologia básica" ou "baixo rendimento" sem ter dado. Mas, se houver dado mostrando que o fato é importante, o card fica, mesmo que seja fácil. Esse dado pode ser a incidência da banca, uma questão que você me mandar ou uma prioridade da Medway. Quando um dado salva um card, ele leva a etiqueta `incidencia::<fonte>`.

## 2. Regras de redação: o seu estilo

Estas regras foram tiradas dos cards que você já editou (HAS, Dislipidemia, Choque e Sepse, DPOC, Sala de Parto, Glomerulopatias).

| Regra | Como fica |
|---|---|
| **Pergunta direta, uma ideia por card** | "Qual a principal causa de HAS resistente?" → "SAHOS" |
| **Número de itens na frente** quando a resposta é lista | "Quais os critérios de internação na exacerbação da DPOC? (6)" |
| **Verso curto, só a resposta** | Sem repetir a frase da pergunta. Lacuna "O edema maleolar é efeito colateral de ____" → verso "Anlodipino" |
| **Listas com "-" e uma linha por item** | `-Anti-GAD65` / `-Anti-IA2` / ... |
| **Siglas consagradas** | IAM, DVA, ATB, iSGLT2, aGLP-1, BRD, SF 0,9%, HAS |
| **Setas e símbolos para causa → efeito** | "Hipoglicemia na madrugada → contrarreguladores → hiperglicemia no jejum" |
| **"OBS:" só para algo que cai** | Uma linha de complemento útil, como uma pegadinha, uma divergência de diretriz ou um mnemônico (ex.: FRICoT no APGAR) |
| **Imagem na frente quando ela é a pergunta** | ECG, fundo de olho, lesão de pele, instrumental |
| **Sem prefixo de tema na frente** | Removo o "Diabetes." / "Tireoide." da Medway, porque o deck já diz o tema |
| **Explicação longa nunca aparece no card** | Vai para o campo **Comentário**, que fica oculto no card e visível só no editor |
| **Diretriz/fonte quando há divergência** | "ADA: < 180 / SBD: < 160", "ADA 2024 (antes: 250)" |

### 2.1 Aprendido com as suas edições do deck Fraturas Ósseas (2026-11-17)

Objetivo acima de tudo: **o card tem que passar rápido**, para dar volume de revisão.

| Regra | Exemplo / detalhe |
|---|---|
| **"(n)" só em lista de 3 ou mais itens** | Pergunta no singular não leva número. "...causas de síndrome compartimental? (5)" |
| **A frente pergunta tudo o que o verso responde**, se for rápido | Embolia gordurosa: "Quais os achados? (3) / E a prevenção?" |
| **Tabela só quando o conteúdo é um esquema** (cenário × conduta, doses, alternativas) | Modelo aprovado: ATB da fratura exposta (Cenário × Esquema EV, alergia). Bordas `#888`, cabeçalho cinza translúcido, fonte 14px |
| **Fluxograma** (HTML, caixas verticais com setas) **só em protocolo** sequencial com decisão | Aprovado em 2026-11-17. Modelo: `novos/exemplo_fluxograma.html` (síndrome compartimental), com cores da tabela, borda vermelha na conduta crítica |
| **Imagem só quando acrescenta muito ao verso**, ou quando ela sozinha já é a resposta | Gustilo-Anderson: verso = só a tabela-imagem. NÃO colocar imagem decorativa nem em todo card, porque atrasa a revisão. Vale também para decks que o usuário já editou: posso sugerir uma imagem quando for realmente pertinente (no deck Fraturas ele já tinha posto as dele) |
| **Comparação "X x Y" na frente** para pares que se confundem | "Fratura de Colles x Smith" → 1. Colles + comum: desvio **dorsal** / 2. Smith + rara: desvio **volar** |
| **Negrito para dar ênfase** ao que diferencia ou é cobrado | **dorsal** × **volar**, **sem desvio** × **desvio parcial** |
| **Listas numeradas / mnemônico** quando ajuda a decorar | "**4 Ps:** 1. Pain 2. Parestesia/Paralisia 3. Palidez (tardio) 4. Pulso ausente (tardio)" |
| **OBS e justificativas continuam valendo** quando acrescentam | O usuário só cortou alguns pontualmente, porque já sabia o conteúdo. Não é regra geral |
| **Justificativa curta entre parênteses** quando cabe | "Não consolida (vascularização)" |
| **Complemento opcional em fonte menor** (`<sub>` ou `<span style="font-size: 80%">`) | Escafoide: exame físico (tabaqueira, tubérculo, pistonagem) |
| **Um item por linha** também em classificação | Gartland II e III em linhas separadas |
| **Siglas explicadas uma vez** | "DHS (Parafuso Deslizante do Quadril)" |
| **Imagens centralizadas** | `<div style="text-align: center;">` |

**Siblings** (cards irmãos, como estágio I / II / III):
- **Separar** quando cada item é cobrado isoladamente e confunde (estágios da HAS, classificação de Bethesda, perfis da IC).
- **Fundir em um card de lista/tabela** quando os itens só fazem sentido juntos (critérios de MODY, critérios de resolução da CAD, conduta pelo potássio, gravidade da CAD pelo pH/HCO₃⁻).

## 3. O que excluir ou suspender (critérios da limpeza)

| Motivo (etiqueta) | Critério |
|---|---|
| `duplicado` | O mesmo fato em outro card, mesmo com outra redação ou em outro deck. Fica o melhor; os outros saem |
| `fundido` | Card absorvido por um card de lista que reúne os irmãos |
| `facil-demais` | Fato que você sabe desde o ciclo básico ("células beta produzem insulina", "DM2 é o tipo mais prevalente") |
| `fisiologia-basica` | Mecanismo que não muda conduta nem é cobrado em prova de residência |
| `baixo-rendimento` | Curiosidade rara (lipodistrofias congênitas, "existem 14 tipos de MODY", percentuais de dieta) |
| `imagem-redundante` | Duas imagens para o mesmo diagnóstico sem achado diferente |

**Exceção que vence qualquer motivo:** se um dado de prova mostra que o fato é importante, o card fica. Isso inclui um tema no topo das bancas-alvo, uma questão sua ou uma prioridade da Medway, e vale até para um card fácil.

E o que eu **corrijo** (etiqueta `limpa::corrigido`): erros factuais do original e valores desatualizados (ex.: critérios de CAD/EHH do consenso ADA 2024, contraindicação das glitazonas, dose de insulina na CAD pediátrica). Quando há dúvida de diretriz vigente, uso `limpa::verificar` para você conferir na apostila.

## 4. Quantos cards por conteúdo

**Meta base: ~100 cards para cada 1% de peso do foco na planilha da Medway**, com mínimo de 10 cards. A regra foi calibrada no piloto: os focos de Diabetes somam 1,99% e o deck limpo ficou com 203 cards. No total, isso dá cerca de 10.000 cards para a prova toda. A meta de cada deck existente está em `dados/PRIORIDADES.md`.

Ajusto a meta pela incidência nas bancas-alvo, pelos fatos já cobrados nas suas questões e pelo meu julgamento. A extensão do capítulo não entra na conta. As faixas abaixo servem de conferência:

| Porte do tema | Exemplos | Cards |
|---|---|---|
| **Pequeno**: 1 aula curta, poucos pontos de corte | Síncope, Takotsubo, Hérnias femorais, Cefaleia em salvas | **15–40** |
| **Médio**: 1 aula completa com classificação + tratamento | Asma, DPOC, TEP, Pneumonia na infância, Anemias carenciais | **60–110** |
| **Grande**: muitas condutas, drogas e pontos de corte | Diabetes (pós-limpeza: **203**), Tireoide, SCA, HAS | **120–220** |
| **Imagem/padrão**: reconhecimento visual | ECG, fundo de olho, RX de tórax, instrumental cirúrgico | **1 card por padrão**, sem repetir o mesmo padrão |

Ajustes que aplico:
- **+25–30%** se o tema está no topo da PSU-GO, SES-GO, SES-DF, ENARE ou ENAMED, ou tem diretriz nova recente.
- **−30%** se o tema quase não cai nessas bancas (pelo dado ou, sem dado, pelo meu julgamento).
- Fatos fáceis entram quando o dado mostra que caem.

## 5. Fluxo de trabalho por conteúdo

**O que você me manda:** o banco de flashcards para criar, editar ou analisar, as questões relacionadas e, quando conseguir, as prioridades da Medway.

**O que eu faço:**
1. Pesquiso o tema: o que mais cai nas bancas-alvo, prevalência, condutas, pontos de corte, pegadinhas e diretrizes vigentes.
2. Cruzo as suas questões com os cards. Todo fato cobrado numa questão precisa ter um card.
3. Limpo os cards existentes (duplicados, fáceis, básicos, desnecessários). O dado de prova vence o meu motivo de exclusão.
4. **Procuro lacunas.** Fatos importantes sem card viram cards novos, com as etiquetas `fonte::claude` e `lacuna`. Isso vale também para os decks antigos que você já considera fechados.
5. Corrijo erros e desatualizações (`limpa::corrigido`) e marco as dúvidas de diretriz (`limpa::verificar`).

## 6. Formato de entrega

Para cada conteúdo, entrego:
1. Um `.apkg` pronto para importar, no deck certo dentro de `02026::...`, com o seu tipo de nota **Básico** (Frente / Verso / Comentário).
2. Uma planilha `.csv` com os cards, para revisar antes se quiser.
3. Etiquetas: `fonte::claude`, o tema e `alta-incidencia` nos cards que mais caem.

## 7. Configuração do Anki (sua predefinição "Config Teste")

O que já está bom:
- **FSRS ativo e otimizado**, com **retenção desejada 0,85**. É o ponto ideal para muitos cards: subir para 0,90 aumenta bastante a carga diária.
- Passos de aprendizado curtos (25 min / 12 h) e de reaprendizado (10 min / 6 h). Funcionam bem com FSRS.

O que eu mudaria:
- **Novos cards/dia = 9999** é a causa do "acúmulo". Recomendo **limitar a 30–50 por dia** e não desbloquear de uma vez. A conta: com ~3.700 novos, 40/dia leva ~3 meses. Se a prova estiver mais perto, priorize os decks de maior incidência em vez de aumentar o limite.
- **Revisões/dia = 9999**: pode manter. Revisão atrasada é pior que revisão feita.
- **Sanguessuga (leech) = suspender com 4 erros**: troque para **"Só etiquetar"**. O card que você erra 4 vezes geralmente é importante e está mal escrito. Me mande esses cards (`tag:leech`) que eu reescrevo.
- Rode **"Otimizar"** os parâmetros do FSRS uma vez por mês, conforme o histórico cresce.

## 8. Rotina de estudo sugerida

1. Aula ou resumo do tema → **questões do tema** no mesmo dia ou no seguinte.
2. Libere os cards do deck desse tema (os novos do tema, não de tudo).
3. **Todo erro de questão vira card** (ou edita um card existente). É o card que mais rende.
4. Revisão diária sem pular. Se atrasar, faça as revisões antes de liberar novos.
5. Teto de ~2–3 h/dia de Anki. O resto do tempo vai para questões.
