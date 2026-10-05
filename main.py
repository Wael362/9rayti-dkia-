import os
import base64
from datetime import time

import requests
import streamlit as st

from database import (
    create_database,

    create_user,
    login_user,

    save_profile,
    get_profile,

    add_subject,
    get_subjects,
    delete_subject,

    add_course,
    get_courses,
    delete_course,

    add_question,
    get_questions,
    delete_question,

    add_answer,
    get_answers,

    save_result,
    has_test_result,
    get_latest_result,

    delete_availability,
    add_availability,

    delete_planning,
    add_planning,
    get_planning,

    complete_course,
    is_course_completed
)

# ============================================================
# CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="9rayti Dkia",
    page_icon="🎓",
    layout="wide"
)

create_database()


# ============================================================
# IA - OLLAMA
# ============================================================

def ask_ai(question, user_name, profile):
    try:

        if profile:
            level = profile[0]
            branch = profile[1]
        else:
            level = "Non renseigné"
            branch = "Non renseignée"

        system_prompt = f"""
Tu es l'assistant pédagogique de 9rayti Dkia.

Tu aides les élèves marocains à apprendre.

Informations sur l'élève :

Nom : {user_name}
Niveau : {level}
Branche : {branch}

Consignes :

- Réponds principalement en français.
- Adapte tes explications au niveau de l'élève.
- Explique simplement.
- Donne des exemples lorsque c'est utile.
- Pour les mathématiques, détaille les étapes.
- Ne donne pas uniquement la réponse d'un exercice.
- Explique la méthode.
- Si l'élève ne comprend pas, reformule.
- Tu peux répondre en arabe ou en darija si l'élève le demande.
- Encourage l'élève.
- Sois précis et pédagogique.
"""

        prompt = system_prompt + f"""

Question de l'élève :

{question}
"""

        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3.2",
                "prompt": prompt,
                "stream": False
            },
            timeout=120
        )

        response.raise_for_status()

        data = response.json()

        return data.get(
            "response",
            "❌ L'IA n'a pas retourné de réponse."
        )

    except requests.exceptions.ConnectionError:

        return """
❌ Impossible de contacter Ollama.

Vérifiez qu'Ollama est installé et lancé.

Essayez :

ollama run llama3.2
"""

    except requests.exceptions.Timeout:

        return """
⏳ L'IA met trop de temps à répondre.

Veuillez réessayer.
"""

    except Exception as e:

        return f"""
❌ Une erreur est survenue avec l'assistant IA.

Erreur :
{str(e)}
"""


# ============================================================
# PROGRAMME
# ============================================================

PROGRAM = {

    "Tronc Commun": {

        "Sciences": [
            "Mathématiques",
            "Physique-Chimie",
            "Sciences de la Vie et de la Terre",
            "Technologie",
            "Français",
            "Anglais",
            "Arabe",
            "Éducation Islamique",
            "Histoire-Géographie"
        ],

        "Lettres et Sciences Humaines": [
            "Arabe",
            "Français",
            "Anglais",
            "Histoire-Géographie",
            "Éducation Islamique",
            "Philosophie",
            "Mathématiques"
        ],

        "Technologie": [
            "Mathématiques",
            "Physique-Chimie",
            "Sciences de l'Ingénieur",
            "Français",
            "Anglais",
            "Arabe",
            "Éducation Islamique",
            "Histoire-Géographie"
        ]
    },

    "1ère Bac": {

        "Sciences Mathématiques": [
            "Mathématiques",
            "Physique-Chimie",
            "Français",
            "Anglais",
            "Arabe",
            "Éducation Islamique",
            "Histoire-Géographie"
        ],

        "Sciences Expérimentales": [
            "Mathématiques",
            "Physique-Chimie",
            "Sciences de la Vie et de la Terre",
            "Français",
            "Anglais",
            "Arabe",
            "Éducation Islamique",
            "Histoire-Géographie"
        ],

        "STE": [
            "Mathématiques",
            "Physique-Chimie",
            "Sciences de l'Ingénieur",
            "Français",
            "Anglais",
            "Arabe",
            "Éducation Islamique",
            "Histoire-Géographie"
        ],

        "STM": [
            "Mathématiques",
            "Physique-Chimie",
            "Sciences de l'Ingénieur",
            "Français",
            "Anglais",
            "Arabe",
            "Éducation Islamique",
            "Histoire-Géographie"
        ],

        "Sciences Économiques": [
            "Mathématiques",
            "Économie Générale",
            "Comptabilité",
            "Français",
            "Anglais",
            "Arabe",
            "Histoire-Géographie",
            "Éducation Islamique"
        ],

        "Gestion": [
            "Mathématiques",
            "Économie Générale",
            "Comptabilité",
            "Organisation Administrative",
            "Français",
            "Anglais",
            "Arabe"
        ],

        "Lettres et Sciences Humaines": [
            "Arabe",
            "Français",
            "Anglais",
            "Histoire-Géographie",
            "Philosophie",
            "Éducation Islamique",
            "Mathématiques"
        ]
    },

    "2ème Bac": {

        "Sciences Mathématiques A": [
            "Mathématiques",
            "Physique-Chimie",
            "Sciences de l'Ingénieur",
            "Français",
            "Anglais",
            "Arabe",
            "Philosophie",
            "Éducation Islamique"
        ],

        "Sciences Mathématiques B": [
            "Mathématiques",
            "Physique-Chimie",
            "Sciences de l'Ingénieur",
            "Français",
            "Anglais",
            "Arabe",
            "Philosophie",
            "Éducation Islamique"
        ],

        "Sciences Physiques": [
            "Mathématiques",
            "Physique-Chimie",
            "Sciences de la Vie et de la Terre",
            "Français",
            "Anglais",
            "Arabe",
            "Philosophie",
            "Éducation Islamique"
        ],

        "Sciences de la Vie et de la Terre": [
            "Mathématiques",
            "Physique-Chimie",
            "Sciences de la Vie et de la Terre",
            "Français",
            "Anglais",
            "Arabe",
            "Philosophie",
            "Éducation Islamique"
        ],

        "STE": [
            "Mathématiques",
            "Physique-Chimie",
            "Sciences de l'Ingénieur",
            "Français",
            "Anglais",
            "Arabe",
            "Philosophie",
            "Éducation Islamique"
        ],

        "STM": [
            "Mathématiques",
            "Physique-Chimie",
            "Sciences de l'Ingénieur",
            "Français",
            "Anglais",
            "Arabe",
            "Philosophie",
            "Éducation Islamique"
        ],

        "Sciences Économiques": [
            "Mathématiques",
            "Économie",
            "Comptabilité",
            "Organisation",
            "Français",
            "Anglais",
            "Arabe",
            "Philosophie"
        ],

        "Sciences de Gestion": [
            "Mathématiques",
            "Économie",
            "Comptabilité",
            "Gestion",
            "Français",
            "Anglais",
            "Arabe",
            "Philosophie"
        ],

        "Lettres et Sciences Humaines": [
            "Arabe",
            "Français",
            "Anglais",
            "Histoire-Géographie",
            "Philosophie",
            "Éducation Islamique"
        ]
    }
}

# ============================================================
# INITIALISATION DES MATIERES
# ============================================================

for level, branches in PROGRAM.items():

    for branch, subjects in branches.items():

        for subject in subjects:
            add_subject(
                level,
                branch,
                subject
            )


# ============================================================
# OUTILS IA / PLANNING
# ============================================================

def get_course_level(score):
    """
    Transforme le score en niveau pédagogique.
    """

    if score is None:
        return "Non évalué"

    if score < 40:
        return "🔴 Très faible"

    elif score < 60:
        return "🟠 Faible"

    elif score < 75:
        return "🟡 Moyen"

    elif score < 90:
        return "🟢 Bon"

    else:
        return "⭐ Excellent"


def get_course_priority(score):
    """
    Plus le score est faible,
    plus la priorité de révision est importante.
    """

    if score is None:
        return 1.0

    if score < 40:
        return 4.0

    elif score < 60:
        return 3.0

    elif score < 75:
        return 2.0

    elif score < 90:
        return 1.3

    else:
        return 0.7


def get_student_courses(user_id, profile):
    """
    Récupère tous les cours de l'élève
    avec leurs résultats et leur priorité.
    """

    if not profile:
        return []

    level = profile[0]
    branch = profile[1]

    subjects = get_subjects(
        level,
        branch
    )

    courses_data = []

    for subject in subjects:

        subject_id = subject[0]
        subject_name = subject[1]

        courses = get_courses(
            subject_id
        )

        for course in courses:

            course_id = course[0]
            course_title = course[1]

            initial = get_latest_result(
                user_id,
                course_id,
                "initial"
            )

            final = get_latest_result(
                user_id,
                course_id,
                "final"
            )

            # --------------------------------------------
            # Choisir le meilleur résultat disponible
            # --------------------------------------------

            score = None

            if final:

                score = final[2]

            elif initial:

                score = initial[2]

            priority = get_course_priority(
                score
            )

            course_level = get_course_level(
                score
            )

            courses_data.append({

                "course_id": course_id,

                "subject_id": subject_id,

                "subject": subject_name,

                "course": course_title,

                "score": score,

                "level": course_level,

                "priority": priority
            })

    return courses_data


def distribute_time(total_minutes, courses):
    """
    Distribue le temps disponible entre les cours
    en fonction des difficultés.

    Les cours faibles reçoivent plus de temps.
    """

    if not courses:
        return []

    if total_minutes <= 0:
        return []

    # ----------------------------------------------------
    # Calcul du poids total
    # ----------------------------------------------------

    total_priority = sum(
        course["priority"]
        for course in courses
    )

    if total_priority <= 0:
        return []

    allocations = []

    for course in courses:
        raw_minutes = (
                total_minutes
                * course["priority"]
                / total_priority
        )

        minutes = int(
            round(raw_minutes / 5) * 5
        )

        allocations.append({
            **course,
            "minutes": minutes
        })

    # ----------------------------------------------------
    # Corriger la différence d'arrondi
    # ----------------------------------------------------

    current_total = sum(
        x["minutes"]
        for x in allocations
    )

    difference = (
            total_minutes
            - current_total
    )

    index = 0

    while difference != 0 and allocations:

        if difference > 0:

            allocations[index]["minutes"] += 5

            difference -= 5

        else:

            if allocations[index]["minutes"] >= 10:
                allocations[index]["minutes"] -= 5

                difference += 5

        index += 1

        if index >= len(allocations):
            index = 0

    # ----------------------------------------------------
    # Supprimer les créneaux trop petits
    # ----------------------------------------------------

    allocations = [
        x for x in allocations
        if x["minutes"] >= 5
    ]

    return allocations


def format_time(minutes):
    """
    Transforme les minutes depuis minuit en HH:MM.
    """

    hours = minutes // 60
    mins = minutes % 60

    return f"{hours:02d}:{mins:02d}"


def generate_daily_plan(
        user_id,
        day,
        start,
        end,
        courses
):
    """
    Génère le planning d'une journée.

    Exemple :

    14:00 - 14:45 Mathématiques - Limites
    14:45 - 15:15 Physique - Électricité
    15:15 - 16:00 Chimie - Acides/Bases
    """

    start_min = (
            start.hour * 60
            + start.minute
    )

    end_min = (
            end.hour * 60
            + end.minute
    )

    available_minutes = (
            end_min - start_min
    )

    if available_minutes <= 0:
        return []

    allocations = distribute_time(
        available_minutes,
        courses
    )

    created = []

    current_minute = start_min

    for item in allocations:

        minutes = item["minutes"]

        if minutes <= 0:
            continue

        next_minute = (
                current_minute
                + minutes
        )

        if next_minute > end_min:
            next_minute = end_min

        title = (
            f"📚 {item['subject']} — "
            f"{item['course']}"
        )

        add_planning(
            user_id,
            item["course_id"],
            day,
            format_time(current_minute),
            format_time(next_minute),
            title,
            "revision"
        )

        created.append({

            "day": day,

            "start": format_time(
                current_minute
            ),

            "end": format_time(
                next_minute
            ),

            "subject": item["subject"],

            "course": item["course"],

            "score": item["score"],

            "level": item["level"],

            "minutes": minutes
        })

        current_minute = next_minute

        if current_minute >= end_min:
            break

    return created


# ============================================================
# SESSION
# ============================================================

if "user" not in st.session_state:
    st.session_state.user = None

if "ai_messages" not in st.session_state:
    st.session_state.ai_messages = []

# ============================================================
# LOGIN
# ============================================================

if st.session_state.user is None:

    st.title(
        "🎓 9rayti Dkia"
    )

    st.subheader(
        "Plateforme intelligente d'apprentissage"
    )

    login_tab, register_tab = st.tabs([
        "🔐 Connexion",
        "📝 Créer un compte étudiant"
    ])

    # --------------------------------------------------------
    # CONNEXION
    # --------------------------------------------------------

    with login_tab:

        email = st.text_input(
            "Email",
            key="login_email"
        )

        password = st.text_input(
            "Mot de passe",
            type="password",
            key="login_password"
        )

        if st.button(
                "Se connecter",
                type="primary"
        ):

            user = login_user(
                email,
                password
            )

            if user:

                st.session_state.user = user

                st.rerun()

            else:

                st.error(
                    "❌ Email ou mot de passe incorrect."
                )

    # --------------------------------------------------------
    # INSCRIPTION
    # --------------------------------------------------------

    with register_tab:

        st.info(
            "Ce formulaire crée uniquement un compte étudiant."
        )

        name = st.text_input(
            "Nom et prénom",
            key="register_name"
        )

        email = st.text_input(
            "Email",
            key="register_email"
        )

        password = st.text_input(
            "Mot de passe",
            type="password",
            key="register_password"
        )

        confirm = st.text_input(
            "Confirmer le mot de passe",
            type="password",
            key="register_confirm"
        )

        if st.button(
                "Créer mon compte",
                type="primary"
        ):

            if not name or not email or not password:

                st.warning(
                    "Veuillez remplir tous les champs."
                )

            elif password != confirm:

                st.error(
                    "Les mots de passe ne correspondent pas."
                )

            else:

                user_id = create_user(
                    name,
                    email,
                    password
                )

                if user_id:

                    st.success(
                        "✅ Compte étudiant créé."
                    )

                    st.info(
                        "Vous pouvez maintenant vous connecter."
                    )

                else:

                    st.error(
                        "❌ Cet email est déjà utilisé."
                    )

    st.stop()

# ============================================================
# UTILISATEUR CONNECTE
# ============================================================

user_id = st.session_state.user[0]

user_name = st.session_state.user[1]

user_email = st.session_state.user[2]

user_role = st.session_state.user[3]

# ============================================================
# ADMIN
# ============================================================

if user_role == "admin":

    st.sidebar.title(
        "🔐 Administration"
    )

    st.sidebar.success(
        "Administrateur"
    )

    st.sidebar.write(
        user_email
    )

    admin_menu = st.sidebar.radio(
        "Administration",
        [
            "🏠 Tableau de bord",
            "📚 Gérer les matières",
            "📄 Gérer les cours",
            "📝 Gérer les tests"
        ]
    )

    st.sidebar.divider()

    if st.sidebar.button(
            "🚪 Déconnexion"
    ):
        st.session_state.user = None

        st.rerun()

    # --------------------------------------------------------
    # DASHBOARD ADMIN
    # --------------------------------------------------------

    if admin_menu == "🏠 Tableau de bord":

        st.title(
            "🔐 Administration 9rayti Dkia"
        )

        st.success(
            "Vous êtes connecté en tant qu'administrateur."
        )

        st.info(
            """
            Depuis cet espace vous pouvez gérer :

            • les matières
            • les cours PDF
            • les questions
            • les tests
            """
        )

    # --------------------------------------------------------
    # MATIERES
    # --------------------------------------------------------

    elif admin_menu == "📚 Gérer les matières":

        st.title(
            "📚 Gestion des matières"
        )

        level = st.selectbox(
            "Niveau",
            list(PROGRAM.keys())
        )

        branch = st.selectbox(
            "Branche",
            list(PROGRAM[level].keys())
        )

        subjects = get_subjects(
            level,
            branch
        )

        for subject in subjects:

            col1, col2 = st.columns([5, 1])

            with col1:

                st.write(
                    f"📚 {subject[1]}"
                )

            with col2:

                if st.button(
                        "🗑️",
                        key=f"delete_subject_{subject[0]}"
                ):
                    delete_subject(
                        subject[0]
                    )

                    st.rerun()

        st.divider()

        st.subheader(
            "➕ Ajouter une matière"
        )

        new_subject = st.text_input(
            "Nom de la matière"
        )

        if st.button(
                "Ajouter"
        ):

            if new_subject:
                add_subject(
                    level,
                    branch,
                    new_subject
                )

                st.success(
                    "Matière ajoutée."
                )

                st.rerun()

    # --------------------------------------------------------
    # COURS ADMIN
    # --------------------------------------------------------

    elif admin_menu == "📄 Gérer les cours":

        st.title(
            "📄 Gestion des cours"
        )

        level = st.selectbox(
            "Niveau",
            list(PROGRAM.keys()),
            key="admin_course_level"
        )

        branch = st.selectbox(
            "Branche",
            list(PROGRAM[level].keys()),
            key="admin_course_branch"
        )

        subjects = get_subjects(
            level,
            branch
        )

        subject_dict = {
            s[1]: s[0]
            for s in subjects
        }

        if subject_dict:

            selected_subject = st.selectbox(
                "Matière",
                list(subject_dict.keys())
            )

            subject_id = subject_dict[
                selected_subject
            ]

            st.divider()

            st.subheader(
                "➕ Ajouter un cours"
            )

            title = st.text_input(
                "Nom du cours"
            )

            pdf = st.file_uploader(
                "PDF du cours",
                type=["pdf"]
            )

            if st.button(
                    "📥 Ajouter le cours",
                    type="primary"
            ):

                if not title:

                    st.warning(
                        "Entrez le nom du cours."
                    )

                elif pdf is None:

                    st.warning(
                        "Sélectionnez un PDF."
                    )

                else:

                    folder = os.path.join(
                        "courses",
                        level.replace(" ", "_"),
                        branch.replace(" ", "_"),
                        selected_subject.replace(" ", "_")
                    )

                    os.makedirs(
                        folder,
                        exist_ok=True
                    )

                    file_path = os.path.join(
                        folder,
                        pdf.name
                    )

                    with open(
                            file_path,
                            "wb"
                    ) as f:

                        f.write(
                            pdf.getbuffer()
                        )

                    add_course(
                        subject_id,
                        title,
                        file_path
                    )

                    st.success(
                        "✅ Cours ajouté."
                    )

                    st.rerun()

            st.divider()

            st.subheader(
                "📚 Cours existants"
            )

            courses = get_courses(
                subject_id
            )

            for course in courses:

                col1, col2 = st.columns([5, 1])

                with col1:

                    st.write(
                        f"📄 {course[1]}"
                    )

                    st.caption(
                        course[2]
                    )

                with col2:

                    if st.button(
                            "🗑️",
                            key=f"delete_course_{course[0]}"
                    ):

                        delete_course(
                            course[0]
                        )

                        if os.path.exists(
                                course[2]
                        ):
                            os.remove(
                                course[2]
                            )

                        st.rerun()

        else:

            st.warning(
                "Aucune matière."
            )

    # --------------------------------------------------------
    # TESTS ADMIN
    # --------------------------------------------------------

    elif admin_menu == "📝 Gérer les tests":

        st.title(
            "📝 Gestion des tests"
        )

        level = st.selectbox(
            "Niveau",
            list(PROGRAM.keys()),
            key="test_level"
        )

        branch = st.selectbox(
            "Branche",
            list(PROGRAM[level].keys()),
            key="test_branch"
        )

        subjects = get_subjects(
            level,
            branch
        )

        subject_dict = {
            s[1]: s[0]
            for s in subjects
        }

        if subject_dict:

            selected_subject = st.selectbox(
                "Matière",
                list(subject_dict.keys()),
                key="test_subject"
            )

            subject_id = subject_dict[
                selected_subject
            ]

            courses = get_courses(
                subject_id
            )

            course_dict = {
                c[1]: c[0]
                for c in courses
            }

            if course_dict:

                selected_course = st.selectbox(
                    "Cours",
                    list(course_dict.keys()),
                    key="test_course"
                )

                course_id = course_dict[
                    selected_course
                ]

                test_type = st.selectbox(
                    "Type de test",
                    [
                        "initial",
                        "final"
                    ]
                )

                st.divider()

                st.subheader(
                    "➕ Ajouter une question"
                )

                question = st.text_area(
                    "Question"
                )

                answer_a = st.text_input(
                    "Réponse A"
                )

                answer_b = st.text_input(
                    "Réponse B"
                )

                answer_c = st.text_input(
                    "Réponse C"
                )

                correct = st.selectbox(
                    "Bonne réponse",
                    ["A", "B", "C"]
                )

                if st.button(
                        "➕ Ajouter la question"
                ):

                    if (
                            question
                            and answer_a
                            and answer_b
                            and answer_c
                    ):
                        question_id = add_question(
                            course_id,
                            question,
                            test_type
                        )

                        add_answer(
                            question_id,
                            answer_a,
                            1 if correct == "A" else 0
                        )

                        add_answer(
                            question_id,
                            answer_b,
                            1 if correct == "B" else 0
                        )

                        add_answer(
                            question_id,
                            answer_c,
                            1 if correct == "C" else 0
                        )

                        st.success(
                            "Question ajoutée."
                        )

                        st.rerun()

                st.divider()

                st.subheader(
                    "Questions existantes"
                )

                questions = get_questions(
                    course_id,
                    test_type
                )

                for q in questions:

                    st.write(
                        f"❓ {q[1]}"
                    )

                    if st.button(
                            "🗑️ Supprimer",
                            key=f"delete_question_{q[0]}"
                    ):
                        delete_question(
                            q[0]
                        )

                        st.rerun()

            else:

                st.warning(
                    "Aucun cours disponible."
                )

        else:

            st.warning(
                "Aucune matière disponible."
            )

    st.stop()

# ============================================================
# ESPACE ETUDIANT
# ============================================================

st.sidebar.title(
    "🎓 9rayti Dkia"
)

st.sidebar.write(
    f"👤 {user_name}"
)

st.sidebar.write(
    user_email
)

menu = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Accueil",
        "👤 Mon profil",
        "📚 Mes matières",
        "📄 Mes cours",
        "📝 Test initial",
        "📊 Analyse IA",
        "📅 Planning",
        "🏁 Test final",
        "📊 Mes résultats",
        "🤖 Assistant IA"
    ]
)

st.sidebar.divider()

if st.sidebar.button(
        "🚪 Déconnexion"
):
    st.session_state.user = None

    st.session_state.ai_messages = []

    st.rerun()

# ============================================================
# ACCUEIL
# ============================================================

if menu == "🏠 Accueil":

    st.title(
        f"👋 Bonjour {user_name}"
    )

    st.write(
        "Bienvenue sur 9rayti Dkia."
    )

    st.info(
        """
        Votre espace vous permet de :

        📚 consulter vos cours

        📝 faire des tests

        🧠 analyser votre niveau

        📊 suivre votre progression

        📅 obtenir un planning personnalisé

        🤖 discuter avec l'assistant IA
        """
    )


# ============================================================
# PROFIL
# ============================================================

elif menu == "👤 Mon profil":

    st.header(
        "👤 Mon profil"
    )

    profile = get_profile(
        user_id
    )

    if profile:
        st.success(
            "Profil enregistré"
        )

        st.write(
            f"🎓 Niveau : **{profile[0]}**"
        )

        st.write(
            f"🏫 Branche : **{profile[1]}**"
        )

    st.divider()

    level = st.selectbox(
        "Niveau",
        list(PROGRAM.keys()),
        key="profile_level"
    )

    branch = st.selectbox(
        "Branche",
        list(PROGRAM[level].keys()),
        key="profile_branch"
    )

    if st.button(
            "💾 Enregistrer le profil"
    ):
        save_profile(
            user_id,
            level,
            branch
        )

        st.success(
            "Profil enregistré."
        )

        st.rerun()


# ============================================================
# MATIERES
# ============================================================

elif menu == "📚 Mes matières":

    st.header(
        "📚 Mes matières"
    )

    profile = get_profile(
        user_id
    )

    if not profile:

        st.warning(
            "Créez votre profil."
        )

    else:

        subjects = get_subjects(
            profile[0],
            profile[1]
        )

        for subject in subjects:
            st.info(
                f"📚 {subject[1]}"
            )


# ============================================================
# COURS
# ============================================================

elif menu == "📄 Mes cours":

    st.header(
        "📄 Mes cours"
    )

    profile = get_profile(
        user_id
    )

    if not profile:

        st.warning(
            "Créez d'abord votre profil."
        )

    else:

        subjects = get_subjects(
            profile[0],
            profile[1]
        )

        subject_dict = {
            s[1]: s[0]
            for s in subjects
        }

        if subject_dict:

            selected_subject = st.selectbox(
                "Matière",
                list(subject_dict.keys()),
                key="courses_subject"
            )

            subject_id = subject_dict[
                selected_subject
            ]

            courses = get_courses(
                subject_id
            )

            if not courses:

                st.info(
                    "Aucun cours disponible."
                )

            else:

                for course in courses:

                    course_id = course[0]

                    title = course[1]

                    pdf_path = course[2]

                    st.subheader(
                        f"📘 {title}"
                    )

                    if os.path.exists(
                            pdf_path
                    ):

                        with open(
                                pdf_path,
                                "rb"
                        ) as f:

                            pdf_bytes = f.read()

                        st.download_button(
                            "📥 Télécharger",
                            pdf_bytes,
                            file_name=os.path.basename(
                                pdf_path
                            ),
                            mime="application/pdf",
                            key=f"download_{course_id}"
                        )

                        encoded = base64.b64encode(
                            pdf_bytes
                        ).decode()

                        viewer = f"""
                        <iframe
                            src="data:application/pdf;base64,{encoded}"
                            width="100%"
                            height="600">
                        </iframe>
                        """

                        st.markdown(
                            viewer,
                            unsafe_allow_html=True
                        )

                        if st.button(
                                "✅ J'ai terminé ce cours",
                                key=f"complete_{course_id}"
                        ):
                            complete_course(
                                user_id,
                                course_id
                            )

                            st.success(
                                "Cours terminé."
                            )

                    else:

                        st.error(
                            "PDF introuvable."
                        )


# ============================================================
# TEST INITIAL
# ============================================================

elif menu == "📝 Test initial":

    st.header(
        "📝 Test initial"
    )

    profile = get_profile(
        user_id
    )

    if not profile:

        st.warning(
            "Créez votre profil."
        )

    else:

        subjects = get_subjects(
            profile[0],
            profile[1]
        )

        subject_dict = {
            s[1]: s[0]
            for s in subjects
        }

        if subject_dict:

            selected_subject = st.selectbox(
                "Matière",
                list(subject_dict.keys()),
                key="initial_subject"
            )

            subject_id = subject_dict[
                selected_subject
            ]

            courses = get_courses(
                subject_id
            )

            course_dict = {
                c[1]: c[0]
                for c in courses
            }

            if course_dict:

                selected_course = st.selectbox(
                    "Cours",
                    list(course_dict.keys()),
                    key="initial_course"
                )

                course_id = course_dict[
                    selected_course
                ]

                questions = get_questions(
                    course_id,
                    "initial"
                )

                if not questions:

                    st.warning(
                        "Le test initial n'est pas encore disponible."
                    )

                elif has_test_result(
                        user_id,
                        course_id,
                        "initial"
                ):

                    result = get_latest_result(
                        user_id,
                        course_id,
                        "initial"
                    )

                    st.success(
                        f"Vous avez déjà obtenu {result[2]}%."
                    )

                else:

                    answers_user = {}

                    for q in questions:
                        answers = get_answers(
                            q[0]
                        )

                        choices = [
                            a[1]
                            for a in answers
                        ]

                        answers_user[
                            q[0]
                        ] = st.radio(
                            q[1],
                            choices,
                            key=f"initial_{q[0]}"
                        )

                    if st.button(
                            "🏁 Terminer",
                            key="finish_initial"
                    ):

                        score = 0

                        for q_id, answer in answers_user.items():

                            for a in get_answers(q_id):

                                if (
                                        a[1] == answer
                                        and a[2] == 1
                                ):
                                    score += 1

                        total = len(questions)

                        percentage = round(
                            score / total * 100
                        )

                        save_result(
                            user_id,
                            course_id,
                            "initial",
                            score,
                            total,
                            percentage
                        )

                        st.success(
                            f"🎯 Score : {percentage}%"
                        )

                        st.info(
                            f"""
                            Niveau détecté :

                            **{get_course_level(percentage)}**

                            Ce résultat sera utilisé automatiquement
                            pour construire votre planning.
                            """
                        )


# ============================================================
# ANALYSE IA
# ============================================================

elif menu == "📊 Analyse IA":

    st.header(
        "🧠 Analyse personnalisée de ton niveau"
    )

    profile = get_profile(
        user_id
    )

    if not profile:

        st.warning(
            "Crée d'abord ton profil."
        )

    else:

        courses_data = get_student_courses(
            user_id,
            profile
        )

        if not courses_data:

            st.info(
                "Aucun cours disponible pour ton profil."
            )

        else:

            st.subheader(
                "📊 Niveau par cours"
            )

            for item in courses_data:

                score = item["score"]

                if score is None:

                    st.info(
                        f"""
                        📚 **{item['subject']} — {item['course']}**

                        ⚪ Test non effectué.

                        Passe le test initial pour que l'IA
                        puisse déterminer ton niveau.
                        """
                    )

                else:

                    if score < 60:

                        st.error(
                            f"""
                            🔴 **{item['subject']} — {item['course']}**

                            Score : **{score}%**

                            Niveau : **{item['level']}**

                            👉 Ce cours est prioritaire.
                            Il recevra plus de temps dans ton planning.
                            """
                        )

                    elif score < 75:

                        st.warning(
                            f"""
                            🟡 **{item['subject']} — {item['course']}**

                            Score : **{score}%**

                            Niveau : **{item['level']}**

                            👉 Révision régulière recommandée.
                            """
                        )

                    elif score < 90:

                        st.success(
                            f"""
                            🟢 **{item['subject']} — {item['course']}**

                            Score : **{score}%**

                            Niveau : **{item['level']}**

                            👉 Niveau satisfaisant.
                            """
                        )

                    else:

                        st.success(
                            f"""
                            ⭐ **{item['subject']} — {item['course']}**

                            Score : **{score}%**

                            Niveau : **{item['level']}**

                            👉 Cours bien maîtrisé.
                            """
                        )

            st.divider()

            st.subheader(
                "🎯 Priorités de révision"
            )

            priority_courses = sorted(
                [
                    x for x in courses_data
                    if x["score"] is not None
                ],
                key=lambda x: x["priority"],
                reverse=True
            )

            if priority_courses:

                for index, item in enumerate(
                        priority_courses,
                        start=1
                ):

                    score = item["score"]

                    if score < 60:

                        emoji = "🔴"

                    elif score < 75:

                        emoji = "🟡"

                    else:

                        emoji = "🟢"

                    st.write(
                        f"""
                        **{index}. {emoji} "
                        f"{item['subject']} — {item['course']} "
                        f"({score}%)**
                        """
                    )


# ============================================================
# PLANNING INTELLIGENT
# ============================================================

elif menu == "📅 Planning":

    st.header(
        "📅 Mon planning intelligent"
    )

    st.write(
        """
        🤖 Le planning analyse automatiquement tes résultats
        et répartit ton temps entre tes cours.

        🔴 Les cours faibles reçoivent plus de temps.

        🟡 Les cours moyens reçoivent un temps intermédiaire.

        🟢 Les cours maîtrisés reçoivent moins de temps.
        """
    )

    profile = get_profile(
        user_id
    )

    if not profile:

        st.warning(
            "⚠️ Crée d'abord ton profil."
        )

    else:

        courses_data = get_student_courses(
            user_id,
            profile
        )

        if not courses_data:

            st.warning(
                "⚠️ Aucun cours disponible."
            )

        else:

            # ------------------------------------------------
            # AFFICHER LES NIVEAUX
            # ------------------------------------------------

            st.subheader(
                "🧠 Ton niveau actuel"
            )

            evaluated_courses = [
                x for x in courses_data
                if x["score"] is not None
            ]

            if evaluated_courses:

                for item in sorted(
                        evaluated_courses,
                        key=lambda x: x["priority"],
                        reverse=True
                ):

                    score = item["score"]

                    if score < 60:

                        color = "🔴"

                    elif score < 75:

                        color = "🟡"

                    else:

                        color = "🟢"

                    st.write(
                        f"""
                        {color} **{item['subject']} — {item['course']}**
                        → {score}% → {item['level']}
                        """
                    )

            else:

                st.info(
                    """
                    Aucun test initial n'a encore été effectué.

                    Le planning sera provisoire et répartira
                    le temps entre les cours disponibles.

                    Après les tests, le planning deviendra
                    automatiquement personnalisé.
                    """
                )

            st.divider()

            # ------------------------------------------------
            # DISPONIBILITES
            # ------------------------------------------------

            st.subheader(
                "⏰ Mes disponibilités"
            )

            days = [
                "Lundi",
                "Mardi",
                "Mercredi",
                "Jeudi",
                "Vendredi",
                "Samedi",
                "Dimanche"
            ]

            slots = []

            for day in days:

                with st.expander(
                        f"📅 {day}"
                ):

                    available = st.checkbox(
                        f"Je suis disponible le {day}",
                        key=f"avail_{day}"
                    )

                    if available:

                        c1, c2 = st.columns(2)

                        with c1:

                            start = st.time_input(
                                "Début",
                                time(14, 0),
                                key=f"s_{day}"
                            )

                        with c2:

                            end = st.time_input(
                                "Fin",
                                time(18, 0),
                                key=f"e_{day}"
                            )

                        if start < end:
                            total_day = (
                                    end.hour * 60
                                    + end.minute
                                    - (
                                            start.hour * 60
                                            + start.minute
                                    )
                            )

                            st.info(
                                f"⏱️ Temps disponible : "
                                f"**{total_day} minutes**"
                            )

                            slots.append(
                                (
                                    day,
                                    start,
                                    end
                                )
                            )

            st.divider()

            # ------------------------------------------------
            # GENERATION
            # ------------------------------------------------

            if st.button(
                    "🤖 Générer mon planning personnalisé",
                    type="primary",
                    use_container_width=True
            ):

                if not slots:

                    st.warning(
                        """
                        ⚠️ Sélectionne au moins un jour
                        et indique tes horaires.
                        """
                    )

                else:

                    # Supprimer ancien planning
                    delete_availability(
                        user_id
                    )

                    delete_planning(
                        user_id
                    )

                    generated_plan = []

                    for day, start, end in slots:
                        # Sauvegarde disponibilité

                        add_availability(
                            user_id,
                            day,
                            start.strftime("%H:%M"),
                            end.strftime("%H:%M")
                        )

                        # ------------------------------------
                        # Générer le planning de cette journée
                        # ------------------------------------

                        daily_plan = generate_daily_plan(
                            user_id,
                            day,
                            start,
                            end,
                            courses_data
                        )

                        generated_plan.extend(
                            daily_plan
                        )

                    st.success(
                        "🎉 Ton planning personnalisé a été généré !"
                    )

                    st.session_state[
                        "planning_generated"
                    ] = True

            # ------------------------------------------------
            # AFFICHAGE PLANNING
            # ------------------------------------------------

            st.divider()

            st.subheader(
                "📚 Mon planning par cours"
            )

            planning = get_planning(
                user_id
            )

            revision_items = [
                item for item in planning
                if len(item) > 4
                   and item[4] == "revision"
            ]

            if not revision_items:

                st.info(
                    """
                    Aucun planning généré.

                    Sélectionne tes disponibilités puis clique sur :

                    **🤖 Générer mon planning personnalisé**
                    """
                )

            else:

                # --------------------------------------------
                # Organiser par jour
                # --------------------------------------------

                day_order = {
                    "Lundi": 1,
                    "Mardi": 2,
                    "Mercredi": 3,
                    "Jeudi": 4,
                    "Vendredi": 5,
                    "Samedi": 6,
                    "Dimanche": 7
                }

                grouped = {}

                for item in revision_items:

                    day = item[0]

                    if day not in grouped:
                        grouped[day] = []

                    grouped[day].append(
                        item
                    )

                for day in sorted(
                        grouped.keys(),
                        key=lambda x: day_order.get(
                            x,
                            99
                        )
                ):

                    st.markdown(
                        f"## 📅 {day}"
                    )

                    for item in grouped[day]:
                        start_time = item[1]

                        end_time = item[2]

                        title = item[3]

                        st.success(
                            f"""
                            ⏰ **{start_time} → {end_time}**

                            {title}
                            """
                        )


# ============================================================
# TEST FINAL
# ============================================================

elif menu == "🏁 Test final":

    st.header(
        "🏁 Test final"
    )

    profile = get_profile(
        user_id
    )

    if profile:

        subjects = get_subjects(
            profile[0],
            profile[1]
        )

        subject_dict = {
            s[1]: s[0]
            for s in subjects
        }

        if subject_dict:

            selected_subject = st.selectbox(
                "Matière",
                list(subject_dict.keys()),
                key="final_subject"
            )

            subject_id = subject_dict[
                selected_subject
            ]

            courses = get_courses(
                subject_id
            )

            course_dict = {
                c[1]: c[0]
                for c in courses
            }

            if course_dict:

                selected_course = st.selectbox(
                    "Cours",
                    list(course_dict.keys()),
                    key="final_course"
                )

                course_id = course_dict[
                    selected_course
                ]

                if not has_test_result(
                        user_id,
                        course_id,
                        "initial"
                ):

                    st.warning(
                        "⚠️ Faites d'abord le test initial."
                    )

                elif not is_course_completed(
                        user_id,
                        course_id
                ):

                    st.warning(
                        "⚠️ Terminez d'abord le cours."
                    )

                else:

                    questions = get_questions(
                        course_id,
                        "final"
                    )

                    if not questions:

                        st.warning(
                            "Le test final n'est pas encore disponible."
                        )

                    elif has_test_result(
                            user_id,
                            course_id,
                            "final"
                    ):

                        result = get_latest_result(
                            user_id,
                            course_id,
                            "final"
                        )

                        st.success(
                            f"🎯 Score final : {result[2]}%"
                        )

                    else:

                        answers_user = {}

                        for q in questions:
                            answers = get_answers(
                                q[0]
                            )

                            choices = [
                                a[1]
                                for a in answers
                            ]

                            answers_user[
                                q[0]
                            ] = st.radio(
                                q[1],
                                choices,
                                key=f"final_{q[0]}"
                            )

                        if st.button(
                                "🏁 Terminer le test final",
                                key="finish_final"
                        ):

                            score = 0

                            for q_id, answer in answers_user.items():

                                for a in get_answers(q_id):

                                    if (
                                            a[1] == answer
                                            and a[2] == 1
                                    ):
                                        score += 1

                            total = len(questions)

                            percentage = round(
                                score / total * 100
                            )

                            save_result(
                                user_id,
                                course_id,
                                "final",
                                score,
                                total,
                                percentage
                            )

                            st.success(
                                f"🎉 Score final : {percentage}%"
                            )


# ============================================================
# RESULTATS
# ============================================================

elif menu == "📊 Mes résultats":

    st.header(
        "📊 Mes résultats"
    )

    profile = get_profile(
        user_id
    )

    if profile:

        subjects = get_subjects(
            profile[0],
            profile[1]
        )

        subject_dict = {
            s[1]: s[0]
            for s in subjects
        }

        if subject_dict:

            selected_subject = st.selectbox(
                "Matière",
                list(subject_dict.keys()),
                key="results_subject"
            )

            subject_id = subject_dict[
                selected_subject
            ]

            courses = get_courses(
                subject_id
            )

            course_dict = {
                c[1]: c[0]
                for c in courses
            }

            if course_dict:

                selected_course = st.selectbox(
                    "Cours",
                    list(course_dict.keys()),
                    key="results_course"
                )

                course_id = course_dict[
                    selected_course
                ]

                initial = get_latest_result(
                    user_id,
                    course_id,
                    "initial"
                )

                final = get_latest_result(
                    user_id,
                    course_id,
                    "final"
                )

                c1, c2, c3 = st.columns(3)

                with c1:

                    st.metric(
                        "Test initial",
                        f"{initial[2]}%" if initial else "-"
                    )

                with c2:

                    st.metric(
                        "Test final",
                        f"{final[2]}%" if final else "-"
                    )

                with c3:

                    if initial and final:

                        progression = (
                                final[2]
                                - initial[2]
                        )

                        st.metric(
                            "Progression",
                            f"{progression:+.0f}%"
                        )

                    else:

                        st.metric(
                            "Progression",
                            "-"
                        )

            else:

                st.info(
                    "Aucun cours disponible."
                )

        else:

            st.info(
                "Aucune matière disponible."
            )

    else:

        st.warning(
            "Créez d'abord votre profil."
        )


# ============================================================
# ASSISTANT IA
# ============================================================

elif menu == "🤖 Assistant IA":

    st.header(
        "🤖 Assistant IA"
    )

    st.subheader(
        "Bienvenue sur l'assistant de 9rayti Dkia"
    )

    st.write(
        """
        Pose une question sur tes études,
        demande une explication,
        un exemple ou un exercice.
        """
    )

    profile = get_profile(
        user_id
    )

    if not profile:

        st.warning(
            "⚠️ Crée d'abord ton profil."
        )

    else:

        st.info(
            f"""
            🎓 Niveau : **{profile[0]}**

            🏫 Branche : **{profile[1]}**
            """
        )

        for message in st.session_state.ai_messages:
            with st.chat_message(
                    message["role"]
            ):
                st.markdown(
                    message["content"]
                )

        question = st.chat_input(
            "Pose ta question à 9rayti Dkia..."
        )

        if question:
            st.session_state.ai_messages.append(
                {
                    "role": "user",
                    "content": question
                }
            )

            with st.chat_message(
                    "user"
            ):
                st.markdown(
                    question
                )

            with st.chat_message(
                    "assistant"
            ):
                with st.spinner(
                        "🤖 9rayti Dkia réfléchit..."
                ):
                    answer = ask_ai(
                        question,
                        user_name,
                        profile
                    )

                st.markdown(
                    answer
                )

            st.session_state.ai_messages.append(
                {
                    "role": "assistant",
                    "content": answer
                }
            )

        if st.session_state.ai_messages:

            st.divider()

            if st.button(
                    "🗑️ Nouvelle conversation"
            ):
                st.session_state.ai_messages = []

                st.rerun()