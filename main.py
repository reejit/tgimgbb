from pyrogram import Client, filters
import requests
from dotenv import load_dotenv
from pyrogram.types import Message
import base64
import json
from imgbb.client import Client as cl
import os
import aiohttp

key = os.getenv('IMGBB')
load_dotenv()
session = aiohttp.ClientSession()
myclient = cl(key,session)

DOWNLOAD = "./"

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
    response = await myclient.post(file)
    url = response['data']['url']
    await message.reply_text(f"Your photo was successful uploaded!\nThe url of the image is {url}.")
  except Exception as e:
    await message.reply_text("Error:\n{}".format(e))
  os.remove(file)
Bot.run()

