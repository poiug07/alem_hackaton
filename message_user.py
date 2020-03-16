import telebot
bot = telebot.TeleBot(TOKEN_here)
main_keyboard = telebot.types.ReplyKeyboardMarkup(True, True, row_width=3)
button_stat= telebot.types.KeyboardButton(text='Статистика')
button_symptom= telebot.types.KeyboardButton(text='Симптомы')
button_news= telebot.types.KeyboardButton(text='Новости')
main_keyboard.add(button_stat, button_symptom, button_news)

id=00000000

message="Срочные новости. от коронавируса не спастись"
bot.send_message(id, message, reply_markup=main_keyboard)