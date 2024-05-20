from random import randrange

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

# Серый цвет для класса Game Object
DEFAULT_COLOR = (100, 100, 100)

APPLE_COLOR = (255, 0, 0)

SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 10

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
    """Parent class for all objects"""

    def __init__(self) -> None:
        self.position = SCREEN_CENTER
        self.body_color = DEFAULT_COLOR

    # Если не унаследован

    def draw(self):
        """Parent abstract method for drawing objects on the field"""
        raise NotImplementedError(
            f'Не определён draw() в {self.__class__.__name__}'
        )

    def draw_cell(self, position):
        rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """Child class for apple objects"""

    def __init__(self) -> None:
        self.position = self.randomize_position()
        self.body_color = APPLE_COLOR

    def randomize_position(self) -> tuple[int, int]:
        """Get random position on screen"""
        return (
            randrange(0, SCREEN_WIDTH, GRID_SIZE),
            randrange(0, SCREEN_HEIGHT, GRID_SIZE)
        )

    def draw(self):
        """Draw apple on screen"""
        self.draw_cell(self.position)


class Snake(GameObject):
    """Child class for snake objects"""

    def __init__(self) -> None:
        self.position = SCREEN_CENTER
        self.direction = RIGHT
        self.next_direction = None
        self.positions = [(SCREEN_CENTER)]
        self.length = len(self.positions)
        self.last = None
        self.body_color = SNAKE_COLOR

    def update_direction(self):
        """Updating direction after clicking a button"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    # Отрисовка Ячеек из списка positions
    def draw(self):
        """Draw snake on screen"""
        for position in self.positions[:-1]:
            self.draw_cell(position)

        # Отрисовка головы змейки
        self.draw_cell(self.positions[0])

        # Затирание последнего элемента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    # Метод который возвращает позицию головы змейки
    def get_head_position(self):
        """Get snake head position"""
        return self.positions[0]

    def move(self):
        """Moves snake on screen"""
        # Получаем направление змейки
        direction_x, direction_y = self.direction

        # Перемножаем на размер ячейки
        direction_x *= GRID_SIZE
        direction_y *= GRID_SIZE

        # Прибавляем к позиции головы питона и получаем след. позицию
        next_pos = ((self.positions[0][0] + direction_x) % SCREEN_WIDTH,
                    (self.positions[0][1] + direction_y) % SCREEN_HEIGHT)

        # След позицию добавляем к голове
        self.positions.insert(0, next_pos)

        # Если длинна питона больше 1
        if len(self.positions) > 1:
            # Кладём в переменную last хвост питона
            self.last = self.positions[len(self.positions) - 1]

        # удаление хвоста из списка positions
        self.positions.pop(len(self.positions) - 1)

    # метод очищения экрана и обнуления позиций
    def reset(self):
        """Restores all values to default state"""
        self.positions = [SCREEN_CENTER]
        self.direction = RIGHT
        self.next_direction = None
        self.length = len(self.positions)
        self.last = None


# Обработка нажатия
def handle_keys(game_object):
    """Keypress event handler"""
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
    """Main"""
    # Инициализация PyGame:
    pygame.init()

    # Создание объектов и отрисовка перед игрой
    snake = Snake()
    apple = Apple()
    apple.randomize_position()
    apple.draw()
    running = True

    while running:
        pygame.display.update()

        # Если длинна змейки больше 3х
        if len(snake.positions) > 3:
            snake_body = snake.positions[1:]
            snake_head = snake.get_head_position()

            # Проходимся и смотрим не совпадает ли позиция головы с телом
            if snake_head in snake_body:

                # Если совпадает обнуляем все и запускаем заново
                snake.reset()
                screen.fill(BOARD_BACKGROUND_COLOR)
                apple.position = apple.randomize_position()
                apple.draw()

        # Если съели яблоко добавляем элемент в список и отрсиосвываем заново
        if snake.get_head_position() == apple.position:
            snake.positions.insert(len(snake.positions), apple.position)
            apple.position = apple.randomize_position()
            apple.draw()

        # Основные механики
        snake.draw()
        snake.move()
        snake.update_direction()
        handle_keys(snake)
        clock.tick(SPEED)


if __name__ == '__main__':
    main()
