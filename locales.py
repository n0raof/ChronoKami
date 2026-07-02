# -*- coding: utf-8 -*-
DEFAULT_LANG = "ru"

LANG_NAMES = {
    "ru": "Русский",
    "en": "English",
    "kk": "Қазақша",
    "zh": "繁體中文",
    "ja": "日本語",
}

CATEGORY_EMOJI = {"study": "📚", "work": "💼", "home": "🏠", "other": "🎯"}
PRIORITY_EMOJI = {"high": "🔴", "medium": "🟡", "low": "🟢"}

L = {
    "ru": {
        "lang_picker_text": "Выберите язык интерфейса:",
        "welcome_text": (
            "Здравствуйте — это ChronoKami.\n"
            "Меньше шума, больше дела.\n"
            "Просто закинь сюда то, что нужно закрыть сегодня, "
            "или выбери привычку, которую давно откладываешь.\n"
            "Начнем?"
        ),
        "btn_make_task": "📌 Сделать задачу",
        "btn_level_habit": "🔥 Прокачать привычку",
        "btn_back": "⬅️ Назад",
        "btn_tasks_add": "➕ Добавить задачу",
        "btn_tasks_list": "📋 Показать задачи",
        "task_text_prompt": "Напиши текст задачи:",
        "choose_category": "Выбери категорию:",
        "cat_study": "Учёба", "cat_work": "Работа", "cat_home": "Дом", "cat_other": "Другое",
        "choose_priority": "Выбери приоритет:",
        "prio_high": "Высокий", "prio_medium": "Средний", "prio_low": "Низкий",
        "task_added": "Задача добавлена: {text} ✅",
        "tasks_header": "Твои задачи:",
        "no_tasks": "У тебя пока нет задач.",
        "task_marked_done": "Задача отмечена выполненной ✅",
        "task_deleted": "Задача удалена 🗑",
        "flow_expired": "Сессия сброшена, начни заново.",
        "btn_habits_add": "➕ Добавить привычку",
        "habits_header": "Твои привычки:",
        "no_habits": "У тебя пока нет привычек.",
        "habit_name_prompt": "Напиши название привычки:",
        "habit_added": "Привычка добавлена: {name} 🔥",
        "ask_reminder": "Поставить ежедневное напоминание для «{name}»?",
        "btn_yes": "Да", "btn_no": "Нет",
        "reminder_time_prompt": "Во сколько напоминать? Формат ЧЧ:ММ, 24ч, твоё локальное время ({offset}) (например 18:30):",
        "reminder_invalid": "Не понял время. Формат ЧЧ:ММ, например 09:00",
        "reminder_set": "Напоминание поставлено на {time} по твоему времени ({offset}) ⏰",
        "habit_already_done": "Сегодня уже отмечено ✅",
        "habit_marked_done": "Готово! Серия: {streak} 🔥",
        "reminder_push_text": "⏰ Напоминание: пора заняться привычкой «{name}». Текущая серия: {streak} 🔥",
        "btn_reminder_done": "✅ Сделано",
        "methodology_text": (
            "📖 Методология ChronoKami\n\n"
            "🔴🟡🟢 Приоритеты задач основаны на матрице Эйзенхауэра — "
            "разделении дел по срочности и важности, чтобы не путать «горит» и «важно».\n\n"
            "🔥 Серии (streaks) у привычек построены на кривой забывания Эббингауза: "
            "регулярные ежедневные касания закрепляют привычку в памяти лучше, "
            "чем редкие длинные сессии — поэтому бот напоминает каждый день, а не раз в неделю.\n\n"
            "🍅 Режим фокус-сессий на основе метода Помодоро: бот сам отсчитывает время, "
            "а по завершении сессии просит честный самоотчёт — отвлекались вы или нет. "
            "Автоматического «детекта» внимания здесь нет и не будет: без инвазивных датчиков "
            "(камера, трекинг экрана) такая штука недостоверна, поэтому мы выбрали таймер "
            "плюс рефлексию самим человеком.\n\n"
            "♿ Доступность: интерфейс построен только на тексте и стандартных кнопках Telegram, "
            "без изображений-кнопок и сложной вёрстки — это естественно совместимо со "
            "встроенными экранными дикторами телефона (TalkBack/VoiceOver)."
        ),
        "help_text": (
            "/tasks — задачи\n/habits — привычки\n/focus — фокус-сессия (Помодоро)\n"
            "/food — питание перед тренировкой\n/timezone — часовой пояс\n"
            "/methodology — методология\n/language — сменить язык\n/start — главный экран"
        ),
        "btn_methodology": "📖 Методология",
        "language_changed": "Язык переключён ✅",

        "btn_focus": "🎯 Фокус-сессия",
        "btn_food": "🍽 Питание перед тренировкой",
        "btn_timezone": "🌐 Часовой пояс",
        "utc_offset_prompt": (
            "Укажи свой часовой пояс, чтобы напоминания и таймеры приходили вовремя.\n"
            "Формат: UTC±ЧЧ или UTC±ЧЧ:ММ, например UTC+5 (Астана) или UTC+3 (Москва):"
        ),
        "utc_offset_invalid": "Не понял часовой пояс. Формат: UTC+5, +5, -3 или +5:30.",
        "utc_offset_set": "Часовой пояс сохранён: {offset} ✅",
        "focus_intro_text": (
            "🍅 Фокус-сессия (Помодоро)\n\n"
            "Бот сам ведёт таймер, а по завершении честно спросит: отвлекался ты или нет. "
            "Никакого автоматического «детекта» — только твой самоотчёт.\n\n"
            "🔥 Серия: {streak} дн. (лучшая: {best})"
        ),
        "btn_focus_start": "▶️ Начать сессию",
        "focus_choose_duration": "Сколько минут длится сессия?",
        "btn_focus_custom": "✏️ Свой вариант",
        "focus_custom_prompt": "Введи длительность в минутах (целое число от 1 до 180):",
        "focus_custom_invalid": "Нужно целое число минут от 1 до 180.",
        "focus_already_running": "У тебя уже идёт фокус-сессия. Дождись её конца или отмени текущую.",
        "focus_started": (
            "🍅 Сессия началась: {minutes} мин. Бот сам последит за временем — "
            "просто занимайся делом, и я напомню, когда пора закончить."
        ),
        "btn_focus_cancel": "❌ Отменить сессию",
        "focus_cancelled": "Сессия отменена.",
        "focus_end_text": "⏰ Время вышло! Отвлекался(-ась) ты во время сессии?",
        "btn_distracted_no": "🙂 Нет, был(а) сфокусирован(а)",
        "btn_distracted_yes": "📵 Да, отвлекался(-лась)",
        "focus_result_focused": "Отлично, без отвлечений! 🔥 Серия: {streak} дн. (лучшая: {best})",
        "focus_result_distracted": "Записал, бывает — попытка всё равно засчитана. 🔥 Серия: {streak} дн. (лучшая: {best})",
        "focus_new_best": " Это новый рекорд! 🏆",
        "food_choose_time": "🍽 Через сколько у тебя тренировка?",
        "btn_food_lt30": "⏱ Меньше 30 минут",
        "btn_food_30_60": "⏱ 30–60 минут",
        "btn_food_1_2h": "⏱ 1–2 часа",
        "btn_food_gt2h": "⏱ Больше 2 часов",
        "food_rec_lt30": (
            "🍌 Меньше 30 минут до тренировки — время только для быстрых углеводов: "
            "банан, немного мёда или сухофруктов, спортивный напиток. Белок и жир сейчас "
            "не успеют перевариться и могут дать тяжесть в желудке."
        ),
        "food_rec_30_60": (
            "🍞 30–60 минут — лёгкий перекус: быстрые углеводы и совсем немного белка. "
            "Тост с мёдом, йогурт, банан с ложкой арахисовой пасты."
        ),
        "food_rec_1_2h": (
            "🍚 1–2 часа — можно полноценнее: углеводы + умеренно белка, немного жира. "
            "Например, овсянка с фруктами, рис с курицей, омлет с тостом."
        ),
        "food_rec_gt2h": (
            "🍝 Больше 2 часов — обычный сбалансированный приём пищи: сложные углеводы, "
            "белок, овощи, немного жира. Паста с нежирным мясом, рис с рыбой и овощами."
        ),
        "food_disclaimer": (
            "Это общие ориентиры, а не индивидуальный план питания. При хронических "
            "заболеваниях, особом рационе или под наблюдением врача — сверяйся со специалистом."
        ),
    },

    "en": {
        "lang_picker_text": "Choose your interface language:",
        "welcome_text": (
            "Hello — this is ChronoKami.\n"
            "Less noise, more action.\n"
            "Just drop in whatever needs to get done today, "
            "or pick a habit you've been putting off.\n"
            "Shall we begin?"
        ),
        "btn_make_task": "📌 Make a task",
        "btn_level_habit": "🔥 Level up a habit",
        "btn_back": "⬅️ Back",
        "btn_tasks_add": "➕ Add task",
        "btn_tasks_list": "📋 Show tasks",
        "task_text_prompt": "Type the task text:",
        "choose_category": "Choose a category:",
        "cat_study": "Study", "cat_work": "Work", "cat_home": "Home", "cat_other": "Other",
        "choose_priority": "Choose a priority:",
        "prio_high": "High", "prio_medium": "Medium", "prio_low": "Low",
        "task_added": "Task added: {text} ✅",
        "tasks_header": "Your tasks:",
        "no_tasks": "You don't have any tasks yet.",
        "task_marked_done": "Task marked as done ✅",
        "task_deleted": "Task deleted 🗑",
        "flow_expired": "Session was reset, please start again.",
        "btn_habits_add": "➕ Add habit",
        "habits_header": "Your habits:",
        "no_habits": "You don't have any habits yet.",
        "habit_name_prompt": "Type the habit name:",
        "habit_added": "Habit added: {name} 🔥",
        "ask_reminder": "Set a daily reminder for \"{name}\"?",
        "btn_yes": "Yes", "btn_no": "No",
        "reminder_time_prompt": "What time? Format HH:MM, 24h, your local time ({offset}) (e.g. 18:30):",
        "reminder_invalid": "Couldn't parse that time. Format HH:MM, e.g. 09:00",
        "reminder_set": "Reminder set for {time} your time ({offset}) ⏰",
        "habit_already_done": "Already logged for today ✅",
        "habit_marked_done": "Nice! Streak: {streak} 🔥",
        "reminder_push_text": "⏰ Reminder: time for your habit \"{name}\". Current streak: {streak} 🔥",
        "btn_reminder_done": "✅ Done",
        "methodology_text": (
            "📖 ChronoKami methodology\n\n"
            "🔴🟡🟢 Task priorities are based on the Eisenhower Matrix — "
            "splitting tasks by urgency and importance so \"urgent\" and \"important\" don't get confused.\n\n"
            "🔥 Habit streaks are built on Ebbinghaus's forgetting curve: "
            "frequent, short daily touches reinforce a habit far better than rare long sessions — "
            "that's why the bot nudges you daily, not weekly.\n\n"
            "🍅 Pomodoro-based focus sessions: the bot runs the timer itself, and at the end asks "
            "for an honest self-report — were you distracted or not. There's no automatic attention "
            "\"detection\" here, by design: without invasive sensors (camera, screen tracking) that "
            "kind of detection isn't trustworthy, so we chose a timer plus the person's own reflection instead.\n\n"
            "♿ Accessibility: the interface is built entirely from plain text and standard Telegram "
            "buttons, with no image-based buttons or complex layouts — this is naturally compatible "
            "with phone screen readers (TalkBack/VoiceOver)."
        ),
        "help_text": (
            "/tasks — tasks\n/habits — habits\n/focus — focus session (Pomodoro)\n"
            "/food — pre-workout food\n/timezone — time zone\n"
            "/methodology — methodology\n/language — change language\n/start — main screen"
        ),
        "btn_methodology": "📖 Methodology",
        "language_changed": "Language switched ✅",

        "btn_focus": "🎯 Focus session",
        "btn_food": "🍽 Pre-workout food",
        "btn_timezone": "🌐 Time zone",
        "utc_offset_prompt": (
            "Tell me your time zone so reminders and timers land at the right time.\n"
            "Format: UTC±HH or UTC±HH:MM, e.g. UTC+5 (Astana) or UTC+3 (Moscow):"
        ),
        "utc_offset_invalid": "Couldn't parse that time zone. Format: UTC+5, +5, -3, or +5:30.",
        "utc_offset_set": "Time zone saved: {offset} ✅",
        "focus_intro_text": (
            "🍅 Focus session (Pomodoro)\n\n"
            "The bot runs the timer itself, and at the end honestly asks: were you distracted "
            "or not. No automatic \"detection\" — just your own self-report.\n\n"
            "🔥 Streak: {streak} day(s) (best: {best})"
        ),
        "btn_focus_start": "▶️ Start session",
        "focus_choose_duration": "How many minutes should the session last?",
        "btn_focus_custom": "✏️ Custom",
        "focus_custom_prompt": "Enter the duration in minutes (a whole number from 1 to 180):",
        "focus_custom_invalid": "Needs to be a whole number of minutes, from 1 to 180.",
        "focus_already_running": "You already have a focus session running. Wait for it to finish or cancel it.",
        "focus_started": (
            "🍅 Session started: {minutes} min. The bot will keep track of the time — "
            "just get to work, I'll ping you when it's time to stop."
        ),
        "btn_focus_cancel": "❌ Cancel session",
        "focus_cancelled": "Session cancelled.",
        "focus_end_text": "⏰ Time's up! Did you get distracted during the session?",
        "btn_distracted_no": "🙂 No, stayed focused",
        "btn_distracted_yes": "📵 Yes, got distracted",
        "focus_result_focused": "Nice, no distractions! 🔥 Streak: {streak} day(s) (best: {best})",
        "focus_result_distracted": "Logged — happens to everyone, the session still counts. 🔥 Streak: {streak} day(s) (best: {best})",
        "focus_new_best": " That's a new record! 🏆",
        "food_choose_time": "🍽 How long until your workout?",
        "btn_food_lt30": "⏱ Less than 30 min",
        "btn_food_30_60": "⏱ 30–60 min",
        "btn_food_1_2h": "⏱ 1–2 hours",
        "btn_food_gt2h": "⏱ More than 2 hours",
        "food_rec_lt30": (
            "🍌 Under 30 minutes to go — stick to fast carbs only: a banana, a bit of honey "
            "or dried fruit, a sports drink. Protein and fat won't digest in time and can "
            "leave you feeling heavy."
        ),
        "food_rec_30_60": (
            "🍞 30–60 minutes — a light snack: fast carbs with just a little protein. "
            "Toast with honey, yogurt, a banana with a spoon of peanut butter."
        ),
        "food_rec_1_2h": (
            "🍚 1–2 hours — you can go a bit fuller: carbs plus moderate protein, a little fat. "
            "Think oatmeal with fruit, rice with chicken, or eggs on toast."
        ),
        "food_rec_gt2h": (
            "🍝 More than 2 hours — a regular balanced meal works: complex carbs, protein, "
            "vegetables, a little fat. Pasta with lean meat, or rice with fish and vegetables."
        ),
        "food_disclaimer": (
            "These are general pointers, not a personalized nutrition plan. If you have a "
            "chronic condition or a specific diet, check with a doctor or dietitian."
        ),
    },

    "kk": {
        "lang_picker_text": "Интерфейс тілін таңдаңыз:",
        "welcome_text": (
            "Сәлеметсіз бе — бұл ChronoKami.\n"
            "Шу аз, іс көп.\n"
            "Бүгін аяқтау керек нәрсені осында тастаңыз, "
            "немесе ұзақ кейінге қалдырып жүрген әдетіңізді таңдаңыз.\n"
            "Бастайық па?"
        ),
        "btn_make_task": "📌 Тапсырма жасау",
        "btn_level_habit": "🔥 Әдетті дамыту",
        "btn_back": "⬅️ Артқа",
        "btn_tasks_add": "➕ Тапсырма қосу",
        "btn_tasks_list": "📋 Тапсырмаларды көрсету",
        "task_text_prompt": "Тапсырма мәтінін жазыңыз:",
        "choose_category": "Санатты таңдаңыз:",
        "cat_study": "Оқу", "cat_work": "Жұмыс", "cat_home": "Үй", "cat_other": "Басқа",
        "choose_priority": "Басымдықты таңдаңыз:",
        "prio_high": "Жоғары", "prio_medium": "Орташа", "prio_low": "Төмен",
        "task_added": "Тапсырма қосылды: {text} ✅",
        "tasks_header": "Сіздің тапсырмаларыңыз:",
        "no_tasks": "Әзірге тапсырмалар жоқ.",
        "task_marked_done": "Тапсырма орындалды деп белгіленді ✅",
        "task_deleted": "Тапсырма жойылды 🗑",
        "flow_expired": "Сессия тазаланды, қайта бастаңыз.",
        "btn_habits_add": "➕ Әдет қосу",
        "habits_header": "Сіздің әдеттеріңіз:",
        "no_habits": "Әзірге әдеттер жоқ.",
        "habit_name_prompt": "Әдеттің атауын жазыңыз:",
        "habit_added": "Әдет қосылды: {name} 🔥",
        "ask_reminder": "«{name}» үшін күнделікті еске салғыш қоясыз ба?",
        "btn_yes": "Иә", "btn_no": "Жоқ",
        "reminder_time_prompt": "Сағат нешеде еске салу керек? Формат СС:ММ, 24сағ, жергілікті уақытыңыз ({offset}) (мысалы 18:30):",
        "reminder_invalid": "Уақыт танылмады. Формат СС:ММ, мысалы 09:00",
        "reminder_set": "Еске салғыш сіздің уақытыңызша {time} ({offset}) уақытына қойылды ⏰",
        "habit_already_done": "Бүгін үшін бұрын белгіленген ✅",
        "habit_marked_done": "Керемет! Сериясы: {streak} 🔥",
        "reminder_push_text": "⏰ Еске салу: «{name}» әдетін орындау уақыты. Ағымдағы серия: {streak} 🔥",
        "btn_reminder_done": "✅ Орындалды",
        "methodology_text": (
            "📖 ChronoKami әдістемесі\n\n"
            "🔴🟡🟢 Тапсырма басымдықтары Эйзенхауэр матрицасына негізделген — "
            "істерді шұғылдығы мен маңыздылығына қарай бөлу, «жанып тұр» мен «маңызды» шатаспас үшін.\n\n"
            "🔥 Әдеттердің сериялары Эббингауздың ұмыту қисығына негізделген: "
            "сирек ұзақ сессиялардан гөрі жиі әрі қысқа күнделікті қайталау әдетті есте жақсырақ бекітеді — "
            "сондықтан бот аптасына емес, күн сайын еске салады.\n\n"
            "🍅 Pomodoro әдісіне негізделген фокус-сессия режимі: бот уақытты өзі санайды, "
            "ал сессия аяқталған соң адал өзін-өзі бағалауды сұрайды — назарыңыз бөлінді ме, жоқ па. "
            "Мұнда назарды автоматты түрде «анықтау» жоқ және болмайды да: инвазивті сенсорларсыз "
            "(камера, экранды бақылау) мұндай анықтау сенімсіз болар еді, сондықтан біз таймер "
            "плюс адамның өзін-өзі бағалауын таңдадық.\n\n"
            "♿ Қолжетімділік: интерфейс тек мәтін мен стандартты Telegram түймелерінен тұрады, "
            "сурет-түймелер мен күрделі макет жоқ — бұл телефондағы экран дикторларымен "
            "(TalkBack/VoiceOver) табиғи түрде үйлесімді."
        ),
        "help_text": (
            "/tasks — тапсырмалар\n/habits — әдеттер\n/focus — фокус-сессия (Pomodoro)\n"
            "/food — жаттығу алдындағы тамақтану\n/timezone — уақыт белдеуі\n"
            "/methodology — әдістеме\n/language — тілді ауыстыру\n/start — басты экран"
        ),
        "btn_methodology": "📖 Әдістеме",
        "language_changed": "Тіл ауыстырылды ✅",

        "btn_focus": "🎯 Фокус-сессия",
        "btn_food": "🍽 Жаттығу алдындағы тамақтану",
        "btn_timezone": "🌐 Уақыт белдеуі",
        "utc_offset_prompt": (
            "Еске салғыштар мен таймерлер уақытында келуі үшін уақыт белдеуіңізді көрсетіңіз.\n"
            "Формат: UTC±СС немесе UTC±СС:ММ, мысалы UTC+5 (Астана) немесе UTC+3 (Мәскеу):"
        ),
        "utc_offset_invalid": "Уақыт белдеуі танылмады. Формат: UTC+5, +5, -3 немесе +5:30.",
        "utc_offset_set": "Уақыт белдеуі сақталды: {offset} ✅",
        "focus_intro_text": (
            "🍅 Фокус-сессия (Pomodoro)\n\n"
            "Бот таймерді өзі жүргізеді, ал соңында адал сұрайды: назарыңыз бөлінді ме, жоқ па. "
            "Автоматты «анықтау» жоқ — тек сіздің өзіңіздің есебіңіз.\n\n"
            "🔥 Серия: {streak} күн (үздігі: {best})"
        ),
        "btn_focus_start": "▶️ Сессияны бастау",
        "focus_choose_duration": "Сессия неше минутқа созылады?",
        "btn_focus_custom": "✏️ Өз нұсқасы",
        "focus_custom_prompt": "Минут санын енгізіңіз (1-ден 180-ге дейінгі бүтін сан):",
        "focus_custom_invalid": "1-ден 180-ге дейінгі бүтін сан керек.",
        "focus_already_running": "Сізде қазірдің өзінде фокус-сессия жүріп жатыр. Аяқталғанын күтіңіз немесе оны тоқтатыңыз.",
        "focus_started": (
            "🍅 Сессия басталды: {minutes} мин. Бот уақытты өзі қадағалайды — "
            "жұмысыңызбен айналыса беріңіз, аяқтау уақыты келгенде хабарлаймын."
        ),
        "btn_focus_cancel": "❌ Сессияны тоқтату",
        "focus_cancelled": "Сессия тоқтатылды.",
        "focus_end_text": "⏰ Уақыт бітті! Сессия кезінде назарыңыз бөлінді ме?",
        "btn_distracted_no": "🙂 Жоқ, зейінім бір жерде болды",
        "btn_distracted_yes": "📵 Иә, назарым бөлінді",
        "focus_result_focused": "Керемет, назар бөлінген жоқ! 🔥 Серия: {streak} күн (үздігі: {best})",
        "focus_result_distracted": "Белгіледім, бәрі болады — сессия бәрібір есептелді. 🔥 Серия: {streak} күн (үздігі: {best})",
        "focus_new_best": " Бұл жаңа рекорд! 🏆",
        "food_choose_time": "🍽 Жаттығуға дейін қанша уақыт қалды?",
        "btn_food_lt30": "⏱ 30 минуттан аз",
        "btn_food_30_60": "⏱ 30–60 минут",
        "btn_food_1_2h": "⏱ 1–2 сағат",
        "btn_food_gt2h": "⏱ 2 сағаттан көп",
        "food_rec_lt30": (
            "🍌 Жаттығуға 30 минуттан аз қалды — тек жылдам көмірсулар: банан, аздап бал немесе "
            "кептірілген жеміс, спорттық сусын. Ақуыз бен май қазір қорытылмай, ауырлық сезімін тудыруы мүмкін."
        ),
        "food_rec_30_60": (
            "🍞 30–60 минут — жеңіл тағамдану: жылдам көмірсулар және өте аз ақуыз. "
            "Балы бар тост, йогурт, бір қасық жержаңғақ майы бар банан."
        ),
        "food_rec_1_2h": (
            "🍚 1–2 сағат — толығырақ болуы мүмкін: көмірсулар + орташа ақуыз, аздап май. "
            "Мысалы, жемісі бар сұлы ботқасы, тауық еті бар күріш, тосты бар омлет."
        ),
        "food_rec_gt2h": (
            "🍝 2 сағаттан көп — әдеттегі теңгерімді тағамдану: күрделі көмірсулар, ақуыз, "
            "көкөністер, аздап май. Майсыз етпен паста немесе балық пен көкөністі күріш."
        ),
        "food_disclaimer": (
            "Бұл жалпы бағдар, жеке тамақтану жоспары емес. Созылмалы аурулар немесе арнайы "
            "диета болса — маманмен (дәрігермен немесе диетологпен) кеңесіңіз."
        ),
    },

    "zh": {
        "lang_picker_text": "請選擇介面語言：",
        "welcome_text": (
            "你好 — 這裡是 ChronoKami。\n"
            "少一些喧囂，多一些行動。\n"
            "把今天要完成的事情丟在這裡，或者選一個你一直拖延的習慣。\n"
            "我們開始吧？"
        ),
        "btn_make_task": "📌 建立任務",
        "btn_level_habit": "🔥 升級習慣",
        "btn_back": "⬅️ 返回",
        "btn_tasks_add": "➕ 新增任務",
        "btn_tasks_list": "📋 顯示任務",
        "task_text_prompt": "請輸入任務內容：",
        "choose_category": "請選擇分類：",
        "cat_study": "學習", "cat_work": "工作", "cat_home": "家庭", "cat_other": "其他",
        "choose_priority": "請選擇優先級：",
        "prio_high": "高", "prio_medium": "中", "prio_low": "低",
        "task_added": "任務已新增：{text} ✅",
        "tasks_header": "你的任務：",
        "no_tasks": "目前還沒有任務。",
        "task_marked_done": "任務已標記為完成 ✅",
        "task_deleted": "任務已刪除 🗑",
        "flow_expired": "工作階段已重置，請重新開始。",
        "btn_habits_add": "➕ 新增習慣",
        "habits_header": "你的習慣：",
        "no_habits": "目前還沒有習慣。",
        "habit_name_prompt": "請輸入習慣名稱：",
        "habit_added": "習慣已新增：{name} 🔥",
        "ask_reminder": "要為「{name}」設定每日提醒嗎？",
        "btn_yes": "是", "btn_no": "否",
        "reminder_time_prompt": "想在幾點提醒？格式 HH:MM，24小時制，你的當地時間（{offset}）（例如 18:30）：",
        "reminder_invalid": "無法辨識時間，格式為 HH:MM，例如 09:00",
        "reminder_set": "提醒已設定為你的當地時間 {time}（{offset}）⏰",
        "habit_already_done": "今天已經記錄過了 ✅",
        "habit_marked_done": "太棒了！連續天數：{streak} 🔥",
        "reminder_push_text": "⏰ 提醒：該執行習慣「{name}」了。目前連續天數：{streak} 🔥",
        "btn_reminder_done": "✅ 已完成",
        "methodology_text": (
            "📖 ChronoKami 方法論\n\n"
            "🔴🟡🟢 任務優先級基於艾森豪矩陣（Eisenhower Matrix）——"
            "依緊急程度與重要程度區分事務，避免把「緊急」與「重要」混為一談。\n\n"
            "🔥 習慣的連續天數機制基於艾賓浩斯遺忘曲線："
            "頻繁的每日短時互動，比偶爾的長時間練習更能鞏固習慣記憶——"
            "這也是為什麼機器人每天提醒，而不是每週提醒一次。\n\n"
            "🍅 基於番茄工作法的專注模式：機器人會自行倒數計時，並在結束時請你誠實自我回報"
            "——是否分心了。這裡沒有、也不會有自動「偵測」專注力的功能：沒有攝影機、螢幕追蹤"
            "等侵入式手段，這類偵測並不可靠，因此我們選擇了計時器加上使用者自我反思的方式。\n\n"
            "♿ 無障礙設計：介面完全由純文字與 Telegram 標準按鈕構成，"
            "不使用圖片按鈕或複雜版面——這天然地與手機內建的螢幕報讀器"
            "（TalkBack/VoiceOver）相容。"
        ),
        "help_text": (
            "/tasks — 任務\n/habits — 習慣\n/focus — 專注模式（番茄鐘）\n"
            "/food — 運動前飲食建議\n/timezone — 時區設定\n"
            "/methodology — 方法論\n/language — 切換語言\n/start — 主畫面"
        ),
        "btn_methodology": "📖 方法論",
        "language_changed": "語言已切換 ✅",

        "btn_focus": "🎯 專注模式",
        "btn_food": "🍽 運動前飲食建議",
        "btn_timezone": "🌐 時區設定",
        "utc_offset_prompt": (
            "請告訴我你的時區，這樣提醒和計時器才能準時送達。\n"
            "格式：UTC±HH 或 UTC±HH:MM，例如 UTC+5（阿斯塔納）或 UTC+8（台北）："
        ),
        "utc_offset_invalid": "無法辨識時區，格式為 UTC+5、+5、-3 或 +5:30。",
        "utc_offset_set": "時區已儲存：{offset} ✅",
        "focus_intro_text": (
            "🍅 專注模式（番茄鐘）\n\n"
            "機器人會自行倒數計時，結束時誠實地問你：有沒有分心。這裡沒有自動「偵測」"
            "——只有你自己的回報。\n\n"
            "🔥 連續天數：{streak} 天（最佳：{best}）"
        ),
        "btn_focus_start": "▶️ 開始專注",
        "focus_choose_duration": "這次專注要進行幾分鐘？",
        "btn_focus_custom": "✏️ 自訂",
        "focus_custom_prompt": "請輸入分鐘數（1 到 180 之間的整數）：",
        "focus_custom_invalid": "需要輸入 1 到 180 之間的整數分鐘數。",
        "focus_already_running": "你已經有一個進行中的專注階段，請等它結束或取消目前的階段。",
        "focus_started": (
            "🍅 專注開始：{minutes} 分鐘。機器人會自己記錄時間"
            "——安心去做事，時間到了我會提醒你。"
        ),
        "btn_focus_cancel": "❌ 取消階段",
        "focus_cancelled": "已取消專注階段。",
        "focus_end_text": "⏰ 時間到了！這段時間你有分心嗎？",
        "btn_distracted_no": "🙂 沒有，全程專注",
        "btn_distracted_yes": "📵 有，分心了",
        "focus_result_focused": "太棒了，完全沒分心！🔥 連續天數：{streak} 天（最佳：{best}）",
        "focus_result_distracted": "記錄下來了，難免會有分心——這次還是算數。🔥 連續天數：{streak} 天（最佳：{best}）",
        "focus_new_best": " 這是新紀錄！🏆",
        "food_choose_time": "🍽 距離運動還有多久？",
        "btn_food_lt30": "⏱ 少於 30 分鐘",
        "btn_food_30_60": "⏱ 30–60 分鐘",
        "btn_food_1_2h": "⏱ 1–2 小時",
        "btn_food_gt2h": "⏱ 超過 2 小時",
        "food_rec_lt30": (
            "🍌 距離運動不到 30 分鐘——只適合快速碳水化合物：香蕉、少量蜂蜜或果乾、運動飲料。"
            "蛋白質和脂肪這時候來不及消化，容易造成腸胃不適。"
        ),
        "food_rec_30_60": (
            "🍞 30–60 分鐘——輕食即可：快速碳水化合物加上一點點蛋白質。"
            "塗蜂蜜的吐司、優格，或香蕉配一匙花生醬。"
        ),
        "food_rec_1_2h": (
            "🍚 1–2 小時——可以吃得完整一些：碳水化合物加適量蛋白質，少量脂肪。"
            "例如燕麥配水果、雞肉配飯，或吐司配蛋。"
        ),
        "food_rec_gt2h": (
            "🍝 超過 2 小時——一般均衡的一餐就好：複合碳水化合物、蛋白質、蔬菜、少量脂肪。"
            "像是義大利麵配瘦肉，或魚肉配蔬菜與米飯。"
        ),
        "food_disclaimer": (
            "這只是一般性建議，不是個人化的飲食計畫。若有慢性疾病或特殊飲食需求，"
            "請諮詢醫師或營養師。"
        ),
    },

    "ja": {
        "lang_picker_text": "インターフェース言語を選んでください：",
        "welcome_text": (
            "こんにちは — ChronoKamiです。\n"
            "雑音は少なく、行動は多く。\n"
            "今日中に片付けたいことをここに書くか、"
            "ずっと先延ばしにしている習慣を選んでください。\n"
            "始めましょうか？"
        ),
        "btn_make_task": "📌 タスクを作成",
        "btn_level_habit": "🔥 習慣をレベルアップ",
        "btn_back": "⬅️ 戻る",
        "btn_tasks_add": "➕ タスクを追加",
        "btn_tasks_list": "📋 タスクを表示",
        "task_text_prompt": "タスクの内容を入力してください：",
        "choose_category": "カテゴリを選んでください：",
        "cat_study": "勉強", "cat_work": "仕事", "cat_home": "家事", "cat_other": "その他",
        "choose_priority": "優先度を選んでください：",
        "prio_high": "高", "prio_medium": "中", "prio_low": "低",
        "task_added": "タスクを追加しました：{text} ✅",
        "tasks_header": "あなたのタスク：",
        "no_tasks": "まだタスクがありません。",
        "task_marked_done": "タスクを完了にしました ✅",
        "task_deleted": "タスクを削除しました 🗑",
        "flow_expired": "セッションがリセットされました。もう一度お試しください。",
        "btn_habits_add": "➕ 習慣を追加",
        "habits_header": "あなたの習慣：",
        "no_habits": "まだ習慣がありません。",
        "habit_name_prompt": "習慣の名前を入力してください：",
        "habit_added": "習慣を追加しました：{name} 🔥",
        "ask_reminder": "「{name}」の毎日のリマインダーを設定しますか？",
        "btn_yes": "はい", "btn_no": "いいえ",
        "reminder_time_prompt": "何時に通知しますか？形式 HH:MM、24時間制、あなたの現地時間（{offset}）（例 18:30）：",
        "reminder_invalid": "時刻を認識できませんでした。形式は HH:MM、例えば 09:00",
        "reminder_set": "リマインダーをあなたの現地時間 {time}（{offset}）に設定しました ⏰",
        "habit_already_done": "今日はすでに記録済みです ✅",
        "habit_marked_done": "いいですね！連続記録：{streak} 🔥",
        "reminder_push_text": "⏰ リマインダー：習慣「{name}」の時間です。現在の連続記録：{streak} 🔥",
        "btn_reminder_done": "✅ 完了",
        "methodology_text": (
            "📖 ChronoKami のメソドロジー\n\n"
            "🔴🟡🟢 タスクの優先度はアイゼンハワー・マトリクスに基づいています。"
            "緊急度と重要度でタスクを分け、「緊急」と「重要」を混同しないようにします。\n\n"
            "🔥 習慣のストリーク（連続記録）はエビングハウスの忘却曲線に基づいています。"
            "稀に長時間取り組むより、毎日短く繰り返すほうが習慣が記憶に定着しやすいため、"
            "ボットは週1回ではなく毎日リマインドします。\n\n"
            "🍅 ポモドーロ・テクニックに基づく集中セッション機能：ボット自身がタイマーを管理し、"
            "セッション終了時に正直な自己申告（セルフレポート）を求めます——集中できたか、"
            "気が散ったか。カメラや画面トラッキングのような侵襲的な手段なしに注意力を自動で"
            "「検知」することはできないため、ここでは自動検知は行いません。タイマーと本人の"
            "振り返りによる、誠実な方式を選んでいます。\n\n"
            "♿ アクセシビリティ：インターフェースはテキストと標準のTelegramボタンのみで構成され、"
            "画像ボタンや複雑なレイアウトを使用していません。そのためスマートフォンの"
            "スクリーンリーダー（TalkBack/VoiceOver）と自然に親和性があります。"
        ),
        "help_text": (
            "/tasks — タスク\n/habits — 習慣\n/focus — 集中セッション（ポモドーロ）\n"
            "/food — 運動前の食事アドバイス\n/timezone — タイムゾーン\n"
            "/methodology — メソドロジー\n/language — 言語を変更\n/start — メイン画面"
        ),
        "btn_methodology": "📖 メソドロジー",
        "language_changed": "言語を切り替えました ✅",

        "btn_focus": "🎯 集中セッション",
        "btn_food": "🍽 運動前の食事アドバイス",
        "btn_timezone": "🌐 タイムゾーン",
        "utc_offset_prompt": (
            "リマインダーやタイマーが正しい時間に届くように、タイムゾーンを教えてください。\n"
            "形式：UTC±HH または UTC±HH:MM。例：UTC+5（アスタナ）、UTC+9（東京）："
        ),
        "utc_offset_invalid": "タイムゾーンを認識できませんでした。形式は UTC+5、+5、-3、+5:30 などです。",
        "utc_offset_set": "タイムゾーンを保存しました：{offset} ✅",
        "focus_intro_text": (
            "🍅 集中セッション（ポモドーロ）\n\n"
            "ボット自身がタイマーを管理し、終了時に正直に尋ねます：気が散りましたか、集中"
            "できましたか。自動検知は行いません——あなた自身の自己申告のみです。\n\n"
            "🔥 連続記録：{streak} 日（最高：{best}）"
        ),
        "btn_focus_start": "▶️ セッション開始",
        "focus_choose_duration": "セッションは何分にしますか？",
        "btn_focus_custom": "✏️ カスタム",
        "focus_custom_prompt": "分数を入力してください（1〜180の整数）：",
        "focus_custom_invalid": "1〜180の整数（分）を入力してください。",
        "focus_already_running": "すでに進行中の集中セッションがあります。終了を待つか、キャンセルしてください。",
        "focus_started": (
            "🍅 セッション開始：{minutes} 分。時間はボットが管理します"
            "——安心して作業に集中してください。終了時間になったらお知らせします。"
        ),
        "btn_focus_cancel": "❌ セッションをキャンセル",
        "focus_cancelled": "セッションをキャンセルしました。",
        "focus_end_text": "⏰ 時間になりました！セッション中、気が散りましたか？",
        "btn_distracted_no": "🙂 いいえ、集中できました",
        "btn_distracted_yes": "📵 はい、気が散りました",
        "focus_result_focused": "素晴らしい、集中できましたね！🔥 連続記録：{streak} 日（最高：{best}）",
        "focus_result_distracted": "記録しました。よくあることです、セッションはカウントされます。🔥 連続記録：{streak} 日（最高：{best}）",
        "focus_new_best": " 新記録です！🏆",
        "food_choose_time": "🍽 運動まであとどれくらいですか？",
        "btn_food_lt30": "⏱ 30分未満",
        "btn_food_30_60": "⏱ 30〜60分",
        "btn_food_1_2h": "⏱ 1〜2時間",
        "btn_food_gt2h": "⏱ 2時間以上",
        "food_rec_lt30": (
            "🍌 運動まで30分未満——速く消化する糖質だけにしましょう。バナナ、少量のはちみつや"
            "ドライフルーツ、スポーツドリンクなど。タンパク質や脂質は消化が間に合わず、"
            "胃もたれの原因になります。"
        ),
        "food_rec_30_60": (
            "🍞 30〜60分——軽めの軽食を。速く消化する糖質に、ほんの少しタンパク質を加えたもの"
            "が良いでしょう。はちみつトースト、ヨーグルト、バナナに少量のピーナッツバターなど。"
        ),
        "food_rec_1_2h": (
            "🍚 1〜2時間——もう少ししっかり食べても大丈夫です。糖質＋適量のタンパク質、少量の"
            "脂質。フルーツ入りオートミール、鶏肉入りご飯、トーストと卵など。"
        ),
        "food_rec_gt2h": (
            "🍝 2時間以上——普段どおりのバランスの良い食事で問題ありません。複合糖質、"
            "タンパク質、野菜、少量の脂質。赤身肉のパスタや、魚と野菜を添えたご飯など。"
        ),
        "food_disclaimer": (
            "これは一般的な目安であり、個別の栄養プランではありません。持病がある場合や"
            "特別な食事制限がある場合は、医師や管理栄養士に相談してください。"
        ),
    },
}


def t(lang, key, **kwargs):
    table = L.get(lang, L[DEFAULT_LANG])
    template = table.get(key, L[DEFAULT_LANG].get(key, key))
    return template.format(**kwargs) if kwargs else template
