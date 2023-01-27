import logging
import time

logging.basicConfig(filename="/var/www/html/log.txt",format='[%(levelname) 5s/%(asctime)s] %(name)s: %(msg)s',level=logging.ERROR)
logging.error("Waiting 30 minutes...")
time.sleep(1800)
logging.error("Running app now")

import os
from dotenv import load_dotenv

from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive



gauth = GoogleAuth(settings_file='./src/configs/conf.yaml')
gauth.LoadCredentialsFile("credentials_module.json")

if gauth.access_token_expired:
    gauth.Refresh()
    gauth.SaveCredentialsFile("credentials_module.json")
else:
    gauth.Authorize()

# gauth.LocalWebserverAuth(launch_browser=False)
drive = GoogleDrive(gauth)

from logging import log, basicConfig, getLogger, INFO, ERROR, WARN

basicConfig(level=INFO, force=True, format="[%(levelname)s - %(asctime)s - %(message)s]")

drive_bot = getLogger("pyroDrive")
drive_bot.setLevel(WARN)

log(INFO, "Iniciando Logger")

from pyrogram import Client, filters
from pyrogram.types import (
    Message, 
    InlineKeyboardButton as IKB, 
    InlineKeyboardMarkup as IKM, 
    CallbackQuery
)

from src.configs.texts import (
    START_MESSAGE, 
    GENERAL_HELP_MESSAGE, 
    COMMANDS_HELP_MESSAGE,
    SUPPORT_DLS_MESSAGE,
    NO_AUTH,
    ERROR_IN_TRY
    )



# Drive Plugins
from src.plugins.drive_modules.list_drive import list_drive
from src.plugins.drive_modules.delete import delete, query_delete
from src.plugins.drive_modules.count import drive_count

from src.plugins.drive_modules.utils import (open_json, 
                                                read_json, 
                                                select_drive, 
                                                change_auto,
                                                sizeof,
                                                list_files)

from src.plugins.drive_modules.upload import (upload, 
                                            upload_to_tdd, 
                                            comp_up)


# Descargas
from src.plugins.downloads.reqs import aiodl
from src.plugins.downloads.mf_dl import download
from src.plugins.downloads.zippy import zdl
from src.plugins.downloads.drive_dl import gdl, complete_gdl
from src.plugins.downloads.tg_dl import tg


load_dotenv(dotenv_path="./src/configs/config.env")


bot: Client = Client(
    name=os.getenv('SESSION'),
    api_hash=os.getenv('HASH'),
    api_id=os.getenv('ID'),
    bot_token=os.getenv('BOT_TK')
)

OWNER = [957370219, 1642684372]

@bot.on_message(filters.command("start", prefixes="/"))
async def start(client: Client, message: Message):


    if message.from_user.id in OWNER:

        await message.reply(START_MESSAGE.format(
    message.from_user.mention
    ),
    reply_markup=IKM(
        [
            [
                IKB("Ayuda🛐", callback_data='help')
            ]
        ]
    ))
    else:
        await message.reply(NO_AUTH)

@bot.on_message(filters.command("help", prefixes="/"))
async def help(client: Client, message: Message):
    
    if message.from_user.id in OWNER:
        await message.reply(GENERAL_HELP_MESSAGE.format(
            message.from_user.mention
        ), reply_markup=IKM(
                [
                    [
                        IKB("💬Comandos", callback_data='commands'),
                        IKB("⬇️Soporte de descarga", callback_data='supp_down')
                    ]
                ]
            ))
    else:
        await message.reply(NO_AUTH)
        

@bot.on_message(filters.command("drive", prefixes="/"))
async def drive_selection(client: Client, message: Message):
    
    if message.from_user.id in OWNER:
        await select_drive(message)
    else:
        await message.reply(NO_AUTH)


@bot.on_message(filters.command("list", prefixes="/"))
async def list_files_drive(client: Client, message: Message):
    
    if message.from_user.id in OWNER:

        msg = await message.reply("Listando archivos")
        await list_drive(drive, msg)
    
    else:
        await message.reply(NO_AUTH)

@bot.on_message(filters.command("del", prefixes="/"))
async def del_files(client: Client, message: Message):
    
    if message.from_user.id in OWNER:
        await delete(message, drive)
    else:
        await message.reply(NO_AUTH)


@bot.on_message(filters.command("count", prefixes="/"))
async def count(client: Client, message: Message):

    if message.from_user.id in OWNER:

        await drive_count(message, drive)
    
    else:
        await message.reply(NO_AUTH)

@bot.on_message(filters.command("auto", prefixes="/"))
async def set_auto(client: Client, message: Message):

    if message.from_user.id in OWNER:

        await change_auto(message)
    
    else:
        await message.reply(NO_AUTH) 

@bot.on_message(filters.command("ls", prefixes="/"))
async def set_auto(client: Client, message: Message):

    if message.from_user.id in OWNER:

        await list_files(message)
    
    else:
        await message.reply(NO_AUTH) 

@bot.on_message(filters.command("upfolder", prefixes="/"))
async def set_auto(client: Client, message: Message):

    if message.from_user.id in OWNER:

        await comp_up(drive, message.text.split(" ")[1], message)
    
    else:
        await message.reply(NO_AUTH)

@bot.on_message(filters.command("gdl", prefixes="/"))
async def folder_dl(client: Client, message: Message):
    
    if message.from_user.id in OWNER:

        await complete_gdl(drive, message.text.split(" ")[1], message)
    
    else:
        await message.reply(NO_AUTH)


@bot.on_message(filters.regex(".*https://.*") | filters.regex(".*http://.*"))
async def dls(client: Client, message: Message):

    if message.from_user.id in OWNER:

        data = read_json()

        global file
        global tdd_file

        if 'mediafire' in message.text:
            log(INFO, "Link de mediafire detectado!")
            output, total, msg = await download(message.text, message.text.split("/")[-2], quiet=False, message=message)
            
            try:

                if data['teamDrive'] is False:
                    await msg.delete()
                    file = await upload(drive, output, message, sizeof(total))
                elif data['teamDrive'] is True:
                    await msg.delete()
                    tdd_file = await upload_to_tdd(drive, output, message, sizeof(total))

            except Exception as e:
                log(INFO, e)
                await message.reply(ERROR_IN_TRY)
                
        elif 'zippyshare' in message.text:
            log(INFO, "Link de zippyshare detectado!")
            Zfile, msg = await zdl(message.text, message)
            try:
                if data['teamDrive'] is False:
                    await msg.delete()
                    file = await upload(drive, Zfile.name, message, Zfile.size_fmt)
                elif data['teamDrive'] is True:
                    await msg.delete()
                    tdd_file = await upload_to_tdd(drive, Zfile.name, message, Zfile.size_fmt)

            except Exception as e:
               log(INFO, e)
               await message.reply(ERROR_IN_TRY)

        elif 'drive':
            await gdl(drive, message.text, message)

        else:
            log(INFO, "Link directo detectado!")
            filename, length, msg = await aiodl(message.text, message)

            try:
                if data['teamDrive'] is False:
                    await msg.delete()
                    file = await upload(drive, filename, message, sizeof(num=length))
                elif data['teamDrive'] is True:
                    await msg.delete()
                    tdd_file = await upload_to_tdd(drive, filename, message, sizeof(num=length))
            except Exception as e:
               log(INFO, e)
               await message.reply(ERROR_IN_TRY)

    else:
        await message.reply(NO_AUTH)

@bot.on_message(filters.document | filters.video | filters.photo | filters.text)
async def up_from_tg(client: Client, message: Message):

    if message.from_user.id in OWNER:

        global file
        global tdd_file

        tg_file, size, data = await tg(message)

        try:

            if data['teamDrive'] is False:

                file = await upload(drive, tg_file.split("\\")[-1], message, sizeof(size))
            
            elif data['teamDrive'] is True:

                tdd_file = await upload_to_tdd(drive, tg_file.split("\\")[-1], message, sizeof(size))
        
        except Exception as e:
               log(INFO, e)
               await message.reply(ERROR_IN_TRY)
    
    else:
        await message.reply(NO_AUTH) 

@bot.on_callback_query()
async def del_f(client: Client, query: CallbackQuery):
    
    back = [IKB("⬅️Regresar", callback_data='help')]
    close = [IKB("❌Cerrar", callback_data='close')]
    data = read_json()

    if query.data == 'call_del':

        await query.answer('Eliminando')

        if data['teamDrive'] is False:
            await query_delete(query=query, drive=drive, file=file)
        
        elif data['teamDrive'] is True:
            await query_delete(query=query, drive=drive, file=tdd_file)
    
    elif query.data == 'help':

        await query.message.edit(
            GENERAL_HELP_MESSAGE,
            reply_markup=IKM(
                [
                    [
                        IKB("💬Comandos", callback_data='commands'),
                        IKB("⬇️Soporte de descarga", callback_data='supp_down')
                    ]
                ]
            )
            )

    elif query.data == 'commands':

        await query.message.edit(
            COMMANDS_HELP_MESSAGE, 
            reply_markup=IKM(
                [
                    back,
                    close
                ]
            )
            )

    elif query.data == 'supp_down':
        await query.message.edit(
            SUPPORT_DLS_MESSAGE,
            reply_markup=IKM(
                [
                    back,
                    close
                ]
            ),
            disable_web_page_preview=True
            )
    elif query.data == 'personal':

        await open_json(False, 'teamDrive')
        await query.message.edit("Vale, subiremos a su nube personal")
    
    elif query.data == 'td':

        await open_json(True, 'teamDrive')
        await query.message.edit("Vale, subiremos a su TeamDrive")

    elif query.data == 'close':
        await query.message.delete()




if __name__ == "__main__":
    log(INFO, "Iniciando el Bot")
    bot.start()
    log(INFO, "Bot iniciado")
    bot.loop.run_forever(
