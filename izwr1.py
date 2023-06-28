import asyncio
from telethon import TelegramClient, events
from telethon.tl import functions
import random

api_id = 28113777
api_hash = '0d53f5c74e600b3e888eff9b056c2341'
messages = ['Teri Maa Chodunga bsdk 😫😩','😂🤣🤣','dar gaya kya bsdk😂🤣','bsdk mere lad nahi sakta tu🤣','Teri behen ka lavda rubber ka 😫😩🥺😢','Gaand main lassan','Toota hua lund','Kutte ka awlat','Chippkali ke jhaant ke paseene','Maa ke bhadwe🥵','Teri maa chodne keliye time nahi ab 🤬','deko chakka hai tu spam kara','abbe spam mat kar','ladna hai to teeke ladna','beta gaali dena sikle😂','randi jesa mat kar 🤣','Randi Ka Bacha Hai Tu🤣', 'Land Le Ga Mera ?', 'teri maa ki bra kol maine deka 🥵😍','Teri Maa Meri Maal😍🥰😘','Behanke Love Day','Teri Behan Ki Rape Kardunga','Bsdk Baap Se ladna Hai Tuje','Lawdu Marne Se Dar Nahi Lagta tuje','Marna Hai Kya Bsdk','Sub avo Line se Inki Maa ki Lelo','Teri Maa ki Chut se Paani Nikalunga aj','Bhai teri Behan Ka hot Videos Dede','Teri Gand MAi Chatri Daal Ke kolunga','Teri Maa ki chut Mai Petrol Lagake Agg lagadung Fir chodunga','Apna land choos','Apni gaand mein muthi daal','Apni ma ko ja choos','Chinaal ke gadde ke nippleke baal ke joon','Mein teri maa ko teri bahenki choot mein chodoonga aur tera baap laltern lekar aayega','Teri maa ki bimaar badboodar choot','Kali Chut ka Safaid Jhaat','Teri maa ki gaand ki baal mein jalaay hue, maarey hue chupkili ki unday','Teri ma ki bund mein chaarpai bichhake teri bhen ko chodun','bhai tuje gaali dena nahi ata ghar ja dood pile🤣🤣🤣','kyu maa chudara hai tu😂','tu bacha hai yrr😂🤣','abe bore mat kar🥱😴']

client = TelegramClient('session_name', api_id, api_hash)
is_bot_active = False
allowed_user_id = [6004027321, 5737890253]
target_chats = {}

@client.on(events.NewMessage)
async def my_event_handler(event):
    global is_bot_active
    if is_bot_active and any(char.isalpha() for char in event.raw_text) and event.chat_id in target_chats:
        chat_id, user_id = target_chats[event.chat_id]
        if event.sender_id == user_id:
            await asyncio.sleep(5)  # Set a timer for 5 seconds
            random_message = random.choice(messages)
            await client.send_message(chat_id, random_message, reply_to=event.message.id)


@client.on(events.NewMessage(pattern=r'(?i)/z\s+(-?\d+)\s+(-?\d+)'))
async def start_command_handler(event):
    global is_bot_active, target_chats
    if event.sender_id in allowed_user_id:
        is_bot_active = True
        chat_id = int(event.pattern_match.group(1))
        user_id = int(event.pattern_match.group(2))
        target_chats[event.chat_id] = (chat_id, user_id)
        message = await event.respond('Bot activated!')
        await asyncio.sleep(1) 
        await client.delete_messages(event.chat_id, message.id)
        await asyncio.sleep(5)  # Set a timer for 2 seconds
        
    elif event.sender_id not in allowed_user_id:
        await client.send_message(
            event.chat_id,
            "Mai there baap ka nawkar nahi hu. bat ka gripnkal kena bat sida tere gand mai dal.",
            reply_to=event.message.id,
        )


@client.on(events.NewMessage(pattern=r'(?i)/h'))
async def stop_command_handler(event):
    global is_bot_active, target_chats
    if event.sender_id in allowed_user_id:
        is_bot_active = False
        group_chat_id = event.chat_id  # Get the group chat ID
        target_chats.pop(group_chat_id, None)  # Remove the chat from target_chats if it exists
        message = await event.respond('Bot deactivated!')
        await asyncio.sleep(1)
        await client.delete_messages(event.chat_id, message.id)
        
    elif event.sender_id not in allowed_user_id:
        await client.send_message(
            event.chat_id,
            "Mai there baap ka nawkar nahi hu. bat ka gripnkal kena bat sida tere gand mai dal.",
            reply_to=event.message.id,
        )


@client.on(events.NewMessage(pattern=r'(?i)/spam\s+(\d+)\s+(.+)'))
async def handle_spam_command(event):
    if event.sender_id in allowed_user_id:
        num_times = int(event.pattern_match.group(1))
        message = event.pattern_match.group(2)

        chat_id = event.chat_id

        # Delete the command message
        await client.delete_messages(chat_id, event.message.id)

        # Send the messages
        for _ in range(num_times):
            await asyncio.sleep(1)
            await client.send_message(chat_id, message)

        response_message = f'Successfully spammed "{message}" {num_times} times in chat {chat_id}.'
        response = await client.send_message(chat_id, response_message)

    elif event.sender_id not in allowed_user_id:
        await client.send_message(
            event.chat_id,
            "Mai there baap ka nawkar nahi hu. bat ka gripnkal kena bat sida tere gand mai dal.",
            reply_to=event.message.id,
        )


async def main():
    await client.start()
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
