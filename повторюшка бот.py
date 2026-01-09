import telebot
from telebot.types import Message, ReplyKeyboardRemove as clear

bot = telebot.TeleBot("8567903766:AAFXO1yxZENlSdPo7grhcQnnN9qc1-YEuGw")

tekst = "Я буду повторять твои сообщения! Попробуй что-нибудь написать 😉"

@bot.message_handler(['start'])  # Обработчик команды /start
def start(msg: Message):
    bot.send_message(msg.chat.id, tekst)

@bot.message_handler(content_types=['text'])  # Реагирует на любое сообщение
def text_handler(msg: Message):
    bot.send_message(msg.chat.id, msg.text)

bot.infinity_polling()