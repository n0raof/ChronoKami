import os
import re
import random
from datetime import (
    time as dt_time,
    timezone as dt_timezone,
    datetime as dt_datetime,
    timedelta as dt_timedelta,
)

from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, BotCommand
from telegram.error import BadRequest
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

import db
from locales import t, LANG_NAMES, CATEGORY_EMOJI, PRIORITY_EMOJI, DEFAULT_LANG

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise ValueError("Токен не найден! Проверь файл .env")

TIME_RE = re.compile(r"^([01]\d|2[0-3]):([0-5]\d)$")
# Часовой пояс
OFFSET_RE = re.compile(r"^(?:UTC)?\s*([+-]?)\s*(\d{1,2})(?::([0-5]\d))?$", re.IGNORECASE)

FOCUS_DURATIONS = (25, 45, 50)  # минуты
FOCUS_MIN_MINUTES = 1
FOCUS_MAX_MINUTES = 180

# СОСТОЯНИЯ ПОЛЬЗОВАТЕЛЕЙ
user_state = {}
user_temp = {}


def get_lang(user_id):
    return db.get_user_language(user_id) or DEFAULT_LANG


def parse_utc_offset(text):
    """'UTC+5' / '+5' / '-3' / '5:30' -> смещение в минутах от UTC"""
    match = OFFSET_RE.match(text.strip().replace(" ", ""))
    if not match:
        return None
    sign, hours_str, minutes_str = match.groups()
    hours = int(hours_str)
    minutes = int(minutes_str) if minutes_str else 0
    total_minutes = hours * 60 + minutes
    if sign == "-":
        total_minutes = -total_minutes
    if not (-12 * 60 <= total_minutes <= 14 * 60):
        return None
    return total_minutes


def format_utc_offset(offset_minutes):
    sign = "+" if offset_minutes >= 0 else "-"
    absolute = abs(offset_minutes)
    hours, minutes = divmod(absolute, 60)
    suffix = f":{minutes:02d}" if minutes else ""
    return f"UTC{sign}{hours}{suffix}"


def local_date_for(user_id):
    """Сегодняшняя дата в локальном времени пользователя — для границы суток серий."""
    offset = db.get_user_utc_offset(user_id) or 0
    return db.local_date_from_offset(offset)


async def safe_edit(query, text, kb=None):
    """edit_message_text, но не падает на 'Message is not modified'."""
    try:
        await query.edit_message_text(text, reply_markup=kb)
    except BadRequest as e:
        if "Message is not modified" not in str(e):
            raise


# КЛАВИАТУРЫ

def kb_language():
    buttons = [[InlineKeyboardButton(name, callback_data=f"lang:{code}")] for code, name in LANG_NAMES.items()]
    return InlineKeyboardMarkup(buttons)


def kb_welcome(lang):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(t(lang, "btn_make_task"), callback_data="task:add")],
        [InlineKeyboardButton(t(lang, "btn_level_habit"), callback_data="menu:habits")],
        [InlineKeyboardButton(t(lang, "btn_focus"), callback_data="menu:focus")],
        [InlineKeyboardButton(t(lang, "btn_food"), callback_data="food:start")],
        [InlineKeyboardButton(t(lang, "btn_timezone"), callback_data="tz:change")],
    ])


def kb_tasks_menu(lang):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(t(lang, "btn_tasks_add"), callback_data="task:add")],
        [InlineKeyboardButton(t(lang, "btn_tasks_list"), callback_data="task:list")],
        [InlineKeyboardButton(t(lang, "btn_back"), callback_data="menu:welcome")],
    ])


def kb_category(lang):
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(f"{CATEGORY_EMOJI['study']} {t(lang, 'cat_study')}", callback_data="cat:study"),
            InlineKeyboardButton(f"{CATEGORY_EMOJI['work']} {t(lang, 'cat_work')}", callback_data="cat:work"),
        ],
        [
            InlineKeyboardButton(f"{CATEGORY_EMOJI['home']} {t(lang, 'cat_home')}", callback_data="cat:home"),
            InlineKeyboardButton(f"{CATEGORY_EMOJI['other']} {t(lang, 'cat_other')}", callback_data="cat:other"),
        ],
    ])


def kb_priority(lang):
    return InlineKeyboardMarkup([[
        InlineKeyboardButton(f"{PRIORITY_EMOJI['high']} {t(lang, 'prio_high')}", callback_data="prio:high"),
        InlineKeyboardButton(f"{PRIORITY_EMOJI['medium']} {t(lang, 'prio_medium')}", callback_data="prio:medium"),
        InlineKeyboardButton(f"{PRIORITY_EMOJI['low']} {t(lang, 'prio_low')}", callback_data="prio:low"),
    ]])


def kb_habits_menu(lang, rows):
    buttons = []
    for habit_id, name, streak, best_streak, last_done_date, reminder_time in rows:
        clock = " ⏰" if reminder_time else ""
        buttons.append([
            InlineKeyboardButton(f"✅ {name} ({streak}🔥){clock}", callback_data=f"habit:done:{habit_id}"),
            InlineKeyboardButton("⏰", callback_data=f"habit:remind_set:{habit_id}"),
        ])
    buttons.append([InlineKeyboardButton(t(lang, "btn_habits_add"), callback_data="habit:add")])
    buttons.append([InlineKeyboardButton(t(lang, "btn_back"), callback_data="menu:welcome")])
    return InlineKeyboardMarkup(buttons)


def kb_methodology(lang):
    return InlineKeyboardMarkup([[InlineKeyboardButton(t(lang, "btn_back"), callback_data="menu:welcome")]])


def kb_reminder_ask(lang, habit_id):
    return InlineKeyboardMarkup([[
        InlineKeyboardButton(t(lang, "btn_yes"), callback_data=f"habit:remind_set:{habit_id}"),
        InlineKeyboardButton(t(lang, "btn_no"), callback_data="habit:remind_skip"),
    ]])


def kb_focus_menu(lang):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(t(lang, "btn_focus_start"), callback_data="focus:new")],
        [InlineKeyboardButton(t(lang, "btn_back"), callback_data="menu:welcome")],
    ])


def kb_focus_duration(lang):
    duration_row = [InlineKeyboardButton(str(m), callback_data=f"focus:dur:{m}") for m in FOCUS_DURATIONS]
    return InlineKeyboardMarkup([
        duration_row,
        [InlineKeyboardButton(t(lang, "btn_focus_custom"), callback_data="focus:dur:custom")],
        [InlineKeyboardButton(t(lang, "btn_back"), callback_data="menu:focus")],
    ])


def kb_focus_running(lang, session_id):
    return InlineKeyboardMarkup([[
        InlineKeyboardButton(t(lang, "btn_focus_cancel"), callback_data=f"focus:cancel:{session_id}")
    ]])


def kb_focus_selfreport(lang, session_id):
    # Самоотчёт
    return InlineKeyboardMarkup([[
        InlineKeyboardButton(t(lang, "btn_distracted_no"), callback_data=f"focus:report:{session_id}:0"),
        InlineKeyboardButton(t(lang, "btn_distracted_yes"), callback_data=f"focus:report:{session_id}:1"),
    ]])


def kb_food_time(lang):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(t(lang, "btn_food_lt30"), callback_data="food:time:lt30")],
        [InlineKeyboardButton(t(lang, "btn_food_30_60"), callback_data="food:time:30_60")],
        [InlineKeyboardButton(t(lang, "btn_food_1_2h"), callback_data="food:time:1_2h")],
        [InlineKeyboardButton(t(lang, "btn_food_gt2h"), callback_data="food:time:gt2h")],
        [InlineKeyboardButton(t(lang, "btn_back"), callback_data="menu:welcome")],
    ])


def kb_food_result(lang):
    return InlineKeyboardMarkup([[InlineKeyboardButton(t(lang, "btn_back"), callback_data="menu:welcome")]])


def build_tasks_list_screen(lang, user_id):
    rows = db.get_tasks_db(user_id)
    if not rows:
        text = t(lang, "no_tasks")
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton(t(lang, "btn_tasks_add"), callback_data="task:add")],
            [InlineKeyboardButton(t(lang, "btn_back"), callback_data="menu:tasks")],
        ])
        return text, kb

    lines = [t(lang, "tasks_header"), ""]
    buttons = []
    for i, (task_id, text_, category, priority, done) in enumerate(rows, start=1):
        status = "✅" if done else "⬜"
        cat_label = t(lang, f"cat_{category}")
        prio_label = t(lang, f"prio_{priority}")
        lines.append(
            f"{i}. {status} {text_}\n"
            f"   {CATEGORY_EMOJI.get(category, '')} {cat_label} | {PRIORITY_EMOJI.get(priority, '')} {prio_label}"
        )
        row = []
        if not done:
            row.append(InlineKeyboardButton(f"✅ {i}", callback_data=f"task:done:{task_id}"))
        row.append(InlineKeyboardButton(f"🗑 {i}", callback_data=f"task:delete:{task_id}"))
        buttons.append(row)

    buttons.append([InlineKeyboardButton(t(lang, "btn_tasks_add"), callback_data="task:add")])
    buttons.append([InlineKeyboardButton(t(lang, "btn_back"), callback_data="menu:tasks")])
    return "\n".join(lines), InlineKeyboardMarkup(buttons)


def build_habits_screen(lang, user_id):
    rows = db.get_habits_db(user_id)
    text = t(lang, "habits_header") if rows else t(lang, "no_habits")
    return text, kb_habits_menu(lang, rows)


# УВЕДОМЛЕНИЯ И ТАЙМЕРЫ 

async def send_habit_reminder(context: ContextTypes.DEFAULT_TYPE):
    job = context.job
    habit_id = job.data["habit_id"]
    user_id = job.data["user_id"]
    lang = get_lang(user_id)

    habit = db.get_habit_db(habit_id, user_id)
    if not habit:
        job.schedule_removal()
        return

    _, name, streak, best_streak, last_done_date, reminder_time = habit
    text = t(lang, "reminder_push_text", name=name, streak=streak)
    kb = InlineKeyboardMarkup([[
        InlineKeyboardButton(t(lang, "btn_reminder_done"), callback_data=f"habit:done:{habit_id}")
    ]])
    await context.bot.send_message(chat_id=user_id, text=text, reply_markup=kb)


def schedule_habit_job(job_queue, habit_id, user_id, time_str, offset_minutes=0):
    hour, minute = map(int, time_str.split(":"))
    job_name = f"habit_reminder_{habit_id}"
    for job in job_queue.get_jobs_by_name(job_name):
        job.schedule_removal()
    tz = dt_timezone(dt_timedelta(minutes=offset_minutes or 0))
    job_queue.run_daily(
        send_habit_reminder,
        time=dt_time(hour=hour, minute=minute, tzinfo=tz),
        name=job_name,
        data={"habit_id": habit_id, "user_id": user_id},
    )


async def focus_session_end(context: ContextTypes.DEFAULT_TYPE):
    """Бот сам следит за временем. По истечении — честный самоотчёт, не 'детект'."""
    job = context.job
    session_id = job.data["session_id"]
    user_id = job.data["user_id"]

    session = db.get_focus_session_db(session_id)
    if not session or session[4] != "running":
        return  # отменена пользователем или уже обработана

    lang = get_lang(user_id)
    await context.bot.send_message(
        chat_id=user_id,
        text=t(lang, "focus_end_text"),
        reply_markup=kb_focus_selfreport(lang, session_id),
    )


async def begin_focus_session(user_id, lang, minutes, context, query=None):
    session_id = db.start_focus_session_db(user_id, minutes)
    context.job_queue.run_once(
        focus_session_end,
        when=minutes * 60,
        name=f"focus_end_{session_id}",
        data={"session_id": session_id, "user_id": user_id},
    )
    text = t(lang, "focus_started", minutes=minutes)
    kb = kb_focus_running(lang, session_id)
    if query is not None:
        await safe_edit(query, text, kb)
    else:
        await context.bot.send_message(chat_id=user_id, text=text, reply_markup=kb)


# КОМАНДЫ 

async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    lang = db.get_user_language(user_id)
    if lang is None:
        await update.message.reply_text(t(DEFAULT_LANG, "lang_picker_text"), reply_markup=kb_language())
        return
    if db.get_user_utc_offset(user_id) is None:
        user_state[user_id] = "waiting_for_utc_offset"
        await update.message.reply_text(t(lang, "utc_offset_prompt"))
        return
    await update.message.reply_text(t(lang, "welcome_text"), reply_markup=kb_welcome(lang))


async def cmd_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_lang(update.effective_user.id)
    await update.message.reply_text(t(lang, "tasks_header"), reply_markup=kb_tasks_menu(lang))


async def cmd_habits(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_lang(update.effective_user.id)
    text, kb = build_habits_screen(lang, update.effective_user.id)
    await update.message.reply_text(text, reply_markup=kb)


async def cmd_focus(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    lang = get_lang(user_id)
    stats = db.get_focus_stats_db(user_id)
    text = t(lang, "focus_intro_text", streak=stats["streak"], best=stats["best_streak"])
    await update.message.reply_text(text, reply_markup=kb_focus_menu(lang))


async def cmd_food(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_lang(update.effective_user.id)
    await update.message.reply_text(t(lang, "food_choose_time"), reply_markup=kb_food_time(lang))


async def cmd_timezone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    lang = get_lang(user_id)
    user_state[user_id] = "waiting_for_utc_offset"
    await update.message.reply_text(t(lang, "utc_offset_prompt"))


async def cmd_methodology(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_lang(update.effective_user.id)
    await update.message.reply_text(t(lang, "methodology_text"), reply_markup=kb_methodology(lang))


async def cmd_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_lang(update.effective_user.id)
    await update.message.reply_text(t(lang, "lang_picker_text"), reply_markup=kb_language())


async def cmd_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_lang(update.effective_user.id)
    await update.message.reply_text(t(lang, "help_text"))


KITTEN_PHOTOS = [
    "https://images.unsplash.com/photo-1592194996308-7b43878e84a6",
    "https://images.unsplash.com/photo-1574158622682-e40e69881006",
    "https://images.unsplash.com/photo-1591871937573-74dbba515c4c",
    "https://images.unsplash.com/photo-1533738363-b7f9aef128ce",
    "https://images.unsplash.com/photo-1561948955-570b270e7c36",
    "https://images.unsplash.com/photo-1495360010541-f48722b34f7d",
]


async def kittens(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo_url = random.choice(KITTEN_PHOTOS)
    await update.message.reply_photo(photo=photo_url, caption="Нашёл для тебя котёнка 🐱")


# CALLBACK-КНОПКИ 

async def on_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = update.effective_user.id
    data = query.data
    lang = get_lang(user_id)

    # язык
    if data.startswith("lang:"):
        code = data.split(":", 1)[1]
        db.set_user_language(user_id, code)
        await query.answer(t(code, "language_changed"))
        if db.get_user_utc_offset(user_id) is None:
            user_state[user_id] = "waiting_for_utc_offset"
            await safe_edit(query, t(code, "utc_offset_prompt"))
        else:
            await safe_edit(query, t(code, "welcome_text"), kb_welcome(code))
        return

    # часовой поя
    if data == "tz:change":
        await query.answer()
        user_state[user_id] = "waiting_for_utc_offset"
        await safe_edit(query, t(lang, "utc_offset_prompt"))
        return

    # навигация по меню
    if data == "menu:welcome":
        await query.answer()
        await safe_edit(query, t(lang, "welcome_text"), kb_welcome(lang))
        return

    if data == "menu:tasks":
        await query.answer()
        await safe_edit(query, t(lang, "tasks_header"), kb_tasks_menu(lang))
        return

    if data == "menu:habits":
        await query.answer()
        text, kb = build_habits_screen(lang, user_id)
        await safe_edit(query, text, kb)
        return

    if data == "menu:methodology":
        await query.answer()
        await safe_edit(query, t(lang, "methodology_text"), kb_methodology(lang))
        return

    if data == "menu:language":
        await query.answer()
        await safe_edit(query, t(lang, "lang_picker_text"), kb_language())
        return

    if data == "menu:focus":
        await query.answer()
        stats = db.get_focus_stats_db(user_id)
        text = t(lang, "focus_intro_text", streak=stats["streak"], best=stats["best_streak"])
        await safe_edit(query, text, kb_focus_menu(lang))
        return

    # задачи
    if data == "task:add":
        await query.answer()
        user_state[user_id] = "waiting_for_task_text"
        user_temp[user_id] = {}
        await safe_edit(query, t(lang, "task_text_prompt"))
        return

    if data == "task:list":
        await query.answer()
        text, kb = build_tasks_list_screen(lang, user_id)
        await safe_edit(query, text, kb)
        return

    if data.startswith("task:done:"):
        task_id = int(data.split(":")[2])
        db.mark_task_done_db(task_id, user_id)
        await query.answer(t(lang, "task_marked_done"))
        text, kb = build_tasks_list_screen(lang, user_id)
        await safe_edit(query, text, kb)
        return

    if data.startswith("task:delete:"):
        task_id = int(data.split(":")[2])
        db.delete_task_db(task_id, user_id)
        await query.answer(t(lang, "task_deleted"))
        text, kb = build_tasks_list_screen(lang, user_id)
        await safe_edit(query, text, kb)
        return

    if data.startswith("cat:"):
        temp = user_temp.get(user_id)
        if not temp or "text" not in temp:
            await query.answer(t(lang, "flow_expired"), show_alert=True)
            await safe_edit(query, t(lang, "tasks_header"), kb_tasks_menu(lang))
            return
        await query.answer()
        temp["category"] = data.split(":")[1]
        await safe_edit(query, t(lang, "choose_priority"), kb_priority(lang))
        return

    if data.startswith("prio:"):
        temp = user_temp.get(user_id)
        if not temp or "category" not in temp:
            await query.answer(t(lang, "flow_expired"), show_alert=True)
            await safe_edit(query, t(lang, "tasks_header"), kb_tasks_menu(lang))
            return
        priority = data.split(":")[1]
        db.add_task_db(user_id, temp["text"], temp["category"], priority)
        added_text = t(lang, "task_added", text=temp["text"])
        user_temp[user_id] = {}
        user_state[user_id] = None
        await query.answer()
        await safe_edit(query, added_text, kb_tasks_menu(lang))
        return

    # привычки
    if data == "habit:add":
        await query.answer()
        user_state[user_id] = "waiting_for_habit_name"
        await safe_edit(query, t(lang, "habit_name_prompt"))
        return

    if data.startswith("habit:done:"):
        habit_id = int(data.split(":")[2])
        today = local_date_for(user_id)
        status, streak = db.mark_habit_done_db(habit_id, user_id, today)
        if status == "already_done":
            await query.answer(t(lang, "habit_already_done"), show_alert=True)
        else:
            await query.answer(t(lang, "habit_marked_done", streak=streak))
        text, kb = build_habits_screen(lang, user_id)
        try:
            await safe_edit(query, text, kb)
        except BadRequest:
            # сообщение могло прийти из push-уведомления и не иметь меню для редактирования
            await context.bot.send_message(chat_id=user_id, text=text, reply_markup=kb)
        return

    if data.startswith("habit:remind_set:"):
        habit_id = int(data.split(":")[2])
        await query.answer()
        user_state[user_id] = "waiting_for_reminder_time"
        user_temp[user_id] = {"habit_id": habit_id}
        offset = db.get_user_utc_offset(user_id) or 0
        await safe_edit(query, t(lang, "reminder_time_prompt", offset=format_utc_offset(offset)))
        return

    if data == "habit:remind_skip":
        await query.answer()
        text, kb = build_habits_screen(lang, user_id)
        await safe_edit(query, text, kb)
        return

    # фокус-сессии (помодоро + самоотчёт)
    if data == "focus:new":
        running = db.get_running_focus_session_db(user_id)
        if running:
            await query.answer(t(lang, "focus_already_running"), show_alert=True)
            return
        await query.answer()
        await safe_edit(query, t(lang, "focus_choose_duration"), kb_focus_duration(lang))
        return

    if data.startswith("focus:dur:"):
        value = data.split(":")[2]
        if value == "custom":
            await query.answer()
            user_state[user_id] = "waiting_for_focus_minutes"
            await safe_edit(query, t(lang, "focus_custom_prompt"))
            return
        running = db.get_running_focus_session_db(user_id)
        if running:
            await query.answer(t(lang, "focus_already_running"), show_alert=True)
            return
        await query.answer()
        await begin_focus_session(user_id, lang, int(value), context, query)
        return

    if data.startswith("focus:cancel:"):
        session_id = int(data.split(":")[2])
        session = db.get_focus_session_db(session_id)
        if session and session[1] == user_id and session[4] == "running":
            db.cancel_focus_session_db(session_id)
            for job in context.job_queue.get_jobs_by_name(f"focus_end_{session_id}"):
                job.schedule_removal()
            await query.answer(t(lang, "focus_cancelled"))
            await safe_edit(query, t(lang, "focus_cancelled"), kb_focus_menu(lang))
        else:
            await query.answer()
        return

    if data.startswith("focus:report:"):
        _, _, session_id_str, distracted_str = data.split(":")
        session_id = int(session_id_str)
        session = db.get_focus_session_db(session_id)
        if not session or session[1] != user_id or session[4] != "running":
            await query.answer(t(lang, "flow_expired"), show_alert=True)
            return
        distracted = distracted_str == "1"
        today = local_date_for(user_id)
        result = db.complete_focus_session_db(session_id, distracted, today)
        if result is None:
            await query.answer(t(lang, "flow_expired"), show_alert=True)
            return
        streak, best, is_new_best = result
        await query.answer()
        key = "focus_result_distracted" if distracted else "focus_result_focused"
        text = t(lang, key, streak=streak, best=best)
        if is_new_best:
            text += t(lang, "focus_new_best")
        await safe_edit(query, text, kb_focus_menu(lang))
        return

    # питание перед тренировкой
    if data == "food:start":
        await query.answer()
        await safe_edit(query, t(lang, "food_choose_time"), kb_food_time(lang))
        return

    if data.startswith("food:time:"):
        bracket = data.split(":")[2]
        await query.answer()
        text = t(lang, f"food_rec_{bracket}") + "\n\n" + t(lang, "food_disclaimer")
        await safe_edit(query, text, kb_food_result(lang))
        return

    await query.answer()


# СВОБОДНЫЙ ТЕКСТ

async def on_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text
    lang = get_lang(user_id)
    state = user_state.get(user_id)

    if state == "waiting_for_utc_offset":
        offset = parse_utc_offset(text)
        if offset is None:
            await update.message.reply_text(t(lang, "utc_offset_invalid"))
            return
        db.set_user_utc_offset(user_id, offset)
        user_state[user_id] = None
        await update.message.reply_text(t(lang, "utc_offset_set", offset=format_utc_offset(offset)))
        await update.message.reply_text(t(lang, "welcome_text"), reply_markup=kb_welcome(lang))
        return

    if state == "waiting_for_task_text":
        user_temp[user_id] = {"text": text}
        user_state[user_id] = None
        await update.message.reply_text(t(lang, "choose_category"), reply_markup=kb_category(lang))
        return

    if state == "waiting_for_habit_name":
        habit_id = db.add_habit_db(user_id, text)
        user_state[user_id] = None
        await update.message.reply_text(t(lang, "habit_added", name=text))
        await update.message.reply_text(
            t(lang, "ask_reminder", name=text),
            reply_markup=kb_reminder_ask(lang, habit_id),
        )
        return

    if state == "waiting_for_reminder_time":
        temp = user_temp.get(user_id, {})
        habit_id = temp.get("habit_id")
        if habit_id is None:
            user_state[user_id] = None
            await update.message.reply_text(t(lang, "flow_expired"))
            return

        match = TIME_RE.match(text.strip())
        if not match:
            await update.message.reply_text(t(lang, "reminder_invalid"))
            return

        time_str = text.strip()
        offset = db.get_user_utc_offset(user_id) or 0
        db.set_habit_reminder_db(habit_id, user_id, time_str)
        schedule_habit_job(context.job_queue, habit_id, user_id, time_str, offset)
        user_state[user_id] = None
        user_temp[user_id] = {}
        await update.message.reply_text(t(lang, "reminder_set", time=time_str, offset=format_utc_offset(offset)))
        habits_text, habits_kb = build_habits_screen(lang, user_id)
        await update.message.reply_text(habits_text, reply_markup=habits_kb)
        return

    if state == "waiting_for_focus_minutes":
        stripped = text.strip()
        if not stripped.isdigit() or not (FOCUS_MIN_MINUTES <= int(stripped) <= FOCUS_MAX_MINUTES):
            await update.message.reply_text(t(lang, "focus_custom_invalid"))
            return
        minutes = int(stripped)
        user_state[user_id] = None
        running = db.get_running_focus_session_db(user_id)
        if running:
            await update.message.reply_text(t(lang, "focus_already_running"))
            return
        await begin_focus_session(user_id, lang, minutes, context)
        return

    # нет активного состояния
    if db.get_user_language(user_id) is None:
        await update.message.reply_text(t(DEFAULT_LANG, "lang_picker_text"), reply_markup=kb_language())
        return
    if db.get_user_utc_offset(user_id) is None:
        user_state[user_id] = "waiting_for_utc_offset"
        await update.message.reply_text(t(lang, "utc_offset_prompt"))
        return
    await update.message.reply_text(t(lang, "welcome_text"), reply_markup=kb_welcome(lang))


# ЗАПУСК

async def post_init(application: Application):
    for habit_id, user_id, reminder_time, _name in db.get_all_reminders_db():
        offset = db.get_user_utc_offset(user_id) or 0
        schedule_habit_job(application.job_queue, habit_id, user_id, reminder_time, offset)

    # Восстановление фокус-таймеров 
    # время
    # самоотчёт 
    now = dt_datetime.utcnow()
    for session_id, user_id, duration_minutes, started_at in db.get_all_running_focus_sessions_db():
        started = dt_datetime.fromisoformat(started_at)
        remaining_seconds = (started + dt_timedelta(minutes=duration_minutes) - now).total_seconds()
        application.job_queue.run_once(
            focus_session_end,
            when=max(remaining_seconds, 1),
            name=f"focus_end_{session_id}",
            data={"session_id": session_id, "user_id": user_id},
        )

    await application.bot.set_my_commands([
        BotCommand("start", "Main screen / Главный экран"),
        BotCommand("tasks", "Tasks / Задачи"),
        BotCommand("habits", "Habits / Привычки"),
        BotCommand("focus", "Focus session / Фокус-сессия"),
        BotCommand("food", "Pre-workout food / Питание перед тренировкой"),
        BotCommand("timezone", "Time zone / Часовой пояс"),
        BotCommand("methodology", "Methodology / Методология"),
        BotCommand("language", "Change language / Сменить язык"),
        BotCommand("help", "Help / Помощь"),
    ])


def main():
    db.init_db()
    app = Application.builder().token(TOKEN).post_init(post_init).build()

    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("tasks", cmd_tasks))
    app.add_handler(CommandHandler("habits", cmd_habits))
    app.add_handler(CommandHandler("focus", cmd_focus))
    app.add_handler(CommandHandler("food", cmd_food))
    app.add_handler(CommandHandler("timezone", cmd_timezone))
    app.add_handler(CommandHandler("methodology", cmd_methodology))
    app.add_handler(CommandHandler("language", cmd_language))
    app.add_handler(CommandHandler("help", cmd_help))
    app.add_handler(CommandHandler("zh3pmfamily", kittens))
    app.add_handler(CallbackQueryHandler(on_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, on_text))

    print("Бот запущен...")
    app.run_polling()


if __name__ == "__main__":
    main()
