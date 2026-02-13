import os
import re
import logging
from dotenv import load_dotenv
from signalbot import SignalBot, Command, Context, triggered, enable_console_logging, regex_triggered
import requests
import json
import httpx

from commands import platecheck, HelpCommand

class PingCommand(Command):
    @triggered("Ping")
    async def handle(self, c: Context) -> None:
        await c.send("Pong")





class healthcheck(Command):
    @regex_triggered(r"^/healthcheck")
    async def handle(self, c: Context) -> None:
        try:
            response = requests.get(url=f"{platitude_url}/health")
            if response.status_code == 200:
                data = response.json()

                status = data["status"]
                database = data["database"]
                timestamp= data["timestamp"]

               
                await c.send(f"Status: {status} \nDatabase: {database} \nTimestamp: {timestamp}")
            else:
                print(response)
        except: 
            print("NO")
            await c.send("Unable to connect to health")

            



if __name__ == "__main__":
    load_dotenv()
    enable_console_logging(logging.INFO)
    platitude_url = os.getenv("PLATITIDE_URL")
    signal_service = os.getenv("SIGNAL_SERVICE")
    print(signal_service)
    phone_number= os.getenv("PHONE_NUMBER")
    print(phone_number)


    bot = SignalBot({
        "signal_service": os.getenv("SIGNAL_SERVICE"),
        "phone_number": os.getenv("PHONE_NUMBER")
    })
    #plate_cmd = platecheck()
    #bot.register(PingCommand(),groups=["group.VDFIZ2ZZdmw3RGROTEROelNobWdpZW55MkZQRTNjRlNGU0tPZFFFOURPVT0=","group.QjFVVW16V3hKb3hLVUFjQll0RFpRbXYvdCtOWkFweGVlWi9aT1l5M29Gdz0="])
    bot.register(healthcheck())
    bot.register(PingCommand())
    bot.register(HelpCommand())
    bot.register(platecheck())

    bot.start()

