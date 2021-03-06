from tkinter import *
from functools import partial  # to prevent unwanted windows
import random
import re


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
        starting_balance = int(starting_balance)

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
        # hold values in game_stats_list
        self.totals_list = []
        self.game_stats_list = [int(starting_balance), int(starting_balance)]
        print(f"Stakes: {stakes}")
        print(f"Starting Balance: {starting_balance}")
        starting_balance = int(starting_balance)

        # initialise variables
        self.balance = 0  # IntVar()
        # set balance to amount entered by user at start of game
        # self.balance.get(starting_balance)
        self.balance = self.balance + starting_balance
        # starting balance needs to be int!!
        '''self.game_stats_list.append(self.balance)
        list_name.insert(index, element)'''
        self.game_stats_list.insert(0, self.balance)

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

        # new lists
        self.round_stats_list = []

        # help and game stats button (row 5)
        self.help_stats_frame = Frame(self.game_frame)
        self.help_stats_frame.grid(row=5, pady=10)

        self.help_button = Button(self.help_stats_frame, text="Help / Rules",
                                  font="arial 15 bold", highlightbackground="#808080", command=self.game_help)
        self.help_button.grid(row=0, column=0, padx=2)

        # stats button
        self.stats_button = Button(self.help_stats_frame, text="Game Stats",
                                   font="arial 14", highlightbackground="#003366",
                                   command=lambda: self.to_stats(self.round_stats_list, self.game_stats_list, self.totals_list))
        self.stats_button.grid(row=0, column=1, padx=2)

        # quit button
        self.quit_button = Button(self.game_frame, text="Quit",
                                  font="arial 15 bold", width=20,
                                  command=self.to_quit, pady=10, padx=10,
                                  highlightbackground="red")
        self.quit_button.grid(row=6, padx=10)

    def reveal_boxes(self):
        # retrieve the balance from the initial function
        current_balance = 0
        current_balance += self.balance
        # {} in the list
        # self.game_stats_list.append(current_balance)

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
            """print(stakes_multiplier)
            print(prize)
            print(round_winnings)"""
            self.round_stats_list.append(round_winnings)
        print(self.round_stats_list)
        # is it the sum value or is it the last value of the round_stats_list???
        sum_list = sum(self.round_stats_list)
        print(f"Sum List: {sum_list}")
        # self.game_stats_list.append(sum_list)

        # display prizes and change background colour of the box
        self.prize1_label.config(text=prize_list[0], bg=background_colours[0])
        self.prize2_label.config(text=prize_list[1], bg=background_colours[1])
        self.prize3_label.config(text=prize_list[2], bg=background_colours[2])

        # deduct cost of game
        current_balance += 5 * stakes_multiplier

        # add winnings
        current_balance += round_winnings

        # set balance to new balance
        # change self.balance.set(current_balance) since not IntVar
        # self.balance = current_balance

        balance_statement = f"Game Cost: ${5* stakes_multiplier}\nPayback: ${round_winnings} \n" \
                            f"Current Balance: ${current_balance}"
        print(f"Current Balance: {current_balance}")
        # change to totals?? self.game_stats_list.append(current_balance)
        self.totals_list.append(current_balance)
        self.game_stats_list.insert(1, current_balance)

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

    def to_stats(self, game_history, game_stats, all_values):
        Statistics(self, game_history, game_stats, all_values)

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
    def __init__(self, partner, game_history, game_stats, all_values):
        background = "#555555"
        heading = "arial 12 bold"
        content = "arial 12"

        print(game_history)

        # disable stats button
        partner.stats_button.config(state=DISABLED)

        # set up child window (i.e. help box)
        self.stats_box = Toplevel()

        # if user press cross at, top, closes help and 'releases' stats button
        self.stats_box.protocol('WM_DELETE_WINDOW', partial(self.close_stats, partner))

        # set up GUI frame
        self.stats_frame = Frame(self.stats_box, bg=background)
        self.stats_frame.grid()

        # set up heading (row 0)
        self.stats_heading = Label(self.stats_frame, text="Game Statistics",
                                   fg="white", font="arial 10 bold", bg=background)
        self.stats_heading.grid(row=0)

        # to export instructions
        self.export_instructions = Label(self.stats_frame,
                                         text="Here are your Game Statistics. "
                                              "Please use the export button to "
                                              "access the results of each "
                                              "round that you played", wrap=250,
                                         font="arial 10 italic", justify=LEFT, fg="green", bg="#7f7f7f")
        self.export_instructions.grid(row=1)

        # balance frame (row 2)
        self.details_frame = Frame(self.stats_frame, bg=background)
        self.details_frame.grid(row=2)

        # starting balance (row 2,0)
        self.starting_balance_label = Label(self.details_frame, text="Starting Balance:",
                                            font=heading, anchor="e", bg=background)
        self.starting_balance_label.grid(row=0, column=0, padx=0)

        self.start_balance_value_label = Label(self.details_frame, font=content,
                                               text=f"${game_stats[0]}", anchor="w", bg=background)
        self.start_balance_value_label.grid(row=0, column=1, padx=0)

        # current balance (row 2,1)
        self.current_balance_label = Label(self.details_frame, text="Current Balance:",
                                           font=heading, anchor="e", bg=background)
        self.current_balance_label.grid(row=1, column=0, padx=0)
        print(game_stats[1])
        self.current_balance_value_label = Label(self.details_frame, font=content,
                                                 text=f"${game_stats[1]}", anchor="w", bg=background)
        self.current_balance_value_label.grid(row=1, column=1, padx=0)

        print(f"game stats: {game_stats}")
        if game_stats[1] > game_stats[0]:
            win_loss = "Amount Won: "
            amount = game_stats[1] - game_stats[0]
            win_loss_fg = "green"
        else:
            win_loss = "Amount Lost: "
            amount = game_stats[0] - game_stats[1]
            win_loss_fg = "red"


        # amount won / lost (row 2,2)
        self.win_loss_label = Label(self.details_frame, text=f"{win_loss}",
                                    font=heading, anchor="e", bg=background)
        self.win_loss_label.grid(row=2, column=0, padx=0)

        self.win_lose_value_label = Label(self.details_frame, font=content,
                                          fg=win_loss_fg,
                                          text=f"${amount}", anchor="w", bg=background)
        self.win_lose_value_label.grid(row=2, column=1, padx=0)

        # rounds played (row 2,4)
        self.games_played_label = Label(self.details_frame,
                                        text="Rounds Played", font=heading,
                                        anchor="e", bg=background)
        self.games_played_label.grid(row=3, column=0, padx=0)

        self.games_played_value_label = Label(self.details_frame, font=content,
                                              text=len(all_values), anchor="w", bg=background)
        self.games_played_value_label.grid(row=3, column=1, padx=0)

        # stats text (label, row 1)
        '''self.stats_text = Label(self.stats_frame, text=round_stats_list,
                               justify=LEFT, width=40, bg=background, wrap=250, fg="white")
        self.stats_text.grid(row=1)'''

        # bottom row of button frame (row 3)
        self.bot_button_frame = Frame(self.stats_frame, bg=background)
        self.bot_button_frame.grid(row=3)

        # export button, next to dismiss on left (row 1, column 0)
        self.export_button = Button(self.bot_button_frame, text="Export",
                                    width=10, bg='orange', font="arial 10 bold",
                                    command=partial(self.export_stats, partner, game_stats, game_history))
        self.export_button.grid(row=1, column=0, pady=10)

        # dismiss button (row 3)
        self.dismiss_btn = Button(self.bot_button_frame, text="Dismiss",
                                  width=10, bg='orange', font="arial 10 bold",
                                  command=partial(self.close_stats, partner))
        self.dismiss_btn.grid(row=1, column=1, pady=10)


    def close_stats(self, partner):
        # put help button back to normal...
        partner.stats_button.config(state=NORMAL)
        self.stats_box.destroy()

    def export_stats(self, partner, game_history, game_stats):
        Export(self, game_history, game_stats)


class Export:
    def __init__(self, partner, game_history, game_stats):
        background = "#404040"  # dark grey

        print(game_stats)

        # disable export button
        partner.export_button.config(state=DISABLED)

        # set up child window (i.e. export box)
        self.export_box = Toplevel()

        # if user press cross at, top, closes export and 'releases' export button
        self.export_box.protocol('WM_DELETE_WINDOW',
                                 partial(self.close_export, partner))

        # set up GUI frame
        self.export_frame = Frame(self.export_box, width=300, bg=background)
        self.export_frame.grid()

        # set up export heading (row 0)
        self.how_heading = Label(self.export_frame, text="Export / Instructions",
                                 font="Garamond 14 bold", bg=background, fg="#ffffff")
        self.how_heading.grid(row=0)

        # export text (label, row 1)
        self.export_text = Label(self.export_frame, text="Enter a filename "
                                                         "in the box below "
                                                         "and press the Save "
                                                         "button to save your "
                                                         "calculation history "
                                                         "to a text file",
                                 justify=LEFT, width=40,
                                 bg=background, wrap=250, fg="#ffffff")
        self.export_text.grid(row=1)

        # export text (label, row 1)
        self.export_text = Label(self.export_frame, text="If the filename "
                                                    "you enter below "
                                                    "already exists, "
                                                    "its contents will "
                                                    "be replaced with "
                                                    "your calculation "
                                                    "history",
                                 justify=LEFT, bg="#555555",
                                 fg="red", wrap=225, padx=10, pady=10,
                                 font="arial 10 italic")
        self.export_text.grid(row=2)

        # file name entry box (row 3)
        self.filename_entry = Entry(self.export_frame, width=20,
                                    font="arial 14 bold", justify=CENTER)
        self.filename_entry.grid(row=3, pady=10)

        # error message labels (initially blank, row 4)
        self.save_error_label = Label(self.export_frame, text="", fg="#ffafaf",
                                      bg=background)
        self.save_error_label.grid(row=4)

        # save / cancel frame (row 5)
        self.save_cancel_frame = Frame(self.export_frame)
        self.save_cancel_frame.grid(row=5, pady=10)

        # save and cancel buttons (row 0 of save_cancel frame)
        self.save_button = Button(self.save_cancel_frame, text="Save",
                                  font="Arial 14 bold", padx=5, pady=5,
                                  highlightbackground="#ffbb33",
                                  command=partial(lambda: self.save_history(partner, game_history, game_stats)))
        self.save_button.grid(row=0, column=0)

        self.cancel_button = Button(self.save_cancel_frame, text="Cancel",
                                    font="Arial 14 bold",
                                    padx=5, pady=5,
                                    highlightbackground= "#FFD580",
                                    command=partial(self.close_export, partner))
        self.cancel_button.grid(row=0, column=1)

    def save_history(self, partner, game_history, game_stats):
        # get filename, can't be blank or invalid
        valid_char = "[A-Za-z0-9_]"
        has_error = "no"

        # retrieve input entered into Entry field
        filename = self.filename_entry.get()
        print(filename)

        for letter in filename:
            if re.match(valid_char, letter):
                continue

            elif letter == " ":
                problem = "(no spaces allowed)"
                has_error = "yes"

            else:
                problem = ("(no {}'s allowed)".format(letter))
                has_error = "yes"
            break

        if filename == "":
            problem = "can't be blank"
            has_error = "yes"

        # check that there are no errors before saving the file
        if has_error == "yes":
            # display error message
            self.save_error_label.config(text="Invalid filename - {}".format(problem))
            # change entry box to pink
            self.filename_entry.config(bg="#ffafaf")
            print("error in filename")

        else:
            print("you entered a valid filename")

            # add .txt suffix!
            filename = filename + ".txt"

            # create file to hold data
            f = open(filename, "w+")

            # heading
            f.write("Game Statistics \n\n")

            # stats display
            # add new line at end of each item
            for round in game_stats:
                round = str(round)
                f.write(round + "\n")

            # heading for rounds
            f.write("\nRound Details\n\n")

            for data in game_history:
                data = str(data)
                f.write(data + "\n")

            # close file
            f.close()
            # close dialogue
            self.close_export(partner)

    def close_export(self, partner):
        # put export button back to normal...
        partner.export_button.config(state=NORMAL)
        self.export_box.destroy()


# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Mystery Box Game")
    something = Start(root)
    root.mainloop()
