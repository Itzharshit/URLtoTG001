#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from main import Config
from pyrogram import filters
from pyrogram import Client
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from urllib.parse import quote_plus, unquote
import math, os, time, datetime, aiohttp, asyncio, mimetypes, logging
from helpers.download_from_url import download_file, get_size
from helpers.file_handler import send_to_transfersh_async, progress
from hachoir.parser import createParser
from hachoir.metadata import extractMetadata
from helpers.display_progress import progress_for_pyrogram, humanbytes
from helpers.tools import execute
from helpers.ffprobe import stream_creator
from helpers.thumbnail_video import thumb_creator
from helpers.url_uploader import leecher2
from helpers.video_renamer import rnv2
from helpers.audio_renamer import rna2
from helpers.file_renamer import rnf2
from helpers.vconverter import to_video2
from helpers.media_info import cinfo2
from helpers.link_info import linfo2

logger = logging.getLogger(__name__)

HELP_TXT = """
/upload : reply to your url to upload your link to telegram.
/c2v : reply to your document to convert it into video.
/rnv : reply to your video to rename.
Eg:- /rnv | videoname.ext

/rna : reply to your audio to edit audio tag. \"-\" : leave without change.
/rna | audioname | title | artists
/rna | audioname
/rna | - | title
/rna | - | - | artists
/rnf : reply to your document to rename. Eg:- /rnf | filename.ext
"""

@Client.on_message(filters.command("start") & filters.private)
async def start(_, message):
   user = message.from_user.mention
   return await message.reply_text(f"""𝗛𝗶𝗶 {user},\n𝗜 𝗮𝗺 𝗨𝗥𝗟 𝘂𝗽𝗹𝗼𝗮𝗱𝗲𝗿 𝗕𝗼𝘁.
𝗜 𝗰𝗮𝗻 𝗱𝗼 𝗮 𝗹𝗼𝘁 𝗼𝗳 𝘁𝗵𝗶𝗻𝗴𝘀 𝗶𝗻𝗰𝗹𝘂𝗱𝗶𝗻𝗴 𝘂𝗽𝗹𝗼𝗮𝗱𝗶𝗻𝗴 𝗨𝗥𝗟.""",
    reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("𝙎𝙪𝙥𝙥𝙤𝙧𝙩 𝙂𝙧𝙤𝙪𝙥", url="https://t.me/+7ScFy39Vckk5MWQ1"),
                     InlineKeyboardButton("𝙐𝙥𝙙𝙖𝙩𝙚𝙨 𝘾𝙝𝙖𝙣𝙣𝙚𝙡", url="https://t.me/pyrogrammers")],
                    [InlineKeyboardButton("𝙔𝙤𝙪𝙏𝙪𝙗𝙚 𝘾𝙝𝙖𝙣𝙣𝙚𝙡", url="https://youtube.com/channel/UC2anvk7MNeNzJ6B4c0SZepw")]
                ])
            )
    
@Client.on_message(filters.command(["help"]))
async def help(client , m):
    """Send a message when the command /help is issued."""
    await m.reply_text(text=f"{HELP_TXT}")   

@Client.on_message(filters.private & filters.command(["rnv"]))
async def rnv1(client , u):
        await rnv2(client , u)
    
    
@Client.on_message(filters.private & filters.command(["rna"]))
async def rna1(client , u):
        await rna2(client , u)
  

@Client.on_message(filters.private & filters.command(["rnf"]))
async def rnf1(client , u):
        await rnf2(client , u) 
   
   
@Client.on_message(filters.private & filters.command(["c2v"]))
async def to_video1(client , u):
        await to_video2(client , u) 
    
    
@Client.on_message(filters.private & (filters.audio | filters.document | filters.video))
async def cinfo1(client , m):
    await cinfo2(client , m)


@Client.on_message(filters.private & filters.incoming & filters.text & (filters.regex('^(ht|f)tp*')))
async def linfo1(client , m):
    await linfo2(client , m)

@Client.on_message(filters.private & filters.command(["upload"]))
async def leecher1(client , u):
        await leecher2(client , u)
    
