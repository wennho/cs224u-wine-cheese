import pickle

convert_dict = {
    'Gewurz-Traminer': 'Gewurztraminer',
    'PinotBlanc': 'Pinot Blanc',
    'Champagne': 'White Wine',
    'Chanin Blanc': 'Chenin Blanc',
    'Chianti': 'Sangiovese',
    'Dessertwine': 'Dessert',
    'GrunerVeltiner': 'Gruner Veltliner',
    'Rioja': 'Tempranillo',
    'Pinot Gris': 'Pinot GrisGrigio',
    'Chiraz': 'SyrahShiraz',
    'SauvignonBlanc': 'Sauvignon Blanc',
}

pairings = pickle.load(open('../cheese_wine_dict.p', 'rb'))

for cheese, wine_list in pairings.iteritems():
    for key, val in convert_dict.iteritems():
        if key in wine_list:
            wine_list.remove(key)
            wine_list.append(val)

pickle.dump(pairings, open('cheese_wine_dict.p', 'wb'))