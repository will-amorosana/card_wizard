import pandas as pd
import sklearn as sk
import sklearn.neural_network as sk_nn
import sklearn.tree as sk_tree
from sklearn.decomposition import PCA



def preprocess_df(df: pd.DataFrame):
    features = [x for x in list(df.columns) if x.startswith("f_")]
    labels = [x for x in list(df.columns) if x.startswith("label_")]

    ml_df = df[features + labels]

    sk_scaler = sk.preprocessing.StandardScaler().fit(ml_df)

    train, test = sk.model_selection.train_test_split(ml_df, test_size = 0.15)

    return ml_df, train[features], train[labels], test[features], test[labels]


def decision_tree():
    tree_clf = sk_tree.DecisionTreeClassifier()
    tree_clf.fit(train_features, train_labels["label_identity"])
    tree_clf.score(test_features, test_labels["label_identity"])


def neural_net_classifier(train_features, train_labels, test_features, test_labels):
    # SKLearn MLP on mono-colored creatures
    sk_clf = sk_nn.MLPClassifier(solver='sgd', hidden_layer_sizes=(10, 6), max_iter = 20000, verbose= True)

    sk_clf.fit(train_features, train_labels["label_identity"])

    sk_clf.score(test_features, test_labels["label_identity"])

def principle_component_analysis