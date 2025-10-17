#!/usr/bin/env python

import math
import random
import numpy as np
import copy
from collections import Counter


class Card():
	def __init__(self):
		# A card has the following properties:
		# A figure: from 2 to 10 or Jack, Queen, King, Ace
		# An associated value: from 2 to 14
		# A color: Heart, Spikes, Clubs, Diamonds
		# A name
		# A pictogram (TODO - front end)

		self.name: str
		self.figure: str
		self.color: str 
		self.value : int 
	
	def init_figure_and_name(self):
		value_to_string={
			2: "Two",
			3: "Three",
			4: "Four",
			5: "Five",
			6: "Six",
			7: "Seven",
			8: "Eight",
			9: "Nine",
			10: "Ten",
			11: "Jack",
			12: "Queen",
			13: "King",
			14: "Ace"}
			
		self.figure = value_to_string[self.value]
		self.name = ' '.join([self.figure,"of",self.color])

class deckOfCards():
	def __init__(self):
		self.deck= []
		self.init_deck()
	
	def init_deck(self):
		for color in ["Heart", "Spikes", "Clubs", "Diamonds"]:
			for i in range (2,15):
				cardObject = Card()
				cardObject.value = i
				cardObject.color = color
				cardObject.init_figure_and_name()

				self.deck.append(cardObject)

	def shuffle_deck(self):
		random.shuffle(self.deck)
	
	def draw(self,n):
		cards = []
		for i in range(n):
			cards.append(self.deck.pop())

		return cards

	def display_deck(self):
		print("\nDeck:\n",[card.name for card in self.deck])
		print("Deck size:",len(self.deck))

class PokerRules():
	def __init__(self):
		self.cards_on_table: list
		self.small_blind: int
		self.big_blind: int
		self.pot: int

	def init_table(self, players):
		self.players = players
		self.cards_on_table = []
		self.small_blind = 5
		self.big_blind = 10
		self.pot = 0

	def betting_round(self):
		# Handles all bet rules, pot, blinds, and bet increase

		for player in self.players:
			player.bet = 10
			player.money -= player.bet

			# while all players are either out of game or have the same bets
			# print(player.name,"'s bet:")
			# player.bet = input()
			# while player.bet < self.big_blind:
				# print("Invalid bet, minimum is",self.big_blind)
				# print(player.name,"'s bet:")
				# player.bet = input()

	def bets_to_pot(self):
		for player in self.players:
			self.pot += player.bet
			player.bet = 0

	# @staticmethod
	# def is_straight_flush(cards):
	# 	pass

	# @staticmethod
	# def is_straight(cards):
	# 	# print('cards:', cards)
	# 	# remove redundent cards
	# 	cards_list = copy.deepcopy(cards)
	# 	for i in range(len(cards)-1):
	# 		if cards[i].value == cards[i+1].value:
	# 			cards_list.remove(cards_list[i+1])

	# 	cards_values_list = [card.value for card in cards_list]
	# 	cards_color_list = [card.color for card in cards_list]

	# 	print([card.name for card in cards_list])
	# 	print(cards_values_list)
	# 	print(cards_color_list)
		
	# 	# Ace low straight
	# 	if cards_values_list[:4]==[2,3,4,5] and 14 in cards_values_list:
	# 		return True, [cards_list[-1]] + cards_list[:4]
		
	# 	# while len(cards)>=5:
	# 	# 	# print('cards:', cards)
	# 	# 	for i in range(4):
	# 	# 		# comparing highest cards (to get highest straight)
	# 	# 		if cards[4-i-1] != cards[4-i]-1:
	# 	# 			# not a straight
	# 	# 			cards.pop()		# remove highest value
	# 	# 			break

	# 	# 	# if all cards values follow each other: straight (i.e., no break in for loop)
	# 	# 	else: 
	# 	# 		return True, cards[-5:]
		
	# 	# # Exhausted list
	# 	# return False, []

	@staticmethod
	def is_straight(cards):
		# Checks if straight, straight flush, or royal flush
		# input: 
		# - sorted_cards: list of 7 sorted cards
		# output: 
		# - output_cards: list either empty or five straight cards
		# - straight_type: int corresponding to type of straight (0 is none, 1 straight, 2 straight flush, 3 royal)
		sorted_cards = sorted(cards, key=lambda card: card.value)
		sorted_cards_values = [card.value for card in sorted_cards]
		mem_index_list = []

		'''
		Behaviour: 
		- Starting at the left of the list len(sorted_cards_values) - k, k = 1
		- Memorize the starting index in index
		- Initialize a counter unit_cnt to 1, to count the number of unique cards encountered
		- Initialize a counter cnt to 1, to count the number of cards in each possible straights
		- Parsing the list from right to left. As long as each value are successive (i.e value at [i]-1 == value at [i-1]), or the same
		increment cnt. If the values are the same, continue but without parsing cnt.
		- If two cards are apart by more than 1 point, two choices:
			1) cnt >= 5 indicates the presence of at least 1 straight from this index (5 unique cards or more that follow each others).
			In this case the couple (index, cnt) is memorized in mem_index_list.
			2) cnt < 5 : no possiblity for a straight, simple break.

		- Repeat for index = 6, 5, 4. Lower than 4, no straight is possible.

		Note: a cnt = 5 is not enough to stop the program because of the possiblity of a lower straight to be a flush.
		Example: [2 of spade, 3 of spade, 4 of spade, 5 of spade, 6 of spade, 7 of spade, 8 of heart]
		In this example, a lower straight (from 2 to 7) constitutes a flush, which is better than the higher straight (from 3 to 8)
		'''

		for index in range(6,3,-1):
			# print('0 index:', index)
			cnt = 1
			unit_cnt = 1
			for i in range(index,0,-1):
				if sorted_cards_values[i] == sorted_cards_values[i-1]:
					cnt+=1 # same card values
					# print(i,':',sorted_cards_values[i],'-',sorted_cards_values[i-1],"mem:",index,"cnt:",cnt)
				elif sorted_cards_values[i]-1 == sorted_cards_values[i-1]:
					cnt+=1 # successive card values
					unit_cnt+=1
					# print(i,':',sorted_cards_values[i],'-',sorted_cards_values[i-1],"mem:",index,"cnt:",cnt)
				else:
					# non-successive cards
					# print(i,':',sorted_cards_values[i],'-',sorted_cards_values[i-1],"mem:",index,"cnt:",cnt)
					if unit_cnt >= 5:
						# only if there are at least 5 unique cards can there be a straight
						mem_index_list.append((index,cnt)) # memorize index and number or successive cards
					break
			if unit_cnt>=5:
				# in case the for loop completed without breaking out (straight from top to bottom)
				mem_index_list.append((index,cnt))
			
			# print(mem_index_list)
		
		'''
		Each element of mem_index_list is a couple (index position, size of straight)
		The next processing step extracts each straights and tests for flushes.
		If a flush is found, it is returned. Because we parse from high to low, we know the first flush to be found will be the highest.
		Else, we return the highest straight without doubles.
		'''

		if mem_index_list:
			# test for flushes
			for item in mem_index_list:
				output_cards = sorted_cards[item[0]-item[1]+1:item[0]+1]
				output_cards_colors = [card.color for card in output_cards]
				
				counts = Counter(output_cards_colors)
				# counts.most_common(1)[0][0] : top 1 most common color 
				# counts.most_common(1)[0][1] : number of element of top 1 most common color 
				
				if counts.most_common(1)[0][1] >=5:
					# found a flush !!
					output_cards = [card for card in output_cards if card.color==counts.most_common(1)[0][0]]
					if [card.value for card in output_cards] == [10,11,12,13,14]:
						# Royal flush !!
						return output_cards, 3
					else: 
						return output_cards, 2
		
			# no flush, return only the straight without duplicate values
			item = mem_index_list[0]
			tmp = sorted_cards[item[0]-item[1]+1:item[0]+1]
			output_cards = [tmp[0]]
			for i in range (1,len(tmp)):
				if tmp[i].value != tmp[i-1].value:
					output_cards.append(tmp[i])

			return output_cards, 1
		# no straight
		return [], 0
			

	def get_hand_value(self, player):
		# High card: single value of highest card
		# Pair: 2 cards of same value
		# Two pairs: two times 2 cards of the same value
		# Three of a kind: 3 cards of the same value
		# Straight: sequence of 5 cards in increasing value (Ace can precede 2 or follow up King, but not both), not of the same suit
		# straight: 5 cards of the same suit, not in sequential order	
		# Full House: Combination of three of a kind and a pair	
		# Four of a kind: Four cards of the same value	
		# Straight flush: Straight of the same suit	
		# Royal flush: Highest straight of the same suit	
		player_hand = player.hand
		cards = player_hand + self.cards_on_table
		print("Cards for",player.name)
		print([card.name for card in cards])
		
		# # DEBUG
		# deck = deckOfCards()
		# # cards = deck.deck[-9:-2]
		# # cards[2] = deck.deck[8]
		# # cards = deck.deck[:2] + deck.deck[5:10]
		# # cards[5] = deck.deck[25]
		# # cards.insert(0,deck.deck[25])
		# cards = deck.deck[8:13] + [deck.deck[38]] + [deck.deck[24]]
		straight_output, straight_type = self.is_straight(cards)
		if straight_type == 3:
			print(player.name,"has a Royal Flush:")
			print([card.value for card in straight_output])
		if straight_type == 2:
			print(player.name,"has a Straight Flush:")
			print([card.value for card in straight_output])
		
		# four of a kind

		# full house

		if straight_type == 1:
			print(player.name,"has a Straight:")
			print([card.name for card in straight_output])




	def display_table(self):
		print("Cards on table:")
		print([card.name for card in self.cards_on_table])

		print("\nPot:",self.pot)

		print("\nCurrent bets:")
		for player in self.players:
			print(player.name,":",player.bet)

class playerClass():
	def __init__(self):
		self.name:str
		self.hand: list
		self.money: int
		self.bet: int
		self.hand_value: str
	
	def create_player(self,name):
		self.name = name
		self.hand = []
		self.money = 5000 #TODO set as a global value (min_entry_fee)
		self.bet = 0
		self.hand_value = None

	def clear_hand(self):
		self.hand = []
		self.bet = 0
		self.hand_value = None
	
	def display_player_info(self):
		print(self.name,":")
		print("Hand:",[card.name for card in self.hand])
		print("Money: ", self.money)

if __name__=="__main__":
	# Init a deck of cards
	deck = deckOfCards()
	deck.shuffle_deck()

	# Init players
	# for now: hard set
	player_list = []
	for i in range(1,6):
		playerObject = playerClass()
		playerObject.create_player("Player "+str(i))
		player_list.append(playerObject)
	
	# print([vars(player) for player in player_list])

	game = PokerRules()
	while(1):
		# Setting up game
		game.init_table(player_list)

		# Distribute cards
		for player in player_list:
			player.hand = deck.draw(2)

		print(50*"-","Player Infos",50*"-")
		for player in player_list:
			player.display_player_info()

		# pre-flop
		print(50*"-","Pre-Flop",50*"-")
		game.betting_round()
		game.display_table()

		print("\nPlayer Infos:\n")
		for player in player_list:
			player.display_player_info()
		
		# flop
		print(50*"-","Flop",50*"-")
		game.bets_to_pot()
		game.cards_on_table=deck.draw(3)
		game.betting_round()


		game.display_table()
		deck.display_deck()

		print("\nPlayer Infos:\n")
		for player in player_list:
			player.display_player_info()


		# turn
		print(50*"-","Turn",50*"-")
		game.bets_to_pot()
		game.cards_on_table.append(deck.draw(1)[0])
		game.betting_round()


		game.display_table()
		deck.display_deck()

		print("\nPlayer Infos:\n")
		for player in player_list:
			player.display_player_info()

		# river
		print(50*"-","River",50*"-")
		game.bets_to_pot()
		game.cards_on_table.append(deck.draw(1)[0])
		game.betting_round()


		game.display_table()
		deck.display_deck()

		print("\nPlayer Infos:\n")
		for player in player_list:
			player.display_player_info()

		# showdown
		print(50*"-","Showdown",50*"-")
		for player in player_list:
			player.hand_value = game.get_hand_value(player)
			input()





		break

















# class deckOfCards():
# 	def __init__(self):
# 		# a card has a value between 1 and 13 represented by 4 bits and a color represented by 2 bit
# 		# e.g., the king of spade is 0b110000

# 		# self.values = np.arange(2,11)
# 		# self.heads = ['Jack', 'Queen', 'King', 'Ace']
# 		# self.colors = ['Diamonds', 'Clubs', 'Hearts', 'Spikes']
# 		self.values = np.arange(12)
	
# 	def build_deck(self):
# 		deck = []
# 		col = 0b00
# 		while col <= 0b11:
# 			for col in range(4):
# 				value = 0b000001
# 				while value < 14:
# 					print(bin(value))
# 					print(bin(col))
# 					print(bin (value<<2 + col))
# 					input()
# 					value += 1
# 				col += 1

# 					# deck.append((val<<2 + col))
# 					# print('\n')
# 					# print(bin(val))
# 					# print(bin(col))
# 					# print((bin(val<<2) + bin(col)))
# 					# input()

# 		return deck

# 	def lookup(b):
# 		# spade = 0x00, heart = 0x01, clubs = 0x10, diamond = 0x11
# 		value_mask = 0b111100
# 		color_mask = 0b000011
# 		return b & value_mask, b & color_mask

# deck_class = deckOfCards()
# print(deck_class.build_deck())



# 	def build_deck(self):
# 		deck = []
# 		for color in self.colors:
# 			for value in self.values:
# 				deck.append(str(value)+' of '+color)
			
# 			for head in self.heads:
# 				deck.append(str(head)+' of '+color)
# 		return deck

# 	def shuffle_deck(self, deck):
# 		random.shuffle(deck)
# 		return deck
	
# 	def draw(self, deck):
# 		card = deck.pop()
# 		# print(card)
# 		# print(50*'-',deck)
# 		# discard_pile.append(card)

# 		return deck, card
	
# class playerClass():
# 	def __init__(self,n):
# 		self.name='Player '+str(n) # Default
# 		self.hand = []
# 		self.money = 5000
# 		self.bet = 0

# 	def clear_hand(self):
# 		self.hand = []

# def display_player_status(player_list):
# 	for item in player_list:
# 		print(vars(item))

# def get_card_value(card):
# 	value_name = card.split(' of ')[0]

# 	if value_name in ['Jack', 'Queen', 'King', 'Ace']:
# 		if value_name == 'Jack':
# 			value = 11
# 		elif value_name == 'Queen':
# 			value = 12
# 		elif value_name == 'King':
# 			value = 13
# 		elif value_name == 'Ace':
# 			value = 14
# 	else:
# 		value = int(value_name) 
	
# 	return value

# def sort_hand(hand):
# 	# init sorted hand
# 	sorted_hand = ['15','15','15','15','15','15','15']
	
# 	# sort
# 	for i in range(7):
# 		for j in range(len(hand)):
# 			if get_card_value(hand[j])<get_card_value(sorted_hand[i]):
# 				sorted_hand[i]= hand[j]
# 		hand.remove(sorted_hand[i])
# 	# print('\nhand:',hand)
# 	# print('sorted_hand:',sorted_hand)

# 	return sorted_hand


# def is_straight_hand(hand):
# 	sorted_hand = sort_hand(hand)
# 	sorted_hand= ['8 of Clubs', '8 of Hearts', '10 of Hearts', 'Jack of Hearts', 'Queen of Clubs', 'King of Hearts', 'Ace of Diamonds']
	
# 	print('sorted_hand:',sorted_hand)
# 	flags = [True, True, True]

# 	for i in range(0, 4):
# 		if not get_card_value(sorted_hand[i])+1==get_card_value(sorted_hand[i+1]):
# 			flags[0]= False
# 	for i in range(1, 5):
# 		if not get_card_value(sorted_hand[i])+1==get_card_value(sorted_hand[i+1]):
# 			flags[1]= False
# 	for i in range(2, 6):
# 		if not get_card_value(sorted_hand[i])+1==get_card_value(sorted_hand[i+1]):
# 			flags[2]= False

# 	if True in flags:
# 		return True
# 	else:
# 		return False
	
# 	# For now returns if there is a straight but since the valeus are calculated over 5 cards (not 7) 
# 	# need it to check for the highest straight





# def get_hand_values(hand):
# 	# High card: single value of highest card
# 	# Pair: 2 cards of same value
# 	# Two pairs: two times 2 cards of the same value
# 	# Three of a kind: 3 cards of the same value
# 	# Straight: sequence of 5 cards in increasing value (Ace can precede 2 or follow up King, but not both), not of the same suit
# 	# straight: 5 cards of the same suit, not in sequential order	
# 	# Full House: Combination of three of a kind and a pair	
# 	# Four of a kind: Four cards of the same value	
# 	# Straight flush: Straight of the same suit	
# 	# Royal flush: Highest straight of the same suit	
	
# 	# print(is_straight_hand(hand))

# 	if is_straight_hand(hand):
# 		# Check for Royal, i.e if 1st is 8
# 		# for i in range(len(sorted_hand)-1):
# 		# 	if not get_card_value(sorted_hand[i])+1==get_card_value(sorted_hand[i+1]):
# 		# 		return False
# 	# return True








# deck_fct = deckOfCards()
# deck = deck_fct.build_deck()
# deck = deck_fct.shuffle_deck(deck)
# print(deck)

# #TODO: try/exept
# nbr_players = int(input('number of players:'))
# assert int(nbr_players) < 11 

# player_list=[]
# for n in range(nbr_players):
# 	player_list.append(playerClass(n+1))

# display_player_status(player_list)
# table = []


# # Dealing
# for i in range (2):
# 	for player in player_list:
# 		deck, card = deck_fct.draw(deck) 
# 		player.hand.append(card)
# print('deck_size:',len(deck))
# display_player_status(player_list)
# # TODO: Pre-flop

# # Flop
# for i in range(3):
# 	deck, card = deck_fct.draw(deck)
# 	table.append(card)
# print('Table:', table)

# # TODO: Betting 

# # Turn
# deck, card = deck_fct.draw(deck)
# table.append(card)
# print('Table:', table)

# # TODO: Betting 

# # River
# deck, card = deck_fct.draw(deck)
# table.append(card)
# print('Table:', table)

# # Showdown
# for player in player_list:
# 	total_cards = table + player.hand
# 	print(player.name, ':', total_cards)
# 	# input()
# 	get_hand_values(total_cards)
# 	input()	
	
	
		

