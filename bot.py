import os
import dictionary
import discord
from asyncio import sleep

import requests
import datetime

TOKEN = os.environ.get('DISCORD_TOKEN')
VC_ID = os.environ.get('VOICECHAT_ID')

def spla2API(rule):
    match = rule
    if match == 'regular':
        color_disp = 0x54ff0c
    elif match == 'gachi':
        color_disp = 0xf78709
    elif match == 'league':
        color_disp = 0xff2296
    else:
        color_disp = 0xffffff
    when = 'schedule'
    url = f'https://spla2.yuu26.com/{match}/{when}'
    r = requests.get(f'https://spla2.yuu26.com/{match}/{when}')
    if r.status_code != 200:
        return r.status_code
    stages = r.json().get('result')
    for index, stage in enumerate(stages):
        rule = stage.get('rule_ex').get('name')
        maps = stage.get('maps_ex')
        map1, map2 = maps[0], maps[1]
        map1_name, map1_img = map1.get('name'), map1.get('image')
        map2_name, map2_img = map2.get('name'), map2.get('image')
        unix_start = stage.get('start_t')
        unix_end = stage.get('end_t')
        dt_s = datetime.datetime.fromtimestamp(unix_start)
        dt_e = datetime.datetime.fromtimestamp(unix_end)
        start = dt_s.strftime('%H')
        end = dt_e.strftime('%H')
        time_disp = f'{start}時〜{end}時'
        map_disp = f'{map1_name}，{map2_name}'
        if index == 0:
            embed = discord.Embed(title=rule, description=time_disp, color=color_disp)
            embed.set_image(url=map1_img)
            embed.set_thumbnail(url=map2_img)
        else:
            embed.add_field(name=rule, value=time_disp, inline=False)
        embed.add_field(name=map_disp, value='\u200b', inline=False)
    embed.set_footer(text="ておくれちゃんより")
    return embed


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
            try:
                vc = await channel.connect()
            except Exception as e:
                await message.channel.send(e)
                return
            await message.delete()
            mp3 = dictionary.dict.get(message.content)
            try:
                vc.play(discord.FFmpegPCMAudio(mp3))
            except Exception as e:
                await message.channel.send(e)
                await message.guild.voice_client.disconnect()
                return
            while vc.is_playing():
                await sleep(1)
            await vc.disconnect()

        if message.content == '?stop':
            if message.guild.voice_client is not None:
                message.guild.voice_client.stop()
                await message.guild.voice_client.disconnect()
            await message.delete()

        if client.user in message.mentions:

            # こっからスプラbot
            if 'ナワバリ' in message.content or 'ナワバリバトル' in message.content:
                embed = spla2API('regular')
                if type(embed) is int:
                    reply = f'{message.author.mention} {embed}エラーです'
                    await message.channel.send(reply)
                else:
                    await message.channel.send(embed=embed)

            if 'ガチマ' in message.content or 'ガチマッチ' in message.content:
                embed = spla2API('gachi')
                if type(embed) is int:
                    reply = f'{message.author.mention} {embed}エラーです'
                    await message.channel.send(reply)
                else:
                    await message.channel.send(embed=embed)

            if 'リグマ' in message.content or 'リーグマッチ' in message.content:
                embed = spla2API('league')
                if type(embed) is int:
                    reply = f'{message.author.mention} {embed}エラーです'
                    await message.channel.send(reply)
                else:
                    await message.channel.send(embed=embed)


client = MyClient()

if TOKEN is None or VC_ID is None:
    print('環境変数が適切に設定されていません')
else:
    client.run(TOKEN)
