# shop, buy

import discord
from Cybernator import Paginator
from discord.ext import commands
from utils.config import Variable

class ShopCog(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.command(name = 'shop')
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def __shop(self, ctx):
        try:
            embeds = []
            roles_in_shop = []
            roles_counter = self.client.db.cursor.execute("SELECT COUNT(role_id) FROM shop").fetchone()[0] or 0
            place = 1
            if roles_counter == 0:
                embed = discord.Embed(title=Variable.error_title,
                                      description='В магазине нет ролей',
                                      color=Variable.red_color)
                
                await ctx.send(embed=embed)
                return

            for i in range(0, roles_counter, 5):
                embed = discord.Embed(title='Магазин ролей')
                flag = 0
                for row in self.client.db.cursor.execute("SELECT role_id, cost FROM shop"):
                    if flag == 5:
                        break
                    role = ctx.guild.get_role(row[0])
                    if (role is not None) and (row[0] not in roles_in_shop):
                        embed.add_field(name=f'#{place} {role.name}', value=f'Цена: {row[1]} {Variable.currency}', inline=False)
                        roles_in_shop.append(row[0])
                        flag += 1
                        place += 1
                embeds.append(embed)

            message = await ctx.send(embed=embeds[0])
            page = Paginator(self.client, message, only=ctx.author, use_more=False, embeds=embeds, timeout= 120)
            await page.start()
        except Exception as e:
            print(f'error: {e}')


    
    @commands.command(name='buy')
    @commands.cooldown(1, 3600, commands.BucketType.user)
    async def __buy(self, ctx, role: discord.Role = None):
        try:
            if role is None:
                embed = discord.Embed(title=Variable.error_title,
                                      description=f'Укажите какую роль хотите купить',
                                      color=Variable.red_color)
                
                await ctx.send(embed=embed)
                ctx.command.reset_cooldown(ctx)
                return
            elif self.client.db.get_role_id(role.id) is None:
                embed = discord.Embed(title=Variable.error_title,
                                      description=f'Роли {role.mention} нет в магазине',
                                      color=Variable.red_color)
                
                await ctx.send(embed=embed)
                ctx.command.reset_cooldown(ctx)
                return
            
            cash = self.client.db.get_member_cash(ctx.author.id)
            cost = self.client.db.get_role_cost(role.id)
            author_roles = []
            for row in ctx.author.roles:
                author_roles.append(row.id)

            if cash < cost:
                embed = discord.Embed(title=Variable.error_title,
                                      description=f'Недостаточно {Variable.currency} для покупки роли',
                                      color=Variable.red_color)
                
                await ctx.send(embed=embed)
                ctx.command.reset_cooldown(ctx)
                return
            elif role.id in author_roles:
                embed = discord.Embed(title=Variable.error_title,
                                      description=f'У вас уже есть роль {role.mention}',
                                      color=Variable.red_color)
                
                await ctx.send(embed=embed)
                ctx.command.reset_cooldown(ctx)
                return
            
            await ctx.author.add_roles(role)
            self.client.db.update_member_cash(cost, '-', ctx.author.id)

            embed = discord.Embed(title=Variable.succes_title,
                                  description=f'Вы успешно приобрели роль {role.mention}',
                                  color=Variable.green_color)
            
            await ctx.send(embed=embed)
        except Exception as e:
            print(f"Ошибка: {e}")




async def setup(client):
    await client.add_cog(ShopCog(client))