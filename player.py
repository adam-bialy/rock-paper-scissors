from random import randint


class Player:

    def __init__(self):
        self.credits = 0
        self.games = 0
        self.wins = 0

    def add_credits(self):
        if self.credits == 0:
            self.credits += 10
        else:
            raise ValueError("You cannot add credits if you more than 0.")

    def play_game(self, choice):
        if self.credits < 3:
            raise ValueError("You have too few credits to play. One game costs 3 credits.")
        self.credits -= 3
        computer = randint(0, 2)
        d = {"rock": 0, "paper": 1, "scissors": 2}
        l = ["rock", "paper", "scissors"]
        print(f"You choose {choice}, computer chose {l[computer]}")
        choice = d[choice]
        if (choice + 1) % 3 == computer:
            print("You lose.")
        elif choice == computer:
            print("It is a draw.")
        else:
            self.credits += 4
            print("You win.")


if __name__ == "__main__":
    player = Player()
    player.add_credits()
    for i in range(3):
        player.play_game("rock")
        print(player.credits)
