import discord
from discord.ext import commands
from utils.config import Variable
from view.add_bet import AddBetModal, AddBetView



class RatesCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    # -------------------------------------------------- админ команды
    # создание ивента
    @commands.command(name='abet', aliases=['add_bet'])
    @commands.cooldown(10, 1, commands.BucketType.user)
    async def __add_bet(self, ctx):
        try:
            embed = discord.Embed(title='Ивенты', description='Описание ивента', color=discord.Color.dark_teal())
            embed.add_field(name='Событие 1', value='коэфицент на выйгрыш', inline=True)
            embed.add_field(name='Событие 2', value='коэфицент на выйгрыш', inline=True)
            await ctx.send(embed=embed)
        except Exception as e:
            print(f'error: {e}')


    # отмена ивента
    @commands.command(name='cbet', aliases=['cancel_bet'])
    @commands.cooldown(10, 1, commands.BucketType.user)
    async def __cancel_bet(self, ctx):
        pass


    # редактирование ивента
    @commands.command(name='ebet', aliases=['edit_bet'])
    @commands.cooldown(10, 1, commands.BucketType.user)
    async def __edit_bet(self, ctx):
        pass


    # добавление результата ивента
    @commands.command(name='rbet', aliases=['result_bet'])
    @commands.cooldown(10, 1, commands.BucketType.user)
    async def __result_bet(self, ctx):
        pass





    # -------------------------------------------------- пользовательские команды
    # просмотр ивентов



    # ставка





    

async def setup(client):
    await client.add_cog(RatesCog(client))