# transfer, bank

import discord
from discord.ext import commands
from utils.config import Variable
from view.bank import BankDeposit, BankWithdrawal
from datetime import datetime, timedelta

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
            
            self.client.db.update_member_cash(-amount, ctx.author.id)
            self.client.db.update_member_cash(amount, member.id)

            embed = discord.Embed(title=Variable.succes_title,
                                description=f'Пользователю {member.mention} успешно переведено {amount} {Variable.currency}',
                                color=Variable.green_color)
            
            await ctx.send(embed=embed)
        except Exception as e:
            print(f'error: {e}')




    @commands.command(name='bank')
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def __bank(self, ctx, amount: int = None):
        try:
            if self.client.db.get_bank_id(ctx.author.id):
                end_date = self.client.db.get_bank_end_date(ctx.author.id)
                if end_date > datetime.now():
                    term = str(end_date - datetime.now()).split('.')[0]
                    embed = discord.Embed(title='У вас уже есть вклад :x:',
                                            description=f'Вы сможете забрать {Variable.currency} через {term}',
                                            color=Variable.red_color)
                    
                    await ctx.send(embed=embed)
                    return
                else:
                    embed = discord.Embed(title='Срок хранения вклада закончился :white_check_mark:',
                                          description=f'Вы можете вывести {Variable.currency} прямо сейчас!',
                                          color=discord.Color.gold())
                    
                    view = BankWithdrawal(self.client, ctx.author)
                    view.message = await ctx.send(embed=embed, view=view)
                    return

            member_cash = self.client.db.get_member_cash(ctx.author.id)
            if amount is None:
                embed = discord.Embed(title=Variable.error_title,
                                        description=f'Укажите сумму для вклада',
                                        color=Variable.red_color)
                    
                await ctx.send(embed=embed)
                return
            elif amount < 1000:
                embed = discord.Embed(title=Variable.error_title,
                                        description=f'Минимальная сумма вклада 1000 {Variable.currency}',
                                        color=Variable.red_color)
                    
                await ctx.send(embed=embed)
                return
            elif member_cash < amount:
                embed = discord.Embed(title=Variable.error_title,
                                        description=f'У вас не хватает {Variable.currency} для вклада',
                                        color=Variable.red_color)
                    
                await ctx.send(embed=embed)
                return
            elif amount > 100000:
                embed = discord.Embed(title=Variable.error_title,
                                        description=f'Максимальная сумма вклада 1000 {Variable.currency}',
                                        color=Variable.red_color)
                    
                await ctx.send(embed=embed)
                return
            
            embed = discord.Embed(title='Выберите вид вклада',
                                  color=discord.Color.dark_blue())
            embed.add_field(name='1 день', value='Срок вклада: 1 день\nПроценты: 10%', inline=False)
            embed.add_field(name='3 дня', value='Срок вклада: 3 дня\nПроценты: 40%', inline=False)
            embed.add_field(name='7 дней', value='Срок вклада: 7 дней\nПроценты: 100%', inline=False)
            
            view = BankDeposit(self.client, amount, ctx.author)
            view.message = await ctx.send(embed=embed, view=view)
        except Exception as e:
            print(f'command "bank" error: {e}')





async def setup(client):
    await client.add_cog(BankCog(client))