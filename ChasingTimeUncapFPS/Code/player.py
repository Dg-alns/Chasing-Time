from __future__ import annotations

import pygame
from entity import Entity
from keylistener import KeyListener
from screen import Screen
from inventoryList import InventoryList
from artefact import Artefact
from switch import Switch


class Player(Entity):
    def __init__(self, keylistener: KeyListener, screen: Screen, x: int, y: int):
        super().__init__(keylistener, screen, x, y)
        self.text_font = pygame.font.Font("../Design/gabriola.ttf", 40)
        self.vies: int = 3

        self.switchs: list[Switch] | None = None
        self.change_map: Switch | None = None

        self.onGround = False
        self.Mirror_detected = False
        self.Piece_detected = False
        self.Anneau_detected = False
        self.PNJ1_detected = False
        self.PNJ2_detected = False
        self.PNJ3_detected = False
        self.PNJ4_detected = False
        self.PNJ1_Dialogue_detected = False
        self.PNJ2_Dialogue_detected = False
        self.PNJ3_Dialogue_detected = False
        self.PNJ4_Dialogue_detected = False
        self.key_detected = False
        self.gravity = 5.2
        self.is_jumping = False
        self.jump_height = 4.5
        self.inventoryList = InventoryList()
        self.artefact = Artefact()
        self.jump_count = self.jump_height * 3
        self.is_colliding_ground = False
        self.is_colliding_bottom = False
        self.previous_position = pygame.math.Vector2(x, y)
        self.trapped_traps = {}
        self.trapped_cle = {}
        self.collision_win_detected = False
        self.invisibility = 0

        self.inventory = ["","","","","","","","",""]
        self.witchArtefact = None
        self.pvImage = []
        for i in range(4):self.pvImage.append(pygame.transform.scale(pygame.image.load(f"../Design/PV{i}.png"),(pygame.image.load(f"../Design/PV{i}.png").get_width()*1.5,pygame.image.load(f"../Design/PV{i}.png").get_height()*1.5)))
    def check_move(self) -> None:
        # Déplacement horizontal
        self.animation_walk = False
        temp_hitbox = self.hitbox.copy()
        if self.keylistener.key_pressed(pygame.K_q):
            temp_hitbox.x -= 32
            self.check_collisions_switchs(temp_hitbox)
            self.move_left()
            self.position.x -= self.speed
        elif self.keylistener.key_pressed(pygame.K_d):
            temp_hitbox.x += 32
            self.check_collisions_switchs(temp_hitbox)
            self.move_right()
            self.position.x += self.speed


        elif self.keylistener.key_pressed(pygame.K_i):
            pass

        # Saut
        if self.keylistener.key_pressed(pygame.K_z):
            self.move_up()
            self.jump()

        # Saut continu
        if self.is_jumping and not self.is_colliding_bottom:
            self.position.y -= self.speed * 2
            self.jump_count -= 1
            if self.jump_count <= 0:
                self.is_jumping = False
                self.jump_count = self.jump_height * 3

    def add_switchs(self, switchs: list[Switch]):
        self.switchs = switchs

    def check_collisions_switchs(self, temp_hitbox):
        if self.switchs:
            for switch in self.switchs:
                if switch.check_collision(temp_hitbox):
                    self.change_map = switch
                    self.vies = 3
        return None

    def jump(self) -> None:
        if not self.is_jumping and self.is_colliding_ground:
            self.is_jumping = True

    def ClaimArtefact(self, artefact):
        if self.artefact.name == "shield" not in self.inventory:
            element = self.inventoryList.elements.pop(self.inventoryList.elements.index(self.artefact.name))
            self.inventory[0] = "shield"
        if self.artefact.name == "anneau" not in self.inventory:
            element = self.inventoryList.elements.pop(self.inventoryList.elements.index(self.artefact.name))
            self.inventory[1] = "anneau"
        elif self.artefact.name == "piece" not in self.inventory:
            element = self.inventoryList.elements.pop(self.inventoryList.elements.index(self.artefact.name))
            self.inventory[2] = "piece"

    def DRAWTEXT(self, text, font, color, x, y):
        font = self.text_font.render(text, True, color)
        self.screen.display.blit(font, (x, y))

    def check_collision(self, collisionsGround: list[pygame.Rect], collisionsGauche: list[pygame.Rect],
                        collisionsDROITE: list[pygame.Rect], collisionsBottom: list[pygame.Rect],
                        collisionsTrap: list[pygame.Rect], collisionsTrapMax: list[pygame.Rect],  collisionsWin: list[pygame.Rect],
                        COLArtefactMirror: list[pygame.Rect],COLArtefactAnneau: list[pygame.Rect],
                        COLArtefactPiece: list[pygame.Rect], PNJ1: list[pygame.Rect], PNJ2: list[pygame.Rect], PNJ3: list[pygame.Rect], PNJ4: list[pygame.Rect],
                        COLCLE: list[pygame.Rect], COLGCLE: list[pygame.Rect]) -> None:
        collision_ground_detected = False
        collision_gauche_detected = False
        collision_droite_detected = False
        collision_bottom_detected = False

        if self.invisibility > 0:
            self.invisibility += 0.016
            if self.invisibility > 1.5:
                self.invisibility = 0

        for collision in collisionsGround:
            self.onGround = True
            if self.rect.colliderect(collision):
                collision_ground_detected = True
                self.Mirror_detected = False
                self.Piece_detected = False
                self.Anneau_detected = False
                self.PNJ1_detected = False
                self.PNJ2_detected = False
                self.PNJ3_detected = False
                self.PNJ4_detected = False
                self.PNJ1_Dialogue_detected = False
                self.PNJ2_Dialogue_detected = False
                self.PNJ3_Dialogue_detected = False
                self.PNJ4_Dialogue_detected = False
                self.key_detected = False

        for collision in collisionsBottom:
            if self.rect.colliderect(collision):
                collision_bottom_detected = True

        for collision in collisionsGauche:
            if self.rect.colliderect(collision):
                collision_gauche_detected = True

        for collision in COLGCLE:
            self.artefact.name = "piece"
            if self.rect.colliderect(collision):
                self.Piece_detected = True
                if self.keylistener.key_pressed(pygame.K_f):
                    self.ClaimArtefact(self.witchArtefact)

        for collision in collisionsDROITE:
            if self.rect.colliderect(collision):
                collision_droite_detected = True



        for collision in collisionsTrap:
            if self.rect.colliderect(collision):
                trap_key = (collision.x, collision.y)
                if (trap_key not in self.trapped_traps or not self.trapped_traps[trap_key]) and self.invisibility == 0:
                    self.vies -= 1
                    self.invisibility += 0.016

        for collision in collisionsTrapMax:
            if self.rect.colliderect(collision):
                trap_key = (collision.x, collision.y)
                if trap_key not in self.trapped_traps or not self.trapped_traps[trap_key]:
                    self.invisibility += 0.016
                    self.vies = 0

        for collision in COLCLE:
            if self.rect.colliderect(collision):
                if self.trapped_cle:
                    collision_gauche_detected = False
                else:
                    collision_gauche_detected = True

        for collision in collisionsWin:
            if self.rect.colliderect(collision):
                self.collision_win_detected = True

        if collision_ground_detected and collision_gauche_detected:
            self.position.x -= self.speed

        if collision_ground_detected and collision_droite_detected:
            self.position.x += self.speed

        self.is_colliding_ground = collision_ground_detected

        for collision in COLArtefactMirror:
            self.artefact.name = "shield"
            if self.rect.colliderect(collision):
                self.Mirror_detected = True
                if self.keylistener.key_pressed(pygame.K_f):
                    self.ClaimArtefact(self.witchArtefact)

        for collision in COLArtefactPiece:
            if self.rect.colliderect(collision):
                self.PNJ1_detected = True
                if self.keylistener.key_pressed(pygame.K_f):
                    self.PNJ1_Dialogue_detected = True

        for collision in COLArtefactAnneau:
            self.artefact.name = "anneau"
            if self.rect.colliderect(collision):
                self.Anneau_detected = True
                if self.keylistener.key_pressed(pygame.K_f):
                    self.ClaimArtefact(self.witchArtefact)

        for collision in PNJ1:
            if self.rect.colliderect(collision):
                self.PNJ2_detected = True
                if self.keylistener.key_pressed(pygame.K_f):
                    self.PNJ2_Dialogue_detected = True

        for collision in PNJ2:
            if self.rect.colliderect(collision):
                self.PNJ3_detected = True
                if self.keylistener.key_pressed(pygame.K_f):
                    self.PNJ3_Dialogue_detected = True

        for collision in PNJ3:
            if self.rect.colliderect(collision):
                self.PNJ4_detected = True
                if self.keylistener.key_pressed(pygame.K_f):
                    self.PNJ4_Dialogue_detected = True

        for collision in PNJ4:
            if self.rect.colliderect(collision):
                cle_key = (collision.x, collision.y)
                self.key_detected = True
                if self.keylistener.key_pressed(pygame.K_f):
                    if cle_key not in self.trapped_cle or not self.trapped_cle[cle_key]:
                        self.trapped_cle[cle_key] = True






    def update(self, collisions: list[pygame.Rect], collisionsGauche: list[pygame.Rect],
               collisionsDROITE: list[pygame.Rect], collisionsBottom: list[pygame.Rect],
               collisionsTrap: list[pygame.Rect], collisionsWin: list[pygame.Rect],collisionsTrapMax: list[pygame.Rect], COLArtefactMirror: list[pygame.Rect], COLArtefactAnneau: list[pygame.Rect],
               COLArtefactPiece: list[pygame.Rect], PNJ1: list[pygame.Rect], PNJ2: list[pygame.Rect], PNJ3: list[pygame.Rect], PNJ4: list[pygame.Rect],
               COLCLE: list[pygame.Rect], COLGCLE: list[pygame.Rect]) -> None:
        self.check_move()
        super().update()

        self.previous_position = self.position.copy()

        if not self.is_colliding_ground:
            self.gravity = 5.2
        else:
            self.gravity = 0

        self.position.y += self.gravity
        self.rect.center = self.position

        if self.is_jumping:
            if self.jump_count >= -self.jump_height * 3:
                neg = 1
                if self.jump_count < 0:
                    neg = -7
                self.position.y -= (self.jump_count ** 2) * 0.2 * neg
            else:
                self.is_jumping = False
                self.jump_count = self.jump_height * 3

        self.check_collision(collisions, collisionsGauche, collisionsDROITE, collisionsBottom, collisionsTrap,
                             collisionsTrapMax,
                             collisionsWin, COLArtefactMirror, COLArtefactPiece, PNJ1, PNJ2, PNJ3, PNJ4, COLCLE, COLGCLE, COLArtefactAnneau)

    def draw_lives(self):
        self.screen.display.blit(self.pvImage[self.vies],(10,10))
