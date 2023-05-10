import pygame
import pytmx
import csv
from pygame import transform
from pygame.image import load
from playerLoader import PlayerSelector

# Initialize Pygame
pygame.init()

# Set up the screen
screen_width = 1500
screen_height = 900
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Illinois Jackson and the Shrine of Impending Dread!")

# Load the map image
map_image = pygame.image.load("Platformer assets pack\Level_1.png").convert_alpha()

# Load the collision data from the CSV file
collision_data = []
with open("Platformer assets pack\Level_1.csv", "r") as file:
    reader = csv.reader(file)
    for row in reader:
        collision_data.append([int(cell) for cell in row])

# Load the Tiled map
tmx_data = pytmx.TiledMap("Platformer assets pack\Level_1.tmx")

# Get the collision layer from the Tiled map
collision_layer = tmx_data.get_layer_by_name("Tile Layer 1")

# Set up the camera
camera = pygame.Rect(0, 0, screen_width, screen_height)

###################################################################################################
"""
 ██╗██╗     ██╗     ██╗███╗   ██╗ ██████╗ ██╗███████╗       
 ██║██║     ██║     ██║████╗  ██║██╔═══██╗██║██╔════╝       
 ██║██║     ██║     ██║██╔██╗ ██║██║   ██║██║███████╗       
 ██║██║     ██║     ██║██║╚██╗██║██║   ██║██║╚════██║       
 ██║███████╗███████╗██║██║ ╚████║╚██████╔╝██║███████║       
 ╚═╝╚══════╝╚══════╝╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚═╝╚══════╝       
                                                            
      ██╗ █████╗  ██████╗██╗  ██╗███████╗ ██████╗ ███╗   ██╗
      ██║██╔══██╗██╔════╝██║ ██╔╝██╔════╝██╔═══██╗████╗  ██║
      ██║███████║██║     █████╔╝ ███████╗██║   ██║██╔██╗ ██║
 ██   ██║██╔══██║██║     ██╔═██╗ ╚════██║██║   ██║██║╚██╗██║
 ╚█████╔╝██║  ██║╚██████╗██║  ██╗███████║╚██████╔╝██║ ╚████║
  ╚════╝ ╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═╝  ╚═══╝
                                                            
"""
class IllinoisJackson(pygame.sprite.Sprite):
    def __init__(self, location, smsc_dimensions, inverted=False):

        self.Player = ""
        self.SpriteObject = ""
        temp = PlayerSelector()
        self.Player = temp.player
        self.smsc = smsc_dimensions
        self.player_x = location[0]
        self.player_y = location[1]

        self.idleFrame = 0
        self.idleFrames = self.Player["Action"]["Idle"]["frameCount"]
        self.idleImageLink = self.Player["Action"]["Idle"]["imagePath"] + f"\{self.idleFrame}.png"

        self.SpriteObject = self.load_sprite()

        self.rect = self.SpriteObject.get_rect()


    def load_sprite(self,with_alpha=True):
        loaded_sprite = load(self.idleImageLink)
        loaded_sprite = transform.smoothscale(loaded_sprite, self.smsc)

        if with_alpha:
            return loaded_sprite.convert_alpha()
        else:
            return loaded_sprite.convert()
    
    def updateFrames(self):
        if self.idleFrame < self.idleFrames - 1:
            self.idleFrame += 1
        else:
            self.idleFrame = 0

        self.idleImageLink = self.Player["Action"]["Idle"]["imagePath"] + f"\{self.idleFrame}.png"

        self.SpriteObject = self.load_sprite()

    def movePlayer(self, x=0, y=0):
        self.player_x += x
        self.player_y += y


    def drawPlayer(self, surface):
        blit_position = (self.player_x, self.player_y)
        surface.blit(self.SpriteObject, blit_position)

    def update(self):
        # Handle movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.player_x -= 5
        elif keys[pygame.K_RIGHT]:
            self.player_x += 5
        elif keys[pygame.K_UP]:
            self.player_y -= 5
        elif keys[pygame.K_DOWN]:
            self.player_y += 5

        # Check for collisions with the collision layer
        for x, y, gid in collision_layer:
            if gid:
                tile_rect = pygame.Rect(x * tmx_data.tilewidth, y * tmx_data.tileheight, tmx_data.tilewidth, tmx_data.tileheight)
                if self.rect.colliderect(tile_rect):
                    self.player_y += 1

# Create the player sprite and add it to a sprite group
player = IllinoisJackson((175, screen_height - 300), (90,90))

# Game loop
clock = pygame.time.Clock()
while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    # Draw the map and the player sprite to the screen
    map_rect = map_image.get_rect()
    screen.blit(map_image, (0, 0), camera)

    player.drawPlayer(screen)
    player.update()

    # Update the display
    pygame.display.update()

    # Cap the frame rate
    clock.tick(60)
