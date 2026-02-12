import asyncio
import json
import logging
import re
import httpx
import os

from signalbot import SignalBot, Command, Context, triggered, enable_console_logging, regex_triggered

platitude_url = os.getenv("PLATITIDE_URL")

class platecheck(Command):
    @regex_triggered(r"^/plateadd\b")
    async def handle(self, c: Context) -> None:
        await c.react("\U0001f440")
        parts = c.message.text.split(maxsplit=1)
        has_text = len(parts) > 1 and parts[1].strip()
        if has_text:
            raw_plate = parts[1].strip().upper()
        else: 
            await c.reply("No plate detected in message")
        #check if plate has been entered into DB
        try: 
            async with httpx.AsyncClient() as client:
                response = await client.post(f"{platitude_url}/plates/{raw_plate}")
            if response.status_code == 200:
                    data = response.json()
                    plate_id= data["id"]
                    plate_code =data["code"]
                    #if plate has been found we look for sightings
                    async with httpx.AsyncClient() as client:
                         sight_response = await client.get(f"{platitude_url}/sightings/{plate_id}")
                         if sight_response.status_code == 200: 
                            sighting = sight_response.json()
                            #lets chat know one sighting reported
                            if len(sighting) == 1:
                                c.send(f"One Sighting found\n {sighting}")
                            #lets chat know multiple sightings reported
                            if len(sighting) >1:
                                c.send(f"Multiple Sightings found:\n {sighting}")
                         #if no sightings reported let chat know plateadd
                         else:
                            c.send("No Sightings found please use /plateadd to add the plate")
                        
            else: 
                    await c.reply("No P")

        except:
            await c.reply("Unable to connect to Platitude try again later.")
        
