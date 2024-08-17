if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

import pandas as pd

from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LinearRegression

@transformer
def transform(data, *args, **kwargs):
    """
    Template code for a transformer block.

    Add more parameters to this function if this block has multiple parent blocks.
    There should be one parameter for each output variable from each parent block.

    Args:
        data: The output from the upstream parent block
        args: The output from any additional upstream blocks (if applicable)

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    # Specify your transformation logic here
    y_train = data['duration'].values
    df = data[['PULocationID', 'DOLocationID']]
    df_dicts = df.to_dict(orient='records')
    # Fit a dictionary vectorizer
    vectorizer = DictVectorizer()
    X_train = vectorizer.fit_transform(df_dicts)
    # Q5. Training a model
    # Now let's use the feature matrix from the previous step to train a model.
    # Train a plain linear regression model with default parameters, where duration is the response variable
    logreg = LinearRegression()
    logreg.fit(X_train, y_train)
    print(logreg.intercept_)

    return logreg, vectorizer


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'