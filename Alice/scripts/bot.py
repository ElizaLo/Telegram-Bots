# coding: utf-8
# import required libraries
import os
from os import environ
import random
import config
import dbworker
import datetime
import requests
import urllib.request
import subprocess

import telebot
from telebot.types import Message


bot = telebot.TeleBot(config.TOKEN)

#BOT_TOKEN = '1004026853:AAH7TyM-PhWKoR8j0XZcraIyKTIif0pqFbs'

# bot = telebot.TeleBot(environ['BOT_TOKEN'])

@bot.message_handler(commands=['start'])
def cmd_start(message):
    bot.send_message(message.chat.id, "Hello from Wonderland! 💙"
                                      "\nLet's start  our journey 🌹 and try to find Cheshire Cat 🐱"
                                      "\n \nHere are some commands: "
                                      "\n🔹 /dialog - start dialog"
                                      "\n🔹 /reset - reset dialog"
                                      "\n🔹 /recognition - image classification"
                                      "\n🔹 /help")
    bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAIlhV5BcyAnaBGAcJysDmF3JgtghWcIAAKeAQACW90SCDdyny47NvZFGAQ')

# Start of dialogue
@bot.message_handler(commands=["dialog"])
def cmd_start_dialog(message):
    state = dbworker.get_current_state(message.chat.id)
    if state == config.States.S_ENTER_NAME.value:
        bot.send_message(message.chat.id, "It seems that someone promised to send his name, but did not do it 🙁 "
                                          "I’m still waiting ...")
        bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAIlol5BtoxQy51l0C_qagFDqnK0pB8FAAKRAQACW90SCDRGaQI0kBg5GAQ')
    elif state == config.States.S_ENTER_AGE.value:
        bot.send_message(message.chat.id, "It seems that someone promised to send his age, but did not do it 😔 "
                                          "I’m waiting ...")
        bot.send_sticker(message.chat.id, 'CAACAgQAAxkBAAIlpF5BtuCdB9st0kkrWt4LXxIjaRvwAAIgAQACu-RJAAELHSxfy9fdZxgE')
    elif state == config.States.S_SEND_LOCATION.value:
        bot.send_message(message.chat.id, "It seems that someone promised to send where is he from 📍"
                                          "I’m waiting ...")
        bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAImCl5DGV2OOHfY0I68srfw0a4IUhpGAAKdAQACW90SCGDKljOL018mGAQ')
    elif state == config.States.S_SEND_PIC.value:
        bot.send_message(message.chat.id, "It seems that someone promised to send a picture"
                                          "I’m waiting ...")
        bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAImDF5DGXPYz0MjX0FPtdZuzXz02DIXAAKhAQACW90SCK-NOiy7s1mWGAQ')
    elif state == config.States.S_SEND_MOVIE.value:
        bot.send_message(message.chat.id, "It seems that someone promised to send favourite movie 🎥🎞"
                                          "I’m waiting ...")
        bot.send_sticker(message.chat.id, 'CAACAgQAAxkBAAImEl5DHM3pQvQrIzQFJvNrd0vQw3TzAAKXAQACu-RJAAHczGY8BnvXjxgE')
    else:  # By "else" mean the state "0" - the beginning of the dialogue
        bot.send_message(message.chat.id, "So what is your name?")
        bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAIlkV5BqGBycjbQb4Ova2H1OGzxBfchAAKVAQACW90SCCDte3BgeUheGAQ')
        dbworker.set_state(message.chat.id, config.States.S_ENTER_NAME.value)

# Using the / reset command, we will reset the states, returning to the beginning of the dialogue
@bot.message_handler(commands=["reset"])
def cmd_reset(message):
    bot.send_message(message.chat.id, "Well, let's start in a new way. What's your name?")
    dbworker.set_state(message.chat.id, config.States.S_ENTER_NAME.value)

@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_ENTER_NAME.value)
def user_entering_name(message):
    # In the case of the name don’t check anything
    bot.send_message(message.chat.id, "Good name, I'll remember! "
                                      "\nNow tell me your age, please?")
    dbworker.set_state(message.chat.id, config.States.S_ENTER_AGE.value)

@bot.message_handler(commands=['help'])
def cmd_help(message):
    bot.send_message(message.chat.id, "Here are commands: "
                                      "\n \n🔹 /dialog - start dialog"
                                      "\n🔹 /reset - reset dialog"
                                      "\n🔹 /recognition - image classification"
                                      "\n🔹 /help")
    dbworker.set_state(message.chat.id, config.States.S_START.value)


@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_ENTER_AGE.value)
def user_entering_age(message):
    # Here we’ll do a check
    if not message.text.isdigit():
        # Состояние не меняем, поэтому только выводим сообщение об ошибке и ждём дальше
        bot.send_message(message.chat.id, "Something get wrong 🤔 Try again!")
        bot.send_sticker(message.chat.id, 'CAACAgQAAxkBAAIlml5BssgRiup761KZTm_eAfnNwhmQAAIeAQACu-RJAAEYZh0WQkIVsRgE')
        return
    # At this stage, we are sure that message.text can be converted to a number, so we do not risk anything
    if int(message.text) < 10 or int(message.text) > 100:
        bot.send_message(message.chat.id, "What a strange age! I don't believe you! Answer honestly 🙃")
        bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAIloF5BtAPCWDpC4NmBuqPSqgN9dCz1AAKWAQACW90SCIRDegskrgwjGAQ')
        return
    else:
        # Age entered correctly, can go further
        bot.send_message(message.chat.id, "Once upon a time, I was the same age as you do ... oh ... "
                                          "However, we will not be distracted. "
                                          "\nLet me know a little bit more about you ☺️"
                                          "\nWhere are you from?")
        dbworker.set_state(message.chat.id, config.States.S_SEND_LOCATION.value)

@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) ==
                                          config.States.S_SEND_LOCATION.value)
def user_sending_location(message):
    bot.send_message(message.chat.id, "Wow! It seems far away from Wonderland..."
                                      "\nSend me any picture you like 😊")
    dbworker.set_state(message.chat.id, config.States.S_SEND_PIC.value)

@bot.message_handler(content_types=["photo"],
                     func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_SEND_PIC.value)
def user_sending_photo(message):
    # We already checked that this is a photo in the handler, no additional actions are needed.
    bot.send_message(message.chat.id, "That's nice!"
                                      "\nWhat is your favourite movie? 🎥🎞")
    dbworker.set_state(message.chat.id, config.States.S_SEND_MOVIE.value)

@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) ==
                                          config.States.S_SEND_MOVIE.value)
def user_sending_location(message):
    bot.send_message(message.chat.id, "Excellent! 🤗"
                                      "\n\nIf you would like to chat again - send the command /dialog.")
    bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAImEF5DHKHzt_ncvcof707s0hmWXTq9AAKJAQACW90SCCBacVSfHiAlGAQ')
    dbworker.set_state(message.chat.id, config.States.S_START.value)



# ----------- Recognition ---------------

bot_text = '''
Hi once more! 😊

So let's classify images using neural networks ✨

Send any pictures you like and I with Cheshire Cat 🐱 will classify them for you 🙃
'''

# store files in /tmp so storage does not get complete
result_storage_path = 'tmp'

@bot.message_handler(commands=['recognition'])
def send_welcome(message):
 bot.send_message(message.chat.id, bot_text)

@bot.message_handler(content_types=['photo'])
def handle(message):

  log_request(message)

  image_name = save_image_from_message(message)

  # object recognition
  object_recognition_image(image_name)
  bot.send_photo(message.chat.id, open('.data/darknet/predictions.jpg','rb'), 'Identified objects, if any! 😊')

  # image classification
  classification_list_result = classify_image(image_name)

  # send classification results
  output = 'The image classifies as:\n'
  for result in classification_list_result:
    output += result
  output += '\n Gimme more pictures! 🌸'

  bot.reply_to(message, output)

  cleanup_remove_image(image_name);




# ----------- Helper functions ---------------

def log_request(message):
  file = open('.data/logs.txt', 'a') #append to file
  file.write("{0} - {1} {2} [{3}]\n".format(datetime.datetime.now(), message.from_user.first_name, message.from_user.last_name, message.from_user.id))
  print("{0} - {1} {2} [{3}]".format(datetime.datetime.now(), message.from_user.first_name, message.from_user.last_name, message.from_user.id))
  file.close()


def get_image_id_from_message(message):
  # there are multiple array of images, check the biggest
  return message.photo[len(message.photo)-1].file_id


def save_image_from_message(message):
  cid = message.chat.id

  image_id = get_image_id_from_message(message)

  bot.send_message(cid, '🌹 I am nalyzing image, be patient! 🌹 ')

  # prepare image for downlading
  file_path = bot.get_file(image_id).file_path

  # generate image download url
  #image_url = "https://api.telegram.org/file/bot{0}/{1}".format(environ['BOT_TOKEN'], file_path)
  image_url = "https://api.telegram.org/file/bot{0}/{1}".format(config.TOKEN, file_path)
  print(image_url)

  # create folder to store pic temporary, if it doesnt exist
  if not os.path.exists(result_storage_path):
    os.makedirs(result_storage_path)

  # retrieve and save image
  image_name = "{0}.jpg".format(image_id)
  urllib.request.urlretrieve(image_url, "{0}/{1}".format(result_storage_path,image_name))

  return image_name;


def classify_image(image_name):
  # classify image -> https://pjreddie.com/darknet/imagenet/
  os.system('cd .data/darknet && ./darknet classifier predict cfg/imagenet1k.data cfg/darknet19.cfg darknet19.weights ../../{0}/{1} > ../../{0}/results.txt'.format(result_storage_path, image_name))

  # retrieve classification results
  results_file = open("{0}/results.txt".format(result_storage_path),"r")
  results = results_file.readlines()
  results_file.close()

  return results

def object_recognition_image(image_name):
  # object recognition -> https://pjreddie.com/darknet/yolo/
  os.system('cd .data/darknet && ./darknet detect cfg/yolov3-tiny.cfg yolov3-tiny.weights ../../{0}/{1}'.format(result_storage_path, image_name))


def cleanup_remove_image(image_name):
  os.remove('{0}/{1}'.format(result_storage_path, image_name))

alice_stickers = [
    'CAACAgIAAxkBAAIlEl5ATnk3_o-kRhc5rxKG6Jg04CMiAAKGAQACW90SCBDIKAipD9lUGAQ',
    'CAACAgIAAxkBAAIlFF5AToxtuxrVa2P_EsvaOpAdFVtTAAKHAQACW90SCDyuM_zA2A6EGAQ',
    'CAACAgIAAxkBAAIlFl5ATqivCMnan81dAS-se3nidrAqAAKIAQACW90SCFvCpX25FBMUGAQ',
    'CAACAgIAAxkBAAIlGF5ATrmWRmWMUqeUwggCBxIvqZOjAAKJAQACW90SCCBacVSfHiAlGAQ',
    'CAACAgIAAxkBAAIlGl5ATscH5ej_n7oTXwHT5P3bHm0GAAKKAQACW90SCAj0ldCSAnQXGAQ',
    'CAACAgIAAxkBAAIlHF5ATtae5nZQDYIgdUhBLQv-7nCkAAKLAQACW90SCFUkiX0GOxAjGAQ',
    'CAACAgIAAxkBAAIlHl5ATuO2UjKPtagDuPwaAZI_GuxqAAKMAQACW90SCFJWxbdx2-YWGAQ',
    'CAACAgIAAxkBAAIlIF5ATu9ivvNnO91pe6rK8NfAUbLtAAKNAQACW90SCC481L9ADH7WGAQ',
    'CAACAgIAAxkBAAIlIl5ATwLAkvo1qb4nBnYdbrRBLnyhAAKOAQACW90SCBOZ_nAHqJjZGAQ',
    'CAACAgIAAxkBAAIlJF5ATxGqbT_-NCaAcQZem4umMzUpAAKPAQACW90SCK2VvIE0tjXpGAQ',
    'CAACAgIAAxkBAAIlJl5ATyEPkw087q1opu4cY1eIdFLvAAKQAQACW90SCNxHHa8F6S5jGAQ',
    'CAACAgIAAxkBAAIlKF5ATzEDZwNjyKEFVWkopeIWUHa_AAKRAQACW90SCDRGaQI0kBg5GAQ',
    'CAACAgIAAxkBAAIlKl5AT0Kxl3szoj4QMYhlmX4LtXmtAAKSAQACW90SCGtMwn5wvcP8GAQ',
    'CAACAgIAAxkBAAIlLF5AT1D6hamjNgyZ9F6IWsxxqFPRAAKTAQACW90SCHxZLYzFkPAxGAQ',
    'CAACAgIAAxkBAAIlLl5AT2Hkzh_TYT5UPj4Hv1EUSvYaAAKUAQACW90SCHHTcZT2A2_aGAQ',
    'CAACAgIAAxkBAAIlMF5AT2_UMdZjhdq--haLDzZYI6EAA5UBAAJb3RIIIO17cGB5SF4YBA',
    'CAACAgIAAxkBAAIlMl5AT37SJx4Ym93TLmPbA2xIsTsDAAKWAQACW90SCIRDegskrgwjGAQ',
    'CAACAgIAAxkBAAIlNF5AT4whE0D0csIHW3jOzzaUwPqdAAKXAQACW90SCCusG2d1kyqNGAQ',
    'CAACAgIAAxkBAAIlNl5AT5sBUKbqlnmBfuapeg-bmmiSAAKYAQACW90SCNgDfbLnimOFGAQ',
    'CAACAgIAAxkBAAIlOF5AT6nHlesiVVLuRzXisq0kRqy4AAKZAQACW90SCIBg5KcPjkpZGAQ',
    'CAACAgIAAxkBAAIlOl5AT7sM2FvCy4pxKcZNB3ZoC7L3AAKbAQACW90SCLmTkbVIMHDUGAQ',
    'CAACAgIAAxkBAAIlPF5AT8q5H1AFCzq3jcizNdJBUZApAAKcAQACW90SCEJ1bQiXFbYdGAQ',
    'CAACAgIAAxkBAAIlPl5AT9coM5n9gDs-VBMvK6q1NREmAAKdAQACW90SCGDKljOL018mGAQ',
    'CAACAgIAAxkBAAIlQF5AT-TkSoTC4cFnoSNaTq5GvEa5AAKeAQACW90SCDdyny47NvZFGAQ',
    'CAACAgIAAxkBAAIlQl5AT_HspZj2JRUMd-__iKUfefcVAAKfAQACW90SCIIxccx-cO8UGAQ',
    'CAACAgIAAxkBAAIlRF5AT_97NPGOCQlMG27PKdkv9zomAAKgAQACW90SCMMSQGPEcDCVGAQ',
    'CAACAgIAAxkBAAIlRl5AUA4_1RxROdLG18jMmwV0SqiKAAKhAQACW90SCK-NOiy7s1mWGAQ',
    'CAACAgIAAxkBAAIlSF5AUBrq6m2uV4qZofMecS8FXkjzAAKiAQACW90SCAw6GzeO3rcRGAQ',
    'CAACAgIAAxkBAAIlSl5AUCmCs7pOIdz9WBi8EUMczDxnAAKjAQACW90SCCYBbJ52uU61GAQ',
]

@bot.message_handler(func = lambda message: True)
def send_sticker(message: Message):
    bot.send_sticker(message.chat.id, random.choice(alice_stickers))



if __name__ == "__main__":
    bot.infinity_polling()
