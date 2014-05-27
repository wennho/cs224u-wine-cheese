import numpy as np
import pickle
import sys

# Uses least-squares linear regression for cheese-wine matching.
# Call train_all() before calling predict()
class LinearMatcher:
    def __init__(self):
        self.A = None
        self.wines = {}
        self.cheeses = {}
        self.pairingsDict = pickle.load(open('100cheese_wine_dict.p', 'rb'))
        self.excluded_wines = [
            'Red Blends',
            'White Blends',
            'White Wine',
            'NonVintage',
            'Vintage',
            'JunmaiDaiginjo',
        ]

        # build data. file types are provided in pickle_file_summary.txt
        wine_features = pickle.load(open('../wine_type_descriptor_mat.p', 'rb'))
        wine_names = pickle.load(open('../wine_type_list.p', 'rb'))
        cheese_features = pickle.load(open('../100cheese_type_descriptor_mat.p', 'rb'))
        cheese_names = pickle.load(open('../100cheese_names.p', 'rb'))

        self.wine_feat_len = wine_features.shape[1]
        self.cheese_feat_len = cheese_features.shape[1]

        for index, wine_name in enumerate(wine_names):
            self.wines[wine_name] = wine_features[index, :]

        for index, cheese_name in enumerate(cheese_names):
            self.cheeses[cheese_name] = np.hstack((cheese_features[index, :], [1]))


    def getXY(self, pairings):
        X = []
        Y = []
        for cheese, wine in pairings:
            cheese_desc = self.cheeses[cheese]
            wine_desc = self.wines[wine]
            X.append(cheese_desc)
            Y.append(wine_desc)
        X = np.array(X)
        Y = np.array(Y)
        return X, Y

    def train(self, pairings):
        # We want to find A that best satisfies AX = Y. The solution is A = (X^T X)^-1 X^T Y
        # X is the cheese data, one column per cheese
        # Y is the wine data, one column per wine

        # build X & Y
        X, Y = self.getXY(pairings)

        # perform least-squares regression
        self.A = (np.linalg.lstsq(np.dot(X.T, X), np.dot(X.T, Y))[0]).T


    def train_all(self):

        pairings = []
        for cheese, wine_list in self.pairingsDict.iteritems():
            for wine in wine_list:
                pairings.append((cheese, wine))
        self.train(pairings)
        result = []
        for cheese in self.cheeses.iterkeys():
            prediction = self.predict(cheese)
            if prediction in self.pairingsDict[cheese]:
                result.append(1.0)
            else:
                print 'WRONG: Predicted', prediction, 'for', cheese, 'but expected one of', \
                    self.pairingsDict[cheese]
                result.append(0.0)
        print 'Trained on', len(result), 'examples'
        print 'Average training accuracy:', sum(result) / len(result)

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


    def closest_wine(self, wine_desc):
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

    # need to call train() first
    def predict(self, cheese_name):
        cheese_desc = self.cheeses[cheese_name]
        wine_desc = self.predict_feat(cheese_desc)
        return self.closest_wine(wine_desc)

    def predict_feat(self, cheese_desc):
        return np.dot(self.A, cheese_desc)