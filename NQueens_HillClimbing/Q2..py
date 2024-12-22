import random, sys, copy
from optparse import OptionParser
import time

try:
    import psyco

    psyco.full()
except ImportError:
    pass

q = int(input("Enter number of Queens\n"))
ni = q


class board:
    def __init__(self, list=None):
        if list == None:
            self.board = [[0 for i in range(0, q)] for j in range(0, q)]
            for i in range(0, q):
                while 1:
                    rand_row = random.randint(0, q - 1)
                    rand_col = random.randint(0, q - 1)
                    if self.board[rand_row][rand_col] == 0:
                        self.board[rand_row][rand_col] = "Q"
                        break

    def __repr__(self):
        mstr = ""
        for i in range(0, q):
            for j in range(0, q):
                mstr = mstr + str(self.board[i][j]) + " "

            mstr = mstr + "\n"
        return (mstr)


class queens:
    def __init__(self, numruns, verbocity, passedboard=None):
        self.totalruns = numruns
        self.totalsucc = 0
        self.totalnumsteps = 0
        self.verbocity = verbocity
        for i in range(0, numruns):
            if self.verbocity == True:
               
                print("====================")
            self.mboard = board(passedboard)
            self.cost = self.calc_cost(self.mboard)
            self.hill_solution()

    def hill_solution(self):
        noofIS = int(input("Enter number of iterations\n"))
        noofIS = noofIS + 1
        noofI = 0
        while noofI <= noofIS:
            noofI = noofI + 1
            currViolations = self.cost
            self.getlowercostboard()
            if noofIS == noofI:
                break
            elif currViolations == self.cost:
                break
            self.totalnumsteps += 1
            if self.verbocity == True:
                print("Attack in this Step", self.calc_cost(self.mboard))
                print(self.mboard)
        if self.cost != 0:
            if self.verbocity == True:
                print("Solution not found!")
        else:
            if self.verbocity == True:
                print("Solution found!")
            self.totalsucc += 1

        return self.cost

    def calc_cost(self, tboard):
        totalhcost = 0
        totaldcost = 0
        for i in range(0, q):
            for j in range(0, q):
                
                if tboard.board[i][j] == "Q":
                   
                    totalhcost -= 2
                    for k in range(0, q):
                        if tboard.board[i][k] == "Q":
                            totalhcost += 1
                        if tboard.board[k][j] == "Q":
                            totalhcost += 1
                    k, l = i + 1, j + 1
                    while k < ni and l < ni:
                        if tboard.board[k][l] == "Q":
                            totaldcost += 1
                        k += 1
                        l += 1
                    k, l = i + 1, j - 1
                    while k < ni and l >= 0:
                        if tboard.board[k][l] == "Q":
                            totaldcost += 1
                        k += 1
                        l -= 1
                    k, l = i - 1, j + 1
                    while k >= 0 and l < ni:
                        if tboard.board[k][l] == "Q":
                            totaldcost += 1
                        k -= 1
                        l += 1
                    k, l = i - 1, j - 1
                    while k >= 0 and l >= 0:
                        if tboard.board[k][l] == "Q":
                            totaldcost += 1
                        k -= 1
                        l -= 1
        return ((totaldcost + totalhcost) / 2)

    def getlowercostboard(self):
        lowcost = self.calc_cost(self.mboard)
        lowestavailable = self.mboard
       
        for q_row in range(0, q):
            for q_col in range(0, q):
                if self.mboard.board[q_row][q_col] == "Q":
                    for m_row in range(0, q):
                        for m_col in range(0, q):
                            if self.mboard.board[m_row][m_col] != "Q":
                                tryboard = copy.deepcopy(self.mboard)
                                tryboard.board[q_row][q_col] = 0
                                tryboard.board[m_row][m_col] = "Q"
                                thiscost = self.calc_cost(tryboard)
                                if thiscost < lowcost:
                                    lowcost = thiscost
                                    lowestavailable = tryboard
        self.mboard = lowestavailable
        self.cost = lowcost


if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-q", "--quiet", dest="verbose",
                      action="store_false", default=True,
                      help="Don't print all the moves... wise option if using large numbers")

    parser.add_option("--numrun", dest="numrun", help="Number of random Boards", default=1,
                      type="int")

    (options, args) = parser.parse_args()

    mboard = queens(verbocity=options.verbose, numruns=options.numrun)
    time.sleep(10)

