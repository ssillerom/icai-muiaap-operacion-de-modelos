import os
import joblib
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

X, y = load_iris(return_X_y=True)
X_tr, X_te, y_tr, y_te = train_test_split(
    X, y, test_size=0.2, random_state=42)

model = LogisticRegression(max_iter=200).fit(X_tr, y_tr)
print(f"Accuracy: {model.score(X_te, y_te):.2f}")

os.makedirs("models", exist_ok=True)
joblib.dump(model, "models/model.joblib")
print("Modelo guardado en models/model.joblib")
