class Territory:

    def __init__(self, name, neighbors, color = None):

        self.name      = name
        self.neighbors = neighbors
        self.color     = color

    def __str__(self):
        return str((self.name, self.neighbors, self.color))

class MapColor:

    def __init__(self, graph, colors):

        self.map     = graph
        self.colors  = colors
        self.vars    = list(self.map.keys())
        self.domains = { var: set(self.colors) for var in self.vars }

    def solve(self, i):
        if i == len(self.vars):
            return True

        old = {var: set(self.domains[var]) for var in self.vars} 
        var = self.vars[i]
        print ('domain for '  + var + ': ' + str(self.domains[var]))
        if self.map[var].color != None:
            return self.solve(i + 1)

        for color in self.domains[var]:

            if self.is_valid(var, color):

                self.map[var].color = color

                territory = self.map[var]
                for var in territory.neighbors:
                    if self.map[var].color != None:
                        continue
                    if color in self.domains[var]:
                        self.domains[var].remove(color)
                        
                if self.solve(i + 1):
                    return True

                self.set_map(var, None)
                self.domains = old

        return False

    def is_valid(self, var, color):
        territory = self.map[var]

        for neighbor in territory.neighbors:
            if color == self.map[neighbor].color:
                return False

        return True
        


DJ  = 'DJ'
SO  = 'SQ'
ET  = 'ET'
KE  = 'KE'
UG  = 'UG'
TA  = 'TA'
RW  = 'RW'
BU  = 'BU'

colors    = {'r', 'g', 'b'}

australia = { DJ:  Territory(DJ,  [SO, ET]            ),
              SO:  Territory(SO,  [DJ, ET, KE]         ),
              ET:  Territory(ET,  [DJ, SO, KE] ),
              KE:   Territory(KE,   [SO, ET,TA,UG]       ),
              UG: Territory(UG, [KE,TA,RW]          ),
              TA:   Territory(TA,   [UG,KE,RW,BU]        ),
              RW:   Territory(RW,   [UG,TA,BU]                 ),
              BU:   Territory(BU,   [RW,TA]                 ) }

problem = MapColor(australia, colors)

problem.solve(0)

print("\nThe proposed solution by the code becomes as folows:\n",)

for a in problem.vars:
    print(a,"   ",problem.map[a].color)
