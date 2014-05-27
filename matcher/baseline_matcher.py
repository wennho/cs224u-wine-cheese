import numpy as np
import pickle
import sys
from matplotlib import pylab as plt

#WINE_FEATURE_FILE = '../wine_type_descriptor_mat.p' #orig file
WINE_FEATURE_FILE = '../wine_type_descriptor_mat_pmi.p' #pmi reweighted
#WINE_FEATURE_FILE = '../wine_type_descriptor_mat_pmi_pos_disc.p' #pmi reweighted with positive, discounting
#WINE_FEATURE_FILE = '../wine_type_descriptor_mat_tfidf.p' #tfidf reweighting

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
            'Grenache',
            'Red Wine',
            'Carmenere',
            'Nero dAvola',
            'Barbera',
            'Junmai',
            'Albarino',
            'JunmaiGinjo',
            'Primitivo',
            'Torrontes',
            'Viognier',
            'Dolcetto',
            'Tempranillo',
            'Malbec',
            'Gamay',
            'Nebbiolo',
            'Madeira',
            'Mourvedre',
        ]

        # build data. file types are provided in pickle_file_summary.txt
        wine_features = pickle.load(open(WINE_FEATURE_FILE, 'rb'))
        wine_names = pickle.load(open('../wine_type_list.p', 'rb'))
        cheese_features = pickle.load(open('../100cheese_type_descriptor_mat_lsa.p', 'rb'))
        cheese_names = pickle.load(open('../100cheese_names.p', 'rb'))

        self.wine_feat_len = wine_features.shape[1]
        self.cheese_feat_len = cheese_features.shape[1]

        for index, wine_name in enumerate(wine_names):
            self.wines[wine_name] = wine_features[index, :]

        for index, cheese_name in enumerate(cheese_names):
            self.cheeses[cheese_name] = cheese_features[index, :]


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
                #print 'WRONG: Predicted', prediction, 'for', cheese, 'but expected one of', \
                #    self.pairingsDict[cheese]
                result.append(0.0)
        print 'Trained on', len(result), 'examples'
        print 'Average training accuracy:', sum(result) / len(result)

    def validate(self):
        result = []
        existing_wines = set(self.wines).difference(set(self.excluded_wines))
        for cheese_leaveout in self.cheeses.iterkeys():
            pairings = []
            for cheese, wine_list in self.pairingsDict.iteritems():
                if cheese == cheese_leaveout:
                    continue
                for wine in wine_list:
                    pairings.append((cheese, wine))
            self.train(pairings)
            prediction = self.predict(cheese_leaveout)
            expected_wines = self.pairingsDict[cheese_leaveout]
            can_predict_right = False
            for wine in expected_wines:
                if wine in existing_wines:
                    can_predict_right = True
                    break
            if not can_predict_right:
                continue
            if prediction in self.pairingsDict[cheese_leaveout]:
                result.append(1.0)
            else:
                print 'WRONG: Predicted', prediction, 'for', cheese_leaveout, 'but expected one of', \
                    self.pairingsDict[cheese_leaveout]
                result.append(0.0)
        print 'Leave-one-out validation on', len(result), 'examples'
        print 'Average accuracy:', sum(result) / len(result)

    
    def plot_accuracy_vs_examples(self):
        num_training = range(25, 105, 5)
        accuracy_5top = []
        accuracy_top = []
        existing_wines = set(self.wines).difference(set(self.excluded_wines))
        for num in num_training:
            result_5top = []
            result_top = []
            num_used = 0
            for cheese_leaveout in self.cheeses.iterkeys():
                num_used += 1
                if num_used > num: break
                pairings = []
                for cheese, wine_list in self.pairingsDict.iteritems():
                    if cheese == cheese_leaveout:
                        continue
                    for wine in wine_list:
                        pairings.append((cheese, wine))
                self.train(pairings)
                expected_wines = self.pairingsDict[cheese_leaveout]
                can_predict_right = False
                for wine in expected_wines:
                    if wine in existing_wines:
                        can_predict_right = True
                        break
                if not can_predict_right:
                    continue
                prediction_list = self.predict_list(cheese_leaveout)
                top_prediction = self.predict(cheese_leaveout)
                top_predictions = [pred_dist_pair[0] for pred_dist_pair in prediction_list][0:5]
                found_prediction = False
                for prediction in top_predictions:
                    if prediction in self.pairingsDict[cheese_leaveout]:
                        result_5top.append(1.0)
                        found_prediction = True
                        break
                if not found_prediction:
                    #print 'WRONG: Predicted', prediction, 'for', cheese_leaveout, 'but expected one of', \
                    #    self.pairingsDict[cheese_leaveout]
                    result_5top.append(0.0)
                if top_prediction in self.pairingsDict[cheese_leaveout]:
                    result_top.append(1.0)
                else:
                    result_top.append(0.0)
            print 'Leave-one-out validation on', len(result_top), 'examples'
            print 'Average accuracy:', sum(result_5top) / len(result_5top)
            accuracy_5top.append(sum(result_5top)/len(result_5top))
            accuracy_top.append(sum(result_top)/len(result_top))
        plt.plot(num_training, accuracy_5top, 'g', label='Top 5 predictions')
        plt.plot(num_training, accuracy_top, 'b', label='Top 1 predictions')
        plt.xlabel('number of training examples')
        plt.ylabel('accuracy (Leave one out validation)')
        plt.legend(loc='upper right')
        #plt.ylim(0,0.6)
        plt.title('Accuracy of Linear Regression Predictor \nwith Different Number of Training Examples')
        plt.show()

    # need to call train() first
    def predict(self, cheese_name):
        cheese_desc = self.cheeses[cheese_name]
        wine_desc = self.predict_feat(cheese_desc)

        # find closest-matching wine
        min_dist = sys.float_info.max
        best_wine = None
        best_wines = []
        for wine_name, desc in self.wines.iteritems():
            if wine_name in self.excluded_wines:
                continue
            dist = np.linalg.norm(wine_desc - desc)
	    best_wines.append((wine_name, dist))

            if dist < min_dist:
                min_dist = dist
                best_wine = wine_name
        return best_wine
	#return sorted(best_wines,key=lambda x: x[1])

    def predict_list(self, cheese_name):
        cheese_desc = self.cheeses[cheese_name]
        wine_desc = self.predict_feat(cheese_desc)

        # find closest-matching wine
        min_dist = sys.float_info.max
        best_wines = []
        for wine_name, desc in self.wines.iteritems():
            if wine_name in self.excluded_wines:
                continue
            dist = np.linalg.norm(wine_desc - desc)
            best_wines.append((wine_name, dist))

            if dist < min_dist:
                min_dist = dist
                best_wine = wine_name
        return sorted(best_wines,key=lambda x: x[1])


    def predict_feat(self, cheese_desc):
        return np.dot(self.A, cheese_desc)
