import os
import importlib
import re


moduledict = {}
currentdir = os.path.dirname(os.path.abspath( __file__ ))
#os.chdir(currentdir)
pkg_dir = 'cleaning_by_website_pkg'
print('{}/{}'.format(currentdir,pkg_dir))
for root, dirs, files in os.walk('{}/{}'.format(currentdir,pkg_dir)):
    for filename in files:
        res = re.findall('^([A-Z][A-Za-z _]+).py$', filename)
        if len(res) > 0:
            moduledict[res[0]] = importlib.import_module('{}.{}'.format(pkg_dir,res[0]))
            print(res[0])

def L3_filter(elem):
    if elem['WEBSITE'] in moduledict:
        return True
    else:
        return False


def L3_Cleaning(elem):
    schemalst=['WEBSITE', 'PID', 'shipping', 'brand', 'model', 'UPC',
               'price', 'price_type', 'availability', 'channel', 'LAST_CRAWL']
    retdict={}
    tempdict = moduledict[elem['WEBSITE']].main(elem)
    for eachcol in schemalst:
        if eachcol in tempdict:
            retdict[eachcol] = tempdict[eachcol]
        elif eachcol in elem:
            retdict[eachcol] = elem[eachcol]
        else:
            retdict[eachcol] = None

    return retdict
