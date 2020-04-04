import sys
import os
from matplotlib import pyplot
import pylab
from pprint import pprint as pp
pjoin=os.path.join

home=os.getenv('HOME')
repo=pjoin(home, 'ncov19')
libpy=pjoin(repo, 'lib')
sys.path.append(libpy)

import timeseries as ts

if __name__ == '__main__':
    data = list(ts.docalcs(ts.data, country='California', edate='5/1/20'))
    xaxis = [item[1] for item in data[-50:]]
    yaxis = [item[4] for item in data[-50:]]
    pp(xaxis)
    item = pyplot.plot(xaxis, yaxis, marker='o')
    pylab.show()
