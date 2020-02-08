import telebot
from telebot.types import Message

TOKEN = '1004026853:AAH7TyM-PhWKoR8j0XZcraIyKTIif0pqFbs'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Hello from Wonderland! 💙")

@bot.message_handler(func = lambda message: True)
def send_sticker(message: Message):
    bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAIkQV4_JejNDhtE1MVjeNINATQzqj78AAKMAQACW90SCFJWxbdx2-YWGAQ')

# bot.send_message(393576580, 'Hi!')

@bot.message_handler(func = lambda message: True)
def upper(message: Message):
    bot.reply_to(message, message.text.upper())



bot.polling()
