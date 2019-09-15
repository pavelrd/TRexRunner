import pygame


class Scene:
    def __init__(self, resolution):
        self.objects = []
        self.screen = pygame.display.set_mode(resolution)
        pygame.display.set_caption('Dinorun')
        self.width = resolution[0]
        self.height = resolution[1]
        self.font = None

    def add_object(self, another_object):
        self.objects.append(another_object)

    def remove_object(self, object_to_remove):
        self.objects.remove(object_to_remove)

    def clear(self):
        self.screen.fill((255, 255, 255))

    def draw_text(self, text, x=0, y=0):
        for i in range(len(text)):
            self.screen.blit(self.font[text[i]], (x + i * self.font[0].get_size()[0], y))
