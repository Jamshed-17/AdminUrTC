import json
import telebot
from pathlib import Path

path = Path('Data/DB.json')

def pushing_message_to_admin(kab:str, what:str, comment:str,time:str, user:str="HAVENT_NICK_NAME:((("):
    """Эта функция записывает аявку в базу данных
     Вид базы данных (JSON формат)
    {
        "kab": "45"
        "what": "Не рбаотает интернет"
        "comment": "Нет"
        "user": "@BushmelevaEA"
        "time": "12.10.2024 14:55:26"
        "status": "На обработке"
    }
    
    Ещё нужно обозначить администратора - для этого запишу его id в файлик, с которым потом будет сравниваться входной id
    """
    data = json.loads(path.read_text(encoding='utf-8'))
    try:
        id = data[-1]["ID"]+1
    except:
        id = 1
        
    quest = {"ID" : id,
        "kab": kab,
        "what": what,
        "comment": comment,
        "user": f"@{user}",
        "time": time.split(".")[0],
        "status": "Отправлен"}  
    data.append(quest)
    path.write_text(json.dumps(data, ensure_ascii=False), encoding='utf-8')

def get_mes_bot(b, m):
    """Здесь данные админа, чтобы отправлять что-то конкретно ему"""
    global bot
    global message
    bot = b
    message = m
    
def get_admin_mes_bot():
    with open("admin_message.txt", "r") as file:
        return file.read()

def admin_questions_data(messages, bots, news:bool=False):
    data = json.loads(path.read_text(encoding='utf-8'))
    if news == False:
        for i in range(0, len(data)):
                if data[i]["status"] == "Отправлен":
                    c = True
                    markup = telebot.types.InlineKeyboardMarkup(row_width=1)
                    but1 = telebot.types.InlineKeyboardButton("Взяться", callback_data="give_quest")
                    markup.add(but1)
                    new_quests = f"{data[i]["ID"]}\nЗаявка от {data[i]["user"]}: \nВ кабинете {data[i]["kab"]} {data[i]["what"]}. \nКомментарий: {data[i]["comment"]}\nЗаявка отправлена в {data[i]["time"]}"
                    bots.send_message(messages.chat.id, text=f"{new_quests}".format(messages.from_user), reply_markup = markup)
    elif news == True:
        new_quest = f"{data[-1]["ID"]} - новая заявка\nЗаявка от {data[-1]["user"]}: \nВ кабинете {data[-1]["kab"]} {data[-1]["what"]}. \nКомментарий: {data[-1]["comment"]}\nЗаявка отправлена в {data[-1]["time"].split(" ")[1]}, {data[-1]["time"].split(" ")[0]}"
        return new_quest
            
def give_to_db(ID):
    ID = int(ID)
    db = json.loads(path.read_text(encoding='utf-8'))
    for i in range(0, len(db)):
        if db[i]["ID"] == ID:
            with open ('Data/DB.json', 'w') as f:
                db[i]["status"] = "В процессе"
                json.dump(db, f, ensure_ascii=False, indent=4)        
                
def admin_complite_questions_data(messages, bots):
    data = json.loads(path.read_text(encoding='utf-8'))
    quests = ""
    for i in range(0, len(data)):
        quests = quests + f"{data[i]["ID"]}\nЗаявка от {data[i]["user"]}: \nВ кабинете {data[i]["kab"]} {data[i]["what"]}. \nКомментарий: {data[i]["comment"]}\nЗаявка отправлена в {data[i]["time"]}\nСтатус заявки: {data[i]["status"]}\n\n"
    bots.send_message(messages.chat.id, text=f"{quests}".format(messages.from_user))
 
def continue_questions_db(messages, bots):
    data = json.loads(path.read_text(encoding='utf-8'))
    for i in range(0, len(data)):
                if data[i]["status"] == "В процессе":
                    c = True
                    markup = telebot.types.InlineKeyboardMarkup(row_width=1)
                    but1 = telebot.types.InlineKeyboardButton("Выполнено", callback_data="complete_quest")
                    markup.add(but1)
                    new_quests = f"{data[i]["ID"]}\nЗаявка от {data[i]["user"]}: \nВ кабинете {data[i]["kab"]} {data[i]["what"]}. \nКомментарий: {data[i]["comment"]}\nЗаявка отправлена в {data[i]["time"]}"
                    bots.send_message(messages.chat.id, text=f"{new_quests}".format(messages.from_user), reply_markup = markup)

def complete_to_db(ID):
    ID = int(ID)
    db = json.loads(path.read_text(encoding='utf-8'))
    for i in range(0, len(db)):
        if db[i]["ID"] == ID:
            with open ('Data/DB.json', 'w') as f:
                db[i]["status"] = "Выполнено"
                json.dump(db, f, ensure_ascii=False, indent=4)
                
def check_user_quest(messages, bots, username):
    data = json.loads(path.read_text(encoding='utf-8'))
    for i in range(len(data)-1, 0, -1):
        if data[i]["user"] == "@"+username:
            quest = f"Ваша последняя заявка - ** {data[i]["what"]} **. Отправлена в {data[i]["time"].split(" ")[1]}, {data[i]["time"].split(" ")[0]} и находится на стадии '{data[i]["status"]}'"
            bots.send_message(messages.chat.id, text=f"{quest}".format(messages.from_user), parse_mode="Markdown")
            break
