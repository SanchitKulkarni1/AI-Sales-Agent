import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.metrics import roc_auc_score, classification_report

# -----------------------------
# 1. Load Dataset
# -----------------------------
df = pd.read_csv("data/Lead Scoring.csv")

# Replace placeholder 'Select' with NA
df = df.replace("Select", '0')

# -----------------------------
# 2. Drop ID + Leakage Columns
# -----------------------------
ID_COLS = ["Prospect ID", "Lead Number"]

LEAKAGE_COLS = [
    "Lead Quality",
    "Tags",
    "Asymmetrique Activity Index",
    "Asymmetrique Profile Index",
    "Asymmetrique Activity Score",
    "Asymmetrique Profile Score",
    "Lead Profile"
]

df = df.drop(columns=ID_COLS + LEAKAGE_COLS, errors="ignore")

# -----------------------------
# 3. Define Target & Features
# -----------------------------
TARGET = "Converted"

X = df.drop(columns=[TARGET])
y = df[TARGET]

# Identify column types
numeric_features = X.select_dtypes(include=["int64", "float64"]).columns
categorical_features = X.select_dtypes(include=["object"]).columns

# -----------------------------
# 4. Preprocessing Pipelines
# -----------------------------
numeric_transformer = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler())
])

categorical_transformer = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="constant", fill_value="Missing")),
    ("onehot", OneHotEncoder(handle_unknown="ignore"))
])

preprocessor = ColumnTransformer(
    transformers=[
        ("num", numeric_transformer, numeric_features),
        ("cat", categorical_transformer, categorical_features)
    ]
)

# -----------------------------
# 5. Train / Test Split (STRATIFIED)
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# -----------------------------
# 6. Model Pipeline
# -----------------------------
model = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("classifier", LogisticRegression(
        max_iter=1000,
        class_weight="balanced"  # important for imbalance
    ))
])

print("Training model...")
model.fit(X_train, y_train)
FEATURE_COLUMNS = X.columns.tolist()

# -----------------------------
# 7. Evaluation (Correct Metrics)
# -----------------------------
y_pred_prob = model.predict_proba(X_test)[:, 1]
y_pred = model.predict(X_test)

roc_auc = roc_auc_score(y_test, y_pred_prob)

print("\nROC-AUC Score:", round(roc_auc, 4))
print("\nClassification Report:\n")
print(classification_report(y_test, y_pred))

# -----------------------------
# 8. Save Model Artifact
# -----------------------------
joblib.dump(model, "lead_conversion_model.pkl")
joblib.dump(FEATURE_COLUMNS, "feature_columns.pkl")
print("\nModel saved as lead_conversion_model.pkl")
