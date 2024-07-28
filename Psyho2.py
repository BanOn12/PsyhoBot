

from aiogram.filters.command import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
import asyncio
import cfg
# Set up logging
logging.basicConfig(level=logging.INFO)


# Initialize bot and dispatcher
token=""

twd_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, keyboard=[[KeyboardButton(text="Да"), KeyboardButton(text="Нет")]])
twd_kb2 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, keyboard=[[KeyboardButton(text="Да"), KeyboardButton(text="нет")]])
twd_kb3 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, keyboard=[[KeyboardButton(text="да"), KeyboardButton(text="конечно")]])
twd_kb4 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, keyboard=[[KeyboardButton(text="дa"), KeyboardButton(text="нeт")]])
keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Уже подписан", callback_data="check_subscription")],
        [InlineKeyboardButton(text="Подписался", callback_data="check_subscription")]])
keyboard2 = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Да", callback_data="yes")],
        [InlineKeyboardButton(text="Нет", callback_data="no")]])



bot = Bot(token,parse_mode="HTML")
dp = Dispatcher()

# Questions and user responses
questions = [
    "<b>Вопрос 1:</b> нарушение сна",
    "<b>Вопрос 2:</b> повышенная чувствительность",
    "<b>Вопрос 3:</b> повышение бдительности в ожидании опасности",
    "<b>Вопрос 4:</b> учащение сердцебиения, повышение артериального давления",
    "<b>Вопрос 5:</b> повышение глюкозы в крови и ощущение сухости во рту, жажды",
    "<b>Вопрос 6:</b> учащенное мочеиспускание",
    "<b>Вопрос 7:</b> потливость или зябкость",
    "<b>Вопрос 8:</b> мышечное напряжение (вплоть до дрожи), мышечные боли (колющие, жгучие, ноющие, мучительные, которые сложно вербализовать)",
    "<b>Вопрос 9:</b> ускорения темпа мышления, речь быстрая, сбивчивая",
    "<b>Вопрос 10:</b> двигательное беспокойство от мышечного напряжения до двигательного возбуждения, суетливость, сложность усидеть на месте"
]


user_responses = []

# Function to create inline keyboard
def create_inline_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="Да", callback_data="yes")
    builder.button(text="Нет", callback_data="no")
    return builder.as_markup()

# Start command handler
@dp.message(Command("start"))
async def start_command(message: types.Message):
    await message.answer(cfg.text_5)
    await message.answer(cfg.text_6)
    await message.answer('Выберете наиболее подходящее Вам состояние')
    user_responses.clear()  # Clear previous responses
    await send_question(message.chat.id, 0)

async def send_question(chat_id, question_index):
    if question_index < len(questions):
        question = questions[question_index]
        await bot.send_message(chat_id, question, reply_markup=create_inline_keyboard())
    else:
        if any(user_responses[:8]):
            await bot.send_message(chat_id, f"{cfg.text_7}")
        if len(user_responses) > 8 and user_responses[8] == 1:
            await bot.send_message(chat_id, f"{cfg.text_8}")
        if len(user_responses) > 9 and user_responses[9] == 1:
            await bot.send_message(chat_id, f"{cfg.text_9}")
        await bot.send_message(chat_id, text="Хотите узнать причину возникновения тревожности?", reply_markup=twd_kb)

# Callback query handler for questions
@dp.callback_query(lambda c: c.data in ["yes", "no"])
async def process_callback(callback_query: CallbackQuery):
    response = 1 if callback_query.data == "yes" else 0
    user_responses.append(response)
    await bot.answer_callback_query(callback_query.id)
    
    next_question_index = len(user_responses)
    await send_question(callback_query.message.chat.id, next_question_index)

@dp.callback_query(lambda c: c.data == "check_subscription")
async def check_subscription(callback_query: CallbackQuery):
    try:
        user_channel_status = await bot.get_chat_member(chat_id='', user_id=callback_query.from_user.id)
        if user_channel_status.status != 'left':
            await callback_query.answer('Спасибо за подписку!')
            await bot.send_message(chat_id=callback_query.from_user.id ,text= f"{cfg.text_10}")
            await bot.send_message(chat_id=callback_query.from_user.id,text = 
                                   
                                   "Хотите узнать ещё о тревожности?", reply_markup= twd_kb3)
        else:
            await callback_query.answer('Для начала подпишитесь на наш канал')
    except Exception as e:
        await callback_query.answer('Не удалось проверить подписку. Пожалуйста, попробуйте позже.')
        print(f"Error: {e}")
async def check_subscription(message: types.Message):
    try:
        user_channel_status = await bot.get_chat_member(chat_id='', user_id=message.from_user.id)
        return user_channel_status.status != 'left'
    except Exception as e:
        await message.answer('Не удалось проверить подписку. Пожалуйста, попробуйте позже.')
        print(f"Error: {e}")
        return False


#block yes or no
@dp.message(F.text == "Да")
async def roma(message: types.Message):
    if await check_subscription(message):
        await message.answer(cfg.text_10)
        await message.reply("Хотите узнать ещё о тревожности?", reply_markup=twd_kb3)
    else:
        await message.answer('Пожалуйста, подпишитесь на наш канал: <a href=""</a>', reply_markup=keyboard)

@dp.message(F.text == "да")
async def roma(message: types.Message):
    if await check_subscription(message):
        await message.reply(cfg.text_11)
        await message.reply(cfg.text_12, reply_markup= twd_kb4)
    else:
        await message.answer('Пожалуйста, подпишитесь на наш канал: <a href=""</a>', reply_markup=keyboard)
@dp.message(F.text == "конечно")
async def roma(message: types.Message):
    
    await message.reply(cfg.text_11)
    await message.reply(cfg.text_12, reply_markup= twd_kb4)

@dp.message(F.text == "дa")
async def roma(message: types.Message):
    await message.answer("Поздравляю! Вы сделали прекрасный выбор! Впереди вас ждёт увлекательная работа над собой по умению управлять стрессом, обидами, гневом, страхом, злостью, завистью, чувством вины. Вы научитесь строить генограмму своей семьи и понимать, какие вам нужно сделать шаги, чтобы брать силы и энергию в своей семье. А также, поработаете со своим подсознанием через Метафорические карты и, научитесь стартовать из настоящего, а не из прошлого или будущего. К тому же, после этих занятий, как правило, происходит увеличение дохода.” Вот ссылка на авторский курс “Версия 2.0 Перезагрузка” https://kursy.bryzgalina.com/maraphon_versiya_2.0 ")
    await message.answer("Обратите внимание, что данный курс создан для того, чтобы вы смогли обрести лучшую версию себя. Вы уже являетесь своей Версией 1.0. Так найдите себя лучше, чем вы есть сейчас и избавьтесь от стресса, тревожности, страхов, переживаний. Научитесь жить с позитивом и радостью в каждом дне! Более того, этими знаниями вы сможете всегда поделиться с близкими и родными! А приятным бонусом к курсу становятся три медитации, помогающие в работе с Вашим подсознанием и вы уже точно не вернётесь к предыдущему образу жизни!")

@dp.message(F.text == "нeт")
async def roma(message: types.Message):
    await message.answer("Странно. Вам нравится жить в тревожности и не знать, что вы можете управлять этим состоянием? От вашего благополучия и умения жить в гармонии, вас отделяет всего 6 занятий с психологом! А побочным эффектом работы над собой становится увеличение вашего дохода” Посмотрите, вдруг Вам станет интересно авторский курс “Версия 2.0 Перезагрузка” https://kursy.bryzgalina.com/maraphon_versiya_2.0 ")
    await message.answer("Обратите внимание, что данный курс создан для того, чтобы вы смогли обрести лучшую версию себя. Вы уже являетесь своей Версией 1.0. Так найдите себя лучше, чем вы есть сейчас и избавьтесь от стресса, тревожности, страхов, переживаний. Научитесь жить с позитивом и радостью в каждом дне! Более того, этими знаниями вы сможете всегда поделиться с близкими и родными! А приятным бонусом к курсу становятся три медитации, помогающие в работе с Вашим подсознанием и вы уже точно не вернётесь к предыдущему образу жизни!")

@dp.message(F.text == "Нет")
async def net(message: types.Message):
    if await check_subscription(message):
        await message.reply("Хм… Может вы хотите знать, какие причины возникновения тревожности? Ведь многие болезни возникают из-за тревожности. ",reply_markup= twd_kb2)
    else:
        await message.answer('Пожалуйста, подпишитесь на наш канал: <a href=""</a>', reply_markup=keyboard)
@dp.message(F.text == "нет")
async def da_net(message: types.Message):
    await message.answer("Тогда посмотрите вебинар “Выгорание в бизнесе и не только” по этой ссылке  ")


# Callback query handler for subscription check


# Run the bot
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())