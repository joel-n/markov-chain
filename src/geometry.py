import numpy as np

class Geometry:

    def get_coordinates(self, n_nodes):

        coords = []
        base_x = 6
        base_y = 0
        ang = 2*np.pi/n_nodes
        
        for i in range(n_nodes):
            coords.append([base_x, base_y])
            x = base_x*np.cos(ang) - base_y*np.sin(ang)
            y = base_x*np.sin(ang) + base_y*np.cos(ang)
            base_x = x
            base_y = y
        
        return coords


    def get_anchor_points(self, coords, radius):
        n_nodes = len(coords)
        # 2 anchor points per node pair, one for incoming
        # and one for outgoing
        anchor_x = np.zeros((n_nodes, 2*n_nodes))
        anchor_y = np.zeros((n_nodes, 2*n_nodes))

        
        polygon_ang = (n_nodes - 2)*np.pi           # Total angle sum of polygon
        corner_ang = polygon_ang / n_nodes          # Angle at nodes in polygon
        if n_nodes == 2:
            anchor_ang = np.pi/8
            start_ang = -anchor_ang*n_nodes
        else:
            anchor_ang = 0.5*corner_ang / (n_nodes - 2) # Angle increment
            start_ang = np.pi - anchor_ang*n_nodes

        for i in range(n_nodes):
            cx = coords[i][0]
            cy = coords[i][1]
            for j in range(2*n_nodes):
                anchor_x[i,j] = cx + radius*np.cos(start_ang + j*anchor_ang)
                anchor_y[i,j] = cy + radius*np.sin(start_ang + j*anchor_ang)
            
            start_ang += 4*anchor_ang
            if n_nodes == 2:
                start_ang = np.pi - anchor_ang*n_nodes

        return anchor_x, anchor_y