import json
import datetime
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.types import ParseMode, ContentType
from aiogram.utils import executor
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import config
import keyboards
from config import TOKEN
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from keyboards import main_keyboard, reg_keyboard
import database

bot = Bot(token=TOKEN)
state = MemoryStorage()
dp = Dispatcher(bot, storage=state)


class Message(StatesGroup):
    waiting_company = State()
    waiting_msg = State()
    waiting_private_msg = State()


@dp.message_handler(commands=['start'])
async def process_start_command(msg: types.Message):
    if not database.if_user_in_users(msg.from_user.username):
        await msg.answer("Добрый день! Для работы с ботом, пожалуйста, зарегистрируйтесь", reply_markup=reg_keyboard())
    else:
        await msg.answer('С возвращением! Вы уже зарегистрированы', reply_markup=main_keyboard())


async def logout(msg: types.Message):
    username = msg.from_user.id
    database.delete_user(username)
    await msg.answer("До свидания!", reply_markup=reg_keyboard())


async def table(msg: types.Message):
    try:
        date = datetime.datetime.now()
        day = str(date.day)
        f = open(f'{config.TABLES_DIR}\\{day}.md', 'r', encoding='utf-8')
        text = f.read()
        # print(text)
        f.close()
        await msg.answer(text, parse_mode=ParseMode.MARKDOWN)
    except:
        await msg.answer(f"Расписание на {day} августа не найдено :(")


async def profile_data(msg: types.Message):
    username = msg.from_user.id
    user = ''
    if msg.from_user.first_name is not None:
        user += str(msg.from_user.first_name)
    user += ' '
    if msg.from_user.last_name is not None:
        user += str(msg.from_user.last_name)
    team = database.get_team_by_chat_id(username)
    score = database.get_money(team)

    if team <= 6:
        ans = f'''
*======== PROFILE ========\n*
Ваше имя: {user}
Ваш TELEGRAM ID: {username}
Компания №{team}
Счет компании: {score} кадриков
        '''
        kb = keyboards.main_keyboard()
    else:
        ans = f'''
*======== PROFILE ========\n*
Ваше имя: {user}
Ваш TELEGRAM ID: {username}
Вы вожатый :) 
        '''
        kb = keyboards.voz_kb()
    await msg.answer(ans, parse_mode=ParseMode.MARKDOWN, reply_markup=kb)


async def scoreboard(msg: types.Message):
    username = msg.from_user.id
    team_num = database.get_team_by_chat_id(username)
    if team_num is None:
        await msg.answer("Введите токен команды!")
    else:
        places = ['🥇', '🥈', '🥉']
        you_pointer = '◀️'
        sb = database.get_money_scoreboard()
        answer = '*======= SCOREBOARD =======*\n\n'
        for i, record in enumerate(sb):
            rec = str(i + 1) + ') Компания №' + str(record['team_id']) + ' - ' + str(record['money']) + ' кадриков'
            if 0 <= i <= 2:
                rec += places[i]
            if record['team_id'] == database.get_team_by_chat_id(   username):
                rec = '*' + rec + '*' + you_pointer
            rec += '\n'
            answer += rec
        await msg.answer(answer, parse_mode=ParseMode.MARKDOWN)


async def activity(msg: types.Message):
    try:
        date = datetime.datetime.now()
        day = str(date.day)
        f = open(f'{config.ACTIVITIES_DIR}\\{day}.json', 'r', encoding='utf-8')
        text = json.load(f)['text']
        await msg.answer(text, parse_mode=ParseMode.MARKDOWN)
    except:
        await msg.answer("Дневных активностей на сегодня нет :(")


@dp.message_handler(regexp='token_[0-9a-zA-z]{8}$')
async def reg_token(msg: types.Message):
    username = msg.from_user.id
    token = msg.text
    if database.if_user_in_users(username) and database.if_token_valid(token):
        await msg.answer("Вы уже зарегистрированы, отправьте боту сообщение \"разлогиниться\" и попробуйте снова!")
    else:
        user = ''
        if msg.from_user.first_name is not None:
            user += str(msg.from_user.first_name)
        user += ' '
        if msg.from_user.last_name is not None:
            user += str(msg.from_user.last_name)
        if database.reg_user(msg.from_user.username, token, msg.from_user.id, user):
            await msg.answer('''
            *ПОЗДРАВЛЯЕМ!* \nВы успешно зарегистрировались! Ваша компания №{}
            '''.format(database.get_team_by_chat_id(username)), parse_mode=ParseMode.MARKDOWN,
                             reply_markup=main_keyboard())
            if msg.from_user.id in config.ADMINS or msg.from_user.username in config.ADMINS:
                await msg.answer("Подтверждены полномочия администратора!")
            if database.get_team_by_chat_id(msg.from_user.id) == 7:
                await msg.answer("Подтвержены полномочия вожатого!", reply_markup=keyboards.voz_kb())
        else:
            await msg.answer("Токен некорректен")


@dp.message_handler(commands=['echo', 'private'], state='*')
async def spam(msg: types.Message):
    if not database.get_team_by_chat_id(msg.from_user.id):
        await msg.answer("Вы не зарегистрированы. Для регистрации отправьте токен Вашей компании")
        return
    if not database.get_team_by_chat_id(msg.from_user.id):
        await msg.answer("Вы не вошли в систему!")
        return
    if msg.from_user.id in config.ADMINS or msg.from_user.username in config.ADMINS:
        if msg.text == '/echo':
            await msg.answer("Пожалуйста, введите сообщение для рассылки или /cancel для отмены")
            await Message.waiting_msg.set()
        if msg.text == '/private':
            await msg.answer("Пожалуйста, введите сообщение для ПРИВАТНОЙ рассылки или /cancel для отмены")
            await Message.waiting_private_msg.set()
    else:
        await msg.answer("Простите, но вы не в группе администраторов :)")


@dp.message_handler(commands=['cancel'], state=Message.waiting_msg)
async def cancel_broadcast(msg: types.Message, state: FSMContext):
    await state.finish()
    await msg.answer('Отправка рассылки отменена')


@dp.message_handler(commands=['cancel'], state=Message.waiting_private_msg)
async def cancel_broadcast(msg: types.Message, state: FSMContext):
    await state.finish()
    await msg.answer('Отправка приватной рассылки отменена')


@dp.message_handler(state=Message.waiting_msg)
async def broadcast(msg: types.Message, state: FSMContext):
    for user in database.get_users():
        await bot.send_message(user, msg.html_text, parse_mode=ParseMode.HTML)
    await state.finish()


@dp.message_handler(state=Message.waiting_private_msg)
async def private_broadcast(msg: types.Message, state: FSMContext):
    for user in database.get_users():
        if database.get_team_by_chat_id(user) == 7:
            await bot.send_message(user, msg.html_text, parse_mode=ParseMode.HTML)
    await state.finish()


@dp.message_handler(commands=['update'])
async def update_money(msg: types.Message):
    if not database.get_team_by_chat_id(msg.from_user.id):
        await msg.answer("Вы не зарегистрированы. Для регистрации отправьте токен Вашей компании")
        return
    try:
        if msg.from_user.username in config.ADMINS:
            args = msg.get_args().split(' ')
            if len(args) == 2:
                team_num = int(args[0])
                money = int(args[1])
                database.set_money(team_num, money)
                await msg.answer("Успешно обновлено!")
            elif len(args) == 3:
                team_num = int(args[0])
                sign = args[1]
                money = int(args[2])
                if sign == '+':
                    database.set_money(team_num, database.get_money(team_num) + money)
                    await msg.answer("Успешно обновлено!")
                elif sign == '-':
                    database.set_money(team_num, database.get_money(team_num) - money)
                    await msg.answer("Успешно обновлено!")
                else:
                    await msg.answer('Неправильный математический операнд')
            else:
                await msg.answer("Ошибка в количестве аргументов")
        else:
            await msg.answer("Вы не входите в группу админов :)")
    except:
        await msg.answer('Возникла непредвиденная ошибка!')


@dp.message_handler(commands=['reset'])
async def reset_money(msg: types.Message):
    if not database.get_team_by_chat_id(msg.from_user.id):
        await msg.answer("Вы не зарегистрированы. Для регистрации отправьте токен Вашей компании")
        return
    if msg.from_user.username in config.ADMINS or msg.from_user.id in config.ADMINS:
        for i in range(1, 7):
            database.set_money(i, 0)
        await msg.answer("Все счета успешно сброшены!")
    else:
        await msg.answer("Вы не входите в группу админов :)")


@dp.message_handler(commands=['admin'])
async def get_admin_cap(msg: types.Message):
    if msg.from_user.username in config.ADMINS or msg.from_user.id in config.ADMINS:
        await msg.answer("Вы являетесь админом!")
    else:
        await msg.answer("Вы не являетесь админом!")


async def tel(msg: types.Message):
    if database.get_team_by_chat_id(msg.from_user.id) == 7:
        f = open('tel.md', 'r', encoding='utf-8')
        telephones = f.read()
        f.close()
        await msg.answer(telephones, parse_mode=ParseMode.MARKDOWN)
    else:
        await msg.answer("Вы не вожатый, я все вижу :(")
    pass


@dp.message_handler(content_types=ContentType.TEXT)
async def handler(msg: types.Message):
    username = msg.from_user.id
    if not database.if_user_in_users(username):
        if msg.text.lower() == 'регистрация':
            await msg.answer('Пожалуйста, введите токен авторизации')
        else:
            await msg.answer("Вы не зарегистрированы. Для регистрации отправьте токен Вашей компании")
    else:
        if msg.text.lower() == 'разлогиниться':
            await logout(msg)
        elif msg.text.lower() == 'профиль':
            await profile_data(msg)
        elif msg.text.lower() == 'рейтинг':
            await scoreboard(msg)
        elif msg.text.lower() == 'активность дня':
            await activity(msg)
        elif msg.text.lower() == 'расписание':
            await table(msg)
        elif msg.text.lower() == 'телефоны/расселение':
            await tel(msg)

if __name__ == '__main__':
    executor.start_polling(dp)
