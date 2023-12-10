import curses
import time
import random

def main(stdscr):
    # Set up the screen
    curses.curs_set(0)
    stdscr.nodelay(1)
    stdscr.timeout(1000)

    # Initialize the snake
    snake_x = curses.COLS // 2
    snake_y = curses.LINES // 2
    snake = [
        [snake_y, snake_x],
        [snake_y, snake_x - 1],
        [snake_y, snake_x - 2],
        [snake_y, snake_x - 3],
        [snake_y, snake_x - 4]
    ]

    # Initialize the food
    food = [random.randint(2, curses.LINES - 3), random.randint(2, curses.COLS - 3)]

    # initialize direction:
    direction = curses.KEY_RIGHT

    # Initialize color pairs for Effects
    curses.start_color()
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(6, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(7, curses.COLOR_WHITE, curses.COLOR_BLACK)

    # Intro screen
    for i in range(1, 30):
        stdscr.addstr(curses.LINES // 2, curses.COLS // 2 - 10, "Snake In The Terminal", curses.color_pair(i % 7 +1) | curses.A_BLINK)
        stdscr.refresh()
        time.sleep(0.1)

    # Game loop
    while True:

        # set the speed
        stdscr.timeout(1000 // (len(snake) // 3))

        # Get user input
        key = stdscr.getch()

        # If no key is pressed, continue moving in the current direction
        if key == -1:
            key = direction

        # Quit the game if 'q' is pressed
        if key == ord('q'):
            break

        # Move the snake
        new_head = [snake[0][0], snake[0][1]]
        if key == curses.KEY_UP:
            new_head[0] -= 1
        if key == curses.KEY_DOWN:
            new_head[0] += 1
        if key == curses.KEY_LEFT:
            new_head[1] -= 1
        if key == curses.KEY_RIGHT:
            new_head[1] += 1
        snake.insert(0, new_head)

        # Update the direction
        direction = key

        # Check if the snake has collided with the wall or itself
        if (snake[0][0] in [0, curses.LINES - 1] or
            snake[0][1] in [0, curses.COLS - 1] or
            snake[0] in snake[1:]):
            break

        # Check if the snake has eaten the food
        if snake[0] == food:
            # Generate new food
            food = [random.randint(2, curses.LINES - 3), random.randint(2, curses.COLS - 3)]
            # Grow the snake by 2 '*'
            snake.append(snake[-1][:])
            snake.append(snake[-1][:])

        else:
            # Remove the tail of the snake
            snake.pop()

        # Clear the screen
        stdscr.clear()

        # Draw the snake
        for i, (y, x) in enumerate(snake):
            if i == 0:  # Draw the tongue at the first cell of the snake
                if direction == curses.KEY_RIGHT:
                    stdscr.addch(y, x, '<', curses.color_pair(3))
                elif direction == curses.KEY_LEFT:
                    stdscr.addch(y, x, '>', curses.color_pair(3))
                elif direction == curses.KEY_UP:
                    stdscr.addch(y, x, 'v', curses.color_pair(3))
                elif direction == curses.KEY_DOWN:
                    stdscr.addch(y, x, '^', curses.color_pair(3))
            elif i == 1:  # Draw the head at the second cell of the snake
                stdscr.addch(y, x, 'O', curses.color_pair(3))
            else:
                stdscr.addch(y, x, '*', curses.color_pair(3))  # Draw the rest of the snake

        # # Draw the food
        stdscr.addch(food[0], food[1], '@')

        # Refresh the screen
        stdscr.refresh()

    # End the game
    for i in range(1, 15):
        stdscr.addstr(curses.LINES // 2, curses.COLS // 2 - 5, "Game Over", curses.color_pair(i % 7 + 1) | curses.A_BLINK)
        stdscr.refresh()
        time.sleep(0.1)

# Run the game
curses.wrapper(main)
