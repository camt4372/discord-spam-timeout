import discord
from discord.ext import commands
import datetime
import requests

intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)

# 홍보 감지안할 카테고리 아이디 넣으쇼
CATEGORY_ID = 1126835661954101258
# 홍보 감지안할 유저 아이디 넣으세요.
EXEMPT_USER_ID = 333383404852609025

# 홍보 감지 키워드
DISCORD_KEYWORDS = ["discord.gg", "discord.com/invite"] 

BASE = "https://discord.com/api/v9/"
TOKEN = '' # 님 봇 토큰 넣으세요.

def timeout_user(user_id: int, guild_id: int, duration: int):
    endpoint = f'guilds/{guild_id}/members/{user_id}'
    headers = {"Authorization": f"Bot {TOKEN}"}
    url = BASE + endpoint
    timeout = (datetime.datetime.utcnow() + datetime.timedelta(minutes=duration)).isoformat()
    json = {'communication_disabled_until': timeout}
    session = requests.patch(url, json=json, headers=headers)
    return session.status_code

@bot.event
async def on_ready():
    print('봇 켜짐')

@bot.event
async def on_message(message):
    if not message.author.bot:
        if message.channel.category_id != CATEGORY_ID:
            if any(keyword in message.content.lower() for keyword in DISCORD_KEYWORDS):
                if message.author.id != EXEMPT_USER_ID:
                    await message.delete() # 무단 홍보 삭제
                    status = timeout_user(message.author.id, message.guild.id, 1)
                    if status in range(200, 299): # 타임아웃 1분간 줍니다.
                        await message.channel.trigger_typing()
                        await message.channel.send(f"{message.author.mention}님, 무단홍보는 금지되어있습니다.") # 그 채널에 보내요.

                        embed = discord.Embed(title="경고", description="무단홍보를 하지마세요!", color=0xFF0000) # 디엠으로 알립니다
                        await message.author.send(embed=embed)

bot.run(TOKEN)