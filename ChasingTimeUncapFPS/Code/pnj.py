from player import Player
from screen import Screen
from keylistener import KeyListener

class PNJ:
    def __init__(self, question, questionA="", questionB="", questionC="", questionD="", Answer=""):
        self.question = question
        self.screen = Screen()
        self.keylistener = KeyListener()
        self.player = Player(self.keylistener, self.screen, 5408, 576)
        if question == 1:
            self.qestionA = questionA
            self.qestionB = questionB
            self.qestionC = questionC
            self.qestionD = questionD
            self.Answer = Answer

    def DRAWTEXT(self, question, options, font, color, x, y):
        # Dessiner la question
        question_surface = font.render(question, True, color)
        self.screen.display.blit(question_surface, (x, y))
        y += question_surface.get_height()  # Ajuster la position Y pour les réponses

        # Dessiner les options de réponse
        for idx, option in enumerate(options):
            option_surface = font.render(option, True, color)
            self.screen.display.blit(option_surface, (x, y + idx * option_surface.get_height()))

