import socket, time
import pygame

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Настраиваем сокет
sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)  # Отключаем пакетирование
sock.connect(("localhost", 10000))

pygame.init()

WIDTH = 800
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Бактерии")

run = False
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    sock.send("Привет".encode())
    time.sleep(0.01)

pygame.quit()
