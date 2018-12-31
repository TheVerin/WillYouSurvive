from . import preprocessing
from sklearn.ensemble import RandomForestClassifier

y, x = preprocessing.final_data()


def classifier():
    classifier_rf = RandomForestClassifier(n_estimators=500, criterion='gini', random_state=0, class_weight='balanced',
                                           verbose=1)
    return classifier_rf.fit(x, y)
