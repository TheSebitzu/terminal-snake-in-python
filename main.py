import random

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


def main():
    # Get height
    while True:
        try:
            height = int(input("Height: "))
            break
        except ValueError:
            pass

    # Get width
    while True:
        try:
            width = int(input("Width: "))
            break
        except ValueError:
            pass

    # Game loop
    Game(height, width).play()


class Game:
    def __init__(self, height, width):
        self.height = height
        self.width = width
        # Default snake
        self.snake = Snake([(0, 0)], UP)
        # Generate first apple
        self.regen_apple()

    def render(self):
        # Get board
        matrix = self.board_matrix()

        # Upper border
        print("+" + "-" * self.width + "+")

        # Render line
        for y in range(0, self.height):
            # Left border
            line = "|"
            # Content
            for x in range(0, self.width):
                line += matrix[x][y]
            # Right border
            line += "|"

            print(line)

        # Lower border
        print("+" + "-" * self.width + "+")

    def board_matrix(self):
        # Empty board
        matrix = [[" " for _ in range(self.height)] for _ in range(self.width)]

        # Snake body
        for part in self.snake.body:
            matrix[part[0]][part[1]] = "0"

        # Modify head to "X"
        head = self.snake.head
        matrix[head[0]][head[1]] = "X"

        # Apple
        apple_loc = self.apple.location
        matrix[apple_loc[0]][apple_loc[1]] = "*"

        return matrix

    def next_position(self, position, direction):
        # Get next position (also wrap snake)
        return (
            (position[0] + direction[0]) % self.width,
            (position[1] + direction[1]) % self.height,
        )

    def regen_apple(self):
        # Find location
        while True:
            new_loc = (
                random.randint(0, self.width - 1),
                random.randint(0, self.height - 1),
            )

            # Until apple loc isnt snake
            if new_loc not in self.snake.body:
                break

        # New apple at location
        self.apple = Apple(new_loc)

    def play(self):
        score = 0

        # Main loop
        while True:
            # Render
            self.render()

            # Get direction
            direction = input()
            match direction:
                case "w":
                    if self.snake.direction != DOWN:
                        self.snake.set_direction(UP)
                case "a":
                    if self.snake.direction != RIGHT:
                        self.snake.set_direction(LEFT)
                case "s":
                    if self.snake.direction != UP:
                        self.snake.set_direction(DOWN)
                case "d":
                    if self.snake.direction != LEFT:
                        self.snake.set_direction(RIGHT)
                # Exit with q
                case "q":
                    print(f"Your score: {score}")
                    break
                # Most probable is a plain ENTER (the snake still moves one position)
                case _:
                    pass

            # Get position
            next_pos = self.next_position(self.snake.head, self.snake.direction)

            # It snake hits itself, its game over
            if next_pos in self.snake.body:
                print(f"Your score: {score}")
                break

            # If snake eats apple, it grows
            if next_pos == self.apple.location:
                score += 1
                self.snake.extend_body(next_pos)
                self.regen_apple()
            else:
                self.snake.take_step(next_pos)


class Snake:
    def __init__(self, body, direction):
        self.body = body
        self.direction = direction

    def take_step(self, position):
        # In the snake's body list, remove the first touple (the tail) and move the head towards next pos
        self.body = self.body[1:] + [position]

    def set_direction(self, direction):
        self.direction = direction

    # Snake's head
    @property
    def head(self):
        return self.body[-1]

    def extend_body(self, pos):
        # Grow at the head
        self.body.append(pos)


class Apple:
    def __init__(self, location):
        self.location = location


if __name__ == "__main__":
    main()
