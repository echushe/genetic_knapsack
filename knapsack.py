import sys
import os
import collections
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


class Knapsack:

    def __init__(self, items:dict):

        self.items = items
        self.search_table = dict()

    # f (max_cost, id) = max( f (max_cost - cost(id), id - 1) + value(id), f (max_cost, id - 1) )

    def __search_recursive(self, max_cost, id):

        item = self.items[id]

        if (max_cost, id) in self.search_table:
            return self.search_table[(max_cost, id)]

        if max_cost < item.cost:
            self.search_table[(max_cost, id)] = (0, None)
            return self.search_table[(max_cost, id)]
        elif id == 1:
            self.search_table[(max_cost, id)] = (item.value, (None, item))
            return self.search_table[(max_cost, id)]

        value_1, last_item_1 = self.__search_recursive(max_cost - item.cost, id - 1)
        value_2, last_item_2 = self.__search_recursive(max_cost, id - 1)

        if value_1 + item.value > value_2:
            self.search_table[(max_cost, id)] = (value_1 + item.value, (last_item_1, item))
        else:
            self.search_table[(max_cost, id)] = (value_2, last_item_2)

        return self.search_table[(max_cost, id)]



    def optimized_solution(self, max_cost:int):

        id_begin_with = len(self.items)

        max_value, last_item = self.__search_recursive(max_cost, id_begin_with)

        selected_items = dict()

        prev_item = last_item
        while prev_item is not None:
            prev_item, current_item = prev_item
            selected_items[current_item.id] = current_item

        return max_value, selected_items





if __name__ == "__main__":

    items = dict()

    for i in range(1000):
        item = KnapsackItem(random.randint(1, 10), random.randint(1, 10))
        items[item.id] = item

    model = Knapsack(items)
    total_value, selected_items = model.optimized_solution(max_cost=15)

    total_value_to_verify = 0

    for id in sorted(selected_items.keys()):
        item = items[id]
        total_value_to_verify += item.value
        print('({}, {}, {})'.format(id, item.value, item.cost), end=' ')

    print()
    print('total value:          ', total_value)
    print('total value to verify:', total_value_to_verify)

    binary_answer = []

    
    for i in range(1, 11):
        if i in selected_items:
            binary_answer.append(1)
        else:
            binary_answer.append(0)

    print(binary_answer)

    
