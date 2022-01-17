from pyrogram import Client, filters
#from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
#from urllib.parse import quote_plus, unquote
#import math
from helpers.download_from_url import get_size
#from helpers.file_handler import send_to_transfersh_async, progress
#from hachoir.parser import createParser
#from hachoir.metadata import extractMetadata
from helpers.display_progress import progress_for_pyrogram, humanbytes
import os, time, datetime, aiohttp, asyncio, mimetypes, logging
from helpers.tools import execute, clean_up
#from helpers.ffprobe import stream_creator
#from helpers.thumbnail_video import thumb_creator

logger = logging.getLogger(__name__)
status = False

async def rnf2(bot , u):
  
  global status
  file_path = None
  
  if not u.reply_to_message:
    await u.reply_text(text=f"𝐏𝐥𝐞𝐚𝐬𝐞 𝐫𝐞𝐩𝐥𝐲 𝐭𝐨 𝐲𝐨𝐮𝐫 𝐝𝐨𝐜𝐮𝐦𝐞𝐧𝐭 !\n\n𝐄𝐱𝐚𝐦𝐩𝐥𝐞:\n**/rnf | filename.ext**\n\n𝐬𝐞𝐞 /help.", quote=True)
    return
  
  logger.info(f"status: {status}")
  if status:
    await u.reply_text(text=f"wait until last process finish. status: {status}", quote=True)
    return
  
  m = u.reply_to_message
  
  if m.video:
    ft = m.video
  elif m.audio:
    ft = m.audio
  elif m.document:
    ft = m.document
  else:
    await m.reply_text(text=f"𝐏𝐥𝐞𝐚𝐬𝐞 𝐫𝐞𝐩𝐥𝐲 𝐭𝐨 (audio-video-document) 𝐟𝐢𝐥𝐞𝐬!\n\n𝐒𝐞𝐞 /help", quote=True)
    return

  fsize = get_size(ft.file_size)
  
  if not "|" in u.text:
    await m.reply_text(text=f"𝐏𝐥𝐞𝐚𝐬𝐞 𝐬𝐞𝐧𝐝 𝐧𝐞𝐰 𝐟𝐢𝐥𝐞 𝐭𝐲𝐩𝐞 𝐰𝐢𝐭𝐡 𝐞𝐱𝐭𝐞𝐧𝐬𝐢𝐨𝐧!\n\n𝐄𝐱𝐚𝐦𝐩𝐥𝐞:\n**/rnf | filename.ext**\n\n𝐬𝐞𝐞 /help.", quote=True)
    return
  else:
    args = u.text.split("|")
    if len(args) == 2:
      cmd , newname = u.text.split("|", 1)
      newname = newname.strip()
      if not os.path.splitext(newname)[1]:
        await m.reply_text(text=f"𝐓𝐲𝐩𝐞 𝐞𝐱𝐭𝐞𝐧𝐬𝐢𝐨𝐧 !\n\n𝐄𝐱𝐚𝐦𝐩𝐥𝐞:\n**/rnf | filename.ext\n\n𝐬𝐞𝐞 /help.**", quote=True)
        return
      else:
        tnow = str(datetime.datetime.now())
        tnow = tnow.replace(' ','_')
        tnow = tnow.replace('-','_')
        tnow = tnow.replace(':','_')
        tnow = tnow.replace('/','_')
        tnow = tnow.replace('.','_')
        print("tnow = ", tnow)
        
        ext = os.path.splitext(newname)[1]
        oldname = "File_CHATID" + str(m.chat.id) + "_DATE_" + str(tnow) + str(ext)
        if ft.file_name:
            oldname = ft.file_name
            oldname = oldname.replace('%40','@')
            oldname = oldname.replace('%25','_')
            oldname = oldname.replace(' ','_')

        print("oldname = ", oldname)
        msg = await m.reply_text(text=f"⬇️ 𝐃𝐨𝐰𝐧𝐥𝐨𝐚𝐝𝐢𝐧𝐠 𝐝𝐨𝐜𝐮𝐦𝐞𝐧𝐭", quote=True)
        
        #################################################################### Downloading Document
        status = True
        logger.info(f"status: {status}")
        
        c_time = time.time()
        file_path = await bot.download_media(
          m,
          file_name=oldname,
          progress=progress_for_pyrogram,
          progress_args=(
            "⬇️ 𝐃𝐨𝐰𝐧𝐥𝐨𝐚𝐝𝐢𝐧𝐠 𝐝𝐨𝐜𝐮𝐦𝐞𝐧𝐭:",
            msg,
            c_time
          )
        )
        if not file_path:
          status = False
          logger.info(f"status: {status}")
          await msg.edit(f"❌ 𝐃𝐨𝐰𝐧𝐥𝐨𝐚𝐝𝐢𝐦𝐠 𝐟𝐚𝐢𝐥𝐞𝐝 !")
          await clean_up(file_path)
          return
        try:
          await msg.edit(f"𝐔𝐩𝐥𝐨𝐚𝐝𝐢𝐧𝐠 𝐝𝐨𝐜𝐮𝐦𝐞𝐧𝐭 ...")
          c_time = time.time()
          await bot.send_document(
            chat_id=m.chat.id,
            file_name=newname,
            document=file_path,
            force_document=True,
            caption=f"{newname} [{fsize}]",
            reply_to_message_id=m.message_id,
            progress=progress_for_pyrogram,
            progress_args=(
              "𝐔𝐩𝐥𝐨𝐚𝐝𝐢𝐧𝐠 𝐃𝐨𝐜𝐮𝐦𝐞𝐧𝐭:",
              msg,
              c_time
            )
          )
          status = False
          logger.info(f"status: {status}")
          await msg.delete()
          await clean_up(file_path)
        except Exception as e:
          await msg.edit(f"❌ 𝐅𝐚𝐢𝐥𝐞𝐝 𝐭𝐨 𝐮𝐩𝐥𝐨𝐚𝐝 𝐝𝐨𝐜𝐮𝐦𝐞𝐧𝐭 **𝐄𝐫𝐫𝐨𝐫:**\n\n{e}")
          status = False
          logger.info(f"status: {status}")
          await clean_up(file_path)
    else:
      await m.reply_text(text=f"𝗪𝗵𝗮𝘁 𝘁𝗵𝗲 𝗵𝗲𝗹𝗹?\n\n𝗘𝘅𝗮𝗺𝗽𝗹𝗲:\n/rnf | filename.ext\n\n𝘀𝗲𝗲 /hlep.", quote=True)
      return
