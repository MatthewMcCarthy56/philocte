import collections
import itertools
import random

arrow_directions = [
    (-1, -1), # up left
    (0, -1), # up
    (1, -1), # up right
    (1, 0), # right
    (1, 1), # down right
    (0, 1), # down
    (-1, 1), # down left
    (-1, 0) # left
]

class Wall:
    def __init__(self):
        self.type = 'wall'
    def __repr__(self):
        return 'Wall()'

wall = Wall()

class Card:
    def __init__(self, name, arrow_ids, max_hp, attack_strength, attack_type, physical_defense, magical_defense, owner):
        self.name = name
        self.arrow_ids = arrow_ids
        self.max_hp = max_hp
        self.attack_strength = attack_strength
        self.attack_type = attack_type
        self.physical_defense = physical_defense
        self.magical_defense = magical_defense
        self.owner = owner
    def with_full_health(self, controller):
        return CardState(self, controller, self.max_hp)
    def __str__(self):
        return f'{self.max_hp} {self.attack_strength}{self.attack_type}{self.physical_defense}{self.magical_defense}'

class CardState:
    def __init__(self, card, controller, hp):
        self.type = 'card'
        self.card = card
        self.controller = controller
        self.hp = hp
    def __str__(self):
        return f'{self.controller}:{self.hp}/{str(self.card)}'
    def __eq__(self, other):
        if other is None or other.type != 'card':
            return False
        return self.card == other.card and self.controller == other.controller and self.hp == other.hp

class GameState:
    def __init__(self, board, player_hands, current_player):
        self.board = board
        self.player_hands = player_hands
        self.current_player = current_player
    def turn(self, card: Card, position, attack_order):
        x, y = position
        new_board = [list(l) for l in self.board]
        new_hands = [set(l) for l in self.player_hands]
        new_hands[self.current_player].remove(card)
        card_state = card.with_full_health(self.current_player)
        new_board[x][y] = card_state
        def combo(battle_winner, defeated_position):
            defeated_x, defeated_y = defeated_position
            defeated_card = new_board[defeated_x][defeated_y]
            new_board[defeated_x][defeated_y] = defeated_card.card.with_full_health(battle_winner)
            for facing_pos in facing_positions(defeated_card.card, (defeated_x, defeated_y), self.board):
                facing_x, facing_y = facing_pos
                faced = new_board[facing_x][facing_y]
                if faced is not None and faced.type == 'card' and faced.controller != battle_winner:
                    new_board[facing_x][facing_y] = faced.card.with_full_health(battle_winner)
        died = False
        battled = set()
        for direction_id in attack_order:
            # Do all battles first
            x_offset, y_offset = arrow_directions[direction_id]
            target_x = x + x_offset
            target_y = y + y_offset
            battled.add((target_x, target_y))
            target = new_board[target_x][target_y]
            if target.controller == self.current_player:
                continue
            new_target_hp = target.hp - card.attack_strength
            card_state.hp -= target.card.magical_defense if card.attack_type == 'M' else target.card.physical_defense
            if new_target_hp <= 0 and card_state.hp <= 0:
                # Both dead - pop
                new_board[x][y] = None
                new_hands[target.controller].add(card)
                new_board[target_x][target_y] = None
                new_hands[self.current_player].add(target.card)
                break
            elif new_target_hp <= 0:
                # Defeated target - combo
                combo(self.current_player, (target_x, target_y))
            elif card_state.hp <= 0:
                # Attacking card was defeated - combo
                combo(target.controller, position)
                died = True
            else:
                # Both survived
                new_board[target_x][target_y] = CardState(target.card, target.controller, new_target_hp)
        if not died:
            # Still alive, can do non-battle damage
            for facing_pos in facing_positions(card_state.card, position, self.board):
                if facing_pos in battled:
                    continue
                facing_x, facing_y = facing_pos
                facing = new_board[facing_x][facing_y]
                if facing is not None and facing.type == 'card' and facing.controller != self.current_player:
                    new_target_hp = facing.hp - card_state.card.attack_strength
                    if new_target_hp <= 0:
                        new_board[facing_x][facing_y] = facing.card.with_full_health(self.current_player)
                    else:
                        new_board[facing_x][facing_y] = CardState(facing.card, facing.controller, new_target_hp)
        return GameState(new_board, new_hands, other_player(self.current_player))
    def score(self):
        points = collections.defaultdict(int)
        for column in self.board:
            for cell in column:
                if cell is not None and cell.type == 'card':
                    points[cell.controller] += 1
        return points
    def equivalent(self, other):
        return self.current_player == other.current_player and self.board == other.board
    def __str__(self):
        text_width = 14 * len(self.board)
        text_height = 3 * len(self.board[0])
        board_text = [[' ' for _ in range(text_height)] for _ in range(text_width)]
        for y in range(len(self.board[0])):
            for x in range(len(self.board)):
                cell = self.board[x][y]
                board_text[x * 14][y * 3] = '┌'
                board_text[x * 14][y * 3 + 1] = '│'
                board_text[x * 14][y * 3 + 2] = '└'
                board_text[(x + 1) * 14 - 1][y * 3] = '┐'
                board_text[(x + 1) * 14 - 1][y * 3 + 1] = '│'
                board_text[(x + 1) * 14 - 1][y * 3 + 2] = '┘'
                if cell is None:
                    continue
                elif cell.type == 'wall':
                    for col in range(3):
                        for row in range(x * 14 + 1, (x + 1) * 14 - 1):
                            board_text[row][y * 3 + col] = '#'
                else:
                    for col, char in zip(range(x * 14 + 2, x * 14 + 13), str(cell)):
                        board_text[col][y * 3 + 1] = char
                    card = cell.card
                    if 0 in card.arrow_ids:
                        board_text[x * 14 + 2][y * 3] = '↖'
                    if 1 in card.arrow_ids:
                        board_text[x * 14 + 7][y * 3] = '↑'
                    if 2 in card.arrow_ids:
                        board_text[x * 14 + 11][y * 3] = '↗'
                    if 3 in card.arrow_ids:
                        board_text[x * 14 + 12][y * 3 + 1] = '→'
                    if 4 in card.arrow_ids:
                        board_text[x * 14 + 11][y * 3 + 2] = '↘'
                    if 5 in card.arrow_ids:
                        board_text[x * 14 + 7][y * 3 + 2] = '↓'
                    if 6 in card.arrow_ids:
                        board_text[x * 14 + 2][y * 3 + 2] = '↙'
                    if 7 in card.arrow_ids:
                        board_text[x * 14 + 1][y * 3 + 1] = '←'
        stringified = ''
        for col in range(text_height):
            for row in range(text_width):
                stringified += board_text[row][col]
            stringified += '\n'
        for player, hand in enumerate(self.player_hands):
            stringified += f'\nPlayer {player} hand: {[str(c) for c in hand]}'
        stringified += f'\nTurn: player {self.current_player}'
        return stringified

class Game:
    def __init__(self, player_hands, initial_state):
        self.history = [initial_state]
        self.player_hands = player_hands
    def current_state(self):
        return self.history[-1]
    def turn(self, card, position, attack_order):
        new_state = self.current_state().turn(card, position, attack_order)
        self.history.append(new_state)
    def check_win(self):
        state = self.current_state()
        game_over = False
        if len(state.player_hands[0]) == 0 and len(state.player_hands[1]) == 0:
            game_over = True
        else:
            repetitions = 0
            for old_state in self.history:
                if state.equivalent(old_state):
                    repetitions += 1
            game_over = repetitions >= 3
        if game_over:
            points = state.score()
            if points[1] > points[0]:
                return 1
            else:
                return 0
        return None

def other_player(player):
    return 1 - player

def facing_position_directions(card, position, board):
    x, y = position
    width = len(board)
    height = len(board[0])
    facing = []
    for arrow_id in card.arrow_ids:
        x_offset, y_offset = arrow_directions[arrow_id]
        facing_x = x + x_offset
        facing_y = y + y_offset
        if facing_x >= 0 and facing_x < width and facing_y >= 0 and facing_y < height:
            facing.append((arrow_id, facing_x, facing_y))
    return facing

def facing_positions(card, position, board):
    return [(x, y) for (_, x, y) in facing_position_directions(card, position, board)]

def battle_directions(card, position, board, player):
    x, y = position
    battles = []
    for arrow_id, facing_x, facing_y in facing_position_directions(card, position, board):
        facing = board[facing_x][facing_y]
        if facing is None or facing.type != 'card' or facing.controller == player:
            continue
        if position in facing_positions(facing.card, (facing_x, facing_y), board):
            battles.append(arrow_id)
    return battles

def generate_walls(board_size, num_walls):
    width, height = board_size
    board = [[None for _ in range(height)] for _ in range(width)]
    for x, y in random.sample(list(itertools.product(range(width), range(height))), k=num_walls):
        board[x][y] = wall
    return board

def new_game(board, player_hands):
    state = GameState(board, player_hands, 0)
    return Game(player_hands, state)