import sys

from blackjack import Dealer, Deck, Player


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
                print("Invalid input. Choose one of Hit, Stay, or Hit. ")
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
            self.calculate_winner()
            self.display()

    def calculate_winner(self) -> None:
        if self.player.score > self.dealer.score:
            print("You win! Congratulations.")

        elif self.player.score < self.dealer.score:
            print("You lose! Better luck next time.")

        else:
            print("Its a tie... Shucks.")

        self.play_again()

    def dealer_decision(self) -> None:
        while self.dealer.score < 17:
            self.hit(self.dealer)
        else:
            print("Dealer stays.")
            self.dealer.flip()
            self.display()

    def bust(self, loser: Player | Dealer) -> None:
        if isinstance(loser, Player):
            print(f"{loser.name} busts with {loser.score}! {self.dealer.name} wins!")

        else:
            print(f"{loser.name} busts with {loser.score}! A good attempt, but {loser.name} loses.")

        self.display()
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
