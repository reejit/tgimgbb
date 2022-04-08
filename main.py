import os
from pyrogram import Client, filters
from imgbbpy.aio import Client as cl
from dotenv import load_dotenv
from pyrogram.types import Message

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
  imgbb = cl(os.environ.get('IMGBB'))
  file = await bot.download_media(message, DOWNLOAD)
  try:
    image = await imgbb.upload(file)
    await message.reply_text(f"Your photo was successful uploaded!\nThe url of the image is {image.url}.")
    await imgbb.close()
  except Exception as e:
    await message.reply_text("Error:\n{}".format(e))
  os.remove(file)
Bot.run()

