from tkinter import *

from functools import partial # to prevent unwanted windows
import random


class Start:
    def __init__(self,parent):

        # GUI to get starting balance and stakes
        self.start_frame = Frame(padx=10, pady=10)
        self.start_frame.grid()

        # mystery heading (row 0)
        self.mystery_box_label = Label(self.start_frame, text="Mystery Box Game",
                                       font="Garamond 19 bold")
        self.mystery_box_label.grid(row=1)

        # entry box (row 1)
        self.start_amount_entry = Entry(self.start_frame, font="Arial 16 bold")
        self.start_amount_entry.grid(row=2)

        # button frame
        self.start_button_frame = Frame(self.start_frame)
        self.start_button_frame.grid(row=3, pady=10)

        # play button (row 2)
        self.lowstakes_button = Button(self.start_button_frame, text="Low ($5)",
                                       highlightbackground="orange",
                                       command=lambda: self.to_game(1))
        self.lowstakes_button.grid(row=0, column=0, pady=10)

        # play button (row 3)
        self.medstakes_button = Button(self.start_button_frame, text="Medium ($10)",
                                       highlightbackground="yellow",
                                       command=lambda: self.to_game(1))
        self.medstakes_button.grid(row=0, column=1, pady=10)

        # play button (row 4)
        self.highstakes_button = Button(self.start_button_frame, text="High ($15)",
                                        highlightbackground="green",
                                        command=lambda: self.to_game(1))
        self.highstakes_button.grid(row=0, column=2, pady=10)

    def to_game(self, stakes):
        starting_balance = self.start_amount_entry.get()
        Game(self, stakes, starting_balance)


class Game:
    def __init__(self, partner, stakes, starting_balance):
        print(stakes)
        print(starting_balance)

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

