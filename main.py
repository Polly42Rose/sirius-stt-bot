import telebot
import string

token = 'VERY_SECRET_TOKEN'
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, f'Я бот. Приятно познакомиться, {message.from_user.first_name}')

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    mod_message = message.text.lower()
    mod_message = mod_message.translate(str.maketrans('','', string.punctuation))
    if mod_message == 'привет':
        bot.send_message(message.from_user.id, 'Привет!')
    else:
        bot.send_message(message.from_user.id, 'Не понимаю, что это значит.')

bot.polling(none_stop=True)
