import pygame
from bouttons import Boutton

pygame.init()

#create a game window
screen = pygame.display.set_mode((1920,1080), pygame.FULLSCREEN)
pygame.display.set_caption("Main Menu")

#game variables
pause = False
menu_state = "main"

#Define fonts
font = pygame.font.SysFont("arialblack", 20, bold= False, italic= False )

#Define colors
COL_TEXT = (255, 255, 255)

#load button images
resume_img = pygame.image.load("../Design/continuer.png")
loot_img = pygame.image.load("../Design/inventaire.png")
quit_img = pygame.image.load("../Design/quitter.png")
opt_image = pygame.image.load("../Design/options.png")

#create a pause Background
background_pause = pygame.image.load("../Design/pause_background.png ")

#create button instances
resume_button = Boutton(623, 300, resume_img, 1)
loot_button = Boutton(623, 460, loot_img, 1)
option_button = Boutton(623, 620, opt_image, 1)
quit_button = Boutton(623, 780, quit_img, 1)

#Load an OST
song = "../Musique/Belle_musique_chinoise.mp3"
pygame.mixer.init()
pygame.mixer.music.load(song)
pygame.mixer.music.play()

def text_draw(text, font, color_text, x, y):
    image= font.render(text, True, color_text)
    screen.blit(image,(x, y))

def display_background_pause (background_pause):
    size = pygame.transform.scale(background_pause, (1920, 1080))
    screen.blit(size, (0, 0))

def play_sound():
    if pygame.mixer.music.get_busy() :
        print("La musique est jouée")
    else:
        pygame.mixer.music.play()
        print("fini")

#game loop
run = True
while run :
    screen.fill((52, 78, 91))

    #Check if game is paused
    if pause == True:
    #check menu state
        if menu_state == "main":
        #draw pause screen buttons
            display_background_pause (background_pause)
            if resume_button.draw_and_locate(screen):
                pause = False
            elif loot_button.draw_and_locate(screen):
                print("Inventaire")
            elif option_button.draw_and_locate(screen):
                print("Options")
            elif quit_button.draw_and_locate(screen):
                run = False
    if pause == False:
        text_draw("Press SPACE to pause", font, COL_TEXT, 160, 250)

#Event handler
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                pause = True
                play_sound()
        if event.type == pygame.QUIT:
            run = False
    
    pygame.display.update()

pygame.quit()