import numpy as np
import pandas as pd
import sklearn.metrics as skm
from rpy2.robjects import r
from rpy2.robjects.packages import importr
from rpy2.robjects.vectors import (
    FloatVector,
    IntVector,
    FactorVector,
    StrVector,
)
from sklearn.base import ClassifierMixin
from .base import Base
from .utils import format_value, r_list_to_namedtuple

base = importr("base")
stats = importr("stats")
utils = importr("utils")


class Classifier(Base, ClassifierMixin):
    """
    Classifier.
    """

    def __init__(
        self,
        method="ranger",
        pi_method="none",
        level=95,
        type_prediction_set="score",
        B=100,
        nb_hidden=0,
        nodes_sim="sobol",
        activ="relu",
        seed=123,
    ):
        """
        Initialize the model.
        """
        super().__init__(
            name="Classifier",
            type="classification",
            method=method,
            pi_method=pi_method,
            level=level,
            B=B,
            nb_hidden=nb_hidden,
            nodes_sim=nodes_sim,
            activ=activ,
            seed=seed,
        )

        self.type_prediction_set = type_prediction_set

        try:
            r_obj_command = (
                "suppressWarnings(suppressMessages(library(learningmachine))); "
                + "Classifier$new(method = "
                + str(format_value(self.method))
                + ", "
                + "pi_method = "
                + str(format_value(self.pi_method))
                + ", "
                + "level = "
                + str(format_value(self.level))
                + ", "
                + "type_prediction_set = "
                + str(format_value(self.type_prediction_set))
                + ", "
                + "B = "
                + str(format_value(self.B))
                + ", "
                + "nb_hidden = "
                + str(format_value(self.nb_hidden))
                + ", "
                + "nodes_sim = "
                + str(format_value(self.nodes_sim))
                + ", "
                + "activ = "
                + str(format_value(self.activ))
                + ", "
                + "seed = "
                + str(format_value(self.seed))
                + ")"
            )
            self.obj = r(r_obj_command)
        except Exception:
            try:
                self.obj = r(
                    f"suppressWarnings(suppressMessages(library(learningmachine))); Classifier$new(method = {format_value(self.method)}, pi_method = {format_value(self.pi_method)}, level = {format_value(self.level)}, type_prediction_set = {format_value(self.type_prediction_set)}, B = {format_value(self.B)}, nb_hidden = {format_value(self.nb_hidden)}, nodes_sim = {format_value(self.nodes_sim)}, activ = {format_value(self.activ)}, seed = {format_value(self.seed)})"
                )
            except Exception:
                self.obj = r(
                    f"learningmachine::Classifier$new(method = {format_value(self.method)}, pi_method = {format_value(self.pi_method)}, level = {format_value(self.level)}, type_prediction_set = {format_value(self.type_prediction_set)}, B = {format_value(self.B)}, nb_hidden = {format_value(self.nb_hidden)}, nodes_sim = {format_value(self.nodes_sim)}, activ = {format_value(self.activ)}, seed = {format_value(self.seed)})"
                )

    def fit(self, X, y, **kwargs):
        """
        Fit the model according to the given training data.
        """
        params_dict = {}

        for k, v in kwargs.items():
            if k == "lambda_":
                params_dict["lambda"] = v
            elif "__" in k:
                params_dict[k.replace("__", ".")] = v
            else:
                params_dict[k] = v

        if isinstance(X, pd.DataFrame):
            self.column_names = X.columns
            X_r = r.matrix(
                FloatVector(X.values.ravel()),
                byrow=True,
                ncol=X.shape[1],
                nrow=X.shape[0],
            )
            X_r.colnames = StrVector(self.column_names)
        else:
            X_r = r.matrix(
                FloatVector(X.ravel()),
                byrow=True,
                ncol=X.shape[1],
                nrow=X.shape[0],
            )

        if isinstance(y, pd.DataFrame) or isinstance(y, pd.Series):
            y = y.values.ravel()

        self.obj["fit"](X_r, FactorVector(IntVector(y)), **params_dict)
        self.classes_ = np.unique(y)  # /!\ do not remove
        return self

    def predict_proba(self, X):
        """
        Predict using the model.
        """

        if isinstance(X, pd.DataFrame):
            X_r = r.matrix(
                FloatVector(X.values.ravel()),
                byrow=True,
                ncol=X.shape[1],
                nrow=X.shape[0],
            )
            X_r.colnames = StrVector(self.column_names)
        else:
            X_r = r.matrix(
                FloatVector(X.ravel()),
                byrow=True,
                ncol=X.shape[1],
                nrow=X.shape[0],
            )

        if self.pi_method == "none":
            if isinstance(X, pd.DataFrame):
                res = self.obj["predict_proba"](X_r)
            return np.asarray(res)
        if isinstance(X, pd.DataFrame):
            return r_list_to_namedtuple(self.obj["predict_proba"](X_r))

    def predict(self, X):
        """
        Predict using the model.
        """

        if isinstance(X, pd.DataFrame):
            X_r = r.matrix(
                FloatVector(X.values.ravel()),
                byrow=True,
                ncol=X.shape[1],
                nrow=X.shape[0],
            )
            X_r.colnames = StrVector(self.column_names)
        else:
            X_r = r.matrix(
                FloatVector(X.ravel()),
                byrow=True,
                ncol=X.shape[1],
                nrow=X.shape[0],
            )

        if self.pi_method == "none":
            return np.asarray(self.obj["predict"](X_r)) - 1

        return r_list_to_namedtuple(self.obj["predict"](X_r))
