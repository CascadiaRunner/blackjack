import pygame
import os
pygame.font.init()

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

FPS = 60

GREEN = (0 , 255, 0)
WHITE = (255, 255, 255)
BLACK = (0,0,0)
RED = (255,0,0)

CARDBACK_IMAGE = pygame.image.load(
    os.path.join('.\images\cards', 'back.png'))

CARD_WIDTH = CARDBACK_IMAGE.get_width()
CARD_HEIGHT = CARDBACK_IMAGE.get_height()

CARD = pygame.Rect(1, 1, CARD_WIDTH, CARD_HEIGHT)

CARD_FONT = pygame.font.SysFont('comicsans', 24)


def draw_card(card_num):
	# card_image = pygame.image.load(os.path.join('.\images\cards', '{}{}.png'.format(CARD_MAP['suits'][card.suit], CARD_MAP['ranks'][card.rank])))
	WIN.blit(CARDBACK_IMAGE, (CARD.x + (CARD_WIDTH * card_num), CARD.y))


def draw_window():
	WIN.fill(GREEN)
	num_cards = 6
	for n in range(0,num_cards):
		draw_card(n)

	


	pygame.display.update()

def main():
	clock = pygame.time.Clock()
	run = True 

	while run:
		clock.tick(FPS)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

		draw_window()
					
	pygame.quit()

if __name__ == "__main__":
	main()