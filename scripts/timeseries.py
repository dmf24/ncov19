import sys, os
import datetime
from pprint import pprint as pp
import math
import csv
import numpy
import datetime
from collections import defaultdict

A=numpy.array

def loadcsv(fh):
    data = list(csv.reader(fh))
    return {'header': data[0],
            'rows': data[1:]}

def loadcsvf(fname):
    return loadcsv(open(fname))

def d2s(dt):
    return dt.strftime('%m-%d')

def s2d(dstring):
    return datetime.datetime.strptime(dstring, '%m/%d/%y')

def dump(fname):
    csvdict = loadcsv(open(sys.argv[1]))
    print(csvdict['header'])
    for row in csvdict['rows']: 
        print(row)

def getcountry(csvdict, country):
    index=csvdict['header'].index('Country/Region')
    for row in csvdict['rows']:
        if row[index] == country:
            yield row

def getall(csvdict):
    country_index = csvdict['header'].index('Country/Region')
    results = {}
    indices = defaultdict(list)
    datetimes = [datetime.datetime.strptime(item, '%m/%d/%y') for item in csvdict['header'][4:]]
    for index, row in enumerate(csvdict['rows']):
        country = row[country_index]
        indices[country].append(index)
    for country in indices:
        series = A(list(map(int, csvdict['rows'][indices[country][0]][4:])))
        for index in indices[country][1:]:
            series += A(list(map(int, csvdict['rows'][index][4:])))
        results[country] = list(zip(datetimes, series))
    return results

def getallUS(csvdict):
    'UID,iso2,iso3,code3,FIPS,Admin2,Province_State,Country_Region,Lat,Long_,Combined_Key,1/22/20'
    state_index=csvdict['header'].index('Province_State')
    results = {}
    indices = defaultdict(list)
    datetimes = [datetime.datetime.strptime(item, '%m/%d/%y') for item in csvdict['header'][11:]]
    for index, row in enumerate(csvdict['rows']):
        state = row[state_index]
        indices[state].append(index)
    for state in indices:
        series = A(list(map(int, csvdict['rows'][indices[state][0]][11:])))
        for index in indices[state][1:]:
            series += A(list(map(int, csvdict['rows'][index][11:])))
        results[state] = list(zip(datetimes, series))
    return results

INTERVAL=5
ONE_MILLION=1000000
def days2reach(start_cases, numcases, change, interval=1):
    for x in range(1, 3600, interval):
        if start_cases * change ** (x/interval) > numcases:
            return x
    return x

def doubling(start_cases, change, interval=1):
    return days2reach(start_cases, start_cases*2, change, interval=interval)

def caserates(timeseries):
    week=INTERVAL
    for index, item in enumerate(timeseries):
        date, numcases = item
        if index == 0:
            change = numcases
            lastweek_rates = [change] * week
        else:
            prevcases = timeseries[index-1][1]
            newcases = numcases - prevcases
            change = round(numcases/prevcases, 2)
            if index > week:
                prev_week_cases = timeseries[index-week][1]
                lastweek_rates = lastweek_rates[1:] + [change]
        yield (index, date, numcases, change, round(sum(lastweek_rates)/week, 2))

def estimate(data, edate):
    for index, date, numcases, change, avchange in data:
        days2edate = (s2d(edate) - date).days
        total_estimate = numcases * change ** days2edate
        est2 = numcases * avchange ** days2edate
        toamil = days2reach(numcases, ONE_MILLION, change)
        toamilX = days2reach(numcases, ONE_MILLION, avchange) #change7day, interval=INTERVAL)
        doubling_time = doubling(numcases, avchange)
        yield(index, d2s(date), numcases, change, avchange, edate,
              '{:,}'.format(round(total_estimate)),
              '{:,}'.format(round(est2)),
              d2s(date + datetime.timedelta(toamil)),              
              d2s(date + datetime.timedelta(toamilX)),
              doubling_time
              )

def docalcs(data, country=None, edate='5/1/20'):
    if country is None:
        results = {}
        for c in data:
            results[c] = estimate(caserates(data[c]), edate)
        return results
    else:
        return estimate(caserates(data[country]), edate)

def sumup(data):
    result=None
    for key, series in data.items():
        if result is None:
            result = A([x[1] for x in series])
            dates = [x[0] for x in series]
        else:
            result += A([x[1] for x in series])
    return list(zip(dates, result))

def dumpout(series, edate='5/1/20'):
    for xitem in estimate(caserates(series), edate):
        print(xitem)

def dumpall(data):
    for key in data:
        series=list(caserates(data[key]))
        print(key, series[-2:-1])
        print(key, series[-1:])

datadir = os.path.join(os.getenv('HOME'), 'COVID-19', 'csse_covid_19_data', 'csse_covid_19_time_series')

Odata=getall(loadcsvf(os.path.join(datadir, 'time_series_covid19_confirmed_global.csv')))
USdata=getallUS(loadcsvf(os.path.join(datadir, 'time_series_covid19_confirmed_US.csv')))

data=Odata
data['US'] = sumup(USdata)
data.update(USdata)

#pp(list(caserates(data[sys.argv[2]])))
if __name__ == '__main__':
    if sys.argv[1] == 'X':
        dumpall(data)
        sys.exit(0)
    if sys.argv[1] == 'world':
        dumpout(sumup(data), sys.argv[2])
    elif sys.argv[1] in USdata.keys():
        dumpout(USdata[sys.argv[1]], sys.argv[2])
    else:
        dumpout(data[sys.argv[1]], sys.argv[2])

#for xitem in estimate(caserates(data[sys.argv[1]]), sys.argv[2]):
#    print(xitem)
