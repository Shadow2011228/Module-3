import math
import socket, time
import pygame
import pyautogui

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Настраиваем сокет
sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)  # Отключаем пакетирование
sock.connect(("localhost", 10000))

pygame.init()

WIDTH = 800
HEIGHT = 600
CC = (WIDTH//2,HEIGHT//2)

old = (0,0)
radius = 50

text = pyautogui.prompt(text='Выберете цвет для бактерии', title='Поле ввода')
text2 = pyautogui.prompt(text='Выберете имя для бактерии', title='Поле ввода')

font = pygame.font.SysFont('arial', 15)
text_surface = font.render(text2, True, (0, 0, 0))
text_rect = text_surface.get_rect()
text_rect.center = CC

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Бактерии")

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

    # Рисуем новое поле
    screen.fill('gray')
    pygame.draw.circle(screen, text, CC, radius)
    screen.blit(text_surface, text_rect)
    pygame.display.update()

    time.sleep(0.01)

pygame.quit()
