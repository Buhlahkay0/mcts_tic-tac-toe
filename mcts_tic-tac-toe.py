import random
import math
from copy import deepcopy

class TicTacToe:
    def __init__(self):
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.current_winner = None

    def print_board(self):
        for row in self.board:
            print('| ' + ' | '.join(row) + ' |')

    def available_moves(self):
        return [(i, j) for i in range(3) for j in range(3) if self.board[i][j] == ' ']

    def make_move(self, square, letter):
        if self.board[square[0]][square[1]] == ' ':
            self.board[square[0]][square[1]] = letter
            if self.winner(square, letter):
                self.current_winner = letter
            return True
        return False

    def winner(self, square, letter):
        row_ind, col_ind = square
        row = self.board[row_ind]
        if all([spot == letter for spot in row]):
            return True
        col = [self.board[i][col_ind] for i in range(3)]
        if all([spot == letter for spot in col]):
            return True
        if row_ind == col_ind:
            diagonal = [self.board[i][i] for i in range(3)]
            if all([spot == letter for spot in diagonal]):
                return True
        if row_ind + col_ind == 2:
            diagonal = [self.board[i][2-i] for i in range(3)]
            if all([spot == letter for spot in diagonal]):
                return True
        return False

    def empty_squares(self):
        return ' ' in [spot for row in self.board for spot in row]

    def num_empty_squares(self):
        return len(self.available_moves())

    def is_full(self):
        return self.num_empty_squares() == 0

class Node:
    def __init__(self, move=None, parent=None, state=None):
        self.move = move
        self.parent = parent
        self.state = state
        self.children = []
        self.wins = 0
        self.visits = 0
        self.untried_moves = state.available_moves() if state else []
        self.player = 'O' if parent is None or parent.player == 'X' else 'X'

    def select_child(self):
        return sorted(self.children, key=lambda c: c.wins / c.visits + math.sqrt(2 * math.log(self.visits) / c.visits))[-1]

    def add_child(self, move, state):
        child = Node(move=move, parent=self, state=state)
        self.untried_moves.remove(move)
        self.children.append(child)
        return child

    def update(self, result):
        self.visits += 1
        self.wins += result

def MCTS(rootstate, max_iterations):
    rootnode = Node(state=rootstate)

    for _ in range(max_iterations):
        node = rootnode
        state = deepcopy(rootstate)

        # Select
        while node.untried_moves == [] and node.children != []:
            node = node.select_child()
            state.make_move(node.move, node.player)

        # Expand
        if node.untried_moves:
            m = random.choice(node.untried_moves)
            state.make_move(m, node.player)
            node = node.add_child(m, state)

        # Rollout
        while state.available_moves():
            state.make_move(random.choice(state.available_moves()), 'X' if state.num_empty_squares() % 2 == 0 else 'O')

        # Backpropagate
        while node:
            node.update(1 if state.current_winner == node.player else 0)
            node = node.parent

    return sorted(rootnode.children, key=lambda c: c.visits)[-1].move

def play_game():
    game = TicTacToe()
    human = 'X'
    agent = 'O'

    while game.empty_squares():
        if game.num_empty_squares() % 2 == 0:
            move = MCTS(game, 100_000)
            game.make_move(move, agent)
            print(f"Agent played {move}")
        else:
            game.print_board()
            move = None
            while move not in game.available_moves():
                row = int(input('Enter row (1, 2, 3): '))
                col = int(input('Enter col (1, 2, 3): '))
                move = (row - 1, col - 1)
            game.make_move(move, human)

        if game.current_winner:
            game.print_board()
            print(f"{game.current_winner} wins")
            return
        elif game.is_full():
            game.print_board()
            print("Tie")
            return

if __name__ == '__main__':
    play_game()
