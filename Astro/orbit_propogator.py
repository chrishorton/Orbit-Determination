import numpy as np
import math

class OrbitalElements(object):
    def __init__(self, r, v):
        self.r = r
        self.v = v
        self.mu = 1
    
    
    def h_n_e(self):
        h = np.cross(r,v)
        nhat = np.cross([0,0,1], h)
        evec = np.multiply(( np.linalg.norm(v) ** 2 ) - (1 / np.linalg.norm(r)), r)
        evec -= np.multiply(np.dot(r,v), v)
        e = np.linalg.norm(evec)

        energy = np.linalg.norm(v) **2 / 2 - self.mu / np.linalg.norm(r)

        if e != 1:
            a = -1 * self.mu / (2 * energy)
            p = a * (1 - e ** 2)
        else:
            p = np.linalg.norm(h) ** 2 / self.mu
            a = "Infinity"

        i = math.acos(h[2] / np.linalg.norm(h))

        Omega = math.acos( nhat[0] / np.linalg.norm(nhat) )

        if nhat[1] < 0:
            Omega = 360 - Omega

        argp = math.acos( np.dot(nhat,evec) / (np.linalg.norm(nhat) * e) )
        
        if e < 0:
            argp = 360 - argp

        nu = math.acos( np.dot(evec,r) / ( e * np.linalg.norm(r)) )

        if np.dot(r,v) < 0:
            nu = 360 - nu

        print("a: " + str(a) + "\ne: " + str(e) + "\ni: " + str(i) + "\nOmega: " + str(Omega) + "\nargp: " + str(argp) + "\nnu: " + str(nu))
        return a, e, i, Omega, argp, nu

if __name__ == '__main__':
    r = [2, 0,  0]
    v = [0,1,0]
    Element = OrbitalElements(r, v)
    Element.h_n_e()