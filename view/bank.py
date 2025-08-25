import discord
from discord.ui import Button, View
from utils.config import Variable
from datetime import datetime, timedelta



class BankDeposit(View):
    def __init__(self, client, deposit: int, member: discord.Member):
        super().__init__(timeout=30)
        self.client = client
        self.deposit = deposit
        self.member = member

    @discord.ui.button(label='1 день', style=discord.ButtonStyle.blurple)
    async def one_day(self, interaction: discord.Interaction, button: Button):
        await self.process_deposit(interaction, 1, 1.1)

    @discord.ui.button(label='3 дня', style=discord.ButtonStyle.blurple)
    async def three_days(self, interaction: discord.Interaction, button: Button):
        await self.process_deposit(interaction, 3, 1.4)

    @discord.ui.button(label='7 дней', style=discord.ButtonStyle.blurple)
    async def seven_days(self, interaction: discord.Interaction, button: Button):
        await self.process_deposit(interaction, 7, 2.0)
        

    async def process_deposit(self, interaction: discord.Interaction, days: int, multiplier: float):
        try:
            if interaction.user != self.member:
                return

            end_date = (datetime.now() + timedelta(days=days))

            self.client.db.insert_bank(self.member.id, end_date, self.deposit, multiplier)
            self.client.db.update_member_cash(-self.deposit, self.member.id)


            if days == 1:
                day = 'день'
            elif days == 3:
                day = 'дня'
            elif days == 7:
                day = 'дней'
            embed = discord.Embed(title=Variable.succes_title,
                                  description=f'Вы оформили вклад на {days} {day} на сумму {self.deposit} {Variable.currency}',
                                  color=Variable.green_color)
            self.stop()
            await interaction.response.edit_message(embed=embed, view=None)
        except Exception as e:
            print(f'process_deposit() error: {e}')
    
    

    async def on_timeout(self):
        embed = discord.Embed(
            title='Время вышло!',
            description='Депозит отменен из-за бездействия',
            color=discord.Color.dark_grey()
        )
        await self.message.edit(embed=embed, view=None)


class BankWithdrawal(View):
    def __init__(self, client, member):
        super().__init__(timeout=30)
        self.client = client
        self.member = member

    @discord.ui.button(label='Вывод', style=discord.ButtonStyle.blurple)
    async def withdrawal(self, interaction: discord.Interaction, button: Button):
        try:
            if interaction.user != self.member:
                return
            
            deposit = self.client.db.get_bank_deposit(self.member.id)
            multiplier = self.client.db.get_bank_multiplier(self.member.id)
            result = int(deposit * multiplier)

            self.client.db.update_member_cash(result, self.member.id)
            self.client.db.delete_bank(self.member.id)

            if multiplier == 1.1:
                self.client.db.level_xp_update(self.member.id, 7)
            elif multiplier == 1.4:
                self.client.db.level_xp_update(self.member.id, 24)
            elif multiplier == 2.0:
                self.client.db.level_xp_update(self.member.id, 50)

            embed = discord.Embed(title='Деньги зачислены :white_check_mark:',
                                description=f'На вас счет поступило {result} {Variable.currency}',
                                color=Variable.green_color)
            
            self.stop()
            await interaction.response.edit_message(embed=embed, view=None)
        except Exception as e:
            print(f'withdrawal() error: {e}')



    async def on_timeout(self):
        embed = discord.Embed(
            title='Время вышло!',
            description=f'Можете забрать {Variable.currency} в любое другое время',
            color=discord.Color.dark_grey()
        )
        await self.message.edit(embed=embed, view=None)
