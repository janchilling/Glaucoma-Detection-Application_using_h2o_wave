from h2o_wave import Q

def add_card(q: Q, name, card) -> None:
    q.client.cards.add(name)
    q.page[name] = card

def clear_cards(q: Q, ignore=[]) -> None:
    for name in q.client.cards.copy():
        if name not in ignore:
            del q.page[name]
            q.client.cards.remove(name)
