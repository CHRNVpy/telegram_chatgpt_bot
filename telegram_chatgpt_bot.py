import datetime
import locale

import openai
import aiogram
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode

# Set up your OpenAI API key
openai.api_key = 'YOUR_OPENAI_TOKEN'

# Create a bot instance and set up the dispatcher
bot = Bot(token='YOUR_TELEGRAM_BOT_TOKEN')
dp = Dispatcher(bot)


# Define a handler function for the /start command
@dp.message_handler(commands=['start'])
async def start_command_handler(message: types.Message):
    """
    Sends a welcome message when the user starts the bot
    """
    welcome_message = "Hello! I'm an OpenAI-powered custom chatbot built by enthusiast. What can I help you with?" \
                      "Disclaimer: It's not an Openai product"
    await message.reply(welcome_message)


# Define a handler function for all other messages
@dp.message_handler()
async def message_handler(message: types.Message):
    """
    Processes the user's message using OpenAI API and sends the response back
    """
    if message.text.lower() == 'what date is today':
        locale.setlocale(locale.LC_TIME, 'en_US.UTF-8')
        response_text = f'Today is {datetime.datetime.today().strftime("%A %d %B %Y")}'
    elif message.text.lower() == 'какой сегодня день':
        locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')
        response_text = f'Сегодня {datetime.datetime.today().strftime("%A %d %B %Y")} года'
    else:
        # Use OpenAI API to generate a response to the user's message
        response = openai.ChatCompletion.create(
              model="gpt-3.5-turbo",
              messages=[
                    #{"role": "system", "content": "You are a helpful assistant."},
                    #{"role": "user", "content": "Who won the world series in 2020?"},
                    {"role": "assistant", "content": message.text}
                    #{"role": "user", "content": "Where was it played?"}
                ]
)

        # Extract the response text from the API response
        response_text = response.choices[0]['message']['content']

    # Send the response back to the user
    await message.reply(response_text, parse_mode=ParseMode.HTML)

# Start the bot
if __name__ == '__main__':
    try:
        aiogram.executor.start_polling(dp, skip_updates=True)
    except Exception:
        print('Oops, something went wrong !')