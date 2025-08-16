import discord, os
from discord.ext import commands
from utils.config import Variable
from utils.database import Database
from utils.functions import Functions
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('TOKEN')
PREFIX = os.getenv('PREFIX')

intents = discord.Intents.all()
client = commands.Bot(command_prefix = PREFIX, intents=intents)
client.remove_command('help')


@client.event
async def on_ready():
    await load_cogs()
    client.db = Database(client)
    print('Бот успешно подключен к дискорду')



@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        embed = discord.Embed(title=Variable.error_title,
                              description=f'Укажите корректное значение',
                              color=Variable.red_color)
        
        await ctx.send(embed=embed)
        ctx.command.reset_cooldown(ctx)

    elif isinstance(error, commands.CommandOnCooldown):
        cooldown = int(error.retry_after)
        time = Functions.format_time(cooldown)
        embed = discord.Embed(title=Variable.error_title,
                              description=f'⏳ Вы сможете использовать эту команду через {time}',
                              color=Variable.red_color)
        
        await ctx.send(embed=embed)

    elif isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(title=Variable.error_title,
                              description=f'У вас недостаточно прав для использования команды',
                              color=Variable.red_color)
        
        await ctx.send(embed=embed)
        ctx.command.reset_cooldown(ctx)


    elif isinstance(error, commands.NotOwner):
        embed = discord.Embed(title=Variable.error_title,
                              description=f'У вас недостаточно прав для использования команды',
                              color=Variable.red_color)
        
        await ctx.send(embed=embed)
    
    elif isinstance(error, commands.RoleNotFound):
        embed = discord.Embed(title=Variable.error_title,
                              description=f'Такой роли не существует',
                              color=Variable.red_color)
        
        await ctx.send(embed=embed)
        ctx.command.reset_cooldown(ctx)


@client.event
async def on_member_remove(member):
    pass



@client.event
async def on_member_join(member):
    member_name = str(member.name)
    client.db.cursor.execute("INSERT INTO users (user_id, name) VALUES (?, ?)", (member.id, member_name))
    client.db.connection.commit()



@client.command(name='load')
@commands.is_owner()
async def load(ctx, extension):
    try:
        await client.load_extension(f'cogs.{extension}')
        await ctx.send(f'расширение {extension} загружено')
    except Exception as e:
        print(f'Ошибка при загрузке расширения {extension}')
        await ctx.send('Не удалось загрузить расширение')



@client.command(name='unload')
@commands.is_owner()
async def unload(ctx, extension):
    try:
        await client.unload_extension(f'cogs.{extension}')
        await ctx.send(f'расширение {extension} отгружено')
    except Exception as e:
        print(f'Ошибка при загрузке расширения {extension}')
        await ctx.reply('Не удалось загрузить расширение')



@client.command(name='reload')
@commands.is_owner()
async def reload(ctx, extension):
    try:
        await client.unload_extension(f'cogs.{extension}')
        await client.load_extension(f'cogs.{extension}')
        await ctx.send(f'расширение {extension} перезапущено')
    except Exception as e:
        print(f'Ошибка при загрузке расширения {extension}')
        await ctx.send('Не удалось загрузить расширение')




async def load_cogs():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await client.load_extension(f'cogs.{filename[:-3]}')
            print(f'Расширение {filename} загружено')

client.run(TOKEN)