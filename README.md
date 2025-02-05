# Markov Chain Transition Diagrams in Python

Simple Markov Chain visualization module in Python. Only requires **matplotlib** and **numpy** to work.

## Description

The current version works with 2 to 9 states - it is possible to plot more, but graph becomes cluttery. (2 to 4 states in the original version 2021-12-14.)
 
## Getting Started

### Dependencies

* matplotlib
* numpy

### Installation

Copy the files src/node.py and src/markovchain.py in your script directory. Then

```
from markovchain import MarkovChain
```

#### 2-state Markov chain demo

```
P = np.array([[0.8, 0.2], [0.1, 0.9]]) # Transition matrix
mc = MarkovChain(P, ['1', '2'])
mc.draw("../img/markov-chain-two-states.png")
```

![two state markov chain transition diagram python](https://github.com/NaysanSaran/markov-chain/blob/master/img/markov-chain-two-states.png)

## Contribution by [joel-n](https://github.com/joel-n)

#### 4-state Markov chain demo

```
P = np.array([
    [0.65, 0.2, 0.15, 0.0], 
    [0.3, 0.3, 0.3, 0.15],
    [0.1, 0.0, 0.7, 0.15],
    [0.4, 0.2, 0.3, 0.1]
])
mc = MarkovChain(P, [r'$Z^1$', r'$Z^2$', r'$Z^3$', r'$Z^4$'])
mc.draw("../img/markov-chain-four-states.png")
```

![four state markov chain transition diagram python](https://github.com/joel-n/markov-chain/blob/master/img/markov-chain-four-states.png)

#### Plotting more than 4 states with automatic coordinate generation

```
N = 7
P = np.random.random((N, N))
for n in range(N):
	P[n,:] = P[n,:]/np.sum(P[n,:])
P = np.around(P, 3)

mc = MarkovChain(P, [f'{i+1}' for i in range(N)])
mc.draw("../img/markov-chain-N-states.png")
```

![seven state markov chain transition diagram python](https://github.com/joel-n/markov-chain/blob/master/img/markov-chain-N-states.png)


#### Plotting HMM Markov chains with initial probabilities and emission means

```
N = 5
P = np.random.random((N, N))
for n in range(N):
	P[n,:] = P[n,:]/np.sum(P[n,:])
P = np.around(P, 3)

init_probs = np.random.random(N)
init_probs = np.around(init_probs / np.sum(init_probs), 3)
        
mean = np.random.random((N, 3))
        
mc = MarkovChain(P, [f'{i+1}' for i in range(N)], init_probs, mean)
mc.draw("../img/markov-chain-N-states-hmm.png")

```

![five state markov chain transition diagram hmm python](https://github.com/joel-n/markov-chain/blob/master/img/markov-chain-N-states-hmm.png)


## Original author

[Naysan Saran](naysan.ca)

Link to my [blog](https://naysan.ca/2020/07/08/drawing-state-transition-diagrams-in-python/).

## License

This project is licensed under the GPL V3 licence.

