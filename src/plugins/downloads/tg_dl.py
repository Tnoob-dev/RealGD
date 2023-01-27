from pyrogram.types import Message
from ..drive_modules.utils import read_json
from pathlib import Path

async def tg(msg: Message):
    data = read_json()


    if data['auto'] == True:

        if msg.document:

            await msg.reply("Documento detectado!")
            message = await msg.reply("Descargando")
            tg_file = await msg.download(file_name="./")

        elif msg.video:

            await msg.reply("Video detectado!")
            message = await msg.reply("Descargando")
            tg_file = await msg.download(file_name="./")

        elif msg.photo:

            await msg.reply("Imagen detectada!")
            message = await msg.reply("Descargando")
            tg_file = await msg.download(file_name="./")


        size = Path(tg_file).stat().st_size
        print(tg_file.split("\\")[-1])

    elif data['auto'] == False:

        if msg.text == "/dl":

            if not msg.reply_to_message:
                await msg.reply("No ha seleccionado ningun archivo")
            
            else:

                await msg.reply("Detectado!")
                message = await msg.reply("Descargando")
                tg_file = await msg.reply_to_message.download(file_name="./")
        
                size = Path(tg_file).stat().st_size
                print(tg_file.split("\\")[-1])

                
        await message.edit("Descargado {}".format(tg_file.split("\\")[-1]))


    return tg_file, size, data