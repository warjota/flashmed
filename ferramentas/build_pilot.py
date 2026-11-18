import sys, json, re, html, shutil, os
sys.path.insert(0, os.path.dirname(__file__))
from autoclean import clean
import dm_decisions as D
from anki.collection import Collection, ExportAnkiPackageOptions, DeckIdLimit
S, OUT = sys.argv[1], sys.argv[2]
shutil.copy(os.path.join(S,'col.db'), os.path.join(S,'pilot.anki2'))
if os.path.exists(os.path.join(S,'pilot.anki2.wal')): os.remove(os.path.join(S,'pilot.anki2.wal'))
col = Collection(os.path.join(S,'pilot.anki2'))
R = {r['cid']: r for r in json.load(open(os.path.join(S,'cards.json'), encoding='utf-8'))}
ids = json.load(open(os.path.join(S,'dm_ids.json')))
def to_html(t):
    t = html.escape(t, quote=False)
    t = re.sub(r'\[IMG:([^\]]+)\]', lambda m: f'<img src="{html.unescape(m.group(1))}">', t)
    return t.replace('\n', '<br>')
rows = []; susp = []
for i, cid in enumerate(ids):
    card = col.get_card(cid); note = card.note()
    v = list(R[cid]['fields'].values()); orig_f, orig_b = note['Frente'], note['Verso']
    if i in D.X:
        note.add_tag(f'limpa::excluir::{D.X[i]}'); susp.append(cid); act = 'EXCLUIR'; nf, nb, mot = v[0], v[1], D.X[i]
    else:
        if i in D.E:
            nf, nb, mot = D.E[i]; act = 'EDITAR'
            note.add_tag('limpa::editado')
            if 'corrigido' in mot: note.add_tag('limpa::corrigido')
            if 'verificar' in mot: note.add_tag('limpa::verificar')
            # mantém imagem da frente original
            if '[IMG' in v[0] and '[IMG' not in nf: nf += '\n' + '\n'.join(re.findall(r'\[IMG:[^\]]+\]', v[0]))
        else:
            nf, nb, _, _ = clean(v[0], v[1], 'Diabetes'); mot = 'limpeza-automatica'; act = 'LIMPAR'
            note.add_tag('limpa::limpo')
            if i in D.RESTAURADOS:
                note.add_tag(D.RESTAURADOS[i]); mot = 'mantido-por-dado ' + D.RESTAURADOS[i]; act = 'MANTER-REVISAR'
        note['Frente'] = to_html(nf); note['Verso'] = to_html(nb)
        note['Comentário'] = '<b>Original Medway</b><br>' + orig_f + '<hr>' + orig_b
    col.update_note(note)
    rows.append(dict(n=i, acao=act, motivo=mot, frente=nf, verso=nb, original_frente=v[0], original_verso=v[1]))
col.sched.suspend_cards(susp)
# --- cards novos (lacunas) ---
import dm_lacunas
did_dm = col.decks.id_for_name('02026::CM::Endocrino::Diabetes')
nt = col.models.by_name('Básico')
for f, v, tags in dm_lacunas.L:
    n = col.new_note(nt); n['Frente'] = to_html(f); n['Verso'] = to_html(v)
    for t in ['fonte::claude', 'lacuna'] + tags: n.add_tag(t)
    col.add_note(n, did_dm)
    rows.append(dict(n='novo', acao='NOVO', motivo='lacuna ' + ' '.join(tags), frente=f, verso=v, original_frente='', original_verso=''))
did = col.decks.id_for_name('02026::CM::Endocrino::Diabetes')
col.export_anki_package(out_path=OUT, options=ExportAnkiPackageOptions(with_scheduling=True, with_media=True, with_deck_configs=False, legacy=False), limit=DeckIdLimit(did))
json.dump(rows, open(os.path.join(S,'pilot_rows.json'),'w',encoding='utf-8'), ensure_ascii=False, indent=1)
col.close()
print('ok', len(rows), 'suspensos', len(susp))
