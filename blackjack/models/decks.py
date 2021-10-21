import random

from blackjack.models import Card


class Deck:
    """Represents a deck of playing cards"""

    def __init__(self) -> None:
        self.new_deck()

    @property
    def cards(self) -> list[Card]:
        """The cards in the deck."""
        return self._cards

    def new_deck(self) -> None:
        """Generates a new deck of 52 cards and shuffles them."""
        self._cards: list[Card] = []

        for r in Card.RANKS:
            self.cards.extend(Card(r, s) for s in Card.SUITS)

        self.shuffle()

    def shuffle(self) -> None:
        """Shuffles the deck."""
        random.shuffle(self.cards)

    def draw(self) -> Card:
        """Draws one card from the deck."""
        return self.cards.pop()

    def draw_many(self, amount: int) -> list[Card]:
        """Draws multiple cards from the deck."""
        drawn = self.cards[-amount:]
        self._cards = self.cards[:-amount]
        return drawn

    def __repr__(self) -> str:
        """Representation of a deck."""
        return "\n".join(str(c) for c in self.cards)
