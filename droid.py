import discord
from discord.ext import commands
import os
import sys
import asyncio
import re

client =commands.Bot(command_prefix='b!')
client.remove_command('help')

with open("./admins.txt") as f:
    admins = f.read()

@client.command()
async def help(ctx):
    await ctx.send('>>> ヘルプを表示しています。\n```b!help 今表示してるやつだよ```\n```b!youtube 開発者のYouTubeチャンネル表示```\n```b!intro_bot このBOTの紹介ビデオを表示するよ！```\n```b!server_list 公認サーバーのリストを表示```\n```b!gban <ID> 指定されたユーザーをGBANするよ```\n```b!ungban <ID> 指定されたユーザーのGBAN解除するよ```')

@client.command()
async def youtube(ctx):
    await ctx.send('>>> 開発者ぶろりーのYouTubeドス！\nhttps://www.youtube.com/channel/UCbp2wAJ1JBYGwXeAQLICAUw?view_as=subscriber%60%60%60')

@client.command()
async def intro_bot(ctx):
    await ctx.send('>>> BROLIYSYSTEMの紹介動画です。\n-まだ無い..許してヒヤシンス-')

@client.command()
async def server_list(ctx):
    await ctx.send('>>> 公認サーバーのリストです。\nhttps://discord.gg/RGwTZzf\nhttps://discord.gg/92eH2U7\nhttps://discord.gg/tQG5GMC')

@client.command()
async def restart(ctx, type=None):
    if re.search(f"{ctx.author.id}", f"{admins}") != None:
        if type == None:
            await ctx.send('botを再起動します。')
            python = sys.executable
            os.execl(python, python, *sys.argvsys.cmd)
    else:
        await ctx.send('再起動できるのは管理者のみです。')

@client.command()
async def runcmd(ctx, * , cmd):
    k=os.system(cmd)
    await ctx.send(k)

@client.command()
async def leaveserver(ctx,serverid= None):
    if serverid == None:
        await ctx.send("エラー: サーバーIDが入力されていないか正しくありません。")
        return
    guild = await client.fetch_guild(serverid)
    status = await ctx.send(f"{guild.name}から退出しています...")
    await guild.leave()
    await status.edit(f"{guild.name}から退出しました。")

@client.command()
async def gban(ctx, user):
    if re.search(f"{ctx.author.id}", f"{admins}") != None:
        if re.search(f"{user}", f"{admins}") != None:
            await ctx.send(" 管理者をGBANすることはできません")
            return
        user = await client.fetch_user(user)
        status = await ctx.send(f"{user.name}をGBANしています...")
        try:
            for guild in client.guilds:
                await guild.ban(user, reason="Broccoli Systemによる自動GBANです。")
        except discord.Forbidden:pass
        await status.edit(content=f"{user.name}のGBANが完了しました。")
    else:
        await ctx.send("管理者のみが実行可能なコマンドです")

@client.command()
async def ungban(ctx, user):
    if re.search(f"{ctx.author.id}", f"{admins}") != None:
        user = await client.fetch_user(user)
        status = await ctx.send(f"{user.name}のGBANを解除しています...")
        try:
            for guild in client.guild:
                await guild.unban(user, reason="Broccoli Systemによる自動GBANです。")
        except discord.Forbidden:
            pass
        await status.edit(content=f"{user.name}のGBAN解除が完了しました。")
    else:
        await ctx.send("管理者のみが実行可能なコマンドです")

@client.command()
async def addadmin(ctx, user):
    if re.search(f"{ctx.author.id}", f"{admins}") != None:
        with open("./admins.txt") as f:
            admin = f.read()
        with open("./admins.txt", mode='w') as f:
            f.write(f"{admin},{user}")
        await ctx.send("設定を変更しました、再起動します。")
        python = sys.executable
        os.execl(python, python, *sys.argv)
    else:
        await ctx.send("管理者のみが実行可能なコマンドです")

@client.command()
async def show_server(ctx):
    await ctx.send(f"サーバー数:{len(client.guilds)}")
    for guild in client.guilds:
        await ctx.author.send(f"{guild.name}(id:{guild.id})")

@client.event
async def on_command_error(ctx,error):
    if isinstance(error,commands.CommandNotFound):
        await ctx.channel.send(f"コマンドが正しくありません。\nb!helpを参照してください。\n実行コマンド:{ctx.content}")
    else:
        await ctx.channel.send(f"エラーが発生しました。\nエラー内容:{error}")

@client.event
async def on_ready():
    ch = await client.fetch_channel("672431630656208910")
    await ch.send(">>> 起動完了```Broccoli Systemがオンラインになりました。```")

with open("./token.txt") as f:
    token=f.read()

client.run(token)