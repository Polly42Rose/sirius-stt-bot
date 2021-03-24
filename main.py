import telebot
import string
import requests
import os
import glob
import torch
from inference import InferenceModel


TELEGRAM_API_TOKEN = ''
AUDIO_FOLDER = "audio"
bot = telebot.TeleBot(TELEGRAM_API_TOKEN)
model = InferenceModel(checkpoint_path='/home/mnakhodnov/sirius-stt/models/6_recovered/epoch_0.pt', device=torch.device('cpu'))


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, f'Я бот. Приятно познакомиться, {message.from_user.first_name}!\nПроробуй /translate')


@bot.message_handler(commands=['translate'])
def sst_request(message):
    bot.reply_to(message, f'{message.from_user.first_name}, отправь мне voice message:)')


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
    user_name = message.from_user.username
    user_folder = os.path.join(AUDIO_FOLDER, user_name)
    if not os.path.isdir(user_folder):
        os.mkdir(user_folder)

    if not os.listdir(user_folder):
        new_id = 0
    else:
        files = glob.glob(os.path.join(user_folder, "*"))
        latest_file = max(files, key=os.path.getctime)
        new_id = int(os.path.splitext(os.path.basename(latest_file))[0]) + 1

    filename = os.path.join(user_folder, f"{new_id}.ogg")
    with open(filename, "wb+") as f:
        f.write(file.content)
    text = model.run(os.path.join("../stt-bot/audio", filename))
    bot.send_message(message.from_user.id, f'Распознанный текст: {text}.')


if __name__ == "__main__":

    bot.polling(none_stop=True)

