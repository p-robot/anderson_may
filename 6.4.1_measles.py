"""
Script to perform the analyses listed in chapter 6 of 
Anderson and May.  

W. Probert, 2016.
"""

import numpy as np, pandas as pd
from matplotlib import pyplot as plt
from os.path import join

main_dir = join('/', 'Users', 'wjmprobert', 'Projects', \
    'companion anderson and may')

measles = pd.read_csv(join(main_dir, 'data', 'ch6_measles_uk_48_66.csv'))

# Plot the data in figure 6.3
fig, ax = plt.subplots()
ax.plot(measles.date, measles.cases, c = [0, 0, 0, 1])
ax.set_xlim([measles.date.min(), measles.date.max()])

yticks = np.arange(0, 50, 5)
ax.set_yticks(yticks*1000)
ax.set_yticklabels(yticks)

xticks = np.arange(1948, 1967, 2)
ax.set_xticks(xticks)
ax.set_xticklabels(xticks)

ax.set_xlabel("Year")
ax.set_ylabel("Weekly cases of measles (thousands)")

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')
plt.savefig(join(main_dir, 'graphics', 'fig_6.3.pdf'))
plt.close()

# Autocorrelation function in Numpy
#out = np.correlate(measles.cases, measles.cases, mode='full')

# From Anderson et al., (1984)
# also p31 Box and Jenkins (1968, eqn 2.1.11 and 2.1.12)

# Sample autocovariate coefficient (across all lags)
xbar = np.log(measles.cases).mean()

N = len(measles)
K = np.floor(len(measles)/2).astype(int)

C = np.array([])
for k in range(K):
    lims = np.arange(N-k)
    a = np.log(measles.cases.values[lims]) - xbar
    b = np.log(measles.cases.values[lims+k]) - xbar
    
    c = 1./N * np.dot(a, b)
    C = np.append(C, c)

# Sample autocorrelation coefficient (for all lags)
r = C/C[0]

from scipy.stats import t
t_alpha = t.cdf(0.95, N-1)
x = np.sqrt(1./N*t_alpha)


fig, ax = plt.subplots(frameon = 0)
ax.plot(range(K), r, c = 'black', lw = 1.5)

# Plot the confidence intervals
ax.axhline(x, c = "#666666", ls = "--")
ax.axhline(-x, c = "#666666", ls = "--")

ax.set_ylim([-1, 1])
ax.set_xlim([0, 500])

xticks = np.linspace(0, 500, 11).astype(int)
ax.set_xticks(xticks)
ax.set_xticklabels(xticks)

yticks = np.linspace(-1, 1, 5)
ax.set_yticks(yticks)
ax.set_yticklabels(yticks)

ax.spines['bottom'].set_position('zero')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')

ax.set_xlabel("Time lag (weeks)")
ax.set_ylabel("Autocorrelation")

# Re-position the xlabel wrt the data coordinates
ax.xaxis.set_label_coords(240, -0.8, transform = ax.transData)

fig.set_size_inches(12, 3)
plt.savefig(join(main_dir, "fig_6.4.pdf"))
plt.close()

# Can do this straight away in R using 
# >>> df <- read.table("ch6_measles_uk_48_66.csv", sep = ",", header = TRUE)
# >>> acf(log(df$cases), lag.max = 500, type = "covariance")

# Signficance test for overall departure from randomness
# Box and Jenkins (1968) Time Series Analysis: Forecasting and Control.  

x = measles.cases.values - measles.cases.mean()

C = np.array([])
for k in range(K):
    lims = np.arange(N-k)
    a = x[lims]
    b = x[lims+k]
    
    c = 1./N * np.dot(a, b)
    C = np.append(C, c)


freqs = np.linspace(0, np.pi, 51)

# Range of window cut-off poitns
Ms = [107, 232, 357]

M = 107

full = []
for omega in freqs:
    res = 0
    for i in (np.arange(M-1)+1):
        # What's lambda?  
        lamb = (1 + np.cos(np.pi*i/M))/2. # eqn A8, Anderson et al. (1984)
        res += lamb * C[i] * np.cos(omega*i)
    
    full.append((C[0] + 2*res)/np.pi)


