import pandas as pd
import random


NUMBER_OF_STUDENTS = 500

students = []


chapters = [
    "Nombres réels",
    "Suites",
    "Limites",
    "Dérivation",
    "Électricité",
    "Mécanique",
    "Ondes",
    "Acides et bases",
    "Réactions chimiques",
    "Chimie organique"
]


for student_id in range(1, NUMBER_OF_STUDENTS + 1):

    for chapter in chapters:

        score = random.randint(20, 100)

        # Temps consacré au chapitre
        study_time = round(
            random.uniform(0.2, 2.0),
            1
        )

        # Nombre de questions
        questions = 10

        # Nombre de réponses correctes
        correct_answers = round(
            score / 10
        )

        # Déterminer le niveau
        if score < 50:
            level = "Faible"

        elif score < 70:
            level = "Moyen"

        elif score < 85:
            level = "Bon"

        else:
            level = "Excellent"

        students.append([
            student_id,
            chapter,
            score,
            correct_answers,
            questions,
            study_time,
            level
        ])


data = pd.DataFrame(
    students,
    columns=[
        "student_id",
        "chapter",
        "score",
        "correct_answers",
        "questions",
        "study_time",
        "level"
    ]
)


data.to_csv(
    "chapter_dataset.csv",
    index=False
)


print("================================")
print("Dataset par chapitre créé !")
print("================================")

print("Nombre de lignes :", len(data))

print("\nAperçu :")
print(data.head(15))