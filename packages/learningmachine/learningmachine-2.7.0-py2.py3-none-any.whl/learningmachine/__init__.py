"""Top-level package for learningmachine."""

__author__ = """T. Moudiki"""
__email__ = "thierry.moudiki@gmail.com"

from .base import Base
from .classifier import Classifier
from .regression import Regressor

__all__ = ["Base", "Classifier", "Regressor"]
