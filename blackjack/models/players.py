from blackjack.models import Card, Deck

class Player:
    """Represents a user in the game."""

    def __init__(self, name: str, deck: Deck) -> None:
        self._name = name
        self._deck = deck
        self._hand = self.deck.draw_many(2)
        self._score = 0
        self.update()

    @property
    def deck(self) -> Deck:
        """The deck associated with this player."""
        return self._deck

    @property
    def hand(self) -> list[Card]:
        """The players hand of cards."""
        return self._hand

    @property
    def name(self) -> str:
        """The players name."""
        return self._name

    @property
    def score(self) -> int:
        """The players actual score including hidden cards."""
        return self._score

    @property
    def peek_score(self) -> int:
        """The players visible score."""
        return sum(c.value(self.score) for c in self.hand if not c.hidden)

    def draw(self) -> Card:
        """Draws a card from the deck for the player."""
        self.hand.append(self.deck.draw())
        self.update()
        return self.hand[-1]

    def update(self) -> int:
        """Updates the players current score."""
        self._score = sum(c.value(self.score) for c in self.hand)
        return self.score


class Dealer(Player):
    """Represents the dealer in the game."""

    def __init__(self, deck: Deck) -> None:
        super().__init__("Dealer", deck)
        self.flip()

    def flip(self) -> Card:
        """Flip the dealers first card over."""
        flipped = self.hand[0].flip()
        self.update()
        return flipped
