import pygame
import bouttons


#create display window
screen = pygame.display.set_mode((1920, 1080))

#load button images
start_img = pygame.image.load('../Design/start_btn.png')
exit_img = pygame.image.load('../Design/exit_btn.png')

#create button instances
start_button = bouttons.Boutton(100, 200, start_img, 0.8)
exit_button = bouttons.Boutton(450, 200, exit_img, 0.8)

#game loop
run = True
while run:

	screen.fill((202, 228, 241))

	if start_button.draw(screen):
		print('START')
	if exit_button.draw(screen):
		print('EXIT')

	#event handler
	for event in pygame.event.get():
		#quit game
		if event.type == pygame.QUIT:
			run = False

	pygame.display.update()

pygame.quit()