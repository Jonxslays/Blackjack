"""
Card
Deck
ComputerUser
HumanUser
Game
"""
import random
import sys


RANKS = (2, 3, 4, 5, 6, 7, 8, 9, 10, "jack", "queen", "king", "ace")
SUITS = ("clubs", "diamonds", "hearts", "spades")


class Card:
    """Represents a playing card."""

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

        for r in RANKS:
            self._cards.extend([Card(r, s) for s in SUITS])

        self.shuffle()

    def shuffle(self) -> "Deck":
        """Shuffles the deck."""
        random.shuffle(self._cards)
        return self

    def draw(self) -> Card:
        """Draws one card from the deck."""
        return self._cards.pop()

    def draw_many(self, amount: int) -> list[Card]:
        """Draws multiple cards from the deck."""
        drawn = self.cards[-amount:]
        self._cards = self.cards[:-amount]
        return drawn

    def __repr__(self) -> str:
        """Representation of a deck."""
        return "\n".join(str(c) for c in self.cards)


class Player:
    """Represents a user in the game."""

    def __init__(self, name: str, deck: Deck) -> None:
        self._name = name
        self._deck = deck
        self._hand = self.deck.draw_many(2)
        self._score: int = 0
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


class Game:
    """Represents a game of blackjack."""

    def __init__(self) -> None:
        self._active = True
        self._deck = Deck()
        self._dealer = Dealer(self._deck)
        print("Welcome to blackjack!")
        print("Dealer stays on 17.")

    @property
    def deck(self) -> Deck:
        """The deck associated with this game."""
        return self._deck

    @property
    def dealer(self) -> Dealer:
        """The dealer associated with this game."""
        return self._dealer

    @property
    def player(self) -> Player:
        """The player associated with this game."""
        return self._player

    def start(self) -> None:
        """Stars the game."""
        p_name = input(f"Enter your name: ")
        self._player = Player(p_name, self.deck)
        self.advance()

    def display(self) -> None:
        """Displays the current board state."""
        print("-" * 20)
        for user in (self.dealer, self.player):
            print(f"{user.name}: {user.peek_score}\n" + "\n".join(str(c) for c in user.hand))
            print("-" * 20)

    def prompt(self) -> None:
        """Prompts the user to make a choice."""
        choice = input("Hit, Stay, or Split: ")

        match choice.lower():
            case "hit":
                print(f"{self.player.name} hits...")
                self.hit(self.player)
            case "stay":
                self._active = False
                print(f"{self.player.name} stays...")
                self.advance()
            case _:
                print("Invalid input. Hit, Stay, or Split: ")
                self.prompt()

    def hit(self, player: Player | Dealer) -> None:
        card = player.draw()
        print(f"{player.name} drew: {str(card)}")

        if player.score > 21:
            self.bust(player)

        self.advance()

    def advance(self) -> None:
        if self._active:
            self.display()
            self.prompt()

        else:
            self.dealer_decision()
            self.display()
            self.calculate_winner()

    def calculate_winner(self) -> None:
        if self.player.score > self.dealer.score:
            print("You win! Congratulations.")

        elif self.player.score < self.dealer.score:
            print("You lose! Better luck next time.")

        else:
            print("Its a tie... Shucks.")

        self.play_again()

    def dealer_decision(self) -> None:
        while self.dealer.peek_score < 17:
            self.hit(self.dealer)

        else:
            print("Dealer stays.")
            self.dealer.flip()

        self.display()

    def bust(self, loser: Player | Dealer) -> None:
        if isinstance(loser, Player):
            print(f"{loser.name} busts! {self.player.name} wins!")

        else:
            print(f"{loser.name} busts! A good attempt, but {loser.name} lose.")

        self.play_again()

    def play_again(self) -> None:
        choice = input("Continue playing? [y/n]: ")

        match choice[0].lower():
            case "y":
                self = Game()
                self.start()

            case "n":
                self.close()

            case _:
                print("Invalid input [y/n] only.")
                self.play_again()

    def close(self) -> None:
        print("Thanks for playing Blackjack! Have a good one.")
        sys.exit(0)
