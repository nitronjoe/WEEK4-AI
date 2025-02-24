# config.py
#
# Configuration information for the Genetic Algorithm for solving the Queens puzzle.
# Adjust the parameters below to experiment with different GA behaviours.
#
# Modes:
#   MODE.SELECTION_TEST  - Tests tournament selection (prints the best individual).
#   MODE.CROSSOVER_TEST  - Tests single point crossover (displays parents and offspring).
#   MODE.MUTATION_TEST   - Tests mutation (displays original and mutated solution).
#   MODE.RUN_GA          - Runs the full GA to solve the puzzle.
#
# Written by: Simon Parsons
# Modified by: [Your Name]
# Last Modified: [Date]

import random
from enum import Enum

class MODE(Enum):
    SELECTION_TEST = 0
    CROSSOVER_TEST = 1  # Test with a crossoverRate of 1 to ensure crossover occurs.
    MUTATION_TEST = 2   # Test with a mutationRate of 1 to force mutation on all genes.
    RUN_GA = 3

# Board dimensions (number of rows and columns).
worldLength = 8
worldBreadth = 8

numberOfQueens = worldLength           # One queen per column.
numberOfLocations = worldBreadth         # Possible rows for each queen.

# GA parameters:
populationSize = 50
numberOfGenerations = 10
crossoverRate = 1.0  # Probability of performing crossover.
mutationRate = 0.1   # Probability of mutating a gene.

displayBestAfterEachGeneration = True

# Set mode for testing.
# To test individual components (selection, crossover, mutation) change this value accordingly.
# For the final GA run, set mode to MODE.RUN_GA.

# mode = MODE.SELECTION_TEST # Tests tournament selection.
# mode = MODE.CROSSOVER_TEST # Tests single point crossover.
mode = MODE.MUTATION_TEST # Tests mutation.
# mode = MODE.RUN_GA # Runs the full Genetic Algorithm.