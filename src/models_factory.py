from sklearn.linear_model import LogisticRegression, RidgeClassifier, SGDClassifier, PassiveAggressiveClassifier, Perceptron
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, AdaBoostClassifier, ExtraTreesClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC, LinearSVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB, BernoulliNB
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis, QuadraticDiscriminantAnalysis
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from catboost import CatBoostClassifier

def get_algorithm_suite(random_state=42):
    """Returns a dictionary of 20 algorithms curated for this project."""
    return {
        "Logistic Regression": LogisticRegression(),
        "Random Forest": RandomForestClassifier(n_estimators=100, random_state=random_state),
        "Gradient Boosting": GradientBoostingClassifier(random_state=random_state),
        "XGBoost": XGBClassifier(use_label_encoder=False, eval_metric='logloss', random_state=random_state),
        "LightGBM": LGBMClassifier(random_state=random_state, verbose=-1),
        "CatBoost": CatBoostClassifier(verbose=0, random_state=random_state, allow_writing_files=False),
        "AdaBoost": AdaBoostClassifier(random_state=random_state),
        "Decision Tree": DecisionTreeClassifier(random_state=random_state),
        "Extra Trees": ExtraTreesClassifier(n_estimators=100, random_state=random_state),
        "SVC (RBF)": SVC(probability=True, random_state=random_state),
        "Linear SVC": LinearSVC(random_state=random_state),
        "KNN": KNeighborsClassifier(),
        "Gaussian NB": GaussianNB(),
        "Bernoulli NB": BernoulliNB(),
        "Ridge Classifier": RidgeClassifier(),
        "SGD Classifier": SGDClassifier(random_state=random_state),
        "Passive Aggressive": PassiveAggressiveClassifier(random_state=random_state),
        "Perceptron": Perceptron(random_state=random_state),
        "LDA": LinearDiscriminantAnalysis(),
        "QDA": QuadraticDiscriminantAnalysis()
    }
