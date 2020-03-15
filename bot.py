import telebot
from datetime import datetime, timedelta
bot = telebot.TeleBot('902439732:AAF4hmwaf91A4h3_T4SIIRGQ2rW5d5cQQlE')

keyboard = telebot.types.ReplyKeyboardMarkup(True, True, row_width=3)
button_stat= telebot.types.KeyboardButton(text='Статистика')
button_symptom= telebot.types.KeyboardButton(text='Симптомы')
button_news= telebot.types.KeyboardButton(text='Новости')
keyboard.add(button_stat, button_symptom, button_news)

def read_stat_from_log():
    a=open('stats.txt','r')
    lines = a.readlines()
    if lines:
        last_line = lines[-1]
        stat_logs=last_line.split('|')
        last_date_offset = datetime.strptime(stat_logs[0], "%d-%B-%Y %H:%M")+timedelta(hours=9)
        if datetime.today()>last_date_offset:
            return ("need to check!")
        else:
            return (stat_logs[1])

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Салам это бот с коронавирусом', reply_markup=keyboard)

@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text.lower() == 'статистика':
        bot.send_message(message.chat.id, text=read_stat_from_log())
    if message.text.lower() == 'новости':
        bot.send_message(message.chat.id, 'Пока новостей нет иди посиди')

bot.polling()