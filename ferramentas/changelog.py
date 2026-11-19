"""Gera a planilha de revisão (.csv) e o changelog (.md) de um deck a partir de pilot_rows.json.
Uso: python changelog.py <pilot_rows.json> <saida.csv> <saida.md> <nome do deck>"""
import json, re, csv, sys, collections, html

def c(t, n=None):
    t = t or ''
    if t.startswith('HTML:'):   # tabela/fluxograma: mostra só o texto das células/caixas
        tipo = '[tabela] ' if '<table' in t else '[fluxograma] '
        t = tipo + re.sub(r'\s*(·\s*)+', ' · ', re.sub(r'<br\s*/?>|</t[dh]>|</div>', ' · ', t[5:])).replace('↓', '→')
        t = html.unescape(re.sub(r'<[^>]+>', '', t)).strip(' ·')
    t = t.replace('^^', '')
    t = re.sub(r'\[IMG:[^\]]*\]', '🖼', t); t = re.sub(r'^\w+\.\s*(?=[A-ZÀ-Ú_])', '', t.strip(), count=1) if t.startswith(('Diabetes.', 'Tireoide.')) else t.strip()
    t = t.replace('|', '/').replace('\n', ' · ')
    return t if not n or len(t) <= n else t[:n] + '…'

def main(rows_path, out_csv, out_md, deck):
    rows = json.load(open(rows_path, encoding='utf-8'))
    with open(out_csv, 'w', encoding='utf-8-sig', newline='') as f:
        w = csv.writer(f, delimiter=';'); w.writerow(['nº', 'ação', 'motivo', 'frente nova', 'verso novo', 'frente original', 'verso original'])
        for r in rows:
            ex = r['acao'] == 'EXCLUIR'
            w.writerow([r['n'], r['acao'], r['motivo'], '' if ex else r['frente'], '' if ex else r['verso'], r['original_frente'], r['original_verso'][:600]])
    by = collections.defaultdict(list)
    for r in rows: by[r['acao']].append(r)
    orig = sum(isinstance(r['n'], int) for r in rows)          # cards divididos geram linhas "12.2", "12.3"...
    kept = len(rows) - len(by['NOVO']) - len(by['EXCLUIR'])     # cards ativos vindos da Medway (já contando as divisões)
    div = sum(isinstance(r['n'], str) and r['n'] != 'novo' for r in rows)
    L = [f'# Alterações no deck {deck}', '', f'**{orig} cards originais → {kept} mantidos + {len(by["NOVO"])} novos = {kept + len(by["NOVO"])} ativos.**'
         + (f' ({div} vêm da divisão de cards longos em cards curtos.)' if div else ''), '',
         '| Ação | Cards |', '|---|---|']
    for k, lab in [('EXCLUIR', 'Excluídos'), ('EDITAR', 'Reescritos, fundidos ou corrigidos'), ('LIMPAR', 'Limpeza automática'), ('MANTER-REVISAR', 'Mantidos por dado (eu excluiria)'), ('NOVO', 'Novos (lacunas)')]:
        L.append(f'| {lab} | {len(by[k])} |')
    L += ['', 'O texto original da Medway de cada card editado fica no campo **Comentário**.', '']
    L += ['## 1. Cards novos (lacunas)', '', '| Frente | Verso | Dado |', '|---|---|---|']
    L += [f"| {c(r['frente'])} | {c(r['verso'])} | {r['motivo'].replace('lacuna ', '') or 'julgamento clínico'} |" for r in by['NOVO']]
    L += ['', '## 2. Mantidos por dado de prova', '', 'Eu excluiria estes cards por serem fáceis ou básicos, mas o dado indica que o tema é cobrado.', '', '| Nº | Dado | Frente | Verso |', '|---|---|---|---|']
    L += [f"| {r['n']} | {r['motivo'].replace('mantido-por-dado ', '')} | {c(r['frente'])} | {c(r['verso'])} |" for r in by['MANTER-REVISAR']]
    L += ['', '## 3. Reescritos, fundidos ou corrigidos', '', '| Nº | Motivo | Antes (frente → verso) | Depois (frente → verso) |', '|---|---|---|---|']
    L += [f"| {r['n']} | {r['motivo']} | {c(r['original_frente'], 120)} → {c(r['original_verso'], 160)} | **{c(r['frente'])}** → {c(r['verso'])} |" for r in by['EDITAR']]
    L += ['', '## 4. Limpeza automática', '', 'O prefixo do tema saiu da frente, o verso ficou só com a resposta e a explicação foi para o Comentário.', '', '| Nº | Frente | Verso antes | Verso depois |', '|---|---|---|---|']
    L += [f"| {r['n']} | {c(r['frente'], 120)} | {c(r['original_verso'], 140)} | {c(r['verso'])} |" for r in by['LIMPAR']]
    L += ['', '## 5. Excluídos', '', '| Nº | Motivo | Frente | Verso original |', '|---|---|---|---|']
    L += [f"| {r['n']} | {r['motivo']} | {c(r['original_frente'], 140)} | {c(r['original_verso'], 120)} |" for r in sorted(by['EXCLUIR'], key=lambda r: (r['motivo'], r['n']))]
    open(out_md, 'w', encoding='utf-8').write('\n'.join(L) + '\n')
    print('ok', {k: len(v) for k, v in by.items()}, 'ativos', kept + len(by['NOVO']))

if __name__ == '__main__':
    main(*sys.argv[1:5])
