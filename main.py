import random
from tkinter import *
import pandas

# ---------------------------- CONSTANTS ------------------------------- #
BACKGROUND_COLOR = "#B1DDC6"
FONT_TITLE = ("Ariel", 40, "italic")
FONT_WORD = ("Ariel", 60, "bold")
FONT_WORD_FINAL = ("Ariel", 15, "bold")
current_card = {}
timer = None

# ---------------------------- PANDAS ------------------------------- #
try:
    data = pandas.read_csv("data/to_learn.csv")
    words_dict = data.to_dict(orient="records")
except:
    data = pandas.read_csv("data/french_words.csv")
    words_dict = data.to_dict(orient="records")


# ---------------------------- FUNCTIONS ------------------------------- #
def next_card():
    global current_card, flip_timer
    current_card = random.choice(words_dict)
    window.after_cancel(flip_timer)
    canvas.itemconfig(card, image=front_card_img)
    canvas.itemconfig(title_text, text="French", fill="black")
    canvas.itemconfig(word_text, text=current_card["French"], fill="black")
    flip_timer = window.after(5000, flip_card)


def flip_card():
    canvas.itemconfig(card, image=back_card_img)
    canvas.itemconfig(title_text, text="Español", fill="white")
    canvas.itemconfig(word_text, text=current_card["Español"], fill="white")


def known_word():
    try:
        words_dict.remove(current_card)
    except ValueError:
        canvas.itemconfig(title_text, text="Ya terminaste con las palabras", fill="black")
        canvas.itemconfig(word_text, text="Cierra la ventana y abrela denuevo para reiniciar", fill="black",
                          font=FONT_WORD_FINAL)
    else:
        to_learn = pandas.DataFrame(words_dict)
        to_learn.to_csv("data/to_learn.csv", index=False)
        next_card()


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Flash card app")
window.config(pady=50, padx=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, flip_card)

# IMAGES
back_card_img = PhotoImage(file="images/card_back.png")
front_card_img = PhotoImage(file="images/card_front.png")
right_button_img = PhotoImage(file="images/right.png")
wrong_button_img = PhotoImage(file="images/wrong.png")

# CANVAS
canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card = canvas.create_image(400, 263, image=front_card_img)
title_text = canvas.create_text(400, 150, text="", font=FONT_TITLE)
word_text = canvas.create_text(400, 263, text="", font=FONT_WORD)
canvas.grid(column=0, row=0, columnspan=2)

# BUTTONS
right_button = Button(image=right_button_img, highlightthickness=0, command=known_word)
right_button.grid(column=1, row=1)

wrong_button = Button(image=wrong_button_img, highlightthickness=0, command=next_card)
wrong_button.grid(column=0, row=1)

next_card()

window.mainloop()
