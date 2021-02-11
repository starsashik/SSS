import os
import sys

import pygame
import requests


def show_map(ll=None, z=None, map_type='map', add_param=None):
    map_api_server = "http://static-maps.yandex.ru/1.x/"

    # if add_param[0] == 'pt':
    #     map_params['pt'] = add_param[1]
    map_file = 'map.png'
    clock = pygame.time.Clock()

    def filess():
        map_params = {
            # позиционируем карту центром на наш исходный адрес
            "ll": ll,
            "z": z,
            "l": map_type
        }
        map_response = requests.get(map_api_server, params=map_params)

        if not map_response:
            print('Ошибка выполнения запроса:')
            print("Http статус:", map_response.status_code, '(', map_response.reason, ")")
            sys.exit(1)

        try:
            with open(map_file, 'wb') as file:
                file.write(map_response.content)
        except IOError as ex:
            print('Ошибка записи временного файла:', ex)
            sys.exit(2)

    def dvig(direction):
        chislo = list(map(float, ll.split(',')))
        if direction == 'left':
            chislo[0] -= 0.050 / z
        if direction == 'right':
            chislo[0] += 0.050 / z
        if direction == 'up':
            chislo[1] += 0.050 / z
        if direction == 'down':
            chislo[1] -= 0.050 / z
        return f'{chislo[0]},{chislo[1]}'

    pygame.init()
    screen = pygame.display.set_mode((600, 450))
    filess()
    screen.blit(pygame.image.load(map_file), (0, 0))
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                if event.key == pygame.K_PAGEDOWN:
                    if z > 4:
                        z -= 1
                if event.key == pygame.K_PAGEUP:
                    if z < 17:
                        z += 1
                if event.key == pygame.K_LEFT:
                    ll = dvig('left')
                if event.key == pygame.K_RIGHT:
                    ll = dvig('right')
                if event.key == pygame.K_UP:
                    ll = dvig('up')
                if event.key == pygame.K_DOWN:
                    ll = dvig('down')
                filess()
                screen.blit(pygame.image.load(map_file), (0, 0))
        pygame.display.flip()
        clock.tick(30)
    pygame.quit()
    os.remove(map_file)
