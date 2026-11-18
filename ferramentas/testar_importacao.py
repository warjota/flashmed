"""Importa um .apkg numa CÓPIA da coleção e mostra o que mudaria (a coleção original não é tocada).
Uso: python testar_importacao.py <col.db/collection.anki2> <pacote.apkg> [deck]"""
import os, sys, shutil, tempfile
from anki.collection import Collection
from anki.import_export_pb2 import ImportAnkiPackageRequest, ImportAnkiPackageOptions


def main(coldb, apkg, deck=None):
    tmp = tempfile.mkdtemp()
    path = os.path.join(tmp, 'teste.anki2')
    shutil.copy(coldb, path)
    col = Collection(path)
    antes = col.note_count()
    r = col.import_anki_package(ImportAnkiPackageRequest(
        package_path=apkg, options=ImportAnkiPackageOptions(with_scheduling=False)))
    print(f'notas: {antes} -> {col.note_count()}')
    print(f'novas: {len(r.log.new)} | atualizadas: {len(r.log.updated)} | iguais/duplicadas: {len(r.log.duplicate)}')
    if deck:
        q = f'"deck:{deck}"'
        print(f'cards no deck: {len(col.find_cards(q))} | corrigidos: {len(col.find_notes(q + " tag:limpa::corrigido"))}')
    col.close()
    shutil.rmtree(tmp, ignore_errors=True)


if __name__ == '__main__':
    main(*sys.argv[1:4])
