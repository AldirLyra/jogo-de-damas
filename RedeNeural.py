from jogo2 import Player
import pygad
import pygad.nn
import pygad.gann
import numpy as np
def fitness_func(solution, solution_idx):
    
    return fitness

class RedeNeural(Player):
    def jogar(self,TABOLEIRO):
        GANN_instance = pygad.gann.GANN(num_solutions=num_solutions,
                                num_neurons_input= 8*8,
                                num_neurons_hidden_layers=[2],
                                num_neurons_output=1,
                                hidden_activations=["relu"],
                                output_activation="softmax")
        GANN_instance.create_population()
        pass