from random import randint


def play_rps(choice):

    d = {"rock": 0, "paper": 1, "scissors": 2}
    l = ["rock", "paper", "scissors"]

    choice_no = d[choice]
    computer_no = randint(0, 2)

    msg = f"You chose {choice.title()} vs {l[computer_no].title()}: "

    if (choice_no + 1) % 3 == computer_no:
        return "lose", msg + "you lose."
    elif choice_no == computer_no:
        return "draw", msg + "it's a draw."
    else:
        return "win", msg + "you win!"