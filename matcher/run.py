from baseline_matcher import LinearMatcher

m = LinearMatcher()
m.train_all()
#m.validate()
m.plot_accuracy_vs_examples()
