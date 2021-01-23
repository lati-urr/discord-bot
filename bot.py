import os
import dictionary
import discord
from asyncio import sleep

TOKEN = os.environ.get('DISCORD_TOKEN')
VC_ID = os.environ.get('VOICECHAT_ID')

class MyClient(discord.Client):

    async def on_ready(self):
        print('Username: {0.name}\nID: {0.id}'.format(self.user))
        print(TOKEN)
        print(int(VC_ID))

    async def on_message(self, message):
        if message.author.bot:
            return

        channel = client.get_channel(int(VC_ID))

        if message.content in dictionary.dict:
            if message.guild.voice_client is not None:
                message.guild.voice_client.disconnect()
            vc = await channel.connect()
            await message.delete()
            mp3 = dictionary.dict.get(message.content)
            vc.play(discord.FFmpegPCMAudio(mp3))
            while vc.is_playing():
                await sleep(1)
            await vc.disconnect()

        if message.content == '?stop':
            if message.guild.voice_client is not None:
                message.guild.voice_client.stop()
                await message.guild.voice_client.disconnect()
            await message.delete()

client = MyClient()

if TOKEN is None or VC_ID is None:
    print('環境変数が適切に設定されていません')
else:
    client.run(TOKEN)
