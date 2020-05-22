import discord
from discord.ext import commands
import asyncio
import os

Bot = commands.Bot(command_prefix='&')
Bot.remove_command('help')

@Bot.event
async def on_ready():
	await Bot.change_presence(activity= discord.Game(name= '&help to open help menu'))
#Commands==========

@Bot.command()
async def help(ctx, page):
	if page == '1':
    embed = discord.Embed( #Показываем что это ембед
    title = 'Тут ваш заговолок' , #Загаловок
    description = 'Тут ваше описание' , #Описание
    colour = discord.Colour.gold #Цвет ебмеда
    ) #Закрываем ембед
    #Доп.Части ембеда
    embed.set_footer(text='Тут ваша строчка ебмеда') #Строчка ембеда
    embed.set_image(url='https://cdn.discordapp.com/attachments/710848456306065410/710879635168297010/1277_koichi.png') #Сылка на картинку
    embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/710848456306065410/710879917235241041/3802_corona_stare.png') #Сылка на картинку
    embed.set_author(name='Тут имя автора') # автор
    icon_url='https://cdn.discordapp.com/attachments/710848456306065410/710880495143092384/4109_tttgun.png' #Ава автора
    embed.add_field(name='Заговолок поля', value='Тут то что внутре ебмеда', inline=False) #Добовления поля
    embed.add_field(name='Заговолок поля', value='Тут то что внутре ебмеда', inline=False) #Добовления поля
    embed.add_field(name='Заговолок поля', value='Тут то что внутре ебмеда', inline=True) #Добовления поля

    await ctx.send(embed=embed) # Отпрвака ембед

  if page == '2':
    await ctx.send('123')
		
token = os.environ.get('EX_TOKEN') #переменная токена

Bot.run(str(token)) # строка запуска бота

# Bot.run('token') #для тех кто не на хостинге
