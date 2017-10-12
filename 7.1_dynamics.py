"""
Script to reproduce figure 7.1 of Anderson and May.  

W. Probert, 2016
"""

from os.path import join
import numpy as np
from scipy.integrate import odeint
from matplotlib import pyplot as plt

def infection(y, t, R0, v, mu, p):
     x, lamb = y
     
     dxdt = mu*(1-p) - (mu + lamb)*x
     dlambdt = v*lamb*(R0*x - 1)
     
     dydt = [dxdt, dlambdt]
     return dydt

if __name__ == "__main__":
    R0 = 15.0
    v = 25.0 #yr^-1
    mu = 1/70.
    p = 0.4

    # Choose values from the re-immunization equilibrium (eqn 6.5, 6.6)
    lamb0 = mu*(R0 - 1) # = 0.2
    x0 = 1/R0

    # Define the initial conditions and the time period over which to solve
    y0 = [x0, lamb0]
    t = np.linspace(0, 20, 1000)

    # Solve the system of differential equations
    sol = odeint(infection, y0, t, args = (R0, v, mu, p))

    fig, ax = plt.subplots()
    # Plot the force of infection
    ax.plot(t, sol[:, 1], 'black', lw = 2)
    ax.hlines(lamb0, xmin = -2, xmax = 0, color = 'black', lw = 2)
    
    ax.set_xticks(np.arange(0, 25, 5))
    ax.set_yticks([0, 0.1, 0.2])
    ax.spines['top'].set_visible(False)
    ax.xaxis.set_ticks_position('bottom')
    ax.set_xlabel("Time, t")
    ax.set_ylabel("Force of infection, $\lambda(t)$")
    
    # Second plot of fraction susceptible
    ax1 = ax.twinx()
    ax1.plot(t, sol[:, 0], 'black', lw = 1)
    ax1.hlines(x0, xmin = -2, xmax = 0, color = 'black', lw = 1)
    
    ax1.set_yticks([0, 0.04, 0.08])
    ax1.spines['top'].set_visible(False)
    ax1.xaxis.set_ticks_position('bottom')
    ax1.set_ylabel("Fraction susceptible, x(t)", rotation = -90, labelpad = 20)
    
    ax.set_xlim([-2, 20])
    ax.set_ylim([0, 0.2])
    
    ax1.set_xlim([-2, 20])
    ax1.set_ylim([0, 0.08])
    
    fig.set_size_inches(12, 8)
    plt.savefig(join('.', 'graphics', 'fig_7.1__test.pdf'))
    plt.close()

