import numpy as np
import matplotlib.patches as mpatches 
from matplotlib.collections import PatchCollection
import matplotlib.pyplot as plt
from numpy.lib.shape_base import tile

# module from this repository
from node import Node
from geometry import Geometry

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
        self.geo = Geometry()

        if M.shape[0] < 2:
            raise Exception("There should be at least 2 states")
        if M.shape[0] > 9:
            raise Exception("Graph get cluttery above 9 states")
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
        if M.shape[0] >= 4:
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
        if self.n_states == 2:
            self.figsize = (10, 4)
            self.xlim = (-7, 7)
            self.ylim = (-2, 2)
            self.node_centers = [[-4,0], [4,0]]
            self.init_prob_direction = ['left', 'right']
        else:
            self.figsize = (10, 10)
            self.xlim = (-9.5, 8.5)
            self.ylim = (-7, 9)
            self.node_centers = self.geo.get_coordinates(self.n_states)
            self.init_prob_direction = ['left' for i in range(self.n_states)]

        self.anchor_x, self.anchor_y = self.geo.get_anchor_points(coords=self.node_centers, radius=self.node_radius)

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
                    ix = i,
                    init_prob=self.init_probs[i],
                    mean=self.means[i] 
                )
                self.nodes.append(node)
        else:
            for i in range(self.n_states):
                node = Node(
                    self.node_centers[i],
                    self.node_radius,
                    self.labels[i],
                    ix = i
                )
                self.nodes.append(node)


    def start_point(self, node1, node2):
        dx = (node2.x - node1.x)
        dy = (node2.y - node1.y)
        length = np.sqrt(dx*dx + dy*dy)
        x = dx / length
        y = dy / length

        x_start = node1.x + x*np.cos(np.pi/12) * node1.radius
        y_start = node1.y + y*np.sin(np.pi/12) * node1.radius

        return x_start, y_start

    def add_arrows(self, ax, node1_ix, node2_ix):
        p12 = self.M[node1_ix, node2_ix]
        p21 = self.M[node2_ix, node1_ix]

        # Node 2 comes after node 1 in the order
        if node1_ix > node2_ix:
            tmp = node1_ix
            node1_ix = node2_ix
            node2_ix = tmp

        rel_offset = node2_ix - node1_ix

        # Arrow from node 1 to node 2
        n1_beg = [self.anchor_x[node1_ix, 2*rel_offset], self.anchor_y[node1_ix,2*rel_offset]]
        n2_end = [self.anchor_x[node2_ix, -2*rel_offset], self.anchor_y[node2_ix, -2*rel_offset]]
        
        # Arrow from node 2 to node 1
        n2_beg = [self.anchor_x[node2_ix,  -(2*rel_offset+1)],  self.anchor_y[node2_ix,  -(2*rel_offset+1)]]
        n1_end = [self.anchor_x[node1_ix,(2*rel_offset+1)], self.anchor_y[node1_ix,(2*rel_offset+1)]]

        arrow = mpatches.FancyArrow(
            n1_beg[0],
            n1_beg[1],
            n2_end[0] - n1_beg[0],
            n2_end[1] - n1_beg[1],
            width = self.arrow_width*(0.3+2.5*p12),
            head_width = self.arrow_head_width,
            length_includes_head=True
        )
        p = PatchCollection(
            [arrow],
            edgecolor = self.arrow_edgecolor,
            facecolor = self.arrow_facecolor
        )
        ax.add_collection(p)

        # Probability to add?
        x_prob = n1_beg[0] + 0.2*(n2_end[0] - n1_beg[0])
        y_prob = n1_beg[1] + 0.2*(n2_end[1] - n1_beg[1])
        if p12:
            ax.annotate(str(p12), xy=(x_prob, y_prob), color='#000000', **self.text_args)

        arrow21 = mpatches.FancyArrow(
            n2_beg[0],
            n2_beg[1],
            n1_end[0] - n2_beg[0],
            n1_end[1] - n2_beg[1],
            width = self.arrow_width*(0.3+2.5*p21),
            head_width = self.arrow_head_width,
            length_includes_head=True
        )
        p = PatchCollection(
            [arrow21],
            edgecolor = self.arrow_edgecolor,
            facecolor = self.arrow_facecolor
        )
        ax.add_collection(p)

        # Probability to add?
        x_prob = n2_beg[0] + 0.2*(n1_end[0] - n2_beg[0])
        y_prob = n2_beg[1] + 0.2*(n1_end[1] - n2_beg[1])
        if p21:
            ax.annotate(str(p21), xy=(x_prob, y_prob), color='#000000', **self.text_args)


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
                elif i > j:
                    continue
                elif self.M[i,j] > 0:
                    self.add_arrows(ax, i, j)

        plt.axis('off')
        
        if title_:
            plt.title(title_)

        if img_path:
            plt.savefig(img_path)
            plt.savefig(f'{img_path[:-3]}svg')
            
        plt.show()
