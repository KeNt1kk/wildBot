# add_cash, take_cash, set, add_shop, delete_shop
# @commands.Cog.listener() // @commands.command()

import discord
from discord.ext import commands
from utils.config import Variable

class AdminCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    

    @commands.command(name='acash', aliases=['add_cash'])
    @commands.is_owner()
    async def __add_cash(self, ctx, amount: int = None, member: discord.Member = None):
        try:
            if amount is None:
                embed = discord.Embed(title=Variable.error_title,
                                      description=f'Укажите количество {Variable.currency} которое хотите добавить',
                                      color=Variable.red_color)
                
                await ctx.send(embed=embed)
                return
            elif amount < 1:
                embed = discord.Embed(title=Variable.error_title,
                                      description=f'Количество {Variable.currency} должно быть больше 1',
                                      color=Variable.red_color)
                
                await ctx.send(embed=embed)
                return
            
            if member is None:
                self.client.db.update_member_cash(amount, '+', ctx.author.id)

                embed = discord.Embed(title=Variable.succes_title,
                                      description=f'Игроку {ctx.author.mention} начислено {amount} {Variable.currency}',
                                      color=Variable.green_color)
                
                await ctx.send(embed = embed)
            elif member:
                self.client.db.update_member_cash(amount, '+', member.id)

                embed = discord.Embed(title=Variable.succes_title,
                                      description=f'Игроку {member.mention} начислено {amount} {Variable.currency}',
                                      color=Variable.green_color)
                
                await ctx.send(embed = embed)
        except Exception as e:
            print(f'error: {e}')



    @commands.command(name='tcash', aliases=['take_cash'])
    @commands.is_owner()
    async def __take_cash(self, ctx, amount: int = None, member: discord.Member = None):
        try:
            if amount is None:
                embed = discord.Embed(title=Variable.error_title,
                                      description=f'Укажите количество {Variable.currency} которое хотите отнять',
                                      color=Variable.red_color)
                
                await ctx.send(embed=embed)
                return
            elif amount < 1:
                embed = discord.Embed(title=Variable.error_title,
                                      description=f'Количество {Variable.currency} должно быть больше 1',
                                      color=Variable.red_color)
                
                await ctx.send(embed=embed)
                return
            
            if member is None:
                self.client.db.update_member_cash(amount, '-', ctx.author.id)

                embed = discord.Embed(title=Variable.succes_title,
                                      description=f'Игроку {ctx.author.mention} сняли {amount} {Variable.currency}',
                                      color=Variable.green_color)
                
                await ctx.send(embed = embed)
            elif member:
                self.client.db.update_member_cash(amount, '-', member.id)

                embed = discord.Embed(title=Variable.succes_title,
                                      description=f'Игроку {member.mention} сняли {amount} {Variable.currency}',
                                      color=Variable.green_color)
                
                await ctx.send(embed = embed)
        except Exception as e:
            print(f'error: {e}')




    @commands.command(name='set')
    @commands.is_owner()
    async def __set_cash(self, ctx, amount: int = None, member: discord.Member = None):
        try:
            if amount is None:
                embed = discord.Embed(title=Variable.error_title,
                                      description='Укажите количество денег которое хотите установить',
                                      color=Variable.red_color)
                
                await ctx.send(embed=embed)
                return
            
            if member is None:
                self.client.db.set_member_cash(amount, ctx.author.id)

                embed = discord.Embed(title=Variable.succes_title,
                                      description=f'Игроку {ctx.author.mention} {Variable.currency} были установлены на {amount}',
                                      color=Variable.green_color)
                
                await ctx.send(embed = embed)
            elif member:
                self.client.db.set_member_cash(amount, member.id)

                embed = discord.Embed(title=Variable.succes_title,
                                      description=f'Игроку {member.mention} {Variable.currency} были установлены на {amount}',
                                      color=Variable.green_color)
                
                await ctx.send(embed = embed)
        except Exception as e:
            print(f'error: {e}')




    @commands.command(name='dshop', aliases=['delete_shop'])
    @commands.is_owner()
    async def __delete_role_from_shop(self, ctx, role: discord.Role = None):
        try:
            if role is None:
                embed = discord.Embed(title=Variable.error_title,
                                    description=f'Укажите какую роль хотите удалить',
                                    color=Variable.red_color)
                
                await ctx.send(embed=embed)
                return
            elif self.client.db.get_role_id(role.id) is None:
                embed = discord.Embed(title=Variable.error_title,
                                    description=f'Роли {role.mention} не существует в магазине',
                                    color=Variable.red_color)
                
                await ctx.send(embed=embed)
                return
            
            self.client.db.delete_role(role.id)

            embed = discord.Embed(title=Variable.succes_title,
                                description=f'Роль {role.mention} была успешно убрана из магазина',
                                color=Variable.green_color)
            
            await ctx.send(embed=embed)
        except Exception as e:
            print(f'error: {e}')



    @commands.command(name='ashop', aliases=['add_shop'])
    @commands.is_owner()
    async def __add_role_to_shop(self, ctx, role: discord.Role = None, cost: int = None):
        try:
            if role is None:
                embed = discord.Embed(title=Variable.error_title,
                                    description=f'Укажите какую роль хотите добавить в магазин',
                                    color=Variable.red_color)
                
                await ctx.send(embed=embed)
                return
            elif self.client.db.get_role_id(role.id) is not None:
                embed = discord.Embed(title=Variable.error_title,
                                    description=f'Роль {role.mention} уже есть в магазине',
                                    color=Variable.red_color)
                
                await ctx.send(embed=embed)
                return

            if cost is None:
                embed = discord.Embed(title=Variable.error_title,
                                    description='Укажите стоимость роли',
                                    color=Variable.red_color)
                
                await ctx.send(embed = embed)
                return
            elif cost < 1:
                embed = discord.Embed(title=Variable.error_title,
                                    description=f'Стоимость роли не может быть меньше 1',
                                    color=Variable.red_color)
                
                await ctx.send(embed=embed)
                return
        
            self.client.db.cursor.execute("INSERT INTO shop VALUES (?, ?)", (role.id, cost))
            self.client.db.connection.commit()
            embed = discord.Embed(title=Variable.succes_title,
                                description=f'Роль {role.mention} была успешно добавлена в магазин',
                                color=Variable.green_color)
            
            await ctx.send(embed=embed)
        except Exception as e:
            print(f'error: {e}')

    

    @commands.command(name='check_xp')
    @commands.is_owner()
    async def __check_xp(self, ctx, member: discord.Member = None):
        if member is None:
            level_xp = self.client.db.get_member_level_xp(ctx.author.id)
            await ctx.send(level_xp)
        elif member:
            level_xp = self.client.db.get_member_level_xp(member.id)
            await ctx.send(level_xp)




async def setup(client):
    await client.add_cog(AdminCog(client))