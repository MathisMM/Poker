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

class DeckOfCards():
	def __init__(self):
		self.deck: list
		self.init_deck()
	
	def init_deck(self):
		self.deck=[]
		for color in ["Heart", "Spikes", "Clubs", "Diamonds"]:
			for i in range (2,15):
				cardObject = Card()
				cardObject.value = i
				cardObject.color = color
				cardObject.init_figure_and_name()

				self.deck.append(cardObject)

	def shuffle_deck(self):
		random.shuffle(self.deck)

	def reset_deck(self):
		self.init_deck()
		random.shuffle(self.deck)

	def draw(self,n):
		cards = []
		for i in range(n):
			cards.append(self.deck.pop())
		return cards

	def display_deck(self):
		print("\nDeck:\n",[card.name for card in self.deck])
		print("Deck size:",len(self.deck))

class PokerGame():
	def __init__(self):
		self.cards_on_table: list
		self.small_blind: int
		self.big_blind: int
		self.pot: int

	def init_game(self, players):
		self.players = players
		self.cards_on_table = []
		self.small_blind = 5
		self.big_blind = 10
		self.pot = 0
	
	def reset_table(self):
		self.cards_on_table = []
		self.pot = 0

	def init_blinds(self):
		self.players[-1].blind = "big_blind"
		self.players[-2].blind = "small_blind"
		self.players[-3].blind = "button"

	def rotate_blinds(self):
		self.players.insert(0,self.players.pop())
		if len(self.players)>2:
			self.players[-1].blind = "big_blind"
			self.players[-2].blind = "small_blind"
			self.players[-3].blind = "button"
			if len(self.players)>3:
				for i in range(4,len(self.players)+1):
					self.players[-i].blind = ""

		else:
			# final (1v1)
			self.players[0].blind = "small_blind"
			self.players[1].blind = "big_blind"

	def human_play(self, player):
		# Errors definition
		class InsufficientFundsError(Exception):
			pass
		class InvalidBetError(Exception):
			pass
		class InvalidBetInputError(Exception):
			pass

		# Decides to bet or fold:
		print("\nCurrent bet to match:",self.current_bet)
		print("Current player betted amount:",player.bet)
		print("Current player money:",player.money)
		print(player.name,"input decision:")
		print('1: Call')
		print('2: Raise')
		print('3: Fold')

		try:
			player_choice = input()

			# Call bet
			if player_choice == '1':
				print(player.name,"Checks") if self.current_bet==0 else print(player.name,"Calls")
				if player.money<self.current_bet:
					raise InsufficientFundsError("Insufficient funds. Go all in ? y/n")
				player.bet = self.current_bet	# update player bet if valid

			# Raise bet
			elif player_choice == '2':
				while True:
					print(player.name,"Opens") if self.current_bet==0 else print(player.name,"Raises")
					print("Input bet:")
					try :
						player.bet = int(input())	# set new bet
					except ValueError:
						print("Invalid input, must be a number")
						continue
					
					# Check player has enough money and that bet is valid (>= bid blind)
					if player.bet<self.big_blind:
						raise InvalidBetError ("Invalid bet. Bet needs to be at least the big blind ($%s)"%(self.big_blind))
					if player.money<player.bet:
						raise InsufficientFundsError("Insufficient funds. Go all in ? y/n")
					if player.money==player.bet:
						raise InsufficientFundsError("Go all in ? y/n")


					# if bet valid
					self.current_bet = player.bet	# update current highest bet
					break	# exit raise check loop
			
			# Fold
			elif player_choice == '3':
				player.status = "Folded" # update status
			
			else:
				raise InvalidBetInputError("Invalid input.")
			
			# if input valid
			return 1 # next player

		except (InvalidBetInputError, InvalidBetError) as e:
			print(f"Error: {e}")
			return 0 # re-prompt player
		except (InsufficientFundsError) as e:
			print(f"Error: {e}")
			while True:
				all_in_input = input()
				if all_in_input in ['y', 'Y']:
					player.bet = player.money
					self.current_bet = player.bet
					player.is_all_in = True
					break
				if all_in_input in ['n', 'N']:
					player.bet = 0
					break
				else:
					print("invalid input, please press 'y' or 'n'.")
			return 0 # re-prompt player
	
	def AI_play(self, player):
		# no security check for now (debug version)
		print(player.name,"Checks") if self.current_bet==0 else print(player.name,"Calls")
		player.bet = self.current_bet	# Current default behaviour: call all bet
		return 1 # next player

	def betting_round(self, round):
		# Handles betting system
		if round == 0:
			# pre-flop first betting round
			for player in self.players:
				if player.blind == "big_blind":
					player.bet = self.big_blind
				if player.blind == "small_blind":
					player.bet = self.small_blind
			self.current_bet = self.big_blind
		else:
			self.current_bet = 0	# allows for checks in later rounds 

		bet_flag = False # dummy flag to go through while loop at least once

		while (len(set([player.bet for player in self.players if player.status == "inGame"]))!=1) or (bet_flag==False): # while players have different bets
			# convert list of player bets into a set and checks set size. If set size == 1 => all bets are the same
			# [player.display_player_info() for player in self.players]
			for player in self.players:
				
				# break loop in case we started over because a player raised
				if len(set([player.bet for player in self.players if player.status == "inGame"]))==1 and bet_flag == True :
					break
				
				next_player = 0
				while not next_player:
					if player.is_all_in:
						print(player.name,"is already All-in.")
						break

					if player.is_human:
						next_player = self.human_play(player)

					if not player.is_human :
						next_player = self.AI_play(player)
				
				if len([player for player in self.players if player.status=="inGame"])==1:
					# Only 1 player in game, other have folded => early showdown
					return 1

			
			bet_flag = True # signal we went throught at least 1 round of betting
		
		return 0

	def bets_to_pot(self):
		# updates pot and player money
		for player in self.players:
			self.pot += player.bet
			player.money-=player.bet
			player.betting_hist.append(player.bet)
			player.bet = 0
	
	def get_winners(self):
		# Handles pot distribution at the end of a round
		# TODO: all in system (add a betting history, side pots)
		# TODO: all player fold
		# print(self.pot)
		# print([[card.name for card in player.hand] for player in self.players])
		# print([player.hand_value for player in self.players])
		
		ingame_players = [player for player in self.players if player.status == "inGame"]	# extracting player that have not folded
		player_hand_values = [player.hand_value for player in ingame_players]				# extracting players hand values
		high_hand = max(player_hand_values)													# highest hand value amongst players
		winners = [player for player in ingame_players if player.hand_value == high_hand]	# potential winners
		
		print('-')
		# print(player_hand_values)
		# print(high_hand)
		print([winner.name for winner in winners])
		print([sorted([card.value for card in player.final_hand]) for player in winners])

		if len(winners) > 1:
			# tie-breaker
			# for player in winners:
			if high_hand == 6:
				# In case of full house determining the highest of threes, than twos
				# Poker terminology: 
				# "Trips" (or "Set") => refers to the three of a kind part
				# "Pair" => refers to the two of a kind part.

				winners_high_cards = {player.name: Counter(card.value for card in player.final_hand).most_common(1)[0][0]
													for player in winners}	# extracting the Trips value for each players
				winners_highest_value = max(winners_high_cards.values())	# extracting highest trips value

				# Reducing winners_high_cards to those with the same trips value
				winners_high_cards = {name: value
									for name, value in winners_high_cards.items()
									if value == winners_highest_value}

				# filtering out the winners list, keeping only those with the same trips
				winners = [player for player in winners if player.name in winners_high_cards.keys()]
				
				# print('filtered by trips\n',[winner.name for winner in winners])

				# Repeat this process for the pairs
				if len (winners) > 1:
					winners_high_cards = {player.name: Counter(card.value for card in player.final_hand).most_common(2)[1][0]
														for player in winners}	# extracting the pair value for each players
					winners_highest_value = max(winners_high_cards.values())	# extracting highest pair value

					# Reducing winners_high_cards to those with the same pair value
					winners_high_cards = {name: value
										for name, value in winners_high_cards.items()
										if value == winners_highest_value}

					# filtering out the winners list, keeping only those with the same pair
					winners = [player for player in winners if player.name in winners_high_cards.keys()]

					# print('filtered by pairs\n',[winner.name for winner in winners])
				
				# If tie still not broken, use high pocket cards
				if len (winners) > 1:
					winners_high_cards = {player.name: [max(card.value for card in player.pocket)]
												for player in winners}	# extracting the highest pocket card value for each players
					
					winners_highest_value = max(winners_high_cards.values())

					# Reducing winners_high_cards to those with the same highest pocket card value
					winners_high_cards = {name: value
										for name, value in winners_high_cards.items()
										if value == winners_highest_value}

					# filtering out the winners list, keeping only those with the same highest pocket card value
					winners = [player for player in winners if player.name in winners_high_cards.keys()]
					
					# print('filtered by high\n',[winner.name for winner in winners])
			else:
				# for other hands, only need to check highest cards:
				
				winners_high_cards = {player.name: sorted([card.value for card in player.final_hand])[-1]
													for player in winners}	# extracting the highest card value for each players' hand
				
				winners_highest_value = max(winners_high_cards.values())	# extracting highest value amongst all players

				# Reducing winners_high_cards to those with the same high card value
				winners_high_cards = {name: value
									for name, value in winners_high_cards.items()
									if value == winners_highest_value}

				# filtering out the winners list, keeping only those with the same high card value
				winners = [player for player in winners if player.name in winners_high_cards.keys()]

				print('\nwinners after filtering with high card from final_hand:\n',[player.name for player in winners])

				# If tie still not broken, use high pocket cards
				if len (winners) > 1:
					winners_high_cards = {player.name: [max(card.value for card in player.pocket)]
												for player in winners}	# extracting the highest pocket card value for each players
					
					winners_highest_value = max(winners_high_cards.values())

					# Reducing winners_high_cards to those with the same highest pocket card value
					winners_high_cards = {name: value
										for name, value in winners_high_cards.items()
										if value == winners_highest_value}

					# filtering out the winners list, keeping only those with the same highest pocket card value
					winners = [player for player in winners if player.name in winners_high_cards.keys()]
				
				

		print('\nWinner(s):\n',[winner.name for winner in winners])
					
		return winners

	def split_pot(self, winners):
		if len(winners)==1:
			# single winner
			winners[0].money += self.pot
			self.pot = 0


	@staticmethod
	def is_straight(cards):
		# TODO: Ace straight is preceding or following a KING (functional issue)
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
		return output_cards[-5:], straight_type	#Note: only returning the highest 5 cards of the straight
			
	def get_hand_value(self, player):
		# High card: single value of highest card
		# Pair: 2 cards of same value
		# Two pairs: two times 2 cards of the same value
		# Three of a kind: 3 cards of the same value
		# Straight: sequence of 5 cards in increasing value (Ace can precede 2 or follow up King, but not both), not of the same suit
		# Flush: 5 cards of the same suit, not in sequential order
		# Full House: Combination of three of a kind and a pair	
		# Four of a kind: Four cards of the same value	
		# Straight flush: Straight of the same suit	
		# Royal flush: Highest straight of the same suit	
		player_hand = player.pocket
		cards = player_hand + self.cards_on_table
		hand=[]
		hand_val = 0
		
		
		# # DEBUG
		deck = DeckOfCards()
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
		value_counts = Counter(cards_values)
		color_counts = Counter(cards_colors)
		
		print("Cards for",player.name)
		print([card.name for card in cards])
		
		# Straight Flushes
		hand, straight_hand_type = self.is_straight(cards)
		if straight_hand_type == 3:
			print(player.name,"has a Royal Flush:")
			hand_val = 9
			return hand, hand_val

		elif straight_hand_type == 2:
			print(player.name,"has a Straight Flush:")
			hand_val = 8
			return hand, hand_val
		
		# Four of a kind
		if value_counts.most_common(1)[0][1] == 4:	# more than 4 is not possible
			hand = [card for card in cards if card.value == value_counts.most_common(1)[0][0]]
			print(player.name,"has Four of a Kind:")
			hand.sort(key=lambda x:x.value)	# order list
			hand_val = 7
			return hand, hand_val

		# Full house
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
				if value_counts.most_common(3)[2][1] == 2 : # checking if there are 2 pairs
					if value_counts.most_common(3)[1][0] > value_counts.most_common(3)[2][0]:
						# taking the highest ranking pair to form the full house
						hand = [card for card in cards \
								if card.value == value_counts.most_common(2)[0][0] \
								or card.value == value_counts.most_common(2)[1][0]]
					else:
						hand = [card for card in cards \
								if card.value == value_counts.most_common(1)[0][0] \
								or card.value == value_counts.most_common(3)[2][0]]
				else:
					hand = [card for card in cards \
								if card.value == value_counts.most_common(2)[0][0] \
								or card.value == value_counts.most_common(2)[1][0]]
			print(player.name,"has a Full house:")
			hand_val = 6
			return hand, hand_val
		
		# Flush / Color
		elif color_counts.most_common(1)[0][1]>=5:
			print(player.name,"has a Flush:")
			hand = [card for card in cards 
					if card.color == color_counts.most_common(1)[0][0]]
			hand.sort(key=lambda x:x.value)	# order list to output highest values
			hand_val = 5
			return hand[-5:], hand_val

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
			hand.sort(key=lambda x:x.value)	# order list
			return hand, hand_val

		# Pairs
		pair_cnt = 0
		pairs_val = sorted([item[0] for item in value_counts.most_common(3) if item[1]==2])
		pair_cnt = len(pairs_val)
		
		if pair_cnt >= 2:
			print(player.name,"has Two Pairs:")	
			hand = [card for card in cards if card.value in pairs_val[-2:]]
			hand_val = 2
			hand.sort(key=lambda x:x.value)	# order list
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

	def play(self, n_cards_to_distrib, round_name, round_n):
		print(50*'-',round_name,50*'-')
		game.cards_on_table.extend(deck.draw(n_cards_to_distrib))
		stop_game = game.betting_round(round_n)
		game.bets_to_pot()

		game.display_table()
		deck.display_deck()

		print("\nPlayer Infos:\n")
		print([player.display_player_info() for player in self.players])

		return stop_game
		

 
class playerClass():
	def __init__(self):
		self.name:str				# The name of the player
		self.pocket: list			# The two cards distributed to the player
		self.money: int				# The amount of money the player has
		self.bet: int				# The amount of money the player bets at each turn
		self.betting_hist: list		# History of a player's bet. Used when bets exceed a player's money (all in)
		self.is_all_in: bool		# All-in flag
		self.blind: str				# Big/Small blind or Button
		self.status: str			# inGame / Folded
		self.final_hand = list		# The final hand 
		self.hand_value: int		# The value of the final hand (ex: 0 for high card, 1 for pair, etc...)
		self.is_human: bool			# Stores if a player is human or AI (for later use)
	
	def create_player(self,name):
		self.name = name
		self.pocket = []
		self.money = 5000 #TODO set as a global value (min_entry_fee)
		self.bet = 0
		self.betting_hist = []
		self.is_all_in = False
		self.blind = ""
		self.status = "inGame"
		self.final_hand=[]
		self.hand_value = 0
		self.is_human = False

	def clear_hand(self):
		self.pocket = []
		self.bet = 0
		self.hand_value = None
		self.final_hand = []
	
	def display_player_info(self):
		print(self.name,":")
		print("Pocket Cards:",[card.name for card in self.pocket])
		print("Money:", self.money)
		print("Current bet:", self.bet)
		print("Blind:", self.blind)
		print("Status:", self.status)
		print("Human player ?:", self.is_human)
		print()

def unit_tests():
	# Init a deck of cards
	deck = DeckOfCards()
	'''
	Deck index:
	0 : Two of Heart
	1 : Three of Heart
	2 : Four of Heart
	3 : Five of Heart
	4 : Six of Heart
	5 : Seven of Heart
	6 : Eight of Heart
	7 : Nine of Heart
	8 : Ten of Heart
	9 : Jack of Heart
	10 : Queen of Heart
	11 : King of Heart
	12 : Ace of Heart

	13 : Two of Spikes
	14 : Three of Spikes
	15 : Four of Spikes
	16 : Five of Spikes
	17 : Six of Spikes
	18 : Seven of Spikes
	19 : Eight of Spikes
	20 : Nine of Spikes
	21 : Ten of Spikes
	22 : Jack of Spikes
	23 : Queen of Spikes
	24 : King of Spikes
	25 : Ace of Spikes

	26 : Two of Clubs
	27 : Three of Clubs
	28 : Four of Clubs
	29 : Five of Clubs
	30 : Six of Clubs
	31 : Seven of Clubs
	32 : Eight of Clubs
	33 : Nine of Clubs
	34 : Ten of Clubs
	35 : Jack of Clubs
	36 : Queen of Clubs
	37 : King of Clubs
	38 : Ace of Clubs

	39 : Two of Diamonds
	40 : Three of Diamonds
	41 : Four of Diamonds
	42 : Five of Diamonds
	43 : Six of Diamonds
	44 : Seven of Diamonds
	45 : Eight of Diamonds
	46 : Nine of Diamonds
	47 : Ten of Diamonds
	48 : Jack of Diamonds
	49 : Queen of Diamonds
	50 : King of Diamonds
	51 : Ace of Diamonds
	'''

	# Init players
	# for now: hard set
	player_list = []
	n_players = 3
	for i in range(n_players):
		playerObject = playerClass()
		playerObject.create_player("Player "+str(i+1))
		player_list.append(playerObject)

	# Setting up game
	game = PokerGame()
	game.init_game(player_list)
	game.init_blinds()

	def run_test_get_hand_value():
		# dummy bets:
		for i in range(4):
			game.betting_round(0)
			game.bets_to_pot()

		print("\nPlayer Infos:\n")
		print([player.display_player_info() for player in player_list])

		# showdown
		print(50*"-","Showdown",50*"-")
		for player in player_list:
			print()
			player.final_hand, player.hand_value = game.get_hand_value(player)
			print([card.name for card in player.final_hand])
			# print('hand_val:',player.hand_value)
	
		return [player.hand_value for player in player_list]

	def run_test_get_winner():
		# dummy bets:
		for i in range(4):
			game.betting_round(0)
			game.bets_to_pot()

		print("\nPlayer Infos:\n")
		print([player.display_player_info() for player in player_list])

		# showdown
		print(50*"-","Showdown",50*"-")
		for player in player_list:
			print()
			player.final_hand, player.hand_value = game.get_hand_value(player)
			print([card.name for card in player.final_hand])
			# print('hand_val:',player.hand_value)
	
		return game.get_winners()

	# ----------------------------------------UNIT TESTS----------------------------------------------- 
	# full house
	## 1 full house
	game.cards_on_table=[deck.deck[0]] + [deck.deck[2]] + [deck.deck[23]] + [deck.deck[17]] + [deck.deck[26]] #2-4-Q-6-2
	player_list[0].pocket = [deck.deck[13]] + [deck.deck[36]] #2-Q
	player_list[1].pocket = [deck.deck[24]] + [deck.deck[25]] #K-A
	player_list[2].pocket = [deck.deck[24]] + [deck.deck[25]] #K-A
	assert (run_test_get_winner() == [player_list[0]]), "Full house - test 1 failed."

	## 1 full house, other players have 3 of a kind
	game.cards_on_table=[deck.deck[0]] + [deck.deck[2]] + [deck.deck[13]] + [deck.deck[17]] + [deck.deck[26]] #2-4-2-6-2
	player_list[0].pocket = [deck.deck[17]] + [deck.deck[38]] #6-A
	player_list[1].pocket = [deck.deck[21]] + [deck.deck[5]]  #A-7
	player_list[2].pocket = [deck.deck[6]] + [deck.deck[3]]   #8-5
	assert (run_test_get_winner() == [player_list[0]]), "Full house - test 2 failed."
	
	## 2 full house, player 1 has a higher card
	game.cards_on_table=[deck.deck[0]] + [deck.deck[2]] + [deck.deck[13]] + [deck.deck[17]] + [deck.deck[26]] #2-4-2-6-2
	player_list[0].pocket = [deck.deck[17]] + [deck.deck[38]] #6-A
	player_list[1].pocket = [deck.deck[17]] + [deck.deck[5]]  #6-7
	player_list[2].pocket = [deck.deck[6]] + [deck.deck[3]]   #8-5
	assert (run_test_get_winner() == [player_list[0]]), "Full house - test 3 failed."
	
	## 2 full house, perfect tie
	game.cards_on_table=[deck.deck[0]] + [deck.deck[2]] + [deck.deck[13]] + [deck.deck[17]] + [deck.deck[26]] #2-4-2-6-2
	player_list[0].pocket = [deck.deck[17]] + [deck.deck[38]] #6-A
	player_list[1].pocket = [deck.deck[17]] + [deck.deck[38]] #6-A
	player_list[2].pocket = [deck.deck[6]] + [deck.deck[3]]   #8-5
	assert (run_test_get_winner() == [player_list[0],player_list[1]]), "Full house - test 4 failed."
	
	# straights
	## player 1 has a straight
	game.cards_on_table=[deck.deck[0]] + [deck.deck[14]] + [deck.deck[28]] + [deck.deck[3]] + [deck.deck[36]] #2-3-4-5-Q
	player_list[0].pocket = [deck.deck[17]] + [deck.deck[36]] #6-K
	player_list[1].pocket = [deck.deck[18]] + [deck.deck[36]] #7-K
	player_list[2].pocket = [deck.deck[6]] + [deck.deck[3]]   #8-5
	assert (run_test_get_winner() == [player_list[0]]), "Straights - test 1 failed."

	## player 1 and 2 have a straight or different heights
	game.cards_on_table=[deck.deck[14]] + [deck.deck[28]] + [deck.deck[3]] + [deck.deck[43]] + [deck.deck[36]] #3-4-5-6-Q
	player_list[0].pocket = [deck.deck[31]] + [deck.deck[36]] #7-K
	player_list[1].pocket = [deck.deck[0]] + [deck.deck[36]]  #2-K
	player_list[2].pocket = [deck.deck[6]] + [deck.deck[3]]   #8-5
	assert (run_test_get_winner() == [player_list[0]]), "Straights - test 2 failed."
	
	## players have straights and straight flushes
	game.cards_on_table=[deck.deck[1]] + [deck.deck[2]] + [deck.deck[3]] + [deck.deck[4]] + [deck.deck[36]] #3-4-5-6-Q
	player_list[0].pocket = [deck.deck[5]] + [deck.deck[36]]  #7-K
	player_list[1].pocket = [deck.deck[31]] + [deck.deck[36]] #2-K
	player_list[2].pocket = [deck.deck[41]] + [deck.deck[42]] #8-5
	assert (run_test_get_winner() == [player_list[0]]), "Straights - test 3 failed."

	# Flushes
	## player 1 has a flush
	game.cards_on_table=[deck.deck[1]] + [deck.deck[3]] + [deck.deck[8]] + [deck.deck[11]] + [deck.deck[36]] #3-5-10-K-Q
	player_list[0].pocket = [deck.deck[5]] + [deck.deck[36]]  #7-K
	player_list[1].pocket = [deck.deck[31]] + [deck.deck[36]] #2-K
	player_list[2].pocket = [deck.deck[41]] + [deck.deck[42]] #8-5
	assert (run_test_get_winner() == [player_list[0]]), "Flushes - test 1 failed."

	## multiple players have a flush, one has a higher flush
	game.cards_on_table=[deck.deck[1]] + [deck.deck[3]] + [deck.deck[8]] + [deck.deck[11]] + [deck.deck[36]] #3-5-10-K-Q
	player_list[0].pocket = [deck.deck[5]] + [deck.deck[12]]  #7-A
	player_list[1].pocket = [deck.deck[0]] + [deck.deck[2]]   #2-4
	player_list[2].pocket = [deck.deck[41]] + [deck.deck[42]] #8-5
	assert (run_test_get_winner() == [player_list[0]]), "Flushes - test 2 failed."

	# Pairs et al
	## one player has one pair
	game.cards_on_table=[deck.deck[1]] + [deck.deck[3]] + [deck.deck[8]] + [deck.deck[11]] + [deck.deck[36]] #3-5-10-K-Q
	player_list[0].pocket = [deck.deck[16]] + [deck.deck[39]] #5-2
	player_list[1].pocket = [deck.deck[26]] + [deck.deck[41]] #2-4
	player_list[2].pocket = [deck.deck[45]] + [deck.deck[38]] #8-A
	assert (run_test_get_winner() == [player_list[0]]), "Pairs et al - test 1 failed."

	## two players have one pair, player 1 has a higher one
	game.cards_on_table=[deck.deck[1]] + [deck.deck[2]] + [deck.deck[8]] + [deck.deck[11]] + [deck.deck[36]] #3-4-10-K-Q
	player_list[0].pocket = [deck.deck[42]] + [deck.deck[29]] #5-5
	player_list[1].pocket = [deck.deck[26]] + [deck.deck[39]] #2-2
	player_list[2].pocket = [deck.deck[45]] + [deck.deck[38]] #8-A
	assert (run_test_get_winner() == [player_list[0]]), "Pairs et al - test 2 failed."

	## two players have one pair, player 1 has two pairs
	game.cards_on_table=[deck.deck[1]] + [deck.deck[2]] + [deck.deck[8]] + [deck.deck[11]] + [deck.deck[36]] #3-4-10-K-Q
	player_list[0].pocket = [deck.deck[34]] + [deck.deck[50]] #10-K
	player_list[1].pocket = [deck.deck[21]] + [deck.deck[13]] #10-2
	player_list[2].pocket = [deck.deck[45]] + [deck.deck[38]] #8-A
	assert (run_test_get_winner() == [player_list[0]]), "Pairs et al - test 3 failed."

	## two players have one pair, player 1 has higher pocket card
	game.cards_on_table=[deck.deck[1]] + [deck.deck[2]] + [deck.deck[8]] + [deck.deck[11]] + [deck.deck[36]] #3-4-10-K-Q
	player_list[0].pocket = [deck.deck[34]] + [deck.deck[51]] #10-A
	player_list[1].pocket = [deck.deck[21]] + [deck.deck[13]] #10-2
	player_list[2].pocket = [deck.deck[45]] + [deck.deck[38]] #8-A
	assert (run_test_get_winner() == [player_list[0]]), "Pairs et al - test 4 failed."

	## one has a four of a kind
	game.cards_on_table=[deck.deck[3]] + [deck.deck[16]] + [deck.deck[34]] + [deck.deck[11]] + [deck.deck[36]] #5-5-10-K-Q
	player_list[0].pocket = [deck.deck[29]] + [deck.deck[42]] #5-5
	player_list[1].pocket = [deck.deck[37]] + [deck.deck[49]] #K-Q
	player_list[2].pocket = [deck.deck[0]] + [deck.deck[39]] #2-2
	assert (run_test_get_winner() == [player_list[0]]), "Pairs et al - test 5 failed."

	## one has a four of a kind, one has full house, another has three of a kind
	game.cards_on_table=[deck.deck[3]] + [deck.deck[16]] + [deck.deck[34]] + [deck.deck[10]] + [deck.deck[36]] #5-5-10-Q-Q
	player_list[0].pocket = [deck.deck[29]] + [deck.deck[42]] #5-5
	player_list[1].pocket = [deck.deck[37]] + [deck.deck[49]] #K-Q
	player_list[2].pocket = [deck.deck[0]] + [deck.deck[2]] #2-4
	assert (run_test_get_winner() == [player_list[0]]), "Pairs et al - test 6 failed."

	# High Card
	## one has a four of a kind, one has full house, another has three of a kind
	game.cards_on_table=[deck.deck[3]] + [deck.deck[15]] + [deck.deck[34]] + [deck.deck[10]] + [deck.deck[32]] #5-4-10-Q-8
	player_list[0].pocket = [deck.deck[50]] + [deck.deck[25]] #K-A
	player_list[1].pocket = [deck.deck[37]] + [deck.deck[26]] #K-2
	player_list[2].pocket = [deck.deck[0]] + [deck.deck[1]] #2-3
	assert (run_test_get_winner() == [player_list[0]]), "High - test 1 failed."

	print('All tests passed !')
		


if __name__=="__main__":
	tests = False
	if tests:
		unit_tests()
		exit()
	
	
	# Init a deck of cards
	deck = DeckOfCards()

	# Init players
	# for now: hard set
	player_list = []
	n_players = 3
	for i in range(n_players):
		playerObject = playerClass()
		playerObject.create_player("Player "+str(i+1))
		playerObject.is_human = True

		player_list.append(playerObject)

	# player_list[0].is_human = True #DEBUG TODO: dynamic selection + naming

	# print([vars(player) for player in player_list])

	# Setting up game
	game = PokerGame()
	game.init_game(player_list)
	game.init_blinds()
	cnt_games = 0 # counts the number of games to update the blinds

	while(1):
		# reset table cards and deck of cards (re-shuffled)
		deck.reset_deck()
		game.reset_table()
		stop_game = 0
		cnt_games += 1		
		
		# Distribute cards
		for player in player_list:
			player.pocket = deck.draw(2)

		print(50*"-","Player Infos",50*"-")
		for player in player_list:
			player.display_player_info()

		gameflow = [(0, "Pre-Flop", 0),
					(3, "Flop", 1),
					(1, "Turn", 2),
					(1, "River", 3)]

		for n_cards_to_distrib, round_name, round_n in gameflow:
			stop_game = game.play(n_cards_to_distrib, round_name, round_n)
			if stop_game :
				# no showdown on win by fold
				winners = [player for player in player_list if player.status == "inGame"]
				print('\nWinner(s):\n',[winner.name for winner in winners])
				print()
				break
		else:
			# showdown	#TODO: make a function of game
			print(50*"-","Showdown",50*"-")
			for player in player_list:
				print()
				player.final_hand, player.hand_value = game.get_hand_value(player)
				print([card.name for card in player.final_hand])
				# print('hand_val:',player.hand_value)

			winners = game.get_winners()
			game.split_pot(winners)

		game.rotate_blinds()

		input()