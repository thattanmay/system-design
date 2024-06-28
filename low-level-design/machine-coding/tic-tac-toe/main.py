class Player:
    def __init__(self, name) -> None:
        self.name = name
        self.row = None
        self.col = None

    def get_move(self, msg):
        player_input = list(
            map(
                int,
                input(msg).split(),
            )
        )
        self.row, self.col = player_input
        self.row -= 1
        self.col -= 1


class Board:
    def __init__(self, board_size) -> None:
        self.side = board_size
        self.board = [[" " for _ in range(self.side)] for _ in range(self.side)]

    def display(self):
        print()
        for row in self.board:
            print(" | ".join([i for i in row]))
        print()

    def is_valid_move(self, player: Player):
        if not (0 <= player.row < self.side and 0 <= player.col < self.side):
            return 0
        return self.board[player.row][player.col] == " "

    def make_move(self, player: Player, piece: str):
        self.board[player.row][player.col] = piece

    def check_winner(self, piece):
        # row
        for i in range(self.side):
            if self.board[i].count(piece) == self.side:
                return 1
        # cols
        for i in range(self.side):
            if [self.board[r][i] for r in range(self.side)].count(piece) == self.side:
                return 1
        # diagonal
        if [self.board[i][i] for i in range(self.side)].count(piece) == self.side:
            return 1
        if [self.board[i][self.side - i - 1] for i in range(self.side)].count(
            piece
        ) == self.side:
            return 1
        return 0


class Game:
    def __init__(self, no_of_players: int, board_size: list[int]) -> None:
        self.no_of_players = no_of_players
        self.max_turns = board_size * board_size
        self.board: Board = Board(board_size)
        self.pieces = (
            ["O", "X"]
            if self.no_of_players == 2
            else [chr(65 + i) for i in range(self.no_of_players)]
        )
        self.players: list[Player] = []
        for i in range(no_of_players):
            player_name: str = input(f"Enter player {i+1} name: ")
            self.players.append(Player(player_name))
        self.turn: int = 0

    def start(self):
        self.board.display()
        while 1:
            player = self.players[self.turn % self.no_of_players]
            piece = self.pieces[self.turn % self.no_of_players]

            # get valid move
            player.get_move(
                f"Player {player.name}, please make your move('{piece}') (row, col): "
            )
            while not self.board.is_valid_move(player):
                player.get_move("Invalid move, please try again: ")

            # make move
            self.board.make_move(player, piece)
            self.board.display()

            # check for winner
            if self.board.check_winner(piece):
                print(f"Player {player.name} wins!")
                break

            self.turn += 1
            # check for draw
            if self.turn == self.max_turns:
                print("It's a draw!")
                break


if __name__ == "__main__":
    no_of_players = int(input("Please enter number of players: "))
    board_size = int(input("Enter square board side length: "))
    game = Game(no_of_players, board_size)
    game.start()
