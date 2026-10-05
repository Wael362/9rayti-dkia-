import pandas as pd


# ==========================================
# Charger les résultats
# ==========================================

data = pd.read_csv("chapter_dataset.csv")


# ==========================================
# Élève à analyser
# ==========================================

student_id = 1


student_data = data[
    data["student_id"] == student_id
]


# ==========================================
# Affichage
# ==========================================

print("\n================================")
print("       SMARTSTUDY AI")
print("================================")

print(f"\nAnalyse de l'élève : {student_id}")

print("\n--------------------------------")
print("Résultats par chapitre")
print("--------------------------------")


for _, row in student_data.iterrows():

    chapter = row["chapter"]
    score = row["score"]

    if score < 50:

        status = "🔴 FAIBLE"

    elif score < 70:

        status = "🟡 MOYEN"

    elif score < 85:

        status = "🟢 BON"

    else:

        status = "⭐ EXCELLENT"


    print(
        f"{chapter:<25} "
        f"{score:>3}%  "
        f"{status}"
    )


# ==========================================
# Points faibles
# ==========================================

weak_chapters = student_data[
    student_data["score"] < 50
]


print("\n--------------------------------")
print("🔴 POINTS FAIBLES")
print("--------------------------------")


if len(weak_chapters) == 0:

    print("Aucune difficulté importante.")

else:

    for _, row in weak_chapters.iterrows():

        print(
            f"- {row['chapter']} : "
            f"{row['score']}%"
        )


# ==========================================
# Points forts
# ==========================================

strong_chapters = student_data[
    student_data["score"] >= 85
]


print("\n--------------------------------")
print("🟢 POINTS FORTS")
print("--------------------------------")


if len(strong_chapters) == 0:

    print("Aucun chapitre maîtrisé.")

else:

    for _, row in strong_chapters.iterrows():

        print(
            f"- {row['chapter']} : "
            f"{row['score']}%"
        )