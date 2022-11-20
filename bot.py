import asyncio
import datetime
import ge_checker
import json
import telegram
from time import sleep

async def main():
    print('preferences:' + str(preferences))
    bot = telegram.Bot(secrets["token"])
    async with bot:
        timestamp = datetime.datetime.today()
        print('current time: ' + str(timestamp))
        while True:
            if datetime.datetime.today() - timestamp > datetime.timedelta(hours=2):
                await bot.send_message(chat_id=secrets["authorized_id"][0], text='keepalive')
                timestamp = datetime.datetime.today()
            result = ge_checker.check_availability(preferences)
            if result[0] == True:
                print(str(result[1]))
                await bot.send_message(chat_id=secrets["authorized_id"][0], text=str(result[1]))
            sleep(30)

if __name__ == '__main__':
    with open('secrets.json', 'r') as sfile, open('preferences.json', 'r') as pfile:
        secrets = json.load(sfile)
        preferences = json.load(pfile)
    asyncio.run(main())
