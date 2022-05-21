import game
import random

vepel = game.Card('Vepel', [0, 1, 2, 3, 5, 6, 7], 1, 4, 'M', 3, 2, 0)
dark_matter = game.Card('Dark Matter', [0, 4, 5, 6, 7], 3, 8, 'M', 2, 5, 0)
mog = game.Card('Mog', [], 1, 9, 'P', 1, 2, 0)
gorgant = game.Card('Gorgant', list(range(8)), 6, 2, 'P', 4, 4, 0)
player0_hand = [vepel, dark_matter]
player1_hand = [mog, gorgant]

random.seed(1)
board = game.generate_walls((5, 5), 7)
g = game.new_game(board, [player0_hand, player1_hand])
print(g.current_state())

g.turn(vepel, (1, 1), [])
print(g.current_state())

g.turn(gorgant, (2, 1), [7])
print(g.current_state())

print(game.battle_directions(dark_matter, (0, 0), g.current_state().board, 0))
g.turn(dark_matter, (0, 0), [4])
print(g.current_state())

g.turn(mog, (4, 0), [])
print(g.current_state())
print(g.check_win())