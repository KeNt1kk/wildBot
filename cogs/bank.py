# transfer, bank

import discord
from discord.ext import commands
from utils.config import Variable

class BankCog(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.command(name='transfer', aliases=['ts'])
    @commands.cooldown(1, 3600, commands.BucketType.user)
    async def __transfer(self, ctx, member: discord.Member = None, amount: int = None):
        try:
            if member is None:
                embed = discord.Embed(title=Variable.error_title,
                                    description=f'Укажите кому хотите перевести деньги',
                                    color=Variable.red_color)
                
                await ctx.send(embed=embed)
                ctx.command.reset_cooldown(ctx)
                return
            elif member.id == ctx.author.id:
                embed = discord.Embed(title=Variable.error_title,
                                    description=f'Нельзя переводить деньги самому себе',
                                    color=Variable.red_color)
                
                await ctx.send(embed=embed)
                ctx.command.reset_cooldown(ctx)
                return
            
            if amount is None:
                embed = discord.Embed(title=Variable.error_title,
                                    description=f'Укажите сумму для перевода',
                                    color=Variable.red_color)
                
                await ctx.send(embed=embed)
                ctx.command.reset_cooldown(ctx)
                return
            
            elif amount < 10:
                embed = discord.Embed(title=Variable.error_title,
                                    description=f'Нельзя переводить меньше 10 {Variable.currency}',
                                    color=Variable.red_color)
                
                await ctx.send(embed=embed)
                ctx.command.reset_cooldown(ctx)
                return
            
            self.client.db.update_member_cash(amount, '-', ctx.author.id)
            self.client.db.update_member_cash(amount, '+', member.id)

            embed = discord.Embed(title=Variable.succes_title,
                                description=f'Пользователю {member.mention} успешно переведено {amount} {Variable.currency}',
                                color=Variable.green_color)
            
            await ctx.send(embed=embed)
        except Exception as e:
            print(f'error: {e}')





async def setup(client):
    await client.add_cog(BankCog(client))