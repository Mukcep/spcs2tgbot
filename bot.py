import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from dotenv import dotenv_values

from SpacesMusicParser import SpacesFileType, SpacesMusicParser
from SpacesFileDownloader import SpacesFileDownloader

from logger import logger

current_dir = os.path.dirname(os.path.abspath(__file__))

if not os.path.isfile(f"{current_dir}/.env" ):
  logger.error("Создайте файл .env с токеном")
  exit()

config = {
  **dotenv_values('.env')
}

bot = telebot.TeleBot(config['TELEGRAM_BOT_TOKEN'])


@bot.message_handler(commands=['sz'])
def send_welcome(message):
  query = message.text.replace('/sz', '')
  if query == '':
    bot.send_message(message.chat.id, "Необходимо указать што будем искатi")
    return False
  logger.info(f"({message.from_user.first_name}) хочет найти: {query}".replace('\n', ''))
  result = SpacesMusicParser.shared_zone_search(query)
  if len(result.tracks) == 0:
    logger.info(f"({message.from_user.first_name}) обкакался и ничего не нашел")
    bot.send_message(message.chat.id, "Ничего нема(")
    return False
  logger.info(f"({message.from_user.first_name}) нашлось {len(result.tracks)}")
  text = 'Вроде шото нашлось, смотри:\n\n'
  markup = InlineKeyboardMarkup()
  markup.row_width = 1

  for track in result.tracks:
    if track.spaces_file_type == SpacesFileType.MUSIC:
      icon = "🎶"
    elif track.spaces_file_type == SpacesFileType.FILE:
      icon = '📂'
    markup.add(
        InlineKeyboardButton(f"{icon} {track.getFullName()}", callback_data=f"{track.file_id}|{track.spaces_file_type.value}")
      )

  bot.send_message(message.chat.id, text, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
  file_id = call.data.split('|')[0]
  file_type = SpacesFileType(int(call.data.split('|')[1]))
  # file_name = SpacesFileType(int(call.data.split('|')[2]))
  downloader = SpacesFileDownloader(file_id, file_type)
  downloader.download(fake=True)
  logger.info(f"({call.message.from_user.first_name}) запрос файла с id: {file_id}")
  bot.send_audio(call.message.chat.id, downloader.downloadUrl, caption=downloader.file_name)
  # bot.send_message(call.message.chat.id, downloader.downloadUrl)
  bot.answer_callback_query(call.id, f"FileID = {call.data}")

bot.infinity_polling()

