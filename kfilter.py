import numpy as np
import pdb

class Filter:

    def __init__(self,debug=False):
        '''
        Standard Extended Kalman Filter
        '''
        self.debug = debug
        self.step = 0
        self.X = np.zeros((12,1))
        self.u = np.zeros((6,1))
        self.Pk = np.identity(12)
        self.A = np.identity(12)
        self.B = np.zeros((12,6))
        self.H = np.zeros((6,12))
        self.K = np.ones((12,6))
        self.Rk = np.identity(6)
        self.Q = np.zeros((12,12))

        self.Xsave = []
        self.measurement_save = []
    
    def amat(self,dt):
        self.A[0][3] = dt
        self.A[1][4] = dt
        self.A[2][5] = dt
        self.A[6][9] = dt
        self.A[7][10] = dt
        self.A[8][11] = dt
        if self.debug:
            print("A: ",self.A)

    def bmat(self,dt):
        self.B[0][0] = dt**2/2
        self.B[1][1] = dt**2/2
        self.B[2][2] = dt**2/2
        self.B[6][3] = dt**2/2
        self.B[7][4] = dt**2/2
        self.B[8][5] = dt**2/2
        if self.debug:
            print("B: ",self.B)

    def pmat(self,dt):
        noise = 0.5*dt**2
        n2 = dt
        self.Pk[0][3] = noise
        self.Pk[1][4] = noise
        self.Pk[2][5] = noise
        self.Pk[6][9] = n2
        self.Pk[7][10] = n2
        self.Pk[8][11] = n2
        if self.debug:
            print("Pk: ",self.Pk)

    def qmat(self,dt):
        q = 0.5
        t1 = dt**3/3*q
        t2 = dt**2/2*q
        t3 = dt*q
        self.Q[0][0] = t1
        self.Q[1][1] = t1
        self.Q[2][2] = t1
        self.Q[6][6] = t1
        self.Q[7][7] = t1
        self.Q[8][8] = t1
        
        self.Q[3][3] = t3
        self.Q[4][4] = t3
        self.Q[5][5] = t3
        self.Q[9][9] = t3
        self.Q[10][10] = t3
        self.Q[11][11] = t3
        
        self.Q[0][3] = t2
        self.Q[1][4] = t2
        self.Q[2][5] = t2
        self.Q[3][0] = t2
        self.Q[4][1] = t2
        self.Q[5][2] = t2
        
        self.Q[6][9] = t2
        self.Q[7][10] = t2
        self.Q[8][11] = t2
        self.Q[9][6] = t2
        self.Q[10][7] = t2
        self.Q[11][8] = t2
        if self.debug:
            print("Q: ",self.Q)

    def rmat(self):
        # self.Rk[2][2] = 0.2
        self.Rk[3][3] = 15.0
        self.Rk[4][4] = 15.0
        self.Rk[5][5] = -15.0
        if self.debug:
            print("Rk: ",self.Rk)
    
    def hmat(self,dt):
        self.H[0][3] = dt
        self.H[1][4] = dt
        self.H[2][5] = dt
        self.H[3][9] = 1
        self.H[4][10] = 1
        self.H[5][11] = 1
        if self.debug:
            print("H: ",self.H)
    
    def filter(self,measurement,dt):
        if self.step < 1:
            self.pmat(dt)
            self.rmat()
        
        self.step += 1
        time = self.step*dt
        self.amat(dt)
        self.bmat(dt)
        self.qmat(dt)
        self.hmat(dt)

        model_update = np.dot(self.A,self.X)+np.dot(self.B,self.u)
        noise_update = np.dot(self.A,np.dot(self.Pk,self.A.T))+self.Q

        num = np.dot(self.Pk,self.H.T)
        den = np.linalg.inv(np.dot(self.H,np.dot(self.Pk,self.H.T))+self.Rk)

        self.K = np.dot(num,den)

        measurement_model = np.dot(self.H,self.X)
        measurement_residual = measurement_model-measurement
        self.X = self.X + np.dot(self.K,measurement_residual)

        temp = np.identity(12) - np.dot(self.K,self.H)
        self.Pk = np.dot(temp,self.Pk)
        self.store_data(measurement,time)

        if self.debug:
            print("Model update: ", model_update)
            print("Noise update: ", noise_update)
            print("Gain: ", self.K)
            print("Observation update: ", self.X)
            print("Noise Observation update: ",self.Pk)
            pdb.set_trace()

    def store_data(self,measurement,t):
        self.Xsave.append([self.X,t])
        self.measurement_save.append([measurement,t])