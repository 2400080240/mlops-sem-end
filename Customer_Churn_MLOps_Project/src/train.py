from pathlib import Path
import json
import joblib
import mlflow
import mlflow.sklearn
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "churn.csv"
MODEL_DIR = ROOT / "models"
MODEL_DIR.mkdir(exist_ok=True)

df = pd.read_csv(DATA)
df = df.drop(columns=["customerID"], errors="ignore")
df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
if "Churn" not in df.columns:
    raise ValueError("Dataset must contain a 'Churn' target column.")

target = df.pop("Churn")
y = target.map({"Yes": 1, "No": 0})
if y.isna().any():
    raise ValueError("Churn column must contain only Yes/No values or 0/1 values.")
y = y.astype(int)
X = df

numeric = X.select_dtypes(include=["number"]).columns.tolist()
categorical = X.select_dtypes(exclude=["number"]).columns.tolist()

numeric_pipe = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler())
])
categorical_pipe = Pipeline([
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("onehot", OneHotEncoder(handle_unknown="ignore"))
])
preprocess = ColumnTransformer([
    ("num", numeric_pipe, numeric),
    ("cat", categorical_pipe, categorical)
])
pipeline = Pipeline([
    ("preprocess", preprocess),
    ("classifier", LogisticRegression(max_iter=1000, class_weight="balanced"))
])

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

mlflow.set_tracking_uri((ROOT / "mlruns").as_uri())
mlflow.set_tracking_uri("sqlite:///mlflow.db")
mlflow.set_experiment("Customer-Churn-Prediction")

with mlflow.start_run():
    pipeline.fit(X_train, y_train)
    pred = pipeline.predict(X_test)
    prob = pipeline.predict_proba(X_test)[:, 1]
    metrics = {
        "accuracy": accuracy_score(y_test, pred),
        "precision": precision_score(y_test, pred, zero_division=0),
        "recall": recall_score(y_test, pred, zero_division=0),
        "f1": f1_score(y_test, pred, zero_division=0),
        "roc_auc": roc_auc_score(y_test, prob)
    }
    mlflow.log_param("model", "LogisticRegression")
    mlflow.log_param("test_size", 0.2)
    mlflow.log_metrics(metrics)
    mlflow.sklearn.log_model(
        pipeline,
        name="churn_model",
        skops_trusted_types=["numpy.dtype"]
    )
    joblib.dump(pipeline, MODEL_DIR / "churn_model.pkl")
    (ROOT / "reports").mkdir(exist_ok=True)
    (ROOT / "reports" / "metrics.json").write_text(json.dumps(metrics, indent=2))
    X_train.to_csv(ROOT / "data" / "reference.csv", index=False)
    X_test.to_csv(ROOT / "data" / "current.csv", index=False)
    print("Training complete.")
    print(json.dumps(metrics, indent=2))
