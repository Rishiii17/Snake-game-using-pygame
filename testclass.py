import pytest
from cobra_wars import Game, Snake, HealthPotion, SCREEN_WIDTH, SCREEN_HEIGHT, SNAKE_UNIT_SIZE

# Set up a fixture for the game environment
@pytest.fixture
def game():
    """
    Fixture to create and initialize a game instance.
        Game: An instance of the Game class with the initial state set up.
    :return:
        Game: An instance of the Game class with the initial state set up.
    """
    game_instance = Game()
    game_instance.running = True
    game_instance.playing = True
    return game_instance

# Test snake movement
def test_snake_movement(game):
    """
    Test that the snake moves correctly in the specified direction.

    :return:
    1. Set the initial position of the snake.
    2. Update the snake's direction and call the position update.
    3. Assert that the snake's new position matches the expected position.

    """
    initial_position = game.player1.body[0].copy()
    game.player1.direction = {'x': 1, 'y': 0}  # Ensure the direction is right
    game.player1.update_position()
    expected_position = (initial_position['x'] + 1) % (SCREEN_WIDTH // SNAKE_UNIT_SIZE)
    assert game.player1.body[0]['x'] == expected_position

# Test collision with food
def test_collision_with_food(game):
    """
    Test that the player's score increases when the snake collides with food.

    :return:
    1. Place food at the snake's current position.
    2. Call the game's update method.
    3. Assert that the score has increased by the expected value.

    """
    initial_score = game.player1.score
    game.food = game.player1.body[0]  # Place food at snake's current position
    game.update_game()
    assert game.player1.score == initial_score + 5  # Assumes food is worth 5 points
