from telethon import events
from telethon.tl.functions.contacts import BlockRequest
import commands.database as db

# REMOVING THIS FILE WILL CAUSE THE CRASH OF THE USERBOT!!!

def register(client):
    db.initialize_database()

    @client.on(events.NewMessage(pattern=r'^\.addwl(?: |$)(.*)', outgoing=True))
    async def add_whitelist(event):
        try:
            user_id = event.pattern_match.group(1)
            if user_id.isdigit():
                user_id = int(user_id)
            else:
                user = await client.get_entity(user_id)
                user_id = user.id
            db.add_to_whitelist(user_id)
            await event.edit(f"User {user_id} added to whitelist.")
        except Exception as e:
            await event.reply(f"Error: {str(e)}")

    @client.on(events.NewMessage(pattern=r'^\.rmwl(?: |$)(.*)', outgoing=True))
    async def remove_whitelist(event):
        try:
            user_id = event.pattern_match.group(1)
            if user_id.isdigit():
                user_id = int(user_id)
            else:
                user = await client.get_entity(user_id)
                user_id = user.id
            db.remove_from_whitelist(user_id)
            await event.edit(f"User {user_id} removed from whitelist.")
        except Exception as e:
            await event.reply(f"Error: {str(e)}")

    @client.on(events.NewMessage(incoming=True))
    async def handle_message(event):
        if event.is_private:
            sender = await event.get_sender()
            user_id = sender.id
            
            if db.is_whitelisted(user_id):
                return  # Do nothing if the user is whitelisted
            
            warning_count = db.get_warning_count(user_id)
            
            if warning_count >= 2:
                await client(BlockRequest(user_id))
                db.reset_warning_count(user_id)
                await event.reply("You have been blocked and reported for spamming.")
            else:
                db.increment_warning_count(user_id)
                await event.reply(f"Warning {warning_count + 1}/3: You can't contact this user, Please, stop sending message, otherwhise you'll get blocked.")