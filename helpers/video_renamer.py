from pyrogram import Client, filters
#from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
#from urllib.parse import quote_plus, unquote
import math, os, time, datetime, aiohttp, asyncio, mimetypes, logging
from helpers.download_from_url import get_size
#from helpers.file_handler import send_to_transfersh_async, progress
#from hachoir.parser import createParser
#from hachoir.metadata import extractMetadata
from helpers.display_progress import progress_for_pyrogram, humanbytes
from helpers.tools import execute, clean_up
from helpers.ffprobe import stream_creator
from helpers.thumbnail_video import thumb_creator

logger = logging.getLogger(__name__)
status = False


async def rnv2(bot , u):
        
    global status
    file_path = None
    
    if not u.reply_to_message:
        await u.reply_text(text=f"𝐏𝐥𝐞𝐚𝐬𝐞 𝐫𝐞𝐩𝐥𝐲 𝐭𝐨 𝐚 𝐯𝐢𝐝𝐞𝐨 𝐟𝐢𝐥𝐞!\n\n𝐄𝐱𝐚𝐦𝐩𝐥𝐞:\n**/rnv | 𝐅𝐢𝐥𝐞𝐧𝐚𝐦𝐞**\n\nsee /help.", quote=True)
        return
    
    logger.info(f"status: {status}")
    if status:
        await u.reply_text(text=f"wait until last process finish. status: {status}", quote=True)
        return
    
    m = u.reply_to_message
    
    if m.video or m.document:
        ft = m.document or m.video
        fsize = get_size(ft.file_size)
    else:
        await m.reply_text(text=f"𝐏𝐥𝐞𝐚𝐬𝐞 𝐫𝐞𝐩𝐥𝐲 𝐭𝐨 𝐚 𝐯𝐢𝐝𝐞𝐨 𝐟𝐢𝐥𝐞!\n\n𝐄𝐱𝐚𝐦𝐩𝐥𝐞:\n**/rnv | 𝐅𝐢𝐥𝐞𝐧𝐚𝐦𝐞**\n\nsee /help.", quote=True)
        logger.info(f"No Video File !")
        return
    
    video_types = [
        '.avi', '.mkv', '.mp4', '.wmv', '.mpeg', '.3g2',
        '.divx', '.flv', '.webm', '.rm', '.mov', '.m4p',
        '.f4v', '.swf', '.html5', '.asf', '.ogv', '.divx',
        '.vob', '.m4v', '.mpg', '.mp2', '.3gp', '.mpv'
    ]
    
    if ft.mime_type and ft.mime_type.startswith("video/"):
        pass
    elif (ft.file_name) and (os.path.splitext(ft.file_name)[1] in video_types):
        pass
    else:
        await m.reply_text(text=f"Please Reply To Your Video !\n\nExample:\n**/rnv | filename**\n\nsee /help.", quote=True)
        logger.info(f"No Video File !")
        return
    
    tnow = str(datetime.datetime.now())
    tnow = tnow.replace(' ','_')
    tnow = tnow.replace('-','_')
    tnow = tnow.replace(':','_')
    tnow = tnow.replace('/','_')
    tnow = tnow.replace('.','_')
    print("tnow = ", tnow)
  
    oldname = "Video_CHATID" + str(m.chat.id) + "_DATE_" + str(tnow) + ".mp4"
    if ft.file_name:
        oldname = ft.file_name
        oldname = oldname.replace('%40','@')
        oldname = oldname.replace('%25','_')
        oldname = oldname.replace(' ','_')
  
    print("oldname = ", oldname)
    #########################
    args = u.text.split("|")
    if (len(args) <= 1) or (len(args) > 2):
        await m.reply_text(text=f"𝐖𝐡𝐚𝐭 𝐭𝐡𝐞 𝐡𝐞𝐥𝐥?\n\nExample:\n/rnv | filename\n\nsee /hlep.", quote=True)
        return
    #########################
    
    newname = u.text.split("|", 1)[1]
    newname = newname.strip()
    
    if os.path.splitext(newname)[1]:
        if os.path.splitext(newname)[1] in video_types:
            pass
        else:
            await m.reply_text(text=f"𝐔𝐬𝐞 𝐯𝐢𝐝𝐞𝐨 𝐞𝐱𝐭𝐞𝐧𝐬𝐢𝐨𝐧 𝐢𝐧 𝐟𝐢𝐥𝐞 𝐧𝐚𝐦𝐞!\n\n𝐄𝐱𝐚𝐦𝐩𝐥𝐞:**/rnv | 𝐅𝐢𝐥𝐞𝐧𝐚𝐦𝐞**\n\nsee /help.", quote=True)
            fsw = "app"
            return
    else:
        newname = newname + os.path.splitext(oldname)[1]
        logger.info(f"newname = {newname}")
    
    #################################################################### Downloading Video
    status = True
    logger.info(f"status: {status}")
    msg = await m.reply_text(text=f"⏳𝐃𝐨𝐰𝐧𝐥𝐨𝐚𝐝𝐢𝐧𝐠...", quote=True)
    
    c_time = time.time()
    file_path = await bot.download_media(
        m,
        file_name=oldname,
        progress=progress_for_pyrogram,
        progress_args=(
            "𝐃𝐨𝐰𝐧𝐥𝐨𝐚𝐝𝐢𝐧𝐠...:",
            msg,
            c_time
        )
    )
    if not file_path:
        await msg.edit(f"𝐅𝐚𝐢𝐥𝐞𝐝 𝐭𝐨 𝐝𝐨𝐰𝐧𝐥𝐨𝐚𝐝!")
        status = False
        logger.info(f"status: {status}")
        await clean_up(file_path)
    else:
        await msg.edit(f"🌄 𝐆𝐞𝐧𝐞𝐫𝐚𝐭𝐢𝐧𝐠 𝐭𝐡𝐮𝐦𝐛𝐧𝐚𝐢𝐥...")
        """
        probe = await stream_creator(file_path)
        video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
        width = int(video_stream['width'] if 'width' in video_stream else 0)
        height = int(video_stream['height'] if 'height' in video_stream else 0)
        thumbnail = await thumb_creator(file_path)
        duration = int(float(probe["format"]["duration"]))
        """
        
        thumbnail, duration, width, height = await thumb_creator(file_path)
        
        await msg.edit(f"𝐔𝐩𝐥𝐨𝐚𝐝𝐢𝐧𝐠 𝐯𝐢𝐝𝐞𝐨 ...")
        c_time = time.time()
        try:
            
            await bot.send_video(
                chat_id=m.chat.id,
                file_name=newname,
                video=file_path,
                width=width,
                height=height,
                duration=duration,
                thumb=str(thumbnail),
                caption=f"{newname} [{fsize}]",
                reply_to_message_id=m.message_id,
                progress=progress_for_pyrogram,
                progress_args=(
                    "𝐔𝐩𝐥𝐨𝐚𝐝𝐢𝐧𝐠 𝐕𝐢𝐝𝐞𝐨:",
                    msg,
                    c_time
                )
            )
            await msg.delete()
            status = False
            logger.info(f"status: {status}")
            await clean_up(file_path)
        except Exception as e:
            await msg.edit(f"❌ 𝐅𝐚𝐢𝐥𝐞𝐝 𝐭𝐨 𝐔𝐩𝐥𝐨𝐚𝐝 **𝐄𝐫𝐫𝐨𝐫:**\n\n{e}")
            status = False
            logger.info(f"status: {status}")
            await clean_up(file_path)
