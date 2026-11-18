# Exemplo de arquivo de decisões para ferramentas/build_csv_deck.py.
# Copie para ferramentas/decks/<tema>.py (pasta fora do git) e preencha uma decisão por linha do CSV.
#
# Cabeçalho recomendado: peso do tema na planilha de prioridades, o que a pesquisa achou e a meta de cards.
# Meta: ~100 cards por 1% de peso, mínimo 10, ajuste de ±30% por julgamento e dados de prova.
DECK = 'Baralho::Area::Tema'
TAGS = ['area::tema']

def E(f, v, mot='encurtado'): return ('E', f, v, mot)   # editar (mot com "corrigido" ganha tag limpa::corrigido)
def K(f, v): return ('E', f, v, 'mantido')               # manter, só limpando o HTML

# índice = número da linha do CSV (começa em 1)
D = {
    1: K('Pergunta direta?', 'Resposta curta'),
    2: E('Quais os itens? (3)', '-Item A\n-Item B\n-Item C', 'encurtado + complemento'),
    3: E('Pergunta com erro no original?', 'Resposta certa', 'corrigido (o que estava errado)'),
    4: ('X', 'duplicado'),        # motivos: duplicado, fundido, facil-demais, fisiologia-basica, baixo-rendimento
}

# Cards novos (lacunas): (frente, verso, tags extras)
NOVOS = [
    ('Pergunta de lacuna?', 'Resposta', ['incidencia::enare']),
]
