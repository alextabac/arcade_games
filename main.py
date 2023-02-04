
import arcade
from util_functions import *
import random


class MyGame(arcade.Window):
    """ Main application class. """

    def __init__(self, width, height, wall, speed):
        super().__init__(width, height)
        self.win_width = width
        self.win_height = height
        self.wall_size = wall
        self.speed = speed
        self.player_list = None
        self.player_sprite = None
        self.zombie_list = None
        self.coin_list = None
        self.wall_list = None
        self.physics_engine = None
        self.score = 0
        arcade.set_background_color(arcade.color.AMAZON)

    def setup(self):
        # Set up your game here
        # Create the sprite lists
        self.player_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        self.zombie_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()

        # Score
        self.score = 0

        # Set up the player
        # Character image from kenney.nl
        self.player_sprite = arcade.Sprite("sprites\\superman-child.png", 0.12)
        self.player_sprite.center_x = 60  # Starting position
        self.player_sprite.center_y = 60
        self.player_list.append(self.player_sprite)

        # Create the zombies
        for i in range(10):
            zombie = arcade.Sprite("sprites\\minecraft-zombie.jpg", 0.1)
            zombie.center_x = self.wall_size*3 + random.randrange(self.win_width - self.wall_size*6)
            zombie.center_y = self.wall_size*3 + random.randrange(self.win_height - self.wall_size*6)
            self.zombie_list.append(zombie)

        # Create the coins
        for i in range(100):
            coin = arcade.Sprite("sprites\\gold-coin.jpg", 0.08)
            coin.center_x = self.wall_size*2 + random.randrange(self.win_width - self.wall_size*4)
            coin.center_y = self.wall_size*2 + random.randrange(self.win_height - self.wall_size*4)
            self.coin_list.append(coin)

        # Create the walls
        for i in range(0, self.win_height, self.wall_size):
            wall = arcade.Sprite("sprites\\brick-wall.png", 1.0)
            wall.width = self.wall_size
            wall.height = self.wall_size
            wall.center_x = int(self.wall_size/2)
            wall.center_y = int(self.wall_size/2) + i
            self.wall_list.append(wall)
            wall = arcade.Sprite("sprites\\brick-wall.png", 1.0)
            wall.width = self.wall_size
            wall.height = self.wall_size
            wall.center_x = self.win_width - int(self.wall_size/2)
            wall.center_y = int(self.wall_size/2) + i
            self.wall_list.append(wall)
        for i in range(0, self.win_width, self.wall_size):
            wall = arcade.Sprite("sprites\\brick-wall.png", 1.0)
            wall.width = self.wall_size
            wall.height = self.wall_size
            wall.center_x = int(self.wall_size/2) + i
            self.wall_list.append(wall)
            wall = arcade.Sprite("sprites\\brick-wall.png", 1.0)
            wall.width = self.wall_size
            wall.height = self.wall_size
            wall.center_x = int(self.wall_size/2) + i
            wall.center_y = self.win_height - int(self.wall_size/2)
            self.wall_list.append(wall)

        self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, self.wall_list)

    def on_draw(self):
        """ Render the screen. """
        arcade.start_render()
        self.zombie_list.draw()
        self.coin_list.draw()
        self.player_list.draw()
        self.wall_list.draw()
        arcade.draw_text("Score: " + str(self.score), 5, 2, arcade.color.WHITE)

    def update(self, delta_time):
        """ All the logic to move, and the game logic goes here. """
        coins_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.coin_list)
        for coin in coins_hit_list:
            coin.kill()
            self.score += 1

        zombies_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.zombie_list)
        for zombie in zombies_hit_list:
            zombie.kill()
            self.score = max(0, self.score - 3)
        self.physics_engine.update()

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """
        if key == arcade.key.UP:
            self.player_sprite.change_y = self.speed
        elif key == arcade.key.DOWN:
            self.player_sprite.change_y = -self.speed
        elif key == arcade.key.LEFT:
            self.player_sprite.change_x = -self.speed
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = self.speed

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """
        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0

def main():
    SCREEN_WIDTH = 1400
    SCREEN_HEIGHT = 700
    WALL_SIZE = 30
    MOVEMENT_SPEED = 5
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, WALL_SIZE, MOVEMENT_SPEED)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    # draw_smiley()
    main()
