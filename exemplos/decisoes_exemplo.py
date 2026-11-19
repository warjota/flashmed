# Exemplo de arquivo de decisões para ferramentas/build_csv_deck.py.
# Copie para ferramentas/decks/<tema>.py (pasta fora do git) e preencha uma decisão por linha do CSV.
#
# Cabeçalho recomendado: peso do tema na planilha de prioridades, o que a pesquisa achou e a meta de cards.
# Meta: ~100 cards por 1% de peso, mínimo 10, ajuste de ±30% por julgamento e dados de prova.
DECK = 'Baralho::Area::Tema'
TAGS = ['area::tema']

def E(f, v, mot='encurtado'): return ('E', f, v, mot)   # editar (mot com "corrigido" ganha tag limpa::corrigido)
def K(f, v): return ('E', f, v, 'mantido')               # manter, só limpando o HTML

# Tabela e fluxograma (estilo aprovado: bordas #888, cabeçalho cinza translúcido; funciona no modo noturno)
TB = 'border: 1px solid #888; padding: 4px 8px;'
TH = TB + ' background: rgba(128,128,128,0.2);'
def TAB(cab, linhas):
    h = '<table style="border-collapse: collapse; margin: 0 auto; font-size: 14px;">'
    h += '<tr>' + ''.join(f'<th style="{TH}">{c}</th>' for c in cab) + '</tr>'
    for l in linhas:
        h += '<tr>' + ''.join(f'<td style="{TB}">{c}</td>' for c in l) + '</tr>'
    return 'HTML:' + h + '</table>'

BOX = 'border: 1px solid #888; border-radius: 6px; padding: 6px 10px;'
def FLUXO(passos, ramos):
    """Passos em sequência (o 1º destacado) e, no fim, ramos lado a lado (decisão). Só para protocolos."""
    h = '<div style="display: flex; flex-direction: column; align-items: center; gap: 2px; font-size: 15px;">'
    for i, p in enumerate(passos):
        h += f'<div style="{BOX}{" background: rgba(128,128,128,0.2);" if i == 0 else ""}">{p}</div><div>↓</div>'
    h += '<div style="display: flex; gap: 10px; justify-content: center;">' + ''.join(f'<div style="{BOX}">{r}</div>' for r in ramos)
    return 'HTML:' + h + '</div></div>'

# Marcações no texto: **negrito**, ^^complemento em fonte menor^^, [IMG:url]
# índice = número da linha do CSV (começa em 1)
D = {
    1: K('Pergunta direta?', 'Resposta curta'),
    2: E('Quais os itens? (3)', '-Item A\n-Item B\n-Item C', 'encurtado + complemento'),
    3: E('Pergunta com erro no original?', 'Resposta certa', 'corrigido (o que estava errado)'),
    5: [E('Card longo dividido: parte 1?', 'Resposta 1', 'dividido em cards curtos'), E('Parte 2?', 'Resposta 2', 'dividido em cards curtos')],
    4: ('X', 'duplicado'),        # motivos: duplicado, fundido, facil-demais, fisiologia-basica, baixo-rendimento
}

# Cards novos (lacunas): (frente, verso, tags extras)
NOVOS = [
    ('Pergunta de lacuna?', 'Resposta', ['incidencia::enare']),
]
