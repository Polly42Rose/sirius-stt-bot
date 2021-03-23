import telebot
import string
import requests
import subprocess
import tempfile
import os
TELEGRAM_API_TOKEN = '1616165730:AAEUVpUwpefkxn8gxiQtf6HMVRijKOcIyaQ'
bot = telebot.TeleBot(TELEGRAM_API_TOKEN)


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


@bot.message_handler(content_types=['voice'])
def voice_processing(message):
    file_info = bot.get_file(message.voice.file_id)
    file = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(TELEGRAM_API_TOKEN, file_info.file_path))
    with open("source/audio.ogg", "wb+") as f:
        f.write(file.content)



bot.polling(none_stop=True)
