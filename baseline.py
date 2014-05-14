__author__ = 'wenhao'

import csv
import sys
import numpy as np
from collections import OrderedDict

def convertFlavorsToFeatures(flavors, flavorSet):
    feature = []
    for flavor in flavorSet:
        val = 1 if flavor in flavors else 0
        feature.append(val)

    return feature


if __name__ == "__main__":

    if len(sys.argv) < 3:
        print 'Usage: python ' + __file__ + ' <wine data> <wine type 1>....<wine type n>'
        sys.exit()

    # load wines
    csvfile = open(sys.argv[1])
    reader = csv.reader(csvfile)
    row = reader.next()

    for col, text in enumerate(row):
        if 'Flavors' in text:
            flavorCol = col

    wineToFeature = OrderedDict()
    wineFlavorToAdd = {}

    # collect basic features (except for flavors)
    for row in reader:
        wineName = None
        for i, val in enumerate(row):
            if i == 0:
                wineName = val
                wineToFeature[wineName] = []
            elif i == flavorCol:
                wineFlavorToAdd[wineName] = val.split(';')
            else:
                wineToFeature[wineName].append(float(val))


    # collect all flavor descriptors
    allFlavorList = []
    for flavorList in wineFlavorToAdd.itervalues():
        for flavor in flavorList:
            if flavor not in allFlavorList:
                allFlavorList.append(flavor)

    # update wine features with flavors too
    for name, feature in wineToFeature.iteritems():
        feature.extend(convertFlavorsToFeatures(wineFlavorToAdd[name], allFlavorList))
        # convert to numpy array
        arr = np.array(feature)
        wineToFeature[name] = arr

    # collect seed wine data
    seedData = []
    for name in sys.argv[2:]:
        seedData.append(wineToFeature[name])

    # find closest match in other wines
    bestMatch = None
    closestDist = sys.float_info.max
    for name, val in wineToFeature.iteritems():
        if name in sys.argv[2:]:
            continue
        dist = 0
        for feat in seedData:
            dist += np.linalg.norm(val - feat)
        if dist < closestDist:
            closestDist = dist
            bestMatch = name

    if bestMatch:
        print 'Best matching wine type is', bestMatch

    output = open('fakeWine.csv','wb')

    for name in wineToFeature.iterkeys():
        output.write(',' + name)
    output.write('\n')

    for name, val in wineToFeature.iteritems():
        output.write(name)
        for val2 in wineToFeature.itervalues():
            dist = np.linalg.norm(val - val2)
            output.write(',' + str(dist))
        output.write('\n')

