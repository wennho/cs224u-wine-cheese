"""A module for SVM^python for wine-cheese learning."""

import svmapi

from matcher.linear_matcher import LinearMatcher
import numpy as np

linearMatcher = LinearMatcher()

sparseWines = {k: svmapi.Sparse(v) for k, v in linearMatcher.wines.iteritems()}
pairings = []
for cheese, wine_list in linearMatcher.pairingsDict.iteritems():
    for wine in wine_list:
        pairings.append((linearMatcher.cheeses[cheese], sparseWines[wine]))




def read_examples(filename, sparm):
    """Parses an input file into an example sequence."""

    # This reads example files of the type read by SVM^multiclass.
    examples = []
    # Open the file and read each example.
    for cheese, wine in pairings:
        # Get the target.

        # Add the example to the list
        examples.append((svmapi.Sparse(cheese), wine))
        # Print out some very useful statistics.
    print len(examples), 'examples read'
    return examples


def init_model(sample, sm, sparm):
    """Store the number of features and classes in the model."""
    # Note that these features will be stored in the model and written
    # when it comes time to write the model to a file, and restored in
    # the classifier when reading the model from the file.
    sm.num_features = linearMatcher.cheese_feat_len * linearMatcher.wine_feat_len
    sm.size_psi = sm.num_features


def get_wine_desc(x, sm):
    cheese_feat = [0] * linearMatcher.cheese_feat_len
    for k, v in x:
        cheese_feat[k] = v
    A = np.array(list(sm.w)).reshape((linearMatcher.wine_feat_len, linearMatcher.cheese_feat_len))
    wine_desc = np.dot(A, cheese_feat)
    return wine_desc


def classification_score(x, y, sm, sparm):
    """Return an example, label pair discriminant score."""
    # Utilize the svmapi.Model convenience method 'classify'.
    desc = get_wine_desc(x, sm)
    return - np.linalg.norm(desc - y)


def classify_example(x, sm, sparm):
    """Returns the classification of an example 'x'."""
    # Construct the discriminant-label pairs.
    wine_feat = get_wine_desc(x, sm)
    wine_name = linearMatcher.closest_wine(wine_feat)
    # Return the label with the max discriminant value.
    return sparseWines[wine_name]


def find_most_violated_constraint(x, y, sm, sparm):
    # print sm.w
    """Returns the most violated constraint for example (x,y)."""
    # Similar, but include the loss.
    scores = [(classification_score(x, linearMatcher.wines[name], sm, sparm) + loss(y, c, sparm), c)
              for name, c in sparseWines.iteritems()]
    return max(scores)[1]


def psi(x, y, sm, sparm):
    """Returns the combined feature vector Psi(x,y)."""
    # Just increment the feature index to the appropriate stack position.
    #vecness = [(k,v) for k,v in x]
    xList = [(k, v) for k, v in x]
    yList = [(k + linearMatcher.cheese_feat_len, v) for k, v in y]

    return svmapi.Sparse((xList + yList))


def loss(y, ybar, sparm):
    """Loss is 1 if the labels are different, 0 if they are the same."""
    result = 100.0 * int(y != ybar)
    return result


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
    print '[', ', '.join(['%g' % i for i in sm.w]), ']'
    print 'Losses:',
    print [loss(y, classify_example(x, sm, sparm), sparm) for x, y in sample]