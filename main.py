from aiogram import Dispatcher, Bot, executor, types
from config import API_KEY
import database

bot = Bot(API_KEY)
dp = Dispatcher(bot)

database.init_db()


async def set_commands(bot: Bot):
    commands = [
        types.BotCommand(command='/start', description='Запуск'),
        types.BotCommand(command='/help', description='Помощь')
    ]

    await bot.set_my_commands(commands)

@dp.message_handler(commands='start')
async def start(message: types.Message):
    await message.reply('Привет')

@dp.message_handler(commands='help')
async def help(message: types.Message):
    await message.reply('С помощью команды /add - ты сможешь добавить элемент'
                        '\nС помощью команды /delete - ты сможешь удалить элемент\n'
                        'С помощью команды /list - ты сможешь просмотреть список элементов')

# @dp.message_handler(commands='add')
# async def add(message: types.Message):
#     task = message.get_args()
#     if task:
#         user_id = message.from_user.id
#         username = message.from_user.username
#         database.add_task(user_id, username, task)
#         await message.reply(f"Задача '{task}' добавлена")
#     else:
#         await message.reply('Пожалуйста, укажите задачу через команду /add')


@dp.message_handler(commands='add')
async def add(message: types.Message):
    task = message.get_args()
    if task:
        user_id = message.from_user.id
        username = message.from_user.username
        if database.add_task(user_id, username, task):
            await message.reply(f"Задача '{task}' добавлена")
        else:
            await message.reply(f"Задача '{task}' уже существует")
    else:
        await message.reply('Пожалуйста, укажите задачу через команду /add')

@dp.message_handler(commands='list')
async def add(message: types.Message):
    tasks = database.get_task()
    if tasks:
        tasks_list ="\n".join([f"{task[0]}. {task[3]} (Добавлена пользователем @{task[2]})" for task in tasks])
        await message.reply(f"Ваши задачи:\n{tasks_list}")
    else:
        await message.reply("У вас нет задач")

@dp.message_handler(commands=['delete'])
async def delete_task(message: types.Message):
    task_id = message.get_args()
    if task_id.isdigit():
        task_id = int(task_id)
        database.delete_task(task_id)
        await message.reply(f"Задача {task_id} удалена.")
    else:
        await message.reply("Пожалуйста, укажите корректный ID задачи после команды /delete.")

async def on_startup(dispatcher):
    await set_commands(dispatcher.bot)

if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
