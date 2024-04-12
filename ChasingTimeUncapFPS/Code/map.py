from __future__ import annotations

import pygame
import pyscroll
import pytmx

from player import Player
from screen import Screen
from switch import Switch


class Map:
    def __init__(self, screen: Screen):
        self.screen: Screen = screen
        self.tmx_data: pytmx.TiledMap | None = None
        self.map_layer: pyscroll.BufferedRenderer | None = None
        self.group: pyscroll.PyscrollGroup | None = None

        self.player: Player | None = None



        self.collisionsGround: list[pygame.Rect] | None = None
        self.collisionsGauche: list[pygame.Rect] | None = None
        self.collisionsDROITE: list[pygame.Rect] | None = None
        self.collisionsBottom: list[pygame.Rect] | None = None
        self.collisionsTrap: list[pygame.Rect] | None = None
        self.collisionsWin: list[pygame.Rect] | None = None
        self.collisionsTrapMax: list[pygame.Rect] | None = None
        self.COLArtefactMirror: list[pygame.Rect] | None = None
        self.COLArtefactPiece: list[pygame.Rect] | None = None
        self.COLArtefactAnneau: list[pygame.Rect] | None = None
        self.PNJ1: list[pygame.Rect] | None = None
        self.PNJ2: list[pygame.Rect] | None = None
        self.PNJ3: list[pygame.Rect] | None = None
        self.PNJ4: list[pygame.Rect] | None = None
        self.COLCLE: list[pygame.Rect] | None = None
        self.COLGCLE: list[pygame.Rect] | None = None

        self.switch: tuple[Switch] | None = None

        self.current_map: Switch = Switch("switch", "map1", pygame.Rect(0, 0, 0, 0), 0)

        self.switch_map(self.current_map)

    def switch_map(self, switch: Switch) -> None:
        self.tmx_data = pytmx.load_pygame(f"../Design/{switch.name}.tmx")
        map_data = pyscroll.data.TiledMapData(self.tmx_data)
        self.map_layer = pyscroll.BufferedRenderer(map_data, self.screen.get_size())
        self.group = pyscroll.PyscrollGroup(map_layer=self.map_layer, default_layer=3)
        self.map_layer.zoom = 1.5

        self.switchs = []

        self.collisionsGround = []
        self.collisionsGauche = []
        self.collisionsDROITE = []
        self.collisionsBottom = []
        self.collisionsTrap = []
        self.collisionsTrapMax = []
        self.collisionsWin = []
        self.COLArtefactMirror = []
        self.COLArtefactPiece = []
        self.COLArtefactAnneau = []
        self.PNJ1 = []
        self.PNJ2 = []
        self.PNJ3 = []
        self.PNJ4 = []
        self.COLCLE = []
        self.COLGCLE = []


        for obj in self.tmx_data.objects:
            if obj.name == "Collision":
                self.collisionsGround.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
            elif obj.name == "COL":
                self.collisionsGauche.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
            elif obj.name == "COLD":
                self.collisionsDROITE.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
            elif obj.name == "COLB":
                self.collisionsBottom.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
            elif obj.name == "COLT":
                self.collisionsTrap.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
            elif obj.name == "COLTM":
                self.collisionsTrapMax.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
            elif obj.name == "COLW":
                self.collisionsWin.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
            elif obj.name == "COLArtefactMirror":
                self.COLArtefactMirror.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
            elif obj.name == "COLArtefactPiece":
                self.COLArtefactPiece.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
            elif obj.name == "COLArtefactAnneau":
                self.COLArtefactAnneau.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
            elif obj.name == "PNJ1":
                self.PNJ1.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
            elif obj.name == "PNJ2":
                self.PNJ2.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
            elif obj.name == "PNJ3":
                self.PNJ3.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
            elif obj.name == "PNJ4":
                self.PNJ4.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
            elif obj.name == "COLCLE":
                self.COLCLE.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
            elif obj.name == "COLGCLE":
                self.COLGCLE.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

            for obj in self.tmx_data.objects:
                if obj.name:
                    type = obj.name.split(" ")[0]
                    if type == "switch":
                        self.switchs.append(Switch(
                            type, obj.name.split(" ")[1], pygame.Rect(obj.x, obj.y, obj.width, obj.height),
                            int(obj.name.split(" ")[-1])
                        ))

        if self.player:
            self.pose_player(switch)
            self.player.align_hitbox()
            self.player.add_switchs(self.switchs)
            self.group.add(self.player)
    def add_player(self, player) -> None:
        self.group.add(player)
        self.player = player
        self.player.align_hitbox()
        self.player.add_switchs(self.switchs)
        self.player.collisions = (self.collisionsGround and self.collisionsGauche and self.collisionsDROITE and
                                  self.collisionsBottom and self.collisionsTrap and self.collisionsWin and
                                  self.collisionsTrapMax and self.COLArtefactMirror and self.COLArtefactPiece and self.COLArtefactAnneau
                                  and self.PNJ1 and self.PNJ2 and self.PNJ3 and self.PNJ4 and self.COLCLE and self.COLGCLE)  # Passer la liste des collisions au joueur


    def update(self) -> None:
        if self.player:
            if self.player.change_map:
                self.switch_map(self.player.change_map)
                self.player.change_map = None
        self.group.update(self.collisionsGround, self.collisionsGauche, self.collisionsDROITE, self.collisionsBottom,
                          self.collisionsTrap, self.collisionsWin, self.collisionsTrapMax, self.COLArtefactMirror, self.COLArtefactAnneau,
                          self.COLArtefactPiece, self.PNJ1, self.PNJ2, self.PNJ3, self.PNJ4, self.COLCLE, self.COLGCLE)  # Passer la liste des collisions
        self.group.center(self.player.rect.center)
        self.group.draw(self.screen.get_display())

    def pose_player(self, switch: Switch):
        position = self.tmx_data.get_object_by_name("spawn " + self.current_map.name + " " + str(switch.port))
        self.player.position = pygame.math.Vector2(position.x, position.y)