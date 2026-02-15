import asyncio
import json
import logging
import re
import httpx
import os

from signalbot import SignalBot, Command, Context, triggered, enable_console_logging, regex_triggered

platitude_url = os.getenv("PLATITIDE_URL")
logger = logging.getLogger(__name__)

class plateadd(Command):
    @regex_triggered(r"^/plateadd\b")
    async def handle(self, c: Context) -> None:
        logger.debug("Plate add command triggered")
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
                logger.debug(f"Adding plate {raw_plate} to database")
                response = await client.post(f"{platitude_url}/plates/", json={"code": raw_plate})
            if response.status_code == 200 or response.status_code == 201:
                    data = response.json()
                    plate_id= data["id"]
                    plate_code =data["code"]
                    logger.info(f"Successfully added plate {plate_code} with ID {plate_id}")
                    #if plate has been found we look for sightings
                    async with httpx.AsyncClient() as client:
                         sight_response = await client.get(f"{platitude_url}/sightings/plate/{plate_id}")
                         if sight_response.status_code == 200: 
                            sighting = sight_response.json()
                            #lets chat know one sighting reported
                            if len(sighting) == 1:
                                logger.debug("One sighting found")
                                await c.send(f"One Sighting found\n {sighting}")
                            #lets chat know multiple sightings reported
                            if len(sighting) >1:
                                logger.debug("Multiple sightings found")
                                await c.send(f"Multiple Sightings found:\n {sighting}")
                         #if no sightings reported let chat know plateadd
                         else:
                            logger.debug("No sightings found for this plate")
                            await c.send("No Sightings found please use /plateadd to add the plate")
                        
            else: 
                    logger.error(f"Error adding plate - Status code: {response.status_code}")
                    await c.reply("No P")

        except Exception as e:
            logger.error(f"Error connecting to Platitude: {e}")
            await c.reply("Unable to connect to Platitude try again later.")
        
