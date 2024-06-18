import re
import time
import asyncio

# Dizionario per memorizzare i task schedulati per ogni chat
scheduled_tasks = {}

async def schedule_message(event):
    message = event.text
    # Utilizziamo una regex per estrarre il tempo e il testo dal messaggio
    match = re.search(r'\.sched\s+(\d+[s|m|h])\s+(.+)', message)
    
    if match:
        time_str = match.group(1)
        text = match.group(2)
        
        # Estrai il numero e l'unità di tempo dal tempo specificato
        time_value = int(time_str[:-1])
        time_unit = time_str[-1]
        
        # Converte il tempo in secondi
        if time_unit == 's':
            time_seconds = time_value
        elif time_unit == 'm':
            time_seconds = time_value * 60
        elif time_unit == 'h':
            time_seconds = time_value * 3600
        else:
            await event.respond("Invalid time format. Use Xs, Xm or Xh.")
            return
        
        # Ottieni l'ID della chat
        chat_id = event.chat_id
        
        # Creazione e avvio del task pianificato
        if chat_id not in scheduled_tasks:
            scheduled_tasks[chat_id] = []
        
        async def send_scheduled_message():
            while True:
                await event.respond(text)
                await asyncio.sleep(time_seconds)
        
        task = asyncio.create_task(send_scheduled_message())
        scheduled_tasks[chat_id].append(task)
        
        await event.edit(f"I will post '{text}' every {time_str} in this chat. To cancel, use .cancsched")