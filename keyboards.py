from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton


def main_keyboard():
    # Keyboard Main
    button_profile = KeyboardButton('Профиль')
    button_table = KeyboardButton('Расписание')
    button_score = KeyboardButton('Рейтинг')
    button_activity = KeyboardButton('Активность дня')
    button_logout = KeyboardButton("Разлогиниться")
    main_kb = ReplyKeyboardMarkup(resize_keyboard=True)
    main_kb.row(button_profile, button_table)
    main_kb.row(button_score, button_activity)
    main_kb.add(button_logout)
    return main_kb


def reg_keyboard():
    button_reg = KeyboardButton("Регистрация")
    reg_kb = ReplyKeyboardMarkup()
    reg_kb.add(button_reg)
    return reg_kb


def admin_kb():
    adm_kb = main_keyboard()
    button_echo = KeyboardButton('Рассылка')
    button_money = KeyboardButton('Редактор денег')
    adm_kb.row(button_echo, button_money)
    return adm_kb


def echo_kb():
    e_kb = ReplyKeyboardMarkup()
    btn1 = KeyboardButton('1 компания')
    btn2 = KeyboardButton('2 компания')
    btn3 = KeyboardButton('3 компания')
    btn4 = KeyboardButton('4 компания')
    btn5 = KeyboardButton('5 компания')
    btn6 = KeyboardButton('6 компания')
    btn7 = KeyboardButton('Вожатые')
    btn_all = KeyboardButton('Все')
    btn_cancel = KeyboardButton('Отмена')
    e_kb.row(btn1, btn2, btn3)
    e_kb.row(btn4, btn5, btn6)
    e_kb.row(btn7, btn_all, btn_cancel)
    return e_kb


def voz_kb():
    kb = main_keyboard()
    tel_btn = KeyboardButton("Телефоны/расселение")
    kb.add(tel_btn)
    return kb
