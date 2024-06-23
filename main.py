import pygame
import random
import time

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption("Дави клеща!")
icon = pygame.image.load('image/logomain.png')
pygame.display.set_icon(icon)

target_img = pygame.image.load('image/acarus.png')
hit_img = pygame.image.load('image/hit.png')
target_width = 80
target_height = 80

color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

# Счетчик попаданий
hit_count = 0
font = pygame.font.Font(None, 36)

# Список целей
targets = []
for _ in range(5):
    target_x = random.randint(0, SCREEN_WIDTH - target_width)
    target_y = random.randint(0, SCREEN_HEIGHT - target_height)
    direction_x = random.choice([-1, 1])
    direction_y = random.choice([-1, 1])
    targets.append([target_x, target_y, direction_x, direction_y, target_img, 0, False])  # 0 - время с момента замены, False - попадание

def move_targets():
    for i, target in enumerate(targets):
        if not target[6]:  # Двигаем только, если нет попадания
            target[0] += target[2] * 10 / 60  # 10 пикселей в секунду, делим на 60 для частоты кадров
            target[1] += target[3] * 10 / 60

            # Проверка на столкновение с границами экрана
            if target[0] < 0 or target[0] > SCREEN_WIDTH - target_width:
                target[2] *= -1
            if target[1] < 0 or target[1] > SCREEN_HEIGHT - target_height:
                target[3] *= -1

            # Проверка на столкновение с другими целями
            for j, other in enumerate(targets):
                if i != j and not other[6]:
                    if (target[0] < other[0] + target_width and target[0] + target_width > other[0] and
                        target[1] < other[1] + target_height and target[1] + target_height > other[1]):
                        target[2] *= -1
                        target[3] *= -1
                        other[2] *= -1
                        other[3] *= -1

running = True
clock = pygame.time.Clock()

while running:
    screen.fill(color)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            for target in targets:
                if target[0] < mouse_x < target[0] + target_width and target[1] < mouse_y < target[1] + target_height:
                    target[4] = hit_img  # Замена изображения
                    target[5] = time.time()  # Время замены
                    target[6] = True  # Устанавливаем флаг попадания
                    hit_count += 1

    # Обновляем изображения и проверяем время для замены
    current_time = time.time()
    for target in targets:
        if target[6] and current_time - target[5] >= 2:  # Если прошло 2 секунды после попадания
            target[0] = random.randint(0, SCREEN_WIDTH - target_width)
            target[1] = random.randint(0, SCREEN_HEIGHT - target_height)
            target[2] = random.choice([-1, 1])
            target[3] = random.choice([-1, 1])
            target[4] = target_img  # Возвращаем исходное изображение
            target[5] = 0  # Сбрасываем время замены
            target[6] = False  # Сбрасываем флаг попадания

    # Перемещаем цели
    move_targets()

    # Рисуем цели
    for target in targets:
        if not target[6] or (target[6] and current_time - target[5] < 2):  # Рисуем только, если цель не попала или прошло меньше 2 секунд после попадания
            screen.blit(target[4], (target[0], target[1]))

    # Рисуем счетчик попаданий
    hit_text = font.render(f'Раздавлено: {hit_count}', True, (255, 255, 255))
    screen.blit(hit_text, (SCREEN_WIDTH - 200, 10))

    pygame.display.update()
    clock.tick(60)  # Ограничиваем до 60 кадров в секунду

pygame.quit()