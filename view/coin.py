# class for buttons in coin command

import discord, random
from discord.ui import Button, View
from utils.config import Variable

class CoinFlip(View):
    def __init__(self, client, bet: int, member: discord.Member):
        super().__init__(timeout=30)
        self.client = client
        self.bet = int(bet)
        self.member = member
        self.result = None

    @discord.ui.button(label='Орёл', style=discord.ButtonStyle.green)
    async def heads_button(self, interaction: discord.Interaction, button: Button):
        try:
            if interaction.user != self.member:
                return
            
            self.result = random.choice(['Орёл', 'Решка'])
            win = self.result == 'Орёл'
            
            embed = discord.Embed(
                title=f'Результат: {self.result}',
                color=Variable.green_color if win else Variable.red_color
            )
            embed.add_field(name='Деп', value=f'{self.bet} {Variable.currency}')
            embed.add_field(name='Результат', value=f'Вы выиграли +{self.bet}' if win else f'Вы проиграли -{self.bet}')
            embed.set_footer(text=f'Игрок: {self.member.display_name}')
            
            if win:
                self.client.db.update_member_cash(self.bet, '+', self.member.id)
                self.client.db.update_member_total_wins(1, '+', self.member.id)
            else:
                self.client.db.update_member_cash(self.bet, '-', self.member.id)
                self.client.db.update_member_total_lose(1, '+', self.member.id)

            self.client.db.level_xp_update(self.member.id, 1)
            
            self.stop()
            await interaction.response.edit_message(embed=embed, view=None)
        except Exception as e:
            print(f'error: {e}')

    @discord.ui.button(label='Решка', style=discord.ButtonStyle.blurple)
    async def tails_button(self, interaction: discord.Interaction, button: Button):
        try:
            if interaction.user != self.member:
                return
            
            self.result = random.choice(['Орёл', 'Решка'])
            win = self.result == 'Решка'
            
            embed = discord.Embed(
                title=f'Результат: {self.result}',
                color=Variable.green_color if win else Variable.red_color
            )
            embed.add_field(name='Деп', value=f"{self.bet} {Variable.currency}")
            embed.add_field(name='Результат', value=f'Вы выиграли +{self.bet}' if win else f'Вы проиграли -{self.bet}')
            embed.set_footer(text=f'Игрок: {self.member.display_name}')

            if win:
                self.client.db.update_member_cash(self.bet, '+', self.member.id)
                self.client.db.update_member_total_wins(1, '+', self.member.id)
            else:
                self.client.db.update_member_cash(self.bet, '-', self.member.id)
                self.client.db.update_member_total_lose(1, '+', self.member.id)

            self.client.db.level_xp_update(self.member.id, 1)
                
            self.stop()
            await interaction.response.edit_message(embed=embed, view=None)
        except Exception as e:
            print(f'error: {e}')

    async def on_timeout(self):
        embed = discord.Embed(
            title='Время вышло!',
            description='Игра отменена из-за бездействия',
            color=discord.Color.dark_grey()
        )
        await self.message.edit(embed=embed, view=None)