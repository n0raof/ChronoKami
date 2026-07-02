import sqlite3
from datetime import date, datetime, timedelta

DB_PATH = "tasks.db"

_OLD_CATEGORY_MAP = {
    "📚 Учёба": "study",
    "💼 Работа": "work",
    "🏠 Дом": "home",
    "🎯 Другое": "other",
}
_OLD_PRIORITY_MAP = {
    "Высокий": "high",
    "Средний": "medium",
    "Низкий": "low",
}

VALID_CATEGORIES = ("study", "work", "home", "other")
VALID_PRIORITIES = ("high", "medium", "low")


def _conn():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = _conn()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            text TEXT NOT NULL,
            category TEXT NOT NULL,
            priority TEXT NOT NULL,
            done INTEGER NOT NULL DEFAULT 0
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            language TEXT NOT NULL DEFAULT 'ru'
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS habits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            streak INTEGER NOT NULL DEFAULT 0,
            best_streak INTEGER NOT NULL DEFAULT 0,
            last_done_date TEXT,
            reminder_time TEXT,
            created_at TEXT NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS habit_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            habit_id INTEGER NOT NULL,
            log_date TEXT NOT NULL,
            UNIQUE(habit_id, log_date)
        )
    """)


    cur.execute("""
        CREATE TABLE IF NOT EXISTS focus_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            duration_minutes INTEGER NOT NULL,
            started_at TEXT NOT NULL,
            ended_at TEXT,
            status TEXT NOT NULL DEFAULT 'running',
            distracted INTEGER
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS focus_stats (
            user_id INTEGER PRIMARY KEY,
            streak INTEGER NOT NULL DEFAULT 0,
            best_streak INTEGER NOT NULL DEFAULT 0,
            last_completed_date TEXT,
            total_sessions INTEGER NOT NULL DEFAULT 0,
            distracted_sessions INTEGER NOT NULL DEFAULT 0
        )
    """)

    conn.commit()

    cur.execute("PRAGMA table_info(users)")
    user_columns = {row[1] for row in cur.fetchall()}
    if "utc_offset_minutes" not in user_columns:
        cur.execute("ALTER TABLE users ADD COLUMN utc_offset_minutes INTEGER")
    conn.commit()

    cur.execute("SELECT id, category, priority FROM tasks")
    rows = cur.fetchall()
    for task_id, category, priority in rows:
        new_category = category if category in VALID_CATEGORIES else _OLD_CATEGORY_MAP.get(category, "other")
        new_priority = priority if priority in VALID_PRIORITIES else _OLD_PRIORITY_MAP.get(priority, "medium")
        if new_category != category or new_priority != priority:
            cur.execute(
                "UPDATE tasks SET category = ?, priority = ? WHERE id = ?",
                (new_category, new_priority, task_id),
            )
    conn.commit()
    conn.close()


# ЯЗЫК

def get_user_language(user_id):
    conn = _conn()
    cur = conn.cursor()
    cur.execute("SELECT language FROM users WHERE user_id = ?", (user_id,))
    row = cur.fetchone()
    conn.close()
    return row[0] if row else None


def set_user_language(user_id, lang):
    conn = _conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO users (user_id, language) VALUES (?, ?) "
        "ON CONFLICT(user_id) DO UPDATE SET language = excluded.language",
        (user_id, lang),
    )
    conn.commit()
    conn.close()


# ЧАСОВОЙ ПОЯС 

def get_user_utc_offset(user_id):
    conn = _conn()
    cur = conn.cursor()
    cur.execute("SELECT utc_offset_minutes FROM users WHERE user_id = ?", (user_id,))
    row = cur.fetchone()
    conn.close()
    return row[0] if row and row[0] is not None else None


def set_user_utc_offset(user_id, offset_minutes):
    conn = _conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO users (user_id, language, utc_offset_minutes) VALUES (?, 'ru', ?) "
        "ON CONFLICT(user_id) DO UPDATE SET utc_offset_minutes = excluded.utc_offset_minutes",
        (user_id, offset_minutes),
    )
    conn.commit()
    conn.close()


def local_date_from_offset(offset_minutes):
    return (datetime.utcnow() + timedelta(minutes=offset_minutes or 0)).date()


# ЗАДАЧИ

def add_task_db(user_id, text, category, priority):
    conn = _conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO tasks (user_id, text, category, priority, done) VALUES (?, ?, ?, ?, 0)",
        (user_id, text, category, priority),
    )
    conn.commit()
    conn.close()


def get_tasks_db(user_id):
    conn = _conn()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, text, category, priority, done FROM tasks WHERE user_id = ? ORDER BY done, id",
        (user_id,),
    )
    rows = cur.fetchall()
    conn.close()
    return rows


def mark_task_done_db(task_id, user_id):
    conn = _conn()
    cur = conn.cursor()
    cur.execute("UPDATE tasks SET done = 1 WHERE id = ? AND user_id = ?", (task_id, user_id))
    conn.commit()
    conn.close()


def delete_task_db(task_id, user_id):
    conn = _conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM tasks WHERE id = ? AND user_id = ?", (task_id, user_id))
    conn.commit()
    conn.close()


# ПРИВЫЧКИ

def add_habit_db(user_id, name):
    conn = _conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO habits (user_id, name, streak, best_streak, last_done_date, reminder_time, created_at) "
        "VALUES (?, ?, 0, 0, NULL, NULL, ?)",
        (user_id, name, date.today().isoformat()),
    )
    conn.commit()
    habit_id = cur.lastrowid
    conn.close()
    return habit_id


def get_habits_db(user_id):
    conn = _conn()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, name, streak, best_streak, last_done_date, reminder_time "
        "FROM habits WHERE user_id = ? ORDER BY id",
        (user_id,),
    )
    rows = cur.fetchall()
    conn.close()
    return rows


def get_habit_db(habit_id, user_id):
    conn = _conn()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, name, streak, best_streak, last_done_date, reminder_time "
        "FROM habits WHERE id = ? AND user_id = ?",
        (habit_id, user_id),
    )
    row = cur.fetchone()
    conn.close()
    return row


def mark_habit_done_db(habit_id, user_id, today=None):
    conn = _conn()
    cur = conn.cursor()
    cur.execute(
        "SELECT streak, best_streak, last_done_date FROM habits WHERE id = ? AND user_id = ?",
        (habit_id, user_id),
    )
    row = cur.fetchone()
    if not row:
        conn.close()
        return "not_found", 0

    streak, best_streak, last_done_date = row
    today = today or date.today()
    today_str = today.isoformat()
    yesterday_str = (today - timedelta(days=1)).isoformat()

    if last_done_date == today_str:
        conn.close()
        return "already_done", streak

    new_streak = streak + 1 if last_done_date == yesterday_str else 1
    new_best = max(best_streak, new_streak)

    cur.execute(
        "UPDATE habits SET streak = ?, best_streak = ?, last_done_date = ? WHERE id = ?",
        (new_streak, new_best, today_str, habit_id),
    )
    try:
        cur.execute(
            "INSERT INTO habit_logs (habit_id, log_date) VALUES (?, ?)",
            (habit_id, today_str),
        )
    except sqlite3.IntegrityError:
        pass
    conn.commit()
    conn.close()
    return "ok", new_streak


def set_habit_reminder_db(habit_id, user_id, time_str):
    conn = _conn()
    cur = conn.cursor()
    cur.execute(
        "UPDATE habits SET reminder_time = ? WHERE id = ? AND user_id = ?",
        (time_str, habit_id, user_id),
    )
    conn.commit()
    conn.close()


def clear_habit_reminder_db(habit_id, user_id):
    set_habit_reminder_db(habit_id, user_id, None)


def get_all_reminders_db():
    conn = _conn()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, user_id, reminder_time, name FROM habits WHERE reminder_time IS NOT NULL"
    )
    rows = cur.fetchall()
    conn.close()
    return rows


# ФОКУС-СЕССИИ (ПОМОДОРО + САМООТЧЁТ)

def start_focus_session_db(user_id, duration_minutes):
    conn = _conn()
    cur = conn.cursor()
    started_at = datetime.utcnow().isoformat(timespec="seconds")
    cur.execute(
        "INSERT INTO focus_sessions (user_id, duration_minutes, started_at, status) "
        "VALUES (?, ?, ?, 'running')",
        (user_id, duration_minutes, started_at),
    )
    conn.commit()
    session_id = cur.lastrowid
    conn.close()
    return session_id


def get_running_focus_session_db(user_id):
    conn = _conn()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, user_id, duration_minutes, started_at, status FROM focus_sessions "
        "WHERE user_id = ? AND status = 'running' ORDER BY id DESC LIMIT 1",
        (user_id,),
    )
    row = cur.fetchone()
    conn.close()
    return row


def get_focus_session_db(session_id):
    conn = _conn()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, user_id, duration_minutes, started_at, status FROM focus_sessions WHERE id = ?",
        (session_id,),
    )
    row = cur.fetchone()
    conn.close()
    return row


def cancel_focus_session_db(session_id):
    conn = _conn()
    cur = conn.cursor()
    cur.execute(
        "UPDATE focus_sessions SET status = 'cancelled', ended_at = ? "
        "WHERE id = ? AND status = 'running'",
        (datetime.utcnow().isoformat(timespec="seconds"), session_id),
    )
    conn.commit()
    conn.close()


def complete_focus_session_db(session_id, distracted, today):

    
    conn = _conn()
    cur = conn.cursor()
    cur.execute("SELECT user_id, status FROM focus_sessions WHERE id = ?", (session_id,))
    row = cur.fetchone()
    if not row or row[1] != "running":
        conn.close()
        return None
    user_id = row[0]

    cur.execute(
        "UPDATE focus_sessions SET status = 'completed', ended_at = ?, distracted = ? WHERE id = ?",
        (datetime.utcnow().isoformat(timespec="seconds"), int(bool(distracted)), session_id),
    )

    cur.execute(
        "SELECT streak, best_streak, last_completed_date, total_sessions, distracted_sessions "
        "FROM focus_stats WHERE user_id = ?",
        (user_id,),
    )
    stats = cur.fetchone()
    if stats is None:
        streak, best_streak, last_completed_date, total_sessions, distracted_sessions = 0, 0, None, 0, 0
    else:
        streak, best_streak, last_completed_date, total_sessions, distracted_sessions = stats

    today_str = today.isoformat()
    yesterday_str = (today - timedelta(days=1)).isoformat()

    if last_completed_date == today_str:
        new_streak = streak  # сессия сегодня уже была — серия не растёт повторно
    elif last_completed_date == yesterday_str:
        new_streak = streak + 1
    else:
        new_streak = 1

    is_new_best = new_streak > best_streak
    new_best = max(best_streak, new_streak)
    new_total = total_sessions + 1
    new_distracted = distracted_sessions + (1 if distracted else 0)

    cur.execute(
        "INSERT INTO focus_stats "
        "(user_id, streak, best_streak, last_completed_date, total_sessions, distracted_sessions) "
        "VALUES (?, ?, ?, ?, ?, ?) "
        "ON CONFLICT(user_id) DO UPDATE SET "
        "streak = excluded.streak, best_streak = excluded.best_streak, "
        "last_completed_date = excluded.last_completed_date, "
        "total_sessions = excluded.total_sessions, distracted_sessions = excluded.distracted_sessions",
        (user_id, new_streak, new_best, today_str, new_total, new_distracted),
    )
    conn.commit()
    conn.close()
    return new_streak, new_best, is_new_best


def get_focus_stats_db(user_id):
    conn = _conn()
    cur = conn.cursor()
    cur.execute(
        "SELECT streak, best_streak, last_completed_date, total_sessions, distracted_sessions "
        "FROM focus_stats WHERE user_id = ?",
        (user_id,),
    )
    row = cur.fetchone()
    conn.close()
    if not row:
        return {"streak": 0, "best_streak": 0, "last_completed_date": None,
                 "total_sessions": 0, "distracted_sessions": 0}
    streak, best_streak, last_completed_date, total_sessions, distracted_sessions = row
    return {"streak": streak, "best_streak": best_streak, "last_completed_date": last_completed_date,
             "total_sessions": total_sessions, "distracted_sessions": distracted_sessions}


def get_all_running_focus_sessions_db():
    conn = _conn()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, user_id, duration_minutes, started_at FROM focus_sessions WHERE status = 'running'"
    )
    rows = cur.fetchall()
    conn.close()
    return rows
