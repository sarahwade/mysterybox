from tkinter import *
from functools import partial # to prevent unwanted windows
import random


class Start:
    def __init__(self,parent):

        # GUI to get starting balance and stakes
        self.start_frame = Frame(padx=10, pady=10)
        self.start_frame.grid()

        self.push_me_button = Button(text="Push Me", command=self.to_game)
        self.push_me_button.grid(row=0, pady=10)

    def to_game(self):
        # retrieve starting balance
        starting_balance = 50
        stakes = 1

        Game(self, stakes, starting_balance)

        # hide start up window
        root.withdraw()


class Game:
    def __init__(self, partner, stakes, starting_balance):
        print(stakes)
        print(starting_balance)

        # initialise variables
        self.balance = IntVar()
        # set balance to amount entered by user at start of game
        self.balance.set(starting_balance)

        # get value of stakes (use it as a multiplier when calculating winnings
        self.multiplier = IntVar()
        self.multiplier.set(stakes)

        # GUI setup
        self.game_box = Toplevel()
        self.game_frame = Frame(self.game_box)
        self.game_frame.grid()

        # heading row
        self.heading_label = Label(self.game_frame, text="Play...",
                                   font="arial 24 bold", padx=10,
                                   pady=10)
        self.heading_label.grid(row=0)

        # instructions label
        self.instructions_label = Label(self.game_frame, wrap=300, justify=LEFT,
                                        text="Press <enter> or click the 'Open Boxes'"
                                             "button to reveal the contents of the"
                                             "mystery boxes.",
                                        font="arial 10", padx=10, pady=10)
        self.instructions_label.grid(row=1)

        # boxes go here (row 2)
        box_text = "arial 16 bold"
        box_back = "#b9ea96"  # light green
        box_width = 5
        self.box_frame = Frame(self.game_frame)
        self.box_frame.grid(row=2, pady=10)

        self.prize1_label = Label(self.box_frame, text="?\n", font=box_text,
                                  bg=box_back, width=box_width, padx=10, pady=10)
        self.prize1_label.grid(row=0, column=0)

        self.prize2_label = Label(self.box_frame, text="?\n", font=box_text,
                                  bg=box_back, width=box_width, padx=10, pady=10)
        self.prize2_label.grid(row=0, column=1)

        self.prize3_label = Label(self.box_frame, text="?\n", font=box_text,
                                  bg=box_back, width=box_width, padx=10, pady=10)
        self.prize3_label.grid(row=0, column=2)

        # play button goes here (row 3)
        self.play_button = Button(self.game_frame, text="Open Boxes",
                                  highlightbackground="#FFFF33", font="arial 15 bold",
                                  width=20, pady=10, padx=10, command=self.reveal_boxes)
        self.play_button.grid(row=3)

        # balance label (row 4)
        start_text = f"Game Cost: ${stakes*5} \n "" \n How much " \
                     "will you win?"

        self.balance_label = Label(self.game_frame, font="arial 12 bold",
                                   fg="green", text=start_text, wrap=300, justify=LEFT)
        self.balance_label.grid(row=4, pady=10)

        # help and game stats button (row 5)
        self.help_export_frame = Frame(self.game_frame)
        self.help_export_frame.grid(row=5, pady=10)

        self.help_button = Button(self.help_export_frame, text="Help / Rules",
                                  font="arial 15 bold", highlightbackground="#808080")
        self.help_button.grid(row=0, column=0, padx=2)

        self.stats_button = Button(self.help_export_frame, text="Game Stats...",
                                   font="arial 15 bold", highlightbackground="#003366")
        self.stats_button.grid(row=0, column=1, padx=2)

    def reveal_boxes(self):
        # retrieve the balance from the initial function
        current_balance = self.balance.get()
        stakes_multiplier = self.multiplier.get()

        round_winnings = 0
        prize_list = []
        for item in range(0, 3):
            prize_num = random.randint(1, 100)

            if 0 < prize_num <= 5:
                prize = f"gold\n(${5* stakes_multiplier})"
                round_winnings += 5* stakes_multiplier
            elif 5 < prize_num <= 25:
                prize = f"silver\n(${2* stakes_multiplier})"
                round_winnings += 2*stakes_multiplier
            elif 25 < prize_num <= 65:
                prize = f"copper\n(${1* stakes_multiplier})"
                round_winnings += stakes_multiplier
            else:
                prize = "lead\n($0)"

            prize_list.append(prize)

        # display prizes
        self.prize1_label.config(text=prize_list[0])
        self.prize2_label.config(text=prize_list[1])
        self.prize3_label.config(text=prize_list[2])

        # deduct cost of game
        current_balance -= 5 * stakes_multiplier

        # add winnings
        current_balance += round_winnings

        # set balance to new balance
        self.balance.set(current_balance)

        balance_statement = f"Game Cost: ${5* stakes_multiplier}\nPayback: ${round_winnings} \n" \
                            f"Current Balance: ${current_balance}"

        # edit label so user can see their balance
        self.balance_label.configure(text=balance_statement)

# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Temperature Converter")
    something = Start(root)
    root.mainloop()

