import math

def calculate_winner(heaps, current_player):
    stack = [(heaps, current_player)]  # Stack to keep track of game states

    while stack:
        current_heaps, current_player = stack.pop()

        if all(heap == 0 for heap in current_heaps):
            return 1 - current_player  # Switch player since the current player made the last move and lost

        found_winning_move = False  # Flag to track if a winning move is found

        for i in range(len(current_heaps)):
            if current_heaps[i] > 0:
                for stones_to_take in range(1, math.isqrt(current_heaps[i]) + 1):
                    new_heaps = current_heaps.copy()
                    new_heaps[i] -= stones_to_take

                    if calculate_winner(new_heaps, 1 - current_player) == current_player:
                        found_winning_move = True
                        break  # Break out of the loop once a winning move is found

                if found_winning_move:
                    break  # Break out of the loop once a winning move is found

            if found_winning_move:
                break  # Break out of the loop once a winning move is found

        if not found_winning_move:
            return 1 - current_player  # If no winning move is found, the other player wins

    return 1 - current_player  # If the stack is empty, the other player wins

# Open the input file and read its contents
with open('input.txt', 'r') as file:
    content = file.read().strip().split('\n')

# Get the number of games
G = int(content[0])

winners = 0  # Bit representation of the winners

# Iterate over each game
for i in range(G):
    # Read the number of heaps and their sizes
    game_info = content[i+1].split()
    N = int(game_info[0])
    heaps = list(map(int, game_info[1:]))

    winner = calculate_winner(heaps, 0)  # Start with player 0
    winners |= (1 << winner)  # Update the bit representation of winners

# Output the result as a flag
print(f"flag{{{winners:0{G}b}}}")
