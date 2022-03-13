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


class StackItem:

    def __init__(self, max_cost, id):
        self.max_cost = max_cost
        self.id = id
        self.results_of_subsearch = []


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


    def optimized_solution_recursive(self, max_cost:int):

        id_begin_with = len(self.items)

        max_value, last_item = self.__search_recursive(max_cost, id_begin_with)

        selected_items = dict()

        prev_item = last_item
        while prev_item is not None:
            prev_item, current_item = prev_item
            selected_items[current_item.id] = current_item

        return max_value, selected_items


    def __stack_search(self, stack:list):

        max_cost = stack[-1].max_cost
        id = stack[-1].id

        item = self.items[id]

        if (max_cost, id) in self.search_table:
            stack.pop()
            return self.search_table[(max_cost, id)]

        if max_cost < item.cost:
            self.search_table[(max_cost, id)] = (0, None)
            stack.pop()
            return self.search_table[(max_cost, id)]
        elif id == 1:
            self.search_table[(max_cost, id)] = (item.value, (None, item))
            stack.pop()
            return self.search_table[(max_cost, id)]
        
        elif len(stack[-1].results_of_subsearch) == 0:

            stack.append(StackItem(max_cost - item.cost, id - 1))
            
            return None

        elif len(stack[-1].results_of_subsearch) == 1:

            stack.append(StackItem(max_cost, id - 1))

            return None

        elif len(stack[-1].results_of_subsearch) == 2:

            value_1, last_item_1 = stack[-1].results_of_subsearch[0]
            value_2, last_item_2 = stack[-1].results_of_subsearch[1]

            if value_1 + item.value > value_2:
                self.search_table[(max_cost, id)] = (value_1 + item.value, (last_item_1, item))
            else:
                self.search_table[(max_cost, id)] = (value_2, last_item_2)

            stack.pop()
            
            return self.search_table[(max_cost, id)]


    def optimized_solution_of_stack_mode(self, max_cost:int):

        id_begin_with = len(self.items)

        the_stack = [StackItem(max_cost, id_begin_with)]
        result = None

        while len(the_stack) > 0:
            result = self.__stack_search(the_stack)
            if not (result is None) and len(the_stack) > 0:
                the_stack[-1].results_of_subsearch.append(result)
            else:
                pass

        max_value, last_item = result
        selected_items = dict()

        prev_item = last_item
        while prev_item is not None:
            prev_item, current_item = prev_item
            selected_items[current_item.id] = current_item

        return max_value, selected_items



def test_case(n_items, value_range, cost_range, max_cost):

    items = dict()

    for i in range(n_items):
        item = KnapsackItem(
            value = random.randint(value_range[0], value_range[1]),
            cost = random.randint(cost_range[0], cost_range[1]))
        items[item.id] = item

    model = Knapsack(items)
    
    total_value_1, selected_items_1 = model.optimized_solution_of_stack_mode(max_cost=max_cost)

    total_value_to_verify = 0

    for id in sorted(selected_items_1.keys()):
        item = items[id]
        total_value_to_verify += item.value
        print('({}, {}, {})'.format(id, item.value, item.cost), end=' ')

    print()
    print('total value:          ', total_value_1)
    print('total value to verify:', total_value_to_verify)

    binary_answer = []
    
    for i in range(1, n_items + 1):
        if i in selected_items_1:
            binary_answer.append(1)
        else:
            binary_answer.append(0)

    print(binary_answer)



def cross_test_case(n_items, value_range, cost_range, max_cost):

    items = dict()

    for i in range(n_items):
        item = KnapsackItem(
            value = random.randint(value_range[0], value_range[1]),
            cost = random.randint(cost_range[0], cost_range[1]))
        items[item.id] = item

    model = Knapsack(items)
    
    total_value_1, selected_items_1 = model.optimized_solution_of_stack_mode(max_cost=max_cost)
    total_value_2, selected_items_2 = model.optimized_solution_recursive(max_cost=max_cost)

    assert(total_value_1 == total_value_2)
    assert(len(selected_items_1) == len(selected_items_2))

    for id in selected_items_1.keys():
        assert(id in selected_items_2)

    total_value_to_verify = 0

    for id in sorted(selected_items_1.keys()):
        item = items[id]
        total_value_to_verify += item.value
        print('({}, {}, {})'.format(id, item.value, item.cost), end=' ')

    print()
    print('total value:          ', total_value_1)
    print('total value to verify:', total_value_to_verify)

    binary_answer = []
    
    for i in range(1, n_items + 1):
        if i in selected_items_1:
            binary_answer.append(1)
        else:
            binary_answer.append(0)

    print(binary_answer)



if __name__ == "__main__":

    random.seed(10)

    for i in range(100):
        cross_test_case(200, (1, 20), (1, 20), 100)
        KnapsackItem.STATIC_ID = 0

    for i in range(10):
        test_case(2000, (1, 50), (1, 50), 500)
        KnapsackItem.STATIC_ID = 0

    
    
