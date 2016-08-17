"""
Script to process data from Ben Bolker's website and create a 
csv file for plotting an analysing to recreate the work in chapter
6 of Anderson and May.  

W. Probert, 2016
"""

import numpy as np, pandas as pd, urllib2
from os.path import join

main_dir = join('/', 'Users', 'wjmprobert', 'Projects', \
    'companion anderson and may')

# Pull the data from Ben Bolker's webpage
url = "https://ms.mcmaster.ca/~bolker/measdata/ewmeas.dat"

site = urllib2.urlopen(url)
result = site.read()

# Process the data (it's a long string)
rows = [x.split(' ') for x in result.split('\n')]
rows = rows[:-1]

rows = np.array(rows).astype(np.float64)

measles = pd.DataFrame(rows)
measles.columns = ['date', 'cases']

measles.to_csv(join(main_dir, 'data', 'ch6_measles_uk_48_66.csv'), \
    index = False)
