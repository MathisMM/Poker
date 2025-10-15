#!/usr/bin/env python

import math
import random
import numpy as np

class Card():
	def __init__(self):
		# A card has the following properties:
		# A figure: from 2 to 10 or Jack, Queen, King, Ace
		# An associated value: from 2 to 14
		# A color: Heart, Spikes, Clubs, Diamonds
		# A name
		# A pictogram (later: TODO)

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

	def display_deck(self):
		for card in self.deck:
			print(card.name)

	def shuffle_deck(self):
		random.shuffle(self.deck)
	
	def draw(self):
		card = self.deck.pop()
		# print(card)
		# print(50*'-',deck)
		# discard_pile.append(card)

		return deck, card

class PokerRules():
	def __init__():
		pass
	def bets_handler(self):
		# Handles all bet rules, pot, blinds, and bet increase
		# also handles betting rounds between plays
		pass
	def plays(self):
		# handles reveal of cards (flop, turn, river, showdown)
		pass
	def get_hand_value(self):
		pass

class playerClass():
	def __init__(self,n):
		self.name:str
		self.hand: list
		self.money: int
		# self.bet: int
	
	def create_player(self,name):
		self.name = name
		self.hand = []
		self.money = 5000 #TODO set as a global value
		# self.bet = 0

	def clear_hand(self):
		self.hand = []

if __name__=="__main__":
	deck = deckOfCards()
	deck.shuffle_deck()


















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
# 	# Flush: 5 cards of the same suit, not in sequential order	
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
	
	
		

