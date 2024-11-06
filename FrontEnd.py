import telebot
from telebot import types
import BackEnd
import datetime

# Подключаем бота через botAPI
bot = telebot.TeleBot("7787740456:AAEnBGpQS9n1W1PQ4QlQdI8l40iN8eRzE-Q") #7136769737:AAEZhLglJIQtGr88HEjqUW8sfx2lYglVHAo - test, 7787740456:AAEnBGpQS9n1W1PQ4QlQdI8l40iN8eRzE-Q - work

@bot.message_handler(commands=['start'])
def start(message, first=True):
    #Начало работы бота, подключение админки
    if message.chat.username == "Vongolasoxi": #Vongolasoxi - Женя
        global admin_id
        admin_id = message.chat.id
        #Подклюение администратора
        BackEnd.get_mes_bot(bot, message)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        but1 = types.KeyboardButton(text="Просмотреть новые заявки")
        but3 = types.KeyboardButton(text="Заявки в процессе")
        but2 = types.KeyboardButton(text="История заявок")
        markup.add(but1, but3, but2)
        if first == True:
            bot.send_message(message.chat.id, text="Админка включена. Привет Женя".format(message.from_user), reply_markup=markup)
        else:
            bot.send_message(message.chat.id, text="Главное меню".format(message.from_user), reply_markup=markup)
        bot.register_next_step_handler(message, admin_panel)
            
    else:
        #Стартовые соощения, вход по админке
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        but1 = types.KeyboardButton("Создать заявку")
        but2 = types.KeyboardButton("Проверить статус заявки")
        markup.add(but1, but2)
        # Вклчаем кнопки, выводим текст
        bot.send_message(message.chat.id, text="Выберите действие".format(message.from_user), reply_markup=markup)
        bot.register_next_step_handler(message, new_question)
        
def new_question(message):
    if message.text == "Лютый пранк":
            bot.send_message(admin_id, text=f"Востание роботов начинается СЕГОДНЯ!!".format(message.from_user))
            bot.send_message(message.chat.id, text="Ахахаха, нормальная тема. Да да да, это моё изобретение)))".format(message.from_user))
            start(message)
    # Выбор действия, создание новой заявки
    elif message.text == "Создать заявку":
        markup_clear = types.ReplyKeyboardRemove()    
        bot.send_message(message.chat.id, text="В каком кабинете проблема?".format(message.from_user), reply_markup=markup_clear)
        bot.register_next_step_handler(message, kab_what)
    elif message.text == "Проверить статус заявки":
        BackEnd.check_user_quest(message, bot, message.chat.username)
        start(message)
    
def kab_what(message):
    # Создание новой заявки - причина заявки
    global kab 
    kab = message.text
    bot.send_message(message.chat.id, text="Что у вас случилось?".format(message.from_user))
    bot.register_next_step_handler(message, comments)
    
def comments(message):
    # Создание новой заявки - комментарий
    global what
    what = message.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    but1 = types.KeyboardButton("Не оставлять комментарий")
    markup.add(but1)
    bot.send_message(message.chat.id, text="Оставьте комментарий".format(message.from_user), reply_markup=markup)
    bot.register_next_step_handler(message, go)

def go(message):
    # Подтверждение отправки заявки
    global comment
    if message.text == "Не оставлять комментарий":
        comment = "Нет"
    else:
        comment = message.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Да, отправить заявку")
    btn2 = types.KeyboardButton("Нет, начать заново")
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, f" Кабинет: {kab}, \nПричина заявки: {what},\nКомментарий: {comment}\nВсё верно?".format(message.from_user), reply_markup=markup)
    bot.register_next_step_handler(message, check_message)
    
def check_message(message):
    # Отправка заяки в базу данных
    if message.text == "Да, отправить заявку":
        markup_clear = types.ReplyKeyboardRemove()
        BackEnd.pushing_message_to_admin(str(kab), what, comment, str(datetime.datetime.now()), message.chat.username)
        markup = telebot.types.InlineKeyboardMarkup(row_width=1)
        but1 = telebot.types.InlineKeyboardButton("Взяться", callback_data="give_quest")
        markup.add(but1)
        bot.send_message(admin_id, text=f"{BackEnd.admin_questions_data(admin_id, bot, True)}".format(message.from_user), reply_markup = markup)
        bot.send_message(message.chat.id, text="Ваша заявка отправлена".format(message.from_user),reply_markup=markup_clear)
        start(message)
    else:
        start(message)


def admin_panel(message):
    if message.text=="Просмотреть новые заявки":
        admin_questions(message)
    elif message.text == "История заявок":
        complete_questions(message)
    elif message.text=="Заявки в процессе":
        continue_questions(message)
        

def admin_questions(message):
    BackEnd.admin_questions_data(message, bot)
    bot.send_message(message.chat.id, text="Это все заявки на данный момент".format(message.from_user))
    start(message, False)
def complete_questions(message):
    BackEnd.admin_complite_questions_data(message, bot)
    start(message, False)
def continue_questions(message):
    BackEnd.continue_questions_db(message, bot)
    start(message, False)
    
@bot.callback_query_handler(func=lambda call: call.data == "give_quest")
def given_quest_button(call: types.CallbackQuery):
    markup_clear = types.ReplyKeyboardRemove()
    BackEnd.give_to_db(call.message.text.split("\n")[0])
    bot.send_message(call.message.chat.id, text=f"Заявка под номером {call.message.text.split("\n")[0]} теперь имеет статус 'В процессе'")
    
    
@bot.callback_query_handler(func=lambda call: call.data == "complete_quest")
def given_quest_button(call: types.CallbackQuery):
    markup_clear = types.ReplyKeyboardRemove()
    BackEnd.complete_to_db(call.message.text.split("\n")[0])
    bot.send_message(call.message.chat.id, text=f"Заявка под номером {call.message.text.split("\n")[0]} теперь имеет статус 'Выполнено'")
        
bot.infinity_polling()
# Оставляем бота включённым