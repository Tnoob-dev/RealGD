import json
from os import listdir, path




from pyrogram.types import (
    Message, 
    InlineKeyboardMarkup as IKM, 
    InlineKeyboardButton as IKB
)



def read_json():
    with open("config.json", "r") as file:
        data = json.load(file)
        file.seek(0)
    return data


async def open_json(selection, info_data: str = None):
    
    with open("config.json", "r+") as file:
            data = json.load(file)
            data[info_data] = bool(selection)
            file.seek(0)
            file.write(json.dumps(data, indent=4))
            file.truncate()


async def select_drive(msg: Message):

    await msg.reply(
        "Seleccione a donde desea subir⬆️",
        reply_markup=IKM(
            [
                [
                    IKB("Personal👤", callback_data='personal'),
                    IKB("TeamDrive👥", callback_data='td')
                ]
            ]
        )
    )

async def change_auto(msg: Message):
    data = read_json()

    if data['auto'] == True: # Llevar de True a False

        await open_json(False, 'auto')
        await msg.reply("Las descargas no seran automaticas, use el comando /download para comenzar la descarga del archivo")

    elif data['auto'] == False: # Llevar de False a True

        await open_json(True, 'auto')
        await msg.reply("Las descargas seran automaticas, comience a reenviar los archivos, cuidado con el Flood")


async def list_files(message: Message):

    files  = listdir()

    msg = '📂Carpetas: \n\n'

    for archivos in files:
        if path.isdir(archivos) and archivos != 'src':
            msg += "📂" + archivos
            msg += "\nUse /upfolder {nombre de la carpeta} para subirla\n"

    await message.reply(msg)


def sizeof(num, suffix='B'):
    
    for unit in ['','K','M','G','T','P','E','Z']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)