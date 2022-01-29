from tkinter import messagebox
from tkinter import *
from random import choice
import pandas

LANG_01 = "english"
LANG_02 = "german"
FONT_LANG = ("Arial", 40, "italic")
FONT_TITLE = ("Arial", 26, "italic", "bold")
FONT_COUNTER = ("Arial", 20, "normal")
FONT_WORD = ("Arial", 60, "bold")
FONT_END = ("Arial", 24, "bold")

modus = 0
counter = 8
timer = ""
word_front = ""
word_back = ""
word_freq = ""

# --------------------------------- GET DATA ---------------------------------
word_data = pandas.read_csv("data.csv")
db = {index: [row.english, row.german, row.freq] for (index, row) in word_data.iterrows()}
card_num = len(db)
card_num_start = len(db)
db_index = None


# --------------------------------- START ---------------------------------
def start():
    global modus
    start_option = messagebox.askquestion("Lernmodus auswählen", "Zeit Modus:\n"
                                                                 "Karte wird nach 5. Sekunden "
                                                                 "automatisch aufgedeckt.\n\n"
                                                                 "Manuteller Modus:\n"
                                                                 "Karten werden manuell aufgedeckt.\n\n"
                                                                 "Willst du den Zeitmodus nutzen?")

    if start_option != "yes":
        button_turn.config(image=button_turn_img, command=flip)
        modus = 1

    new_card()


# --------------------------------- GET DATA ---------------------------------
def new_card():
    global word_front, word_back, word_freq, db_index
    try:
        db_index = choice(list(db))
    except IndexError:
        label_card_num.config(text=f"Karten: 0/{card_num_start}")
        end()
    else:
        word_front = db[db_index][0]
        word_back = db[db_index][1]
        word_freq = db[db_index][2]

        label_card_num.config(text=f"Karten: {card_num}/{card_num_start}")
        canvas.itemconfig(card_title, text=LANG_01, font=FONT_LANG)
        canvas.itemconfig(card_word, text=word_front, font=FONT_WORD)
        canvas.itemconfig(card_img, image=front_img)

        if modus == 0:
            count_down(counter)


# --------------------------------- FLIP ---------------------------------
def count_down(counter_time):
    global timer
    canvas.itemconfig(card_counter, text=f"({counter_time})")
    if counter_time > 0:
        timer = window.after(1000, count_down, counter_time - 1)
    else:
        flip()


# --------------------------------- FLIP ---------------------------------
def flip():
    canvas.itemconfig(card_counter, text=f"")
    canvas.itemconfig(card_title, text=LANG_02, font=FONT_LANG)
    canvas.itemconfig(card_word, text=word_back, font=FONT_WORD)
    canvas.itemconfig(card_img, image=back_img)


# --------------------------------- BU UNKNOWN ---------------------------------
def unknown():
    # TODO: Learning list
    if modus == 0:
        window.after_cancel(timer)
    new_card()


# --------------------------------- BU UNKNOWN ---------------------------------
def known():
    global card_num, db
    del db[db_index]
    card_num = len(db)
    if modus == 0:
        window.after_cancel(timer)
    new_card()

# --------------------------------- SAVE ---------------------------------
# TODO: optional save and resume option


# --------------------------------- END ---------------------------------
def end():
    if modus == 0:
        window.after_cancel(timer)
    messagebox.showinfo("Lernzyklus beendet", "Du hast alle 500 Karten abgeschlossen.\n\nGut gemacht! ✔")
    exit()


# --------------------------------- GUI ---------------------------------
window = Tk()
window.title("Jörg - English 'Flash-Cards'")
window.config(padx=50, pady=25, background="#B1DDC6")

# Canvas
canvas = Canvas(width=800, height=526, highlightthickness=0, background="#B1DDC6")
front_img = PhotoImage(file="./images/card_front.png")
back_img = PhotoImage(file="./images/card_back.png")
card_img = canvas.create_image(400, 263, image=front_img)

card_title = canvas.create_text(400, 150, text=LANG_01, font=FONT_LANG)
card_word = canvas.create_text(400, 263, text=word_front, font=FONT_WORD)
card_counter = canvas.create_text(700, 50, font=FONT_COUNTER)
canvas.grid(row=1, column=0, columnspan=3, pady=25)

# Label
label_timer = Label(text="English 'Flash-Cards'", font=FONT_TITLE, bg="#B1DDC6", fg="#728d7f")
label_timer.grid(row=0, column=0, sticky="nw")

label_card_num = Label(text=f"Karten: {card_num}/{card_num_start}", padx=50, font=FONT_TITLE, bg="#B1DDC6",
                       fg="#728d7f")
label_card_num.grid(row=0, column=2, sticky="ne")

# Buttons
button_unknown_img = PhotoImage(file="./images/wrong.png")
button_unknown = Button(image=button_unknown_img, borderwidth=0, highlightthickness=0, command=unknown)
button_unknown.grid(row=2, column=0)

button_known_img = PhotoImage(file="./images/right.png")
button_known = Button(image=button_known_img, borderwidth=0, highlightthickness=0, command=known)
button_known.grid(row=2, column=2)

button_turn_img = PhotoImage(file="./images/turn.png")
button_turn = Button(borderwidth=0, highlightthickness=0, bg="#B1DDC6", activebackground="#B1DDC6", command=flip)
button_turn.grid(row=2, column=1, sticky="w")

start()

window.mainloop()
