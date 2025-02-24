# GA.py
#
# This file implements a Genetic Algorithm (GA) for solving the N-Queens puzzle.
# It creates an initial random population of solutions (chromosomes), and then
# repeatedly creates new generations by selecting parents, performing crossover,
# and applying mutation. The fitness function counts the number of queen collisions.
#
# Written by: Simon Parsons
# Modified by: [Your Name]
# Last Modified: [Date]

import world
import random
import config
import utils

from numpy.random import randint  # for generating random integers using numpy
from numpy.random import rand     # for generating random floats using numpy

class GA():
    def __init__(self, world):
        # Store a reference to the world so the GA can query its state.
        self.world = world
        
        # Initialise the population with randomly generated individuals.
        # Each individual is a list of integers (queen positions) of length numberOfQueens.
        self.population = [randint(0, config.numberOfLocations, config.numberOfQueens).tolist() 
                           for _ in range(config.populationSize)]
        
        # Initialize fitness tracking variables.
        self.fitnesses = []
        self.best_fitness = -1
        self.best_individual = None
        
        # Calculate fitness for the initial population.
        self.calculateFitnessOfPopulation()
        
    # This method creates a new generation and returns the best individual found so far.
    def makeMove(self):
        children = []
        # Process population two at a time.
        for i in range(0, len(self.population), 2):
            # 1. Select parents using tournament selection.
            parent1 = self.performTournamentSelection() 
            parent2 = self.performTournamentSelection() 
            
            # 2. Create children by performing crossover.
            child1, child2 = self.performCrossover(parent1, parent2)
                
            # 3. Mutate the children.
            child1 = self.performMutation(child1)    
            child2 = self.performMutation(child2)       
            	
            children.append(child1)
            children.append(child2)
            
        # Replace the old population with the new generation.
        self.population = children
        self.calculateFitnessOfPopulation()
        return (self.best_individual, self.best_fitness)   
        
    #####################################  
    # GA methods to be implemented:
    
    def performTournamentSelection(self, k=3):
        """
        Tournament Selection:
        1. Randomly select 'k' individuals from the population.
        2. Compare their fitness values (lower is better) and return the best individual.
        """
        # Get k random indices from the population.
        candidate_indices = random.sample(range(len(self.population)), k)
        # Assume the first candidate is the best initially.
        best_index = candidate_indices[0]
        # Compare fitness values and update best_index accordingly.
        for idx in candidate_indices:
            if self.fitnesses[idx] < self.fitnesses[best_index]:
                best_index = idx
        return self.population[best_index]
    
    
    def performCrossover(self, parent1, parent2): 
        """
        Single Point Crossover:
        1. With probability defined by config.crossoverRate, choose a random crossover point.
        2. Swap the tail segments of the two parents at that point to create two children.
        3. If crossover is not performed, return copies of the parents.
        """
        if random.random() < config.crossoverRate:
            # Choose a crossover point that is not the first or last index.
            crossover_point = random.randint(1, len(parent1) - 2)
            # Create children by exchanging segments of the parents.
            child1 = parent1[:crossover_point] + parent2[crossover_point:]
            child2 = parent2[:crossover_point] + parent1[crossover_point:]
            return child1, child2
        else:
            # No crossover occurs; return direct copies of the parents.
            return parent1.copy(), parent2.copy()
       
    def performMutation(self, individual): 
        """
        Mutation:
        1. For each gene (queen position) in the chromosome, generate a random number.
        2. If the random number is below config.mutationRate, change that gene.
        3. The new gene is a random integer (row number) between 0 and numberOfLocations-1,
           ensuring it differs from the original value.
        """
        mutated = individual.copy()
        for i in range(len(mutated)):
            if random.random() < config.mutationRate:
                new_value = mutated[i]
                # Ensure the mutated value is different from the current gene.
                while new_value == mutated[i]:
                    new_value = random.randint(0, config.numberOfLocations - 1)
                mutated[i] = new_value
        return mutated
       
    #  End of GA modification methods
    #####################################   
    
    ##
    # Methods for fitness calculations    
        
    def calculateFitnessOfPopulation(self):
        # Calculate fitness for every individual in the population.
        self.fitnesses = [self.calculateFitness(i) for i in self.population]

        # Update the best solution found so far.
        for i in range(len(self.population)):
            if (self.best_individual is None) or (self.fitnesses[i] < self.best_fitness):
                self.best_fitness = self.fitnesses[i]
                self.best_individual = self.population[i]
        
    def calculateFitness(self, individual):
        """
        Fitness Function:
        Counts the number of collisions between queens.
        A lower fitness value indicates a better solution.
        """
        total = 0
        # Compare each queen with every other queen that comes later.
        for i in range(len(individual)):
            agent = utils.Pose(i, individual[i])
            for j in range(i+1, len(individual)):
                agent2 = utils.Pose(j, individual[j])
                if self.isColunmCollision(agent, agent2) or \
                   self.isRowCollision(agent, agent2) or \
                   self.isDiagonalCollision(agent, agent2):
                    total += 1
        return total           
    
    # Collision detection functions:
    def isColunmCollision(self, pose1, pose2):
        return (pose1.y == pose2.y)
    
    def isRowCollision(self, pose1, pose2):
        return (pose1.x == pose2.x)
    
    def isDiagonalCollision(self, pose1, pose2):         
        return (abs(pose1.x - pose2.x) == abs(pose1.y - pose2.y))
