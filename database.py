from peewee import *
from models.Team import Team
from models.Point import Point
from models.User import User
from models.Money import Money
import token
import json
import config


def reg_user(username, token, chat_id, user):
    # print(config.TOKEN_FILE)
    f = open(config.TOKEN_FILE, 'r')
    tokens = json.load(f)
    f.close()

    if token in tokens:
        User.create(user_id=username, team_id=tokens[token], chat_id=chat_id, username=user)
        return True
    else:
        return False
    pass


def get_team_by_chat_id(chat):
    try:
        chat = int(chat)
        teams = User.select(User.team_id).where(User.chat_id == chat).execute()
        for team in teams:
            return team.team_id
    except:
        return None


def if_token_valid(token):
    f = open('token/tokens.json', 'r')
    tokens = json.load(f)
    f.close()
    if token in tokens:
        return True
    else:
        return False


def get_scoreboard():
    teams = Team.select().execute()
    res = []
    for team in teams:
        if team.team_id == 7:
            continue
        res.append({
            'team_id': team.team_id,
            'score': team.score
        })
    res.sort(key=lambda a: a['score'], reverse=True)
    return res


def get_point_coordinate(point_id):
    coords = Point.select(Point.latitude, Point.longitude).where(Point.point_id == point_id)
    coords = coords.execute()
    res = {}
    for point in coords:
        res = {
            'latitude': point.latitude,
            'longitude': point.longitude
        }
    return res


def if_user_in_users(chat_id):
    try:
        User.get(User.chat_id == chat_id)
        return True
    except:
        return False


def delete_user(chat_id):
    try:
        User.delete_by_id(chat_id)
        return True
    except:
        return False


def get_score(team_num):
    if team_num == 7:
        return None
    scores = Team.select(Team.score).where(Team.team_id == team_num).execute()
    for s in scores:
        return s.score


def get_money(team_num):
    scores = Money.select(Money.money).where(Money.team_id == team_num).execute()
    for s in scores:
        return s.money


def get_money_scoreboard():
    teams = Money.select().execute()
    res = []
    for team in teams:
        if team.team_id == 7:
            continue
        res.append({
            'team_id': team.team_id,
            'money': team.money
        })
    res.sort(key=lambda a: a['money'], reverse=True)
    return res


def get_users():
    users = User.select(User.chat_id).execute()
    res = []
    for user in users:
        res.append(user.chat_id)
    return res


def set_money(team_num, money):
    if money < 0:
        money = 0
    res = Money.select(Money.money).where(Money.team_id == team_num).execute()
    for r in res:
        r.team_id = team_num
        r.money = money
        r.save()

