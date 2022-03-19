import random
from knapsack_item import *
from knapsack_classic import KnapsackItem, StackItem, Knapsack

n_items = 16
value_range = (1, 100)
cost_range = (1, 100)
max_cost = 256

# Generate knapsack items using a seed
random.seed(10)
items = generate_knapsack_items(
    n_items=n_items,
    value_range=value_range,
    cost_range=cost_range)

model = Knapsack(items)
    
total_value, cost, selected_items = model.optimized_solution_of_stack_mode(max_cost=max_cost)

print_selected_items_in_binary_mode(items, selected_items)

