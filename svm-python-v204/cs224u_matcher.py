"""A module for SVM^python for wine-cheese learning."""

import svmapi

from matcher.linear_matcher import LinearMatcher
import numpy as np

linearMatcher = LinearMatcher()

pairings = []
for cheese, wine_list in linearMatcher.pairingsDict.iteritems():
    for wine in wine_list:
        pairings.append((linearMatcher.cheeses[cheese], linearMatcher.wines[wine]))


def read_examples(filename, sparm):
    """Parses an input file into an example sequence."""
    # This reads example files of the type read by SVM^multiclass.
    examples = pairings
    # Print out some very useful statistics.
    print len(examples), 'examples read'
    return examples


def init_model(sample, sm, sparm):
    """Store the number of features and classes in the model."""
    # Note that these features will be stored in the model and written
    # when it comes time to write the model to a file, and restored in
    # the classifier when reading the model from the file.
    sm.num_features = (linearMatcher.cheese_feat_len + 1) * linearMatcher.wine_feat_len
    sm.size_psi = sm.num_features


def get_wine_desc(x, sm):
    cheese_feat = x
    A = np.array(list(sm.w)).reshape((linearMatcher.wine_feat_len, linearMatcher.cheese_feat_len + 1))
    wine_desc = np.dot(A, cheese_feat)
    return wine_desc


def classify_example(x, sm, sparm):
    """Returns the classification of an example 'x'."""
    # Construct the discriminant-label pairs.
    wine_feat = get_wine_desc(x, sm)
    wine_name = linearMatcher.closest_wine(wine_feat)
    # Return the label with the max discriminant value.
    return linearMatcher.wines[wine_name]


def find_most_violated_constraint(x, y, sm, sparm):
    # print sm.w
    """Returns the most violated constraint for example (x,y)."""
    # Similar, but include the loss.
    wine_desc = get_wine_desc(x, sm)
    wine_distances = [(loss(y, desc, sparm) - np.linalg.norm(wine_desc - desc), desc)
                      for desc in linearMatcher.wines.itervalues()]
    most_violated = max(wine_distances)[1]
    return most_violated


def psi(x, y, sm, sparm):
    """Returns the combined feature vector Psi(x,y)."""
    # Just increment the feature index to the appropriate stack position.
    #vecness = [(k,v) for k,v in x]
    # print x

    return svmapi.Sparse(list(x) + list(y))


def loss(y, ybar, sparm):
    """Loss is 1 if the labels are different, 0 if they are the same."""

    return 100.0 * np.linalg.norm(y - ybar)

def print_learning_stats(sample, sm, cset, alpha, sparm):
    """Print statistics once learning has finished.

    This is called after training primarily to compute and print any
    statistics regarding the learning (e.g., training error) of the
    model on the training sample.  You may also use it to make final
    changes to sm before it is written out to a file.  For example, if
    you defined any non-pickle-able attributes in sm, this is a good
    time to turn them into a pickle-able object before it is written
    out.  Also passed in is the set of constraints cset as a sequence
    of (left-hand-side, right-hand-side) two-element tuples, and an
    alpha of the same length holding the Lagrange multipliers for each
    constraint.

    The default behavior is that nothing is printed."""
    print 'Model learned:',
    print '[',', '.join(['%g'%i for i in sm.w]),']'
    print 'Losses:',
    print [loss(y, classify_example(x, sm, sparm), sparm) for x,y in sample]