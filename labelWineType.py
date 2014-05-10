__author__ = 'wenhao'

import csv
import sys


wineGroupMappingDict = {
    'Riesling': 1,
    'Cabernet Sauvignon': 2,
    'Chardonnay': 3,
    'Sauvignon Blanc': 4,
    'Bordeaux': 5,
    'Syrah': 6,
    'Shiraz': 6, # syrah/shiraz are the same
    'Pinot Noir':7,
    'Merlot': 8,
    'Other': 9,
}

if __name__ == "__main__":

    if len(sys.argv) < 3:
        print 'Usage: python ' + __file__ + ' <input csv> <output file>'
        sys.exit()

    csvfile = open(sys.argv[1])
    output = open(sys.argv[2], 'wb')
    reader = csv.reader(csvfile)
    for row in reader:
        wineName = row[0]
        written = False
        for type, group in wineGroupMappingDict.iteritems():
            if type in wineName:
                output.write(group + '\n')
                written = True
                break

        if not written:
            output.write(wineGroupMappingDict['Other'] + '\n')