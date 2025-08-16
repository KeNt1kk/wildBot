# leaderboard, profile, help

import discord
from Cybernator import Paginator
from discord.ext import commands
from utils.config import Variable

class AssistCog(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.command(name='help')
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def __help(self, ctx):
        try:
            embed = discord.Embed(title='Помощь по командам', color=discord.Color.dark_purple())
            embed.add_field(name='help', value='Узнать все доступные команды', inline=True)
            embed.add_field(name='job', value='Позволяет заработать валюты', inline=True)
            embed.add_field(name='leaderboard', value='Показывает таблицу лидеров', inline=True)
            embed.add_field(name='coin *ставка*', value='Позволяет совершить ставку сыграв в монетку', inline=True)
            embed.add_field(name='rob *участник*', value='Обворовать участника (опасно)', inline=True)
            embed.add_field(name='shop', value='Открывает магазин с ролями', inline=True)
            embed.add_field(name='buy *роль*', value='Покупка роли из магазина', inline=True)
            embed.add_field(name='profile [*пользователь*]', value='Отображает профиль пользователя', inline=True)
            embed.add_field(name='transfer *пользователь* *сумма*', value='Перевод денег другому пользователю', inline=True)
            embed.add_field(name='daily', value='(в разработке)', inline=True)
            embed.add_field(name='bank', value='(в разработке)', inline=True)

            await ctx.send(embed=embed)
        except Exception as e:
            print(f'error: {e}')


    @commands.command(name='ld', aliases=['leaderboard'])
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def __leaderboard(self, ctx):
        try:
            embeds = []
            members_in_list = []
            members_count = sum(1 for member in ctx.guild.members if not member.bot)
            place = 0

            
            for i in range(0, members_count, 7):
                embed = discord.Embed(title='Таблица лидеров 🏆', color=discord.Color.gold())
                embed.add_field(name='Место', value=' ', inline=True)
                embed.add_field(name='Участник', value=' ', inline=True)
                embed.add_field(name='Деньги', value=' ', inline=True)
                flag = 0
                for row in self.client.db.cursor.execute("SELECT name, cash FROM users ORDER BY cash DESC"):
                    if flag == 7:
                        break

                    if (row[0] is not None) and (row[0] not in members_in_list):
                        place += 1
                        embed.add_field(name=f'#{place}', value=' ', inline=True)
                        embed.add_field(name=f'{row[0]}', value=' ', inline=True)
                        embed.add_field(name=f'{row[1]} {Variable.currency}', value=' ', inline=True)
                        members_in_list.append(row[0])
                        flag += 1
                        
                embeds.append(embed)

            message = await ctx.send(embed=embeds[0])
            page = Paginator(self.client, message, only=ctx.author, use_more=False, embeds=embeds, timeout= 120)
            await page.start()
        except Exception as e:
            print(f'error: {e}')



    @commands.command(name='profile')
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def __profile(self, ctx, member: discord.Member = None):
        try:
            target = member or ctx.author
        
            total_wins = self.client.db.get_member_total_wins(target.id) or 0
            total_lose = self.client.db.get_member_total_lose(target.id) or 0
            cash = self.client.db.get_member_cash(target.id) or 0
            level = self.client.db.get_member_level(target.id) or 1

            embed = discord.Embed(
                title=f'Профиль {target.display_name}',
                color=discord.Color.dark_blue()
            )
            
            if target.avatar:
                embed.set_thumbnail(url=target.avatar.url)
            else:
                embed.set_thumbnail(url=target.default_avatar.url)
            
            embed.add_field(name='Статистика игр', value=f'Всего игр: {total_lose + total_wins}\nПобед: {total_wins}\nПоражений: {total_lose}', inline=True)
            embed.add_field(name='Информация', value=f'Деньги: {cash}\nУровень: {level}', inline=True)

            await ctx.send(embed=embed)
        except Exception as e:
            print(f'error: {e}')




async def setup(client):
    await client.add_cog(AssistCog(client))