import random
from knapsack_item import *


class Individual:

    STATIC_ID = 0

    def increase_id(cls):
        cls.STATIC_ID += 1

    def __init__(self, all_items:dict(), genetic_code:list, max_cost):

        Individual.increase_id(Individual)
        self.id = self.STATIC_ID

        if len(genetic_code) < len(all_items):
            red = len(all_items) - len(genetic_code)
            for _ in range(red):
                genetic_code.append(0)

        elif len(genetic_code) > len(all_items):
            genetic_code = genetic_code[0 : len(all_items)]

        self.all_items = all_items
        self.genetic_code = genetic_code
        self.max_cost = max_cost

    def get_value(self):

        value = 0
        for i in range(len(self.genetic_code)):
            id = i + 1
            if self.genetic_code[i] > 0:
                value += self.all_items[id].value

        return value

    def get_cost(self):

        cost = 0
        for i in range(len(self.genetic_code)):
            id = i + 1
            if self.genetic_code[i] > 0:
                cost += self.all_items[id].cost

        return cost


    def get_fitness(self):

        cost = self.get_cost()
        value = self.get_value()

        if cost > self.max_cost:
            return 0
        else:
            return value

        


class KnapsackGenetic:

    def __init__(self, items:dict, max_cost, init_population=10):

        self.all_items = items
        self.max_cost = max_cost

        self.__initialize_population(init_population)


    def __initialize_population(self, init_population):
        self.population = dict()
        digits = len(self.all_items)
        max_code = 2 << digits

        format_str = ':0{}b'.format(digits)
        format_str = '{' + format_str + '}'

        for _ in range(init_population):
            code = random.randrange(max_code)
            str_digits = format_str.format(code)
            list_of_int = list(map(int, str_digits))

            new_individual = Individual(self.all_items, list_of_int, self.max_cost)
            self.population[new_individual.id] = new_individual


    def survive(self):

        total_fitness = 0
        for id, individual in self.population.items():
            total_fitness += individual.get_fitness()

        if total_fitness == 0:
            print('Entire population died out!')
            self.population.clear()
            return

        big_number = len(self.population) * (2 << 10)

        survival_roulette = []
        for id, individual in self.population.items():
            survival_count = individual.get_fitness() * big_number // total_fitness
            for _ in range(survival_count):
                survival_roulette.append(id)

        new_population = dict()
        for i in range(len(self.population)):
            id = survival_roulette[random.randrange(len(survival_roulette))]
            survived_individual = self.population[id]
            new_population[id] = survived_individual

        self.population = new_population


    def proliferate_and_survive(self):

        total_fitness = 0
        for id, individual in self.population.items():
            total_fitness += individual.get_fitness()

        if total_fitness == 0:
            print('Entire population died out!')
            self.population.clear()
            return

        big_number = len(self.population) * (2 << 10)

        survival_roulette = []
        for id, individual in self.population.items():
            survival_count = individual.get_fitness() * big_number // total_fitness
            for _ in range(survival_count):
                survival_roulette.append(id)

        new_population = dict()
        while len(new_population) < len(self.population):
            id = survival_roulette[random.randrange(len(survival_roulette))]
            survived_individual = self.population[id]

            survived_individual_cpy = Individual(self.all_items, survived_individual.genetic_code, self.max_cost)
            new_population[survived_individual_cpy.id] = survived_individual_cpy

        self.population = new_population


    def crossover(self):
        
        id_list = []
        for id in self.population.keys():
            id_list.append(id)

        random.shuffle(id_list)

        mid = len(id_list) // 2

        mate_group_a = id_list[: mid]
        mate_group_b = id_list[mid :]

        new_population = dict()

        for i in range(min(len(mate_group_a), len(mate_group_b))):
            mate_a : Individual = self.population[mate_group_a[i]]
            mate_b : Individual = self.population[mate_group_b[i]]

            gen_code_len = len(self.all_items)
            cross_point = random.randrange(1, gen_code_len)

            new_ge_code_a = mate_a.genetic_code[:cross_point] + mate_b.genetic_code[cross_point:]
            new_ge_code_b = mate_b.genetic_code[:cross_point] + mate_a.genetic_code[cross_point:]

            new_mate_a = Individual(self.all_items, new_ge_code_a, self.max_cost)
            new_mate_b = Individual(self.all_items, new_ge_code_b, self.max_cost)

            new_population[new_mate_a.id] = new_mate_a
            new_population[new_mate_b.id] = new_mate_b

        if len(mate_group_a) > len(mate_group_b):
            single_id = mate_group_a[mid]
            new_population[single_id] = self.population[single_id]
        elif len(mate_group_a) < len(mate_group_b):
            single_id = mate_group_b[-1]
            new_population[single_id] = self.population[single_id]

        self.population = new_population


    def proliferate(self, rate):

        big_number = 2 << 32
        produce_part = int(rate * big_number)

        new_individuals = []
        for id, individual in self.population.items():

            if random.randrange(big_number) < produce_part:
                new_individual = Individual(self.all_items, individual.genetic_code, self.max_cost)
                new_individuals.append(new_individual)

        for new_individual in new_individuals:
            self.population[new_individual.id] = new_individual

    
    def mutate(self):

        mutate_roulette = [0] * 1000
        mutate_roulette[0] = 1
        
        for individual in self.population.values():
            for i in range(len(self.all_items)):
                mutation = mutate_roulette[random.randrange(len(mutate_roulette))]
                if mutation > 0:
                    if individual.genetic_code[i] > 0:
                        individual.genetic_code[i] = 0
                    else:
                        individual.genetic_code[i] = 1
        
    
    
    def optimized_solution(self, max_cost:int):

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


    def print_population(self):

        for id, individual in self.population.items():
            print('value: {},\tcost: {},\tgene: {}'.format(
                individual.get_value(),
                individual.get_cost(),
                individual.genetic_code))


    def print_population_properties(self):

        max_value = -1
        total_value = 0
        total_cost = 0
        best_individual = None
        for id, individual in self.population.items():
            value = individual.get_value()
            cost = individual.get_cost()

            total_value += value
            total_cost += cost
            if value > max_value:
                max_value = value
                best_individual = individual

        print('population:      {}'.format(len(self.population)))

        if len(self.population) > 0:
            print('best individual: {}'.format(best_individual.genetic_code))
            print('its value:       {}'.format(best_individual.get_value()))
            print('its cost:        {}'.format(best_individual.get_cost()))
            print('\nmax value:       {}'.format(max_value))
            print('avg value: {:.4f}'.format(total_value / len(self.population)))
            print('avg cost:  {:.4f}'.format(total_cost / len(self.population)))


if __name__ == "__main__":

    n_items = 32
    value_range = (1, 100)
    cost_range = (1, 100)
    max_cost = 800

    # Generate knapsack items using a seed
    random.seed(10)
    items = generate_knapsack_items(
        n_items=n_items,
        value_range=value_range,
        cost_range=cost_range)

    print_items(items)

    model = KnapsackGenetic(items, max_cost, init_population=200)
    model.print_population_properties()
    model.print_population()
    
    for i in range(500):

        print('======================== {} ==========================='.format(i))

        #model.proliferate(0.5)
        #model.survive()
        model.proliferate_and_survive()

        print_items(items)
        model.print_population()
        model.print_population_properties()

        model.crossover()
        model.mutate()


