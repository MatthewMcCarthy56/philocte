import game
import random

def make_cards(generator, count, owner):
    return [generator(str(i), owner) for i in range(count)]

def make_card(name, owner):
    num_arrows = random.choice(range(9))
    arrows = random.sample(range(8), k=num_arrows)
    attack_strength = random.choice(range(9))
    hp = max(1, 8 - attack_strength)
    attack_type = random.choice(['M', 'P'])
    if attack_type == 'M':
        magical_defense = random.choice([0, 1, 1, 2, 2, 3, 3, 3, 4, 4, 4])
        physical_defense = random.choice([0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 3, 4])
    else:
        physical_defense = random.choice([0, 1, 1, 2, 2, 3, 3, 3, 4, 4, 4])
        magical_defense = random.choice([0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 3, 4])
    return game.Card(name, arrows, hp, attack_strength, attack_type, physical_defense, magical_defense, owner)
    
def make_strong_card(name, owner):
    num_arrows = random.choice(range(9))
    arrows = random.sample(range(8), k=num_arrows)
    attack_strength = random.choice([3, 3, 4, 4, 5, 5, 6, 6, 6, 6, 7, 7, 7, 8, 8])
    hp = max(1, 8 - attack_strength)
    attack_type = random.choice(['M', 'P'])
    if attack_type == 'M':
        magical_defense = random.choice([2, 3, 3, 3, 4, 4, 4])
        physical_defense = random.choice([1, 1, 1, 2, 2, 2, 3, 4])
    else:
        physical_defense = random.choice([2, 3, 3, 3, 4, 4, 4])
        magical_defense = random.choice([1, 1, 1, 2, 2, 2, 3, 4])
    return game.Card(name, arrows, hp, attack_strength, attack_type, physical_defense, magical_defense, owner)