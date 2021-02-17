from flask import Flask, request
import os
import telebot


app = Flask(__name__)
TOKEN = os.environ.get('TOKEN')
bot = telebot.TeleBot(TOKEN)

with open('courses.txt') as file:
    courses = [item.split(',') for item in file]

with open('planning.txt') as file:

    plans = {'start': [],
             'pro': [],
             'other': []}
    for item in file:
        if 'start' in item.lower():
            plans['start'].append(item)
        elif 'pro' in item.lower():
            plans['pro'].append(item)
        else:
            plans['other'].append(item)


@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 'PROG.Kyiv.UA')


@bot.message_handler(commands=['help'])
def start(message):
    res = '/courses - список курсов \n' \
          '/planning - расписание запуска курсов,'
    bot.reply_to(message, res)


@bot.message_handler(commands=['courses'])
def echo_message_courses(message):

    keyboard = telebot.types.InlineKeyboardMarkup(row_width=1)

    for text, url in courses:
        url_button = telebot.types.InlineKeyboardButton(text=text.strip(), url=url.strip(' \n'))
        keyboard.add(url_button)
    bot.send_message(message.chat.id, "Привет! Выбери курс", reply_markup=keyboard)


@bot.message_handler(commands=['planning'])
def echo_message_planning(message):

    res = ''
    for courses in plans:
        for item in plans[courses]:
            course, data = item.split(',')
            res += f'<b>{course}</b>: <code>{data}</code>\n'
        else:
            res += '\n'
    bot.send_message(message.from_user.id, text=res, parse_mode='HTML')


@app.route('/' + TOKEN, methods=['POST'])
def get_message():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "Python Telegram Bot 21-11-2020", 200


@app.route('/')
def main():
    bot.remove_webhook()
    bot.set_webhook(url='https://sinchuk.herokuapp.com/' + TOKEN)
    return "Python Telegram Bot", 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
