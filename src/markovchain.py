import numpy as np
import matplotlib.patches as mpatches 
from matplotlib.collections import PatchCollection
import matplotlib.pyplot as plt
from numpy.lib.shape_base import tile

# module from this repository
from node import Node

class MarkovChain:

    def __init__(self, M, labels, init_probs_=None, means_=None):
        """
        Initializes a Markov Chain (for drawing purposes)
        Inputs:
            - M             Transition Matrix
            - labels        State Labels
            - init_probs_   List of initial probabilities for the states
            - means_        List of means for the (HMM) emissions of each state
        """

        if M.shape[0] < 2:
            raise Exception("There should be at least 2 states")
        if M.shape[0] > 4:
            raise Exception("Only works with 4 states max for now")
        if M.shape[0] != M.shape[1]:
            raise Exception("Transition matrix should be square")
        if M.shape[0] != len(labels):
            raise Exception("There should be as many labels as states")

        self.M = M
        self.n_states = M.shape[0]
        self.labels = labels

        self.init_probs = init_probs_
        self.means = means_

        # Colors
        self.arrow_facecolor = '#a3a3a3'
        self.arrow_edgecolor = '#a3a3a3'

        self.node_facecolor = '#233dff'
        self.node_edgecolor = '#565251'

        # Drawing config
        if M.shape[0] == 4:
            self.node_radius = 0.65
        else:
            self.node_radius = 0.5
            
        self.arrow_width = 0.03
        self.arrow_head_width = 0.20
        self.text_args = {
            'ha': 'center',
            'va': 'center',
            'fontsize': 16
        }

        # Build the network
        self.build_network()


    def set_node_centers(self):
        """
        Positions the node centers given the number of states
        """
        # Node positions
        self.node_centers = []

        if self.n_states == 2:
            self.figsize = (10, 4)
            self.xlim = (-7, 7)
            self.ylim = (-2, 2)
            self.node_centers = [[-4,0], [4,0]]
            self.init_prob_direction = ['left', 'right']
        elif self.n_states == 3:
            self.figsize = (10, 6)
            self.xlim = (-5.5, 5.5)
            self.ylim = (-3, 3)
            self.node_centers = [[-3,-2], [3,-2], [-3,2]]
            self.init_prob_direction = ['left', 'right', 'left']
        elif self.n_states == 4:
            self.figsize = (8, 8)
            self.xlim = (-7, 7)
            self.ylim = (-6.5, 6.5)
            self.node_centers = [[-4,4], [4,4], [4,-4], [-4,-4]]
            self.init_prob_direction = ['left', 'right', 'right', 'left']


    def build_network(self):
        """
        Loops through the matrix, add the nodes
        """
        # Position the node centers
        self.set_node_centers()

        # Set the nodes
        self.nodes = []
        if self.means is not None and self.init_probs is not None:
            for i in range(self.n_states):
                node = Node(
                    self.node_centers[i],
                    self.node_radius,
                    self.labels[i],
                    init_prob=self.init_probs[i],
                    mean=self.means[i] 
                )
                self.nodes.append(node)
        else:
            for i in range(self.n_states):
                node = Node(
                    self.node_centers[i],
                    self.node_radius,
                    self.labels[i] 
                )
                self.nodes.append(node)


    def add_arrow(self, ax, node1, node2, prob=None):
        """
        Add a directed arrow between two nodes
        """
        # x,y start of the arrow
        x_start = node1.x + np.sign(node2.x-node1.x) * node1.radius
        y_start = node1.y + np.sign(node2.y-node1.y) * node1.radius

        # arrow length
        dx = abs(node1.x - node2.x) - 2.5* node1.radius
        dy = abs(node1.y - node2.y) - 2.5* node1.radius

        # we don't want xoffset and yoffset to both be non-nul
        yoffset = 0.4 * self.node_radius * np.sign(node2.x-node1.x)
        if yoffset == 0:
            xoffset = 0.4 * self.node_radius * np.sign(node2.y-node1.y)
        else:
            xoffset = 0

        arrow = mpatches.FancyArrow(
            x_start + xoffset,
            y_start + yoffset,
            dx * np.sign(node2.x-node1.x),
            dy * np.sign(node2.y-node1.y),
            width = self.arrow_width*(0.3+2.5*prob),
            head_width = self.arrow_head_width
        )
        p = PatchCollection(
            [arrow],
            edgecolor = self.arrow_edgecolor,
            facecolor = self.arrow_facecolor
        )
        ax.add_collection(p)

        # Probability to add?
        x_prob = x_start + xoffset + 0.2*dx*np.sign(node2.x-node1.x)
        y_prob = y_start + yoffset + 0.2*dy*np.sign(node2.y-node1.y)
        if prob:
            ax.annotate(str(prob), xy=(x_prob, y_prob), color='#000000', **self.text_args)


    def draw(self, img_path=None, title_=None):
        """
        Draw the Markov Chain
        """
        fig, ax = plt.subplots(figsize=self.figsize)

        # Set the axis limits
        plt.xlim(self.xlim)
        plt.ylim(self.ylim)

        # Draw the nodes
        if self.init_probs is not None:
            for i, node in enumerate(self.nodes):
                node.add_circle(ax, direction=self.init_prob_direction[i])
        else:
            for node in self.nodes:
                node.add_circle(ax)

        # Add the transitions
        for i in range(self.M.shape[0]):
            for j in range(self.M.shape[1]):
                # self loops
                if i == j:
                    # Loop direction
                    if self.nodes[i].y >= 0:
                        self.nodes[i].add_self_loop(ax, prob = self.M[i,j], direction='up')
                    else:
                        self.nodes[i].add_self_loop(ax, prob = self.M[i,j], direction='down')
                # directed arrows
                elif self.M[i,j] > 0:
                    self.add_arrow(ax, self.nodes[i], self.nodes[j], prob = self.M[i,j])

        plt.axis('off')
        
        if title_:
            plt.title(title_)

        if img_path:
            plt.savefig(img_path)
            
        plt.show()
