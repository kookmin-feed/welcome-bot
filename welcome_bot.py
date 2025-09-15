import discord
from discord.ext import commands
import dotenv
import os

dotenv.load_dotenv()

# 봇 설정
TOKEN = os.getenv("TOKEN")  # 봇 토큰
WELCOME_CHANNEL_ID = os.getenv("WELCOME_CHANNEL_ID")  # 채널 ID (int 변환)

intents = discord.Intents.default()
intents.members = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"✅ 로그인 완료: {bot.user}")


@bot.event
async def on_member_join(member):
    # Embed 만들기
    embed = discord.Embed(
        title="🎉 환영합니다!",
        description=f"{member.mention}님, KOOKMIN-FEED에 오신 것을 환영합니다!\n아래 버튼을 눌러 튜토리얼을 확인해 주세요.",
        color=discord.Color.green(),
    )
    embed.set_thumbnail(url=member.display_avatar.url)  # 프로필 이미지
    embed.set_footer(text="KOOKMIN-FEED 봇")

    # 버튼 만들기
    view = discord.ui.View()
    view.add_item(
        discord.ui.Button(
            label="튜토리얼 보기",
            url="https://voltaic-tapir-bd5.notion.site/KOOKMIN-FEED-1a7615c17a4980b9a39be4a744112c59",
            style=discord.ButtonStyle.link,
        )
    )

    # 1) 채널에 전송
    channel = bot.get_channel(WELCOME_CHANNEL_ID)
    if channel:
        await channel.send(embed=embed, view=view)
        print(f"📩 {member.name}님 환영 Embed (채널) 전송 완료")

    # 2) DM 전송
    try:
        await member.send(embed=embed, view=view)
        print(f"📩 {member.name}님 환영 Embed (DM) 전송 완료")
    except discord.Forbidden:
        print(
            f"⚠️ {member.name}님이 DM을 차단했거나 서버 멤버로부터 DM 수신이 꺼져 있음"
        )


bot.run(TOKEN)
