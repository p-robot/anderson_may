"""
Script to reproduce figure 6.1 of Anderson and May.  

TO DO
-----
Write the solver/integrator by hand.  
Use the scipy.integrate.ode OOP interface to solve this.  

W. Probert, 2016
"""

from os.path import join
import numpy as np
from scipy.integrate import odeint

main_dir = join('/', 'Users', 'wjmprobert', 'Projects', \
    'companion anderson and may')

R0 = 5.0
v = 10 #yr^-1
mu = 0.014

lamb0 = 10E-4
x0 = 1- lamb0

# Define the initial conditions and the time period over which to solve
y0 = [x0, lamb0]
t = np.linspace(0, 90, 1000)


def infection(y, t, R0, v, mu):
     x, lamb = y
     
     dxdt = mu - (mu + lamb)*x
     dlambdt = (v + mu)*lamb*(R0*x - 1)
     
     dydt = [dxdt, dlambdt]
     return dydt

# Solve the system of differential equations
sol = odeint(infection, y0, t, args = (R0, v, mu))



from matplotlib import pyplot as plt
fig, ax = plt.subplots()
ax.plot(t, sol[:, 0], 'black')

ax.axhline(1/R0, ls = ":", c = "#777777")

ax.set_xticks(np.arange(0, 100, 20))
ax.set_yticks([0, 0.5, 1.0])

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')

ax.set_xlabel("Time, t (yr)")
ax.set_ylabel("Fraction susceptible, x")

fig.set_size_inches(12, 8)
plt.savefig(join(main_dir, 'graphics', 'fig_6.1.pdf'))
plt.close()
