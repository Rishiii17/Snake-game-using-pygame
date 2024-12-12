#Author's name :- Rishi Patel
#Description :- The program defines the class 'Game' which has different functions to run the game


class Game:
    """
    Main class to handle the Snake game.
    """
    def __init__(self):
        """
        Initializes the game, setting up the Pygame environment and assets.
        """
        pygame.init()
        self.display_window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Cobra Wars")
        self.clock = pygame.time.Clock()
        self.is_running = True
        self.is_playing = False
        self.is_paused = False
        self.is_game_over = False
        self.are_scores_calculated = False  # New flag to check if scores have been calculated
        self.player1 = Snake({'x': 5, 'y': SCREEN_HEIGHT // SNAKE_UNIT_SIZE // 2}, MOVE_RIGHT, COLOR_GOLD_YELLOW)
        self.player2 = Snake({'x': SCREEN_WIDTH // SNAKE_UNIT_SIZE - 5, 'y': SCREEN_HEIGHT // SNAKE_UNIT_SIZE // 2}, MOVE_LEFT,
                             COLOR_RED_ORANGE)
        self.health_potions_list = []
        self.last_potion_spawn_time = time.time()
        self.food = self.create_food()
        self.ui_buttons = {}
        self.rat_sprite = pygame.image.load('rat_image.jpg')
        self.rat_sprite = pygame.transform.scale(self.rat_sprite, (SNAKE_UNIT_SIZE, SNAKE_UNIT_SIZE))
        self.game_logo_image = pygame.image.load('cobra_wars_image.png')  # Load the game logo image
        self.game_logo_image = pygame.transform.scale(self.game_logo_image, (600, 150))  # Optionally scale the image
        self.round_count = 0
        self.current_round_num = 1
        self.is_input_active = False
        self.input_text = ''
        self.round_scores = {"Player 1": [], "Player 2": []}

    def create_food(self):
        """
        Generates food at a random position
        :return:
        tuple: A random (x, y) position
        """
        return {
            'x': randint(0, SCREEN_WIDTH // SNAKE_UNIT_SIZE - 1),
            'y': randint(0, SCREEN_HEIGHT // SNAKE_UNIT_SIZE - 1),
        }

    def draw_snake(self, snake):
        """
        Draws the snake body
        :param snake: Size, Position, Color
        :return: random(x, y) position, size, color
        """
        for coord in snake.body_parts:
            x = coord['x'] * SNAKE_UNIT_SIZE
            y = coord['y'] * SNAKE_UNIT_SIZE
            pygame.draw.rect(self.display_window, snake.snake_color,
                             pygame.Rect(x, y, SNAKE_UNIT_SIZE, SNAKE_UNIT_SIZE))

    def draw_health_bar(self, x, y, health, max_health):
        if health > 0:
            inner_width = (health / max_health) * 100
            inner_rect = pygame.Rect(x, y, inner_width, 10)
            pygame.draw.rect(self.display_window, COLOR_LIME_GREEN, inner_rect)
            pygame.draw.rect(self.display_window, COLOR_GOLD_BORDER, (x, y, 100, 10), 2)

    def spawn_health_potions(self):
        """
        Updates the health potion
        :return: increase or decrease in health potion of snake
        """
        current_time = time.time()
        if current_time - self.last_potion_spawn_time >= POTION_APPEAR_INTERVAL:
            self.health_potions_list.append(HealthPotion())
            self.last_potion_spawn_time = current_time

    def handle_events(self):
        """
        Handles the input and output of the game
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.is_input_active:
                    if self.ui_buttons.get('enter') and self.ui_buttons['enter'].collidepoint(event.pos):
                        print("Enter button clicked")  # Debug statement
                        try:
                            self.round_count = int(self.input_text)  # Parse the number of rounds from input
                            print(f"Number of rounds set to: {self.round_count}")  # Debug statement
                            self.input_text = ''  # Clear the input text
                            self.is_input_active = False  # Deactivate text input mode
                            self.is_playing = True  # Start the game
                            print("Game set to start")  # Debug statement
                        except ValueError:
                            self.input_text = ''  # Clear input if it's invalid
                            print("Invalid input for rounds")  # Debug statement
                elif self.ui_buttons.get('start') and self.ui_buttons['start'].collidepoint(event.pos):
                    self.is_input_active = True  # Activate text input mode
                    self.is_playing = False  # Ensure playing is False while input is active

                elif self.is_game_over:
                    if self.ui_buttons.get('restart') and self.ui_buttons['restart'].collidepoint(event.pos):
                        self.reset_game()
                    elif self.ui_buttons.get('quit') and self.ui_buttons['quit'].collidepoint(event.pos):
                        self.is_running = False
                else:
                    if not self.is_playing and not self.is_input_active:
                        if self.ui_buttons.get('start') and self.ui_buttons['start'].collidepoint(event.pos):
                            self.is_input_active = True  # Set input active to true to start input for number of rounds
                        elif self.ui_buttons.get('quit') and self.ui_buttons['quit'].collidepoint(event.pos):
                            self.is_running = False  # Quit the game from main menu

            elif event.type == pygame.KEYDOWN:
                if self.is_input_active:
                    if event.key == pygame.K_BACKSPACE:
                        self.input_text = self.input_text[:-1]
                    elif event.unicode.isdigit():  # Ensure only numeric input is added
                        self.input_text += event.unicode
                elif self.is_playing and not self.is_paused:
                    # Player 1 Controls
                    if event.key == pygame.K_w and self.player1.move_direction != MOVE_DOWN:
                        self.player1.move_direction = MOVE_UP
                    elif event.key == pygame.K_a and self.player1.move_direction != MOVE_RIGHT:
                        self.player1.move_direction = MOVE_LEFT
                    elif event.key == pygame.K_s and self.player1.move_direction != MOVE_UP:
                        self.player1.move_direction = MOVE_DOWN
                    elif event.key == pygame.K_d and self.player1.move_direction != MOVE_LEFT:
                        self.player1.move_direction = MOVE_RIGHT
                    # Player 2 Controls
                    if event.key == pygame.K_UP and self.player2.move_direction != MOVE_DOWN:
                        self.player2.move_direction = MOVE_UP
                    elif event.key == pygame.K_LEFT and self.player2.move_direction != MOVE_RIGHT:
                        self.player2.move_direction = MOVE_LEFT
                    elif event.key == pygame.K_DOWN and self.player2.move_direction != MOVE_UP:
                        self.player2.move_direction = MOVE_DOWN
                    elif event.key == pygame.K_RIGHT and self.player2.move_direction != MOVE_LEFT:
                        self.player2.move_direction = MOVE_RIGHT
    