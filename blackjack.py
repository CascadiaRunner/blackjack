import random
from IPython.display import clear_output

# Globals
suits = ('♠', '♦', '♥', '♣')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight',\
		 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7,\
		  'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10, 'Queen':10, 'King':10,\
		  'Ace':11}

playing = True
player_score = 100
doubledown = False

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


def take_bet(chips):
	print('You have ${}'.format(chips.total))
	while True:
		try:
			chips.bet = int(input('How much would you like to bet? '))
			
		
		except TypeError:
			print('Please enter a valid number!')
			continue
			
		else:
			if chips.bet > chips.total:
				print('You only have {} left!'.format(chips.total))
				continue

			else:
				break

def hit(deck,hand):
	
	single_card = deck.deal()
	print(single_card)
	hand.add_card(single_card)
	hand.adjust_for_ace()

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

def player_busts(player,dealer,chips):
	print('The player has ' + str(player.value))
	print('BUST!')
	player_score = chips.lose_bet()
	if doubledown == True:
		player_score = chips.lose_bet()
	return player_score

def player_wins(player,dealer,chips):
	print('The player has ' + str(player.value))
	print('The dealer has ' + str(dealer.value))
	print('Player Wins!')
	player_score = chips.win_bet()
	if doubledown == True:
		player_score = chips.win_bet()
	return player_score

def player_blackjack(player,dealer,chips):
	print('The player has BLACKJACK!')
	player_score = chips.blackjack()
	return player_score

def dealer_busts(player,dealer,chips):
	print('The dealer has ' + str(dealer.value))
	print('Dealer BUST!  Player Wins!')
	player_score = chips.win_bet()
	if doubledown == True:
		player_score = chips.win_bet()
	return player_score
	
def dealer_wins(player,dealer,chips):
	print('The player has ' + str(player.value))
	print('The dealer has ' + str(dealer.value))
	print('Dealer Wins!')
	player_score = chips.lose_bet()
	if doubledown == True:
		player_score = chips.lose_bet()
	return player_score

def dealer_blackjack(player,dealer,chips):
	print('The dealer has BLACKJACK!')
	player_score = chips.lose_bet()
	return player_score
	
def push(player,dealer):
	print('The player has ' + str(player.value))
	print('The dealer has ' + str(dealer.value))
	print('Push!')

if __name__ == "__main__":
# GAME LOOP
	while True:
		# Print an opening statement
		print("Welcome to Chris' BlackJack v1.0")
		
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
			
		# Set up the Player's chips
		player_chips = Chips(player_score)
		
		# Prompt the Player for their bet
		take_bet(player_chips)
		
		# Show cards (but keep one dealer card hidden)
		show_some(player_hand,dealer_hand)
		
		#check for blackjack
		if dealer_hand.value == 21:
			player_score = dealer_blackjack(player_hand, dealer_hand, player_chips)
			playing = False
		elif player_hand.value == 21:
			player_score = player_blackjack(player_hand, dealer_hand, player_chips)
			playing = False
		elif player_hand.value and dealer_hand.value == 21:
			print('Player and Dealer BOTH have BLACKJACK! PUSH!')
			playing = False
		else:
			pass
		
		while playing: # recall this variable from our hit_or_stand function
			
			# Prompt for Player to Hit or Stand
			hit_or_stand(deck,player_hand,player_chips)
		
			# If player's hand exceeds 21, run player_busts() and break out of loop
			if player_hand.value > 21:
				player_score = player_busts(player_hand, dealer_hand, player_chips)
				break

		# If Player hasn't busted, play Dealer's hand until Dealer reaches 17
		if player_hand.value < 21 and dealer_hand.value < 21:
		
			while dealer_hand.value < 17:
				print("Dealer Hits")
				hit(deck, dealer_hand)
			
			# Show all cards
			show_all(player_hand, dealer_hand)
			
			# Run different winning scenarios
			if dealer_hand.value > 21:
				player_score = dealer_busts(player_hand, dealer_hand, player_chips)
			elif dealer_hand.value > player_hand.value:
				player_score = dealer_wins(player_hand, dealer_hand, player_chips)
			elif dealer_hand.value < player_hand.value:
				player_score = player_wins(player_hand, dealer_hand, player_chips)
			else:
				push(player_hand, dealer_hand)
		
		# Inform Player of their chips total 
		print('\nYou have ${}'.format(player_chips.total))
		# Ask to play again
		new_game = input('Would you like to player another hand? Y or N')
						
		if new_game[0].lower() == 'y':
			playing = True
			doubledown = False
			clear_output()
			continue
		else:
			print('Thanks for playing!')
			break
