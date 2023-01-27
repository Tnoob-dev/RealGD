from pydrive2.drive import GoogleDrive
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton as IKB, CallbackQuery 
from ...configs.texts import FILE_UPLOADED
from os import unlink
from pathlib import Path
import py7zr

def compress(fpath: str, part_size: int):
    fpath: Path = Path(fpath)
    filters = [{"id": py7zr.FILTER_COPY}]
    file_list = []

    with py7zr.SevenZipFile(
        f"{fpath}.7z",
        "w",
        filters=filters,
    ) as f:
        f.write(fpath, fpath.name)
    unlink(fpath)

    with open(f"{fpath}.7z", "rb") as zip_file:
        file_count = 1
        eof = False
        while True:
            with open(f"{fpath}.7z.{file_count:03d}", "wb") as file_part:
                wrote_data = 0
                while wrote_data < (part_size * 1024 * 1024):
                    data = zip_file.read(1024 * 1024)
                    if not data:
                        eof = True
                        break
                    else:
                        file_part.write(data)
                        wrote_data += len(data)

            file_list.append(f"{fpath}.7z.{file_count:03d}")

            if eof:
                break
            file_count += 1

    unlink(f"{fpath}.7z")
    
    # for d in file_list:
    #     shutil.move(d, './downloads/')
    return file_list



import os
from dotenv import load_dotenv

load_dotenv(".../configs/config.env")

INDEX_LINK = os.getenv("INDEX_LINK")

async def upload(drive: GoogleDrive, filename, msg: Message = None, length = None):


    metadata = {
        'title': filename
    }

    file = drive.CreateFile(metadata)

    message = await msg.reply("Subiendo {}".format(file['title']))
    
    file.SetContentFile(file['title'])
    file.Upload()

    await message.delete()
    
    await msg.reply(FILE_UPLOADED.format(filename, length, file['id']), 
    reply_markup=InlineKeyboardMarkup(
        
        [
            [
                IKB("Link al archivo🔗", url=file['alternateLink']),
                
                IKB("Eliminar archivo♻️", callback_data='call_del')
            ]
        ]
        ))

    return file

async def upload_to_tdd(drive: GoogleDrive, filename: str, msg: Message = None, length = None):
    
    metadata = {
    'title': filename,
    'parents': [{
        'teamDriveId': os.getenv("TEAMDRIVE_ID"),
        'id': os.getenv("TD_FOLDER_ID")
    }]
    }

    tdd_file = drive.CreateFile(metadata)

    message = await msg.reply("Subiendo {}".format(tdd_file['title']))

    tdd_file.SetContentFile(tdd_file['title'])
    tdd_file['title'] = filename.split("/")[-1]
    tdd_file.Upload()

    await message.delete()


    await msg.reply(FILE_UPLOADED.format(filename, length, tdd_file['id']), 
    reply_markup=InlineKeyboardMarkup(
        [
            [
                IKB("Drive Link🔗", url=tdd_file['alternateLink']),
                    
                IKB("Eliminar archivo♻️", callback_data='call_del')
            ],
            [
                IKB("Index Link", url=str(INDEX_LINK+filename.split("/")[-1].replace(" ", "%20")+"?a=view"))
            ]
        ]
        ))

    return tdd_file

async def comp_up(drive: GoogleDrive, folder: str, msg: Message):

    message = await msg.reply("Comprimiendo carpeta {}".format(folder))
    file_list = compress(folder, 3000)
    await message.edit("Compresion Completada")

    for files in file_list:
        print(files)
        await upload_to_tdd(drive, files, msg)