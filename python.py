def is_safe(board, row, col, n):
    # Check row on left side
    for i in range(col):
        if board[row][i] == 1: return False
    # Check upper diagonal on left side
    for i, j in zip(range(row, -1, -1), range(col, -1, -1)):
        if board[i][j] == 1: return False
    # Check lower diagonal on left side
    for i, j in zip(range(row, n, 1), range(col, -1, -1)):
        if board[i][j] == 1: return False
    return True

def solve_queens(board, col, n):
    if col >= n: return True
    for i in range(n):
        if is_safe(board, i, col, n):
            board[i][col] = 1
            if solve_queens(board, col + 1, n): return True
            board[i][col] = 0 # Backtrack
    return False

n = 8
board = [[0]*n for _ in range(n)]
if solve_queens(board, 0, n):
    for row in board:
        print(" ".join('Q' if x else '.' for x in row))


----------------------------------------------------------------------
def water_jug_problem(jug1_cap, jug2_cap, target):
    # (jug1, jug2)
    path = []
    visited = set()
    queue = [(0, 0, [])]

    while queue:
        j1, j2, current_path = queue.pop(0)
        if (j1, j2) in visited: continue
        visited.add((j1, j2))
        
        new_path = current_path + [(j1, j2)]
        if j1 == target:
            return new_path

        # Possible transitions
        rules = [
            (jug1_cap, j2), # Fill J1
            (j1, jug2_cap), # Fill J2
            (0, j2),        # Empty J1
            (j1, 0),        # Empty J2
            (j1 - min(j1, jug2_cap - j2), j2 + min(j1, jug2_cap - j2)), # Pour J1 -> J2
            (j1 + min(j2, jug1_cap - j1), j2 - min(j2, jug1_cap - j1))  # Pour J2 -> J1
        ]
        
        for state in rules:
            if state not in visited:
                queue.append((*state, new_path))

result = water_jug_problem(5, 3, 4)
print("Steps to reach 4 gallons in 5L jug:")
for step in result: print(step)
---------------------------------------------------------------------------
def check_tic_tac_toe(board):
    lines = []
    lines.extend(board) # Rows
    lines.extend([[board[r][c] for r in range(3)] for c in range(3)]) # Columns
    lines.append([board[i][i] for i in range(3)]) # Main Diagonal
    lines.append([board[i][2-i] for i in range(3)]) # Anti-Diagonal

    for line in lines:
        if line[0] != ' ' and all(s == line[0] for s in line):
            return line[0] # Returns 'X' or 'O'
    
    if all(' ' not in row for row in board):
        return "Draw"
    
    return None # Game still on

def print_board(board):
    print("\n  0 1 2")
    for i, row in enumerate(board):
        print(f"{i} {'|'.join(row)}")
        if i < 2: print("  -----")

# Initialize empty board
board = [[' ' for _ in range(3)] for _ in range(3)]
current_player = 'X'

print("Tic-Tac-Toe Manual Input")
print("Enter coordinates as: row column (e.g., 0 2)")

while True:
    print_board(board)
    try:
        user_input = input(f"Player {current_player}, enter move: ").split()
        row, col = int(user_input[0]), int(user_input[1])

        if board[row][col] != ' ':
            print("Position already taken! Try again.")
            continue
            
        board[row][col] = current_player
    except (ValueError, IndexError):
        print("Invalid input. Please enter numbers between 0 and 2.")
        continue

    # Check status
    status = check_tic_tac_toe(board)
    if status:
        print_board(board)
        if status == "Draw":
            print("It's a Draw!")
        else:
            print(f"Congratulations! Player {status} wins!")
        break

    # Switch players
    current_player = 'O' if current_player == 'X' else 'X'
---------------------------------------------------------------------------------
import heapq

def uniform_cost_search(graph, start, goal):
    # priority queue: (cumulative_cost, current_node, path)
    pq = [(0, start, [start])]
    visited = {} # node: minimum_cost_to_reach

    print(f"Starting UCS from {start} to {goal}...")
    
    while pq:
        cost, node, path = heapq.heappop(pq)

        # Goal check
        if node == goal:
            return path, cost

        # Standard UCS: Only expand if we found a shorter path to this node
        if node in visited and visited[node] <= cost:
            continue
        visited[node] = cost

        for neighbor, weight in graph.get(node, []):
            new_cost = cost + weight
            heapq.heappush(pq, (new_cost, neighbor, path + [neighbor]))

    return None, float('inf')

# Graph definition from image (node: [(neighbor, edge_weight), ...])
graph = {
    'a': [('b', 4), ('c', 3)],
    'b': [('f', 5), ('e', 12)],
    'c': [('e', 10), ('d', 7)],
    'd': [('e', 2)],
    'e': [('z', 5)],
    'f': [('z', 16)]
}

path, total_cost = uniform_cost_search(graph, 'a', 'z')
print(f"Optimal Path: {' -> '.join(path)}")
print(f"Total Path Cost: {total_cost}")
--------------------------------------------------------------------------
import heapq

def a_star_search(graph, heuristics, start, goal):
    # priority queue: (f_score, g_score, current_node, path)
    # f_score = g_score + heuristic
    pq = [(heuristics[start], 0, start, [start])]
    visited = {}

    print(f"Starting A* Search from {start} to {goal}...")

    while pq:
        f_score, g_score, node, path = heapq.heappop(pq)

        if node == goal:
            return path, g_score

        if node in visited and visited[node] <= g_score:
            continue
        visited[node] = g_score

        for neighbor, weight in graph.get(node, []):
            new_g_score = g_score + weight
            new_f_score = new_g_score + heuristics[neighbor]
            heapq.heappush(pq, (new_f_score, new_g_score, neighbor, path + [neighbor]))

    return None, float('inf')

# Data from image
graph = {
    'a': [('b', 4), ('c', 3)],
    'b': [('f', 5), ('e', 12)],
    'c': [('e', 10), ('d', 7)],
    'd': [('e', 2)],
    'e': [('z', 5)],
    'f': [('z', 16)]
}

heuristics = {
    'a': 14, 'b': 12, 'c': 11, 'd': 6, 'e': 4, 'f': 11, 'z': 0
}

path, total_cost = a_star_search(graph, heuristics, 'a', 'z')
print(f"Optimal Path: {' -> '.join(path)}")
print(f"Actual Cost (g): {total_cost}")
-----------------------------------------------------------------------------------------
tree = {
    'D': ['A', 'G'],
    'A': ['C'],
    'G': ['B', 'H'],
    'C': ['E', 'F'],
    'B': [], 'H': [], 'E': [], 'F': []
}

def bfs(start_node):
    visited, queue = [], [start_node]
    while queue:
        node = queue.pop(0)
        if node not in visited:
            visited.append(node)
            queue.extend(tree[node])
    return visited

def dfs(start_node, visited=None):
    if visited is None: visited = []
    visited.append(start_node)
    for neighbor in tree[start_node]:
        dfs(neighbor, visited)
    return visited

print("BFS Order:", bfs('D'))
print("DFS Order:", dfs('D'))

-----------------------------------------------------------------------------------
class WumpusWorld:
    def __init__(self):
        self.size = 4
        self.pit = (1, 3)
        self.wumpus = (3, 3)
        self.gold = (4, 4)
        self.agent_pos = (1, 1)
        self.visited = [(1, 1)]

    def display_grid(self, step_num):
        print(f"\n--- Step {step_num} ---")
        print("-" * 17)
        # Printing from top row (size) down to bottom (1)
        for r in range(self.size, 0, -1):
            row_str = "| "
            for c in range(1, self.size + 1):
                if (r, c) == self.agent_pos:
                    cell = "A"
                elif (r, c) == self.pit:
                    cell = "P"
                elif (r, c) == self.wumpus:
                    cell = "W"
                elif (r, c) == self.gold:
                    cell = "G"
                else:
                    cell = "."
                row_str += cell + " | "
            print(row_str)
            print("-" * 17)

    def get_percepts(self, pos):
        percepts = []
        r, c = pos
        adj = [(r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)]
        for nr, nc in adj:
            if (nr, nc) == self.pit: 
                percepts.append("Breeze")
            if (nr, nc) == self.wumpus: 
                percepts.append("Stench")
        return list(set(percepts))

    def play(self):
        step = 0
        path = [self.agent_pos]
        
        while self.agent_pos != self.gold:
            self.display_grid(step)
            percepts = self.get_percepts(self.agent_pos)
            print(f"Location: {self.agent_pos} | Percepts: {percepts if percepts else 'None'}")
            
            r, c = self.agent_pos
            # Prioritize moving Up and Right to reach (4,4)
            possible_moves = [(r + 1, c), (r, c + 1), (r - 1, c), (r, c - 1)]
            moved = False
            
            for move in possible_moves:
                nr, nc = move
                # Check grid boundaries
                if 1 <= nr <= self.size and 1 <= nc <= self.size:
                    # Logic: Avoid Pits, Wumpus, and already visited squares
                    if move != self.pit and move != self.wumpus and move not in self.visited:
                        self.agent_pos = move
                        self.visited.append(self.agent_pos)
                        path.append(self.agent_pos)
                        moved = True
                        step += 1
                        break
            
            if not moved:
                print("\nAgent stuck! No safe unexplored squares available.")
                break
        
        if self.agent_pos == self.gold:
            self.display_grid(step)
            print(f"Success! Gold reached at {self.gold}")
            print(f"Final Path: {path}")

# Run the game
game = WumpusWorld()
game.play()

----------------------------------------------------------------------------------------

class PredicateLogSystem:
    def __init__(self):
        self.facts = {}
        self.rules = []

    # Add fact
    def add_fact(self, predicate, value):
        self.facts.setdefault(predicate, [])
        if value not in self.facts[predicate]:
            self.facts[predicate].append(value)

    # Add rule
    def add_rule(self, premise, conclusion):
        self.rules.append((premise, conclusion))

    # Inference (Forward Chaining)
    def infer(self):
        changed = True
        while changed:
            changed = False
            for premise, conclusion in self.rules:
                if premise in self.facts:
                    for val in self.facts[premise]:
                        self.facts.setdefault(conclusion, [])
                        if val not in self.facts[conclusion]:
                            self.facts[conclusion].append(val)
                            changed = True

    # Query
    def query(self, predicate, value):
        return value in self.facts.get(predicate, [])

    # Display facts
    def show_facts(self):
        print("\nCurrent Facts:")
        for p, v in self.facts.items():
            print(f"{p} : {v}")


# Main Program
kb = PredicateLogSystem()

while True:
    print("\n===== Predicate Logic System =====")
    print("1. Add Fact")
    print("2. Add Rule (IF -> THEN)")
    print("3. Inference")
    print("4. Query")
    print("5. Show Facts")
    print("6. Exit")

    choice = input("Enter your choice: ")

    if choice == '1':
        pred = input("Enter predicate: ")
        val = input("Enter value: ")
        kb.add_fact(pred, val)
        print("Fact added successfully!")

    elif choice == '2':
        premise = input("IF (Predicate): ")
        conclusion = input("THEN (Predicate): ")
        kb.add_rule(premise, conclusion)
        print(f"Rule added: {premise} -> {conclusion}")

    elif choice == '3':
        kb.infer()
        print("Inference completed!")

    elif choice == '4':
        pred = input("Enter predicate: ")
        val = input("Enter value: ")
        if kb.query(pred, val):
            print("True")
        else:
            print("False")

    elif choice == '5':
        kb.show_facts()

    elif choice == '6':
        print("Exiting program...")
        break

    else:
        print("Invalid choice! Please try again.")

-----------------------------------------------------------------------------------------

from collections import deque

# State representation
class State:
    def __init__(self, monkey, box, on_box, has_banana):
        self.monkey = monkey
        self.box = box
        self.on_box = on_box
        self.has_banana = has_banana

    def __repr__(self):
        return f"(Monkey:{self.monkey}, Box:{self.box}, OnBox:{self.on_box}, Banana:{self.has_banana})"

    def __eq__(self, other):
        return (self.monkey == other.monkey and
                self.box == other.box and
                self.on_box == other.on_box and
                self.has_banana == other.has_banana)

    def __hash__(self):
        return hash((self.monkey, self.box, self.on_box, self.has_banana))


positions = ['A', 'B', 'C']   # C = banana position


# Generate next possible states
def get_next_states(state):
    next_states = []

    # WALK
    if not state.on_box:
        for p in positions:
            if p != state.monkey:
                new_state = State(p, state.box, False, state.has_banana)
                next_states.append(("Walk to " + p, new_state))

    # PUSH BOX
    if not state.on_box and state.monkey == state.box:
        for p in positions:
            if p != state.box:
                new_state = State(p, p, False, state.has_banana)
                next_states.append(("Push box to " + p, new_state))

    # CLIMB
    if not state.on_box and state.monkey == state.box:
        new_state = State(state.monkey, state.box, True, state.has_banana)
        next_states.append(("Climb box", new_state))

    # GRASP
    if state.on_box and state.monkey == 'C' and state.box == 'C':
        new_state = State(state.monkey, state.box, True, True)
        next_states.append(("Grasp banana", new_state))

    return next_states


# BFS Planning
def monkey_banana():
    initial_state = State('A', 'B', False, False)
    queue = deque([(initial_state, [])])
    visited = set([initial_state])

    while queue:
        state, path = queue.popleft()

        if state.has_banana:
            return path

        for action, new_state in get_next_states(state):
            if new_state not in visited:
                visited.add(new_state)
                queue.append((new_state, path + [(state, action, new_state)]))

    return None


# Execute
plan = monkey_banana()

print("Solution Steps:\n")

if plan is None:
    print("No solution found.")
else:
    for i, step in enumerate(plan, 1):
        current_state, action, next_state = step
        print(f"Step {i}:")
        print("Current State :", current_state)
        print("Action        :", action)
        print("Next State    :", next_state)
        print()

-----------------------------------------------------------------------------------

