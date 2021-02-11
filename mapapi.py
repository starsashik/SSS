import os
import sys

import pygame
import requests


def show_map(ll=None, z=None, map_type='map', add_param=None):
    map_api_server = "http://static-maps.yandex.ru/1.x/"
    map_params = {
        # позиционируем карту центром на наш исходный адрес
        "ll": ll,
        "z": z,
        "l": map_type
    }
    if add_param[0] == 'pt':
        map_params['pt'] = add_param[1]

    map_response = requests.get(map_api_server, params=map_params)

    if not map_response:
        print('Ошибка выполнения запроса:')
        print("Http статус:", map_response.status_code, '(', map_response.reason, ")")
        sys.exit(1)

    map_file = 'map.png'
    try:
        with open(map_file, 'wb') as file:
            file.write(map_response.content)
    except IOError as ex:
        print('Ошибка записи временного файла:', ex)
        sys.exit(2)

    pygame.init()
    screen = pygame.display.set_mode((600, 450))
    screen.blit(pygame.image.load(map_file), (0, 0))
    pygame.display.flip()
    while pygame.event.wait().type != pygame.QUIT:
        pass

    pygame.quit()
    os.remove(map_file)
