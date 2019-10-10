from functools import total_ordering
from collections import OrderedDict

sorted_ranks = [str(rank) for rank in range(2, 10)]
sorted_ranks.extend(['T', 'J', 'Q', 'K', 'A'])

suits = ['D', 'H', 'S', 'C']

@total_ordering
class Card(object):
  rank = None
  suit = None

  def __init__(self, rank, suit):
    self.rank = rank
    self.suit = suit

  def __lt__(self, card):
    return sorted_ranks.index(self.rank) < sorted_ranks.index(card.rank)
  
  def __eq__(self, card):
    return sorted_ranks.index(self.rank) == sorted_ranks.index(card.rank)

  def __str__(self):
    return '%s%s' % (self.rank, self.suit)
  
  def __repr__(self):
    return self.__str__()

@total_ordering
class PokerHand(object):

  cards   = []
  grouped = []
  
  def __init__(self, cards):

    # Sort the cards in the hand by rank, highest cards first.
    self.cards = cards
    self.cards.sort(reverse=True)

    # Now we'll group matching ranks together.
    # [KC, 5C, 5S, 4C, 2C] will become [KC, [5C, 5S], 4C, 2C].
    # An OrderedDict here ensures that we're still in card rank order.
    group_map = OrderedDict()
    for card in self.cards:
      group = group_map.get(card.rank, [])
      group.append(card)
      group_map[card.rank] = group
    grouped = []
    for value in group_map.values():
      grouped.append(value if len(value) > 1 else value[0])
    
    # The grouped data structure is still sorted and grouped by card ranks 
    # ([KC, [5C, 5S], 4C, 2C]), but we'd like to sort groups (like the pair of 5's 
    # in the example) into the front of the list: [[5C, 5S], KC, 4C, 2C].
    # 
    # This allows us to linearly compare groups to each other for tiebreaks. To do this,
    # We'll just sort by list length, which will put larger groups (4-of-a-kind, 3-of-a-kind)
    # into proper order.
    grouped.sort(key=lambda c: len(c) if isinstance(c, list) else 1, reverse=True)
    self.grouped = grouped

  def _score(self):
    """
    Returns a score (1-8) on the strength of the poker hand. Returns None
    if the hand only contains a "High Card" value.
    """
    outcomes = [
      {
        'score': 1,
        'method': self.is_one_pair,
      },
      {
        'score': 2,
        'method': self.is_two_pair,
      },
      {
        'score': 3,
        'method': self.is_three_of_a_kind,
      },
      {
        'score': 4,
        'method': self.is_straight,
      },
      {
        'score': 5,
        'method': self.is_flush,
      },
      {
        'score': 6,
        'method': self.is_full_house,
      },
      {
        'score': 7,
        'method': self.is_four_of_a_kind,
      },
      {
        'score': 8,
        'method': self.is_straight_flush
      },
      {
        'score': 9,
        'method': self.is_royal_flush
      }
    ]
    score = None
    for outcome in outcomes:
      if outcome['method']():
        score = outcome['score']
    return score
  
  def _has_tiebreak(self, hand):
    """
    Determines if this hand will beat "hand" in a tiebreak scenario.

    Assuming the _score method returns the same value when comparing this hand with another,
    this method will linearly look at the ranks within each group and determine which
    hand has the highest value.

    Returned value is True when this hand wins, False when it loses, and None when it's a tie.
    """
    for i, group in enumerate(self.grouped):
      group2 = hand.grouped[i]
      card1 = group[0] if isinstance(group, list) else group
      card2 = group2[0] if isinstance(group2, list) else group2
      if card1 == card2:
        # The ranks are the same within the group, move on to the next card or group.
        continue
      return card1 > card2
    # Tie
    return None

  def __lt__(self, hand):

    score1 = self._score()
    score2 = hand._score()

    if score1 == score2:
      # If the hands have the same score, we'll look at the tiebreak.
      # Explicitly looking for equality to False because None is returned in a tie.
      tiebreak = self._has_tiebreak(hand)
      return tiebreak == False  
    return score1 < score2
    

  def __eq__(self, hand):
    """
    Returns True if the hands result in a tie.
    """
    score1 = self._score()
    score2 = hand._score()
    return score1 == score1 and self._has_tiebreak(hand) == None

  def is_four_of_a_kind(self):
    """
    Returns True if this hand contains a four of a kind.

    """
    return isinstance(self.grouped[0], list) and len(self.grouped[0]) == 4

  def is_three_of_a_kind(self):
    """
    Returns True if this hand contains a three of a kind.
    """
    return isinstance(self.grouped[0], list) and len(self.grouped[0]) == 3
  
  def is_full_house(self):
    """
    Returns True if this hand contains a full house.
    """
    is_three_of_a_kind = self.is_three_of_a_kind()
    has_a_pair = isinstance(self.grouped[1], list) and len(self.grouped[1]) == 2
    return is_three_of_a_kind and has_a_pair
  
  def is_two_pair(self):
    """
    Returns True if this hand contains two pairs.
    """
    return isinstance(self.grouped[0], list) and len(self.grouped[0]) == 2\
      and isinstance(self.grouped[1], list) and len(self.grouped[1]) == 2
  
  def is_one_pair(self):
    """
    Returns True if this hand contains a pair.
    """
    return isinstance(self.grouped[0], list) and len(self.grouped[0]) == 2
  
  def is_straight(self):
    """
    Returns True if this hand contains a straight.
    """
    index = None
    old_index = None
    for card in self.grouped:
      if isinstance(card, list):
        # A straight won't contain a list (no duplicate ranks).
        return False
      if index is not None:
        old_index = index
      index = sorted_ranks.index(card.rank)
      if old_index and old_index - 1 != index:
        # We'll just make sure each card is single rank away from the previous, this
        # works because we know that self.grouped is already sorted.
        return False
    return True

  def is_flush(self):
    """
    Returns True if this hand contains a flush.
    """
    return len(set(card.suit for card in self.cards)) == 1

  def is_straight_flush(self):
    """
    Returns True if this hand contains a straight flush.
    """
    return self.is_straight() and self.is_flush()

  def is_royal_flush(self):
    """
    Returns True if this hand contains a royal flush.
    """
    return self.is_flush() and\
      set(card.rank for card in self.cards) == set(['T', 'J', 'Q', 'K', 'A'])

  def __str__(self):
    return str(self.grouped)