# project-euler-54

I knew I wanted to use Python's equality operators to handle ranking the cards and poker hands. This led me to a simple OOP design for a `Card` and a `PokerHand` class. I thought most of the complexity would be in handling tiebreaks, so I wanted to design a structure where I could easily determine the "groupings" of cards within the hand (things like pairs and n-of-a-kind). I also wanted to keep the hands sorted so rank comparisons would be easy and done linearly.

The internal structure of a hand is a sorted list of cards, or a nested list of found groups (pairs or n-of-a-kind). A few examples:

```
[TS, 8C, 6S, 5C, 2D]     # 10 high
[[TC, TS], QC, JD, 8C]   # Pair of 10
[9H, 9C], [8S, 8H], JC]  # Two pairs 8 and 9, Jack high
[[6H, 6S, 6C], [KS, KH]] # Full house
```

### Run
```
pip install -r requirements.txt
python ./run.py
```

### Test
```
pytest
```

### TODOS
Things I'd work on / think about if this was something to be used in production:
- Validation on valid cards and duplicate in a hand. I took the liberty to trust the data.
- `is_full_house` and `is_three_of_a_kind` will always reeturn `True` together. Would being mutually exclusive be better? I did this intentionally so that logic was reduced, but user needs to be aware.
- Potential optimization: Since the list of cards is sorted within the poker hand, I should be able to look at the first and last value and determine a straight.
