import telebot
from telebot import types

# Подключаем бота через botAPI
bot = telebot.TeleBot("7787740456:AAEnBGpQS9n1W1PQ4QlQdI8l40iN8eRzE-Q")

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    but1 = types.KeyboardButton("Создать заявку")
    but2 = types.KeyboardButton("Проверить статус заявки")
    markup.add(but1, but2)
    # Вклчаем кнопки, выводим текст
    bot.send_message(message.chat.id, text="Здравствуйте! Выберите действие".format(message.from_user), reply_markup=markup)
    bot.register_next_step_handler(message, new_question)

def new_question(message):
    if message.text == "J8d#jUd8an#njd8*ndksusiEVGENIIIIIY":
        pass
    elif message.text == "Создать заявку":
        markup_clear = types.ReplyKeyboardRemove()    
        bot.send_message(message.chat.id, text="В каком кабинете проблема?".format(message.from_user), reply_markup=markup_clear)
        bot.register_next_step_handler(message, kab_what)
    elif message.text == "Проверить статус заявки":
        pass
    
def kab_what(message):
    global kab 
    kab = message.text
    bot.send_message(message.chat.id, text="Что у вас случилось?".format(message.from_user))
    bot.register_next_step_handler(message, comments)
    
def comments(message):
    global what
    what = message.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    but1 = types.KeyboardButton("Не оставлять комментарий")
    markup.add(but1)
    bot.send_message(message.chat.id, text="Оставьте комментарий".format(message.from_user), reply_markup=markup)
    bot.register_next_step_handler(message, go)

def go(message):
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
    if message.text == "Да, отправить заявку":
        markup_clear = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, text="Ваша заявка отправлена".format(message.from_user),reply_markup=markup_clear)
        bot.register_next_step_handler(message, push_message)
    else:
        start(message)
        
def push_message():
    pass
    
bot.infinity_polling()
# Оставляем бота включённым