import random

class KnapsackItem:
    
    STATIC_ID = 0

    def increase_id(cls):
        cls.STATIC_ID += 1

    def __init__(self, value:int, cost:int):

        KnapsackItem.increase_id(KnapsackItem)
        self.id = self.STATIC_ID

        self.value = value
        self.cost = cost


def generate_knapsack_items(n_items, value_range, cost_range):

    items = dict()

    for i in range(n_items):
        item = KnapsackItem(
            value = random.randrange(value_range[0], value_range[1]),
            cost = random.randrange(cost_range[0], cost_range[1]))
        items[item.id] = item

    KnapsackItem.STATIC_ID = 0

    return items


def print_items(items):
    
    total_value = 0
    total_cost = 0
    for id in sorted(items.keys()):
        item = items[id]
        total_value += item.value
        total_cost += item.cost
        print('({}, {}, {})'.format(id, item.value, item.cost), end=' ')

    print()
    print('total value:          ', total_value)
    print('total cost:           ', total_cost)
    print()

    return total_value, total_cost


def print_selected_items_in_binary_mode(all_items, selected_items):

    binary_answer = []
    n_items = len(all_items)
    
    for i in range(1, n_items + 1):
        if i in selected_items:
            binary_answer.append(1)
        else:
            binary_answer.append(0)

    print(binary_answer)
    return binary_answer



