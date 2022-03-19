import random
from knapsack_item import *


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

        if (max_cost, id) in self.search_table:
            return self.search_table[(max_cost, id)]

        if id == 0:
            self.search_table[(max_cost, id)] = (0, None)
            return self.search_table[(max_cost, id)]

        item = self.items[id]

        if max_cost < item.cost:
            self.search_table[(max_cost, id)] = self.__search_recursive(max_cost, id - 1)
            return self.search_table[(max_cost, id)]

        else:
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

        cost = 0
        prev_item = last_item
        while prev_item is not None:
            prev_item, current_item = prev_item
            selected_items[current_item.id] = current_item
            cost += current_item.cost


        return max_value, cost, selected_items


    def __search_stack(self, stack:list):

        max_cost = stack[-1].max_cost
        id = stack[-1].id

        if (max_cost, id) in self.search_table:
            stack.pop()
            return self.search_table[(max_cost, id)]

        if id == 0:
            self.search_table[(max_cost, id)] = (0, None)
            stack.pop()
            return self.search_table[(max_cost, id)]

        item = self.items[id]
        
        if max_cost < item.cost:
            if len(stack[-1].results_of_subsearch) == 0:
                stack.append(StackItem(max_cost, id - 1))
                return None
            else:
                self.search_table[(max_cost, id)] = stack[-1].results_of_subsearch[0]

                stack.pop()

                return self.search_table[(max_cost, id)]
        
        else:
            if len(stack[-1].results_of_subsearch) == 0:
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
            result = self.__search_stack(the_stack)
            if not (result is None) and len(the_stack) > 0:
                the_stack[-1].results_of_subsearch.append(result)
            else:
                pass

        max_value, last_item = result
        selected_items = dict()

        cost = 0
        prev_item = last_item
        while prev_item is not None:
            prev_item, current_item = prev_item
            selected_items[current_item.id] = current_item
            cost += current_item.cost

        return max_value, cost, selected_items



def test_case(n_items, value_range, cost_range, max_cost):

    print('------------------------------------------------------------')

    items = generate_knapsack_items(n_items, value_range, cost_range)

    '''
    for id in sorted(items.keys()):
        item = items[id]
        print('({}, {}, {})'.format(id, item.value, item.cost), end=' ')
    print()
    '''

    model = Knapsack(items)
    
    total_value_1, cost_1, selected_items_1 = model.optimized_solution_of_stack_mode(max_cost=max_cost)

    total_value_to_verify = 0

    for id in sorted(selected_items_1.keys()):
        item = items[id]
        total_value_to_verify += item.value
        print('({}, {}, {})'.format(id, item.value, item.cost), end=' ')

    print()
    print('total value:          ', total_value_1)
    print('total cost:           ', cost_1)
    
    print_items(selected_items_1)
    print_selected_items_in_binary_mode(items, selected_items_1)



def cross_test_case(n_items, value_range, cost_range, max_cost):

    print('------------------------------------------------------------')

    items = generate_knapsack_items(n_items, value_range, cost_range)

    model = Knapsack(items)
    
    total_value_1, total_cost_1, selected_items_1 = model.optimized_solution_of_stack_mode(max_cost=max_cost)
    total_value_2, total_cost_2, selected_items_2 = model.optimized_solution_recursive(max_cost=max_cost)

    assert(total_value_1 == total_value_2)
    assert(total_cost_1 == total_cost_2)
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
    print('total cost:           ', total_cost_1)

    total_value, total_cost = print_items(selected_items_1)
    print_selected_items_in_binary_mode(items, selected_items_1)

    assert(total_value == total_value_1)
    assert(total_cost == total_cost_1)



if __name__ == "__main__":

    random.seed(10)

    for i in range(10):
        test_case(8, (1, 32), (1, 32), 128)
        KnapsackItem.STATIC_ID = 0

    for i in range(100):
        cross_test_case(100, (1, 32), (1, 32), 512)
        KnapsackItem.STATIC_ID = 0

    for i in range(10):
        test_case(1200, (1, 50), (1, 50), 256)
        KnapsackItem.STATIC_ID = 0

    
    
