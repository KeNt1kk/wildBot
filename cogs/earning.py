# coin, rob, job, daily

import discord, random
from discord.ext import commands
from utils.config import Variable
from view.coin import CoinFlip

class EarningCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    
    @commands.command(name='coin')
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def __coin(self, ctx, bet: int = None):
        try:
            level = self.client.db.get_member_level(ctx.author.id)
            min_bet = level * 100

            if bet is None:
                embed = discord.Embed(title=Variable.error_title,
                                    description=f'Укажите сколько {Variable.currency} хотите депнуть',
                                    color=Variable.red_color)
                
                await ctx.send(embed=embed)
                ctx.command.reset_cooldown(ctx)
                return
            elif bet < 1:
                embed = discord.Embed(title=Variable.error_title,
                                    description=f'Нельзя депать меньше 1 {Variable.currency}',
                                    color=Variable.red_color)
                
                await ctx.send(embed=embed)
                ctx.command.reset_cooldown(ctx)
                return
            elif bet < min_bet:
                embed = discord.Embed(title=Variable.error_title,
                                    description=f'Минимальная ставка {min_bet} {Variable.currency}',
                                    color=Variable.red_color)
                
                await ctx.send(embed=embed)
                ctx.command.reset_cooldown(ctx)
                return
            elif self.client.db.get_member_cash(ctx.author.id) < bet:
                embed = discord.Embed(title=Variable.error_title,
                                    description='Нельзя депать больше чем у тебя есть!',
                                    color=Variable.red_color)
                
                await ctx.send(embed=embed)
                ctx.command.reset_cooldown(ctx)
                return
        
            embed = discord.Embed(
                title="Орёл или Решка?",
                description=f"Ставка: {bet} 💰",
                color=discord.Color.blue()
            )
            embed.set_footer(text=f"Игрок: {ctx.author.display_name}")
            
            view = CoinFlip(self.client, bet, ctx.author)
            view.message = await ctx.send(embed=embed, view=view)
        except Exception as e:
            print(f'error: {e}')



    @commands.command(name='rob')
    @commands.cooldown(1, 3600, commands.BucketType.user)
    async def __rob(self,ctx, member: discord.Member = None):
        try:
            author_cash = self.client.db.get_member_cash(ctx.author.id)
            if author_cash < 500:
                embed = discord.Embed(title='Ты слишком нищий :x:',
                                    description=f'Заработай хотя бы 500 {Variable.currency} что бы начать воровать',
                                    color=Variable.red_color)
                
                await ctx.send(embed=embed)
                ctx.command.reset_cooldown(ctx)
                return

            if member is None:
                embed = discord.Embed(title=Variable.error_title,
                                    description=f'Укажите какого игрока хотите грабануть',
                                    color=Variable.red_color)
                
                await ctx.send(embed=embed)
                ctx.command.reset_cooldown(ctx)
                return
            elif member.id == ctx.author.id:
                embed = discord.Embed(title=Variable.error_title,
                                    description=f'Нельзя воровать у самого себя',
                                    color=Variable.red_color)
                
                await ctx.send(embed=embed)
                ctx.command.reset_cooldown(ctx)
                return
            
            chance = random.randint(1, 10)
            member_cash = int(self.client.db.get_member_cash(member.id) / 10)
            author_cash = int(author_cash / 10)
            print(member_cash)

            if chance == 1:
                embed = discord.Embed(title='Ура! Вы обокрали человека :partying_face:',
                                    description=f'С кражи {member.mention} вы получили {member_cash} {Variable.currency}',
                                    color=discord.Color.gold())
                
                await ctx.send(embed=embed)

                self.client.db.update_member_cash(member_cash, '-', member.id)
                self.client.db.update_member_cash(member_cash, '+', ctx.author.id)

                self.client.db.level_xp_update(ctx.author.id, 20)
            else:
                embed = discord.Embed(title='Ты че?',
                                    description=f'Нельзя воровать у людей, штраф {author_cash} {Variable.currency}',
                                    color=Variable.red_color)
                
                await ctx.send(embed=embed)

                self.client.db.update_member_cash(author_cash, '-', ctx.author.id)

                self.client.db.level_xp_update(ctx.author.id, 5)
        except Exception as e:
            print(f'error: {e}')




    @commands.command(name='job')
    @commands.cooldown(1, 600, commands.BucketType.user)
    async def __job(self, ctx):
            try:
                level = self.client.db.get_member_level(ctx.author.id)
                reward = (random.randint(1, 50)) + (level * 50)

                self.client.db.update_member_cash(reward, '+', ctx.author.id)
                self.client.db.level_xp_update(ctx.author.id, 5)

                embed = discord.Embed(title=Variable.succes_title,
                                    description=f'На работе вы заработали {reward} {Variable.currency}',
                                    color=Variable.green_color)
                
                await ctx.send(embed=embed)
            except Exception as e:
                print(f'error: {e}')





async def setup(client):
    await client.add_cog(EarningCog(client))