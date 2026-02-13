import asyncio
import json
import logging
import re
import httpx
import os

from signalbot import SignalBot, Command, Context, triggered, enable_console_logging, regex_triggered

#"http://192.168.3.141" = os.getenv("PLATITIDE_URL")

class platecheck(Command):
    @regex_triggered(r"^/platecheck\b")
    async def handle(self, c: Context) -> None:
        await c.react("\U0001f440")
        parts = c.message.text.split(maxsplit=1)
        has_text = len(parts) > 1 and parts[1].strip()
        print("HAS TEXT")
        if has_text:
            raw_plate = parts[1].strip().upper()
        else: 
            await c.reply("No plate detected in message")
        #check if plate has been entered into DB
        try: 
            async with httpx.AsyncClient() as client:
                print("http://192.168.3.141:8000")
                response = await client.get(f"http://192.168.3.141:8000/plates/code/{raw_plate}")
            if response.status_code == 200:
                    print("GOT PLATE")
                    data = response.json()
                    plate_id= data["id"]
                    plate_code =data["code"]
                    #if plate has been found we look for sightings
                    async with httpx.AsyncClient() as client:
                         sight_response = await client.get(f"http://192.168.3.141:8000/sightings/plate/{plate_id}")
                         print("SIGHING TESTED")
                         if sight_response.status_code == 200: 
                            print("SIGHT 200")
                            sighting = sight_response.json()
                            print(sighting)
                            sightings_formatted = []
                            vehicle_info = None
                            if sighting[0].get("vehicle_id") is not None:
                                print("VEHICLEID FOUND")
                                vehicle_id = sighting[0]['vehicle_id']
                                print("VEHICLE_ID" +vehicle_id)
                                async with httpx.AsyncClient() as client:
                                    print("GETTING VEHICLE")
                                    vehicle_response = await client.get(f"http://192.168.3.141:8000/vehicles/{vehicle_id}")
                                    print("GOT VEHICLE")
                                    print(vehicle_response)
                                    vehicle_info = vehicle_response.json()
                            else: 
                                print("NO VEHICLEID")

                            #format sightings to look nice in signal
                            print("STARTING SIGHTINGS LOOP")
                            for s in sighting:
                                longitude = s["longitude"]
                                latitude = s["latitude"]
                                timestamp = s["timestamp"]
                                plate= plate_code
                                #vehicle = s.get("vehicle_id", "unknown")
                                
                                line = (f"Location:{longitude},{latitude}",f" || Time:{timestamp}")
                                sightings_formatted.append(line)
                                print("LOOP")
                            #Format VEHICLE INFO
                            print("FORMATTING VEHICLE INFO")
                            print(vehicle_info)
                            if vehicle_info is not None: vehicle_msg = (
                                                f"Make {vehicle_info.get('make', 'unknown')}\n"
                                                f"Model  {vehicle_info.get('model', 'unknown')}\n"
                                                f"Color  {vehicle_info.get('color', 'unknown')}"
                                            )
                            else: vehicle_msg =("VEHICLE INFO UNKOWN")
                            print(vehicle_msg)
                            msg = "\n\n".join(f"{loc},{time}" for loc,time in sightings_formatted)
                            #lets chat know one sighting reported
                            print(f"MSG: {msg}")
                            if len(sighting) == 1:
                                await c.send(f"One Sighting found\nPlate: {plate}\n{vehicle_msg}\n{msg}")
                            #lets chat know multiple sightings reported
                            if len(sighting) >1:
                                await c.send(f"Multiple Sightings found\nPlate: {plate}\n{vehicle_msg}\n{msg}")
                         #if no sightings reported let chat know plateadd
                         else:
                            await c.send(f"No Sightings found for plate {plate_code} please use /plateadd to add the plate")
                        
            else: 
                    await c.reply("No Plate Found")
                    print(response.status_code)

        except:
            await c.reply("Unable to connect to Platitude try again later.")
        
