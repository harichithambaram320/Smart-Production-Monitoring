import pandas as pd
import os

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib


# -----------------------------
# Load Sensor Data
# -----------------------------

file_path = os.path.join(
    "data",
    "sensor_data.csv"
)

df = pd.read_csv(file_path)


# -----------------------------
# Features
# -----------------------------

features = [
    "temperature",
    "vibration",
    "pressure",
    "production_count",
    "error_count"
]

X = df[features]

y = df["machine_condition"]


# -----------------------------
# Train / Test Split
# -----------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)


# -----------------------------
# Random Forest Model
# -----------------------------

model = RandomForestClassifier(
    n_estimators=200,
    random_state=42
)

model.fit(
    X_train,
    y_train
)


# -----------------------------
# Model Evaluation
# -----------------------------

y_pred = model.predict(X_test)

accuracy = accuracy_score(
    y_test,
    y_pred
)

print("\n==============================")
print("Predictive Maintenance Model")
print("==============================")

print(
    f"\nModel Accuracy: {accuracy * 100:.2f}%"
)

print("\nClassification Report:")
print(
    classification_report(
        y_test,
        y_pred
    )
)


# -----------------------------
# Feature Importance
# -----------------------------

print("\nFeature Importance:")

for feature, importance in zip(
    features,
    model.feature_importances_
):

    print(
        f"{feature}: {importance:.4f}"
    )

    top_feature_index = model.feature_importances_.argmax()

model.top_feature = features[top_feature_index]

model.top_feature_importance = (
    model.feature_importances_[top_feature_index]
)


# -----------------------------
# Save Model
# -----------------------------

model_path = os.path.join(
    "models",
    "predictive_maintenance_model.pkl"
)

model.model_accuracy = accuracy

joblib.dump(
    model,
    model_path
)



print(
    f"\nModel saved to: {model_path}"
)