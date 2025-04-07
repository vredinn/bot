import telebot
from telebot import types
import config
import json
from random import randint, choice, shuffle

with open("data.json", "r", encoding="utf-8") as file:
    data = json.load(file)

jokes = data["jokes"]
equations = data["equations"]

bot = telebot.TeleBot(config.TG_API_TOKEN)


base_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
base_markup.add("/about", "/rnd", "/joke", "/math")


help_keyboard = types.InlineKeyboardMarkup()
btn_about = types.InlineKeyboardButton("/about", callback_data="help_about")
btn_help = types.InlineKeyboardButton("/help", callback_data="help_help")
btn_rnd = types.InlineKeyboardButton("/rnd", callback_data="help_rnd")
btn_joke = types.InlineKeyboardButton("/joke", callback_data="help_joke")
btn_math = types.InlineKeyboardButton("/math", callback_data="help_math")
help_keyboard.add(btn_about, btn_help, btn_rnd, btn_joke, btn_math)


@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.send_message(
        message.from_user.id,
        "Привет! Я JokerJames. Напиши /about, чтобы узнать больше обо мне. Напиши /help, чтобы увидеть список команд.",
        reply_markup=base_markup,
    )


@bot.message_handler(commands=["help"])
def send_help(message):
    bot.send_message(
        message.from_user.id,
        "Список команд:\n/about - информация о боте\n/help - список команд\n/rnd - рандомное число от 1 до 3\n/joke - случайная шутка или анекдот\n/math - случайный пример уравнения\nПодробнее о каждой команде:",
        reply_markup=help_keyboard,
    )


@bot.callback_query_handler(func=lambda call: call.data.startswith("help_"))
def handle_help(call):
    if call.data == "help_about":
        keyboard = types.InlineKeyboardMarkup()
        btn_back = types.InlineKeyboardButton("Назад", callback_data="help_back")
        keyboard.add(btn_back)
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="Команда /about показывает информация о боте, разработчике бота и ссылку для связи",
            reply_markup=keyboard,
        )
    elif call.data == "help_help":
        keyboard = types.InlineKeyboardMarkup()
        btn_back = types.InlineKeyboardButton("Назад", callback_data="help_back")
        keyboard.add(btn_back)
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="Комадна /help отображает список доступных команд бота и дает возможность просмотреть информацию о командах более подробно",
            reply_markup=keyboard,
        )
    elif call.data == "help_rnd":
        keyboard = types.InlineKeyboardMarkup()
        btn_back = types.InlineKeyboardButton("Назад", callback_data="help_back")
        keyboard.add(btn_back)
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="Команда /rnd отображает случайное число в диапазоне от 1 до 3",
            reply_markup=keyboard,
        )
    elif call.data == "help_joke":
        keyboard = types.InlineKeyboardMarkup()
        btn_back = types.InlineKeyboardButton("Назад", callback_data="help_back")
        keyboard.add(btn_back)
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="Команда /joke отображает случайную шутку и дает возможность получить новую шутку",
            reply_markup=keyboard,
        )
    elif call.data == "help_math":
        keyboard = types.InlineKeyboardMarkup()
        btn_back = types.InlineKeyboardButton("Назад", callback_data="help_back")
        keyboard.add(btn_back)
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="Команда /math отображает случайное уравнение и дает возможность выбрать один из четырех ответов и проверить Ваш навык математики",
            reply_markup=keyboard,
        )
    elif call.data == "help_back":
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="Список команд:\n/about - информация о боте\n/help - список команд\n/rnd - рандомное число от 1 до 3\n/joke - случайная шутка или анекдот\n/math - случайный пример уравнения\nПодробнее о каждой команде:",
            reply_markup=help_keyboard,
        )


@bot.message_handler(commands=["about"])
def send_about(message):
    markup = types.InlineKeyboardMarkup()
    button_about = types.InlineKeyboardButton(
        "Разработчик", url="https://t.me/vredinn44"
    )
    markup.add(button_about)
    bot.send_message(
        message.from_user.id,
        "Это простой бот созданный Дмитриевым Виктором, студентом НТИ УрФУ. TG: @vredinn44.\nJokerJames - ваш персональный проводник в атмосферу игривости и юмора.",
        reply_markup=markup,
    )


@bot.message_handler(commands=["rnd"])
def send_randint1(message):
    bot.send_message(
        message.from_user.id,
        randint(1, 3),
        reply_markup=base_markup,
    )


@bot.message_handler(commands=["joke"])
def send_joke(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("Еще шутка")
    bot.send_message(
        message.from_user.id,
        choice(jokes),
        reply_markup=keyboard,
    )


correct_answers = {}


@bot.message_handler(commands=["math"])
def send_math(message):
    a = 0
    while a == 0:
        a = randint(-10, 10)
    b = randint(-10, 10)
    c = randint(-10, 10)

    if b == 0:
        equation = f"{a}x = {c}"
        answer = round(c / a, 2)
    elif b < 0:
        equation = f"{a}x - {abs(b)} = {c}"
        answer = round((c + abs(b)) / a, 2)
    else:
        equation = f"{a}x + {b} = {c}"
        answer = round((c - b) / a, 2)

    equation = equation.replace("1x", "x").replace("-1x", "-x")

    answers = set()
    answers.add(answer)

    while len(answers) < 4:
        fake = round(answer + randint(-5, 5), 2)
        if fake != answer:
            answers.add(fake)

    answers = list(answers)
    shuffle(answers)

    math_keyboard = types.InlineKeyboardMarkup()
    for ans in answers:
        callback_data = f"ans:{ans}:{answer}"
        btn = types.InlineKeyboardButton(str(ans), callback_data=callback_data)
        math_keyboard.add(btn)

    bot.send_message(
        message.chat.id,
        f"Уравнение:\n{equation}\nВыберите ответ:",
        reply_markup=math_keyboard,
    )


@bot.callback_query_handler(func=lambda call: call.data.startswith("ans:"))
def handle_answer(call):
    _, selected, correct = call.data.split(":")
    answer_text = call.message.text.replace(
        "\nВыберите ответ:", f"\n\nВаш ответ: {selected}\n"
    )
    if selected == correct:
        bot.answer_callback_query(call.id, "✅ Правильно!")
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=answer_text + "\n✅ Правильно!\nРешить другое уравнение: /math",
        )
    else:
        bot.answer_callback_query(
            call.id, f"❌ Неправильно. Правильный ответ: {correct}"
        )
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=answer_text
            + f"\n❌ Неправильно. Правильный ответ: {correct}\nРешить другое уравнение: /math",
        )


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    if message.text == "привет":
        bot.send_message(
            message.from_user.id,
            f"Привет, {message.from_user.first_name}!",
            reply_markup=base_markup,
        )
    elif message.text == "пока":
        bot.send_message(message.from_user.id, "Пока!", reply_markup=base_markup)
    elif message.text == "как дела":
        bot.send_message(
            message.from_user.id, "Хорошо, а у тебя?", reply_markup=base_markup
        )
    elif message.text == "Еще шутка":
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add("Еще шутка")
        bot.send_message(
            message.from_user.id,
            choice(jokes),
            reply_markup=keyboard,
        )
    else:
        bot.reply_to(message, message.text, reply_markup=base_markup)


bot.infinity_polling()
