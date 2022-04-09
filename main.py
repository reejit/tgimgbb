import os
from pyrogram import Client, filters
import requests
from dotenv import load_dotenv
from pyrogram.types import Message
import base64
import json

download = "./"
load_dotenv()

Bot = Client(
           api_id = os.environ.get("API_ID"),
           api_hash= os.environ.get("API_HASH"),
           bot_token = os.environ.get("TOKEN"),
           session_name = ':memory:'
) 

@Bot.on_message(filters.command("start") & filters.private)
async def start(client: Client, message: Message):
   await client.delete_messages(
                       chat_id=message.chat.id,
                       message_ids=message.message_id
   )
   await message.reply_text(f"""
Hello {message.from_user.first_name}!
I am a Image Uploader Bot!
Send me a picture to get started.
"""
   )

@Bot.on_message(filters.photo & filters.private)
async def upload_(client: Client, message: Message):
  
  file = await bot.download_media(message, DOWNLOAD)
  try:
    with open(file, "rb") as file:
    url = "https://api.imgbb.com/1/upload"
    payload = {
        "key": os.environ.get('IMGBB'),
        "image": base64.b64encode(file.read()),
    }
    res = requests.post(url, payload).json
    url = res['data']['url']
    await message.reply_text(f"Your photo was successful uploaded!\nThe url of the image is {url}.")
    await imgbb.close()
  except Exception as e:
    await message.reply_text("Error:\n{}".format(e))
  os.remove(file)
Bot.run()

