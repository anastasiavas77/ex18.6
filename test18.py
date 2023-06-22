import telebot
from config import keys, TOKEN
from extensions import ConvertionException, CryptoConverter


bot = telebot.TeleBot(TOKEN)



@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу с ботом введите команду в следующем формате: имя валюты /n ' \
           'в какую валюту перевести /n количество переводимой валюты. Список всех валют введите /values'
    bot.reply_to(message,text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'доступные валюты:'
    for key in keys.keys():
        text='\n'.join((text,key,))
    bot.reply_to(message,text)

@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')
        quote, base, amount = message.text.split(' ')

        if len(values) != 3:
            raise ConvertionException ('Слишком много параметров')

        #qoute, base, amount = values
        total_base = CryptoConverter.convert(quote, base,amount)
    except ConvertionException as e:
        bot.reply_to(message, f'ошибка пользователя\n{e}')
    except Exception as e:
        bot.reply_to(message, f'не удалось обработать команду.\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id,text)

bot.polling()