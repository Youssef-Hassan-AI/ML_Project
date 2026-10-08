"""
predictor.py
------------
Handles all prediction logic, completely independent of the UI.
"""

import os
import joblib
import pandas as pd

# ── Paths ──────────────────────────────────────────────────────────────────────
_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
_MODEL_PATH = os.path.join(_BASE_DIR, "income_model.joblib")
_COLS_PATH  = os.path.join(_BASE_DIR, "model_columns.joblib")

# ── Load once at import time ───────────────────────────────────────────────────
_model   = joblib.load(_MODEL_PATH)
_columns = joblib.load(_COLS_PATH)

# ── Valid categorical values (sourced from the training data) ──────────────────
WORKCLASS_OPTIONS = [
    "Private", "Self-emp-not-inc", "Self-emp-inc",
    "Federal-gov", "Local-gov", "State-gov",
    "Without-pay", "Never-worked", "Unknown",
]

MARITAL_OPTIONS = [
    "Married-civ-spouse", "Divorced", "Never-married",
    "Separated", "Widowed", "Married-spouse-absent", "Married-AF-spouse",
]

OCCUPATION_OPTIONS = [
    "Tech-support", "Craft-repair", "Other-service", "Sales",
    "Exec-managerial", "Prof-specialty", "Handlers-cleaners",
    "Machine-op-inspct", "Adm-clerical", "Farming-fishing",
    "Transport-moving", "Priv-house-serv", "Protective-serv",
    "Armed-Forces", "Unknown",
]

RELATIONSHIP_OPTIONS = [
    "Wife", "Own-child", "Husband",
    "Not-in-family", "Other-relative", "Unmarried",
]

RACE_OPTIONS = [
    "White", "Asian-Pac-Islander", "Amer-Indian-Eskimo", "Other", "Black",
]

SEX_OPTIONS = ["Male", "Female"]

COUNTRY_OPTIONS = [
    "United-States", "Cambodia", "England", "Puerto-Rico", "Canada",
    "Germany", "Outlying-US(Guam-USVI-etc)", "India", "Japan", "Greece",
    "South", "China", "Cuba", "Iran", "Honduras", "Philippines", "Italy",
    "Poland", "Jamaica", "Vietnam", "Mexico", "Portugal", "Ireland",
    "France", "Dominican-Republic", "Laos", "Ecuador", "Taiwan", "Haiti",
    "Columbia", "Hungary", "Guatemala", "Nicaragua", "Scotland",
    "Thailand", "Yugoslavia", "El-Salvador", "Trinadad&Tobago",
    "Peru", "Hong", "Holand-Netherlands", "Unknown",
]


# ── Public prediction function ─────────────────────────────────────────────────
def predict(
    age: int,
    workclass: str,
    education_num: int,
    marital_status: str,
    occupation: str,
    relationship: str,
    race: str,
    sex: str,
    capital_gain: int,
    capital_loss: int,
    hours_per_week: int,
    native_country: str,
):
    """
    Build a feature row from raw inputs, align it with the training columns,
    and return a human-readable prediction label plus confidence.
    """
    person = {
        "age":             age,
        "education.num":   education_num,
        "capital.gain":    capital_gain,
        "capital.loss":    capital_loss,
        "hours.per.week":  hours_per_week,
        "workclass":       workclass,
        "marital.status":  marital_status,
        "occupation":      occupation,
        "relationship":    relationship,
        "race":            race,
        "sex":             sex,
        "native.country":  native_country,
    }

    row = pd.get_dummies(pd.DataFrame([person]))
    row = row.reindex(columns=_columns, fill_value=0)

    result = _model.predict(row)[0]
    proba  = _model.predict_proba(row)[0]
    confidence = round(max(proba) * 100, 1)

    label = ">50K" if result == 1 else "<=50K"
    return label, confidence
