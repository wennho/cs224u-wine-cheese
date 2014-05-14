import numpy as np
import pickle
import sys

# Uses least-squares linear regression for cheese-wine matching.
# Call train() before calling predict()
class LinearMatcher:
    def __init__(self):
        self.A = None
        self.wines = {}
        self.cheeses = {}
        self.pairingsDict = pickle.load(open('cheese_wine_dict.p', 'rb'))
        self.excluded_wines = [
            'Red Blends',
            'White Blends',
            'White Wine',
            'NonVintage',
            'Vintage',
        ]

        # build data. file types are provided in pickle_file_summary.txt
        wine_features = pickle.load(open('../wine_type_descriptor_mat.p', 'rb'))
        wine_names = pickle.load(open('../wine_type_list.p', 'rb'))
        cheese_features = pickle.load(open('../cheese_type_descriptor_mat.p', 'rb'))
        cheese_names = pickle.load(open('../cheese_names_list.p', 'rb'))

        for index, wine_name in enumerate(wine_names):
            self.wines[wine_name] = wine_features[index, :]

        for index, cheese_name in enumerate(cheese_names):
            self.cheeses[cheese_name] = cheese_features[index, :]


    def train(self):

        pairings = []
        for cheese, wine_list in self.pairingsDict.iteritems():
            for wine in wine_list:
                pairings.append((cheese, wine))
        self.train(pairings)


    def train(self, pairings):
        # We want to find A that best satisfies AX = Y. The solution is A = (X^T X)^-1 X^T Y
        # X is the cheese data, one column per cheese
        # Y is the wine data, one column per wine

        # build X & Y
        X = []
        Y = []
        for cheese, wine in pairings:
            cheese_desc = self.cheeses[cheese]
            wine_desc = self.wines[wine]
            X.append(cheese_desc)
            Y.append(wine_desc)

        # perform least-squares regression
        X = np.array(X)
        Y = np.array(Y)
        self.A = (np.linalg.lstsq(np.dot(X.T, X), np.dot(X.T, Y))[0]).T


    def validate(self):
        result = []
        for cheese_leaveout in self.cheeses.iterkeys():
            pairings = []
            for cheese, wine_list in self.pairingsDict.iteritems():
                if cheese == cheese_leaveout:
                    continue
                for wine in wine_list:
                    pairings.append((cheese, wine))
            self.train(pairings)
            prediction = self.predict(cheese_leaveout)
            if prediction in self.pairingsDict[cheese_leaveout]:
                result.append(1.0)
            else:
                print 'WRONG: Predicted', prediction, 'for', cheese_leaveout, 'but expected one of', \
                    self.pairingsDict[cheese_leaveout]
                result.append(0.0)
        print 'Leave-one-out validation on', len(result), 'examples'
        print 'Average accuracy:', sum(result) / len(result)

    # need to call train() first
    def predict(self, cheese_name):
        cheese_desc = self.cheeses[cheese_name]
        wine_desc = np.dot(self.A, cheese_desc)

        # find closest-matching wine
        min_dist = sys.float_info.max
        best_wine = None
        for wine_name, desc in self.wines.iteritems():
            if wine_name in self.excluded_wines:
                continue
            dist = np.linalg.norm(wine_desc - desc)
            if dist < min_dist:
                min_dist = dist
                best_wine = wine_name
        return best_wine

