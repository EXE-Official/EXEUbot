import re
import time
import asyncio
from translations import translations

scheduled_tasks = {}

async def schedule_message(event):
    message = event.text
    
    match = re.search(r'\.sched\s+(\d+[s|m|h])\s+(.+)', message)
    
    if match:
        time_str = match.group(1)
        text = match.group(2)
        
        time_value = int(time_str[:-1])
        time_unit = time_str[-1]
        
        if time_unit == 's':
            time_seconds = time_value
        elif time_unit == 'm':
            time_seconds = time_value * 60
        elif time_unit == 'h':
            time_seconds = time_value * 3600
        else:
            await event.respond(translations["invalid_time_format"])
            return
        
        chat_id = event.chat_id
        
        if chat_id not in scheduled_tasks:
            scheduled_tasks[chat_id] = []
        
        async def send_scheduled_message():
            while True:
                await event.respond(text)
                await asyncio.sleep(time_seconds)
        
        task = asyncio.create_task(send_scheduled_message())
        scheduled_tasks[chat_id].append(task)
        
        await event.edit(translations["schedule_message_success"].format(text=text, time_str=time_str))