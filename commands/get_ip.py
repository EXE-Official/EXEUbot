from telethon import events
from ipwhois import IPWhois

async def get_ip_info(event, client):
    command_args = event.message.text.split(' ')
    if len(command_args) == 2:
        target_ip = command_args[1]
        try:
            ip_info = IPWhois(target_ip).lookup_rdap()
            output = f'IP/Domain info for {target_ip}:\n\n'
            output += f'IP Range: {ip_info["network"]["cidr"]}\n'
            output += f'Country: {ip_info["asn_country_code"]}\n'
            output += f'City: {ip_info.get("city", "N/A")}\n'
            output += f'ISP: {ip_info["asn_description"]}\n'
            output += f'Organization: {ip_info["network"]["name"]}\n'
            await event.edit(output)
        except Exception as e:
            await event.edit(f"Error retrieving IP information: {str(e)}")
    else:
        await event.edit("Please provide an IP address or domain after the `.ip` command.")

def register(client):
    @client.on(events.NewMessage(pattern=r'^\.ip\s+\S+$', outgoing=True))
    async def handler(event):
        await get_ip_info(event, client)