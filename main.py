import numpy as np
import random
from operator import itemgetter
import Image
from matplotlib import pyplot as plt
"""
The beginnings of this where based on https://jakevdp.github.io/blog/2013/08/07/conways-game-of-life/
"""


class Population:
    population = []

    def __init__(self, game_size, pop_size, percentage, iter_limit):
        self.game_size = game_size
        self.percentage = percentage
        self.pop_size = pop_size
        self.iter_limit = iter_limit
        self.iter_count = 0
        self.mutate_percent = 0.005
        self.mutate_ratio = {'l': 8, 's': 3, 't': 2}
        self.fitness_type = 1
        self.stats = []
        for iteration in xrange(self.pop_size):
            game = np.zeros(self.game_size, dtype=bool)
            game_random = np.random.random(self.game_size)
            game = game_random > self.percentage
            self.population.append({'start': game.copy(), 'iterations': 0, 'count': 0, 'fitness': 0.0})

    def life_step(self, X):
        """Game of life step using generator expressions"""
        nbrs_count = sum(np.roll(np.roll(X, i, 0), j, 1)
                         for i in (-1, 0, 1) for j in (-1, 0, 1)
                         if (i != 0 or j != 0))
        return (nbrs_count == 3) | (X & (nbrs_count == 2))

    def life(self, X):
        X = np.asarray(X)
        assert X.ndim == 2
        X = X.astype(bool)
        X = self.life_step(X)

        return X.astype(bool)

    def play(self):
        """
        Simulates all games in population
        """
        tmp_pop = []
        for being in self.population:
            tmp_game = being['start'].copy()
            iteration = 0
            begin_count = np.sum(tmp_game)
            while True in tmp_game and iteration < self.iter_limit:
                tmp_game = self.life(tmp_game)
                iteration += 1
            if self.fitness_type == 0:
                fitness = iteration * np.sum(tmp_game)
            elif self.fitness_type == 1:
                if np.sum(tmp_game) == 0:  # Stops 'divide by 0' errors
                    fitness = 0
                else:
                    fitness = iteration * (1.0 / (float(begin_count) / np.sum(tmp_game)))

            tmp_pop.append({'start': being['start'], 'iterations': iteration, 'count': np.sum(tmp_game), 'fitness': fitness})
        self.population = tmp_pop

    def mutate(self, game):
        tmp_game = game.copy()
        mutation_number = int(self.game_size[0] * self.game_size[1] * self.mutate_percent) + 1

        # Flips the selected coordinate.
        for mutation in xrange(mutation_number):
            random_x = random.randint(0, self.game_size[0]-1)
            random_y = random.randint(0, self.game_size[1]-1)
            if game[random_x][random_y] == True:
                tmp_game[random_x][random_y] = False
            elif game[random_x][random_y] == False:
                tmp_game[random_x][random_y] = True

        # Erases mmutation_number of cells
        decay_target = mutation_number  # / 2 + 1
        decay_count = 0
        life_locations = []
        for i in xrange(len(game)):
            for ii in xrange(len(game[i])):
                if game[i][ii] == True:
                    life_locations.append([i, ii])
        while decay_count < decay_target:
            decay_life_target = random.choice(life_locations)
            tmp_game[decay_life_target[0]][decay_life_target[1]] = False
            decay_count += 1

        return tmp_game

    def mutation_helper(self, game):
        tmp_game = self.mutate(game)
        if not np.array_equal(tmp_game, game):
            return tmp_game

        while np.array_equal(tmp_game, game):
            """
            This loop discards mutations that have had no effect
            """
            tmp_game = self.mutate(game)
        return tmp_game

    def merge(self):
        """
        This will merge two games.
        For use in 'mating'
        """

    def evolve(self):
        """
        This creates a new population based on the old one.
        """
        tmp_pop = []
        fittest = sorted(self.population, key=itemgetter('fitness'), reverse=True)
        if self.stats == []:
            for being in fittest:
                self.stats.append([being['fitness']])
        else:
            for being in xrange(len(fittest)):
                self.stats[being].append(fittest[being]['fitness'])

        tmp_r_num = self.pop_size / (self.mutate_ratio['l'] + self.mutate_ratio['s'] + self.mutate_ratio['t'])
        second_number = int(tmp_r_num * self.mutate_ratio['s']) - 1
        third_number = int(tmp_r_num * self.mutate_ratio['t']) - 1
        leader_number = self.pop_size - second_number - third_number - 3

        # Write leader image
        img = Image.new('RGB', (self.game_size[0], self.game_size[1]), "white")  # create a new black image
        pixels = img.load()
        for i in xrange(len(fittest[0]['start'])):
            for ii in xrange(len(fittest[0]['start'][i])):
                if fittest[0]['start'][i][ii] == True:
                    pixels[i, ii] = (0, 0, 0)

        img.save('images/leader_' + str(self.iter_count) + '.png')
        self.iter_count += 1

        tmp_pop.append(fittest[0])  # Always keep the leader
        tmp_pop.append(fittest[1])
        tmp_pop.append(fittest[2])

        for mutation in xrange(second_number):
            tmp_being = {'start': self.mutation_helper(fittest[1]['start'].copy()), 'iterations': 0, 'count': 0, 'fitness': 0}
            tmp_pop.append(tmp_being)

        for mutation in xrange(third_number):
            tmp_being = {'start': self.mutation_helper(fittest[2]['start'].copy()), 'iterations': 0, 'count': 0, 'fitness': 0}
            tmp_pop.append(tmp_being)

        for mutation in xrange(leader_number):
            tmp_being = {'start': self.mutation_helper(fittest[0]['start'].copy()), 'iterations': 0, 'count': 0, 'fitness': 0}
            tmp_pop.append(tmp_being)

        self.population = tmp_pop
        self.play()

        print 'Evolution Summary'
        print 'Count - Fitness - Iterations'
        for being in sorted(self.population, key=itemgetter('fitness'), reverse=True)[:3]:
            print being['count'], being['fitness'], being['iterations']


sim = Population(game_size=(100, 100), pop_size=50, percentage=0.99, iter_limit=200)

for i in xrange(200):
    print 'Run', i
    sim.evolve()

game_map = sim.population[0]['start']
for count in xrange(sim.iter_limit):
    img = Image.new('RGB', (sim.game_size[0], sim.game_size[1]), "white")  # create a new black image
    pixels = img.load()
    for i in xrange(len(game_map)):
        for ii in xrange(len(game_map[i])):
            if game_map[i][ii] == True:
                pixels[i, ii] = (0, 0, 0)

    img.save('images/' + str(count) + '.png')

    game_map = sim.life(game_map.copy())

# Graph fitness
for iteration in sim.stats:
    plt.plot([i for i in xrange(len(sim.stats[0]))], iteration)
plt.savefig('images/stats.jpg')