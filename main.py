from tkinter import *

from functools import partial  # to prevent unwanted windows
import random


class Start:
    def __init__(self, parent):
        # GUI to get starting balance and stakes
        self.start_frame = Frame(padx=10, pady=10)
        self.start_frame.grid()

        # mystery heading (row 0)
        self.mystery_box_label = Label(self.start_frame, text="Mystery Box Game",
                                       font="Garamond 19 bold")
        self.mystery_box_label.grid(row=0)

        # initial instructions (row 1)
        self.mystery_instructions = Label(self.start_frame, font="Arial 10  italic",
                                          text="Please enter a dollar amount "
                                               "(between $5 and $50) in the box "
                                               "below. Then choose the stakes.The "
                                               "higher the stakes the more you can win!",
                                          wrap=275, justify=LEFT, padx=10, pady=10)
        self.mystery_instructions.grid(row=1)

        # entry box (row 2)
        self.start_amount_entry = Entry(self.start_frame, font="Arial 16 bold")
        self.start_amount_entry.grid(row=2)

        # button frame (row 2)
        self.start_button_frame = Frame(self.start_frame)
        self.start_button_frame.grid(row=3, pady=10)

        # button custom
        button_font = "Garamond 12 bold"

        # low button #ff9200|orange
        self.low_stakes_button = Button(self.start_button_frame, text="Low ($5)",
                                        highlightbackground="#ff9200", font=button_font,
                                        command=lambda: self.to_game(1))
        self.low_stakes_button.grid(row=0, column=0, padx=5, pady=10)

        # medium button #ffff36|yellow
        self.med_stakes_button = Button(self.start_button_frame, text="Medium ($10)",
                                        highlightbackground="#ffff36", font=button_font,
                                        command=lambda: self.to_game(2))
        self.med_stakes_button.grid(row=0, column=1, padx=5, pady=10)

        # play button (row 4) #52eb33|green
        self.high_stakes_button = Button(self.start_button_frame, text="High ($15)",
                                         highlightbackground="#52eb33", font=button_font,
                                         command=lambda: self.to_game(3))
        self.high_stakes_button.grid(row=0, column=2, padx=5, pady=10)

        self.amount_error_label = Label(self.start_frame, text="",
                                        justify=LEFT, width=40,
                                        wrap=250)
        self.amount_error_label.grid(row=4)

        # help button
        self.help_button = Button(self.start_frame, text="How to Play",
                                  highlightbackground="#808080", font=button_font)
        self.help_button.grid(row=4, padx=5, pady=10)

    def to_game(self, stakes):
        starting_balance = self.start_amount_entry.get()

        # set error background colours (and assume that there are no errors at the start
        error_back = "#ffafaf"
        has_errors = "no"

        # change background to white (for testing purposes)
        self.start_amount_entry.config(bg="white")
        self.amount_error_label.config(text="")

        try:
            starting_balance = int(starting_balance)

            if starting_balance < 5:
                has_errors = "yes"
                error_feedback = "Sorry the least you " \
                                 "can play with is $5"
            elif starting_balance > 50:
                has_errors = "yes"
                error_feedback = "Too high! The most you can risk in" \
                                 "this game is $50"
            elif starting_balance < 10 and (stakes == 2 or stakes == 3):
                has_errors = "yes"
                error_feedback = "Sorry you can only afford to " \
                                 "play a low stakes game"
            elif starting_balance < 15 and stakes == 3:
                has_errors = "yes"
                error_feedback = "Sorry, you can only afford to " \
                                 "play a low or medium game."
        except ValueError:
            has_errors = "yes"
            error_feedback = "Please enter a dollar amount (no text / decimals)"

        if has_errors == "yes":
            self.start_amount_entry.config(bg=error_back)
        else:
            Game(self, stakes, starting_balance)

            # hide start up window
            # root.withdraw()


class Game:
    def __init__(self, partner, stakes, starting_balance):
        print(stakes)
        print(starting_balance)

        # disable low stakes button
        partner.low_stakes_button.config(state=DISABLED)

        # initialise variables
        self.balance = IntVar()

        # set starting balance to amount entered by user at start of game
        self.balance.set(starting_balance)

        # GUI setup
        self.game_box = Toplevel()
        self.game_frame = Frame(self.game_box)
        self.game_frame.grid()

        # heading row
        self.heading_label = Label(self.game_frame, text="Heading",
                                   font="Arial 24 bold",
                                   padx=10, pady=10)
        self.heading_label.grid(row=0)

        # balance label
        self.balance_frame = Frame(self.game_frame)
        self.balance_frame.grid(row=1)

        self.balance_label = Label(self.game_frame, text="Balance")
        self.balance_label.grid(row=2)

        self.play_button = Button(self.game_frame, text="Gain",
                                  padx=10, pady=10, command=self.reveal_boxes)
        self.play_button.grid(row=3)

    def reveal_boxes(self):
        # retrieve the balance from the initial function
        current_balance = self.balance.get()

        # adjust the balance (subtract game cost and add pay out)
        # for testing purposes, just add 2
        current_balance += 2

        # set balance to adjusted balance
        self.balance.set(current_balance)

        # edit label so user can see their balance
        self.balance_label.configure(text="Balance: {}".format(current_balance))


# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Temperature Converter")
    something = Start(root)
    root.mainloop()
