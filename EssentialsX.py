import discord
from discord.ext import commands
import asyncio
import os

Bot = commands.Bot(command_prefix='&')
Bot.remove_command('help')

@Bot.event
async def on_ready():
	await Bot.change_presence(activity= discord.Game(name= '&help to open Help menu.'))
#Commands==========

@Bot.command()
async def hello(ctx):
	await ctx.send('Hi')
		
token = os.environ.get('EX_TOKEN')

Bot.run(str(token))
	
#Bot.run(open('token1.txt', 'r').read()) # Строка запуска бота
