import pygame


class Enemy:
    def __init__(self, picture, scene):
        self.image = picture
        self.scene = scene
        self.vx = -5
        self.x = self.scene.width-80
        self.y = self.scene.height-200
        self.right = 0
        self.left = 0
        self.up = 0
        self.down = 0
        self.bottom = scene.height - 200

    def move(self, vx=0):
        self.x += vx
        self.vx += vx

        if self.right < 0:
            self.x = self.scene.width + self.image.get_size()[0]

        self.scene.screen.blit(self.image, (self.left, self.up))
        self.recalculate_borders()

    def place_to(self, x=0, y=0):
        self.x = x
        x1 = x - self.image.get_size()[0] * 0.5
        self.y = y
        y1 = y - self.image.get_size()[1] * 0.5
        self.left = self.x - self.image.get_size()[0] * 0.5
        self.right = self.x + self.image.get_size()[0] * 0.5
        self.up = self.y - self.image.get_size()[1] * 0.5
        self.down = self.y + self.image.get_size()[1] * 0.5
        self.scene.screen.blit(self.image, (x1, y1))

    def recalculate_borders(self):
        self.right = self.x + self.image.get_size()[0]*0.5
        self.left = self.x - self.image.get_size()[0]*0.5
        self.up = self.y - self.image.get_size()[1] * 0.5
        self.down = self.y + self.image.get_size()[1] * 0.5

    def update(self):
        self.scene.screen.blit(self.image, (self.left, self.up))

    def set_sprite(self, sprite):
        self.image = sprite

    def draw_borders(self, color):
        pygame.draw.line(self.scene.screen, color, (self.x, self.up), (self.x, self.down))
        pygame.draw.line(self.scene.screen, color, (self.left, self.y), (self.right, self.y))
        pygame.draw.line(self.scene.screen, color, (self.left, self.up), (self.right, self.up))
        pygame.draw.line(self.scene.screen, color, (self.left, self.down), (self.right, self.down))
        pygame.draw.line(self.scene.screen, color, (self.left, self.up), (self.left, self.down))
        pygame.draw.line(self.scene.screen, color, (self.right, self.up), (self.right, self.down))

