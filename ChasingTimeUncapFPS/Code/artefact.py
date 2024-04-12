import pygame.image


class Artefact:
    def __init__(self):
        self.name = None


    def DrawClaimItem(self, name):
        image = pygame.image.load(f"../../Design/text{name}.png")
