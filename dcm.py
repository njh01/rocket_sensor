import math
import numpy as np
import pdb

# TODO figure out correct signs for sines

class direction_cosine_matrix:
    def __init__(self):
        self.dcm = np.ones((3,3))
    # takes in a eueler angle, returns a D3 (typically about z, depending on axes names) matrix
    def d3(self, angle):
        return np.asarray([[math.cos(angle),-math.sin(angle),0], [math.sin(angle), math.cos(angle),0], [0,0,1]])


    # takes in a eueler angle, returns a D2 (typically about y) matrix
    def d2(self, angle):
        return np.asarray([[math.cos(angle),0,math.sin(angle)],[0,1,0],[-math.sin(angle),0,math.cos(angle)]])


    # takes in a eueler angle, returns a D1 (typically about x) matrix
    def d1(self, angle):
        return np.asarray([[1,0,0], [0,math.cos(angle),-math.sin(angle)], [0,math.sin(angle),math.cos(angle)]])


    def DCM(self, angles, sequence):
        if sequence[0] == 1:
            self.dcm *= self.d1(angles[0])
        elif sequence[0] == 2:
            self.dcm *= self.d2(angles[1])
        else:
            self.dcm *= self.d3(angles[2])

        for i in range(len(sequence)-1):
            if sequence[i+1] == 1:
                self.dcm *= self.d1(angles[i+1])
            elif sequence[i+1] == 2:
                self.dcm *= self.d2(angles[i+1])
            else:
                self.dcm *= self.d3(angles[i+1])
        return self.dcm
