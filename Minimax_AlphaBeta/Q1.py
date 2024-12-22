from math import inf
import copy
class MinimaxAlphaBetaAgent():

    def __init__(self):
        return
    def staticEval(self,state):
        return state.score

    def minimax_alpha_beta(self, state, depth, alpha, beta, isMax):
            if state.gameOver() or depth is 0:
                return -1, state.score() - depth
            if isMax:
                bestValue = -1, -inf
            else:
                bestValue = -1, inf

            for s in self.get_all_next_moves(state):
                player = 'X' if isMax else 'O'
                state.move(player, s)
                value = s, self.minimax_alpha_beta(state, depth - 1, alpha, beta, not isMax)[1]
                state.undo_move(player, s)
                if isMax:
                    bestValue = max(bestValue, value, key= lambda i: i[1])
                    alpha = max(alpha, bestValue[1])
                    if alpha >= beta:
                        break
                else:
                    bestValue = min(bestValue, value, key= lambda i: i[1])
                    beta = min(beta, value[1])
                    if alpha >= beta:
                        break

            return bestValue

    def choose(self, state, player):
        return self.minimax_alpha_beta(state, len(self.get_all_next_moves(state)), -inf, inf, player)

    def get_all_next_moves(self, state):
        moves = []
        for row in state.empty_tiles():
            for tile in row:
                moves.append(tile)
        return moves

class Model():

    def __init__(self):
        position = 0
        self.board = [[{"position": 0, "value": 0} for y in range(0, 3)] for x in range(0, 3)]
        position = 0
        for row in self.board:
            for tile in row:
                position += 1
                tile["position"] = position

        self.depth = 9
        self.players = ['X', 'O']

    def move(self, player, position):
        for row in self.board:
            for tile in row:
                if tile["position"] is position:
                    if tile["value"] is 0:
                        if player == 'X':
                            tile["value"] = 1
                            self.depth -= 1
                            return
                        elif player == 'O':
                            tile["value"] = -1
                            self.depth -= 1
                            return
                        else:
                            raise Exception("Player {} not found.".format(player))
                    else:
                        raise Exception("Invalid move at {}.".format(position))
        raise Exception("Out of bounds {}.".format(position))

    def undo_move(self, player, position):
        for row in self.board:
            for tile in row:
                if tile["position"] is position:
                    if tile["value"] is not 0:
                        tile["value"] = 0
                        self.depth += 1
                    else:
                        raise Exception("No move to undo at {}.".format(position))


    def empty_tiles(self):
        return [[tile["position"] for tile in row if tile["value"] is 0] for row in self.board]

    def score(self):
        verticals = [[row[i]["value"] for row in self.board] for i in range(len(self.board))]
        index = 2
        diagonals = [[self.board[num][num]["value"] for num in range(0, 3)], [self.board[num][index - num]["value"] for num in range(0, 3)]]
        winPossibilities = []
        winPossibilities.append([[tile["value"] for tile in row] for row in self.board])
        winPossibilities.append(verticals)
        winPossibilities.append(diagonals)

        for possibility in winPossibilities:
            for row in possibility:
                if sum(row) is 3:
                    return 10
                elif sum(row) is -3:
                    return -10

        return 0

    def gameOver(self):
        if self.score() > 0 or self.depth <= 0 or self.score() < 0:
            return True
        else:
            return False

class TextView():
    def __init__(self, state):
        self.currState = state
        self.initState = state
        self.gameRepr = ""
        self.rules = ""
        self.rules +="\n\n"
        for row in self.currState.board:
            for tile in row:
                self.rules +="| {} |".format(tile["position"])
            self.rules += "\n"
        self.rules += "\n"

    def draw(self):
        self.gameRepr = ""      
        for row in self.currState.board:
            for tile in row:
                if tile["value"] is not 0:
                    self.gameRepr +="| {} |".format('X' if tile["value"] is 1 else 'O')
                else:
                    self.gameRepr +="|   |"
            self.gameRepr += "\n"
        return self.gameRepr

    def reset():
        self.currState = self.initState

def main(view, agent):
    player = 1
    temp = ''
    while not view.currState.gameOver():
        temp = 'X' if player is 1 else 'O'
        print("=======================================================================================")
        print(view.rules)
        print("=======================================================================================\n\n")
        move = 0
        if player is 1:
            print("Player X's turn:")
            depth = len(agent.get_all_next_moves(view.currState))
            print(depth)
            move = agent.choose(view.currState, False)[0]
            print(move)
        else:
            print("Player O's turn:")
            depth = len(agent.get_all_next_moves(view.currState))
            print(depth)
            move = agent.choose(view.currState, False)[0]
            print(move)
        view.currState.move(temp, int(move))
        print("=======================================================================================")
        print(view.draw())
        print(view.currState.empty_tiles())
        player = -player
    if view.currState.score() == 10:
        print("Player X wins!")

    elif view.currState.score() == -10:
        print("Player O wins!")

    else:
        print("It's a draw!")

game = Model()
text = TextView(game)
agent = MinimaxAlphaBetaAgent()
main(text, agent)




