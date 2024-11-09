"""Class for classification models.
"""

import pandas as pd
import numpy as np

# pylint: disable=dangerous-default-value, invalid-name, too-many-instance-attributes, too-many-arguments


class Classifier:
    """Fit, train and get hyperparams of model.
    Parameters:
        model (model Constructor, callable): Model from library to create instance as our classifier.
        X_train, X_test, y_train, y_test (pd.DataFrame, pd.DataFrame, pd.Series, pd.Series): Data for train and test model.
        is_binary_class (bool): Information if classifier is binary -> metrics calculations depend on that.
        params (dict): Hyperparameters for classifier initiation.
        proba (float): For binary classification, threshold for classifing case as True.
    """

    def __init__(
        self,
        model,
        X_train: pd.DataFrame,
        X_test: pd.DataFrame,
        y_train: pd.Series,
        y_test: pd.Series,
        is_binary_class: bool,
        params: dict = {},
        proba: float = 0.5,
    ):
        self.model = model
        self.model_name = type(model()).__name__
        if "id_client" in X_train.columns:
            self.X_train = X_train.drop("id_client", axis=1)
        else:
            self.X_train = X_train
        self.y_train = y_train
        if "id_client" in X_test.columns:
            self.X_test = X_test.drop("id_client", axis=1)
        else:
            self.X_test = X_test
        self.y_test = y_test
        self.random_state = 2024
        self.is_binary_class = is_binary_class
        self.classifier = None
        self.y_pred = []
        self.proba = proba
        self.y_pred_proba = []
        self.fit_predict(params)

    def fit(self, params: dict = None):
        """Fits model to X_train, y_train.

        Args:
            params (dict, optional): Hyperparams for model creation. Defaults to None.
        """
        if params is None:
            params = {}
        self.classifier = (
            self.model(**params) if params != {} else self.model(random_state=self.random_state)
        )
        self.classifier.fit(self.X_train, self.y_train.values.ravel())

    def predict(self):
        """Predict values for self.X_train

        Returns:
            pd.Series: Predicted labels for X_test.
        """
        self.y_pred = self.classifier.predict(self.X_test)
        return self.y_pred

    def fit_predict(self, params={}):
        """Fit model for X_train and predict for X_test.

        Args:
            params (dict, optional): Params for the model. Defaults to {}.

        Returns:
            pd.Series: Predicted labels for X_test.
        """
        self.fit(params)
        self.predict()
        return self.y_pred

    def fit_predict_proba(self):
        """
        Function to train and predict for given threshold (for binary classification only).

        Returns:
            None
        """

        assert self.is_binary_class, "Predict_proba works only for binary classification"

        self.y_pred_proba = (
            self.classifier.predict_proba(self.X_test.values)[:, 1] >= self.proba
        ).astype(bool)

    def hyperparams_model(self):
        """Return all hyperparameters of model, data path and all data columns.

        Returns
        -------
        params
            All params.
        """
        params = {
            key: value
            for key, value in self.classifier.get_params().items()
            if value is not None and value is not np.nan
        }
        params["proba"] = self.proba
        params["feature_names"] = str(self.X_train.columns.tolist())
        return params
