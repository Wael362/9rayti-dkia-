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
# Fonction de recommandation
# ==========================================

def get_recommendation(chapter, score):

    recommendations = {

        "Nombres réels":
            "Revoir les propriétés des nombres réels et faire des exercices de calcul.",

        "Suites":
            "Revoir les suites arithmétiques et géométriques puis faire des exercices.",

        "Limites":
            "Revoir les limites, les formes indéterminées et les méthodes de calcul.",

        "Dérivation":
            "Revoir les règles de dérivation et s'entraîner avec des fonctions.",

        "Électricité":
            "Revoir la loi d'Ohm, les circuits électriques et faire des exercices.",

        "Mécanique":
            "Revoir les forces, le mouvement et les lois de Newton.",

        "Ondes":
            "Revoir les caractéristiques des ondes et leurs formules principales.",

        "Acides et bases":
            "Revoir le pH, les acides, les bases et les réactions acido-basiques.",

        "Réactions chimiques":
            "Revoir l'équilibrage des équations chimiques et les transformations.",

        "Chimie organique":
            "Revoir les fonctions organiques et les principales réactions."
    }


    if score < 40:

        priority = "TRÈS HAUTE"
        study_time = 45

    elif score < 50:

        priority = "HAUTE"
        study_time = 30

    elif score < 70:

        priority = "MOYENNE"
        study_time = 20

    else:

        priority = "FAIBLE"
        study_time = 10


    return {
        "chapter": chapter,
        "score": score,
        "priority": priority,
        "study_time": study_time,
        "recommendation": recommendations.get(
            chapter,
            "Revoir le cours et faire des exercices."
        )
    }


# ==========================================
# Générer les recommandations
# ==========================================

print("\n================================")
print("     SMARTSTUDY AI")
print("     RECOMMANDATIONS")
print("================================")


recommendations = []


for _, row in student_data.iterrows():

    chapter = row["chapter"]
    score = row["score"]

    recommendation = get_recommendation(
        chapter,
        score
    )

    recommendations.append(
        recommendation
    )


# ==========================================
# Afficher uniquement les difficultés
# ==========================================

print("\n🔴 CHAPITRES À RÉVISER")
print("--------------------------------")


has_problem = False


for recommendation in recommendations:

    if recommendation["score"] < 70:

        has_problem = True

        print(
            f"\n📚 {recommendation['chapter']}"
        )

        print(
            f"Score : {recommendation['score']}%"
        )

        print(
            f"Priorité : "
            f"{recommendation['priority']}"
        )

        print(
            f"Temps conseillé : "
            f"{recommendation['study_time']} minutes"
        )

        print(
            f"👉 {recommendation['recommendation']}"
        )


if not has_problem:

    print(
        "\n🎉 Aucun chapitre ne nécessite "
        "une révision importante."
    )


print("\n================================")