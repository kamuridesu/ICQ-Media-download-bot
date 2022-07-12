from ICQBot import ICQBot, Dispatcher
from ICQBot.messages import ReceivedMessage
from random import randint
import os
import sys
import logging

logging.basicConfig(filename="logs.log", level=logging.INFO)


bot = ICQBot("")
dp = Dispatcher(bot)
args = sys.argv[1:]
path = "./content"
for arg in args:
    if "--path=" in arg:
        path = arg.split("--path=")[1]


def generateRandomFilename(ext):
    return str(randint(0, 99999999)) + f".{ext}"


def saveFile(data: bytes, _type: str):
    if _type == "image":
        _type = "jpg"
    elif _type == "video":
        _type = "mp4"
    rd_fn = generateRandomFilename(_type)
    if not os.path.isdir(path):
        os.makedirs(path)
    while os.path.isfile(os.path.join(path, rd_fn)):
        rd_fn = generateRandomFilename(_type)
    full_path = os.path.join(path, rd_fn)
    logging.info(full_path)
    with open(full_path, "wb") as f:
        f.write(data)


@dp.message_handler()
def getAllMedia(message: ReceivedMessage) -> None:
    if len(message.payloads) > 0:
        for p in message.payloads:
            if p.type == "file":
                try:
                    saveFile(bot.downloadFile(p.payload.file_id), p.payload.type)
                    return message.reply("media download successful")
                except Exception:
                    logging.error(p.payload.file_id)
                    return message.reply("media download failed!")


if __name__ == "__main__":
    dp.start_polling()
