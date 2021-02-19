import numpy as np
import math

class OrbitalElements(object):
    def __init__(self, r, v):
        self.r = r
        self.v = v
        self.mu = 1
        self.a = 0
        self.e = 0
        self.i = 0
        self.Omega = 0
        self.argp = 0
        self.nu = 0
    
    
    def get_orbital_elements(self):
        h = np.cross(self.r,self.v)
        nhat = np.cross([0,0,1], h)
        evec = np.multiply(( np.linalg.norm(self.v) ** 2 ) - (1 / np.linalg.norm(self.r)), self.r)
        evec -= np.multiply(np.dot(self.r,self.v), self.v)
        self.e = np.linalg.norm(evec)

        energy = np.linalg.norm(self.v) **2 / 2 - self.mu / np.linalg.norm(self.r)

        if self.e != 1:
            self.a = -1 * self.mu / (2 * energy)
            p = self.a * (1 - self.e ** 2)
        else:
            p = np.linalg.norm(h) ** 2 / self.mu
            self.a = "Infinity"

        self.i = math.acos(h[2] / np.linalg.norm(h))

        self.Omega = math.acos( nhat[0] / np.linalg.norm(nhat) )

        if nhat[1] < 0:
            self.Omega = 360 - self.Omega

        self.argp = math.acos( np.dot(nhat,evec) / (np.linalg.norm(nhat) * self.e) )
        
        if self.e < 0:
            self.argp = 360 - self.argp

        self.nu = math.acos( np.dot(evec,self.r) / ( self.e * np.linalg.norm(self.r)) )

        if np.dot(self.r,self.v) < 0:
            self.nu = 360 - self.nu

        print("Orbital Elements\na: " + str(self.a) + "\ne: " + str(self.e) + "\ni: " + str(self.i) + "\nOmega: " + str(self.Omega) + "\nargp: " + str(self.argp) + "\nnu: " + str(self.nu))

# if __name__ == '__main__':
#     v = [0,1,0]
#     r = [2, 0,  0]
#     Element = OrbitalElements(r, v)
#     Element.get_orbital_elements()