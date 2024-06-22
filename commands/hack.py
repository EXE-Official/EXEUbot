import asyncio
from faker import Faker
from telethon import events

fake = Faker()

async def hack(event):
    try:
        
        await event.edit("`🕵️‍♂️ Starting the hack...`")
        await asyncio.sleep(2)
        await event.edit("`📡 Connecting to target servers...`")
        await asyncio.sleep(2)
        await event.edit("`🔍 Performing port scanning...`")
        await asyncio.sleep(2)
        await event.edit("`🔓 Open port found! Exploit attempt...`")
        await asyncio.sleep(3)
        await event.edit("`💻 Logged in successfully! Extracting data...`")
        await asyncio.sleep(3)
        await event.edit("`📁 Compiling the extracted information...`")
        await asyncio.sleep(2)
        
        
        name = fake.first_name()
        surname = fake.last_name()
        nationality = fake.country()
        address = fake.address()
        age = fake.random_int(min=18, max=90)
        email = fake.email()
        
        
        info_message = (
            f"`First Name: {name}\n`"
            f"`Last name: {surname}\n`"
            f"`Age: {age}\n`"
            f"`Address: {address}\n`"
            f"`Email: {email}\n`"
            f"`Nationality: {nationality}`"
        )
        
        await event.edit(info_message)
    except Exception as e:
        await event.edit(f"An error occurred during the hacking simulation: {str(e)}")
        print(str(e))

def register(client):
    @client.on(events.NewMessage(pattern=r'^\.hack$', outgoing=True))
    async def handler(event):
        await hack(event)
