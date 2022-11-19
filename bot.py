import asyncio
import ge_checker
import json
import telegram
from time import sleep

async def main():
    bot = telegram.Bot(secrets["token"])
    async with bot:
        while True:
            result = ge_checker.check_availability(preferences)
            await bot.send_message(chat_id=secrets["authorized_id"][0], text=str(result[1]))
            sleep(30)

if __name__ == '__main__':
    with open('secrets.json', 'r') as sfile, open('preferences.json', 'r') as pfile:
        secrets = json.load(sfile)
        preferences = json.load(pfile)
    
    asyncio.run(main())
