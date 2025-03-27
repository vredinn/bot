import telebot
import config
import json
from random import randint, choice

with open("data.json", "r", encoding="utf-8") as file:
    data = json.load(file)

jokes = data["jokes"]
equations = data["equations"]

bot = telebot.TeleBot(config.TG_API_TOKEN)


@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.send_message(
        message.from_user.id,
        "Привет! Я JokerJames. Напиши /about, чтобы узнать больше обо мне. Напиши /help, чтобы увидеть список команд.",
    )


@bot.message_handler(commands=["help"])
def send_help(message):
    bot.send_message(
        message.from_user.id,
        "Список команд:\n/about - информация о боте\n/help - список команд\n/rnd - рандомное число от 1 до 3\n/joke - случайная шутка или анекдот\n/math - случайный пример уравнения",
    )


@bot.message_handler(commands=["about"])
def send_about(message):
    bot.send_message(
        message.from_user.id,
        "Это простой бот созданный Дмитриевым Виктором, студентом НТИ УрФУ. TG: @vredinn44.\nJokerJames - ваш персональный проводник в атмосферу игривости и юмора.",
    )


@bot.message_handler(commands=["rnd"])
def send_randint1(message):
    bot.send_message(message.from_user.id, randint(1, 3))


@bot.message_handler(commands=["joke"])
def send_joke(message):
    bot.send_message(message.from_user.id, choice(jokes))


@bot.message_handler(commands=["math"])
def send_math(message):
    equation, answer = choice(equations)
    equation = equation.replace("=", "\\=")
    equation = equation.replace("-", "\\-")
    equation = equation.replace("+", "\\+")
    equation = equation.replace("/", "\\/")
    answer = answer.replace("=", "\\=")
    answer = answer.replace("-", "\\-")
    bot.send_message(
        message.from_user.id,
        f"Уравнение:\n{equation}\n||Ответ: {answer}||",
        parse_mode="MarkdownV2",
    )


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    if message.text == "привет":
        bot.send_message(
            message.from_user.id, f"Привет, {message.from_user.first_name}!"
        )
    elif message.text == "пока":
        bot.send_message(message.from_user.id, "Пока!")
    elif message.text == "как дела":
        bot.send_message(message.from_user.id, "Хорошо, а у тебя?")
    else:
        bot.reply_to(message, message.text)


bot.infinity_polling()
