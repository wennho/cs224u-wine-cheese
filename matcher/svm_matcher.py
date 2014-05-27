from linear_matcher import LinearMatcher
from sklearn.svm import SVR
import numpy as np
import logging



class SVMMatcher(LinearMatcher):
    def __init__(self):
        LinearMatcher.__init__(self)

    def train(self, pairings):
        X, Y = self.getXY(pairings)
        self.svms = []
        for i in range(self.wine_feat_len):
            svm = SVR(kernel='rbf')
            svm.fit(X, Y[:, i])
            self.svms.append(svm)

    def predict_feat(self, cheese_desc):
        result = []
        for svm in self.svms:
            result.append(svm.predict([cheese_desc])[0])
        return np.array(result)
