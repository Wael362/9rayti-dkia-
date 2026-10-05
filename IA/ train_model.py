import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, classification_report


# ==========================================
# 1. Charger le dataset
# ==========================================

data = pd.read_csv("dataset.csv")

print("Dataset chargé avec succès !")
print(data)


# ==========================================
# 2. Séparer les caractéristiques et la cible
# ==========================================

X = data[
    [
        "math_score",
        "physics_score",
        "chemistry_score",
        "study_time"
    ]
]

y = data["level"]


# ==========================================
# 3. Séparer les données
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)


# ==========================================
# 4. Normaliser les données
# ==========================================

scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)


# ==========================================
# 5. Créer le modèle KNN
# ==========================================

model = KNeighborsClassifier(n_neighbors=3)

model.fit(X_train_scaled, y_train)


# ==========================================
# 6. Tester le modèle
# ==========================================

y_pred = model.predict(X_test_scaled)

accuracy = accuracy_score(y_test, y_pred)

print("\n==============================")
print("Résultat du modèle")
print("==============================")

print(f"Accuracy : {accuracy * 100:.2f}%")

print("\nRapport de classification :")
print(classification_report(y_test, y_pred, zero_division=0))


# ==========================================
# 7. Sauvegarder le modèle
# ==========================================

joblib.dump(model, "model.pkl")
joblib.dump(scaler, "scaler.pkl")

print("\n==============================")
print("Modèle sauvegardé avec succès !")
print("==============================")

print("model.pkl")
print("scaler.pkl")