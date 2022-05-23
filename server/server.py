import asyncio
import game
import generation
import json
import websockets

decks = [generation.make_cards(generation.make_card, 30, player) for player in range(2)]
walls = game.generate_walls((5, 5), 7)

player_websockets = []
player_chosen_hands = [None, None]
g: game.Game = None

async def send_json(websocket, message):
    json_text = json.dumps(message)
    await websocket.send(json_text)

async def broadcast_json(message):
    json_text = json.dumps(message)
    for ws in player_websockets:
        await ws.send(json_text)

async def recv_json(websocket):
    json_text = await websocket.recv()
    return json.loads(json_text)

async def websocket_server(websocket, path):
    global g
    print('Websocket connected')
    player_id = len(player_websockets)
    if player_id >= 2:
        print('Too many players')
        return
    player_websockets.append(websocket)
    join_message = {
        'player_id': player_id,
        'walls': walls,
        'deck': decks[player_id]
    }
    await send_json(websocket, join_message)
    card_ids = set(await recv_json(websocket))
    player_chosen_hands[player_id] = [c for c in decks[player_id] if c.id in card_ids]
    if player_chosen_hands[0] is not None and player_chosen_hands[1] is not None:
        g = game.new_game(walls, player_chosen_hands)
        await broadcast_json(g.current_state())
    while True:
        play_message = await recv_json(websocket)
        if player_id != g.current_state().current_player:
            print(f'Player {player_id} played out of turn')
            continue
        card, = [c for c in g.current_state().player_hands[player_id] if c.id == play_message['card']]
        position = tuple(play_message['position'])
        battle_order = play_message['battle_order']
        g.turn(card, position, battle_order)
        print(g.current_state())
        await broadcast_json(g.current_state())
        winner = g.check_win()
        if winner is not None:
            await broadcast_json({'winner': winner})
            print(f'Game over, winner: {winner}')
            exit(0)

start_server = websockets.serve(websocket_server, "localhost", 5000)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()