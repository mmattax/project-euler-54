from poker import Card, PokerHand
from prettytable import PrettyTable

player_one_wins = 0
player_two_wins = 0
table = PrettyTable(['Game', 'Player 1', 'Player 2', 'Winner'])

with open('hands.txt', 'r') as fp:
  for i, line in enumerate(fp):

    cards = line.split()
    cards = [Card(rank, suit) for rank, suit in cards]

    player_one = PokerHand(cards[:5])
    player_two = PokerHand(cards[5:])
 
    outcome = None
    if player_one == player_two:
      outcome = 'Tie'
    elif player_one > player_two:
      outcome = 'Player 1'
      player_one_wins += 1
    else:
      outcome = 'Player 2'
      player_two_wins += 1
    
    table.add_row([i + 1, player_one, player_two, outcome])
    
print table

table = PrettyTable(['Player', 'Wins'])
table.add_row(['Player 1', player_one_wins])
table.add_row(['Player 2', player_two_wins])
print table