class Card:
    """Represents a playing card."""
    RANKS = (2, 3, 4, 5, 6, 7, 8, 9, 10, "jack", "queen", "king", "ace")
    SUITS = ("clubs", "diamonds", "hearts", "spades")

    def __init__(self, rank: str | int, suit: str, hidden: bool = False) -> None:
        self._rank = rank
        self._suit = suit
        self._hidden = hidden

    @property
    def rank(self) -> str | int:
        """The rank of the card."""
        return self._rank

    @property
    def suit(self) -> str:
        """The suit of the card."""
        return self._suit

    @property
    def hidden(self) -> bool:
        """Whether or not the card is hidden."""
        return self._hidden

    def flip(self) -> "Card":
        """Flip the card to the opposite hidden state."""
        self._hidden = not self.hidden
        return self

    def value(self, score: int) -> int:
        """Returns the cards value."""
        if isinstance(self.rank, int):
            return self.rank

        match self.rank:
            case "king" | "queen" | "jack":
                return 10

            case _:
                return 1 if score + 11 > 21 else 11

    def __repr__(self) -> str:
        return f"**HIDDEN**" if self.hidden else f"{self.rank} of {self.suit}"
