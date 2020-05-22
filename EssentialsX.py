import discord
from discord.ext import commands
from discord.utils import get
import asyncio
import os

Bot = commands.Bot(command_prefix='&')
Bot.remove_command('help')

@Bot.event
async def on_ready():
	await Bot.change_presence(activity= discord.Game(name= 'I am Online!'))

def postfix(num:int, end_1:str='год', end_2:str='года', end_3:str='лет'): # Функция обработрки постфикса
    num = num % 10 if num > 20 else num # Делим число на 10 и получаем то что осталось после деления, дальше проверка это больше чем 20 или нет, если больше то оставляем число не изменныс, а если меньше то заменяем число на остаток деления
    return end_1 if num == 1 else end_2 if 1 < num < 5 else end_3 # Тут уже просто прлверяем




@Bot.command() # Декоратор команды
async def ping(ctx): # # Название команды
    emb = discord.Embed( # Переменная ембеда
        title= 'Текущий пинг', # Заполняем заголовок
        description= f'{Bot.ws.latency * 1000:.0f} ms' # Запонлняем описание
    )
    await ctx.send(embed=emb) # Отпрвака ембеда


@Bot.command() # Декоратор команды
async def avatar(ctx, member : discord.Member = None): # Название команды и аргументы
    user = ctx.message.author if member == None else member # Проверка аргуменат и переменная участника
    emb = discord.Embed( # Переменная ембеда
        title=f'Аватар пользователя {user}', # Заполняем заголовок
        description= f'[Ссылка на изображение]({user.avatar_url})', # Запонлняем описание
        color=user.color # Устанавливаем цвет
    )
    emb.set_image(url=user.avatar_url) # Устанавливаем картинку
    await ctx.send(embed=emb) # Отпрвака ембеда


@Bot.command() # Декоратор команды
async def servercount(ctx): # Название команды
    await ctx.send(f'Бот есть на {len(Bot.guilds)} серверах') # Выводит кол-во серверов бота


@Bot.command() # Декоратор команды
async def knb(ctx, move: str = None): # Название команды и аргумент
    solutions = ["`ножницы`", "`камень`", "`бумага`"] # Варианты хода
    winner = "**НИЧЬЯ**" # Тут все понятно
    p1 = solutions.index(f"`{move.lower()}`") # Тут мы ищем номер хода пользователя
    p2 = random.randint(0, 2) # Ну тут бот "делает ход"
    if p1 == 0 and p2 == 1 or p1 == 1 and p2 == 2 or p1 == 2 and p2 == 0: # Проверка комбинации проигрыша
        winner = f"{ctx.message.author.mention} ты **Проиграл**"
    elif p1 == 1 and p2 == 0 or p1 == 2 and p2 == 1 or p1 == 0 and p2 == 2:  # Проверка комбинации выигрыша
        winner = f"{ctx.message.author.mention} ты **Выиграл**"
    await ctx.send(f"{ctx.message.author.mention} **=>** {solutions[p1]}\n{Bot.user.mention} **=>** {solutions[p2]}\n{winner}") # Отправка результатов


@Bot.command() # Декоратор команды
async def profile(ctx, userf: discord.Member = None): # Название команды и аргумент
    user = ctx.message.author if userf == None else userf # Проверка указан ли пользователь, если нет то заменяем автором команды
    status = user.status # Получаем статус

    if user.is_on_mobile() == True: stat = 'На телефоне' # Проверка статуса и указываем статус
    if status == discord.Status.online: stat = 'В сети' # Проверка статуса и указываем статус
    elif status == discord.Status.offline: stat = 'Не в сети' # Проверка статуса и указываем статус
    elif status == discord.Status.idle: stat = 'Не активен' # Проверка статуса и указываем статус
    elif status == discord.Status.dnd: stat = 'Не беспокоить' # Проверка статуса и указываем статус

    create_time = (datetime.datetime.today()-user.created_at).days # Узнаем кол-во дней в дискорде
    join_time = (datetime.datetime.today()-user.joined_at).days # Узнаем кол-во дней на сервере

    emb = discord.Embed(title='Профиль', colour= user.color) # Делаем ембед и устанавливаем цвет
    emb.add_field(name= 'Ник', value= user.display_name, inline= False) # Добавляем поле и заполняем 
    emb.add_field(name= 'ID', value= user.id, inline= False) # Добавляем поле и заполняем 
    
    if create_time == 0: # Проверка на число дней
        emb.add_field(name= 'Присоиденился к дискорду', value= f'{user.created_at.strftime("%d.%m.%Y")} ( Меньше дня )', inline= False) # Добавляем поле и заполняем дни в дискорде
    else:
        emb.add_field(name= 'Присоиденился к дискорду', value= f'{user.created_at.strftime("%d.%m.%Y")} ( {create_time} {postfix(create_time, "день", "дня", "дней")})', inline= False)# Добавляем поле и заполняем кол-во дней в дискорде и подбираем окончание
    if join_time == 0: # Проверка на число дней
        emb.add_field(name= 'Присоединился к серверу', value= f'{user.joined_at.strftime("%d.%m.%Y")} ( Меньше дня )', inline= False) # Добавляем поле и заполняем дни на сервере
    else:
        emb.add_field(name= 'Присоединился к серверу', value= f'{user.joined_at.strftime("%d.%m.%Y")} ( {join_time} {postfix(join_time, "день", "дня", "дней")} )', inline= False) # Добавляем поле и заполняем кол-во дней на сервере и подбираем окончание
    emb.add_field(name= 'Наивысшая роль', value= f"<@&{user.top_role.id}>", inline= False) # Добавляем поле и заполняем роль
    emb.add_field(name= 'Статус', value= stat, inline= False) # Добавляем поле и заполняем статус
    emb.set_thumbnail(url= user.avatar_url) # Устанавливаем картинку сбоку ( В душе хз как назвать xD )

    await ctx.send(embed=emb)


@Bot.command() # Декоратор команды
async def ran_avatar(ctx): # Название команды
    emb = discord.Embed(description= 'Вот подобраная Вам аватарка.') # Переменная ембеда и его описание
    emb.set_image(url=nekos.img('avatar')) # Тут мы с помощью новой библиотеки ищем картинку на тему аватар и ставим её в ембед
    await ctx.send(embed=emb)  # Отпрвака ембеда


@Bot.command() # Декоратор команды
async def ran_color(ctx): # Название команды
    clr = (random.randint(0,16777215)) # Генерируем рандомное число от 0 до 16777215, это нужно чтобы сделать цвет
    emb = discord.Embed( # Переменная ембеда
        description= f'Сгенерированый цвет : ``#{hex(clr)[2:]}``', # Jписание ембеда, и код с помощью которого мы делаем цвет
        colour= clr # Устанавливаем цвет ембеду
    )

    await ctx.send(embed=emb) # Отпрвака ембед


@Bot.command() # Декоратор команды
async def kiss(ctx, member : discord.Member): # Название команды и аргумент
    if member == ctx.message.author: # Проверка кого упомянули
        await ctx.send('Вы не можете поцеловать сами себя.')
    else:
        emb = discord.Embed(description= f'{member.mention}, Вас поцеловал(а) {ctx.message.author.mention}.') # Переменная ембеда и описание
        emb.set_image(url=nekos.img('kiss')) # Ищем картинку и ставим её в ембед

        await ctx.send(embed=emb) # Отпрвака ембед

        
@Bot.command() # Декоратор команды
async def hug(ctx, member : discord.Member): # Название команды и аргумент
    if member == ctx.message.author: # Проверка кого упомянули
        await ctx.send('Вы не можете обнять сами себя.')
    else:
        emb = discord.Embed(description= f'{member.mention}, Вас обнял(а) {ctx.message.author.mention}.') # Переменная ембеда и описание
        emb.set_image(url=nekos.img('hug')) # Ищем картинку и ставим её в ембед

        await ctx.send(embed=emb) # Отпрвака ембед

        
@Bot.command() # Декоратор команды
async def slap(ctx, member : discord.Member): # Название команды и аргумент
    if member == ctx.message.author: # Проверка кого упомянули
        await ctx.send('Вы не можете ударить сами себя.')
    else:
        emb = discord.Embed(description= f'{member.mention}, Вас ударил(а) {ctx.message.author.mention}.') # Переменная ембеда и описание
        emb.set_image(url=nekos.img('slap')) # Ищем картинку и ставим её в ембед

        await ctx.send(embed=emb) # Отпрвака ембед

        
@Bot.command() # Декоратор команды
async def pat(ctx, member : discord.Member): # Название команды и аргумент
    if member == ctx.message.author: # Проверка кого упомянули
        await ctx.send('Вы не можете погладить сами себя.')
    else:
        emb = discord.Embed(description= f'{member.mention}, Вас погладил(а) {ctx.message.author.mention}.') # Переменная ембеда и описание
        emb.set_image(url=nekos.img('pat')) # Ищем картинку и ставим её в ембед

        await ctx.send(embed=emb) # Отпрвака ембед


@Bot.command() # Декоратор команды
@commands.has_permissions(administrator= True) # Ограничение, делает так что бы юзать могит только люди с админ правами
async def say(self, ctx, channel: discord.TextChannel, *, text): # Название команды и аргументы
    text = text.split('|') # Делим текст
    emb = discord.Embed( # Переменная ембеда
        title= text[0], # Заголовок
        description = text[1], # Описание
        colour = 0x00ff80 # Цвет
    )
    for a in ctx.message.attachments: # Проверка на вложения картинок
        if a.url != None:
            emb.set_image(url= f"{a.url}")    
    await channel.send(embed=emb) # Отправка ембеда


@Bot.command() # Декоратор команды
@commands.has_permissions(administrator= True) # Ограничение, делает так что бы юзать могит только люди с админ правами
async def mute(ctx, member: discord.Member, *, reason): # Название команды и аргументы
    if member == ctx.message.author: # Проверка пользователя
        return await ctx.send("Вы не можете замутить сами себя.")
    msgg =  f'Ты кикнул пользователя {member}, по причине : {reason}.' if reason != None else f'Вы замутили пользователя {member}.' # Сообщение которе будет написано на сервере
    msgdm = f'Ты был кикнут на сервере {ctx.guild.name}, по причине : {reason}.' if reason != None else f'Вы были замучены на сервере {ctx.guild.name}.' # Сообщение которое будет написано пользователю
    mute_role = ctx.message.guild.get_role() # Роль мута, вставте айди
    await member.add_roles(mute_role) # Мутим
    await ctx.send(msgg) # Отправка сообщения на сервер
    await member.send(msgdm) # Отправка сообщения пользователю


@Bot.command() # Декоратор команды
@commands.has_permissions(administrator= True) # Ограничение, делает так что бы юзать могит только люди с админ правами
async def kick(ctx, member : discord.User, *, reason=None): # Название команды и аргументы
    if member == ctx.message.author: # Проверка пользователя
        return await ctx.send("Вы не можете кикнуть сами себя.")
    msgg =  f'Вы кикнули пользователя {member}, по причине : {reason}.' if reason != None else f'Вы кикнули пользователя {member}.' # Сообщение которое будет написано на сервере
    msgdm = f'Вы были кикнут на сервере {ctx.guild.name}, по причине : {reason}.' if reason != None else f'Вы были кикнуты на сервере {ctx.guild.name}.'  # Сообщение которое будет написано пользователю
    await ctx.send(msgg) # Отправка сообщения на сервер
    await member.send(msgdm) # Отправка сообщения пользователю
    await ctx.guild.kick(member, reason=reason) # Кик

    
@Bot.command() # Декоратор команды
@commands.has_permissions(administrator= True) # Ограничение, делает так что бы юзать могли только люди с админ правами
async def ban(ctx, member : discord.User, *, reason=None): # Название команды и аргументы
    if member == ctx.message.author: # Проверка пользователя
        return await ctx.send("Вы не можете забанить сами себя.")
    msgg =  f'Пользователь : {member}, забанен по причине : {reason}.' if reason != None else f'Пользователь : {member}, забанен.' # Сообщение которое будет написано на сервере
    msgdm = f'Вы были забанены на сервере {ctx.guild.name}, по причине : {reason}.' if reason != None else f'Вы были забанены на сервере : {ctx.guild.name}.' # Сообщение которое будет написано пользователю
    await ctx.send(msgg) # Отправка сообщения на сервер
    await member.send(msgdm) # Отправка сообщения пользователю
    await ctx.guild.ban(member, reason=reason) # Бан
    
    
@Bot.command() # Декоратор команды
@commands.has_permissions(administrator= True) # Ограничение, делает так что бы юзать могли только люди с админ правами
async def unban(ctx, idf : int): # Название команды и аргументы
    if idu == ctx.message.author.id: # Проверка айди
        return await ctx.send("Вы не можешь разбанить сам себя.")
    await Bot.get_user(idu).unban() # Розбан
    await ctx.send(f'Пользователь : {user}, разбанен.') # Отправка сообщения на сервер
       
    
@Bot.command() # Декоратор команды
@commands.has_permissions(administrator= True) # Ограничение, делает так что бы юзать могит только люди с админ правами
async def tempban(ctx, member : discord.Member, time:int, arg:str, *, reason=None): # Название команды и аргументы
    if member == ctx.message.author: # Проверка пользователя
        return await ctx.send("Вы не можете забанить сами себя.")
    msgg =  f'Пользователь : {member}, забанен по причине : {reason}.' if reason != None else f'Пользователь : {member}, забанен.' # Сообщение которое будет написано на сервере
    msgdm = f'Вы были забанены на сервере {ctx.guild.name}, по причине : {reason}.' if reason != None else f'Вы были забанены на сервере : {ctx.guild.name}.'   # Сообщение которое будет написано пользователю
    await ctx.send(msgg) # Отправка сообщения на сервер
    await member.send(msgdm) # Отправка сообщения пользователю
    await member.ban() # Бан
    if arg == "s":
        await asyncio.sleep(time)          
    elif arg == "m":
        await asyncio.sleep(time * 60)
    elif arg == "h":
        await asyncio.sleep(time * 60 * 60)
    elif arg == "d":
        await asyncio.sleep(time * 60 * 60 * 24)
    await member.unban() # Розбан
    await ctx.send(f'Пользователь : {member}, разбанен.') # Отправка сообщения на сервер
    await member.send(f'Вы были разбанены на сервере : {ctx.guild.name}') # Отправка сообщения пользователю


@Bot.event # Декоратор ивента
async def on_raw_reaction_add(payload): # Тип ивента и переменая с данными
    if payload.message_id == 703531462384812043: # Проверка сообщения
        if str(payload.emoji) == '<:python:703529499677163560>': # Проверка емоджи
            role = Bot.get_guild(payload.guild_id).get_role(703531041800847421) # Получаем роль
            member = Bot.get_guild(payload.guild_id).get_member(payload.user_id) # Получаем пользователя как участника сервера
            await member.add_roles(role) # Выдаём роль
        if str(payload.emoji) == '<:js:703530067619348532>': # Проверка емоджи
            role = Bot.get_guild(payload.guild_id).get_role(703531070162862101) # Получаем роль
            member = Bot.get_guild(payload.guild_id).get_member(payload.user_id) # Получаем пользователя как участника сервера
            await member.add_roles(role) # Выдаём роль
        if str(payload.emoji) == '<:cpp:703530469928599552>': # Проверка емоджи
            role = Bot.get_guild(payload.guild_id).get_role(703531115431985212) # Получаем роль
            member = Bot.get_guild(payload.guild_id).get_member(payload.user_id) # Получаем пользователя как участника сервера
            await member.add_roles(role) # Выдаём роль
        if str(payload.emoji) == '<:cs:703530530590818335>': # Проверка емоджи
            role = Bot.get_guild(payload.guild_id).get_role(703531144788049972) # Получаем роль
            member = Bot.get_guild(payload.guild_id).get_member(payload.user_id) # Получаем пользователя как участника сервера
            await member.add_roles(role) # Выдаём роль
        if str(payload.emoji) == '<:swift:703530609779408906>': # Проверка емоджи
            role = Bot.get_guild(payload.guild_id).get_role(703531193840173147) # Получаем роль
            member = Bot.get_guild(payload.guild_id).get_member(payload.user_id) # Получаем пользователя как участника сервера
            await member.add_roles(role) # Выдаём роль


@Bot.event # Декоратор ивента
async def on_raw_reaction_remove(payload): # Тип ивента и переменая с данными
    if payload.message_id == 703531462384812043: # Проверка сообщения
        if str(payload.emoji) == '<:python:703529499677163560>': # Проверка емоджи
            role = Bot.get_guild(payload.guild_id).get_role(703531041800847421) # Получаем роль
            member = Bot.get_guild(payload.guild_id).get_member(payload.user_id) # Получаем пользователя как участника сервера
            await member.remove_roles(role) # Убираем роль
        elif str(payload.emoji) == '<:js:703530067619348532>': # Проверка емоджи
            role = Bot.get_guild(payload.guild_id).get_role(703531070162862101) # Получаем роль
            member = Bot.get_guild(payload.guild_id).get_member(payload.user_id) # Получаем пользователя как участника сервера
            await member.remove_roles(role) # Убираем роль
        elif str(payload.emoji) == '<:cpp:703530469928599552>': # Проверка емоджи
            role = Bot.get_guild(payload.guild_id).get_role(703531115431985212) # Получаем роль
            member = Bot.get_guild(payload.guild_id).get_member(payload.user_id) # Получаем пользователя как участника сервера
            await member.remove_roles(role) # Убираем роль
        elif str(payload.emoji) == '<:cs:703530530590818335>': # Проверка емоджи
            role = Bot.get_guild(payload.guild_id).get_role(703531144788049972) # Получаем роль
            member = Bot.get_guild(payload.guild_id).get_member(payload.user_id) # Получаем пользователя как участника сервера
            await member.remove_roles(role) # Убираем роль
        elif str(payload.emoji) == '<:swift:703530609779408906>': # Проверка емоджи
            role = Bot.get_guild(payload.guild_id).get_role(703531193840173147) # Получаем роль
            member = Bot.get_guild(payload.guild_id).get_member(payload.user_id) # Получаем пользователя как участника сервера
            await member.remove_roles(role) # Убираем роль


@Bot.command() # Декоратор команды
async def place_react(ctx, msg: discord.Message, react: discord.Emoji):  # Название команды и агрументы
    await msg.add_reaction(react) # Добавляем реакцию

		
token = os.environ.get('BOT_TOKEN')

Bot.run(str(token))
	
#Bot.run(open('token1.txt', 'r').read()) # Строка запуска бота
