"""Monta um deck novo a partir de um CSV exportado (frente;verso) + arquivo de decisões.
Uso: python build_csv_deck.py <decisoes.py> <entrada.csv> <col.db do usuário> <saida.apkg> <rows.json>
Os cards excluídos NÃO entram no .apkg (ainda não estão no Anki); ficam listados no changelog."""
import sys, os, csv, re, html, json, shutil, importlib.util, tempfile
from anki.collection import Collection, ExportAnkiPackageOptions, DeckIdLimit

def clean(s):
    s = re.sub(r'<br\s*/?>|</div>|</p>|</li>', '\n', s, flags=re.I)
    s = re.sub(r'<img[^>]*src="([^"]+)"[^>]*>', r'[IMG:\1]', s, flags=re.I)
    s = re.sub(r'<[^>]+>', '', s); s = html.unescape(s).replace('\xa0', ' ')
    return re.sub(r'\n\s*\n+', '\n', re.sub(r'[ \t]+', ' ', s)).strip()

def to_html(t):
    """Texto simples → HTML do Anki.
    'HTML:' no início = HTML cru (tabela, fluxograma), sem escape.
    **x** = negrito; ^^x^^ = complemento em fonte menor; [IMG:url] = imagem centralizada."""
    if t.startswith('HTML:'):
        return t[5:].strip()
    t = html.escape(t, quote=False)
    t = re.sub(r'\[IMG:([^\]]+)\]', lambda m: f'<div style="text-align: center;"><img src="{html.unescape(m.group(1))}"></div>', t)
    t = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', t)
    t = re.sub(r'\^\^(.+?)\^\^', r'<span style="font-size: 80%">\1</span>', t, flags=re.S)
    return t.replace('\n', '<br>')

def main(dec_path, csv_path, coldb, out, rows_out):
    spec = importlib.util.spec_from_file_location('dec', dec_path); M = importlib.util.module_from_spec(spec); spec.loader.exec_module(M)
    raw = [r for r in csv.reader(open(csv_path, encoding='utf-8-sig'), delimiter=';') if r and any(x.strip() for x in r)]
    tmp = tempfile.mkdtemp(); path = os.path.join(tmp, 'c.anki2'); shutil.copy(coldb, path)
    col = Collection(path)
    did = col.decks.id(M.DECK); nt = col.models.by_name('Básico')
    rows = []
    for i, r in enumerate(raw, 1):
        f0, v0 = clean(r[0]), clean(r[1] if len(r) > 1 else '')
        d = M.D.get(i)
        if d is None: raise SystemExit(f'card {i} sem decisão')
        if d[0] == 'X':
            rows.append(dict(n=i, acao='EXCLUIR', motivo=d[1], frente='', verso='', original_frente=f0, original_verso=v0)); continue
        _, f, v, mot = d
        n = col.new_note(nt); n['Frente'] = to_html(f); n['Verso'] = to_html(v)
        n['Comentário'] = '<b>Original Medway</b><br>' + r[0] + '<hr>' + (r[1] if len(r) > 1 else '')
        for t in M.TAGS + ['fonte::medway', 'limpa::editado'] + (['limpa::corrigido'] if 'corrigido' in mot else []): n.add_tag(t)
        col.add_note(n, did)
        rows.append(dict(n=i, acao='EDITAR', motivo=mot, frente=f, verso=v, original_frente=f0, original_verso=v0))
    for f, v, tags in M.NOVOS:
        n = col.new_note(nt); n['Frente'] = to_html(f); n['Verso'] = to_html(v)
        for t in M.TAGS + ['fonte::claude', 'lacuna'] + tags: n.add_tag(t)
        col.add_note(n, did)
        rows.append(dict(n='novo', acao='NOVO', motivo='lacuna ' + ' '.join(tags), frente=f, verso=v, original_frente='', original_verso=''))
    col.export_anki_package(out_path=out, options=ExportAnkiPackageOptions(with_scheduling=False, with_media=True, with_deck_configs=False, legacy=False), limit=DeckIdLimit(did))
    col.close(); shutil.rmtree(tmp, ignore_errors=True)
    json.dump(rows, open(rows_out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('ok: importados', sum(r['acao'] != 'EXCLUIR' for r in rows), '| excluídos', sum(r['acao'] == 'EXCLUIR' for r in rows))

if __name__ == '__main__':
    main(*sys.argv[1:6])
