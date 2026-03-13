import math
import socket
import time
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox
from tkinter.colorchooser import askcolor
import pygame

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
sock.send(("color:<" + name + "," + color + ">").encode())

pygame.init()

font = pygame.font.SysFont('Arial', 15)
text_surface = font.render(name, True, (0, 0, 0))
text_rect = text_surface.get_rect()
text_rect.center = CC

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
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
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
    data = sock.recv(buffer).decode()
    print("Reciev:", data)
    data = find(data).split(",")  # Разбиваем на шары

    # Рисуем новое поле
    screen.fill('gray')

    if data!= ['']:
        radius = int(data[0])  # Сохраняем размер из сообщения в переменную
        draw_bacteries(data[1:])  # Срезаем размер, чтобы он не попадал в ф-ию

    pygame.draw.circle(screen, color, CC, radius)
    screen.blit(text_surface, text_rect)

    pygame.display.update()

    time.sleep(0.01)

pygame.quit()
