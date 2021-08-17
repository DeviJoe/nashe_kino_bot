from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.types import ParseMode
from aiogram.utils import executor
from config import TOKEN
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
import database

bot = Bot(token=TOKEN)
state = MemoryStorage()
dp = Dispatcher(bot, storage=state)


@dp.message_handler(commands=['token'])
async def register(msg: types.Message):
    username = msg.from_user.username
    args = msg.get_args().split(' ')
    if len(args) != 1:
        await msg.answer("Количество аргументов некорректно")
    else:
        token = args[0]
        if database.if_user_in_users(username) and database.if_token_valid(token):
            await msg.answer("Вы уже зарегистрированы")
        else:
            if database.reg_user(username, token):
                await msg.answer('''
                *ПОЗДРАВЛЯЕМ!* \nВы успешно зарегистрировались! Номер вашей команды - {}
                '''.format(database.get_team_by_username(username)), parse_mode=ParseMode.MARKDOWN)
            else:
                await msg.answer("Токен некорректен")


@dp.message_handler(commands=['logout'])
async def logout(msg: types.Message):
    username = msg.from_user.username
    database.delete_user(username)
    await msg.answer("До свидания!")


@dp.message_handler(commands=['score'])
async def scoreboard(msg: types.Message):
    username = msg.from_user.username
    team_num = database.get_team_by_username(username)
    if team_num is None:
        await msg.answer("Введите токен команды!")
    else:
        sb = database.get_scoreboard()
        answer = '*======= SCOREBOARD =======*\n\n'
        for i, record in enumerate(sb):
            rec = str(i + 1) + ') Компания №' + str(record['team_id']) + ' - {' + str(record['score']) + '} \n'
            if record['team_id'] == database.get_team_by_username(username):
                rec = '*' + rec + '*'
            answer += rec
        await msg.answer(answer, parse_mode=ParseMode.MARKDOWN)


@dp.message_handler(commands=['profile'])
async def profile_data(msg: types.Message):
    username = msg.from_user.username
    name = msg.from_user.last_name + ' ' + msg.from_user.first_name
    team = database.get_team_by_username(username)
    score = database.get_score(team)

    ans = f'''
    *======= PROFILE =======\n*
    Ваше имя: {name}
    Ваш ник: {username}
    Компания №{team}
    Счет компании: {score}
    '''
    await msg.answer(ans, parse_mode=ParseMode.MARKDOWN)


if __name__ == '__main__':
    executor.start_polling(dp)
