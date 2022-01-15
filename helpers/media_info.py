from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from urllib.parse import quote_plus, unquote
from helpers.download_from_url import download_file, get_size
from helpers.file_handler import send_to_transfersh_async, progress
from hachoir.parser import createParser
from hachoir.metadata import extractMetadata
from helpers.display_progress import progress_for_pyrogram, humanbytes
import os, math, time, datetime, aiohttp, asyncio, mimetypes,logging
from helpers.tools import execute
from helpers.ffprobe import stream_creator
from helpers.thumbnail_video import thumb_creator

logger = logging.getLogger(__name__)

async def cinfo2(bot , m):
   
   ft = m.audio or m.video or m.document
   fsize = get_size(ft.file_size)
   if ft.mime_type and ft.mime_type.startswith("audio/"):
      if ft.file_name:
         fn = str(ft.file_name)
      else:
         fn = "𝐅𝐢𝐥𝐞 𝐧𝐚𝐦𝐞 𝐧𝐨𝐭 𝐝𝐞𝐭𝐞𝐜𝐭𝐞𝐝!"
      if m.document:
         #await m.reply_text(text=f"📋 𝐋𝐢𝐧𝐤 𝐢𝐧𝐟𝐨:\n\n𝐅𝐢𝐥𝐞: `{cfname}`\nMime-Type: `{mt}`\n𝐒𝐢𝐳𝐞: `{url_size}`\n\n𝐔𝐬𝐞 /upload as reply to your link, it will upload your link to telegram.\n\nSee /help.", quote=True)
         await m.reply_text(text=f"📋 𝐌𝐞𝐝𝐢𝐚 𝐢𝐧𝐟𝐨:\n\n𝐅𝐢𝐥𝐞: `{fn}`\nMime-Type: {ft.mime_type}\n𝐒𝐢𝐳𝐞: `{fsize}`\n\n𝐔𝐬𝐞 /rna to rename and edit audio tags.\n\nSee /help.", quote=True)
         return
      if m.audio.title:
         tt = str(ft.title)
      else:
         tt = "𝐓𝐢𝐭𝐥𝐞 𝐧𝐨𝐭 𝐝𝐞𝐭𝐞𝐜𝐭𝐞𝐝!"
      if m.audio.performer:
         pf = str(ft.performer)
      else:
         pf = "𝐍𝐨 𝐚𝐫𝐭𝐢𝐬𝐭(𝐬) 𝐃𝐞𝐭𝐞𝐜𝐭𝐞𝐝!"
      await m.reply_text(text=f"📋 𝐌𝐞𝐝𝐢𝐚 𝐢𝐧𝐟𝐨:\n\n𝐅𝐢𝐥𝐞: `{fn}`\nMime-Type: `{ft.mime_type}`\n𝐓𝐢𝐭𝐥𝐞: `{tt}`\n𝐀𝐫𝐭𝐢𝐬𝐭: `{pf}`\nSize: `{fsize}`\n\nUse /rna to rename and edit audio tags.\n\nSee /help.", quote=True)
   elif ft.mime_type and ft.mime_type.startswith("video/"):
      if ft.file_name:
         fn = str(ft.file_name)
      else:
         fn = "No File Name Detected!"
      await m.reply_text(text=f"📋 𝐌𝐞𝐝𝐢𝐚 𝐢𝐧𝐟𝐨:\n\n𝐅𝐢𝐥𝐞: `{fn}`\nMime-Type: `{ft.mime_type}`\n𝐒𝐢𝐳𝐞: `{fsize}`\n\n𝐔𝐬𝐞 /c2v to convert or /rnv to rename this video.\n\nSee /help.", quote=True)
   else:
      if ft.file_name:
         fn = str(ft.file_name)
      else:
         fn = "No File Name Detected!"
      await m.reply_text(text=f"📋 𝐌𝐞𝐝𝐢𝐚 𝐢𝐧𝐟𝐨:\n\n𝐅𝐢𝐥𝐞: `{fn}`\nMime-Type: `{ft.mime_type}`\n𝐒𝐢𝐳𝐞: `{fsize}`\n\n𝐔𝐬𝐞 /rnf to rename this file.\n\nSee /help.", quote=True)
