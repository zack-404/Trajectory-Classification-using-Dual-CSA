from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

from params import N_CLASS, movement_features, MAX_SEGMENT_SIZE, TOTAL_EMBEDDING_DIM

from dataset import *
from trajectory_extraction import modes_to_use
#RandomForestClassifier(),SVC(),KNeighborsClassifier(),   MLPClassifier(), DecisionTreeClassifier(),
ml_models = [ SVC() ]

n_features = len(movement_features)
x_train = np.squeeze(x_trj_seg_clean_of_train)
x_test = np.squeeze(x_trj_seg_clean_of_test)

# construct data suitable for ml classifier
# https://stackoverflow.com/questions/57371065/how-to-use-time-series-data-in-classification-in-sklearn
x_train_features = []
for i in range(n_features):
    x_train_features.append(x_train[:, :, i])
x_train = np.hstack(x_train_features)
x_test_features = []
for i in range(n_features):
    x_test_features.append(x_test[:, :, i])
x_test = np.hstack(x_test_features)


def show_confusion_matrix(y_pred):
    print('\n###########')
    y_true = np.argmax(y_test, axis=1)
    cm = confusion_matrix(y_true, y_pred, labels=modes_to_use)
    print(cm)
    re = classification_report(y_true, y_pred, target_names=['walk', 'bike', 'bus', 'driving', 'train/subway'],
                               digits=5)
    print(re)


# for i, model in enumerate(ml_models):
#     print('$$$$ {} $$$$'.format(i))
#     model.fit(x_train, y_train)
#     y_pred = model.predict(x_test)
#     y_pred = np.argmax(y_pred, axis=1)
#     show_confusion_matrix(y_pred)


def svc_classification():
    model = SVC()
    # for svc, y is not one-hot encoding
    y_train_ = np.argmax(y_train, axis=1)
    model.fit(x_train, y_train_)
    y_pred = model.predict(x_test)
    show_confusion_matrix(y_pred)

svc_classification()
