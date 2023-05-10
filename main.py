"""
    Author:   Byron Dowling, Deangelo Brown, Izzy Olaemimimo
    Class:    5443 2D Python Gaming

    Asset Credits:

        Sprite:
            - Author: [Elthen's Pixel Art Shop]
            - https://elthen.itch.io/2d-pixel-art-archaeologist 

        Tileset Art:
            - Author: ["BigBuckBunny"]
            - https://bigbuckbunny.itch.io/platform-assets-pack

"""

import pygame
import pytmx
import sys
from playerLoader import PlayerSelector


###################################################################################################
"""
  ██████╗  █████╗ ███╗   ███╗███████╗        
 ██╔════╝ ██╔══██╗████╗ ████║██╔════╝        
 ██║  ███╗███████║██╔████╔██║█████╗          
 ██║   ██║██╔══██║██║╚██╔╝██║██╔══╝          
 ╚██████╔╝██║  ██║██║ ╚═╝ ██║███████╗        
  ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝        
                                             
 ███████╗██████╗ ██████╗ ██╗████████╗███████╗
 ██╔════╝██╔══██╗██╔══██╗██║╚══██╔══╝██╔════╝
 ███████╗██████╔╝██████╔╝██║   ██║   █████╗  
 ╚════██║██╔═══╝ ██╔══██╗██║   ██║   ██╔══╝  
 ███████║██║     ██║  ██║██║   ██║   ███████╗
 ╚══════╝╚═╝     ╚═╝  ╚═╝╚═╝   ╚═╝   ╚══════╝

"""
class GameSprite(pygame.sprite.Sprite):
    def __init__(self, imgLink, location, smsc_dimensions, inverted=False):
        self.playerMain = pygame.sprite.Sprite()
        self.location = location
        self.playerMain.image = self.__makeImage(imgLink, smsc_dimensions, inverted)
        self.playerMain.rect = self.playerMain.image.get_rect(center = location)
        self.playerMain.mask = pygame.mask.from_surface(self.playerMain.image)

        super().__init__()
        
    def draw(self):
        screen.blit(self.playerMain.image, self.playerMain.rect.topleft)
        
    def move(self, x, y):
        self.rect.x += x
        self.rect.y += y
        
    def changeImage(self, imgLink, smsc_dimensions, inverted=False):
        self.playerMain.image = self.__makeImage(imgLink, smsc_dimensions, inverted)
        
    def __makeImage(self, imgLink, smsc_dimensions, inverted=False):
        if not inverted:
            image = pygame.image.load(imgLink)
            image = pygame.transform.smoothscale(image, smsc_dimensions)

        ## Inverted case where the Sprite is facing left
        else:
            image = pygame.image.load(imgLink)
            image = pygame.transform.smoothscale(image, smsc_dimensions)
            image_Copy = image.copy()
            image = pygame.transform.flip(image_Copy, True, False)
            
        return image

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
class IllinoisJackson(GameSprite):
    def __init__(self, location, smsc_dimensions, inverted=False):

        self.Player = ""
        temp = PlayerSelector()
        self.Player = temp.player
        self.smsc = smsc_dimensions

        self.idleFrame = 0
        self.idleFrames = self.Player["Action"]["Idle"]["frameCount"]
        self.idleImageLink = self.Player["Action"]["Idle"]["imagePath"] + f"\{self.idleFrame}.png"

        super().__init__(self.idleImageLink, location, smsc_dimensions, inverted)

    def updateFrames(self):
        if self.idleFrame < self.idleFrames - 1:
            self.idleFrame += 1
        else:
            self.idleFrame = 0

        self.idleImageLink = self.Player["Action"]["Idle"]["imagePath"] + f"\{self.idleFrame}.png"

        self.changeImage(self.idleImageLink, self.smsc)


###################################################################################################
"""
  ██████╗  █████╗ ███╗   ███╗███████╗                                
 ██╔════╝ ██╔══██╗████╗ ████║██╔════╝                                
 ██║  ███╗███████║██╔████╔██║█████╗                                  
 ██║   ██║██╔══██║██║╚██╔╝██║██╔══╝                                  
 ╚██████╔╝██║  ██║██║ ╚═╝ ██║███████╗                                
  ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝                                
                                                                     
 ██╗   ██╗ █████╗ ██████╗ ██╗ █████╗ ██████╗ ██╗     ███████╗███████╗
 ██║   ██║██╔══██╗██╔══██╗██║██╔══██╗██╔══██╗██║     ██╔════╝██╔════╝
 ██║   ██║███████║██████╔╝██║███████║██████╔╝██║     █████╗  ███████╗
 ╚██╗ ██╔╝██╔══██║██╔══██╗██║██╔══██║██╔══██╗██║     ██╔══╝  ╚════██║
  ╚████╔╝ ██║  ██║██║  ██║██║██║  ██║██████╔╝███████╗███████╗███████║
   ╚═══╝  ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝╚═╝  ╚═╝╚═════╝ ╚══════╝╚══════╝╚══════╝
                                                                     
"""
pygame.init()
tick = 0

# Set the position of the camera
camera_x = 0
camera_y = 460

# Display a portion of the map surface
screen_width = 1000
screen_height = 500
screen = pygame.display.set_mode((screen_width, screen_height))

IJ = IllinoisJackson((camera_x + 300, camera_y - 80), (70,70))

## Set the title of the window
banner = f'Illinois Jackson and the Shrine of Impending Dread'
pygame.display.set_caption(banner)

# Load the TMX file
tmx_data = pytmx.util_pygame.load_pygame("Platformer assets pack\Level_1.tmx")

# Create a Pygame surface with the same dimensions as the map
map_surface = pygame.Surface((tmx_data.width * tmx_data.tilewidth, tmx_data.height * tmx_data.tileheight))

# Iterate over all the layers in the map
for layer in tmx_data.layers:
    # Iterate over all the tiles in the layer
    for x, y, image in layer.tiles():
        # Calculate the position of the tile in pixels
        px = x * tmx_data.tilewidth
        py = y * tmx_data.tileheight
        
        # Blit the tile onto the map surface
        map_surface.blit(image, (px, py))

"""
  ██████╗  █████╗ ███╗   ███╗███████╗    ██╗      ██████╗  ██████╗ ██████╗ 
 ██╔════╝ ██╔══██╗████╗ ████║██╔════╝    ██║     ██╔═══██╗██╔═══██╗██╔══██╗
 ██║  ███╗███████║██╔████╔██║█████╗      ██║     ██║   ██║██║   ██║██████╔╝
 ██║   ██║██╔══██║██║╚██╔╝██║██╔══╝      ██║     ██║   ██║██║   ██║██╔═══╝ 
 ╚██████╔╝██║  ██║██║ ╚═╝ ██║███████╗    ███████╗╚██████╔╝╚██████╔╝██║     
  ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝    ╚══════╝ ╚═════╝  ╚═════╝ ╚═╝     
                                                                           
"""
while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
    # Get the input from the arrow keys
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        camera_x -= 5
    elif keys[pygame.K_RIGHT]:
        camera_x += 5
    if keys[pygame.K_UP]:
        camera_y -= 5
    elif keys[pygame.K_DOWN]:
        camera_y += 5
            
    # Clamp the camera position to the bounds of the map
    camera_x = max(0, min(camera_x, tmx_data.width * tmx_data.tilewidth - screen_width))
    camera_y = max(0, min(camera_y, tmx_data.height * tmx_data.tileheight - screen_height))
    
    # Blit a portion of the map surface onto the screen
    screen.blit(map_surface, (0, 0), pygame.Rect(camera_x, camera_y, screen_width, screen_height))

    IJ.draw()

    if tick % 4 == 0:
        IJ.updateFrames()
    
    tick += 1
    # Update the screen
    pygame.display.flip()
