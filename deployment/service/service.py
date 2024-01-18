import os, json
from datetime import datetime, timezone
import cloudpickle
import numpy as np
import pandas as pd
from pymongo import MongoClient
from fastapi.logger import logger


class ScoringService:
    model = None
    specs = None

    @classmethod
    def get_model(cls):
        """Get the model object for this instance, loading it if it's not already loaded."""
        model_path = os.getenv("SM_MODEL_DIR", "/opt/ml/model")
        if cls.model is None:
            with open(os.path.join(model_path, "model.pkl"), "rb") as inp:
                cls.model = cloudpickle.load(inp)

        if cls.specs is None:
            with open(os.path.join(model_path, "specs.json"), "rt") as r:
                cls.specs = json.load(r)

        return cls.model

    @classmethod
    def fetch(cls, **kwargs) -> pd.DataFrame:
        
        return pd.DataFrame.from_dict([kwargs])

    @classmethod
    def predict(cls, input_):
        """For the input, do the predictions and return them.

        Args:
            input (a pandas dataframe): 
                The data on which to do the predictions. There will be 
                one prediction per row in the dataframe"""
        clf = cls.get_model()

        faults = cls.specs['faults']

        try:
            preds = clf.predict(input_)
            if np.all(preds == 0): res = dict(transaction=faults[0])
            else: res = dict(transaction=faults[1])
        except Exception as e:
            res = None
        return res