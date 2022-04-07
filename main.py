from tkinter import *
from functools import partial  # to prevent unwanted windows
import random


class Start:
    def __init__(self, parent):

        # GUI to get starting balance and stakes
        self.start_frame = Frame(padx=10, pady=10)
        self.start_frame.grid()

        # set initial balance to zero
        self.starting_funds = IntVar()
        self.starting_funds.set(0)

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

        # entry box, button and error label (row 2)
        self.entry_error_frame = Frame(self.start_frame, width=200)
        self.entry_error_frame.grid(row=2)

        # entry box (row 2)
        self.start_amount_entry = Entry(self.entry_error_frame, font="Arial 19 bold", width=20)
        self.start_amount_entry.grid(row=0, column=0)

        self.add_funds_button = Button(self.entry_error_frame,
                                       font="Arial 14 bold", text="Add Funds",
                                       command=self.check_funds, pady=5, padx=5)
        self.add_funds_button.grid(row=0, column=1)

        self.amount_error_label = Label(self.entry_error_frame, fg="maroon",
                                        text="", justify=LEFT,
                                        width=40, wrap=250)
        self.amount_error_label.grid(row=1, columnspan=2, pady=5)

        # button frame (row 2)
        self.start_button_frame = Frame(self.start_frame)
        self.start_button_frame.grid(row=3, pady=10)

        # button custom
        button_font = "Garamond 12 bold"

        # low button #ff9200|orange
        self.low_stakes_button = Button(self.start_button_frame, text="Low ($5)",
                                        highlightbackground="#ff9200", font=button_font,
                                        command=lambda: self.to_game(1))
        self.low_stakes_button.grid(row=0, column=0, padx=5, pady=5)

        # medium button #ffff36|yellow
        self.med_stakes_button = Button(self.start_button_frame, text="Medium ($10)",
                                        highlightbackground="#ffff36", font=button_font,
                                        command=lambda: self.to_game(2))
        self.med_stakes_button.grid(row=0, column=1, padx=5, pady=5)

        # play button (row 4) #52eb33|green
        self.high_stakes_button = Button(self.start_button_frame, text="High ($15)",
                                         highlightbackground="#52eb33", font=button_font,
                                         command=lambda: self.to_game(3))
        self.high_stakes_button.grid(row=0, column=2, padx=5, pady=5)

        # disable all stake buttons at start
        self.low_stakes_button.config(state=DISABLED)
        self.med_stakes_button.config(state=DISABLED)
        self.high_stakes_button.config(state=DISABLED)

        # help button
        self.help_button = Button(self.start_frame, text="How to Play",
                                  highlightbackground="#808080", font=button_font,
                                  command=self.help)
        self.help_button.grid(row=4, padx=5, pady=10)

    def check_funds(self):
        starting_balance = self.start_amount_entry.get()

        # set error background colours (and assume that there are no errors at the start
        error_back = "#ffafaf"
        has_errors = "no"

        # change background to white (for testing purposes)
        self.start_amount_entry.config(bg="white")
        self.amount_error_label.config(text="")

        # disable all stakes buttons incase user changes mind and decreases amount entered
        self.low_stakes_button.config(state=DISABLED)
        self.med_stakes_button.config(state=DISABLED)
        self.high_stakes_button.config(state=DISABLED)

        try:
            starting_balance = int(starting_balance)

            if starting_balance < 5:
                has_errors = "yes"
                error_feedback = "Sorry the least you can play with is $5"
            elif starting_balance > 50:
                has_errors = "yes"
                error_feedback = "Too high! The most you can risk in this game is $50"

            elif starting_balance >= 15:
                self.low_stakes_button.config(state=NORMAL)
                self.med_stakes_button.config(state=NORMAL)
                self.high_stakes_button.config(state=NORMAL)
            elif starting_balance >= 10:
                self.low_stakes_button.config(state=NORMAL)
                self.med_stakes_button.config(state=NORMAL)
            else:
                self.low_stakes_button.config(state=NORMAL)

        except ValueError:
            has_errors = "yes"
            error_feedback = "Please enter a dollar amount (no text / decimals)"

        if has_errors == "yes":
            self.start_amount_entry.config(bg=error_back)
            self.amount_error_label.config(text=error_feedback)
        else:
            # set starting balance to amount entered by user
            self.starting_funds.set(starting_balance)

    def help(self):
        print("You asked for help")
        get_help = Help(self)
        get_help.help_text.configure(text="Help text goes here... add later")

    def to_game(self, stakes):
        # retrieve starting balance
        starting_balance = self.start_amount_entry.get()

        Game(self, stakes, starting_balance)

        # hide start up window
        self.start_frame.destroy()


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
        # if user presses the cross at the top, game quits
        self.game_box.protocol('WM_DELETE_WINDOW', self.to_quit)

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

        # bind button to ,enter. (users can push enter to reveal the boxes)
        self.play_button.focus()
        self.play_button.bind('<Return>', lambda e: self.reveal_boxes())
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
                                  font="arial 15 bold", highlightbackground="#808080", command=self.game_help )
        self.help_button.grid(row=0, column=0, padx=2)

        self.stats_button = Button(self.help_export_frame, text="Game Stats...",
                                   font="arial 15 bold", highlightbackground="#003366", command=self.game_stats)
        self.stats_button.grid(row=0, column=1, padx=2)

        # quit button
        self.quit_button = Button(self.game_frame, text="Quit",
                                  font="arial 15 bold", width=20,
                                  command=self.to_quit, pady=10, padx=10,
                                  highlightbackground="red")
        self.quit_button.grid(row=6, padx=10)

    def reveal_boxes(self):
        # retrieve the balance from the initial function
        current_balance = self.balance.get()
        stakes_multiplier = self.multiplier.get()

        round_winnings = 0
        prize_list = []
        background_colours = []

        for item in range(0, 3):
            prize_num = random.randint(1, 100)

            if 0 < prize_num <= 5:
                prize = f"gold\n(${5* stakes_multiplier})"
                back_colour = "#926f34"  # gold
                round_winnings += 5* stakes_multiplier
            elif 5 < prize_num <= 25:
                prize = f"silver\n(${2* stakes_multiplier})"
                back_colour = "#BEC2CB"  # silver
                round_winnings += 2*stakes_multiplier
            elif 25 < prize_num <= 65:
                prize = f"copper\n(${1* stakes_multiplier})"
                back_colour = "#b87333"  # copper
                round_winnings += stakes_multiplier
            else:
                prize = "lead\n($0)"
                back_colour = "#6c6c6a"  # lead

            prize_list.append(prize)
            background_colours.append(back_colour)

        # display prizes and change background colour of the box
        self.prize1_label.config(text=prize_list[0], bg=background_colours[0])
        self.prize2_label.config(text=prize_list[1], bg=background_colours[1])
        self.prize3_label.config(text=prize_list[2], bg=background_colours[2])

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

        if current_balance < 5 * stakes_multiplier:
            self.play_button.config(state=DISABLED)
            self.game_box.focus()
            self.play_button.config(text="Game Over")
            balance_statement = f"Current Balance: ${current_balance}\n" \
                                f"You balance is too low. You can only quit " \
                                f"or view your stats. Sorry about that."
            self.balance_label.config(fg="red", font="arial 10 bold",
                                      text=balance_statement)

    def game_help(self):
        get_help = Help(self)
        get_help.help_text.configure(text="Help text goes here")

    def game_stats(self):
        get_stats = Statistics(self)

    def to_quit (self):
        root.destroy()


class Help:
    def __init__(self, partner):
        background = "#555555"
        # disable help button
        partner.help_button.config(state=DISABLED)
        # set up child window (i.e. help box)
        self.help_box = Toplevel()
        # if user press cross at, top, closes help and 'releases' help button
        self.help_box.protocol('WM_DELETE_WINDOW', partial(self.close_help, partner))
        # set up GUI frame
        self.help_frame = Frame(self.help_box, width=300, bg=background)
        self.help_frame.grid()

        # set up heading (row 0)
        self.how_heading = Label(self.help_frame, text="Help / Instructions",
                                 fg="white", font="arial 10 bold", bg=background)
        self.how_heading.grid(row=0)

        # help text (label, row 1)
        self.help_text = Label(self.help_frame, text="",
                               justify=LEFT, width=40, bg=background, wrap=250, fg="white")
        self.help_text.grid(row=1)

        # dismiss button (row 2)
        self.dismiss_btn = Button(self.help_frame, text="Dismiss",
                                  width=10, bg='orange', font="arial 10 bold",
                                  command=partial(self.close_help, partner))
        self.dismiss_btn.grid(row=2, pady=10)

    def close_help(self, partner):
        # put help button back to normal...
        partner.help_button.config(state=NORMAL)
        self.help_box.destroy()


class Statistics:
    def __init__(self, partner):
        background = "#555555"
        # disable help button
        partner.stats_button.config(state=DISABLED)
        # set up child window (i.e. help box)
        self.stats_box = Toplevel()
        # if user press cross at, top, closes help and 'releases' help button
        self.stats_box.protocol('WM_DELETE_WINDOW', partial(self.close_stats, partner))
        # set up GUI frame
        self.stats_frame = Frame(self.stats_box, width=300, bg=background)
        self.stats_frame.grid()

        # set up heading (row 0)
        self.how_heading = Label(self.stats_frame, text="Game Statistics",
                                 fg="white", font="arial 10 bold", bg=background)
        self.how_heading.grid(row=0)

        # help text (label, row 1)
        self.stats_text = Label(self.stats_frame, text="",
                               justify=LEFT, width=40, bg=background, wrap=250, fg="white")
        self.stats_text.grid(row=1)

        # dismiss button (row 2)
        self.dismiss_btn = Button(self.stats_frame, text="Dismiss",
                                  width=10, bg='orange', font="arial 10 bold",
                                  command=partial(self.close_stats, partner))
        self.dismiss_btn.grid(row=2, pady=10)

    def close_stats(self, partner):
        # put help button back to normal...
        partner.stats_button.config(state=NORMAL)
        self.stats_box.destroy()


# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Temperature Converter")
    something = Start(root)
    root.mainloop()
