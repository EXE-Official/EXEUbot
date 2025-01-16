import re
import asyncio
import json
from telethon import events
from translations import translations

def register(client):
    @client.on(events.NewMessage(pattern=r'^\.timer (\d+)([hms]) (.+)', outgoing=True))
    async def timer_handler(event):
        try:
            # Parsing the command
            match = re.match(r'^\.timer (\d+)([hms]) (.+)', event.text)
            if not match:
                await event.reply(translations["invalid_command_format"])
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
                await event.reply(translations["invalid_time_unit"])
                return

            # Initial message
            message = await event.reply(translations["timer_started"].format(reason=reason, countdown_time=countdown_time))

            # Countdown logic
            while countdown_time > 0:
                countdown_time -= 1
                time_display = format_time(countdown_time)
                await message.edit(translations["timer_running"].format(reason=reason, time_display=time_display))
                await asyncio.sleep(1)

            # Timer finished
            await message.edit(translations["timer_finished"].format(reason=reason))

        except Exception as e:
            await event.reply(translations["error_occurred"].format(error=str(e)))
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
