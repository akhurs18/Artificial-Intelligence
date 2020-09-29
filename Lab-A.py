import collections

# Very basic class for implementing the tree (Source: StackOverflow).
class Node(object):
    def __init__(self, data, parent=None, gScore = 0):
        self._data = data
        self._parent = parent
        self._children = []
        self._direction = None
        self._md = 0
        self._gScore = 0
        
    def add_child(self, obj):
        self._children.append(obj)

# Basic state representation class.
class State():
    def __init__(self):
        self._mouse = (0, 0)
        self._prizes = []
        self._prizes_archive = []
        self._total_cost = 0
    
    def _convertMaze(self, file):
        """Takes a file and converts it into a two-dimensional array."""
        maze = []
        open_file = open(file, "r")
        read_file = open_file.read()
        split_file = read_file.split("\n")
        for x in split_file:
            maze.append(list(x))
        return maze
 
    def _move(self, state, maze, command):
        """Takes a state node, a maze, and a command to make the mouse move one space."""
        if command == "East":
            maze[state._mouse[0]][state._mouse[1]+1] = "P"
            maze[state._mouse[0]][state._mouse[1]] = "#"
            state._mouse = (state._mouse[0], state._mouse[1]+1)
            state._total_cost += 1
        if command == "West":
            maze[state._mouse[0]][state._mouse[1]-1] = "P"
            maze[state._mouse[0]][state._mouse[1]] = "#"
            state._mouse = (state._mouse[0], state._mouse[1]-1)
            state._total_cost += 1
        if command == "North":
            maze[state._mouse[0]-1][state._mouse[1]] = "P"
            maze[state._mouse[0]][state._mouse[1]] = "#"
            state._mouse = (state._mouse[0]-1, state._mouse[1])
            state._total_cost += 1
        if command == "South":
            maze[state._mouse[0]+1][state._mouse[1]] = "P"
            maze[state._mouse[0]][state._mouse[1]] = "#"
            state._mouse = (state._mouse[0]+1, state._mouse[1])
            state._total_cost += 1

    def closest_prize_fScore(self, space, gScore):
        """Determines the closest prize to the mouse using the Manhattan distance (for part 3)."""
        closest_prize = 1000000
        prize_coordinate = (0, 0)
        for i in self._prizes:
            i_distance = (self.return_md(space, i) + gScore)
            if i_distance < closest_prize:
                prize_coordinate = i
        return prize_coordinate
    
    def return_md(self, space, prize):
        """Takes a node and a prize coordinate and prints out the Manhattan distance between the two."""
        return abs(space[0] - prize[0]) + abs(space[1] - prize[1])

def goal_test(state):
    """Takes a state and checks if a goal state has been reached."""
    if len(state._prizes) != 0:
        return False
    else:
        return True
    
#---------------------------------------------------------------------------------------    
    
def single_dfs(file):
    """Takes a .txt file representing a SINGLE-PRIZE maze and prints a workable solution using DFS (depth-first search)."""
    # State Representation Scheme
    state = State()
    # Opens and reads the maze file.
    maze = state._convertMaze(file)
    
    # Necessary tables:
    stack = [] # Stack for implementing DFS.
    visited = [] # Keeps track of visited nodes for DFS.
    path = [] # Where the final path for the mouse will be stored.
    nodes_expanded = 0
    
    # This block finds the mouse's location and the prizes.
    for i in maze:
        if "P" in i:
            state._mouse = (maze.index(i), i.index("P"))
        if "." in i:
            state._prizes.append((maze.index(i), i.index(".")))
            state._prizes_archive.append((maze.index(i), i.index(".")))
    
    # This block implements depth-first search. (Used pseudocode from textbook as outline).
    root = Node(state._mouse)
    stack.append(root)
    
    while stack:
        cursor = stack.pop()
        nodes_expanded += 1
        if cursor._data in state._prizes: # Checks if the current node is the goal node.
            end = cursor
            if goal_test(state) == True: # Checking for multiple prizes.
                break
            else:
                continue
        else:
            if cursor._data not in visited:
                visited.append(cursor._data)

                if maze[cursor._data[0]-1][cursor._data[1]] != "%":
                    n = Node((cursor._data[0]-1, cursor._data[1]))
                    n._parent = cursor
                    n._direction = "North"
                    cursor.add_child(n)
                    stack.append(n)
                else:
                    n = Node((cursor._data[0],cursor._data[1]))
                    n._parent = cursor
                    n._direction = "North"
                    cursor.add_child(n)
                    
                if maze[cursor._data[0]+1][cursor._data[1]] != "%": 
                    s = Node((cursor._data[0]+1, cursor._data[1]))
                    s._parent = cursor
                    s._direction = "South"
                    cursor.add_child(s)
                    stack.append(s)
                else:
                    s = Node((cursor._data[0]+1, cursor._data[1]))
                    s._parent = cursor
                    s._direction = "South"
                    cursor.add_child(s)

                if maze[cursor._data[0]][cursor._data[1]+1] != "%": 
                    e = Node((cursor._data[0], cursor._data[1]+1))
                    cursor.add_child(e)
                    e._parent = cursor
                    e._direction = "East"
                    stack.append(e)
                else:
                    e = Node((cursor._data[0], cursor._data[1]))
                    cursor.add_child(e)
                    e._direction = "East"
                    e._parent = cursor

                if maze[cursor._data[0]][cursor._data[1]-1] != "%":
                    w = Node((cursor._data[0], cursor._data[1]-1))
                    cursor.add_child(w)
                    w._parent = cursor
                    w._direction = "West"
                    stack.append(w)
                else:
                    w = Node((cursor._data[0], cursor._data[1]))
                    cursor.add_child(w)
                    w._direction = "West"
                    w._parent = cursor
    
    # This block prints the output, including instructions the mouse's chosen path and the finished maze.    
    cursor = end
    path.append(cursor._direction)
    while cursor._parent._direction != None:
        cursor = cursor._parent
        path.append(cursor._direction)
    for i in reversed(path):
        state._move(state, maze, i)
    for i in range(0, len(maze)):
        print("".join(maze[i]))
    print("Step Cost:", state._total_cost)
    print("Nodes Expanded:", nodes_expanded)

#---------------------------------------------------------------------------------------

def single_bfs(file):
    """Takes a .txt file representing a SINGLE-PRIZE MAZE and prints a workable solution using BFS (breadth-first search)."""
    state = State() # State Representation Scheme
    maze = state._convertMaze(file) # Opens and reads the maze file.
    
    # Necessary storage:
    queue = collections.deque([]) # Stack for implementing DFS.
    visited = [] # Keeps track of visited nodes for DFS.
    path = [] # Where the final path for the mouse will be stored.
    nodes_expanded = 0 #How many nodes the tree had to expand to reach the goal.
    
    # This block finds the mouse's location and the prizes.
    for i in maze:
        if "P" in i:
            state._mouse = (maze.index(i), i.index("P"))
        if "." in i:
            state._prizes.append((maze.index(i), i.index(".")))
            state._prizes_archive.append((maze.index(i), i.index(".")))
    
    # This block implements breadth-first search.
    root = Node(state._mouse)
    queue.append(root)
    
    while queue:
        cursor = queue.popleft()
        nodes_expanded += 1
        if cursor._data in state._prizes: # Checks if the current node is the goal node.
            end = cursor
            state._prizes.pop()
            if goal_test(state) == True: # Checking for multiple prizes.
                break
            else:
                continue
        else:
            if cursor._data not in visited:
                visited.append(cursor._data)
                
                # Checks if mouse can go North.
                if maze[cursor._data[0]-1][cursor._data[1]] != "%":
                    n = Node((cursor._data[0]-1, cursor._data[1]))
                    n._parent = cursor
                    n._direction = "North"
                    cursor.add_child(n)
                    queue.append(n)
                else:
                    n = Node((cursor._data[0],cursor._data[1]))
                    n._parent = cursor
                    n._direction = "North"
                    cursor.add_child(n)
                    
                # Checks if mouse can go South.    
                if maze[cursor._data[0]+1][cursor._data[1]] != "%": 
                    s = Node((cursor._data[0]+1, cursor._data[1]))
                    s._parent = cursor
                    s._direction = "South"
                    cursor.add_child(s)
                    queue.append(s)
                else:
                    s = Node((cursor._data[0]+1, cursor._data[1]))
                    s._parent = cursor
                    s._direction = "South"
                    cursor.add_child(s)
                    
                # Checks if mouse can go East.
                if maze[cursor._data[0]][cursor._data[1]+1] != "%": 
                    e = Node((cursor._data[0], cursor._data[1]+1))
                    cursor.add_child(e)
                    e._parent = cursor
                    e._direction = "East"
                    queue.append(e)
                else:
                    e = Node((cursor._data[0], cursor._data[1]))
                    cursor.add_child(e)
                    e._direction = "East"
                    e._parent = cursor
                    
                # Checks if mouse can go West.
                if maze[cursor._data[0]][cursor._data[1]-1] != "%":
                    w = Node((cursor._data[0], cursor._data[1]-1))
                    cursor.add_child(w)
                    w._parent = cursor
                    w._direction = "West"
                    queue.append(w)
                else:
                    w = Node((cursor._data[0], cursor._data[1]))
                    cursor.add_child(w)
                    w._direction = "West"
                    w._parent = cursor
    
    # This block prints the output, including instructions the mouse's chosen path and the finished maze.
    path.append(cursor._direction)
    while cursor._parent._direction != None:
        cursor = cursor._parent
        path.append(cursor._direction)
    for i in reversed(path):
        state._move(state, maze, i)
    for i in range(0, len(maze)):
        print("".join(maze[i]))
    print("Step Cost:", state._total_cost)
    print("Nodes Expanded:", nodes_expanded)

#--------------------------------------------------------------------------------------- 

def single_gbfs(file):
    """Takes a .txt file representing a SINGLE-PRIZE MAZE and prints a workable solution using greedy best-first search)."""
    state = State() # State Representation Scheme
    maze = state._convertMaze(file) # Opens and reads the maze file.   
    
    # Necessary variables:
    next_node = None
    next_dir = ""
    queue = []
    visited = [] # Keeps track of visited nodes.
    path = [] # Where the final path for the mouse will be stored.
    nodes_expanded = 0 #How many nodes the tree had to expand to reach the goal.
    
    # This block finds the mouse's location and the prizes.
    for i in maze:
        if "P" in i:
            state._mouse = (maze.index(i), i.index("P"))
        if "." in i:
            state._prizes.append((maze.index(i), i.index(".")))
            state._prizes_archive.append((maze.index(i), i.index(".")))
    
    # This block implements greedy best-first search.
    root = Node(state._mouse)
    queue.append(root)
    
    while queue:
        cursor = queue[0]
        for j in queue:
            if j._md <= cursor._md:
                cursor = j
        queue.remove(cursor)
        
        nodes_expanded += 1
        if cursor._data == state._prizes[0]: # Checks if the current node is the goal node.
            state._prizes.remove(cursor._data)
            if goal_test(state) == True: # Checking for multiple prizes.
                end = cursor
                break
        
        if cursor._data not in visited:
            visited.append(cursor._data)

            # Checks if mouse can go North.
            if maze[cursor._data[0]-1][cursor._data[1]] != "%":
                n = Node((cursor._data[0]-1, cursor._data[1]))
                n._parent = cursor
                n._direction = "North"
                n._md = state.return_md(n._data, state._prizes[0])
                cursor.add_child(n)
                queue.append(n)
            else:
                n = Node((cursor._data[0],cursor._data[1]))
                n._parent = cursor
                n._direction = "North"
                n._md = state.return_md(n._data, state._prizes[0])
                cursor.add_child(n)

            # Checks if mouse can go South.    
            if maze[cursor._data[0]+1][cursor._data[1]] != "%": 
                s = Node((cursor._data[0]+1, cursor._data[1]))
                s._parent = cursor
                s._direction = "South"
                s._md = state.return_md(s._data, state._prizes[0])
                cursor.add_child(s)
                queue.append(s)
            else:
                s = Node((cursor._data[0]+1, cursor._data[1]))
                s._parent = cursor
                s._direction = "South"
                s._md = state.return_md(s._data, state._prizes[0])
                cursor.add_child(s)

            # Checks if mouse can go East.
            if maze[cursor._data[0]][cursor._data[1]+1] != "%": 
                e = Node((cursor._data[0], cursor._data[1]+1))
                cursor.add_child(e)
                e._parent = cursor
                e._direction = "East"
                e._md = state.return_md(e._data, state._prizes[0])
                queue.append(e)
            else:
                e = Node((cursor._data[0], cursor._data[1]))
                cursor.add_child(e)
                e._direction = "East"
                e._md = state.return_md(e._data, state._prizes[0])
                e._parent = cursor

            # Checks if mouse can go West.
            if maze[cursor._data[0]][cursor._data[1]-1] != "%":
                w = Node((cursor._data[0], cursor._data[1]-1))
                cursor.add_child(w)
                w._parent = cursor
                w._direction = "West"
                w._md = state.return_md(w._data, state._prizes[0])
                queue.append(w)
            else:
                w = Node((cursor._data[0], cursor._data[1]))
                cursor.add_child(w)
                w._direction = "West"
                w._md = state.return_md(w._data, state._prizes[0])
                w._parent = cursor

    
    # This block prints the output, including instructions the mouse's chosen path and the finished maze.
    
    path.append(cursor._direction)
    while cursor._parent._direction != None:
        cursor = cursor._parent
        path.append(cursor._direction)
    for i in reversed(path):
        state._move(state, maze, i)
    for i in range(0, len(maze)):
        print("".join(maze[i]))
    print("Step Cost:", state._total_cost)
    print("Nodes Expanded:", nodes_expanded)
        
#---------------------------------------------------------------------------------------       
        
def single_astar(file):
    """Takes a .txt file representing a SINGLE-PRIZE MAZE and prints a workable solution using A* search)."""
    state = State() # State Representation Scheme
    maze = state._convertMaze(file) # Opens and reads the maze file.   
    
    # Necessary variables:
    next_node = None
    next_dir = ""
    frontier = []
    visited = [] # Keeps track of visited nodes.
    path = [] # Where the final path for the mouse will be stored.
    nodes_expanded = 0 #How many nodes the tree had to expand to reach the goal.
    
    # This block finds the mouse's location and the prizes.
    for i in maze:
        if "P" in i:
            state._mouse = (maze.index(i), i.index("P"))
        if "." in i:
            state._prizes.append((maze.index(i), i.index(".")))
            state._prizes_archive.append((maze.index(i), i.index(".")))
    
    # This block implements greedy best-first search.
    root = Node(state._mouse)
    md = state.return_md(root._data, state._prizes[0])
    frontier.append(root)

    while frontier:
        cursor = frontier[0]
        for j in frontier:
            if (j._md + j._gScore) < (cursor._md + cursor._gScore):
                cursor = j
        
        frontier.remove(cursor)
        nodes_expanded += 1 
    
        if cursor._data == state._prizes[0]: # Checks if the current node is the goal node.
            state._prizes.remove(cursor._data)
            if goal_test(state) == True: # Checking for multiple prizes.
                end = cursor
                break
             
        if cursor._data not in visited:
            visited.append(cursor._data)
            
            # Checks if mouse can go North.
            if maze[cursor._data[0]-1][cursor._data[1]] != "%":
                n = Node((cursor._data[0]-1, cursor._data[1]))
                n._parent = cursor
                n._direction = "North"
                n._md = state.return_md(n._data, state._prizes[0])
                n._gScore = cursor._gScore + 1
                cursor.add_child(n)
                frontier.append(n)
            else:
                n = Node((cursor._data[0],cursor._data[1]))
                n._parent = cursor
                n._direction = "North"
                n._md = state.return_md(n._data, state._prizes[0])
                n._gScore = cursor._gScore

            # Checks if mouse can go South.    
            if maze[cursor._data[0]+1][cursor._data[1]] != "%": 
                s = Node((cursor._data[0]+1, cursor._data[1]))
                cursor.add_child(s)
                s._parent = cursor
                s._direction = "South"
                s._md = state.return_md(s._data, state._prizes[0])
                s._gScore = cursor._gScore + 1
                frontier.append(s)
            else:
                s = Node((cursor._data[0]+1, cursor._data[1]))
                s._parent = cursor
                s._direction = "South"
                s._md = state.return_md(s._data, state._prizes[0])
                s._gScore = cursor._gScore
                s._gScore = cursor._gScore

            # Checks if mouse can go East.
            if maze[cursor._data[0]][cursor._data[1]+1] != "%": 
                e = Node((cursor._data[0], cursor._data[1]+1))
                cursor.add_child(e)
                e._parent = cursor
                e._direction = "East"
                e._md = state.return_md(e._data, state._prizes[0])
                e._gScore = cursor._gScore + 1
                frontier.append(e)
            else:
                e = Node((cursor._data[0], cursor._data[1]))
                e._direction = "East"
                e._md = state.return_md(e._data, state._prizes[0])
                e._gScore = cursor._gScore
                e._parent = cursor

            # Checks if mouse can go West.
            if maze[cursor._data[0]][cursor._data[1]-1] != "%":
                w = Node((cursor._data[0], cursor._data[1]-1))
                cursor.add_child(w)
                w._parent = cursor
                w._direction = "West"
                w._md = state.return_md(w._data, state._prizes[0])
                w._gScore = cursor._gScore + 1
                frontier.append(w)
            else:
                w = Node((cursor._data[0], cursor._data[1]))
                w._direction = "West"
                w._md = state.return_md(w._data, state._prizes[0])
                w._gScore = cursor._gScore
                w._parent = cursor
            

    
    # This block prints the output, including instructions the mouse's chosen path and the finished maze.
    
    path.append(cursor._direction)
    while cursor._parent:
        cursor = cursor._parent
        path.append(cursor._direction)
    for i in reversed(path):
        state._move(state, maze, i)
    for i in range(0, len(maze)):
        print("".join(maze[i]))
    print("Step Cost:", state._total_cost)
    print("Nodes Expanded:", nodes_expanded)
    
    # This block prints the output, including instructions the mouse's chosen path and the finished maze.
    
#---------------------------------------------------------------------------------------    
    
def multi_astar(file):
    """Takes a .txt file representing a MULTI-PRIZE MAZE and prints a workable solution using A* search)."""
    state = State() # State Representation Scheme
    maze = state._convertMaze(file) # Opens and reads the maze file.
    
    width = len(maze[0])
    height = len(maze)
    
    # Necessary variables:
    next_node = None
    next_dir = ""
    frontier = []
    visited = [] # Keeps track of visited nodes.
    path = [] # Where the final path for the mouse will be stored.
    nodes_expanded = 0 #How many nodes the tree had to expand to reach the goal.
    
    # This block finds the mouse's location and the prizes.
    for i in range(0, height-1):
        for k in range(0, width-1):
            if maze[i][k] == "P":
                state._mouse = (i, k)
            if maze[i][k] == ".":
                state._prizes.append((i, k))
                state._prizes_archive.append((i, k))
    
    root = Node(state._mouse)
    md = state.return_md(root._data, state._prizes[0])
    frontier.append(root)
    current_prize = state.closest_prize_fScore(root._data, root._gScore)

    while frontier:
        cursor = frontier[0]
        for j in frontier:
            if (j._md + j._gScore) < (cursor._md + cursor._gScore):
                cursor = j
        
        frontier.remove(cursor)
        nodes_expanded += 1 
    
        if cursor._data in state._prizes: # Checks if the current node is the goal node.
            state._prizes.remove(cursor._data)
            visited = []
            if goal_test(state) == True: # Checking for multiple prizes.
                end = cursor
                break
            else:
                current_prize = state.closest_prize_fScore(cursor._data, cursor._gScore)
                frontier = [cursor]
                continue
             
        if cursor._data not in visited:
            visited.append(cursor._data)
            
            # Checks if mouse can go North.
            if maze[cursor._data[0]-1][cursor._data[1]] != "%":
                n = Node((cursor._data[0]-1, cursor._data[1]))
                n._parent = cursor
                n._direction = "North"
                n._md = state.return_md(n._data, current_prize)
                n._gScore = cursor._gScore + 1
                cursor.add_child(n)
                frontier.append(n)
            else:
                n = Node((cursor._data[0],cursor._data[1]))
                n._parent = cursor
                n._direction = "North"
                n._md = state.return_md(n._data, current_prize)
                n._gScore = cursor._gScore

            # Checks if mouse can go South.    
            if maze[cursor._data[0]+1][cursor._data[1]] != "%": 
                s = Node((cursor._data[0]+1, cursor._data[1]))
                cursor.add_child(s)
                s._parent = cursor
                s._direction = "South"
                s._md = state.return_md(s._data, current_prize)
                s._gScore = cursor._gScore + 1
                frontier.append(s)
            else:
                s = Node((cursor._data[0]+1, cursor._data[1]))
                s._parent = cursor
                s._direction = "South"
                s._md = state.return_md(s._data, current_prize)
                s._gScore = cursor._gScore
                s._gScore = cursor._gScore

            # Checks if mouse can go East.
            if maze[cursor._data[0]][cursor._data[1]+1] != "%": 
                e = Node((cursor._data[0], cursor._data[1]+1))
                cursor.add_child(e)
                e._parent = cursor
                e._direction = "East"
                e._md = state.return_md(e._data, current_prize)
                e._gScore = cursor._gScore + 1
                frontier.append(e)
            else:
                e = Node((cursor._data[0], cursor._data[1]))
                e._direction = "East"
                e._md = state.return_md(e._data, current_prize)
                e._gScore = cursor._gScore
                e._parent = cursor

            # Checks if mouse can go West.
            if maze[cursor._data[0]][cursor._data[1]-1] != "%":
                w = Node((cursor._data[0], cursor._data[1]-1))
                cursor.add_child(w)
                w._parent = cursor
                w._direction = "West"
                w._md = state.return_md(w._data, current_prize)
                w._gScore = cursor._gScore + 1
                frontier.append(w)
            else:
                w = Node((cursor._data[0], cursor._data[1]))
                w._direction = "West"
                w._md = state.return_md(w._data, current_prize)
                w._gScore = cursor._gScore
                w._parent = cursor
    
    # This block prints the output, including instructions the mouse's chosen path and the finished maze.
    
    path.append(cursor._direction)
    while cursor._parent._direction:
        cursor = cursor._parent
        path.append(cursor._direction)
    for i in reversed(path):
        state._move(state, maze, i)
    for i in range(0, len(maze)):
        print("".join(maze[i]))
    print("Step Cost:", state._total_cost)
    print("Nodes Expanded:", nodes_expanded)
          
if __name__ == "__main__":
    door = 1
    while door == 1:
        print("What's the name of your maze file? (example: file_name.txt)")
        file = input("File Name: ")
        type(file)
        if ".txt" not in file:
            print("Please include .txt in your input.")
        else:
            try:
                f = open(file)
            except IOError:
                print("File not accessible")
            else:
                print("")
                print("Type the number corresponding to the search algorithm you would like to use.")
                print("  1. single_dfs()")
                print("  2. single_bfs()")
                print("  3. single_gbfs()")
                print("  4. single_astar()")
                print("  5. multi-astar()")
                print("")
                function = int(input("Chosen Algorithm: "))
                type(function)
                print("")
                if function == 1:
                      single_dfs(file)
                elif function == 2:
                      single_bfs(file)
                elif function == 3:
                      single_gbfs(file)
                elif function == 4:
                      single_astar(file)
                elif function == 5:
                      multi_astar(file)
                else:
                      print("Not a valid input.")
                print("")
                print("Would you like to try again?")
                print("   1. Yes")
                print("   2. No")
                answer = int(input("Answer: "))
                if answer == 2:
                    door = 0
                    print("")
                    print("Thank you.")
                    break
                else:
                    print("")
                    continue