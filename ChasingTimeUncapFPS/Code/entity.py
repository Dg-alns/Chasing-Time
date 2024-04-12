import pygame
from keylistener import KeyListener
from screen import Screen
from tool import Tool


class Entity(pygame.sprite.Sprite):
    def __init__(self, keylistener: KeyListener, screen: Screen, x: int, y: int):
        super().__init__()
        self.screen: Screen = screen
        self.keylistener: KeyListener = keylistener
        self.spritesheet: pygame.image = pygame.image.load("../Sprite/SpriteSheet.png")
        self.image: pygame.image = Tool.split_image(self.spritesheet, 0, 0, 64, 120)
        self.position: pygame.math.Vector2 = pygame.math.Vector2(x, y)
        self.rect: pygame.Rect = self.image.get_rect()
        self.all_images: dict[str, list[pygame.image]] = self.get_all_images(self.spritesheet)
        self.index_image: int = 0
        self.image_part: int = 0
        self.reset_animation: bool = False
        self.hitbox: pygame.Rect = pygame.Rect(0, 0, 16, 16)

        self.previousStep = "right"
        self.directionBis = "right"
        self.numAnimation = 0
        self.sameSprite = 0

        self.step: int = 0
        self.animation_walk: bool = False
        self.direction: str = "down"

        self.animtion_step_time: float = 0.0
        self.action_animation: int = 16

        self.speed: float = 4

    def update(self) -> None:
        self.setSprite()
        self.move()
        self.rect.center = self.position
        self.hitbox.midbottom = self.rect.midbottom
        self.animationSprite()

    def move_left(self) -> None:
        self.animation_walk = True
        self.directionBis = "left"
        self.direction = "left"

    def move_right(self) -> None:
        self.animation_walk = True
        self.directionBis = "right"
        self.direction = "right"

    def move_up(self) -> None:
        self.animation_walk = True
        self.direction = "up"

    def setSprite(self) -> None:
        if int(self.step // 8) + self.image_part >= 4:
            self.image_part = 0
            self.reset_animation = True
        self.index_image = int(self.step // 8) + self.image_part

    def animationSprite(self):
        if self.animation_walk:
            if self.directionBis == "left" and self.direction == "up":
                self.direction = "upLeft"
            elif self.directionBis == "right" and self.direction == "up":
                self.direction = "upRight"

            if self.previousStep == self.direction:
                self.sameSprite += 1
            else:
                self.previousStep = self.direction
                self.sameSprite = 0
                self.numAnimation = 0

            if self.sameSprite == 10:
                self.numAnimation += 1
                self.sameSprite = 0

            if self.numAnimation >= 6:
                self.numAnimation = 0

            self.image = self.all_images[self.direction][self.index_image + self.numAnimation]
        else:
            self.image = pygame.image.load("../Sprite/Prof.png")


    def move(self) -> None:
        if self.animation_walk:
            self.animtion_step_time += self.screen.get_delta_time()
            if self.step < 16 and self.animtion_step_time >= self.action_animation:
                self.step += self.speed
                if self.direction == "left":
                    self.position.x -= self.speed
                elif self.direction == "right":
                    self.position.x += self.speed
                elif self.direction == "up":
                    self.position.y -= self.speed
                self.animtion_step_time = 0
            elif self.step >= 16:
                self.step = 0
                self.animation_walk = False
                if self.reset_animation:
                    self.reset_animation = False
                else:
                    if self.image_part == 0:
                        self.image_part = 2
                    else:
                        self.image_part = 0

    def align_hitbox(self) -> None:
        self.position.x += 16
        self.rect.center = self.position
        self.hitbox.midbottom = self.rect.midbottom
        while self.hitbox.x % 16 != 0:
            self.rect.x -= 1
            self.hitbox.midbottom = self.rect.midbottom
        while self.hitbox.y % 16 != 0:
            self.rect.y -= 1
            self.hitbox.midbottom = self.rect.midbottom
        self.position = pygame.math.Vector2(self.rect.center)

    def get_all_images(self, spritesheet) -> dict[str, list[pygame.image]]:
        all_images = {
            "right": [],
            "left": [],
            "upRight": [],
            "upLeft": []
        }

        width: int = spritesheet.get_width() // 7
        height: int = spritesheet.get_height() // 4

        for i in range(7):
            for j, key in enumerate(all_images.keys()):
                if j == 0:
                    all_images[key].append(Tool.split_image(self.spritesheet, i * width, j * height, 88, 128))
                if j == 1:
                    all_images[key].append(Tool.split_image(self.spritesheet, i * width, 512 - 366, 88, 122))
                if j == 2 and i < 7:
                    if i == 0:
                        all_images[key].append(Tool.split_image(self.spritesheet, 0, 512 - 244, 90, 116))
                    if i == 1:
                        all_images[key].append(Tool.split_image(self.spritesheet, 619 - 530, 512 - 244, 530 - 460, 116))
                    if i == 2:
                        all_images[key].append(Tool.split_image(self.spritesheet, 619 - 460, 512 - 244, 460 - 360, 116))
                    if i == 3:
                        all_images[key].append(Tool.split_image(self.spritesheet, 619 - 360, 512 - 244, 360 - 270, 116))
                    if i == 4:
                        all_images[key].append(Tool.split_image(self.spritesheet, 619 - 270, 512 - 244, 270 - 170, 116))
                    if i == 5:
                        all_images[key].append(Tool.split_image(self.spritesheet, 619 - 170, 512 - 244, 170 - 90, 116))
                if j == 3 and i < 7:
                    if i == 0:
                        all_images[key].append(Tool.split_image(self.spritesheet, 0, 512 - 128, 90, 116))
                    if i == 1:
                        all_images[key].append(Tool.split_image(self.spritesheet, 619 - 530, 512 - 128, 530 - 460, 116))
                    if i == 2:
                        all_images[key].append(Tool.split_image(self.spritesheet, 619 - 460, 512 - 128, 460 - 360, 116))
                    if i == 3:
                        all_images[key].append(Tool.split_image(self.spritesheet, 619 - 360, 512 - 128, 360 - 270, 116))
                    if i == 4:
                        all_images[key].append(Tool.split_image(self.spritesheet, 619 - 270, 512 - 128, 270 - 170, 116))
                    if i == 5:
                        all_images[key].append(Tool.split_image(self.spritesheet, 619 - 170, 512 - 128, 170 - 90, 116))

        return all_images
