import turtle
import random
import tkinter as tk
from tkinter import messagebox

# Tkinter arayüzü kapalı
root = tk.Tk()
root.withdraw()

# Kelime listesi
WORDS = ["apple", "bread" ,"fruit","ocean","water","zebra","table","green","white","black","pasta","light","paper"
         "happy","funny","dance","glass","stone","chair","world","earth","color","ready"]
secret_word = random.choice(WORDS).lower()

# Renkler
GREEN = "#2ECC71"
YELLOW = "#F1C40F"
GRAY = "#BDC3C7"
DARK_GRAY = "#95A5A6"
BLACK = "#2C3E50"
RED = "#E74C3C"
WHITE = "#FFFFFF"

# Oyun durumu
guesses = [[""] * 5 for _ in range(6)]
colors_grid = [[GRAY] * 5 for _ in range(6)]
current_row = 0
current_col = 0
BOX_SIZE = 60
START_X = -150
START_Y = 180

# Turtle ekranı
screen = turtle.Screen()
screen.setup(width=600, height=700)
screen.bgcolor("#000000")
screen.title("WordSquare")
screen.tracer(0)

pen = turtle.Turtle()
pen.penup()
pen.hideturtle()

def draw_box(x, y, color, letter=""):
    pen.goto(x, y)
    pen.fillcolor(color)
    pen.begin_fill()
    for _ in range(6):
        pen.forward(BOX_SIZE / 1.75)
        pen.right(60)
    pen.end_fill()

    if letter:
        pen.goto(x + BOX_SIZE / 3.5, y - BOX_SIZE * 0.85)
        pen.color(BLACK)
        pen.write(letter.upper(), align="center", font=("Arial", 28, "bold"))

def draw_grid():
    for row in range(6):
        for col in range(5):
            x = START_X + col * (BOX_SIZE + 10)
            y = START_Y - row * (BOX_SIZE + 10)
            draw_box(x, y, colors_grid[row][col], guesses[row][col])

def draw_title():
    pen.goto(8, 250)
    pen.color(WHITE)
    pen.write("WordHEX", align="center", font=("Arial", 32, "bold"))

def update_screen():
    screen.tracer(0)
    pen.clear()
    draw_title()
    draw_grid()
    screen.update()

def color_result(row):
    word = "".join(guesses[row])
    temp = list(secret_word)
    result_colors = [GRAY] * 5

    for i in range(5):
        if word[i] == secret_word[i]:
            result_colors[i] = GREEN
            temp[i] = None

    for i in range(5):
        if result_colors[i] != GREEN and word[i] in temp:
            result_colors[i] = YELLOW
            temp[temp.index(word[i])] = None

    colors_grid[row] = result_colors
    update_screen()

def restart_game():
    global secret_word, guesses, colors_grid, current_row, current_col
    secret_word = random.choice(WORDS).lower()
    guesses = [[""] * 5 for _ in range(6)]
    colors_grid = [[GRAY] * 5 for _ in range(6)]
    current_row = 0
    current_col = 0
    update_screen()
    setup_key_listeners()

def handle_restart(key):
    if key.lower() == "e":
        messagebox.showinfo("Yeniden Başlat", "Yeni oyun başlatılıyor!")
        restart_game()
    elif key.lower() == "h":
        messagebox.showinfo("Çıkış", "Görüşmek üzere!")
        screen.bye()

def show_game_over(success):
    if success:
        pen.goto(15, 300)
        pen.color(GREEN)
        pen.write("Tebrikler! 🎉", align="center", font=("Arial", 26, "bold"))
    else:
        pen.goto(10, 300)
        pen.color(RED)
        pen.write(f"Başarısız! Kelime: {secret_word.upper()}", align="center", font=("Arial", 18, "bold"))

    pen.goto(10, -280)
    pen.color(WHITE)
    pen.write("Tekrar oynamak için [E] | Çıkmak için [H]", align="center", font=("Arial", 14, "normal"))

    screen.onkey(lambda: handle_restart("e"), "e")
    screen.onkey(lambda: handle_restart("h"), "h")
    screen.listen()

def on_keypress(char):
    global current_col
    char = char.lower()
    if current_col < 5:
        guesses[current_row][current_col] = char
        current_col += 1
        update_screen()
    screen.listen()

def on_backspace():
    global current_col
    if current_col > 0:
        current_col -= 1
        guesses[current_row][current_col] = ""
        update_screen()
    screen.listen()

def on_enter():
    global current_row, current_col
    word = "".join(guesses[current_row])
    if len(word) != 5:
        messagebox.showwarning("Hatalı Giriş", "Lütfen 5 harfli bir kelime girin!")
        screen.listen()
        return

    color_result(current_row)

    if word == secret_word:
        show_game_over(True)
        return

    current_row += 1
    current_col = 0

    if current_row >= 6:
        show_game_over(False)

    screen.listen()

def clear_key_bindings():
    for ch in "abcdefghijklmnopqrstuvwxyz":
        screen.onkey(None, ch)
        screen.onkey(None, ch.upper())
    screen.onkey(None, "BackSpace")
    screen.onkey(None, "Return")
    screen.onkey(None, "e")
    screen.onkey(None, "h")

def setup_key_listeners():
    clear_key_bindings()
    for ch in "abcdefghijklmnopqrstuvwxyz":
        screen.onkey(lambda c=ch: on_keypress(c), ch)
        screen.onkey(lambda c=ch: on_keypress(c.upper()), ch.upper())
    screen.onkey(on_backspace, "BackSpace")
    screen.onkey(on_enter, "Return")
    screen.listen()

# Tuş dinleyicileri
for ch in "abcdefghijklmnopqrstuvwxyz":
    screen.onkey(lambda c=ch: on_keypress(c), ch)
    screen.onkey(lambda c=ch: on_keypress(c.upper()), ch.upper())

screen.onkey(on_backspace, "BackSpace")
screen.onkey(on_enter, "Return")  # SADECE Return

# Başlat
update_screen()
screen.listen()
screen.mainloop()
