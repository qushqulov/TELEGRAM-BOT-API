import telebot

bot = telebot.TeleBot("8237248296:AAExjK4NPIzOxmNmnRFo5pYn4sTDAweX598")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot(message, message.text)

bot.infinity_polling()