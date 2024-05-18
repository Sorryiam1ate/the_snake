from random import choice, randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Дефолтная позиция
DEFAULT_POSITION = (0, 0)

# Позиция по центру экрана
SCREEN_CENTER = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:

    def __init__(self, body_color) -> None:
        self.position = DEFAULT_POSITION
        self.body_color = body_color

    def draw(self):
        raise NotImplementedError(
            f'Не определён draw() в {self.__class__.__name__}'
        )


class Apple(GameObject):

    def __init__(self, body_color) -> None:
        self.position = self.randomize_position()
        self.body_color = body_color
        # super().__init__(body_color)

    def randomize_position(self) -> tuple[int, int]:
        return (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        )

        # return (randint(0, SCREEN_WIDTH - GRID_SIZE, GRID_SIZE))

    def draw(self):
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):

    def __init__(self, positions, body_color) -> None:
        self.direction = RIGHT
        self.next_direction = None
        self.positions = [positions]
        self.length = len(self.positions)
        self.last = None
        super().__init__(body_color)

    # Метод обновления направления после нажатия на кнопку

    def update_direction(self):
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def draw(self):
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        return self.positions[0]

    def move(self):
        direction_x, direction_y = self.direction
        direction_x *= GRID_SIZE
        direction_y *= GRID_SIZE

        next_pos = (self.positions[0][0] + direction_x,
                    self.positions[0][1] + direction_y)
        self.positions.insert(0, next_pos)
        if len(self.positions) > 1:
            self.last = self.positions[len(self.positions) - 1]
        self.positions.pop(len(self.positions) - 1)

        if self.positions[0][0] not in range(0, SCREEN_WIDTH):
            self.positions.insert(
                0, (self.positions[0][0] % SCREEN_WIDTH, self.positions[0][1]))
            self.positions.pop(1)

        if self.positions[0][1] not in range(0, SCREEN_HEIGHT):
            self.positions.insert(
                0, (self.positions[0][0], self.positions[0][1] % SCREEN_HEIGHT))
            self.positions.pop(1)

        #     self.positions.pop(1)

        # if self.positions[0][1] >= SCREEN_HEIGHT:

        #     self.positions.insert(0, (self.positions[0][0], 0))
        #     self.positions.pop(1)

        # elif self.positions[0][1] < 0:

        #     self.positions.insert(
        #         0, (self.positions[0][0], SCREEN_HEIGHT - GRID_SIZE))
        #     self.positions.pop(1)


def handle_keys(game_object):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    # Инициализация PyGame:
    pygame.init()

    # Тут нужно создать экземпляры классов.
    snake = Snake(SCREEN_CENTER, SNAKE_COLOR)

    apple = Apple(APPLE_COLOR)

    apple.randomize_position()

    apple.draw()

    running = True

    while running:

        pygame.display.update()

        snake.draw()

        snake.move()

        snake.update_direction()

        if snake.get_head_position() == apple.position:
            snake.positions.insert(len(snake.positions), apple.position)
            apple.position = apple.randomize_position()
            apple.draw()

        clock.tick(SPEED)

        handle_keys(snake)


if __name__ == '__main__':
    main()
