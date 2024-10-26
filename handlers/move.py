import random


# See https://docs.battlesnake.com/api/example-move for available data
def handle_move(game_state: dict) -> dict:
    is_move_safe = {"up": True, "down": True, "left": True, "right": True}

    # prevent from moving backwards
    my_head = game_state["you"]["body"][0]  # Coords of your head
    my_neck = game_state["you"]["body"][1]  # Coords of your "neck"

    if my_neck["x"] < my_head["x"]:  # Neck is left of head, don't move left
        is_move_safe["left"] = False

    elif my_neck["x"] > my_head["x"]:  # Neck is right of head, don't move right
        is_move_safe["right"] = False

    elif my_neck["y"] < my_head["y"]:  # Neck is below head, don't move down
        is_move_safe["down"] = False

    elif my_neck["y"] > my_head["y"]:  # Neck is above head, don't move up
        is_move_safe["up"] = False

    # TODO: Step 1 - Prevent your Battlesnake from moving out of bounds
    board_width = game_state['board']['width']
    board_height = game_state['board']['height']
    if my_head["x"] == 0:
        is_move_safe["left"] = False
    if my_head["x"] == board_width - 1:
        is_move_safe["right"] = False
    if my_head["y"] == 0:
        is_move_safe["down"] = False
    if my_head["y"] == board_height - 1:
        is_move_safe["up"] = False
    # TODO: Step 2 - Prevent your snake from colliding with itself
    my_body = game_state['you']['body']
    for coords in my_body:
        if my_head["x"] + 1 == coords["x"] and my_head["y"] == coords["y"]:
            is_move_safe["right"] = False
        if my_head["x"] - 1 == coords["x"] and my_head["y"] == coords["y"]:
            is_move_safe["left"] = False
        if my_head["x"] == coords["x"] and my_head["y"] + 1 == coords["y"]:
            is_move_safe["up"] = False
        if my_head["x"] == coords["x"] and my_head["y"] - 1 == coords["y"]:
            is_move_safe["down"] = False
    # TODO: Step 3 - Prevent your snake from colliding with other snakes
    opponents = game_state['board']['snakes']
    for i in range(len(opponents)):
        opponents_coords = opponents[i]['body']
        for j in range(len(opponents_coords)):
            if my_head["x"] + 1 == opponents_coords[j]["x"] and my_head["y"] == opponents_coords[j]["y"]:
                is_move_safe["right"] = False
            if my_head["x"] - 1 == opponents_coords[j]["x"] and my_head["y"] == opponents_coords[j]["y"]:
                is_move_safe["left"] = False
            if my_head["x"] == opponents_coords[j]["x"] and my_head["y"] + 1 == opponents_coords[j]["y"]:
                is_move_safe["up"] = False
            if my_head["x"] == opponents_coords[j]["x"] and my_head["y"] - 1 == opponents_coords[j]["y"]:
                is_move_safe["down"] = False
    # Are there any safe moves left?
    safe_moves = []
    for move, is_safe in is_move_safe.items():
        if is_safe:
            safe_moves.append(move)

    # Move down if there is no better solution...
    if len(safe_moves) == 0:
        return {"move": "down"}

    # Choose a random move from the safe ones
    next_move = random.choice(safe_moves)

    # TODO: Step 4 - Move towards food instead of random, to regain health
    # food = game_state['board']['food']

    print(f"MOVE {game_state.get('turn', '')}: {next_move}")
    return {"move": next_move}
