import telebot
import random
import time
import base64
from telebot import types
import requests
from bs4 import BeautifulSoup
import urllib.parse
import json

bot = telebot.TeleBot("TOKEN")

chars = "abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
pron = ["lewdk", "classic"]
print(bot.get_me())
BASE = "https://mini.s-shot.ru/1920x1080/JPEG/1920/Z100/?"
count = 0


@bot.message_handler(commands=["start", "info"])
def command(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    box_myid = types.KeyboardButton("Myid")
    box_logpass = types.KeyboardButton("Генератор log:pass")
    box_code = types.KeyboardButton("Base 64 code")
    box_decode = types.KeyboardButton("Base 64 decode")
    box_python = types.KeyboardButton("Python")
    box_site_screen = types.KeyboardButton("Site screen")
    box_ip_info = types.KeyboardButton("IP info")
    box_hentai = types.KeyboardButton("Hentai")
    markup.add(
        box_myid,
        box_logpass,
        box_code,
        box_decode,
        box_python,
        box_site_screen,
        box_ip_info,
        box_hentai,
    )
    bot.send_message(message.chat.id, "Выберите действие:", reply_markup=markup)


@bot.message_handler(content_types=["text"], func=lambda m: True)
def function(message):
    global login, password
    if message.text == "Генератор log:pass":
        for _ in range(12):
            login = ""
        for _ in range(12):
            login += random.choice(chars)
        for _ in range(15):
            password = ""
        for _ in range(15):
            password += random.choice(chars)

        bot.reply_to(
            message, f"Сгенерирован логин - {login}\nСгенерирован пароль - {password}"
        )
    elif message.text == "Base 64 code":
        bot.reply_to(message, "Введите сообщение которое нужно зашифровать:")
        bot.register_next_step_handler(message, code)
    elif message.text == "Base 64 decode":
        bot.reply_to(message, "Введите сообщение которое нужно разшифровать:")
        bot.register_next_step_handler(message, decode)
    elif message.text == "Myid":
        bot.reply_to(message, f"Ваш  ID - {message.from_user.id}")
    elif message.text == "Python":
        last_python(message)
    elif message.text == "Site screen":
        bot.send_message(message.chat.id, "Введите ссылку:")
        bot.register_next_step_handler(message, main)
    elif message.text == "IP info":
        bot.send_message(message.chat.id, "Введите ip:")
        bot.register_next_step_handler(message, ip_info)
    elif message.text == "Hentai":
        if random.choice(pron) == "classic":
            response = requests.get("https://nekos.life/api/v2/img/classic")
            json_data = json.loads(response.text)
            bot.send_document(message.chat.id, json_data["url"])
        elif random.choice(pron) == "lewdk":
            response = requests.get("https://nekos.life/api/v2/img/lewdk")
            json_data = json.loads(response.text)
            bot.send_photo(message.chat.id, json_data["url"])

    time_message = time.ctime(message.date)
    print(
        "Дата лога:{",
        time_message,
        "}\nСодержимое:{",
        message.text,
        "}\nАвтор:{(Никнейм -",
        message.from_user.username,
        ") -",
        "(Имя -",
        message.from_user.first_name,
        ")}\n",
        "##########",
    )


def code(message):
    code = str(message.text)
    try:
        bot.reply_to(message, f'{base64.b64encode(bytes(code, "utf-8")).decode()}')
    except:
        bot.reply_to(message, "Вы ввели ересть!")


def decode(message):
    code = str(message.text)
    try:
        bot.reply_to(message, f'{base64.b64decode(bytes(code, "utf-8")).decode()}')
    except:
        bot.reply_to(message, "Вы ввели ересть!")


def last_python(message):
    try:
        url = "https://www.python.org"
        r = requests.get(url).text
        soup = BeautifulSoup(r, "lxml")
        block3 = soup.find("div", class_="small-widget download-widget")
        bot.reply_to(message, f'{block3.find_all("p")[1].text}')
    except:
        bot.reply_to(message, "[ОШИБКА], обратитесь к администратору - @Brainfox33421")


def ip_info(message):
    try:
        ipinfo = requests.get(f"http://ipinfo.io/{message.text}/json")

        user_ip = ipinfo.json()["ip"]
        user_city = ipinfo.json()["city"]
        user_region = ipinfo.json()["region"]
        user_country = ipinfo.json()["country"]
        user_location = ipinfo.json()["loc"]
        user_org = ipinfo.json()["org"]

        bot.send_message(
            message.chat.id,
            f"\n<IP: {user_ip}\nГород: {user_city}\nРегион: {user_region}\nСтрана: {user_country}\nМестонахождение: {user_location}\nПровайдер: {user_org} >",
        )
    except:
        bot.send_message(
            message.chat.id, "[ERROR]"
        )


def main(message):
    try:
        url = message.text
        bot.send_message(message.chat.id, "Ожидайте...")
        path = f"{message.from_user.id}.jpg"
        url = urllib.parse.quote_plus(url)
        response = requests.get(BASE + url, stream=True)
        with open(path, "wb") as photo:
            for chunk in response:
                photo.write(chunk)
        img = open(path, "rb")
        bot.send_photo(message.chat.id, img)
    except:
        bot.send_photo(
            message.chat.id, "[ERROR]"
        )


bot.polling(none_stop=True)
