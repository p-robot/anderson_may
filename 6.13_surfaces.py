"""
Figure 6.13 in Anderson and May

TODO
----
Add second subplot of pertussis

W. Probert, 2016
"""

from mpl_toolkits.mplot3d import Axes3D
from matplotlib.collections import PolyCollection
import matplotlib.pyplot as plt
import numpy as np, pandas as pd

from os.path import join

if __name__=="__main__":

    measles = pd.read_csv(join('.', 'data', 'ch6_measles_uk_48_66.csv'))
    measles['year'] = np.floor(measles.date)
    measles['fraction'] = measles.date % 1

    years = measles.year.unique()[::-1]

    verts = []
    for yr in years:
        sub = measles.loc[measles.year == yr]
    
        xs = sub.fraction.values
        xs = np.insert(xs, 0, xs[0])
        xs = np.append(xs, xs[-1])
    
        ys = sub.cases.values
        ys = np.insert(ys, 0, 0)
        ys = np.append(ys, 0)
    
        verts.append(zip(xs, ys))


    fig = plt.figure()
    ax = fig.gca(projection='3d')

    poly = PolyCollection(verts, facecolors = '#d3d3d3')
    poly.set_alpha(0.6)
    ax.add_collection3d(poly, zs = years, zdir = 'z')

    ax.set_xlabel('X')
    ax.set_xlim3d(0, 1)
    ax.set_ylabel('Y')
    ax.set_ylim3d(0, 45000)
    ax.set_zlabel('Z')
    ax.set_zlim3d(1948, 1966)

    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('bottom')
    ax.zaxis.set_ticks_position('bottom')

    ax.view_init(120, -90)
    ax.set_axis_off()

    fig.set_size_inches(12, 8)
    plt.savefig(join('.', 'graphics', 'fig_6.13.pdf'))
    plt.close()
