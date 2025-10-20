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
		output_cards = []
		straight_type = 0

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
						straight_type = 3
						break
					else: 
						straight_type = 2
						break
		
			# no flush, return only the straight without duplicate values
			if not straight_type:
				item = mem_index_list[0]
				tmp = sorted_cards[item[0]-item[1]+1:item[0]+1]
				output_cards = [tmp[0]]
				for i in range (1,len(tmp)):
					if tmp[i].value != tmp[i-1].value:
						output_cards.append(tmp[i])
				
				straight_type = 1
		
		# Testing for Ace low / wheel. Skipped if we already found a higher flush
		if all(elem in sorted_cards_values for elem in [2,3,4,5,14]) and straight_type<2:
			print("found ace low")
			# Ace low found:
			ace_low_cards = [item for item in sorted_cards if item.value in [2,3,4,5,14]]
			counts = Counter([card.color for card in ace_low_cards])
			
			if counts.most_common(1)[0][1] >=5:
				# found a flush !! Note: Royal flush is impossible
				output_cards = [card for card in ace_low_cards if card.color==counts.most_common(1)[0][0]]
				straight_type = 2
			elif not straight_type: # did not find another straight earlier
				tmp = [ace_low_cards[0]]
				for i in range (1,len(ace_low_cards)):
					if ace_low_cards[i].value != ace_low_cards[i-1].value:
						tmp.append(ace_low_cards[i])
				output_cards = tmp
				straight_type = 1

		# no straight
		return output_cards, straight_type
			
	def get_hand_value(self, player):
		# High card: single value of highest card
		# Pair: 2 cards of same value
		# Two pairs: two times 2 cards of the same value
		# Three of a kind: 3 cards of the same value
		# Straight: sequence of 5 cards in increasing value (Ace can precede 2 or follow up King, but not both), not of the same suit
		# Full House: Combination of three of a kind and a pair	
		# Four of a kind: Four cards of the same value	
		# Straight flush: Straight of the same suit	
		# Royal flush: Highest straight of the same suit	
		player_hand = player.hand
		cards = player_hand + self.cards_on_table
		hand=[]
		hand_val = 0
		
		
		# # DEBUG
		deck = deckOfCards()
		# cards = deck.deck[-9:-2] # regular straight
		# cards[2] = deck.deck[8] # add to regular to make non-straight
		# cards = deck.deck[:2] + deck.deck[5:10] # high straight
		# cards = deck.deck[8:13] + [deck.deck[38]] + [deck.deck[24]] # straight + royal flush
		# cards = deck.deck[:4] + [deck.deck[25]]+ [deck.deck[50]] + [deck.deck[13]] # Ace low straight
		# cards = deck.deck[:4] + [deck.deck[25]]+ [deck.deck[50]] + [deck.deck[12]] # Ace low flush
		# cards = deck.deck[:5] + [deck.deck[25]] + [deck.deck[12]] # Ace low flush + straight
		# cards = deck.deck[:3] + [deck.deck[11]] + [deck.deck[24]] + [deck.deck[50]] + [deck.deck[37]] # four of a kind
		# cards = deck.deck[:3] + [deck.deck[27]] + [deck.deck[24]] + [deck.deck[50]] + [deck.deck[37]] # Full house
		# cards = [deck.deck[0]] + [deck.deck[13]]+ [deck.deck[26]]+ [deck.deck[28]] \
		# 	+ [deck.deck[24]] + [deck.deck[50]] + [deck.deck[37]] # two threes of a kind (house)
		# cards = [deck.deck[1]] + [deck.deck[12]]+ [deck.deck[26]]+ [deck.deck[28]] \
		# 	+ [deck.deck[24]] + [deck.deck[50]] + [deck.deck[37]] # three of a kind
		# cards = [deck.deck[0]] + [deck.deck[13]]+ [deck.deck[28]]+ [deck.deck[28]] \
		# 	+ [deck.deck[25]] + [deck.deck[50]] + [deck.deck[38]] # three pairs
		# cards = [deck.deck[5]] + [deck.deck[14]]+ [deck.deck[28]]+ [deck.deck[28]] \
		# 	+ [deck.deck[25]] + [deck.deck[50]] + [deck.deck[38]] # two pairs
		# cards = [deck.deck[5]] + [deck.deck[19]]+ [deck.deck[32]]+ [deck.deck[28]] \
		# 	+ [deck.deck[25]] + [deck.deck[50]] + [deck.deck[40]] # single pair
		# cards = [deck.deck[5]] + [deck.deck[0]]+ [deck.deck[32]]+ [deck.deck[28]] \
		# 	+ [deck.deck[25]] + [deck.deck[50]] + [deck.deck[40]] # High card
		cards_values = [card.value for card in cards]
		cards_colors = [card.color for card in cards]

		print("Cards for",player.name)
		print([card.name for card in cards])
		
		# Flushes
		hand, straight_hand_type = self.is_straight(cards)
		if straight_hand_type == 3:
			print(player.name,"has a Royal Flush:")
			hand_val = 8
			return hand, hand_val

		elif straight_hand_type == 2:
			print(player.name,"has a Straight Flush:")
			hand_val = 7
			return hand, hand_val
		
		# Four of a kind
		value_counts = Counter(cards_values)
		if value_counts.most_common(1)[0][1] == 4:
			hand = [card for card in cards if card.value == value_counts.most_common(1)[0][0]]
			print(player.name,"has Four of a Kind:")
			hand_val = 6
			return hand, hand_val

		# Full house
		#TODO: use case 3 - 2 - 2 => need to take the highest pair here 
		#TODO: priviledge full house to three of a kind if 3 - 3 
		elif value_counts.most_common(2)[0][1] == 3 and value_counts.most_common(2)[1][1]>=2:
			if value_counts.most_common(2)[1][1]==3:
				# Full house with double triple cards
				hand = [card for card in cards \
						if card.value == value_counts.most_common(2)[0][0] \
						or card.value == value_counts.most_common(2)[1][0]]
				if value_counts.most_common(2)[0][0] > value_counts.most_common(2)[1][0]:
					hand = hand[:-1]	 # remove last element to get 3 and 2 cards
				else:
					hand.remove(hand[2]) # remove third element to get 3 and 2 cards
			else:
				# second most common occurence is of 2 cards: regular house
				if value_counts.most_common(3)[1][0] > value_counts.most_common(3)[2][0]:
					hand = [card for card in cards \
							if card.value == value_counts.most_common(2)[0][0] \
							or card.value == value_counts.most_common(2)[1][0]]
				else:
					hand = [card for card in cards \
							if card.value == value_counts.most_common(1)[0][0] \
							or card.value == value_counts.most_common(3)[2][0]]
			print(player.name,"has a Full house:")
			hand_val = 5
			return hand, hand_val
		
		# Straight
		elif straight_hand_type == 1:
			print(player.name,"has a Straight:")
			hand_val = 4
			return hand, hand_val
		
		# Three of a kind
		elif value_counts.most_common(2)[0][1] == 3 and value_counts.most_common(2)[1][1] < 3: 
			# we want to avoid going here if there are 2 threes of a kind because that is a full house (use case described before).
			print(player.name,"has a Three of a kind:")
			hand = [card for card in cards if card.value == value_counts.most_common(1)[0][0]]
			hand_val = 3
			return hand, hand_val

		# Pairs
		pair_cnt = 0
		pairs_val = sorted([item[0] for item in value_counts.most_common(3) if item[1]==2])
		pair_cnt = len(pairs_val)
		
		if pair_cnt >= 2:
			print(player.name,"has Two Pairs:")	
			hand = [card for card in cards if card.value in pairs_val[-2:]]
			hand_val = 2
			return hand, hand_val

		elif pair_cnt == 1: 
			print(player.name,"has a Pair:")
			hand = [card for card in cards if card.value in pairs_val[-1:]]
			hand_val = 1
			return hand, hand_val
		
		# High card
		else:
			print(player.name,"has a High Card:")
			hand = [sorted(cards, key=lambda card: card.value)[-1]]
			hand_val = 0
			return hand, hand_val


			





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
		self.final_hand = list
		self.hand_value: str
	
	def create_player(self,name):
		self.name = name
		self.hand = []
		self.money = 5000 #TODO set as a global value (min_entry_fee)
		self.bet = 0
		self.hand_value = None
		self.final_hand=[]

	def clear_hand(self):
		self.hand = []
		self.bet = 0
		self.hand_value = None
		self.final_hand = []
	
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
			player.final_hand, player.hand_value = game.get_hand_value(player)
			print([card.name for card in player.final_hand])
			print('hand_val:',player.hand_value)
			input()

		break