from pyrogram import Client, filters
#from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
#from urllib.parse import quote_plus, unquote
from helpers.download_from_url import download_file, get_size
#from helpers.file_handler import send_to_transfersh_async, progress
#from hachoir.parser import createParser
#from hachoir.metadata import extractMetadata
from helpers.display_progress import progress_for_pyrogram, humanbytes
import os, time, datetime, aiohttp, asyncio, mimetypes, logging, math
from helpers.tools import execute, clean_up
from helpers.ffprobe import stream_creator
#from helpers.thumbnail_video import thumb_creator

logger = logging.getLogger(__name__)
status = False


async def rna2(bot , u):
  
  global status
  file_path = None
  
  if not u.reply_to_message:
    await u.reply_text(text=f"𝐏𝐥𝐞𝐚𝐬𝐞 𝐫𝐞𝐩𝐥𝐲 𝐭𝐨 𝐲𝐨𝐮𝐫 𝐚𝐮𝐝𝐢𝐨 !\n\n𝐄𝐱𝐚𝐦𝐩𝐥𝐞:\n**/rna | 𝐟𝐢𝐥𝐞𝐧𝐚𝐦𝐞**\n\n𝐬𝐞𝐞 /help.", quote=True)
    return
  
  logger.info(f"status: {status}")
  if status:
    await u.reply_text(text=f"𝐖𝐚𝐢𝐭 𝐮𝐧𝐭𝐢𝐥𝐥 𝐥𝐚𝐬𝐭 𝐩𝐫𝐨𝐜𝐞𝐬𝐬 𝐭𝐨 𝐟𝐢𝐧𝐢𝐬𝐡. 𝐭𝐡𝐞𝐧 𝐭𝐫𝐲 𝐚𝐠𝐚𝐢𝐧.", quote=True)
    return

  m = u.reply_to_message
  
  if m.audio or m.document:
    ft = m.document or m.audio
    fsize = get_size(ft.file_size)
  else:
    await m.reply_text(text=f"𝐏𝐥𝐞𝐚𝐬𝐞 𝐫𝐞𝐩𝐥𝐲 𝐭𝐨 𝐲𝐨𝐮𝐫 𝐚𝐮𝐝𝐢𝐨 !\n\n𝐬𝐞𝐞 /help", quote=True)
    logger.info(f"No Audio File !")
    return
  
  audio_types = ['.aac', '.m4a', '.mp3', '.wma', '.mka', '.wav', '.oga', '.ogg', '.ra', '.flac', '.amr', '.opus', '.alac', '.aiff']
  
  if ft.mime_type and ft.mime_type.startswith("audio/"):
    pass
  elif (ft.file_name) and (os.path.splitext(ft.file_name)[1] in audio_types):
    pass
  else:
    await m.reply_text(text=f"𝐏𝐥𝐞𝐚𝐬𝐞 𝐫𝐞𝐩𝐥𝐲 𝐭𝐨 𝐲𝐨𝐮𝐫 𝐚𝐮𝐝𝐢𝐨 !\n\n𝐒𝐞𝐞 /help", quote=True)
    logger.info(f"No Audio File !")
    return
  
  tnow = str(datetime.datetime.now())
  tnow = tnow.replace(' ','_')
  tnow = tnow.replace('-','_')
  tnow = tnow.replace(':','_')
  tnow = tnow.replace('/','_')
  tnow = tnow.replace('.','_')
  print("tnow = ", tnow)
  
  oldname = "Audio_CHATID" + str(m.chat.id) + "_DATE_" + str(tnow) + ".mp3"
  if ft.file_name:
    oldname = ft.file_name
    oldname = oldname.replace('%40','@')
    oldname = oldname.replace('%25','_')
    oldname = oldname.replace(' ','_')
  
  print("oldname = ", oldname)
  #########################
  args = u.text.split("|")
  if len(args) <= 1:
    await m.reply_text(text=f"𝐰𝐡𝐚𝐭 𝐭𝐡𝐞 𝐡𝐞𝐥𝐥 ?\n\n𝐄𝐱𝐚𝐦𝐩𝐥𝐞:\n`/rna | 𝐟𝐢𝐥𝐞𝐧𝐚𝐦𝐞`\n\n𝐬𝐞𝐞 /hlep.", quote=True)
    return
  #########################
  if len(args) == 2:
    cmd, newname = u.text.split("|", 1)
    newname = newname.strip()
    if newname == "-":
      await m.reply_text(text=f"𝐰𝐡𝐚𝐭 𝐭𝐡𝐞 𝐡𝐞𝐥𝐥 ?\n\n𝐄𝐱𝐚𝐦𝐩𝐥𝐞:\n`/rna | 𝐟𝐢𝐥𝐞𝐧𝐚𝐦𝐞`\n\n𝐬𝐞𝐞 /hlep.", quote=True)
      return
                  
    if m.audio and m.audio.title:
      newtitle = m.audio.title
    else:
      newtitle = None
    if m.audio and m.audio.performer:
      newartist = m.audio.performer
    else:
      newartist = None
  
  elif len(args) == 3:
    cmd, newname, newtitle = u.text.split("|", 2)
    newname = newname.strip()
    newtitle = newtitle.strip()
                  
    if newname == "-":
      if newtitle == "-":
        await m.reply_text(text=f"𝐰𝐡𝐚𝐭 𝐭𝐡𝐞 𝐡𝐞𝐥𝐥?\n\n𝐄𝐱𝐚𝐦𝐩𝐥𝐞:\n`/rna | 𝐟𝐢𝐥𝐞𝐧𝐚𝐦𝐞`\n\n𝐬𝐞𝐞 /hlep.", quote=True)
        return  
                  
    if newname == "-":
      newname = os.path.splitext(oldname)[0]
          
    if newtitle == "-":
      if m.audio and m.audio.title:
        newtitle = m.audio.title
      else:
        newtitle = None
      if m.audio and m.audio.performer:
        newartist = m.audio.performer
      else:
        newartist = None
  
  elif len(args) == 4:
    cmd, newname, newtitle, newartist = u.text.split("|", 3)
    newname = newname.strip()
    newtitle = newtitle.strip()
    newartist = newartist.strip()
    if newname == "-":
      if newtitle == "-":
        if newartist == "-":
          await m.reply_text(text=f"𝐰𝐡𝐚𝐭 𝐭𝐡𝐞 𝐡𝐞𝐥𝐥?\n\n𝐄𝐱𝐚𝐦𝐩𝐥𝐞:\n`/rna | 𝐟𝐢𝐥𝐞𝐧𝐚𝐦𝐞`\n\n𝐬𝐞𝐞 /help.", quote=True)
          return
          
    if newname == "-":
      newname = os.path.splitext(oldname)[0]
                    
    if newtitle == "-":
      if m.audio and m.audio.title:
        newtitle = m.audio.title
      else:
        newtitle = None
    
    if newartist == "-":
      if m.audio and m.audio.performer:
        newartist = m.audio.performer
      else:
        newartist = None

  else:
    await m.reply_text(text=f"𝐓𝐫𝐲 𝐚𝐠𝐚𝐢𝐧 !\n\n𝐄𝐱𝐚𝐦𝐩𝐥𝐞:\n**/rna | 𝐅𝐢𝐥𝐞𝐧𝐚𝐦𝐞**\n**/rna | 𝐅𝐢𝐥𝐞𝐧𝐚𝐦𝐞 | 𝐭𝐢𝐭𝐥𝐞(𝐨𝐩𝐭𝐢𝐨𝐧𝐚𝐥) | 𝐚𝐫𝐭𝐢𝐬𝐭𝐬(𝐨𝐩𝐭𝐢𝐨𝐧𝐚𝐥)**", quote=True)
    return

  if os.path.splitext(newname)[1]:
    if os.path.splitext(newname)[1] in audio_types:
      pass
    else:
      await m.reply_text(text=f"𝐔𝐬𝐞 𝐚𝐮𝐝𝐢𝐨 𝐞𝐱𝐭𝐞𝐧𝐬𝐢𝐨𝐧 𝐟𝐨𝐫 𝐧𝐞𝐰 𝐧𝐚𝐦𝐞 !\n\n𝐄𝐱𝐚𝐦𝐩𝐥𝐞:\n**/rna | 𝐟𝐢𝐥𝐞𝐧𝐚𝐦𝐞**\n**/rna | 𝐟𝐢𝐥𝐞𝐧𝐚𝐦𝐞 | 𝐭𝐢𝐭𝐥𝐞(𝐨𝐩𝐭𝐢𝐨𝐧𝐚𝐥) | 𝐚𝐫𝐭𝐢𝐬𝐭𝐬(𝐨𝐩𝐭𝐢𝐨𝐧𝐚𝐥)**", quote=True)
      fsw = "app"
      return
  else:
    newname = newname + os.path.splitext(oldname)[1]
    logger.info(f"newname = {newname}")
    
  #################################################################### Downloading Audio
  
  status = True
  logger.info(f"status: {status}")
  
  msg = await m.reply_text(text=f"⬇️ 𝐓𝐫𝐲𝐢𝐧𝐠 𝐭𝐨 𝐝𝐨𝐰𝐧𝐥𝐨𝐚𝐝 𝐚𝐮𝐝𝐢𝐨", quote=True)

  c_time = time.time()
  file_path = await bot.download_media(
    m,
    file_name=oldname,
    progress=progress_for_pyrogram,
    progress_args=(
      "⬇️ 𝐃𝐨𝐰𝐧𝐥𝐨𝐚𝐝𝐢𝐧𝐠 𝐚𝐮𝐝𝐢𝐨:",
      msg,
      c_time
    )
  )
  logger.info(f"file_path: {file_path}")
  if not file_path:
    status = False
    await msg.edit(f"❌ 𝐃𝐨𝐰𝐧𝐥𝐨𝐚𝐝𝐢𝐧𝐠 𝐟𝐚𝐢𝐥𝐞𝐝!")
    logger.info(f"status: {status}")
    await clean_up(file_path)
    return
  else:
    if m.audio and m.audio.duration:
      duration = m.audio.duration
    else:
      duration = 0
      probe = await stream_creator(file_path)
      #logger.info(probe)
      duration = int(float(probe["format"]["duration"]))
      ptlist = list(probe["format"]["tags"].keys())
      if "title" in ptlist:
        if not newtitle:
          newtitle = probe["format"]["tags"]["title"]
      if "artist" in ptlist:
        if not newartist:
          newartist = probe["format"]["tags"]["artist"]

    await msg.edit(f"⬆️ 𝐔𝐩𝐥𝐨𝐚𝐝𝐢𝐧𝐠 𝐚𝐮𝐝𝐢𝐨 ...")
      
    c_time = time.time()
    try:
      await bot.send_audio(
        chat_id=m.chat.id,
        file_name=newname,
        performer=newartist,
        title=newtitle,
        duration=duration,
        audio=file_path,
        caption=f"**File:** `{newname}`\n**Title:** `{newtitle}`\n**Artist(s):** `{newartist}`\n**Size:** {fsize}",
        reply_to_message_id=m.message_id,
        progress=progress_for_pyrogram,
        progress_args=(
          f"⬆️ 𝐔𝐩𝐥𝐨𝐚𝐝𝐢𝐧𝐠 𝐚𝐬 𝐚𝐮𝐝𝐢𝐨:",
          msg,
          c_time
        )
      )
      await msg.delete()
      status = False
      logger.info(f"status: {status}")
      await clean_up(file_path)
    except Exception as e:
      status = False
      logger.info(f"status: {status}")
      await msg.edit(f"❌ 𝐔𝐩𝐥𝐨𝐚𝐝𝐢𝐧𝐠 𝐚𝐬 𝐚𝐮𝐝𝐢𝐨 𝐟𝐚𝐢𝐥𝐞𝐝 **𝐄𝐫𝐫𝐨𝐫:**\n\n{e}")
      await clean_up(file_path)
