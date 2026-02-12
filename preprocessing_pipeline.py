from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import RobustScaler, PowerTransformer, OneHotEncoder
from sklearn.impute import SimpleImputer

def get_preprocessing_pipeline(num_features, cat_features):
    """
    [PROCESS 6: INSTITUTIONAL PREPROCESSING PIPELINE]
    1:1 Port of Masterclass Notebook Logic.
    """
    
    # Numeric Pipeline (Skewness fixed via PowerTransformer + Robust Scaling)
    num_pipe = Pipeline([
        ('impute', SimpleImputer(strategy='median')),
        ('skew_corr', PowerTransformer(method='yeo-johnson')),
        ('scale', RobustScaler())
    ])

    # Categorical Pipeline (One-Hot Encoding)
    cat_pipe = Pipeline([
        ('impute', SimpleImputer(strategy='constant', fill_value='missing')),
        ('ohe', OneHotEncoder(handle_unknown='ignore', drop='first'))
    ])

    # Final Unified Preprocessor
    preprocessor = ColumnTransformer([
        ('num', num_pipe, num_features),
        ('cat', cat_pipe, cat_features)
    ])
    
    return preprocessor
