import pandas as pd
import random


# ==========================================
# Configuration
# ==========================================

NUMBER_OF_STUDENTS = 500


# ==========================================
# Générer les données
# ==========================================

students = []

for i in range(NUMBER_OF_STUDENTS):

    math_score = random.randint(20, 100)
    physics_score = random.randint(20, 100)
    chemistry_score = random.randint(20, 100)

    study_time = round(random.uniform(0.5, 5.0), 1)

    # Score général de l'élève
    average_score = (
        math_score +
        physics_score +
        chemistry_score
    ) / 3

    # ==========================================
    # Déterminer le niveau
    # ==========================================

    if average_score < 45:
        level = "Faible"

    elif average_score < 60:
        level = "Moyen"

    elif average_score < 80:
        level = "Bon"

    else:
        level = "Excellent"

    students.append([
        math_score,
        physics_score,
        chemistry_score,
        study_time,
        level
    ])


# ==========================================
# Créer le DataFrame
# ==========================================

data = pd.DataFrame(
    students,
    columns=[
        "math_score",
        "physics_score",
        "chemistry_score",
        "study_time",
        "level"
    ]
)


# ==========================================
# Sauvegarder
# ==========================================

data.to_csv(
    "dataset.csv",
    index=False
)


print("================================")
print("Dataset créé avec succès !")
print("================================")

print(f"Nombre d'élèves : {len(data)}")

print("\nRépartition des niveaux :")
print(data["level"].value_counts())

print("\nAperçu :")
print(data.head(10))