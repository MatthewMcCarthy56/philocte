import collections
import game
import generation
import random

def pick_space(board):
    empty_spaces = []
    for x in range(len(board)):
        for y in range(len(board[0])):
            if board[x][y] is None:
                empty_spaces.append((x, y))
    return random.choice(empty_spaces)

def random_move(g: game.Game):
    state = g.current_state()
    space = pick_space(state.board)
    card, = random.sample(state.player_hands[state.current_player], k=1)
    battles = game.battle_directions(card, space, state.board, state.current_player)
    random.shuffle(battles)
    g.turn(card, space, battles)

def simulate_game(generators):
    board = game.generate_walls((5, 5), 7)
    initial_hands = [generation.make_cards(gen, 8, player) for player, gen in zip(range(2), generators)]
    g = game.new_game(board, initial_hands)
    while g.check_win() is None:
        random_move(g)
    return g

if __name__ == "__main__":
    # g = simulate_game()
    # for step in g.history:
    #     print(step)
    # print('Winner:', g.check_win())
    wins = collections.defaultdict(int)
    simulations = 5000
    for _ in range(simulations):
        g = simulate_game([generation.make_card, generation.make_card])
        wins[g.check_win()] += 1
    print('Player 0', wins[0], f'({wins[0] / simulations * 100:.1f}%, {wins[0] / (wins[0] + wins[1]) * 100:.1f}% of non-draws)', sep='\t')
    print('Player 1', wins[1], f'({wins[1] / simulations * 100:.1f}%, {wins[1] / (wins[0] + wins[1]) * 100:.1f}% of non-draws)', sep='\t')
    print('Tie     ', wins[2], sep='\t')