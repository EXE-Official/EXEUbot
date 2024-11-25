import re
import asyncio
from telethon import events

def register(client):
    @client.on(events.NewMessage(pattern=r'^\.timer (\d+)([hms]) (.+)', outgoing=True))
    async def timer_handler(event):
        try:
            # Parsing the command
            match = re.match(r'^\.timer (\d+)([hms]) (.+)', event.text)
            if not match:
                await event.reply("Invalid command format. Use `.timer 2m reason`.")
                return

            time_value = int(match.group(1))
            time_unit = match.group(2)
            reason = match.group(3)

            # Convert time to seconds
            if time_unit == 'h':
                countdown_time = time_value * 3600
            elif time_unit == 'm':
                countdown_time = time_value * 60
            elif time_unit == 's':
                countdown_time = time_value
            else:
                await event.reply("Invalid time unit. Use `h`, `m`, or `s`.")
                return

            # Initial message
            message = await event.reply(f"⏳ Timer started: {reason}\nRemaining: {countdown_time} seconds.")

            # Countdown logic
            while countdown_time > 0:
                countdown_time -= 1
                time_display = format_time(countdown_time)
                await message.edit(f"⏳ Timer started: {reason}\nRemaining: {time_display}")
                await asyncio.sleep(1)

            # Timer finished
            await message.edit(f"✅ Timer finished: {reason}!")

        except Exception as e:
            await event.reply(f"Error: {str(e)}")

def format_time(seconds):
    """Format seconds into a more readable hh:mm:ss format."""
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    if hours > 0:
        return f"{hours}h {minutes}m {seconds}s"
    elif minutes > 0:
        return f"{minutes}m {seconds}s"
    else:
        return f"{seconds}s"
