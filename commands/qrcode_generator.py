import qrcode
import io
from telethon import TelegramClient, events
from translations import translations

async def generate_qr(event, content):
    try:
        
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(content)
        qr.make(fit=True)

        img = qr.make_image(fill='black', back_color='white')
        bio = io.BytesIO()
        bio.name = 'qrcode.png'
        img.save(bio, 'PNG')
        bio.seek(0)
        
        await event.reply(file=bio) 
        await event.delete()
    except Exception as e:
        await event.reply(translations.get('error_occurred', error=str(e)))
        print(str(e))

def register(client):
    @client.on(events.NewMessage(pattern=r'^\.qrcode (.+)$', outgoing=True))
    async def handler(event):
        content = event.pattern_match.group(1)
        await generate_qr(event, content)