import telebot
from logs import tg_api, f_currencies_user, currencies_user
from extensions import ConvertionException, CryptoConverter

bot = telebot.TeleBot(tg_api)

# обработчики команд
@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(message.chat.id, 'Добро пожаловать, ' + str(message.from_user.first_name) + ',' + '\n' +
                     'отправьте сообщение боту в виде:\n<имя валюты> <имя валюты в которой надо узнать цену первой '
                     'валюты> <количество первой валюты>.')


@bot.message_handler(commands=['help'])
def help_(message):
    bot.send_message(message.chat.id,
                     '/start - запуск бота\n/help - команды бота\n/values - доступные валюты')


# вывод доступных валют в сокращенном виде
@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    txt = 'доступные валюты:'
    for value in currencies_user.keys():
        txt = '\n'.join((txt, value))
    bot.reply_to(message, txt)


# вывод доступных валют в полном списке
@bot.message_handler(commands=['f_values'])
def values(message: telebot.types.Message):
    txt = 'доступные валюты:'
    for value in f_currencies_user.keys():
        txt = '\n'.join((txt, value))
    bot.reply_to(message, txt)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values_ = message.text.split(' ')

        if len(values_) != 3:
            raise ConvertionException('Слишком много параметров')

        quote, base, amount = values_
        total_base = CryptoConverter.convert(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'ошибка пользователя\n{e}')
    except Exception as e:
        bot.reply_to(message, f'не удалось обработать команду\n{e}')
    else:
        if base == 'доллар':
            txt = f'{amount} {quote} в {base}ах - {total_base}'
            txt = txt.lower()
            bot.send_message(message.chat.id, txt)
        elif base == 'usd' or base == 'USD' or base == 'dollar':
            txt = f'{amount} {quote} in {base} - {total_base}'
            txt = txt.lower()
            bot.send_message(message.chat.id, txt)


# условие, в ходе которого бот работает
if __name__ == "__main__":
    bot.polling()
