import numpy as np 
import pandas as pd 
from collections import namedtuple
from time import time 

Solution = namedtuple('Solution', ['x', 'f', 'nIter', 'cpu'])

def generate_a_single_monomial(nx, deg):
    '''
    Generate a random monomial  
    nx variables and degree deg.

    INPUT
    -----
    nx: number of variables 
    deg: degreee of the randomly created monomial

    OUTPUT
    ------
    power: the matrix of powers of each component.
    '''
    I = np.random.permutation(np.arange(0,nx))
    power = np.array([0 for _ in range(nx)])
    d = power.sum()
    for i in range(nx):
        power[I[i]] = np.random.randint(0, deg-d+1)
        d = power.sum()
    return power

def generate_X(xmin, xmax, n):
    '''
    generate a matrix of values of dimenion 
    (n x nx) in the hypercube defined by 
    xmin and xmax.

    INPUT
    -----
    xmin: lower bound 
    xmax: upper bound 
    n: numer of vectors to generate 

    OUTPUT
    ------
    The matrix of values 
    '''

    dx = np.array(xmax)-np.array(xmin)
    nx = len(xmin)
    X = [xmin[i] + np.random.rand(n) * dx[i] for i in range(nx)]

    return np.array(X).T

class Pol:
    '''
    An instance of this class is defined by the matrix of powers 
    (each line defines a monomial without coefficients) and the 
    vector of coefficients associated to the monomials.

    ATTRIBUTES
    ----------
    ncoefs: the number of coefficients 
    nx: the number of variables
    powers: the matrix of powers 
    coefs: the coefficients of the monomials 
    deg: the degree of the polynomial in a conventional sense.
    (the max of sums of powers over monomials)
    '''

    def generate_random_pol(nx, deg_max, card):
        '''
        This is a class method (not an instance one)
        Generates a random polynomial of nx variables where each 
        term is powered to less than deg_max-th power. The number 
        of non zero monomial is equal to card.

        INPUT
        ------
        nx: the number of variables 
        deg_max: the maximum power of individual terms
        card: the number of monomial in the polynomial 

        OUTPUT
        ------
        An instance of the class polynomial that contains 
        the randomly generated monomial. 
        '''
        powers = [generate_a_single_monomial(nx, deg_max) 
            for _ in range(card)]
        
        coefs = np.random.randn(card)
        pol = Pol(powers, coefs)
        return pol 

    def __init__(self, powers, coefs):
        '''
        Defines an instance of the class Pol. 

        INPUT:
        ------
        powers: the matrix of powers (each line --> a monomial without coef.)
        voefs: the coefficients of the monomials 
        '''
        self.ncoefs = len(coefs)
        self.nx = np.array(powers).reshape(self.ncoefs,-1).shape[1]
        self.powers = powers
        self.coefs = coefs 
        self.deg = int(np.array(powers).sum(axis=1).max())

    def to_df(self):
        '''
        create a pandas dataframe to display the power matrix 
        and the coefficients vector. 
        '''

        col_powers = [f'x{i+1}' for i in range(self.nx)]
        df = pd.DataFrame(self.powers, columns=col_powers)
        df['coeff'] = self.coefs
        return df

    def to_dict(self):
        '''
        returns a dictionary version of the instance of Pol
        that might be helpful for representations such as 
        pandas or streamlit.
        '''
        dic = {
            'nx': self.nx,
            'ncoefs': self.ncoefs,
            'powers': self.powers,
            'coefs' : self.coefs,
            'deg': self.deg
        }

        return dic
    
    def eval(self, X):
        '''
        Evaluates the values of the instance at a given 
        matrix of values of x.

        INPUT
        -----
        X: the matrix of values (each line is an instance of x)

        OUTPUT
        -----
        The value of the polynomial at the lines of the matrix X
        '''
        X = np.array(X).reshape(-1,self.nx)
        v = np.zeros(len(X))
        for i in range(self.ncoefs):
           v +=  np.power(X, self.powers[i]).prod(axis=1) * self.coefs[i]
        if len(v) == 1:
            v = v[0]
        return v
    
    def extract_sc_pol(self, x, ix):
        '''
        Extract a scalar polynomial for the coordinate number ix 
        at a given value x of the variable. 

        INPUT
        -----
        x: the current value of x 
        ix: the index of the component w.r.t which the scalar polynomial 
        is to be defined 

        OUTPUT
        ------
        The scalar polynomial in numpy.poly1d form.
        '''
        df = pd.DataFrame(self.powers)
        dg = df.groupby(by=ix)
        deg_r = df[ix].max()
        pol_r = [0 for _ in range(deg_r+1)]

        for k in dg.groups.keys():

            dh = dg.get_group(k)
            powers = dh.values 
            coefs = np.array([self.coefs[i] for i in list(dh.index)])
            pol_ix = Pol(powers, coefs)
            xw = 1.0 * x
            xw[ix] = 1.0
            pol_r[deg_r-k] = float(pol_ix.eval(xw))

        pol_r = np.poly1d(pol_r)
        return pol_r

    def solve(self, x0, xmin, xmax, Ntrials=1, ngrid=1000, 
                    iter_max=100,eps=0.001, psi=lambda v: v):

        def single_trial(x0):
            t0 = time()
            xI = [
                np.linspace(xmin[i], xmax[i], ngrid) 
                for i in range(self.nx)
            ]
            xc = 1.0*np.array(x0)
            again = False
            n = 0
            for it in range(iter_max):
                if it == 0 or again:
                    n += 1
                    again = False
                    for ix in range(self.nx):
                        Jopt = self.eval(xc)
                        p = self.extract_sc_pol(xc, ix)
                        v = p(xI[ix])
                        iopt = np.argsort(psi(v))[0]
                        xc[ix] = xI[ix][iopt]
                        if v[iopt] <  Jopt - eps * abs(Jopt):
                            again = True
            
            cpu = time()-t0
            solution = Solution(xc, Jopt, n, cpu)
                
            return solution

        Jbest = np.inf
        lesJbest = []
        t0 = time()
        for i in range(Ntrials):
            if i == 0:
                x0_w = 1.0 * np.array(x0)
            else:
                x0_w = np.random.randn(self.nx)
            sol = single_trial(x0_w)
            if sol.f < Jbest:
                Jbest = sol.f
                solution = sol
            lesJbest.append(Jbest)
            t = time()-t0

        cpu = time()-t0
        return solution, cpu

