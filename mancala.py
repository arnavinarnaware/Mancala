import random

class MancalaGame:
    def __init__(self, pits_per_player=6, initial_stones=4):
        self.pits_per_player = pits_per_player
        self.board = [initial_stones] * (2 * pits_per_player + 2)
        self.current_player = 1
        self.countdown_pit = random.randint(1, pits_per_player)  #randomly choose a countdown pit
        self.countdown_counter = 3  #initial countdown value

    def display_board(self):
        print("Player 2 (bottom)")
        print("  ", " ".join(map(str, self.board[self.pits_per_player + 2 : 2 * self.pits_per_player + 2][::-1])))
        print(self.board[0], " " * (3 * self.pits_per_player - 1), self.board[self.pits_per_player + 1])
        print("  ", " ".join(map(str, self.board[1:self.pits_per_player + 1])))
        print("Player 1 (top)")

    def make_move(self, pit_index):
        stones_to_move = self.board[pit_index]
        self.board[pit_index] = 0

        while stones_to_move > 0:
            pit_index = (pit_index + 1) % len(self.board)
            if (self.current_player == 1 and pit_index == self.pits_per_player + 1) or (
                self.current_player == 2 and pit_index == 0
            ):
                continue  #skip opponent store
            self.board[pit_index] += 1
            stones_to_move -= 1

        self.handle_special_pits(pit_index)

        #check if another turn
        if self.current_player == 1 and pit_index == 0:
            return True  #Player 1 gets another turn
        elif self.current_player == 2 and pit_index == self.pits_per_player + 1:
            return True  #Player 2 gets another turn

        return False  #doesn't get extra turn

    def handle_special_pits(self, last_pit_index):
        #Countdown pit
        if last_pit_index == self.countdown_pit and self.countdown_counter > 0:
            print(f"Countdown pit activated! Countdown: {self.countdown_counter}")
            self.countdown_counter -= 1
            if self.countdown_counter == 0:
                print("Boom! Countdown pit exploded!")
                self.distribute_stones_from_countdown_pit()

        #warp pit
        elif last_pit_index == self.warp_pit:
            print("Warp pit activated! Warping to a random pit on the opponent's side.")
            self.warp_to_random_pit()

    def distribute_stones_from_countdown_pit(self):
        stones_to_distribute = self.board[self.countdown_pit]
        self.board[self.countdown_pit] = 0

        pit_index = (self.countdown_pit + 1) % len(self.board)
        while stones_to_distribute > 0:
            if (self.current_player == 1 and pit_index == self.pits_per_player + 1) or (
                self.current_player == 2 and pit_index == 0
            ):
                continue  #skip opponent's store
            self.board[pit_index] += 1
            stones_to_distribute -= 1
            pit_index = (pit_index + 1) % len(self.board)

        self.countdown_pit = random.randint(1, self.pits_per_player)  # Randomly choose a new countdown pit
        self.countdown_counter = 3  #reset countdown counter

    def warp_to_random_pit(self):
        opponent_pits = list(range(1, self.pits_per_player + 1))
        opponent_pits.reverse()  #reverse the list to simulate moving in the opposite direction

        random_opponent_pit = random.choice(opponent_pits)
        print(f"Warped to pit {random_opponent_pit} on the opponent's side!")

        stones_to_move = self.board[random_opponent_pit]
        self.board[random_opponent_pit] = 0

        pit_index = (random_opponent_pit + 1) % len(self.board)
        while stones_to_move > 0:
            if (self.current_player == 1 and pit_index == self.pits_per_player + 1) or (
                self.current_player == 2 and pit_index == 0
            ):
                continue  #skip opponent store
            self.board[pit_index] += 1
            stones_to_move -= 1
            pit_index = (pit_index + 1) % len(self.board)

    def switch_player(self):
        self.current_player = 3 - self.current_player  #switch between Player 1 and Player 2

# Example usage:
if __name__ == "__main__":
    game = MancalaGame()

    while True:
        game.display_board()

        if game.current_player == 1:
            pit_choice = int(input(f"Player 1, choose a pit (1-{game.pits_per_player}): ")) - 1
        else:
            pit_choice = random.randint(1, game.pits_per_player) - 1
            print(f"Player 2 chose pit {pit_choice + 1} randomly.")

        if 0 <= pit_choice < game.pits_per_player and game.board[pit_choice + 1] != 0:
            another_turn = game.make_move(pit_choice + 1)

            if not another_turn:
                game.switch_player()
        else:
            print("Invalid move. Try again.")
