import sys, os
import datetime

default='data/worldometer/us-cases'

if len(sys.argv) > 1:
    fpath = sys.argv[1]
else:
    fpath = default

if os.path.isfile(fpath):
    datafile = open(fpath, 'r')
else:
    datafile = sys.stdin

_data=[x.strip() for x in datafile.readlines()
       if x.strip() != '' and not x.strip().startswith('#')]

data=list(map(int, _data[1:]))

start_date = datetime.datetime.strptime(_data[0], '%m/%d/%Y')

def d2s(dt):
    return dt.strftime('%Y-%m-%d')

def calc(data):
    for i, x in enumerate(data):
        date=start_date + datetime.timedelta(i)
        if i==0:
            yield (i, d2s(date), x, None, None)
        else:
            change = round((x*1.0)/data[i-1], 2)
            yield (i, d2s(date), x, change, round((change-1)*100))

def totext(data):
    for item in calc(data):
        sys.stdout.write("%s (%s) %s = %s (%s%%)\n" % item)

if __name__ == '__main__':
    totext(data)
