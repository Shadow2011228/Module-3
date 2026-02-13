import math
import socket
import time
import pygame
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox
from tkinter.colorchooser import askcolor

pygame.init()

WIDTH = 800
HEIGHT = 600
CC = (WIDTH // 2, HEIGHT // 2)

old = (0, 0)
radius = 50

color = ''
name = ''

def login():
    global name
    name = row.get()
    if name and color:
        root.destroy()
        root.quit()
    else:
        tk.messagebox.showerror("Ошибка", "Ты не выбрал цвет или не ввёл имя!")


root = tk.Tk()
root.title("Логин")
root.geometry("300x200")

style = ttk.Style()
style.theme_use('clam')

name_label = tk.Label(root, text="Введи свой никнейм:")
name_label.pack()

row = tk.Entry(root, width=30, justify="center")
row.pack()

def arc():
    global color
    color_code = askcolor(title="Выбери цвет")
    color = color_code[1]

color_btn = tk.Button(root, text="Выбери цвет:", command=arc)
color_btn.pack()

name_btn = tk.Button(root, text="Зайти в игру", command=login)
name_btn.pack()
root.mainloop()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Настраиваем сокет
sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)  # Отключаем пакетирование
sock.connect(("localhost", 10000))

# Отправляем цвет и имя
sock.send(("color:<" + name + "," + color + ">").encode())

font = pygame.font.SysFont('arial', 15)
text_surface = font.render(name, True, (0, 0, 0))
text_rect = text_surface.get_rect()
text_rect.center = CC

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Бактерии")

def find(vector: str):
    first = None
    for num, sign in enumerate(vector):
        if sign == "<":
            first = num
        if sign == ">" and first is not None:
            second = num
            result = vector[first + 1:second]  # Поменяли
            return result
    return ""

def draw_bacteries(data: list[str]):
    for num, bact in enumerate(data):
        data = bact.split(" ")  # Разбиваем по пробелам подстроку одной бактерии
        x = CC[0] + int(data[0])
        y = CC[1] + int(data[1])
        size = int(data[2])
        color = data[3]
        pygame.draw.circle(screen, color, (x, y), size)

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if pygame.mouse.get_focused():
            pos = pygame.mouse.get_pos()
            vector = pos[0] - CC[0], pos[1] - CC[1]

            lenv = math.sqrt(vector[0] ** 2 + vector[1] ** 2)
            vector = vector[0] / lenv, vector[1] / lenv

            if vector != old:
                old = vector
                msg = f"<{vector[0]},{vector[1]}>"
                sock.send(msg.encode())

    # Получаем
    data = sock.recv(1024).decode()
    print("Получил:", data)
    data = find(data).split(",")  # Разбиваем на шары

    # Рисуем новое поле
    screen.fill('gray')
    pygame.draw.circle(screen, color, CC, radius)
    if data!= ['']:
        draw_bacteries(data)
    screen.blit(text_surface, text_rect)
    pygame.display.update()

    time.sleep(0.01)

pygame.quit()
