import os
import re
import logging
from dotenv import load_dotenv
from signalbot import SignalBot, Command, Context, triggered, enable_console_logging, regex_triggered
import requests
import json

class PingCommand(Command):
    @triggered("Ping")
    async def handle(self, c: Context) -> None:
        await c.send("Pong")

class healthcheck(Command):
    @regex_triggered(r"^/healthcheck")
    async def handle(self, c: Context) -> None:
        try:
            response = requests.get(url="http://127.0.0.1/health")
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
    signal_service = os.getenv("SIGNAL_SERVICE")
    print(signal_service)
    phone_number= os.getenv("PHONE_NUMBER")
    print(phone_number)


    bot = SignalBot({
        "signal_service": os.getenv("SIGNAL_SERVICE"),
        "phone_number": os.getenv("PHONE_NUMBER")
    })

    bot.register(PingCommand(),groups=["group.VDFIZ2ZZdmw3RGROTEROelNobWdpZW55MkZQRTNjRlNGU0tPZFFFOURPVT0=","group.QjFVVW16V3hKb3hLVUFjQll0RFpRbXYvdCtOWkFweGVlWi9aT1l5M29Gdz0="]) # Run the command for all contacts and groups

    bot.start()
