import pickle

convert_dict = {
    'Gewurz-Traminer': 'Gewurztraminer',
    'PinotBlanc': 'Pinot Blanc',
    'Champagne': 'White Wine',
    'champagne': 'White Wine',
    'Sparkling wine': 'White Wine',
    'Orvieto': 'White Wine',
    'Gavi': 'White Wine',
    'Ribeiro': 'White Wine',
    'Chanin Blanc': 'Chenin Blanc',
    'Chianti': 'Sangiovese',
    'Dessertwine': 'Dessert',
    'Sauternes': 'Dessert',
    'GrunerVeltiner': 'Gruner Veltliner',
    'Rioja': 'Tempranillo',
    'Riojas': 'Tempranillo',
    'Pinot Gris': 'Pinot GrisGrigio',
    'Pinot Grigio': 'Pinot GrisGrigio',
    'Chiraz': 'SyrahShiraz',
    'Shiraz': 'SyrahShiraz',
    'Syrah': 'SyrahShiraz',
    'Syrah/Shiraz': 'SyrahShiraz',
    'SauvignonBlanc': 'Sauvignon Blanc',
    'Sauvignon blanc': 'Sauvignon Blanc',
    'Fume Blanc': 'Sauvignon Blanc',
    'Pouilly Fume': 'Sauvignon Blanc',
    'Sancerre': 'Sauvignon Blanc',
    'Red Sancerre': 'Pinot Noir',
    'Pino Noir': 'Pinot Noir',
    'Cabernet Saubvignon': 'Cabernet Sauvignon',
    'Burgundy': 'Red Wine',
    'Bordeaux': 'Bordeaux Red Blends',
    'Rhone reds': 'Rhone Red Blends',
    'Rhone': 'Rhone Red Blends',
    'Cotes du Rhone': 'Rhone Red Blends',
    'Beaujolais': 'Gamay',
    'Beaujolais Nouveau': 'Gamay',
    'Prosecco': 'White Wine',
    'Chablis': 'Chardonnay',
    'White Zinfandel': 'Zinfandel',
    'Zinfadel': 'Zinfandel',
    'Moscato': 'Muscat',
    'Viogner': 'Viognier',
    'Banyuls': 'Grenache',
    'Cotes du Jura': 'Chardonnay',
    'Barolo': 'Nebbiolo',
    'Manzanilla': 'Sherry',
}

discard_list = [
    'Lager',
    'Pale ale',
    'Marc de Bourgogne', # is brandy
    'whiskey',
    'Cotes d Auvergne', # no specific grape
]

pairings = pickle.load(open('../100cheese_wine_dict.p', 'rb'))

for cheese, wine_list in pairings.iteritems():
    for key, val in convert_dict.iteritems():
        if key in wine_list:
            wine_list.remove(key)
            if val not in wine_list:
                wine_list.append(val)
    for discard in discard_list:
        if discard in wine_list:
            wine_list.remove(discard)

pickle.dump(pairings, open('100cheese_wine_dict.p', 'wb'))