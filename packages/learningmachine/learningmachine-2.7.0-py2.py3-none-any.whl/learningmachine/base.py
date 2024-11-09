import pandas as pd
import sklearn.metrics as skm
import subprocess
from functools import lru_cache
from sklearn.base import BaseEstimator
from rpy2.robjects.vectors import (
    StrVector,
    ListVector,
    FloatVector,
    IntVector,
    FactorVector,
)
from rpy2.robjects.packages import importr
from rpy2.robjects import r
from rpy2.robjects import NULL as rNULL

base = importr("base")
stats = importr("stats")
utils = importr("utils")


class Base(BaseEstimator):
    """
    Base class.
    """

    def __init__(
        self,
        type=None,
        name="Base",
        method="ranger",
        pi_method="kdesplitconformal",
        level=95,
        B=100,
        nb_hidden=0,
        nodes_sim="sobol",
        activ="relu",
        params=None,
        seed=123,
    ):
        """
        Initialize the model.
        """
        super().__init__()
        self.name = name
        self.type = type
        self.method = method
        self.pi_method = pi_method
        self.level = level
        self.B = B
        self.nb_hidden = nb_hidden
        assert nodes_sim in (
            "sobol",
            "halton",
            "unif",
        ), "must have nodes_sim in ('sobol', 'halton', 'unif')"
        self.nodes_sim = "sobol"
        assert activ in (
            "relu",
            "sigmoid",
            "tanh",
            "leakyrelu",
            "elu",
            "linear",
        ), "must have activ in ('relu', 'sigmoid', 'tanh', 'leakyrelu', 'elu', 'linear')"
        self.activ = activ
        self.params = params
        self.seed = seed
        self.obj = None
        self.column_names = None

    def load_learningmachine(self):
        # Install R packages
        # check "learningmachine" is installed
        commands1_lm = 'base::system.file(package = "learningmachine")'
        # check "learningmachine" is installed locally
        commands2_lm = 'base::system.file("learningmachine_r", package = "learningmachine")'
        exec_commands1_lm = subprocess.run(
            ["Rscript", "-e", commands1_lm], capture_output=True, text=True
        )
        exec_commands2_lm = subprocess.run(
            ["Rscript", "-e", commands2_lm], capture_output=True, text=True
        )
        if (
            len(exec_commands1_lm.stdout) == 7
            and len(exec_commands2_lm.stdout) == 7
        ):  # kind of convoluted, but works
            print("Installing R packages along with 'learningmachine'...")
            commands1 = [
                'try(utils::install.packages(c("R6", "Rcpp", "skimr"), repos="https://cloud.r-project.org", dependencies = TRUE), silent=FALSE)',
                'try(utils::install.packages("learningmachine", repos="https://techtonique.r-universe.dev", dependencies = TRUE), silent=FALSE)',
            ]
            commands2 = [
                'try(utils::install.packages(c("R6", "Rcpp", "skimr"), lib="./learningmachine_r", repos="https://cloud.r-project.org", dependencies = TRUE), silent=FALSE)',
                'try(utils::install.packages("learningmachine", lib="./learningmachine_r", repos="https://techtonique.r-universe.dev", dependencies = TRUE), silent=FALSE)',
            ]
            try:
                for cmd in commands1:
                    subprocess.run(["Rscript", "-e", cmd])
            except NotImplementedError as e:  # can't install packages globally
                subprocess.run(["mkdir", "learningmachine_r"])
                for cmd in commands2:
                    subprocess.run(["Rscript", "-e", cmd])

            try:
                base.library(StrVector(["learningmachine"]))
            except:  # can't load the package from the global environment
                try:
                    base.library(
                        StrVector(["learningmachine"]),
                        lib_loc="learningmachine_r",
                    )
                except:  # well, we tried
                    try:
                        r(
                            "try(suppressWarnings(suppressMessages(library('learningmachine'))), silence=TRUE)"
                        )
                    except:  # well, we tried everything at this point
                        r(
                            "try(suppressWarnings(suppressMessages(library('learningmachine', lib.loc='learningmachine_r'))), silence=TRUE)"
                        )

    def score(self, X, y, scoring=None, **kwargs):
        """Score the model on test set features X and response y.

        Parameters:

            X: {array-like}, shape = [n_samples, n_features]
                Training vectors, where n_samples is the number
                of samples and n_features is the number of features

            y: array-like, shape = [n_samples]
                Target values

            scoring: str
                must be in ('explained_variance', 'neg_mean_absolute_error',
                            'neg_mean_squared_error', 'neg_mean_squared_log_error',
                            'neg_median_absolute_error', 'r2')

            **kwargs: additional parameters to be passed to scoring functions

        Returns:

        model scores: {array-like}

        """

        preds = self.predict(X)

        if self.type == "classification":

            if scoring is None:
                scoring = "accuracy"

            # check inputs
            assert scoring in (
                "accuracy",
                "average_precision",
                "brier_score_loss",
                "f1",
                "f1_micro",
                "f1_macro",
                "f1_weighted",
                "f1_samples",
                "neg_log_loss",
                "precision",
                "recall",
                "roc_auc",
            ), "'scoring' should be in ('accuracy', 'average_precision', \
                            'brier_score_loss', 'f1', 'f1_micro', \
                            'f1_macro', 'f1_weighted',  'f1_samples', \
                            'neg_log_loss', 'precision', 'recall', \
                            'roc_auc')"

            scoring_options = {
                "accuracy": skm.accuracy_score,
                "average_precision": skm.average_precision_score,
                "brier_score_loss": skm.brier_score_loss,
                "f1": skm.f1_score,
                "f1_micro": skm.f1_score,
                "f1_macro": skm.f1_score,
                "f1_weighted": skm.f1_score,
                "f1_samples": skm.f1_score,
                "neg_log_loss": skm.log_loss,
                "precision": skm.precision_score,
                "recall": skm.recall_score,
                "roc_auc": skm.roc_auc_score,
            }

            try:
                preds = preds.ravel().astype(int)
                return scoring_options[scoring](y, preds, **kwargs)
            except TypeError:
                return scoring_options[scoring](y, preds, **kwargs)

        if self.type == "regression":

            if (
                type(preds) == tuple
            ):  # if there are std. devs in the predictions
                preds = preds[0]

            if scoring is None:
                scoring = "neg_mean_squared_error"

            # check inputs
            assert scoring in (
                "explained_variance",
                "neg_mean_absolute_error",
                "neg_mean_squared_error",
                "neg_mean_squared_log_error",
                "neg_median_absolute_error",
                "r2",
            ), "'scoring' should be in ('explained_variance', 'neg_mean_absolute_error', \
                            'neg_mean_squared_error', 'neg_mean_squared_log_error', \
                            'neg_median_absolute_error', 'r2')"

            scoring_options = {
                "explained_variance": skm.explained_variance_score,
                "neg_mean_absolute_error": skm.median_absolute_error,
                "neg_mean_squared_error": skm.mean_squared_error,
                "neg_mean_squared_log_error": skm.mean_squared_log_error,
                "neg_median_absolute_error": skm.median_absolute_error,
                "r2": skm.r2_score,
            }

            return scoring_options[scoring](y, preds, **kwargs)

    def summary(
        self,
        X,
        y,
        class_index=None,
        cl=None,
        type_ci="student",
        show_progress=True,
    ):

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

        if cl is None:

            if self.type == "classification":

                assert (
                    class_index is not None
                ), "For classifiers, 'class_index' must be provided"

                return self.obj["summary"](
                    X=X_r,
                    y=FactorVector(IntVector(y)),
                    class_index=int(class_index) + 1,
                    type_ci=StrVector([type_ci]),
                    show_progress=show_progress,
                )

            elif self.type == "regression":

                return self.obj["summary"](
                    X=X_r,
                    y=FloatVector(y),
                    type_ci=StrVector([type_ci]),
                    show_progress=show_progress,
                )

        else:  # cl is not None, parallel computing

            pass
