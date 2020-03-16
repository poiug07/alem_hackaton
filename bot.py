import telebot
from datetime import datetime, timedelta
import mysql.connector
import stat

db = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  database="medbot"
)
cursor = db.cursor()

bot = telebot.TeleBot('TOKEN HERE')

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
            stat.get_data()
        else:
            return (f"Статистика по Казахстану:\nЗараженных: {stat_logs[1]}\nУмерли: {stat_logs[2]}\nВылечились: {stat_logs[3]}")

@bot.message_handler(commands=['start'])
def start_message(message):
    global cursor
    bot.send_message(message.chat.id, 'Здравствуйте, это телеграм-бот для информирования и поддержки населения Казахстана касательно коронавируса.', reply_markup=main_keyboard)
    cursor.execute(f"SELECT `id` FROM users WHERE `id`={message.chat.id}")
    result = cursor.fetchone()
    if result==None:
        cursor.execute(f'INSERT INTO users (id) VALUES ({message.chat.id})')
    db.commit()

@bot.message_handler(commands=['help'])
def help_message(message):
    bot.send_message(message.chat.id, 'Вы можете проверить свои симптомы, получить последние новости и офицальные заявления касательно коронавируса в Казахстане', reply_markup=main_keyboard)

@bot.message_handler(content_types=['text'])
def send_text(message):
    global cursor, db
    if message.text.lower() == 'статистика':
        bot.send_message(message.chat.id, text=read_stat_from_log())
    if message.text.lower() == 'новости':
        cursor.execute("SELECT * FROM news")
        result=cursor.fetchall()
        if result==None:
            bot.send_message(message.chat.id, 'Пока новостей нет', reply_markup=symptoms_keyboard)
        else:
            news_template="Последние статьи о коронавирусе в СМИ"
            for news in result:
                news_template=news_template+f"\n{news['title']} Ссылка на статью: {news['link']}"
            bot.send_message(message.chat.id, news_template, reply_markup=symptoms_keyboard)
    if message.text.lower() == 'симптомы':
        bot.send_message(message.chat.id, 'У вас повышенная температура?', reply_markup=symptoms_keyboard)
        bot.register_next_step_handler(message, get_symptom_1)

def get_symptom_1(message):
    global cursor, db
    if message.text.lower() == 'да':
        l=1
    elif message.text.lower() == 'нет':
        l=0
    else:
        bot.send_message(message.chat.id, 'Используйте кнопки для ответов!')
        bot.send_message(message.chat.id, 'У вас повышенная температура?', reply_markup=symptoms_keyboard)
        bot.register_next_step_handler(message, get_symptom_1)
        return
    cursor.execute(f'UPDATE users SET symp1={l} WHERE `id`={message.chat.id}')
    db.commit()
    bot.send_message(message.chat.id, 'Есть кашель?', reply_markup=symptoms_keyboard)
    bot.register_next_step_handler(message, get_symptom_2)

def get_symptom_2(message):
    global cursor, db
    if message.text.lower() == 'да':
        l=1
    elif message.text.lower() == 'нет':
        l=0
    else:
        bot.send_message(message.chat.id, 'Используйте кнопки для ответов!')
        bot.send_message(message.chat.id, 'Есть кашель?', reply_markup=symptoms_keyboard)
        bot.register_next_step_handler(message, get_symptom_2)
        return
    cursor.execute(f'UPDATE users SET symp2={l} WHERE `id`={message.chat.id}')
    db.commit()
    bot.send_message(message.chat.id, 'Есть боль в горле?', reply_markup=symptoms_keyboard)
    bot.register_next_step_handler(message, get_symptom_3)

def get_symptom_3(message):
    global cursor, db
    if message.text.lower() == 'да':
        l=1
    elif message.text.lower() == 'нет':
        l=0
    else:
        bot.send_message(message.chat.id, 'Используйте кнопки для ответов!')
        bot.send_message(message.chat.id, 'Есть боль в горле?', reply_markup=symptoms_keyboard)
        bot.register_next_step_handler(message, get_symptom_3)
        return
    cursor.execute(f'UPDATE users SET symp3={l} WHERE `id`={message.chat.id}')
    db.commit()
    bot.send_message(message.chat.id, 'Есть головная боль?', reply_markup=symptoms_keyboard)
    bot.register_next_step_handler(message, get_symptom_4)

def get_symptom_4(message):
    global cursor, db
    if message.text.lower() == 'да':
        l=1
    elif message.text.lower() == 'нет':
        l=0
    else:
        bot.send_message(message.chat.id, 'Используйте кнопки для ответов!')
        bot.send_message(message.chat.id, 'Есть голвная боль?', reply_markup=symptoms_keyboard)
        bot.register_next_step_handler(message, get_symptom_4)
        return
    cursor.execute(f'UPDATE users SET symp4={l} WHERE `id`={message.chat.id}')
    db.commit()
    bot.send_message(message.chat.id, 'Есть усталость?')
    bot.register_next_step_handler(message, get_symptom_5)
    
def get_symptom_5(message):
    global cursor, db
    if message.text.lower() == 'да':
        l=1
    elif message.text.lower() == 'нет':
        l=0
    else:
        bot.send_message(message.chat.id, 'Используйте кнопки для ответов!')
        bot.send_message(message.chat.id, 'Есть усталость?', reply_markup=symptoms_keyboard)
        bot.register_next_step_handler(message, get_symptom_5)
        return
    cursor.execute(f'UPDATE users SET symp5={l} WHERE `id`={message.chat.id}')
    db.commit()
    bot.send_message(message.chat.id, 'Насморк или понос?')
    bot.register_next_step_handler(message, get_symptom_6)

def get_symptom_6(message):
    global cursor, db
    if message.text.lower() == 'да':
        l=1
    elif message.text.lower() == 'нет':
        l=0
    else:
        bot.send_message(message.chat.id, 'Используйте кнопки для ответов!')
        bot.send_message(message.chat.id, 'Насморк или понос?', reply_markup=symptoms_keyboard)
        bot.register_next_step_handler(message, get_symptom_5)
        return
    cursor.execute(f'UPDATE users SET symp6={l} WHERE `id`={message.chat.id}')
    db.commit()
    cursor.execute(f'SELECT * FROM users WHERE `id`={message.chat.id}')
    result=cursor.fetchone()
    if result==None:
        bot.send_message(message.chat.id, 'Ошибка', reply_markup=main_keyboard)
        return

    if symptoms_test(result):
        bot.send_message(message.chat.id, 'Вам нужно скорее пройти тест на коронавирус!', reply_markup=main_keyboard)
    else:
        bot.send_message(message.chat.id, 'Скорее всего у вас нет поводов для беспокойства', reply_markup=main_keyboard)

def symptoms_test(line):
    score=0
    symptoms=[line['symp1'], line['symp2'],line['symp3'],line['symp4'],line['symp5'],line['symp6']]
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
    if score>=40:
        return True
    else:
        return False

bot.polling()
