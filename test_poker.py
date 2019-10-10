import pytest
from poker import Card, PokerHand, sorted_ranks, suits

@pytest.fixture
def deck():
  deck = {}
  for rank in sorted_ranks:
    for suit in suits:
      deck['%s%s' % (rank, suit)] = Card(rank, suit)
  return deck

@pytest.fixture
def high_card(deck):
  return PokerHand([
    deck['3H'],
    deck['8D'],
    deck['JS'],
    deck['6C'],
    deck['7C']
  ])

@pytest.fixture
def one_pair(deck):
  return PokerHand([
    deck['2H'],
    deck['8D'],
    deck['JS'],
    deck['2C'],
    deck['7C']
  ])

@pytest.fixture
def two_pair(deck):
  return PokerHand([
    deck['2H'],
    deck['8D'],
    deck['JS'],
    deck['2C'],
    deck['JC']
  ])

@pytest.fixture
def three_of_a_kind(deck):
  return PokerHand([
    deck['JH'],
    deck['8D'],
    deck['JS'],
    deck['2C'],
    deck['JC']
  ])

@pytest.fixture
def straight(deck):
  return PokerHand([
    deck['6H'],
    deck['7D'],
    deck['8S'],
    deck['9C'],
    deck['TC']
  ])

@pytest.fixture
def flush(deck):
  return PokerHand([
    deck['6H'],
    deck['2H'],
    deck['AH'],
    deck['7H'],
    deck['5H']
  ])

@pytest.fixture
def full_house(deck):
  return PokerHand([
    deck['JH'],
    deck['JC'],
    deck['JS'],
    deck['7H'],
    deck['7C']
  ])

@pytest.fixture
def four_of_a_kind(deck):
  return PokerHand([
    deck['2D'],
    deck['2H'],
    deck['2C'],
    deck['2S'],
    deck['5H']
  ])

@pytest.fixture
def straight_flush(deck):
  return PokerHand([
    deck['6H'],
    deck['7H'],
    deck['8H'],
    deck['9H'],
    deck['TH']
  ])

@pytest.fixture
def royal_flush(deck):
  return PokerHand([
    deck['TH'],
    deck['JH'],
    deck['QH'],
    deck['KH'],
    deck['AH']
  ])

def test_high_card(high_card):
  assert high_card._score() is None # Score is None
  assert not high_card.is_flush()
  assert not high_card.is_two_pair()
  assert not high_card.is_four_of_a_kind()
  assert not high_card.is_full_house()
  assert not high_card.is_one_pair()
  assert not high_card.is_royal_flush()
  assert not high_card.is_straight()
  assert not high_card.is_straight_flush()
  assert not high_card.is_three_of_a_kind()

def test_high_card_tie_break(deck):
  a = PokerHand([deck['3H'], deck['8D'], deck['JS'], deck['6C'], deck['7C']])
  b = PokerHand([deck['QH'], deck['2D'], deck['9S'], deck['6S'], deck['7S']])
  assert a._score() is None
  assert b._score() is None
  assert a < b # Queen beats Jack

def test_one_pair(one_pair):
  assert one_pair.is_one_pair()
  assert not one_pair.is_two_pair()
  assert not one_pair.is_flush()
  assert not one_pair.is_four_of_a_kind()
  assert not one_pair.is_full_house()
  assert not one_pair.is_royal_flush()
  assert not one_pair.is_straight()
  assert not one_pair.is_straight_flush()
  assert not one_pair.is_three_of_a_kind()

def test_one_pair_tie_break(deck):
  a = PokerHand([deck['3H'], deck['8D'], deck['3S'], deck['6C'], deck['7C']])
  b = PokerHand([deck['QH'], deck['2D'], deck['9S'], deck['6S'], deck['2S']])
  assert a.is_one_pair()
  assert b.is_one_pair()
  assert a > b # 3 beats 2

def test_one_pair_tie_break_1(deck):
  """
  Test tiebreak situation for the pair being the same rank, and the first high
  card beiing the same (should fall to the 2nd high card).
  """
  a = PokerHand([deck['AD'], deck['AH'], deck['9C'], deck['2C'], deck['7C']])
  b = PokerHand([deck['AC'], deck['AS'], deck['9S'], deck['JS'], deck['2S']])
  assert a.is_one_pair()
  assert b.is_one_pair()
  assert b > a

def test_two_pair(two_pair):
  assert two_pair.is_one_pair()
  assert two_pair.is_two_pair()
  assert not two_pair.is_flush()
  assert not two_pair.is_four_of_a_kind()
  assert not two_pair.is_full_house()
  assert not two_pair.is_royal_flush()
  assert not two_pair.is_straight()
  assert not two_pair.is_straight_flush()
  assert not two_pair.is_three_of_a_kind()

def test_two_pair_tie_break(deck):
  a = PokerHand([deck['3H'], deck['7D'], deck['3S'], deck['6C'], deck['7C']])
  b = PokerHand([deck['QH'], deck['2D'], deck['2S'], deck['6S'], deck['QS']])
  assert a.is_two_pair()
  assert b.is_two_pair()
  assert b > a # Queen beats 7

def test_two_pair_tie_break_2(deck):
  a = PokerHand([deck['3H'], deck['7D'], deck['3S'], deck['KC'], deck['7C']])
  b = PokerHand([deck['3D'], deck['3C'], deck['7H'], deck['6S'], deck['7S']])
  assert a.is_two_pair()
  assert b.is_two_pair()
  assert a > b # King high wins.

def test_two_pair_tie_break_2_tie(deck):
  a = PokerHand([deck['3H'], deck['7D'], deck['3S'], deck['6C'], deck['7C']])
  b = PokerHand([deck['3D'], deck['3C'], deck['7H'], deck['6S'], deck['7S']])
  assert a.is_two_pair()
  assert b.is_two_pair()
  assert b == a # Each hand has a pair of 3 and 7, with 6 high card (tie)

def test_three_of_a_kind(three_of_a_kind):
  assert three_of_a_kind.is_three_of_a_kind()
  assert not three_of_a_kind.is_one_pair()
  assert not three_of_a_kind.is_two_pair()
  assert not three_of_a_kind.is_flush()
  assert not three_of_a_kind.is_four_of_a_kind()
  assert not three_of_a_kind.is_full_house()
  assert not three_of_a_kind.is_royal_flush()
  assert not three_of_a_kind.is_straight()
  assert not three_of_a_kind.is_straight_flush()

def test_three_of_a_kind_tiebreak(deck):
  a = PokerHand([deck['3H'], deck['7D'], deck['3S'], deck['3C'], deck['9C']])
  b = PokerHand([deck['QH'], deck['QD'], deck['2S'], deck['6S'], deck['QS']])
  assert a.is_three_of_a_kind()
  assert b.is_three_of_a_kind()
  assert b > a # Queen beats 7
  
def test_straight(straight):
  assert straight.is_straight()
  assert not straight.is_three_of_a_kind()
  assert not straight.is_one_pair()
  assert not straight.is_two_pair()
  assert not straight.is_flush()
  assert not straight.is_four_of_a_kind()
  assert not straight.is_full_house()
  assert not straight.is_royal_flush()
  assert not straight.is_straight_flush()

def test_straight_tiebreak(deck):
  a = PokerHand([deck['3H'], deck['4D'], deck['5S'], deck['6C'], deck['7C']])
  b = PokerHand([deck['4H'], deck['5D'], deck['6S'], deck['7S'], deck['8S']])
  assert a.is_straight()
  assert b.is_straight()
  assert b > a # Straight ending in 8 beats one ending in 7

def test_three_of_a_kind_tiebreak(deck):
  a = PokerHand([deck['3H'], deck['7D'], deck['3S'], deck['3C'], deck['9C']])
  b = PokerHand([deck['QH'], deck['QD'], deck['2S'], deck['6S'], deck['QS']])
  assert a.is_three_of_a_kind()
  assert b.is_three_of_a_kind()
  assert b > a # Queen beats 7

def test_flush(flush):
  assert flush.is_flush()
  assert not flush.is_straight()
  assert not flush.is_three_of_a_kind()
  assert not flush.is_one_pair()
  assert not flush.is_two_pair()
  assert not flush.is_four_of_a_kind()
  assert not flush.is_full_house()
  assert not flush.is_royal_flush()
  assert not flush.is_straight_flush()

def test_flush_tiebreak(deck):
  a = PokerHand([deck['2H'], deck['7H'], deck['6H'], deck['KH'], deck['9H']])
  b = PokerHand([deck['2D'], deck['QD'], deck['5D'], deck['9D'], deck['AD']])
  assert a.is_flush()
  assert b.is_flush()
  assert b > a # Queen beats 7

def test_full_house(full_house):
  assert full_house.is_full_house()
  assert full_house.is_three_of_a_kind()
  assert not full_house.is_flush()
  assert not full_house.is_straight()
  assert not full_house.is_one_pair()
  assert not full_house.is_two_pair()
  assert not full_house.is_four_of_a_kind()
  assert not full_house.is_royal_flush()
  assert not full_house.is_straight_flush()

def test_full_house_tibreak(deck):
  a = PokerHand([deck['2H'], deck['7H'], deck['7D'], deck['2C'], deck['7C']])
  b = PokerHand([deck['9D'], deck['4D'], deck['9S'], deck['4S'], deck['9C']])
  assert a.is_full_house()
  assert b.is_full_house()
  assert b > a

def test_four_of_a_kind(four_of_a_kind):
  assert four_of_a_kind.is_four_of_a_kind()
  assert not four_of_a_kind.is_flush()
  assert not four_of_a_kind.is_straight()
  assert not four_of_a_kind.is_three_of_a_kind()
  assert not four_of_a_kind.is_one_pair()
  assert not four_of_a_kind.is_two_pair()
  assert not four_of_a_kind.is_full_house()
  assert not four_of_a_kind.is_royal_flush()
  assert not four_of_a_kind.is_straight_flush()

def test_four_of_a_kind_tibreak(deck):
  a = PokerHand([deck['2H'], deck['2D'], deck['2D'], deck['2C'], deck['7C']])
  b = PokerHand([deck['9D'], deck['9H'], deck['9S'], deck['4S'], deck['9C']])
  assert a.is_four_of_a_kind()
  assert b.is_four_of_a_kind()
  assert b > a

def test_straight_flush(straight_flush):
  assert straight_flush.is_straight_flush()
  assert straight_flush.is_straight()
  assert straight_flush.is_flush()
  assert not straight_flush.is_four_of_a_kind()
  assert not straight_flush.is_three_of_a_kind()
  assert not straight_flush.is_one_pair()
  assert not straight_flush.is_two_pair()
  assert not straight_flush.is_full_house()
  assert not straight_flush.is_royal_flush()

def test_straight_flush_tiebreak(deck):
  a = PokerHand([deck['3H'], deck['4H'], deck['5H'], deck['6H'], deck['7H']])
  b = PokerHand([deck['4D'], deck['5D'], deck['6D'], deck['7D'], deck['8D']])
  assert a.is_straight_flush()
  assert b.is_straight_flush()
  assert b > a # Straight ending in 8 beats one ending in 7

def test_royal_flush(royal_flush):
  assert royal_flush.is_royal_flush()
  assert royal_flush.is_straight_flush()
  assert royal_flush.is_straight()
  assert royal_flush.is_flush()
  assert not royal_flush.is_four_of_a_kind()
  assert not royal_flush.is_three_of_a_kind()
  assert not royal_flush.is_one_pair()
  assert not royal_flush.is_two_pair()
  assert not royal_flush.is_full_house()

def test_ranking(high_card, one_pair, two_pair, three_of_a_kind, straight, flush, 
  full_house, four_of_a_kind, straight_flush, royal_flush):
  assert high_card < one_pair < two_pair < three_of_a_kind < straight < flush\
    < full_house < four_of_a_kind < straight_flush < royal_flush