import sqlite3
import hashlib

DATABASE_NAME = "smartstudy.db"

# ============================================================
# ADMIN UNIQUE
# ============================================================
# CHANGE CES DEUX VALEURS AVANT DE LANCER L'APPLICATION
ADMIN_EMAIL = "wwail5958@gmail.com"
ADMIN_PASSWORD = "K132135550"


# ============================================================
# DATABASE
# ============================================================

def get_connection():
    return sqlite3.connect(DATABASE_NAME)


def hash_password(password):
    return hashlib.sha256(
        password.encode("utf-8")
    ).hexdigest()


def create_database():

    conn = get_connection()
    cursor = conn.cursor()

    # USERS
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'student'
        )
    """)

    # Si ancienne base sans role
    try:
        cursor.execute(
            "ALTER TABLE users ADD COLUMN role TEXT DEFAULT 'student'"
        )
    except sqlite3.OperationalError:
        pass

    # PROFILES
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS profiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER UNIQUE NOT NULL,
            level TEXT NOT NULL,
            branch TEXT NOT NULL
        )
    """)

    # SUBJECTS
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS subjects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            level TEXT NOT NULL,
            branch TEXT NOT NULL,
            name TEXT NOT NULL,
            UNIQUE(level, branch, name)
        )
    """)

    # COURSES
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            pdf_path TEXT NOT NULL
        )
    """)

    # QUESTIONS
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            course_id INTEGER NOT NULL,
            question TEXT NOT NULL,
            test_type TEXT NOT NULL,
            difficulty INTEGER DEFAULT 1
        )
    """)

    # ANSWERS
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS answers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question_id INTEGER NOT NULL,
            answer TEXT NOT NULL,
            is_correct INTEGER NOT NULL
        )
    """)

    # RESULTS
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            course_id INTEGER NOT NULL,
            test_type TEXT NOT NULL,
            score INTEGER NOT NULL,
            total INTEGER NOT NULL,
            percentage REAL NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # AVAILABILITY
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS availability (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            day TEXT NOT NULL,
            start_time TEXT NOT NULL,
            end_time TEXT NOT NULL
        )
    """)

    # PLANNING
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS planning (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            course_id INTEGER,
            day TEXT NOT NULL,
            start_time TEXT NOT NULL,
            end_time TEXT NOT NULL,
            activity TEXT NOT NULL,
            type TEXT NOT NULL
        )
    """)

    # COMPLETED COURSES
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS completed_courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            course_id INTEGER NOT NULL,
            completed INTEGER DEFAULT 1,
            completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(user_id, course_id)
        )
    """)

    conn.commit()

    # ========================================================
    # CREATION / VERIFICATION ADMIN UNIQUE
    # ========================================================

    admin_password_hash = hash_password(ADMIN_PASSWORD)

    cursor.execute("""
        SELECT id
        FROM users
        WHERE email = ?
    """, (ADMIN_EMAIL,))

    admin = cursor.fetchone()

    if admin:

        cursor.execute("""
            UPDATE users
            SET role = 'admin',
                password = ?,
                name = ?
            WHERE email = ?
        """, (
            admin_password_hash,
            "Administrateur",
            ADMIN_EMAIL
        ))

    else:

        cursor.execute("""
            INSERT INTO users
            (
                name,
                email,
                password,
                role
            )
            VALUES (?, ?, ?, 'admin')
        """, (
            "Administrateur",
            ADMIN_EMAIL,
            admin_password_hash
        ))

    conn.commit()
    conn.close()


# ============================================================
# USERS
# ============================================================

def create_user(name, email, password):

    conn = get_connection()
    cursor = conn.cursor()

    email = email.strip().lower()

    # Un étudiant ne peut jamais créer un compte admin
    cursor.execute("""
        SELECT id
        FROM users
        WHERE email = ?
    """, (email,))

    if cursor.fetchone():

        conn.close()
        return None

    cursor.execute("""
        INSERT INTO users
        (
            name,
            email,
            password,
            role
        )
        VALUES (?, ?, ?, 'student')
    """, (
        name.strip(),
        email,
        hash_password(password)
    ))

    user_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return user_id


def login_user(email, password):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            name,
            email,
            role
        FROM users
        WHERE email = ?
        AND password = ?
    """, (
        email.strip().lower(),
        hash_password(password)
    ))

    user = cursor.fetchone()

    conn.close()

    return user


# ============================================================
# PROFILE
# ============================================================

def save_profile(user_id, level, branch):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR REPLACE INTO profiles
        (
            user_id,
            level,
            branch
        )
        VALUES (?, ?, ?)
    """, (
        user_id,
        level,
        branch
    ))

    conn.commit()
    conn.close()


def get_profile(user_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            level,
            branch
        FROM profiles
        WHERE user_id = ?
    """, (user_id,))

    profile = cursor.fetchone()

    conn.close()

    return profile


# ============================================================
# SUBJECTS
# ============================================================

def add_subject(level, branch, name):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR IGNORE INTO subjects
        (
            level,
            branch,
            name
        )
        VALUES (?, ?, ?)
    """, (
        level,
        branch,
        name
    ))

    cursor.execute("""
        SELECT id
        FROM subjects
        WHERE level = ?
        AND branch = ?
        AND name = ?
    """, (
        level,
        branch,
        name
    ))

    result = cursor.fetchone()

    conn.commit()
    conn.close()

    return result[0]


def get_subjects(level, branch):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            name
        FROM subjects
        WHERE level = ?
        AND branch = ?
        ORDER BY id
    """, (
        level,
        branch
    ))

    subjects = cursor.fetchall()

    conn.close()

    return subjects


def delete_subject(subject_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM subjects
        WHERE id = ?
    """, (subject_id,))

    conn.commit()
    conn.close()


# ============================================================
# COURSES
# ============================================================

def add_course(subject_id, title, pdf_path):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO courses
        (
            subject_id,
            title,
            pdf_path
        )
        VALUES (?, ?, ?)
    """, (
        subject_id,
        title,
        pdf_path
    ))

    course_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return course_id


def get_courses(subject_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            title,
            pdf_path
        FROM courses
        WHERE subject_id = ?
        ORDER BY id
    """, (subject_id,))

    courses = cursor.fetchall()

    conn.close()

    return courses


def delete_course(course_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM answers
        WHERE question_id IN (
            SELECT id
            FROM questions
            WHERE course_id = ?
        )
    """, (course_id,))

    cursor.execute("""
        DELETE FROM questions
        WHERE course_id = ?
    """, (course_id,))

    cursor.execute("""
        DELETE FROM results
        WHERE course_id = ?
    """, (course_id,))

    cursor.execute("""
        DELETE FROM completed_courses
        WHERE course_id = ?
    """, (course_id,))

    cursor.execute("""
        DELETE FROM courses
        WHERE id = ?
    """, (course_id,))

    conn.commit()
    conn.close()


# ============================================================
# QUESTIONS
# ============================================================

def add_question(
    course_id,
    question,
    test_type,
    difficulty=1
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO questions
        (
            course_id,
            question,
            test_type,
            difficulty
        )
        VALUES (?, ?, ?, ?)
    """, (
        course_id,
        question,
        test_type,
        difficulty
    ))

    question_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return question_id


def get_questions(course_id, test_type):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            question,
            difficulty
        FROM questions
        WHERE course_id = ?
        AND test_type = ?
        ORDER BY id
    """, (
        course_id,
        test_type
    ))

    questions = cursor.fetchall()

    conn.close()

    return questions


def delete_question(question_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM answers
        WHERE question_id = ?
    """, (question_id,))

    cursor.execute("""
        DELETE FROM questions
        WHERE id = ?
    """, (question_id,))

    conn.commit()
    conn.close()


# ============================================================
# ANSWERS
# ============================================================

def add_answer(
    question_id,
    answer,
    is_correct
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO answers
        (
            question_id,
            answer,
            is_correct
        )
        VALUES (?, ?, ?)
    """, (
        question_id,
        answer,
        is_correct
    ))

    conn.commit()
    conn.close()


def get_answers(question_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            answer,
            is_correct
        FROM answers
        WHERE question_id = ?
        ORDER BY id
    """, (question_id,))

    answers = cursor.fetchall()

    conn.close()

    return answers


# ============================================================
# RESULTS
# ============================================================

def save_result(
    user_id,
    course_id,
    test_type,
    score,
    total,
    percentage
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO results
        (
            user_id,
            course_id,
            test_type,
            score,
            total,
            percentage
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        user_id,
        course_id,
        test_type,
        score,
        total,
        percentage
    ))

    conn.commit()
    conn.close()


def has_test_result(
    user_id,
    course_id,
    test_type
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id
        FROM results
        WHERE user_id = ?
        AND course_id = ?
        AND test_type = ?
        LIMIT 1
    """, (
        user_id,
        course_id,
        test_type
    ))

    result = cursor.fetchone()

    conn.close()

    return result is not None


def get_latest_result(
    user_id,
    course_id,
    test_type
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            score,
            total,
            percentage,
            created_at
        FROM results
        WHERE user_id = ?
        AND course_id = ?
        AND test_type = ?
        ORDER BY id DESC
        LIMIT 1
    """, (
        user_id,
        course_id,
        test_type
    ))

    result = cursor.fetchone()

    conn.close()

    return result


# ============================================================
# AVAILABILITY
# ============================================================

def delete_availability(user_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM availability
        WHERE user_id = ?
    """, (user_id,))

    conn.commit()
    conn.close()


def add_availability(
    user_id,
    day,
    start_time,
    end_time
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO availability
        (
            user_id,
            day,
            start_time,
            end_time
        )
        VALUES (?, ?, ?, ?)
    """, (
        user_id,
        day,
        start_time,
        end_time
    ))

    conn.commit()
    conn.close()


# ============================================================
# PLANNING
# ============================================================

def delete_planning(user_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM planning
        WHERE user_id = ?
    """, (user_id,))

    conn.commit()
    conn.close()


def add_planning(
    user_id,
    course_id,
    day,
    start_time,
    end_time,
    activity,
    planning_type
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO planning
        (
            user_id,
            course_id,
            day,
            start_time,
            end_time,
            activity,
            type
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        user_id,
        course_id,
        day,
        start_time,
        end_time,
        activity,
        planning_type
    ))

    conn.commit()
    conn.close()


def get_planning(user_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            day,
            start_time,
            end_time,
            activity,
            type
        FROM planning
        WHERE user_id = ?
        ORDER BY id
    """, (user_id,))

    planning = cursor.fetchall()

    conn.close()

    return planning


# ============================================================
# COMPLETED COURSES
# ============================================================

def complete_course(user_id, course_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR REPLACE INTO completed_courses
        (
            user_id,
            course_id,
            completed
        )
        VALUES (?, ?, 1)
    """, (
        user_id,
        course_id
    ))

    conn.commit()
    conn.close()


def is_course_completed(user_id, course_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT completed
        FROM completed_courses
        WHERE user_id = ?
        AND course_id = ?
    """, (
        user_id,
        course_id
    ))

    result = cursor.fetchone()

    conn.close()

    return result is not None and result[0] == 1