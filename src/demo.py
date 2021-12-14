import numpy as np
import matplotlib.pyplot as plt

# modules from this repository
from markovchain import MarkovChain

def main():
    
    #--------------------------------------------------------------------------
    # N-state Markov chain
    #--------------------------------------------------------------------------
    states = [i for i in range(2, 10)]
    for N in states:
        
        P = np.random.random((N, N))
        for n in range(N):
            P[n,:] = P[n,:]/np.sum(P[n,:])
        P = np.around(P, 3)

        init_probs = np.random.random(N)
        init_probs = np.around(init_probs / np.sum(init_probs), 3)
        
        mean = np.random.random((N, 3))
        
        mc = MarkovChain(P, [f'{i+1}' for i in range(N)])
        # mc = MarkovChain(P, [f'{i+1}' for i in range(N)], init_probs, mean)
        mc.draw("../img/markov-chain-N-states.png")

 

if __name__ == "__main__":
    main()

