import pygame
import time


class Player:
    def __init__(self, picture, scene):
        self.lives = 3  # player lives
        self.scene = scene  # scene object
        self.image = picture  # define sprite
        self.left = 0  # left border
        self.right = 0  # right border
        self.x = 0  # define x coordinate
        self.down = 0  # lower border
        self.up = 0   # upper border
        self.y = 0  # define y coordinate
        self.jump_speed = -12.5  # define jump speed
        self.vy = self.jump_speed  # define vertical speed
        self.gravity = 0.5  # define gravity
        self.is_in_jump = 0  # define object state
        self.score = 0  # define user score
        self.bottom = scene.height - 200
        self.digits = None
        self.font = 0
        self.sprites = None
        self.dt = 0
        self.played = False
        pygame.mixer.init()
        self.sound = pygame.mixer.Sound('sounds/jump.wav')
        self.lives = 3
	self.negativeFontOffsetRelativeToAsciiCodes = 32

    def move(self, vy=0):
        self.down += vy
        self.up += vy
        self.y = 0.5 * (self.up + self.down)
        self.vy += vy
        self.place_to(self.x, self.y)

    def jump(self):
        red = 255, 0, 0
        if self.is_in_jump:
            if not self.played:
                self.sound.play()
                self.played = True
            self.set_sprite(self.sprites[0])
            if self.down <= self.bottom:  # when player is not on the ground
                self.vy += self.gravity
                self.y += self.vy
                if self.down == self.bottom and self.vy > 0:  # if player is going down and touches the ground
                    self.vy = self.jump_speed
                    self.place_to(self.x, self.bottom - self.image.get_size()[1] * 0.5)  # bring player to the ground
                    self.is_in_jump = False  # stop jumping code execution
                    self.played = False
            self.recalculate_borders()
            #self.draw_borders(red)
        #self.draw_borders(red)

    def place_to(self, x=0, y=0):
        self.x = x
        x1 = x - self.image.get_size()[0] * 0.5
        self.y = y
        y1 = y - self.image.get_size()[1]*0.5
        self.left = self.x - self.image.get_size()[0]*0.5
        self.right = self.x + self.image.get_size()[0] * 0.5
        self.up = self.y - self.image.get_size()[1] * 0.5
        self.down = self.y + self.image.get_size()[1] * 0.5
        self.scene.screen.blit(self.image, (x1, y1))

    def draw_borders(self, color):
        pygame.draw.line(self.scene.screen, color, (self.x, self.up), (self.x, self.down))
        pygame.draw.line(self.scene.screen, color, (self.left, self.y), (self.right, self.y))
        pygame.draw.line(self.scene.screen, color, (self.left, self.up), (self.right, self.up))
        pygame.draw.line(self.scene.screen, color, (self.left, self.down), (self.right, self.down))
        pygame.draw.line(self.scene.screen, color, (self.left, self.up), (self.left, self.down))
        pygame.draw.line(self.scene.screen, color, (self.right, self.up), (self.right, self.down))

    def set_sprite(self, sprite):
        self.image = sprite

    def update(self):
        self.scene.screen.blit(self.image, (self.left, self.up))

    def recalculate_borders(self):
        self.up = self.y - self.image.get_size()[1]*0.5
        self.down = self.y + self.image.get_size()[1]*0.5

    def check_for_collisions(self):
        o = self.scene.objects
        width = self.image.get_size()[0]
        height = self.image.get_size()[1]
        for i in range(1, len(self.scene.objects), 1):
            if self.left - 0.5*width <= o[i].x <= self.right + 0.5*width and\
                    self.up - 0.5*height <= o[i].y <= self.down + 0.5*height:  # checks for collision
                return True
        return False

    def set_scene(self, scene):
        self.scene = scene

    def get_surface_from_symbol( self, symbol ):
        # ord - Returns a numeric representation for the specified character.
        return self.font[ ord(symbol) - self.negativeFontOffsetRelativeToAsciiCodes ]

    def get_surfaces_array_from_string( self, str ):
        surfacesArray = []
        for symbol in str:
            surfacesArray.append( self.get_surface_from_symbol( symbol ) )
        return surfacesArray
	
    def draw_label_with_value( self, label, value, verticalOffsetPx ):
		 
        labelSurfacesArray = self.get_surfaces_array_from_string( label )
		
        ssize = labelSurfacesArray[0].get_size()[0]
		
		# draw label
		
        for i in range(len(labelSurfacesArray)):
            self.scene.screen.blit( labelSurfacesArray[i], ( 20 + i * ssize, verticalOffsetPx ) )
			
		# draw number value
		
        valueString = str(value)
		
        zsize = self.get_surface_from_symbol('0').get_size()[0]
		
        for i in range(len(valueString)):
            self.scene.screen.blit( self.get_surface_from_symbol(valueString[i]), ( 7 * ssize + i * zsize, verticalOffsetPx ) )
