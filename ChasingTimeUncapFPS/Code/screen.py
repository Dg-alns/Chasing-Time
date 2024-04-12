import pygame


class Screen:
    def __init__(self):
        self.display: pygame.display = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption("GC")
        self.clock: pygame.time.Clock = pygame.time.Clock()
        self.framerate: int = 144
        self.deltatime: float = 0.0

    def update(self) -> None:
        pygame.display.flip()
        pygame.display.update()
        self.clock.tick(self.framerate)
        self.clear()  # Ajoutez cette ligne pour effacer l'écran à chaque mise à jour
        self.deltatime = self.clock.get_time()


    def get_delta_time(self) -> float:
        return self.deltatime

    def get_size(self) -> tuple[int, int]:
        return self.display.get_size()

    def get_display(self) -> pygame.display:
        return self.display