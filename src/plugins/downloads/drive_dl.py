from pydrive2.drive import GoogleDrive
from pyrogram.types import Message
import os



async def gdl(drive: GoogleDrive, url: str, message: Message):
    
    # EJEMPLO DE ENLACES:
    # https://drive.google.com/file/d/1-pZSs2jRHEAB_tL_tepAjMDSiIkAlkV9/view
    # O SEA, DEBE ESTAR EL ID EN EL PENULTIMO SLASH(/) DEL ENLACE

    msg = await message.reply("Descargando")
    metadata = {
        'id': url.split("/")[-2]
    }

    Gfile = drive.CreateFile(metadata=metadata)
    Gfile.GetContentFile(Gfile['title'])

    return Gfile, msg

async def complete_gdl(drive: GoogleDrive, url: str, message: Message):

    folder_id = url.split("/")[-1]

    metadata = {
        'q': f"'{folder_id}' in parents and trashed=false"
    }

    father_folder = drive.ListFile(metadata).GetList()
    try:
        await message.reply("Descargando")
        for folder in father_folder:

            child_folder = drive.ListFile({'q':f"'{folder['id']}' in parents and trashed=false"}).GetList()

            ############################################
            # mimeTypes:                               #
            # application/vnd.google-apps.document     #
            # application/vnd.google-apps.spreadsheet  #
            # application/vnd.google-apps.presentation #
            # application/vnd.google-apps.form         #
            # application/vnd.google-apps.drawing      #
            # application/vnd.google-apps.script       #
            # application/vnd.google-apps.site         #
            # application/vnd.google-apps.folder       #
            # application/vnd.google-apps.map          #
            # application/vnd.google-apps.unknown      #
            ############################################

            if folder['mimeType'] == 'application/vnd.google-apps.folder':
                
                if not os.path.exists(folder['title']):
                    os.mkdir(folder['title'])

                for files in child_folder:
                    # print(files['id'])
                    print('Descargando ' + files['title'])
                    files.GetContentFile("./" + folder['title'] + "/" + files['title'])
                    print('Finalizado')
    except: 
        pass

    try: 
        for under_files in father_folder:
            if under_files['mimeType'] != 'application/vnd.google-apps.folder':
                print("Descargando " + under_files['title'])
                under_files.GetContentFile("./" + under_files['title'])
                print('Finalizado')
    except:
        pass

