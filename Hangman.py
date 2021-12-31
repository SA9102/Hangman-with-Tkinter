from tkinter import *
import random

WIDTH = '500'
HEIGHT = '375'
BG_COLOUR = '#49826e'

word = 0
fill_text = '' # the word which is to be filled; displays the letters that the user has entered, and
               # underscores for the missing letters
guessed_letters = [] # the letters which the user has already guessed

# the procedure that chooses a word from the text file
def chooseWord():
    global failed_guesses
    global guessed_letters
    guessed_letters = []

    failed_guesses = 0
    failed_guesses_text.config(text='Failed guesses: ' + str(failed_guesses) + '/5')
    game_over_text.config(text='')

    # get the number of words in the file
    file = open('European Countries.txt', 'r')
    length = len(file.readlines())
    file.close()

    # the random number chosen will correspond to the line number of a word - this will be the chosen word
    random_line = random.randint(1, length)

    global word

    # open the file again so that we can iterate through it from the beginning again
    file = open('European Countries.txt', 'r')

    # use the random number to choose the word
    line = 0
    for i in file:
        line += 1
        if line == random_line:
            word = i
            break
    file.close()

    word = word.strip().upper()
    global fill_text
    fill_text = ''
    for j in word:

        # spaces are represented by a ' / ' (spaces on either side)
        if j == ' ':
            fill_text += ' / '
        # letters are represented by a ' _ ' (spaces on either side)
        else:
            fill_text += ' _ '
    word_label.config(text=fill_text)


# the procedure that checks whether or not the letter entered is in the word
def processInput():
    global failed_guesses
    global fill_text
    
    # i.e. if the player is still playing (not lost and not won yet)
    if failed_guesses < 5 and '_' in fill_text:
        letter = letter_entry.get()

        # the program will not accept words or phrases
        if len(letter) != 1:
            info_text.config(text='Invalid input')
        else:
            letter = letter.upper()

            # if the letter is a capital letter; if the input is a number or symbol, it will
            # not change if the program tries to make it an uppercase. So, this condition is
            # used to ensure that only uppercase and lowercase letters are accepted
            if ord(letter) < 65 or ord(letter) > 90:
                info_text.config(text='Invalid input')
            else:

                if letter in guessed_letters:
                    info_text.config(text='You already guessed that letter')

                else: 

                    letter_flag = False # a flag that is used to indicate whether or not the word contains the entered letter
                    info_text.config(text='')
                    index = 0

                    global word
                    for i in word:
                        if letter == i:
                            letter_flag = True # the text contains the entered letter, so set this flag to True
                            index_for_insertion = (index-1) + (2 * (index + 1))
                            fill_text = fill_text[:index_for_insertion] + letter + fill_text[index_for_insertion + 1:]
                            word_label.config(text=fill_text)

                        index += 1

                    guessed_letters.append(letter)
                    
                    # if this flag remains False, then it means that the entered letter is not in the word
                    if letter_flag == False:
                        failed_guesses += 1
                        failed_guesses_text.config(text='Failed guesses: ' + str(failed_guesses)+'/5')

                        if failed_guesses > 4:
                            game_over_text.config(text='Game over. The country was: ' + word)
                    else:
                        # if there are no underscores, then it means that all letters have been entered, so the user has correctly
                        # guessed the country name
                        if '_' not in fill_text: 
                            game_over_text.config(text='You guessed the word!\nClick "Choose another word" to have another go.')


root = Tk()
root.config(bg=BG_COLOUR)
root.geometry(WIDTH + 'x' + HEIGHT)
root.resizable(False, False)

display_frame = Frame(root, bg=BG_COLOUR)
display_frame.pack()

title_label = Label(display_frame, text='Hangman', font='Bahnschrift 20 bold', bg=BG_COLOUR, pady=20)
title_label.pack()

button = Button(display_frame, text='Choose another word', font='Bahnschrift 10', bg='#28473c', fg='white', command=chooseWord)
button.pack()

# this displays the word, where the missing letters are shown as underscores
word_label = Label(display_frame, font='Bahnschrift 15', bg=BG_COLOUR, pady=20)
word_label.pack()

enter_text = Label(display_frame, text='Please enter a letter', font='Bahnschrift 10', bg=BG_COLOUR, pady=10)
enter_text.pack()

# an entry where the user enters a letter
letter_entry = Entry(display_frame, font='Bahnschrift 10', width=1)
letter_entry.pack()

# this text informs the user that the input is invalid, or that they have already guessed that letter
info_text = Label(display_frame, text='', font='Bahnschrift 10', bg=BG_COLOUR, pady=7)
info_text.pack()

enter_button = Button(display_frame, text='Enter', bg='#28473c', fg='white', command=processInput)
enter_button.pack()

failed_guesses = 0
failed_guesses_text = Label(display_frame, text='Failed guesses: ' + str(failed_guesses)+'/5', bg=BG_COLOUR, font='Bahnschrift 10')
failed_guesses_text.pack()

game_over_text = Label(display_frame, bg=BG_COLOUR, font='Bahnschrift 10')
game_over_text.pack()


chooseWord()


root.mainloop()
