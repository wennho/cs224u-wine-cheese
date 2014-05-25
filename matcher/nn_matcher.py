from baseline_matcher import LinearMatcher
from pybrain.datasets import SupervisedDataSet
from pybrain.tools.neuralnets import NNregression, Trainer
import numpy as np
import logging

logging.getLogger('').setLevel(logging.DEBUG)

class NNMatcher(LinearMatcher):
    def __init__(self):
        LinearMatcher.__init__(self)

    def train(self, pairings):
        self.dataset = SupervisedDataSet(self.cheese_feat_len, self.wine_feat_len)
        for cheese, wine in pairings:
            cheese_desc = self.cheeses[cheese]
            wine_desc = self.wines[wine]
            self.dataset.addSample(cheese_desc, wine_desc)
        self.nn = NNregression(self.dataset, hidden=self.cheese_feat_len + self.wine_feat_len, maxepochs=35)
        self.nn.setupNN()
        self.nn.runTraining()

    def predict_feat(self, cheese_desc):
        return self.nn.Trainer.module.activate(cheese_desc)
