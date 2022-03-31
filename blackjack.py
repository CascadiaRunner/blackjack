import random
from IPython.display import clear_output
import pygame
import time
import os

pygame.init()

# Globals
WIDTH, HEIGHT = 900, 500

BET_FONT = pygame.font.SysFont('comicsans', 40)
PLAYER_CHIPS_FONT = pygame.font.SysFont('comicsans', 30)
WINNER_FONT = pygame.font.SysFont('comicsans', 20)

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chris' Blackgame v2.0")
BUTTON_AREA = (0, 0, 200, HEIGHT)

GREEN = (0 , 255, 0)
WHITE = (255, 255, 255)
BLACK = (0,0,0)
RED = (255,0,0)

suits = ('♠', '♦', '♥', '♣')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight',\
		 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7,\
		  'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10, 'Queen':10, 'King':10,\
		  'Ace':11}
CARD_MAP = {
	'suits': {'♠':'s', '♦':'d', '♥':'h', '♣':'c'},
	'ranks': {'Two':'2', 'Three':'3', 'Four':'4', 'Five':'5', 'Six':'6', 'Seven':'7',\
		 'Eight':'8','Nine':'9', 'Ten':'10', 'Jack':'j', 'Queen':'q', 'King':'k', 'Ace':'a'}
}

# CARD = pygame.Rect(1, 1, CARD_WIDTH, CARD_HEIGHT)
# CARD_FONT = pygame.font.SysFont('comicsans', 24)

HIT_IMAGE = pygame.image.load(
    os.path.join('.\images', 'hit.png'))
HIT_GREY_IMAGE = pygame.image.load(
    os.path.join('.\images', 'hit-grey.png'))
STAND_IMAGE = pygame.image.load(
    os.path.join('.\images', 'stand.png'))
STAND_GREY_IMAGE = pygame.image.load(
    os.path.join('.\images', 'stand-grey.png'))
UP_IMAGE = pygame.image.load(
    os.path.join('.\images', 'up.png'))
DOWN_IMAGE = pygame.image.load(
    os.path.join('.\images', 'down.png'))
UP_GREY_IMAGE = pygame.image.load(
    os.path.join('.\images', 'up-grey.png'))
DOWN_GREY_IMAGE = pygame.image.load(
    os.path.join('.\images', 'down-grey.png'))
DEAL_IMAGE = pygame.image.load(
    os.path.join('.\images', 'deal.png'))
DEAL_GREY_IMAGE = pygame.image.load(
    os.path.join('.\images', 'deal-grey.png'))
DD_IMAGE = pygame.image.load(
    os.path.join('.\images', 'double.png'))
DD_GREY_IMAGE = pygame.image.load(
    os.path.join('.\images', 'double-grey.png'))
SPLIT_IMAGE = pygame.image.load(
    os.path.join('.\images', 'split.png'))
SPLIT_GREY_IMAGE = pygame.image.load(
    os.path.join('.\images', 'split-grey.png'))
CARDBACK_IMAGE = pygame.image.load(
    os.path.join('.\images\cards', 'back.png'))
CARD_WIDTH = CARDBACK_IMAGE.get_width()
CARD_HEIGHT = CARDBACK_IMAGE.get_height()

HIT_POS = (10, 50)
STAND_POS = (10, 100)
DD_POS = (10, 150)
SPLIT_POS = (10, 200)
UP_POS = (10, 300)
DOWN_POS = (120, 300)
DEAL_POS = (10, 400)
BET_POS = (65, 300)
FIRST_CARD = (300, 50)
PLAYER_CHIPS_POS = (10, 450)
WINNER_POS = (500,25)

HIT_BUTTON = pygame.Rect(HIT_POS[0], HIT_POS[1], HIT_IMAGE.get_width(), HIT_IMAGE.get_height())
STAND_BUTTON = pygame.Rect(STAND_POS[0], STAND_POS[1], STAND_IMAGE.get_width(), STAND_IMAGE.get_height())
DD_BUTTON = pygame.Rect(DD_POS[0], DD_POS[1], DD_IMAGE.get_width(), DD_IMAGE.get_height())
SPLIT_BUTTON = pygame.Rect(SPLIT_POS[0], SPLIT_POS[1], SPLIT_IMAGE.get_width(), SPLIT_IMAGE.get_height())
UP_BUTTON = pygame.Rect(UP_POS[0], UP_POS[1], UP_IMAGE.get_width(), UP_IMAGE.get_height())
DOWN_BUTTON = pygame.Rect(DOWN_POS[0], DOWN_POS[1], DOWN_IMAGE.get_width(), DOWN_IMAGE.get_height())
DEAL_BUTTON = pygame.Rect(DEAL_POS[0], DEAL_POS[1], DEAL_IMAGE.get_width(), DEAL_IMAGE.get_height())

FPS = 60

# CLASS DEFINITIONS
class Card:
	def __init__(self,suit,rank):
		self.suit = suit
		self.rank = rank
	
	def __str__(self):
		return self.rank + ' of ' + self.suit

class Deck:
	def __init__(self):
		self.deck = []  # start with an empty list
		for suit in suits:
			for rank in ranks:
				self.deck.append(Card(suit,rank))
		
	def __str__(self):
		deck_comp = ''
		for card in self.deck:
			deck_comp += '\n' + card.__str__()
		return 'The deck has: ' + deck_comp

	def shuffle(self):
		random.shuffle(self.deck)
		
	def deal(self):
		new_card = self.deck.pop()
		return new_card

class Hand:
	def __init__(self):
		self.cards = []  # start with an empty list as we did in the Deck class
		self.value = 0   # start with zero value
		self.aces = 0    # add an attribute to keep track of aces
	
	def add_card(self,card):
		# card passed in
		# from Deck.deal()
		self.cards.append(card)
		self.value += values[card.rank]
		
		# track aces
		if card.rank == 'Ace':
			self.aces += 1
	
	def adjust_for_ace(self):
		
		# IF TOTAL VALUE > 21 AND I STILL HAVE AN ACE
		# THAN CHANGE MY ACE TO BE A 1 INSTEAD OF 11
		while self.value > 21 and self.aces > 0:
			self.value -= 10
			self.aces -= 1

class Chips:
	
	def __init__(self, total):
		self.total = total  # This can be set to a default value or supplied by a user input
		self.bet = 0
		
	def win_bet(self):
		self.total += self.bet
		return self.total
	
	def lose_bet(self):
		self.total -= self.bet
		return self.total
	
	def blackjack(self):
		self.total += (self.bet * 1.5)
		return self.total

def hit(deck,hand):
	
	single_card = deck.deal()
	# print(single_card)
	hand.add_card(single_card)
	hand.adjust_for_ace()
	return hand

def hit_or_stand(deck,hand,chips):
	global playing # to control an upcoming while loop
	global doubledown
	
	while True:
		print("Player has {}".format(hand.value))
		play = input("Hit, Stand or Double Down? Enter 'H', 'S' or 'D': " )
		
		if play[0].lower() == 'h':
			hit(deck,hand)
			break
			
		elif play[0].lower() == 's':
			print("Player Stands! Dealer's turn\n")
			playing = False
			break
		
		elif play[0].lower() == 'd':
			if (chips.bet * 2) > chips.total:
				print("You dont have enough chips to double down!  Enter 'H' or 'S' only")
				break
			
			print('Double Down!  One more card')
			hit(deck,hand)
			doubledown = True
			playing = False
			break
		else:
			print("Sorry I did not understand.  Enter 'H, 'S' or 'D' only!")

def show_some(player,dealer):
	
	print('Dealer Hand:')
	print('*ONE CARD HIDDEN*')
	print(dealer.cards[1])
	print('\n')
	print('Players Hand:')
	for card in player.cards:
		print(card)
	
def show_all(player,dealer):
	
	print('Dealer Hand:')
	for card in dealer.cards:
		print(card)
	print('\n')
	print('Players Hand:')
	for card in player.cards:
		print(card)

def check_for_blackjack(player_hand, dealer_hand, player_chips):
	if dealer_hand.value == 21:
		player_score = dealer_blackjack(player_hand, dealer_hand, player_chips)
		winner_text = 'Dealer BLACKJACK!  Player Loses {}!'.format(str(bet))
	elif player_hand.value == 21:
		player_score = player_blackjack(player_hand, dealer_hand, player_chips)
		playing = False
	elif player_hand.value and dealer_hand.value == 21:
		print('Player and Dealer BOTH have BLACKJACK! PUSH!')
		playing = False
	else:
		pass

def player_busts(player,dealer,chips):
	print('The player has ' + str(player.value))
	print('BUST!')
	player_score = chips.lose_bet()
	# if doubledown == True:
	# 	player_score = chips.lose_bet()
	return player_score

def player_wins(player,dealer,chips):
	print('The player has ' + str(player.value))
	print('The dealer has ' + str(dealer.value))
	print('Player Wins!')
	player_score = chips.win_bet()
	# if doubledown == True:
	# 	player_score = chips.win_bet()
	return player_score

def player_blackjack(player,dealer,chips):
	print('The player has BLACKJACK!')
	player_score = chips.blackjack()
	return player_score

def dealer_busts(player,dealer,chips):
	print('The dealer has ' + str(dealer.value))
	print('Dealer BUST!  Player Wins!')
	player_score = chips.win_bet()
	# if doubledown == True:
	# 	player_score = chips.win_bet()
	return player_score
	
def dealer_wins(player,dealer,chips):
	print('The player has ' + str(player.value))
	print('The dealer has ' + str(dealer.value))
	print('Dealer Wins!')
	player_score = chips.lose_bet()
	# if doubledown == True:
	# 	player_score = chips.lose_bet()
	return player_score

def dealer_blackjack(player,dealer,chips):
	print('The dealer has BLACKJACK!')
	player_score = chips.lose_bet()
	return player_score
	
def determine_winner(player_hand, dealer_hand, player_chips):
	# Run different winning scenarios
	if dealer_hand.value > 21:
		player_score = dealer_busts(player_hand, dealer_hand, player_chips)
		winner_text = 'Dealer BUST!  Player Wins {}!'.format(str(player_chips.bet))
	elif dealer_hand.value > player_hand.value:
		player_score = dealer_wins(player_hand, dealer_hand, player_chips)
		winner_text = 'Dealer WINS!  Player Loses {}!'.format(str(player_chips.bet))
	elif dealer_hand.value < player_hand.value:
		player_score = player_wins(player_hand, dealer_hand, player_chips)
		winner_text = 'Player WINS!  Player Wins {}!'.format(str(player_chips.bet))
	else:
		winner_text = 'PUSH!  No winner!'
	return winner_text

def handle_blackjack(player_hand, dealer_hand, player_chips):
	if player_hand.value == 21 or dealer_hand.value == 21:
		if player_hand.value == 21 and dealer_hand.value == 21:
			winner_text = 'Player and Dealer BOTH have BLACKJACK! PUSH!'
		elif dealer_hand.value == 21:
			player_score = dealer_blackjack(player_hand, dealer_hand, player_chips)
			winner_text = 'Dealer BLACKJACK!  Player Loses {}!'.format(str(player_chips.bet))
		elif player_hand.value == 21:
			player_score = player_blackjack(player_hand, dealer_hand, player_chips)
			winner_text = 'Player BLACKJACK!  Player Wins {}!'.format(str(player_chips.bet * 1.5))
		return winner_text
	return ''

##############################

def draw_card(card, card_num, player_position, hide_card):
	if hide_card == True:
		card_image = CARDBACK_IMAGE
	else:
		card_image = pygame.image.load(os.path.join('.\images\cards', '{}{}.png'.format(CARD_MAP['suits'][card.suit], CARD_MAP['ranks'][card.rank])))
	WIN.blit(card_image, (FIRST_CARD[0] + (25 * card_num), FIRST_CARD[1] + player_position + (25 * card_num)))

def draw_window(player_hand, dealer_hand, player_chips, bet, dealer_show, winner_text, _state):
	WIN.fill(GREEN)
	pygame.draw.rect(WIN, BLACK, BUTTON_AREA)
	draw_bet = BET_FONT.render(str(bet), 1, WHITE)
	WIN.blit(draw_bet, BET_POS)
	draw_player_chips = PLAYER_CHIPS_FONT.render('Chips: '+str(player_chips.total), 1, WHITE)
	WIN.blit(draw_player_chips, PLAYER_CHIPS_POS)

	if _state == 'taking bets':
		WIN.blit(UP_IMAGE, UP_POS)
		WIN.blit(DOWN_IMAGE, DOWN_POS)
		WIN.blit(HIT_GREY_IMAGE, HIT_POS)
		WIN.blit(STAND_GREY_IMAGE, STAND_POS)
		WIN.blit(DD_GREY_IMAGE, DD_POS)
		WIN.blit(SPLIT_GREY_IMAGE, SPLIT_POS)
		draw_winner_text = WINNER_FONT.render(str(winner_text), 1, WHITE)
		WIN.blit(draw_winner_text, WINNER_POS)
		WIN.blit(DEAL_IMAGE, DEAL_POS)

	elif _state == 'playing':
		WIN.blit(UP_GREY_IMAGE, UP_POS)
		WIN.blit(DOWN_GREY_IMAGE, DOWN_POS)
		WIN.blit(HIT_IMAGE, HIT_POS)
		WIN.blit(STAND_IMAGE, STAND_POS)
		WIN.blit(DD_IMAGE, DD_POS)
		WIN.blit(SPLIT_GREY_IMAGE, SPLIT_POS)
		draw_winner_text = WINNER_FONT.render(str(winner_text), 1, WHITE)
		WIN.blit(draw_winner_text, WINNER_POS)
		WIN.blit(DEAL_GREY_IMAGE, DEAL_POS)
		# Handle cards
		pc = 0
		for card in player_hand.cards:
			draw_card(card, pc, 200, hide_card=False)
			pc += 1

		dc = 0
		for card in dealer_hand.cards:
			if (dc == 0) and (dealer_show == False):
				draw_card(card, dc, 0, hide_card=True)
			else:
				draw_card(card, dc, 0, hide_card=False) 
			dc += 1

	pygame.display.update()

def main(player_chips):

	player_score = player_chips.total
	doubledown = False
	clock = pygame.time.Clock()
	run = True
	_state = 'taking bets' 
	bet = 0
	dealer_show = False
	winner_text = ''

	# Create & shuffle the deck, deal two cards to each player
	deck = Deck()
	deck.shuffle()
	
	#setup the hands for Player and Dealer
	player_hand = Hand()
	player_hand.add_card(deck.deal())
	player_hand.add_card(deck.deal())
	
	dealer_hand = Hand()
	dealer_hand.add_card(deck.deal())
	dealer_hand.add_card(deck.deal())

	# GAME LOOP
	while run:
		clock.tick(FPS)
		mouse = pygame.mouse.get_pos()

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
				pygame.quit()

			if _state == 'taking bets':	
				if event.type == pygame.MOUSEBUTTONDOWN:
					# Clicked on the Up Button 
					if UP_BUTTON.collidepoint((mouse[0], mouse[1])):
						if player_score > bet:
							bet += 1
					# Clicked on the Down Button 
					if DOWN_BUTTON.collidepoint((mouse[0], mouse[1])):
						if bet > 0:
							bet -= 1
					# Clicked on Deal Button 
					if DEAL_BUTTON.collidepoint((mouse[0], mouse[1])):
						if bet == 0:
							winner_text = "Place your bet!"
						else:
							player_chips.bet = bet
							_state = 'playing'
							winner_text = handle_blackjack(player_hand, dealer_hand, player_chips)
							if 'BLACKJACK' in winner_text:
								dealer_show = True
								draw_window(player_hand, dealer_hand, player_chips, bet, dealer_show, winner_text, _state)
								# Inform Player of their chips total 
								print('\nYou have ${}'.format(player_chips.total))
								time.sleep(3)
								run = False
								

			if _state == 'playing':
				if event.type == pygame.MOUSEBUTTONDOWN:
					# Clicked on the Hit Button 
					if HIT_BUTTON.collidepoint((mouse[0], mouse[1])):
						# player_hand.add_card(deck.deal())
						player_hand = hit(deck, player_hand)
						if player_hand.value > 21:
							player_score = player_busts(player_hand, dealer_hand, player_chips)
							winner_text = 'Player BUST!  Player Loses {}!'.format(str(bet))
							dealer_show = True
							draw_window(player_hand, dealer_hand, player_chips, bet, dealer_show, winner_text, _state)
							# Inform Player of their chips total 
							print('\nYou have ${}'.format(player_chips.total))
							time.sleep(3)
							run = False

					# Clicked on the Stand Button
					if STAND_BUTTON.collidepoint((mouse[0], mouse[1])):
						# Play Dealer's hand until Dealer reaches 17
						if player_hand.value < 21 and dealer_hand.value < 21:
							while dealer_hand.value < 17:
								dealer_hand = hit(deck, dealer_hand)
						winner_text = determine_winner(player_hand, dealer_hand, player_chips)
						dealer_show = True
						draw_window(player_hand, dealer_hand, player_chips, bet, dealer_show, winner_text, _state)
						# Inform Player of their chips total 
						print('\nYou have ${}'.format(player_chips.total))
						time.sleep(3)
						run = False

		draw_window(player_hand, dealer_hand, player_chips, bet, dealer_show, winner_text, _state)

	main(player_chips)


if __name__ == "__main__":
	# Set up the Player's chips
	player_score = 100
	player_chips = Chips(player_score)
	main(player_chips)
