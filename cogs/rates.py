import discord, os
from discord.ext import commands
from utils.config import Variable
from view.add_bet import AddBetView
from Cybernator import Paginator
from dotenv import load_dotenv

load_dotenv()
RATE_ROLE_ID = os.getenv('RATE_ROLE_ID')



class RatesCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    # -------------------------------------------------- админ команды
    # создание ивента
    @commands.command(name='abet', aliases=['add_bet'])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def __add_bet(self, ctx):
        try:
            author_roles = []
            for row in ctx.author.roles:
                author_roles.append(row.id)

            if int(RATE_ROLE_ID) not in author_roles:
                embed = discord.Embed(title=Variable.error_title,
                                    description=f'Создавать ставки может только главный по додепу',
                                    color=Variable.red_color)
                
                await ctx.send(embed=embed)
                ctx.command.reset_cooldown(ctx)
                return

            embed = discord.Embed(title='Создать ставку', description=' ')
            
            view = AddBetView(self.client, ctx.author)
            view.message = await ctx.send(embed=embed, view=view)
        except Exception as e:
            print(f'error: {e}')


    # отмена ивента
    @commands.command(name='cbet', aliases=['cancel_bet'])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def __cancel_bet(self, ctx):
        pass


    # редактирование ивента
    @commands.command(name='ebet', aliases=['edit_bet'])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def __edit_bet(self, ctx):
        pass


    # добавление результата ивента
    @commands.command(name='rbet', aliases=['result_bet'])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def __result_bet(self, ctx):
        pass





    # -------------------------------------------------- пользовательские команды
    # просмотр ивентов
    @commands.command(name='rates')
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def __rates(self, ctx):
        try:
            embeds = []
            for row in self.client.db.cursor.execute("SELECT name, description, first_event_name, first_event_chance, second_event_name, second_event_chance FROM rates"):
                title = row[0]
                description = row[1]
                first_event_name = row[2]
                first_event_chance = row[3]
                second_event_name = row[4]
                second_event_chance = row[5]

                embed = discord.Embed(title=title,
                                    description=description,
                                    color=discord.Color.dark_teal())
                embed.add_field(name=first_event_name, value=f'Коэфицент: {first_event_chance}', inline=True)
                embed.add_field(name=second_event_name, value=f'Коэфицент: {second_event_chance}', inline=True)

                embeds.append(embed)
            
            message = await ctx.send(embed=embeds[0])
            page = Paginator(self.client, message, only=ctx.author, use_more=False, embeds=embeds, timeout= 120)
            await page.start()
        except Exception as e:
            print(f'rates error: {e}')



    # ставка





    

async def setup(client):
    await client.add_cog(RatesCog(client))