import pygame
from screen import Screen
from map import Map
from player import Player
from keylistener import KeyListener
import json
from showInventary import showInventary
from bouttons import *
import time

class Game:
    def __init__(self):
        self.running = True
        self.screen = Screen()
        self.map = Map(self.screen)
        self.keylistener = KeyListener()
        self.player = Player(self.keylistener, self.screen, 96, 476)

        self.img = pygame.image.load("../Design/Dialogue.png")
        self.map.add_player(self.player)
        self.game_over_font = pygame.font.Font("../Design/gabriola.ttf", 60)
        self.game_over_text = self.game_over_font.render("Game Over", True, (255, 0, 0))
        self.game_over_text_rect = self.game_over_text.get_rect(
            center=(self.screen.get_size()[0] // 2, self.screen.get_size()[1] // 2))
        self.win = False
        self.win_text = self.game_over_font.render("Merci d'avoir joué !\n        DTS prod", True, (255, 0, 0))
        self.win_text_rect = self.win_text.get_rect(
            center=(self.screen.get_size()[0] // 2, self.screen.get_size()[1] // 2))
        self.showInventory = showInventary(self.player.inventory, self.screen)
        f = open('Artefact.json')
        self.descriptionArtefact = json.load(f)

        self.pause = False
        self.menu_state = "main"
        self.resume_img = pygame.image.load("../Design/continuer.png")
        self.loot_img = pygame.image.load("../Design/inventaire.png")
        self.quit_img = pygame.image.load("../Design/quitter.png")
        self.opt_image = pygame.image.load("../Design/options.png")
        self.background_pause = pygame.image.load("../Design/pause_background.png ")

        self.resume_button = Boutton(623, 300, self.resume_img, 1)
        self.loot_button = Boutton(623, 460, self.loot_img, 1)
        self.option_button = Boutton(623, 620, self.opt_image, 1)
        self.quit_button = Boutton(623, 780, self.quit_img, 1)

        self.song = "../Musique/Belle_musique_chinoise.mp3"
        pygame.mixer.init()
        pygame.mixer.music.load(self.song)
        pygame.mixer.music.play()

        self.game_over = False  # Variable pour suivre l'état de l'écran de fin de partie

    def display_background_pause(self, background_pause):
        size = pygame.transform.scale(background_pause, (1920, 1080))
        self.screen.display.blit(size, (0, 0))

    def play_sound(self):
        if pygame.mixer.music.get_busy():
            pass
        else:
            pygame.mixer.music.play()

    def run(self):
        clock = pygame.time.Clock()
        while self.running:

            self.play_sound()
            self.handling_events()

            if not self.showInventory.active and not self.showInventory.showArtefactActive and not self.pause:
                self.update()
                self.Draw()

            elif self.pause:
                self.screen.display.fill((52, 78, 91))

                if self.menu_state == "main":
                    # draw pause screen buttons
                    self.display_background_pause(self.background_pause)
                    if self.resume_button.draw_and_locate(self.screen):
                        self.pause = False
                    elif self.option_button.draw_and_locate(self.screen):
                        print("Options")
                    elif self.quit_button.draw_and_locate(self.screen):
                        self.running = False
                    elif self.loot_button.draw_and_locate(self.screen):
                        self.pause = False
                        self.showInventory.active = True

            elif self.showInventory.active:
                self.showInventory.DisplayInventory(self.player.inventory, self.screen)
            if self.player.vies <= 0:
                self.show_game_over_screen()
                self.game_over = True

            elif self.player.collision_win_detected:
                self.show_win_screen()

            if self.game_over and pygame.time.get_ticks() - self.game_over_start_time >= 3000:
                self.restart_game()  # Redémarrer le jeu après 3 secondes

            pygame.display.flip()
            dt = clock.tick()
            print(1000/dt)
            if self.win == True:
                time.sleep(10)
                self.running = False

    def Draw(self):
        ####### MIRROIR ########
        if self.player.Mirror_detected:
            self.player.DRAWTEXT("Ouvrez vos livres page 12", self.player.text_font, (255, 255, 255), 100, 100)
            self.player.DRAWTEXT("F", self.player.text_font, (255, 255, 255), 900, 750)
        elif not self.player.Mirror_detected:
            pass
        ####### PIECE ########
        if self.player.Piece_detected:
            self.player.DRAWTEXT("Ouvrez vos livres page 64", self.player.text_font, (255, 255, 255), 100, 100)
            self.player.DRAWTEXT("F", self.player.text_font, (255, 255, 255), 900, 750)
        elif not self.player.Piece_detected:
            pass
        ####### ANNEAU ########
        if self.player.Anneau_detected:
            self.player.DRAWTEXT("Ouvrez vos livres page 73", self.player.text_font, (255, 255, 255), 100, 100)
            self.player.DRAWTEXT("F", self.player.text_font, (255, 255, 255), 900, 750)
        elif not self.player.Anneau_detected:
            pass
        ########### PNJ 1 ############
        if self.player.PNJ1_detected:
            self.player.DRAWTEXT("F", self.player.text_font, (255, 255, 255), 900, 750)
            if self.player.PNJ1_Dialogue_detected:
                self.screen.display.blit(self.img, (
                    self.screen.display.get_width() - self.img.get_width() - self.img.get_width() // 7,
                    self.screen.display.get_height() // 15))
                self.player.DRAWTEXT("Bienvenue étranger, tu te trouve sur le territoire du premier empereur de Chine.\n "
                                     "Nous sommes en l'an 221 et c'est l'empereur Qin Shi Huangqui règne en maître sur\nces terres. "
                                     "Jette un oeil sur son territoire et contemple les richesses qui entourent\nce magnifique pays.",
                                     self.player.text_font, (228,182,69),
                                     self.img.get_rect().centerx - self.img.get_width() // 8,
                                     self.img.get_rect().centery - self.img.get_height() // 8)
        elif not self.player.PNJ1_detected:
            pass
        ########### PNJ 2 ###############
        if self.player.PNJ2_detected:
            self.player.DRAWTEXT("F", self.player.text_font, (255, 255, 255), 1600, 750)
            if self.player.PNJ2_Dialogue_detected:
                self.screen.display.blit(self.img, (
                    self.screen.display.get_width() - self.img.get_width() - self.img.get_width() // 7,
                    self.screen.display.get_height() // 15))
                self.player.DRAWTEXT("Ah, re-bonjour étranger, qu'as-tu pensé du lieu ? Fascinant, n'est-ce pas ?\nSache que notre souverain est connu pour être implacable et autoritaire. Il a conquis de\n nombreuses terres et continuera ainsi. Cependant, afin de protéger son peuple des attaques\n ennemies, il ordonna la construction d'une grande muraille. ", self.player.text_font, (228,182,69),
                                     self.img.get_rect().centerx - self.img.get_width() // 5,
                                     self.img.get_rect().centery - self.img.get_height() // 8)
        elif not self.player.PNJ2_detected:
            pass
        ########### PNJ 3 ############
        if self.player.PNJ3_detected:
            self.player.DRAWTEXT("F", self.player.text_font, (255, 255, 255), 600, 750)
            if self.player.PNJ3_Dialogue_detected:
                self.screen.display.blit(self.img, (
                    self.screen.display.get_width() - self.img.get_width() - self.img.get_width() // 7,
                    self.screen.display.get_height() // 15))
                self.player.DRAWTEXT("Salut à toi étranger, bienvenue dans la Chine sous la domination des Mongols.\nLeur dirigeant: la famille Khan règne en maître sur ces lieux suite à la victoire\ncontre les Song cette guerre marque un tournant majeur pour la Chine, mais je te laisse\nconstater par toi-même pour que tu puisses découvrir.", self.player.text_font, (228,182,69),
                                     self.img.get_rect().centerx - self.img.get_width() // 5,
                                     self.img.get_rect().centery - self.img.get_height() // 8)
        elif not self.player.PNJ3_detected:
            pass
        ########### PNJ4 ########
        if self.player.PNJ4_detected:
            self.player.DRAWTEXT("F", self.player.text_font, (255, 255, 255), 1600, 750)
            if self.player.PNJ4_Dialogue_detected:
                self.screen.display.blit(self.img, (
                    self.screen.display.get_width() - self.img.get_width() - self.img.get_width() // 7,
                    self.screen.display.get_height() // 15))
                self.player.DRAWTEXT("Re-bonjour étranger, alors qu'en penses-tu ? Sache que les Mongols ont instauré un régime\nstrict pour maintenir le contrôle, imposant des taxes lourdes et des réformes administratives.\nCependant, Kubilai Khan a également adopté certaines pratiques chinoises et encouragé le\ncommerce et la culture, ce qui a apporté une certaine stabilité à l'empire. ", self.player.text_font, (228,182,69),
                                     self.img.get_rect().centerx - self.img.get_width() // 5,
                                     self.img.get_rect().centery - self.img.get_height() // 8)
        elif not self.player.PNJ4_detected:
            pass
        if self.player.key_detected:
            self.player.DRAWTEXT("F", self.player.text_font, (255, 255, 255), 900, 450)
        elif not self.player.key_detected:
            pass

    def handling_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self.keylistener.add_key(event.key)
                if event.key == pygame.K_i and not self.showInventory.showArtefactActive:
                    self.showInventory.active = not self.showInventory.active
                if event.key == pygame.K_ESCAPE and not self.showInventory.showArtefactActive and not self.showInventory.active == True :
                    self.pause = not self.pause
                if event.key == pygame.K_r and self.game_over:
                    self.restart_game()  # Appel de la méthode restart_game()  "R" est enfoncée après l'écran de fin de partie
                    self.game_over = False
            elif event.type == pygame.KEYUP:
                self.keylistener.remove_key(event.key)
            if self.showInventory.active and event.type == pygame.MOUSEBUTTONDOWN:
                self.showInventory.ClickItem(event, self.player.inventory, self.screen, self.descriptionArtefact)
            elif self.showInventory.showArtefactActive and event.type == pygame.MOUSEBUTTONDOWN:
                self.showInventory.showArtefactActive = False
                self.showInventory.active = True

    def update(self):
        self.map.update()
        self.player.draw_lives()

    def show_game_over_screen(self):
        if not self.game_over:
            self.game_over_start_time = pygame.time.get_ticks()
        black_surface = pygame.Surface(self.screen.get_size())
        black_surface.set_alpha(220)
        black_surface.fill((0, 0, 0))
        self.screen.get_display().blit(black_surface, (0, 0))
        self.screen.get_display().blit(self.game_over_text, self.win_text_rect)

    def show_win_screen(self):
        black_surface = pygame.Surface(self.screen.get_size())
        black_surface.set_alpha(220)
        black_surface.fill((0, 0, 0))
        self.screen.get_display().blit(black_surface, (0, 0))
        self.screen.get_display().blit(self.win_text, self.win_text_rect)
        self.win = True

    def restart_game(self):
        self.game_over = False
        # Réinitialiser les paramètres
        self.player.position = pygame.math.Vector2(90, 476) # coordoner de spawn
        self.player.vies = 3
        self.player.trapped_traps = {}
        self.player.trapped_cle = {}