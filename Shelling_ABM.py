'''
# Schelling Model
Thomas Schelling (1971) created an agent based model using checker boards to 
simulate the creation of segregated neighborhoods, in a society where no individual 
necessarily has a strong preference for segregation.  To see a simulation with a visual 
component, visit the bottom of this page: http://nifty.stanford.edu/2014/mccown-schelling-model-segregation/
The following code will replicate his model in Python.  
We will not create a visual component in this class, though it is well within 
Python's abilities to do so.  We will use the following guidelines:

1. At least two kinds of agents
2. Each agent needs a preference for similar neighbors
3. Each agent gets to move around if preference not met


The World class has been made for you, take a look and try to understand how it works
Your task is to write a function for Agents 
'''

from numpy import random, mean

params = {'world_size':(20,20),
          'num_agents':380,
          'same_pref_r': 0.4, #red agent's pref for same color neighbours
          'same_pref_b': 0.3, #blue agent's pref for same color neighbours
          'proportion_r': 0.6,
          'max_iter'  :3,
          'print_to_screen': True}  #toggle this T/F to print output

class Agent():
    #An agent needs to know if it is happy, needs to be able to move (find a vacancy and fill
    # it), can either check if it'll be happy in the new location, or not and
    # needs to report to World what it did
    def __init__(self, world, kind, same_pref):
        self.world = world
        self.kind = kind
        self.same_pref = same_pref
        self.location = None
        
    def move(self): 
        if self.kind == 'red':
            if self.am_i_happy() == True:
                return 0
            elif self.am_i_happy() == False:
                if self.world.find_vacant(return_all = True) is not None:
                    return 4
                elif self.world.find_vacant(return_all = True) is None:
                    return 2
        elif self.kind == 'blue':
            if self.am_i_happy() == True:
                return 1
            elif self.am_i_happy() == False:
                if self.world.find_vacant(return_all = True) is not None:
                    return 5
                elif self.world.find_vacant(return_all = True) is None:
                    return 3
        #moves an agent
        #agent has to know if it is happy to decide if it'll move 
        #agent has to be able to find vacancies (use self.world.find_vacant(...))
        #return something that indicates if the agent moved

        #the way it is currently writen:
        #return 4 #red moved
        #return 5 #blue moved
        #return 2 # red unhappy but did not move
        #return 3  # blue unhappy but did not move
        #return 0 # red happy, did not move
        #return 1 # blue happy, did not move        

    def am_i_happy(self, loc=False, neighbor_check=False):
        if neighbor_check == False:
            neighbor_kind = []
            neighbor = self.world.locate_neighbors(self.location)
            for a in self.world.agents:
                if neighbor.count(a.location) == True:
                    neighbor_kind.append(a.kind)
                else:
                    pass
            if self.kind == 'red' and len(neighbor) != 0:
                if neighbor_kind.count('red')/len(neighbor) >= params['same_pref_r']:
                    return True
                else:
                    return False
            elif self.kind == 'blue' and len(neighbor) != 0:
                if neighbor_kind.count('blue')/len(neighbor) >= params['same_pref_b']:
                    return True
                else:
                    return False
            else: 
                return False
        elif neighbor_check == True:
            neighbor_kind = []
            neighbor = self.world.locate_neighbors(self.location)
            for a in self.world.agents:
                if neighbor.count(a.location) == True:
                    neighbor_kind.append(a.kind)
                else:
                    pass
            different_neighbor = []
            for kind in neighbor_kind:
                if kind == self.kind:
                    different_neighbor.append(True)
                else:
                    different_neighbor.append(False)
            return different_neighbor
        #this should return a boolean for whether or not an agent is happy at a location
        #if loc is False, use current location, else use specified location
        #for reporting purposes, allow checking of the current number of similar neighbors

        #if an agent is in a patch with no neighbors at all, treat it as unhappy
        #if len(neighbor_kinds) == 0:
        #    return False
            
    def start_happy_r_b(self):
    #for reporting purposes, allow count of happy before any moves, of red and blue seperately
        if self.am_i_happy and self.kind == 'red':
            return 'a'
        elif self.am_i_happy and self.kind == 'blue':
            return 'b'
        else:
            pass


class World():
    def __init__(self, params):
        assert(params['world_size'][0] * params['world_size'][1] > params['num_agents']), 'Grid too small for number of agents.'
        self.params = params
        self.reports = {}

        self.grid     = self.build_grid(params['world_size'])
        self.agents   = self.build_agents(params['num_agents'], params['same_pref_r'], params['same_pref_b'])

        self.init_world()


    def build_grid(self, world_size):
        #create the world that the agents can move around on
        locations = [(i,j) for i in range(world_size[0]) for j in range(world_size[1])]
        return {l:None for l in locations} #return a dictionary with value 'None'

    def build_agents(self, num_agents, same_pref_r, same_pref_b):
        #generate a list of Agents (with kind and same_preference) that can be iterated over

        def _kind_picker(i):
            if i < round(num_agents * params['proportion_r']):
                return 'red'
            else:
                return 'blue'

        def _pref_picker(i):
            if i < round(num_agents * params['proportion_r']):
                return params['same_pref_r']
            else:
                return params['same_pref_b']
        
        agents = [Agent(self, _kind_picker(i), _pref_picker(i)) for i in range(num_agents)]
        random.shuffle(agents)
        return agents
    

    def init_world(self):
        #a method for all the steps necessary to create the starting point of the model

        for agent in self.agents:
            loc = self.find_vacant()
            self.grid[loc] = agent
            agent.location = loc

        assert(all([agent.location is not None for agent in self.agents])), "Some agents don't have homes!"
        assert(sum([occupant is not None for occupant in self.grid.values()]) == self.params['num_agents']), 'Mismatch between number of agents and number of locations with agents.'

        #set up some reporting dictionaries
        self.reports['integration'] = []
        self.reports['red_integration'] =[]
        self.reports['blue_integration'] = []

    def find_vacant(self, return_all=False):
        #finds all empty patches on the grid and returns a random one, unless kwarg return_all==True,
        #then it returns a list of all empty patches

        empties = [loc for loc, occupant in self.grid.items() if occupant is None]
        if return_all:
            return empties
        else:
            choice_index = random.choice(range(len(empties)))
            return empties[choice_index]

    def locate_neighbors(self, loc):
        #given a location, return a list of all the patches that count as neighbors
        include_corners = True

        x, y = loc
        cardinal_four = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
        if include_corners:
            corner_four = [(x+1, y+1), (x+1, y-1), (x-1, y+1), (x-1, y-1)]
            neighbors = cardinal_four + corner_four
        else:
            neighbors = cardinal_four

        #handle patches that are at the edges, assuming a "torus" shape
        x_max = self.params['world_size'][0] - 1
        y_max = self.params['world_size'][1] - 1

        def _edge_fixer(loc):
            x, y = loc
            if x < 0:
                x = x_max
            elif x > x_max:
                x = 0

            if y < 0:
                y = y_max
            elif y > y_max:
                y = 0

            return (x, y)

        neighbors = [_edge_fixer(loc) for loc in neighbors]
        return neighbors

    def report_integration(self):
        diff_neighbors = []
        diff_neighbours_r = []
        diff_neighbours_b = []
        for agent in self.agents:
            diff_neighbors.append(sum(
                    [not a for a in agent.am_i_happy(neighbor_check=True)]
                                ))
        for agent in self.agents:
            if agent.kind == 'red':
                diff_neighbours_r.append(sum(
                    [not a for a in agent.am_i_happy(neighbor_check=True)]
                                ))
        for agent in self.agents:
            if agent.kind == 'blue':
                diff_neighbours_b.append(sum(
                    [not a for a in agent.am_i_happy(neighbor_check=True)]
                                ))
                

        self.reports['integration'].append(round(mean(diff_neighbors), 2))
        self.reports['red_integration'].append(round(mean(diff_neighbours_r), 2))
        self.reports['blue_integration'].append(round(mean(diff_neighbours_b), 2))


    def run(self): 
        #handle the iterations of the model
        log_of_happy = []
        log_of_happy_r = []
        log_of_happy_b = []
        log_of_moved_r = []
        log_of_moved_b = []
        log_of_moved = []
        log_of_stay  = []
        log_of_stay_r = []
        log_of_stay_b = []

        self.report_integration()
        log_of_happy.append(sum([a.am_i_happy() for a in self.agents])) #starting happiness
        
        happy_results = [agent.start_happy_r_b() for agent in self.agents]
        log_of_happy_r.append(sum([r == 'a' for r in happy_results])) #starting happiness
        log_of_happy_b.append(sum([r == 'b' for r in happy_results])) #starting happiness       
        
        log_of_moved_r.append(0) #no one moved at startup
        log_of_moved_b.append(0) #no one moved at startup

        log_of_stay_r.append(0) #no one stayed at startup
        log_of_stay_b.append(0) #no one stayed at startup

        for iteration in range(self.params['max_iter']):

            random.shuffle(self.agents) #randomize agents before every iteration
            move_results = [agent.move() for agent in self.agents]
            
            self.report_integration()

            num_happy_at_start   =sum([r==0 for r in move_results]) + sum([r==1 for r in move_results])
            num_happy_at_start_r = sum([r==0 for r in move_results])
            num_happy_at_start_b = sum([r==1 for r in move_results])
            num_stayed_unhappy   = sum([r==2 for r in move_results]) + sum([r==3 for r in move_results])
            num_stayed_unhappy_r = sum([r==2 for r in move_results])
            num_stayed_unhappy_b = sum([r==3 for r in move_results])
            num_moved            = sum([r==4 for r in move_results]) + sum([r==5 for r in move_results])
            num_moved_r          = sum([r==4 for r in move_results])
            num_moved_b          = sum([r==5 for r in move_results])

            log_of_happy.append(num_happy_at_start)
            print(log_of_happy)
            log_of_happy_r.append(num_happy_at_start_r)
            log_of_happy_b.append(num_happy_at_start_b)
            log_of_moved.append(num_moved)
            print(log_of_moved)
            log_of_moved_r.append(num_moved_r)
            log_of_moved_b.append(num_moved_b)
            log_of_stay .append(num_stayed_unhappy)
            print(log_of_stay)
            log_of_stay_r.append(num_stayed_unhappy_r)
            log_of_stay_b.append(num_stayed_unhappy_b)

           
            if log_of_happy[-1] == params['num_agents']:
                print('Everyone is happy!  Stopping after iteration {}.'.format(iteration))
                break
            elif log_of_moved[-1] == 0 and log_of_stay[-1] > 0:
                print('Some agents are unhappy, but they cannot find anywhere to move to.  Stopping after iteration {}.'.format(iteration))
                break
            

        self.reports['log_of_happy']   = log_of_happy
        self.reports['log_of_happy_r'] = log_of_happy_r
        self.reports['log_of_happy_b'] = log_of_happy_b
        self.reports['log_of_moved']   = log_of_moved
        self.reports['log_of_moved_r'] = log_of_moved_r
        self.reports['log_of_moved_b'] = log_of_moved_b
        self.reports['log_of_stay']    = log_of_stay
        self.reports['log_of_stay_r']  = log_of_stay_r
        self.reports['log_of_stay_b']  = log_of_stay_b

        self.report(params)

    def report(self, params):
        #report final results after run ends
        reports = self.reports

        if params['print_to_screen']:
            print('\nAll results begin at time=0 and go in order to the end.\n')
            print('The average number of neighbors an agent has not like them:', reports['integration'])
            print('The average number of neighbors a red agent has not like them:', reports['red_integration'])
            print('The average number of neighbors a blue agent has not like them:', reports['blue_integration'])
            print('The number of happy agents:', reports['log_of_happy'])
            print('The number of happy red agents:', reports['log_of_happy_r'])
            print('The number of happy blue agents:', reports['log_of_happy_b'])
            print('The number of red agent moves per turn:', reports['log_of_moved_r'])
            print('The number of blue agent moves per turn:', reports['log_of_moved_b'])
            print('The number of red agents who failed to find a new home:', reports['log_of_stay_r'])
            print('The number of blue agents who failed to find a new home:', reports['log_of_stay_b'])
            


world = World(params)
world.run()


'''
sample output
Everyone is happy!  Stopping after iteration 5.

All results begin at time=0 and go in order to the end.

The average number of neighbors an agent has not like them: [3.67, 1.84, 1.44, 1.37, 1.33, 1.31, 1.31]
The average number of neighbors a red agent has not like them: [3.06, 1.53, 1.2, 1.14, 1.11, 1.09, 1.09]
The average number of neighbors a blue agent has not like them: [4.59, 2.3, 1.8, 1.71, 1.66, 1.64, 1.64]
The number of happy agents: [297, 291, 361, 377, 378, 379, 380]
The number of happy red agents: [228, 184, 217, 227, 228, 228, 228]
The number of happy blue agents: [152, 107, 144, 150, 150, 151, 152]
The number of red agent moves per turn: [0, 44, 11, 1, 0, 0, 0]
The number of blue agent moves per turn: [0, 45, 8, 2, 2, 1, 0]
The number of red agents who failed to find a new home: [0, 0, 0, 0, 0, 0, 0]
The number of blue agents who failed to find a new home: [0, 0, 0, 0, 0, 0, 0]
'''


random.shuffle(world.agents) 
move_results = [agent.move() for agent in world.agents]
happy=sum([a.am_i_happy() for a in world.agents])
different_neighbor = []
for agent in world.agents:
    different_neighbor.append(sum([not a for a in agent.am_i_happy(neighbor_check=True)]))

set(move_results)
set(different_neighbor)


















