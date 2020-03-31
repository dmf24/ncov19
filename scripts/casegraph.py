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
datadir=pjoin(repo, 'data')

import cases

if __name__ == '__main__':
    _data = cases.loaddata(pjoin(datadir, 'worldometer', sys.argv[1]))
    data = list(cases.calc(_data))
    xaxis = [item[1] for item in data][1:]
    yaxis = [item[3] for item in data][1:]
    item = pyplot.plot(xaxis, yaxis, marker='o')
    pylab.show()
