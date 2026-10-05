import pandas as pd


# ==========================================
# Charger les données
# ==========================================

data = pd.read_csv("chapter_dataset.csv")


# ==========================================
# Élève
# ==========================================

student_id = 1

student_data = data[
    data["student_id"] == student_id
].copy()


# ==========================================
# Temps disponible par jour
# ==========================================

daily_time = 90


# ==========================================
# Calculer la priorité
# ==========================================

def calculate_priority(score):

    if score < 40:
        return 4

    elif score < 50:
        return 3

    elif score < 70:
        return 2

    elif score < 85:
        return 1

    else:
        return 0


# ==========================================
# Ajouter la priorité
# ==========================================

student_data["priority"] = student_data[
    "score"
].apply(calculate_priority)


# ==========================================
# Garder les chapitres à travailler
# ==========================================

chapters_to_study = student_data[
    student_data["score"] < 85
].copy()


# ==========================================
# Trier par priorité
# ==========================================

chapters_to_study = chapters_to_study.sort_values(
    by="priority",
    ascending=False
)


# ==========================================
# Calculer le temps
# ==========================================

total_priority = chapters_to_study[
    "priority"
].sum()


if total_priority == 0:

    print("🎉 Aucun chapitre important à réviser.")

else:

    chapters_to_study["study_time"] = (
        chapters_to_study["priority"]
        / total_priority
        * daily_time
    )

    chapters_to_study["study_time"] = (
        chapters_to_study["study_time"]
        .round()
        .astype(int)
    )


# ==========================================
# Afficher le planning
# ==========================================

print("\n======================================")
print("       SMARTSTUDY AI")
print("   PLANNING PERSONNALISÉ")
print("======================================")

print(f"\nÉlève : {student_id}")
print(f"Temps disponible : {daily_time} minutes/jour")

print("\n--------------------------------------")
print("📅 PLANNING DU JOUR")
print("--------------------------------------")


total_time = 0


for _, row in chapters_to_study.iterrows():

    if row["study_time"] <= 0:
        continue

    print(
        f"\n📚 {row['chapter']}"
    )

    print(
        f"Score actuel : {row['score']}%"
    )

    print(
        f"Priorité : {row['priority']}/4"
    )

    print(
        f"⏱️ Temps conseillé : "
        f"{row['study_time']} minutes"
    )

    total_time += row["study_time"]


print("\n--------------------------------------")

print(
    f"⏱️ Temps total : "
    f"{total_time} minutes"
)

print(
    f"⏳ Temps disponible : "
    f"{daily_time} minutes"
)


# ==========================================
# Vérification
# ==========================================

if total_time > daily_time:

    print(
        "\n⚠️ Le planning dépasse "
        "le temps disponible."
    )

else:

    remaining = daily_time - total_time

    print(
        f"\n🕐 Temps restant : "
        f"{remaining} minutes"
    )


print("\n======================================")