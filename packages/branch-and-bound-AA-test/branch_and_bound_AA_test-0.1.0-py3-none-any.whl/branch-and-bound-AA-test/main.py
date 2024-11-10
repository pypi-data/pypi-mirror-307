from collections import deque
import networkx as nx
import matplotlib.pyplot as plt

class Node:
    def __init__(self, level=-1, profit=0, weight=0, parent=None):
        self.level = level    # levels in the decision tree
        self.profit = profit 
        self.weight = weight 
        self.bound = 0        # upper bound on max profit for the node
        self.parent = parent

def bound(node, n, W, items):
    if node.weight >= W:
        return 0

    profit_bound = node.profit
    j = node.level + 1
    total_weight = node.weight

    # try to add items while total weight does not exceed capacity
    while j < n and total_weight + items[j][1] <= W:
        total_weight += items[j][1]
        profit_bound += items[j][0]
        j += 1
    # if we can't add more items, add a fraction of the next item to bound
    if j < n:
        profit_bound += (W - total_weight) * (items[j][0] / items[j][1])

    return profit_bound

def knapsack_branch_and_bound(W, items):
    items.sort(key=lambda x: x[0] / x[1], reverse=True)  # sort items by value-to-weight ratio
    n = len(items)
    Q = deque()  # queue for nodes
    u = Node()
    Q.append(u)

    max_profit = 0
    best_node = None
    ###Visualise
    G = nx.DiGraph()
    node_labels = {}

    while Q:
        u = Q.popleft()  #get the node
        # identify the level of the node
        if u.level == -1:
            v = Node(0)
        elif u.level == n - 1:
            continue
        else:
            v = Node(u.level + 1)
        # take the next item (move down the tree)
        v.weight = u.weight + items[v.level][1]
        v.profit = u.profit + items[v.level][0]
        # update max profit
        if v.weight <= W and v.profit > max_profit:
            max_profit = v.profit
            best_node = v
        # upper bound the node
        v.bound = bound(v, n, W, items)

        #Visualise
        parent_node = (u.level, u.weight, u.profit)
        current_node = (v.level, v.weight, v.profit)
        G.add_edge(parent_node, current_node)  # Add edge between parent and current node
        node_labels[current_node] = f"P:{v.profit}, W:{v.weight}"  # Label nodes with profit and weight


        #if the bound is greater than the max profit, enqueue this node
        if v.bound > max_profit:
            Q.append(v)

        #case where the item is not taken
        v = Node(u.level + 1, u.profit, u.weight)
        v.bound = bound(v, n, W, items)

        #Visualise
        not_taken_node = (v.level, v.weight, v.profit)
        G.add_edge(parent_node, not_taken_node)
        node_labels[not_taken_node] = f"P:{v.profit}, W:{v.weight}"

        if v.bound > max_profit:
            Q.append(v)

    #Visualise
    solution_path = []
    while best_node:
        solution_path.append((best_node.level, best_node.weight, best_node.profit))
        best_node = best_node.parent
    solution_path = set(solution_path)

    #Visualise
    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(G, seed=42)
    node_colors = ["lightgreen" if node in solution_path else "lightblue" for node in G.nodes()]
    nx.draw(G, pos, with_labels=False, node_size=700, node_color=node_colors, edge_color='gray')
    nx.draw_networkx_labels(G, pos, labels=node_labels, font_size=8)
    plt.title("Branch and Bound Decision Tree with Optimal Solution Path Highlighted")
    plt.show()

    return max_profit, solution_path

# # ex
# W = 10  # max capacity
# items = [(10, 2), (5, 3), (15, 5), (7, 7), (6, 1), (18, 4), (3, 1)]  # (value, weight)
# max_profit, solution_path = knapsack_branch_and_bound(W, items)
# print("Maximum profit achievable:", max_profit)
