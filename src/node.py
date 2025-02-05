import numpy as np
import matplotlib.patches as mpatches 
from matplotlib.collections import PatchCollection
import matplotlib.pyplot as plt

class Node():
    
    def __init__(
        self, center, radius, label, ix,
        facecolor='#6aa84f', edgecolor='#e6e6e6', # Original facecolor '#2693de'
        ring_facecolor='#a3a3a3', ring_edgecolor='#a3a3a3',
        init_prob = None, mean = None, mean_anchor=None
        ):
        """
        Initializes a Markov Chain Node(for drawing purposes)
        Inputs:
            - center : Node (x,y) center
            - radius : Node radius
            - label  : Node label

            - initial probabilities and state means (see MarkovChain)
        """
        self.ix = ix
        self.center = center
        self.radius = radius
        self.label  = label

        self.init_prob = init_prob
        self.mean = mean
        if mean is not None:
            self.meanpos_x = mean_anchor[0]
            self.meanpos_y = mean_anchor[1]

        # For convinience: x, y coordinates of the center
        self.x = center[0]
        self.y = center[1]
        
        # Drawing config
        self.node_facecolor = facecolor
        self.node_edgecolor = edgecolor
        
        self.ring_facecolor = ring_facecolor
        self.ring_edgecolor = ring_edgecolor
        self.ring_width = 0.03  
        
        self.text_args = {
            'ha': 'center', 
            'va': 'center', 
            'fontsize': 16
        }
    
        self.text_args_init = {
            'ha': 'center', 
            'va': 'center', 
            'fontsize': 10
        }

        self.text_args_mean = {
            'horizontalalignment': 'center', 
            'verticalalignment': 'center', 
            'fontsize': 8
        }
    
    
    def add_circle(self, ax, direction='left'):
        """
        Add the annotated circle for the node
        """
        circle = mpatches.Circle(self.center, self.radius)
        p = PatchCollection(
            [circle], 
            edgecolor = self.node_edgecolor, 
            facecolor = self.node_facecolor
        )
        ax.add_collection(p)
        ax.annotate(
            self.label, 
            xy = self.center, 
            color = '#ffffff', 
            **self.text_args
        )

        if direction == 'left':
            x_offset = self.x - 4.5*self.radius
        else:
            x_offset = self.x + 2*self.radius

        if self.init_prob is not None:
            ax.annotate(str(self.init_prob), xy=(self.x, self.y - 0.5*self.radius), color='#ffc34c', **self.text_args_init)

        if self.mean is not None:
            y_offset = self.y + 0.5*self.radius*len(self.mean)/2
            ax.annotate(np.array2string(self.mean, precision=3, separator='\n'), xy=(self.meanpos_x, self.meanpos_y), color='#000000', **self.text_args_mean)
            #ax.annotate(np.array2string(self.mean, precision=3, separator='\n'), xy=(x_offset, y_offset), color='#000000', **self.text_args_mean)
        
        
    def add_self_loop(self, ax, prob=None, direction='up', proportional_width=True):
        """
        Draws a self loop
        """
        if direction == 'up':
            start = -30
            angle = 180
            ring_x = self.x
            ring_y = self.y + self.radius
            prob_y = self.y + 1.3*self.radius
            x_cent = ring_x - self.radius + (self.ring_width/2)
            y_cent = ring_y - 0.15
        else:
            start = -210
            angle = 0
            ring_x = self.x
            ring_y = self.y - self.radius
            prob_y = self.y - 1.4*self.radius
            x_cent = ring_x + self.radius - (self.ring_width/2)
            y_cent = ring_y + 0.15
           
        if proportional_width:
            W = self.ring_width*(0.3+2.5*prob)
        else:
            W = self.ring_width
        
        # Add the ring
        ring = mpatches.Wedge(
            (ring_x, ring_y), 
            self.radius, 
            start, 
            angle, 
            width = W
        )
        # Add the triangle (arrow)
        offset = 0.2
        left   = [x_cent - offset, ring_y]
        right  = [x_cent + offset, ring_y]
        bottom = [(left[0]+right[0])/2., y_cent]
        arrow  = plt.Polygon([left, right, bottom, left])

        p = PatchCollection(
            [ring, arrow], 
            edgecolor = self.ring_edgecolor, 
            facecolor = self.ring_facecolor
        )
        ax.add_collection(p)
        
        # Probability to add?
        if prob:
            ax.annotate(str(prob), xy=(self.x, prob_y), color='#000000', **self.text_args)