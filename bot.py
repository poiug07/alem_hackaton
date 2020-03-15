import telebot
from datetime import datetime, timedelta

bot = telebot.TeleBot('902439732:AAF4hmwaf91A4h3_T4SIIRGQ2rW5d5cQQlE')

main_keyboard = telebot.types.ReplyKeyboardMarkup(True, True, row_width=3)
button_stat= telebot.types.KeyboardButton(text='Статистика')
button_symptom= telebot.types.KeyboardButton(text='Симптомы')
button_news= telebot.types.KeyboardButton(text='Новости')
main_keyboard.add(button_stat, button_symptom, button_news)
symptoms_keyboard = telebot.types.ReplyKeyboardMarkup(row_width=2)
symptoms_keyboard.add(telebot.types.KeyboardButton(text='Да'))
symptoms_keyboard.add(telebot.types.KeyboardButton(text='Нет'))
file=1


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
    bot.send_message(message.chat.id, 'Здравствуйте, это телеграм-бот для информирования и поддержки населения Казахстана касательно коронавируса.', reply_markup=main_keyboard)

@bot.message_handler(commands=['help'])
def start_message(message):
    bot.send_message(message.chat.id, 'Вы можете проверить свои симптомы, получить последние новости и офицальные заявления касательно коронавируса в Казахстане', reply_markup=main_keyboard)

@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text.lower() == 'статистика':
        bot.send_message(message.chat.id, text=read_stat_from_log())
    if message.text.lower() == 'новости':
        bot.send_message(message.chat.id, 'Пока новостей нет иди посиди')
    if message.text.lower() == 'симптомы':
        bot.send_message(message.chat.id, 'У вас повышенная температура?', reply_markup=symptoms_keyboard)
        global file
        file=open(f'users/{message.chat.id}.txt', 'w+')
        bot.register_next_step_handler(message, get_symptom_1)

def get_symptom_1(message):
    global file
    if message.text.lower() == 'да':
        l=1
    elif message.text.lower() == 'нет':
        l=0
    else:
        bot.send_message(message.chat.id, 'Используйте кнопки для ответов!')
        bot.send_message(message.chat.id, 'У вас повышенная температура?', reply_markup=symptoms_keyboard)
        bot.register_next_step_handler(message, get_symptom_1)
        return
    file.write(f'{l}|')
    bot.send_message(message.chat.id, 'Есть кашель?', reply_markup=symptoms_keyboard)
    bot.register_next_step_handler(message, get_symptom_2)

def get_symptom_2(message):
    global file
    if message.text.lower() == 'да':
        l=1
    elif message.text.lower() == 'нет':
        l=0
    else:
        bot.send_message(message.chat.id, 'Используйте кнопки для ответов!')
        bot.send_message(message.chat.id, 'Есть кашель?', reply_markup=symptoms_keyboard)
        bot.register_next_step_handler(message, get_symptom_2)
        return
    file.write(f'{l}|')
    bot.send_message(message.chat.id, 'Есть боль в горле?', reply_markup=symptoms_keyboard)
    bot.register_next_step_handler(message, get_symptom_3)

def get_symptom_3(message):
    global file
    if message.text.lower() == 'да':
        l=1
    elif message.text.lower() == 'нет':
        l=0
    else:
        bot.send_message(message.chat.id, 'Используйте кнопки для ответов!')
        bot.send_message(message.chat.id, 'Есть боль в горле?', reply_markup=symptoms_keyboard)
        bot.register_next_step_handler(message, get_symptom_3)
        return
    file.write(f'{l}|')
    bot.send_message(message.chat.id, 'Есть головная боль?', reply_markup=symptoms_keyboard)
    bot.register_next_step_handler(message, get_symptom_4)

def get_symptom_4(message):
    global file
    if message.text.lower() == 'да':
        l=1
    elif message.text.lower() == 'нет':
        l=0
    else:
        bot.send_message(message.chat.id, 'Используйте кнопки для ответов!')
        bot.send_message(message.chat.id, 'Есть голвная боль?', reply_markup=symptoms_keyboard)
        bot.register_next_step_handler(message, get_symptom_4)
        return
    file.write(f'{l}|')
    bot.send_message(message.chat.id, 'Есть усталость?')
    bot.register_next_step_handler(message, get_symptom_5)
    
def get_symptom_5(message):
    global file
    if message.text.lower() == 'да':
        l=1
    elif message.text.lower() == 'нет':
        l=0
    else:
        bot.send_message(message.chat.id, 'Используйте кнопки для ответов!')
        bot.send_message(message.chat.id, 'Есть усталость?', reply_markup=symptoms_keyboard)
        bot.register_next_step_handler(message, get_symptom_5)
        return
    file.write(f'{l}|')
    bot.send_message(message.chat.id, 'Насморк или понос?')
    bot.register_next_step_handler(message, get_symptom_6)

def get_symptom_6(message):
    global file
    if message.text.lower() == 'да':
        l=1
    elif message.text.lower() == 'нет':
        l=0
    else:
        bot.send_message(message.chat.id, 'Используйте кнопки для ответов!')
        bot.send_message(message.chat.id, 'Насморк или понос?', reply_markup=symptoms_keyboard)
        bot.register_next_step_handler(message, get_symptom_5)
        return
    file.write(f'{l}')
    file.close()
    file=open(f'users/{message.chat.id}.txt', 'r')
    if not(file.readlines):
        bot.send_message(message.chat.id, 'Ошибка', reply_markup=main_keyboard)
        return
    user=file.readlines()[0]
    file.close()
    if symptoms_test(user):
        bot.send_message(message.chat.id, 'Вам нужно скорее пройти тест на коронавирус!', reply_markup=main_keyboard)
    else:
        bot.send_message(message.chat.id, 'Скорее всего у вас нет поводов для беспокойства', reply_markup=main_keyboard)

def symptoms_test(line):
    score=0
    symptoms=line.split('|')
    if (symptoms[0]=='1'):
        score=score+20
    else:
        score=score-15
    if (symptoms[1]=='1'):
        score=score+20
    else:
        score=score-15    
    if (symptoms[2]=='1'):
        score=score+10
    else:
        score=score-7
    if (symptoms[3]=='1'):
        score=score+10
    else:
        score=score-7
    if (symptoms[4]=='1'):
        score=score+10
    else:
        score=score-7
    if (symptoms[5]=='1'):
        score=score+5
    else:
        score=score-0
    if score>=35:
        return True
    else:
        return False

bot.polling()