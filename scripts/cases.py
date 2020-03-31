import sys, os
import datetime
from pprint import pprint as pp
import math

def d2s(dt):
    return dt.strftime('%m-%d')

def splitdata(rawdata):
    return (datetime.datetime.strptime(rawdata[0], '%m/%d/%Y'),
            list(map(int, rawdata[1:])))

def mean(lst):
    ll=len(lst)
    return sum(lst)/ll

def calc(rawdata):
    start_date, data = splitdata(rawdata)
    for i, x in enumerate(data):
        date=start_date + datetime.timedelta(i)
        if i==0:
            yield (i, d2s(date), x, 0, 0)
        else:
            newcases = x - data[i-1]
            change = round((x*1.0)/data[i-1], 2)
            yield (i, d2s(date), x, change, round((change-1)*100))

def totext(data):
    for item in calc(data):
        sys.stdout.write("%s (%s) %s = %s (%s%%)\n" % item)

def loaddata(fpath='data/worldometer/us-cases'):
    datafile = open(fpath, 'r')
    return [x.strip() for x in datafile.readlines()
            if x.strip() != '' and not x.strip().startswith('#')]

def main(args):
    default='data/worldometer/us-cases'
    if len(args) > 1:
        fpath = args[1]
    else:
        fpath = default
    if os.path.isfile(fpath):
        datafile = open(fpath, 'r')
    else:
        datafile = sys.stdin
    _data=[x.strip() for x in datafile.readlines()
           if x.strip() != '' and not x.strip().startswith('#')]
    calced=list(calc(_data))
    totext(_data)
    mean1=mean([x[3] for x in calced][1:26])

if __name__ == '__main__':
    main((sys.argv + [None]))
