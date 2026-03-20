import math
import socket
import time
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox
from tkinter.colorchooser import askcolor
import pygame
import pyautogui

WIDTH = 800
HEIGHT = 600
CC = (WIDTH // 2, HEIGHT // 2)
FPS = 100

old = (0, 0)
radius = 50
buffer = 1024

color = ''
name = ''

def login():
    global name
    name = row.get()
    if name and color:
        root.destroy()
        root.quit()
    else:
        tk.messagebox.showerror("Error", "No color or name")


root = tk.Tk()
root.title("Login")
root.geometry("300x200")

style = ttk.Style()
style.theme_use('clam')

name_label = tk.Label(root, text="Enter your nickname:")
name_label.pack()

row = tk.Entry(root, width=30, justify="center")
row.pack()

def arc():
    global color
    color_code = askcolor(title="Choose color")
    color = color_code[1]

color_btn = tk.Button(root, text="Choose color:", command=arc)
color_btn.pack()

name_btn = tk.Button(root, text="Enter the game", command=login)
name_btn.pack()
root.mainloop()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Настраиваем сокет
sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)  # Отключаем пакетирование
sock.connect(("localhost", 10000))

# Отправляем цвет и имя
try:
    sock.send(("color:<" + name + "," + color + ">").encode())

except:
    pyautogui.alert(text="Предуприждение!", title="Ошибка", button="OK")

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bacteries")

clock = pygame.time.Clock()

def find(vector: str):
    global buffer
    first = None
    for num, sign in enumerate(vector):
        if sign == "<":
            first = num
        if sign == ">" and first is not None:
            second = num
            result = vector[first + 1:second]  # Поменяли
            return result
    if buffer < 10000000:
        buffer = int(buffer* 1.5)
    return ""

def draw_text(x, y, r, text, color):
    font = pygame.font.Font(None, r)
    text = font.render(text, True, color)
    rect = text.get_rect(center=(x, y))
    screen.blit(text, rect)

def draw_bacteries(data: list[str]):
    for num, bact in enumerate(data):
        data = bact.split(" ")  # Разбиваем по пробелам подстроку одной бактерии
        x = CC[0] + int(data[0])
        y = CC[1] + int(data[1])
        size = int(data[2])
        color = data[3]
        pygame.draw.circle(screen, color, (x, y), size)
        if len(data) > 4:
            draw_text(x, y, size // 2, data[4], "black")

class Grid:
    def __init__(self, screen, color):
        self.screen = screen
        self.x = 0
        self.y = 0
        self.start_size = 200
        self.size = self.start_size
        self.color = color
    def update(self, parameters: list[int]):
        x, y, L = parameters
        self.size = self.start_size // L
        self.x = -self.size + (-x) % self.size
        self.y = -self.size + (-y) % self.size


    def draw(self):
        for i in range(WIDTH // self.size + 2):
            pygame.draw.line(self.screen, self.color,
                             (self.x + i * self.size, 0),  # Координаты начала линии
                             (self.x + i * self.size, HEIGHT),  # Координаты конца линии
                             1)
        for i in range(HEIGHT // self.size + 2):
            pygame.draw.line(self.screen, self.color,
                             (0, self.y + i * self.size),  # Координаты начала линии
                             (WIDTH, self.y + i * self.size),  # Координаты конца линии
                             1)

grid = Grid(screen, "seashell4")

run = True
while run:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            screen.fill((0,0,0))
            font = pygame.font.Font(None, 72)
            text = font.render('Спасибо за игру!', True, (255,255,255))
            text_rect = text.get_rect(center=(400,300))
            screen.blit(text, text_rect)
            pygame.display.flip()
            time.sleep(3)
            run = False

        if pygame.mouse.get_focused():
            pos = pygame.mouse.get_pos()
            vector = pos[0] - CC[0], pos[1] - CC[1]
            lenv = math.sqrt(vector[0] ** 2 + vector[1] ** 2)
            if lenv != 0:
                vector = vector[0] / lenv, vector[1] / lenv

            if vector != old:
                old = vector
                msg = f"<{vector[0]},{vector[1]}>"
                sock.send(msg.encode())

    # Получаем
    try:
        data = sock.recv(buffer).decode()
        print("Reciev:", data)
        data = find(data).split(",")  # Разбиваем на шары
    except:
        pyautogui.alert(text="Предуприждение!", title="Ошибка", button="OK")

    # Рисуем новое поле
    screen.fill('gray')

    if data!= ['']:
        parameters = list(map(int, data[0].split(" ")))
        radius = parameters[0]  # Сохраняем размер из сообщения в переменную
        grid.update(parameters[1:])
        grid.draw()
        draw_bacteries(data[1:])  # Срезаем размер, чтобы он не попадал в ф-ию

    pygame.draw.circle(screen, color, CC, radius)
    draw_text(CC[0], CC[1], radius // 2, name, "black")

    pygame.display.update()

    time.sleep(0.01)

# exit_label = tk.Label(root, text="Спасибо за игру")
# exit_label.pack()
# root.mainloop()
# time.sleep(3)
# root.quit()

pygame.quit()
