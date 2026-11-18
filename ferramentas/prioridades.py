"""Cruza a planilha da Medway (pesos por foco) com os decks do baralho 02026
e com os dados das bancas-alvo (dados/INCIDENCIA_BANCAS.md).

Uso: python prioridades.py <medway.csv> <cards.json> <saida.md>

Regra de conversão (calibrada no piloto Diabetes):
  meta de cards ≈ 100 cards por 1% de peso Medway  (Diabetes CM+PREV+PED = 1,99% → ~199; o piloto ficou com 198)
  → baralho completo da prova ≈ 10.000 cards.
  Mínimo de 10 cards para focos Prioritários/Alta prevalência.
  Ajuste por julgamento clínico continua valendo (±30%).
Prioridade combinada = peso Medway × 1,25 se a banca-alvo confirma o tema (Medcof PSU-GO / SES-GO / SES-DF).
"""
import csv, json, sys, collections

# deck (sem o prefixo 02026::) -> ranking_global dos focos Medway que ele cobre
MAPA = {
 'CM::Cardiologia::HAS': [21, 89],
 'CM::Cardiologia::Insuficiência Cardíaca': [43],
 'CM::Cardiologia::Síndrome Metabólica e Dislipidemia': [123, 169],
 'CM::Cardiologia::Síndrome Coronariana, DAA, Pericardite e Takotsubo': [15],
 'CM::Cardiologia::Valvopatias e Cardiomiopatias': [28],
 'CM::Cardiologia::Arritmias, Síncope e PCR': [74, 236],
 'CM::Psiquiatria::Transtornos Mentais': [71, 85, 151],
 'CM::Psiquiatria::Abuso de Substâncias': [81, 165, 222],
 'CM::Pneumologia::TVP, TEP e Hipertensão Pulmonar': [189, 243, 237],
 'CM::Pneumologia::DPOC': [38],
 'CM::Pneumologia::Asma': [38, 16],
 'CM::Hematologia::Anemias e Hemoglobinopatias': [122],
 'PED::Anemias e Hemoglobinopatias Pediatricas': [67],
 'CM::Hematologia::Onco-Hemato': [70],
 'CM::Hematologia::Distúrbios da hemostasia': [61],
 'CM::Intensiva::Choque e Sepse': [45],
 'CM::Intensiva::AVC': [52],
 'CM::Endocrino::Tireoide': [46, 107],
 'CM::Endocrino::Diabetes': [14, 36, 105],
 'CM::Neurologia::Cefaleias': [110],
 'CM::GO::Incontinência Urinária e Prolapso': [42],
 'CIR::Anestesia': [54],
 'CIR::xABCDE': [30],
 'CIR::Vias Biliares': [32],
 'CIR::Hérnias': [31],
 'CIR::Trauma Abdominal': [58],
 'CIR::Técnicas Operatórias': [119],
 'CIR::Abdome Agudo Inflamatório': [8],
 'PED::Pneumonias e Síndromes Gripais': [68],
 'PED::Imunizações': [10],
 'SUS::Imunização': [225],
 'PED::Glomerulopatias e Tubulopatias': [76],
 'PED::Doenças Respiratórias Neonatais': [152],
 'PED::Sala de Parto': [114],
 'PED::Distúrbios Estaturais e Puberais': [55],
 'HETRIN': [83],
}
# focos com 2 decks (Distúrbios Obstrutivos 38 = DPOC + Asma) dividem o peso
COMPARTILHADO = {38: 2}

# ranking_global -> evidência das bancas-alvo (Medcof, edição anterior; nº de questões)
BANCAS = {
 3: 'APS: PSU-GO 34, SES-DF 29, SES-GO 12', 6: 'Epidemiologia clínica: SES-GO 30, PSU-GO 13, SES-DF 12',
 13: 'Epidemiologia clínica (idem)', 35: 'Epidemiologia clínica (idem)',
 64: 'Indicadores: SES-GO 23, SES-DF 5', 73: 'Indicadores (idem)',
 4: 'Vigilância: SES-GO 11, SES-DF 4', 20: 'Vigilância (idem)', 12: 'Vigilância (idem)',
 27: 'SUS/RAS: SES-GO 15, SES-DF 11, PSU-GO 6', 147: 'SUS (idem)',
 1: 'Crescimento: PSU-GO 10+4+4, SES-DF 10+3', 68: 'IVAI: SES-DF 15, PSU-GO 9, SES-GO 8',
 10: 'Vacinação: SES-GO 6, SES-DF 6, PSU-GO 5', 39: 'Exantemáticas: PSU-GO 5', 62: 'Maus-tratos: PSU-GO 5',
 152: 'Desconforto resp. neonatal: SES-DF 5', 163: 'Dermatoses infecciosas: SES-GO 8',
 278: 'Meningite: SES-DF 7 (Medway dá 0%)',
 30: 'Trauma: SES-DF 22, PSU-GO 6', 51: 'Trauma (idem)', 58: 'Trauma (idem)', 88: 'Trauma (idem)',
 8: 'Abdome agudo: SES-DF 34, SES-GO 12', 116: 'Abdome agudo (idem)', 131: 'Abdome agudo (idem)', 158: 'Abdome agudo (idem)',
 31: 'Hérnias: SES-DF 13', 32: 'Pâncreas e vias biliares: PSU-GO 6', 77: 'Pâncreas e vias biliares: PSU-GO 6',
 25: 'Coloproctologia: SES-GO 5, PSU-GO 4', 37: 'Urologia/litíase: PSU-GO 8, SES-GO 7 (nefrolitíase)',
 138: 'Uro-oncologia: SES-DF 6, PSU-GO 4', 119: 'Tempos operatórios: SES-GO 7',
 48: 'Câncer de mama: PSU-GO 8', 18: 'Infecção ginecológica: SES-DF 13, SES-GO 7, PSU-GO 6', 112: 'Infecção ginecológica (idem)',
 66: 'SUA: SES-DF 9, PSU-GO 5, SES-GO 3', 19: 'Amenorreia/SOP: SES-DF 10, PSU-GO 4, SES-GO 2', 60: 'Dor pélvica: SES-DF 10',
 69: 'Climatério: SES-GO 4, PSU-GO 3, SES-DF 2', 26: 'Lesões pré-invasivas: SES-DF 5, SES-GO 4',
 17: 'Síndromes hipertensivas na gestação: SES-GO 13, SES-DF 6', 34: 'Sangramento 2ª metade: PSU-GO 7',
 57: 'Sangramento 1ª metade: SES-DF 14, SES-GO 4, PSU-GO 3', 9: 'Pré-natal: PSU-GO 11, SES-GO 11',
 56: 'TPP: SES-GO 7', 104: 'RPMO: SES-DF 4, SES-GO 3', 59: 'Doença hemolítica perinatal: SES-GO 5, PSU-GO 3',
 50: 'Doenças endócrinas na gestação: SES-DF 9',
 43: 'IC: PSU-GO 6, SES-GO 4', 15: 'SCA: SES-DF 9, PSU-GO 3', 74: 'Arritmias: SES-DF 9, PSU-GO 2', 21: 'HAS: SES-DF 5',
 38: 'Obstrutivos (DPOC/asma): SES-DF 8', 79: 'Tuberculose: SES-GO 6, PSU-GO 5', 156: 'ITU: SES-GO 7',
 53: 'DRC: SES-GO 6', 75: 'Paratireoides: SES-DF 5', 46: 'Tireoide: SES-DF 5', 14: 'Diabetes: SES-DF 3; ENAMED 2025 foco em DM',
 117: 'HIV: SES-GO 3', 41: 'Infecções na gestação (HIV, hepatites)',
}

def main(csv_path, cards_path, out):
    F = {int(r['ranking_global']): r for r in csv.DictReader(open(csv_path, encoding='utf-8'))}
    peso = {k: float(r['peso_relativo_prova_dec']) * 100 for k, r in F.items()}
    cards = json.load(open(cards_path, encoding='utf-8'))
    tot = collections.Counter(); novos = collections.Counter()
    for c in cards:
        d = c['deck'].split('::', 1)[-1] if '::' in c['deck'] else c['deck']
        if c['suspended']: continue
        tot[d] += 1
        if c['state'] == 'new': novos[d] += 1
    usados = set(x for v in MAPA.values() for x in v)
    def pdeck(ids): return sum(peso[i] / COMPARTILHADO.get(i, 1) for i in ids)
    def prio(i): return peso[i] * (1.25 if i in BANCAS else 1)
    L = ['# Prioridades: Medway × bancas-alvo × baralho', '',
         'Gerado por `ferramentas/prioridades.py` a partir de `medway_base_claude_code.csv` (294 focos).', '',
         '**Como os números foram calculados:**',
         '- **Peso Medway:** fração da prova (`score_rf` / 59,22).',
         '- **Prioridade:** peso × 1,25 quando PSU-GO, SES-GO ou SES-DF confirmam o tema entre os mais cobrados (Medcof, edição anterior).',
         '- **Meta de cards:** 100 por 1% de peso, calibrada no piloto Diabetes (1,99% → 198 cards), com mínimo de 10. É ponto de partida: meu julgamento ajusta ±30%.', '']
    A = collections.defaultdict(float)
    for k, r in F.items(): A[r['grande_area']] += peso[k]
    L += ['## Peso por grande área (Medway)', '', '| Área | Peso |', '|---|---|']
    L += [f'| {a} | {v:.1f}% |' for a, v in sorted(A.items(), key=lambda x: -x[1])]
    # decks existentes
    L += ['', '## Decks existentes: tamanho × meta', '',
          '| Deck | Focos Medway (ranking) | Peso | Banca-alvo confirma | Cards ativos | Novos | Meta | Situação |', '|---|---|---|---|---|---|---|---|']
    rows = []
    for d, ids in MAPA.items():
        p = pdeck(ids); meta = max(10, round(p * 100)); n = tot.get(d, 0)
        conf = '; '.join(BANCAS[i] for i in ids if i in BANCAS) or '—'
        if d == 'CM::Endocrino::Diabetes': n = 203; sit = 'limpo (piloto v4)'
        elif n > meta * 1.3: sit = f'**acima da meta** (+{n - meta})'
        elif n < meta * 0.7: sit = f'abaixo da meta (−{meta - n}): procurar lacunas'
        else: sit = 'na faixa'
        rows.append((sum(prio(i) / COMPARTILHADO.get(i, 1) for i in ids), d, ids, p, conf, n, novos.get(d, 0), meta, sit))
    for pr, d, ids, p, conf, n, nv, meta, sit in sorted(rows, reverse=True):
        L.append(f'| {d} | {", ".join(str(i) for i in ids)} | {p:.2f}% | {conf} | {n} | {nv} | {meta} | {sit} |')
    # lacunas: focos sem deck
    L += ['', '## Focos SEM deck no baralho (lacunas), por prioridade', '',
          'Só focos com peso ≥ 0,30% ou confirmados pelas bancas-alvo.', '',
          '| # | Área | Tema → Foco | Prevalência | Peso | Banca-alvo | Meta de cards |', '|---|---|---|---|---|---|---|']
    gaps = [(prio(k), k) for k in F if k not in usados and (peso[k] >= 0.30 or k in BANCAS)]
    tot_meta = 0
    for pr, k in sorted(gaps, reverse=True):
        r = F[k]; meta = max(10, round(peso[k] * 100)); tot_meta += meta
        L.append(f"| {k} | {r['grande_area']} | {r['tema']} → **{r['foco_conteudo']}** | {r['prevalencia']} | {peso[k]:.2f}% | {BANCAS.get(k, '—')} | {meta} |")
    L += ['', f'**Total estimado para cobrir essas lacunas: ~{tot_meta} cards.**', '']
    cob = sum(pdeck(ids) for ids in MAPA.values())
    L += [f'**Cobertura atual do baralho: {cob:.1f}% do peso da prova** (soma dos focos que têm deck).', '']
    # divergências
    L += ['## Divergências Medway × bancas-alvo', '',
          '- **Infecções do SNC/meningite na pediatria:** a Medway dá 0% (foco 278), mas a SES-DF teve 7 questões. Para a SES-DF, eu trato como prioridade.',
          '- **Preventiva:** a Medway dá 15,5% da prova, enquanto PSU-GO e SES-GO têm 28–33% dos temas listados em Preventiva. Para as suas bancas, a Preventiva pesa mais do que a média nacional da Medway.',
          '- **Clínica Médica:** a Medway dá 24,2%, enquanto PSU-GO, SES-GO e SES-DF têm 12–14%. Nas suas bancas, a CM pesa menos.', '']
    open(out, 'w', encoding='utf-8').write('\n'.join(L) + '\n')
    print('ok', len(rows), 'decks;', len(gaps), 'lacunas; cobertura', round(cob, 1), '%; meta lacunas', tot_meta)

if __name__ == '__main__':
    main(*sys.argv[1:4])
