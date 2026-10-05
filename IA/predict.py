import pandas as pd
import joblib


# ==========================================
# 1. Charger le modèle
# ==========================================

model = joblib.load("model.pkl")
scaler = joblib.load("scaler.pkl")


# ==========================================
# 2. Informations du nouvel élève
# ==========================================

math_score = 45
physics_score = 75
chemistry_score = 55
study_time = 2


# ==========================================
# 3. Créer les données de l'élève
# ==========================================

student = pd.DataFrame(
    [[
        math_score,
        physics_score,
        chemistry_score,
        study_time
    ]],
    columns=[
        "math_score",
        "physics_score",
        "chemistry_score",
        "study_time"
    ]
)


# ==========================================
# 4. Normaliser les données
# ==========================================

student_scaled = scaler.transform(student)


# ==========================================
# 5. Faire la prédiction
# ==========================================

prediction = model.predict(student_scaled)


# ==========================================
# 6. Afficher le résultat
# ==========================================

print("==============================")
print("     SMARTSTUDY AI")
print("==============================")

print(f"Mathématiques : {math_score}%")
print(f"Physique      : {physics_score}%")
print(f"Chimie        : {chemistry_score}%")
print(f"Temps étude   : {study_time} h/jour")

print("------------------------------")

print(f"Niveau estimé : {prediction[0]}")

print("==============================")