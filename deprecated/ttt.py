import random
import math
import copy

class Tree:
    def __init__(self, board):
        self.board = board
        self.visits = 0
        self.score = 0
        self.children = []

class MCTS:
    def search(self, mx, player):
        root = Tree(mx)
        for i in range(1200):
            leaf = self.expand(root, player)
            result = self.rollout(leaf)
            self.backpropagate(leaf, root, result)
        return self.best_child(root).board

    def expand(self, root, player):
        plays = self.generate_states(root.board, player)
        if root.visits == 0:
            for j in plays:
                root.children.append(j)
        for j in root.children:
            if j.visits == 0:
                return j
        for j in plays:
            if self.final(j.board, player):
                return j
        return self.best_child(root)

    def rollout(self, leaf):
        mx = leaf.board
        aux = 1
        while not self.final(mx, "O"):
            if aux == 1:
                possible_nodes = self.generate_states(mx, "X")
            else:
                possible_nodes = self.generate_states(mx, "O")
            possible_states = [i.board for i in possible_nodes]
            if not possible_states:
                break  # Exit if no more possible states
            mx = random.choice(possible_states)
            aux = 1 - aux
        if self.final(mx, "X"):
            return -1
        elif self.final(mx, "O"):
            return 1
        else:
            return 0

    def backpropagate(self, leaf, root, result):
        leaf.score += result
        leaf.visits += 1
        root.visits += 1

    def generate_states(self, mx, player):
        possible_states = []
        for i in range(len(mx)):
            for k in range(len(mx[i])):
                if mx[i][k] == "-":
                    option = copy.deepcopy(mx)
                    option[i][k] = player
                    possible_states.append(Tree(option))
        return possible_states

    def final(self, mx, player):
        for i in mx:
            if i == [player, player, player]:
                return True
        if mx[0][0] == player and mx[1][1] == player and mx[2][2] == player:
            return True
        if mx[0][2] == player and mx[1][1] == player and mx[2][0] == player:
            return True
        for i in range(3):
            if mx[0][i] == player and mx[1][i] == player and mx[2][i] == player:
                return True
        return False

    def calculate_score(self, score, child_visits, parent_visits, c):
        return score / child_visits + c * math.sqrt(math.log(parent_visits) / child_visits)

    def best_child(self, root):
        treshold = -1 * 10**6
        win_choice = None
        for j in root.children:
            potential = self.calculate_score(j.score, j.visits, root.visits, 2)
            if potential > treshold:
                win_choice = j
                treshold = potential
        return win_choice

def print_board(board):
    for row in board:
        print(" | ".join(row))
        print("-" * 5)

def get_player_move(board):
    while True:
        move = input("Enter your move (row and column): ").split()
        if len(move) != 2:
            print("Invalid input. Please enter row and column.")
            continue
        row, col = int(move[0]), int(move[1])
        if row < 0 or row >= 3 or col < 0 or col >= 3 or board[row][col] != "-":
            print("Invalid move. Try again.")
        else:
            return row, col

def main():
    board = [["-" for _ in range(3)] for _ in range(3)]
    mcts = MCTS()
    player = "X"
    ai = "O"
    
    while True:
        print_board(board)
        if player == "X":
            row, col = get_player_move(board)
            board[row][col] = player
        else:
            print("AI is making a move...")
            board = mcts.search(board, ai)
        
        if mcts.final(board, player):
            print_board(board)
            print(f"Player {player} wins!")
            break
        elif mcts.final(board, ai):
            print_board(board)
            print("AI wins!")
            break
        elif all(cell != "-" for row in board for cell in row):
            print_board(board)
            print("It's a draw!")
            break
        
        player, ai = ai, player

if __name__ == "__main__":
    main()
