from eckity.termination_checkers.termination_checker import TerminationChecker

class GenerationTerminationChecker(TerminationChecker):
    def __init__(self, generations_limit, fitness_threshold):
        super().__init__()
        self.generations_limit = generations_limit
        self.fitness_threshold = fitness_threshold

    def should_terminate(self, population, best_individual, gen_number):
        return (gen_number >= self.generations_limit or
                best_individual.get_pure_fitness() >= self.fitness_threshold)
