import os
from aiogram import Bot,Dispatcher,executor,types
from dotenv import load_dotenv
import openai
import sys

class Reference:
    """
    A class to store previous respons from chatGPT
    """
    def __init__(self) ->None:
        self.response = ""

#load environment variables

load_dotenv()

## setup OpenAI API KEY
openai.api_key=os.getenv("OPENAI_API_KEY")

# create reference object
reference =Reference()
## BOT token can be obtainedd t.me/telebot32_bot
TOKEN=os.getenv("TOKEN")
MODEL_NAME = "gpt-3.5-turbo"

# Initialize bot and dispatcher
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

def clear_past():
    """
    A function to clear the previous conversation and contents
    """
    reference.response = ""

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start`  command
    """
    clear_past()
    await message.reply("Hi!\nI'm chatGPt Telegram  Bot!\nPowered by TSDhope..How can I help you?")



@dp.message_handler(commands=['clear'])
async def clear(message: types.Message):
    
    clear_past()
    await message.reply(" i have cleared the past conversation and context")

@dp.message_handler(commands=['help'])
async def helper(message: types.Message):
    """
    This handler will be used to display the help menu
    """
    help_commands=""" hi there,I'm ChatGPt telegram bot created by TSDHOPE,Pl follow the commnds
    /Start-To start the conversation
    /clear - To clear previous conversation and context
    /help - To help
    I hope this will help you out

    """
    await message.reply(help_command)


@dp.message_handler()
async def chatgpt(message: types.Message):
    """
    A handler to process the user's input and generate a response using the chatGPT API.
    """
    print(f">>> USER: \n\t{message.text}")
    response = openai.ChatCompletion.create(
        model = MODEL_NAME,
        messages = [
            {"role": "assistant", "content": reference.response}, # role assistant
            {"role": "user", "content": message.text} #our query 
        ]
    )
    reference.response = response['choices'][0]['message']['content']
    print(f">>> chatGPT: \n\t{reference.response}")
    await bot.send_message(chat_id = message.chat.id, text = reference.response)



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)