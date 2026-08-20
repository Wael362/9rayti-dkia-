import os
import base64
from datetime import time

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
    page_title="SmartStudy",
    page_icon="🎓",
    layout="wide"
)

create_database()


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
# INITIALISATION
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
# SESSION
# ============================================================

if "user" not in st.session_state:
    st.session_state.user = None


# ============================================================
# PAGE LOGIN
# ============================================================

if st.session_state.user is None:

    st.title("🎓 SmartStudy")

    st.subheader(
        "Plateforme intelligente d'apprentissage"
    )

    login_tab, register_tab = st.tabs([
        "🔐 Connexion",
        "📝 Créer un compte étudiant"
    ])

    # ========================================================
    # LOGIN
    # ========================================================

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

    # ========================================================
    # REGISTER
    # ========================================================

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
# UTILISATEUR CONNECTÉ
# ============================================================

user_id = st.session_state.user[0]
user_name = st.session_state.user[1]
user_email = st.session_state.user[2]
user_role = st.session_state.user[3]


# ============================================================
# ADMIN
# ============================================================

if user_role == "admin":

    st.sidebar.title("🔐 Administration")

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

    # ========================================================
    # ADMIN DASHBOARD
    # ========================================================

    if admin_menu == "🏠 Tableau de bord":

        st.title(
            "🔐 Administration SmartStudy"
        )

        st.success(
            "Vous êtes connecté en tant qu'administrateur."
        )

        st.info(
            """
            Vous êtes le seul administrateur.

            Depuis cet espace vous pouvez gérer :
            • les matières
            • les cours PDF
            • les questions
            • les tests
            """
        )

    # ========================================================
    # GERER MATIERES
    # ========================================================

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

        st.subheader(
            f"{level} → {branch}"
        )

        subjects = get_subjects(
            level,
            branch
        )

        for subject in subjects:

            col1, col2 = st.columns([
                5,
                1
            ])

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

    # ========================================================
    # GERER COURS
    # ========================================================

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

        if not subject_dict:

            st.warning(
                "Aucune matière."
            )

        else:

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

                col1, col2 = st.columns([
                    5,
                    1
                ])

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

    # ========================================================
    # GERER TESTS
    # ========================================================

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
                    [
                        "A",
                        "B",
                        "C"
                    ]
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

    st.stop()


# ============================================================
# ESPACE ETUDIANT
# ============================================================

st.sidebar.title(
    "🎓 SmartStudy"
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
        "📅 Planning",
        "🏁 Test final",
        "📊 Mes résultats"
    ]
)

st.sidebar.divider()

if st.sidebar.button(
    "🚪 Déconnexion"
):

    st.session_state.user = None

    st.rerun()


# ============================================================
# ACCUEIL ETUDIANT
# ============================================================

if menu == "🏠 Accueil":

    st.title(
        f"👋 Bonjour {user_name}"
    )

    st.write(
        "Bienvenue sur SmartStudy."
    )

    st.info(
        """
        Votre espace vous permet de consulter les cours,
        faire les tests, organiser votre temps et suivre
        votre progression.
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
        list(PROGRAM.keys())
    )

    branch = st.selectbox(
        "Branche",
        list(PROGRAM[level].keys())
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
                list(subject_dict.keys())
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

        selected_subject = st.selectbox(
            "Matière",
            list(subject_dict.keys())
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
                list(course_dict.keys())
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

                for i, q in enumerate(
                    questions
                ):

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
                    "🏁 Terminer"
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


# ============================================================
# PLANNING
# ============================================================

elif menu == "📅 Planning":

    st.header(
        "📅 Mon planning"
    )

    st.write(
        """
        Vous indiquez seulement vos disponibilités.
        L'application réserve automatiquement une partie
        du temps pour la révision.
        """
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

        with st.expander(day):

            available = st.checkbox(
                f"Disponible {day}",
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

                    slots.append(
                        (
                            day,
                            start,
                            end
                        )
                    )

    if st.button(
        "🧠 Générer mon planning",
        type="primary"
    ):

        delete_availability(
            user_id
        )

        delete_planning(
            user_id
        )

        for day, start, end in slots:

            start_min = (
                start.hour * 60
                + start.minute
            )

            end_min = (
                end.hour * 60
                + end.minute
            )

            available_min = (
                end_min - start_min
            )

            # 1 heure maximum de révision
            revision = min(
                60,
                available_min
            )

            revision_end = (
                start_min
                + revision
            )

            add_availability(
                user_id,
                day,
                start.strftime("%H:%M"),
                end.strftime("%H:%M")
            )

            add_planning(
                user_id,
                None,
                day,
                f"{start_min // 60:02d}:{start_min % 60:02d}",
                f"{revision_end // 60:02d}:{revision_end % 60:02d}",
                "📚 Révision",
                "revision"
            )

            if revision_end < end_min:

                add_planning(
                    user_id,
                    None,
                    day,
                    f"{revision_end // 60:02d}:{revision_end % 60:02d}",
                    f"{end_min // 60:02d}:{end_min % 60:02d}",
                    "🟢 Temps libre",
                    "free"
                )

        st.success(
            "✅ Planning généré."
        )

    st.divider()

    planning = get_planning(
        user_id
    )

    for item in planning:

        if item[4] == "revision":

            st.success(
                f"📚 {item[0]} : "
                f"{item[1]} → {item[2]} | "
                f"{item[3]}"
            )

        else:

            st.info(
                f"🟢 {item[0]} : "
                f"{item[1]} → {item[2]} | "
                f"{item[3]}"
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

        selected_subject = st.selectbox(
            "Matière",
            list(subject_dict.keys())
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
                list(course_dict.keys())
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
                        "🏁 Terminer le test final"
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

        selected_subject = st.selectbox(
            "Matière",
            list(subject_dict.keys())
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
                list(course_dict.keys())
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
                    f"{initial[2]}%"
                    if initial
                    else "-"
                )

            with c2:

                st.metric(
                    "Test final",
                    f"{final[2]}%"
                    if final
                    else "-"
                )

            with c3:

                if initial and final:

                    st.metric(
                        "Progression",
                        f"{final[2] - initial[2]:+d}%"
                    )

                else:

                    st.metric(
                        "Progression",
                        "-"
                    )