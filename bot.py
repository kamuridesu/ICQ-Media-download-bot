from ICQBot import ICQBot, Dispatcher, executor
from ICQBot.messages import ReceivedMessage

from random import randint
import os
import sys
from zipfile import ZipFile
from tempfile import NamedTemporaryFile
import logging

logging.basicConfig(filename="log.log", level=logging.INFO, datefmt="%Y-%m-%d,%H:%M:%S")

bot = ICQBot("")
dp = Dispatcher(bot)
args = sys.argv[1:]
path = "./content"
for arg in args:
    if "--path=" in arg:
        path = arg.split("--path=")[1]


def generateRandomFilename():
    return str(randint(0, 99999999))


def zipFile(filename, _bytes, ext) -> bytes:
    print("ziping")
    with ZipFile(filename + ".zip", "w") as _zip:
        with NamedTemporaryFile("wb", suffix=ext) as f:
            f.write(_bytes)
            _zip.write(f.name)


def saveFile(data: bytes, _type: str):
    if _type == "image":
        _type = ".jpg"
    elif _type == "video":
        _type = ".mp4"
    rd_fn = generateRandomFilename()
    if not os.path.isdir(path):
        os.makedirs(path)
    while os.path.isfile(os.path.join(path, rd_fn + ".zip")):
        rd_fn = generateRandomFilename()
    full_path = os.path.join(path, rd_fn)
    logging.info(full_path)
    data = zipFile(full_path, data, _type)


@dp.message_handler(commands="/start")
def start(message: ReceivedMessage):
    return message.reply("Olá! Me envie uma imagem ou video para baixar!")


@dp.message_handler()
async def getAllMedia(message: ReceivedMessage) -> None:
    if len(message.payloads) > 0:
        for p in message.payloads:
            if p.type == "file":
                try:
                    msg = await message.reply("Downloading...")
                    saveFile(await bot.downloadFile(p.payload.file_id), p.payload.type)
                    return await msg.edit("media download successful")
                except Exception:
                    logging.error("Failed " + p.payload.file_id)
                    return await msg.edit(f"Dowload of {p.payload.file_id} failed")


if __name__ == "__main__":
    executor(dp)
