"""
Demo for displaying the Markov chain of and HMM
model with (e.g. Gaussian) emission means and 
initial probabilities
"""

import numpy as np
import matplotlib.pyplot as plt

# modules from this repository
from markovchain import MarkovChain

def main():
    
    #--------------------------------------------------------------------------
    # 2-state Markov chain
    #--------------------------------------------------------------------------
    P = np.array([[0.8, 0.2], [0.1, 0.9]]) # Transition matrix
    init_probs = np.array([0.4, 0.6])
    mean = np.array([
        [0.1, 0.4, 0.1, 0.4, 0.1, 0.4],
        [0.22, 0.33, 0.22, 0.33, 0.22, 0.33]
    ])
    mc = MarkovChain(P, [r'$Z^1$', r'$Z^2$'], init_probs, mean)
    mc.draw("../img/markov-chain-two-states-hmm.png")
    
    #--------------------------------------------------------------------------
    # 3-state Markov chain
    #--------------------------------------------------------------------------
    P = np.array([
        [0.8, 0.1, 0.1],
        [0.1, 0.7, 0.2],
        [0.1, 0.7, 0.2],
    ])
    init_probs = np.array([0.3, 0.1, 0.6])
    mean = np.array([
            [12, 2, 4, 9],
            [51, 3, 4, 5],
            [13, 7, 2, 90]
    ])
    mc = MarkovChain(P, [r'$Z^1$', r'$Z^2$', r'$Z^3$'], init_probs, mean)
    mc.draw("../img/markov-chain-three-states-hmm.png")
    
    #--------------------------------------------------------------------------
    # 4-state Markov chain
    #--------------------------------------------------------------------------
    P = np.array([
        [0.65, 0.2, 0.15, 0.0], 
        [0.3, 0.3, 0.3, 0.15],
        [0.1, 0.0, 0.7, 0.15],
        [0.4, 0.2, 0.3, 0.1]
    ])
    init_probs = np.array([0.1, 0.2, 0.6, 0.1])
    mean = np.array([
	    [0.66, 0.3, 0.66, 0.3],
	    [2.2, 9.3, 0.66, 0.3],
        [1.2, 8.9, 0.66, 0.3],
	    [9.1, 0.3, 0.66, 0.3]
	])
    mc = MarkovChain(P, [r'$Z^1$', r'$Z^2$', r'$Z^3$', r'$Z^4$'], init_probs, mean)
    mc.draw("../img/markov-chain-four-states-hmm.png")
 

if __name__ == "__main__":
    main()

