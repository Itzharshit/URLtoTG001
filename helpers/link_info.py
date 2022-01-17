import requests, os, mimetypes, json, logging
from helpers.download_from_url import get_size
from requests.exceptions import RequestException
from urllib.parse import unquote

logger = logging.getLogger(__name__)

async def linfo2(bot , m):
    
  if ("youtube.com" in m.text) or ("youtu.be" in m.text):
    await m.reply_text(text=f"𝐘𝐨𝐮𝐓𝐮𝐛𝐞 𝐋𝐢𝐧𝐤. 𝐔𝐬𝐞 /upload.", quote=True)
    return
  
  if "|" in m.text:
    url , cfname = m.text.split("|", 1)
    url = url.strip()
    cfname = cfname.strip()
    cfname = cfname.replace('%40','@')
    mt = mimetypes.guess_type(str(cfname))[0]
  elif 'drive.google.com' in m.text:
    url = m.text
    r = requests.get(url, allow_redirects=True, stream=True)
    fn = str(r.text)
    if "\'title\':" in fn:
        fn = fn.split('window.viewerData')[-1].split('configJson')[0]
        fn = fn.split("\'title\': \'", 1)[1]
        fn = fn.strip()
        fn = fn.split("\',", 1)[0]
    #logger.info(r.text)
    logger.info(fn)
    await m.reply_text(text=f"📋 𝐋𝐢𝐧𝐤 𝐢𝐧𝐟𝐨:\n\n𝐅𝐢𝐥𝐞: {fn}\n\n𝐔𝐬𝐞 /upload.\n\n𝐒𝐞𝐞 /help.", quote=True)
    return
  else:
    url = m.text.strip()
    if os.path.splitext(url)[1]:
      cfname = unquote(os.path.basename(url))
      mt = mimetypes.guess_type(str(url))[0]
    else:
      try:
        r = requests.get(url, allow_redirects=True, stream=True)
        if "Content-Disposition" in r.headers.keys():
          cfname = r.headers.get("Content-Disposition")
          cfname = cfname.split("filename=")[1]
          if '\"' in cfname:
            cfname = cfname.split("\"")[1]
          mt = mimetypes.guess_type(str(cfname))[0]
        else:
          await m.reply_text(text=f"𝐈 𝐜𝐨𝐮𝐥𝐝 𝐧𝐨𝐭 𝐝𝐞𝐭𝐞𝐫𝐦𝐢𝐧𝐞 𝐭𝐡𝐞 𝐟𝐢𝐥𝐞 𝐭𝐲𝐩𝐞 !\n𝐏𝐥𝐞𝐚𝐬𝐞 𝐮𝐬𝐞 𝐜𝐮𝐬𝐭𝐨𝐦 𝐟𝐢𝐥𝐞𝐧𝐚𝐦𝐞\n\n𝐒𝐞𝐞 /help.", quote=True)
          return
      except RequestException as e:
        await m.reply_text(text=f"𝐄𝐫𝐫𝐨𝐫:\n\n{e}", quote=True)
        return
        
  r = requests.get(url, allow_redirects=True, stream=True)
  url_size = int(r.headers.get("content-length", 0))
  url_size = get_size(url_size)

  await m.reply_text(text=f"📋 𝐋𝐢𝐧𝐤 𝐢𝐧𝐟𝐨:\n\n𝐅𝐢𝐥𝐞: {cfname}\nMime-Type: {mt}\n𝐒𝐢𝐳𝐞: {url_size}\n\n𝐔𝐬𝐞 /upload 𝐚𝐬 𝐫𝐞𝐩𝐥𝐲 𝐭𝐨 𝐲𝐨𝐮𝐫 𝐥𝐢𝐧𝐤, 𝐢𝐭 𝐰𝐢𝐥𝐥 𝐮𝐩𝐥𝐨𝐚𝐝 𝐲𝐨𝐮𝐫 𝐥𝐢𝐧𝐤 𝐭𝐨 𝐲𝐨𝐮𝐫 𝐭𝐞𝐥𝐞𝐠𝐫𝐚𝐦.\n\n𝐒𝐞𝐞 /help.", quote=True)
