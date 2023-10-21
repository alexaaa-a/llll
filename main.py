import telebot
from telebot import custom_filters
from telebot import StateMemoryStorage
from telebot.handler_backends import StatesGroup, State


state_storage = StateMemoryStorage()
# Вставить свой токет или оставить как есть, тогда мы создадим его сами
bot = telebot.TeleBot("6304038220:AAGqoICNs7ShJ7X9YgpQWEDr7vaBa3pFTdQ",
                      state_storage=state_storage, parse_mode='Markdown')


class PollState(StatesGroup):
    name = State()
    age = State()


class HelpState(StatesGroup):
    wait_text = State()


text_poll = "опрос"  # Можно менять текст
text_button_1 = "Советы психолога при подготовке к ОГЭ и ЕГЭ"  # Можно менять текст
text_button_2 = "Мотивация выпускникам"  # Можно менять текст
text_button_3 = "Что делать накануне экзамена"  # Можно менять текст


menu_keyboard = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
menu_keyboard.add(
    telebot.types.KeyboardButton(
        text_poll,
    )
)
menu_keyboard.add(
    telebot.types.KeyboardButton(
        text_button_1,
    )
)

menu_keyboard.add(
    telebot.types.KeyboardButton(
        text_button_2,
    ),
    telebot.types.KeyboardButton(
        text_button_3,
    )
)


@bot.message_handler(state="*", commands=['start'])
def start_ex(message):
    bot.send_message(
        message.chat.id,
        'Привет! Чем будем заниматься?',  # Можно менять текст
        reply_markup=menu_keyboard)

@bot.message_handler(func=lambda message: text_poll == message.text)
def first(message):
    bot.send_message(message.chat.id, 'Супер! *Ваше* _имя_?')  # Можно менять текст
    bot.set_state(message.from_user.id, PollState.name, message.chat.id)


@bot.message_handler(state=PollState.name)
def name(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['name'] = message.text
    bot.send_message(message.chat.id, 'Супер! Ваш `возраст?`')  # Можно менять текст
    bot.set_state(message.from_user.id, PollState.age, message.chat.id)


@bot.message_handler(state=PollState.age)
def age(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['age'] = message.text
    bot.send_message(message.chat.id, 'Спасибо за регистрацию! [Ваш бонус] (https://umschool.net/journal/oge/plan-podgotovki-k-oge-kak-effektivno-podgotovitsya-k-ekzamenam-v-9-klasse/)', reply_markup=menu_keyboard)  # Можно менять текст
    bot.delete_state(message.from_user.id, message.chat.id)


@bot.message_handler(func=lambda message: text_button_1 == message.text)
def help_command(message):
    bot.send_message(message.chat.id, "*В экзаменационную пору* всегда присутствует психологическое напряжение. Стресс при этом - абсолютно нормальная реакция организма. *Легкие* эмоциональные всплески полезны, они положительно сказываются на работоспособности и усиливают умственную деятельность. Но излишнее эмоциональное напряжение зачастую оказывает обратное действие. *Причиной* этого является, в первую очередь, личное отношение к событию. Поэтому важно формирование адекватного отношения к ситуации. Оно поможет выпускникам разумно распределить силы для подготовки и сдачи экзамена, а родителям - оказать своему ребенку правильную помощь.", reply_markup=menu_keyboard)  # Можно менять текст


@bot.message_handler(func=lambda message: text_button_2 == message.text)
def help_command(message):
    bot.send_message(message.chat.id, "*Сдача экзамена* - лишь одно из жизненных испытаний, многих из которых еще предстоит пройти. Не придавайте событию слишком высокую важность, чтобы не увеличивать волнение. *При правильном подходе* экзамены могут служить средством самоутверждения и повышением личностной самооценки. *Заранее* поставьте перед собой цель, которая Вам по силам. Никто не может всегда быть совершенным. *Пусть достижения* не всегда совпадают с идеалом, зато они Ваши личные. *Не стоит* бояться ошибок. Известно, что не ошибается тот, кто ничего не делает. *Люди*, настроенные на успех, добиваются в жизни гораздо больше, чем те, кто старается избегать неудач. *Будьте уверены*: каждому, кто учился в школе, по силам сдать ОГЭ. Все задания составлены на основе школьной программы. Подготовившись должным образом, Вы обязательно сдадите экзамен. ", reply_markup=menu_keyboard)  # Можно менять текст


@bot.message_handler(func=lambda message: text_button_3 == message.text)
def help_command(message):
    bot.send_message(message.chat.id, "1. Оставьте один день перед экзаменом на повторение материала. 2.Откажитесь от вечерних занятий, совершите прогулку и рано ложитесь спать.", reply_markup=menu_keyboard)  # Можно менять текст


bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.add_custom_filter(custom_filters.TextMatchFilter())

bot.infinity_polling()