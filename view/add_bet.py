import discord
from discord.ext import commands
from discord.ui import Button, View, TextInput, Modal


class AddBetModal(Modal, title='Модальное окно'):
    def __init__(self, client):
        super().__init__(timeout=300)
        self.client = client
        self.pole1 = TextInput(label='Поле 1', placeholder='Подсказка')
        self.pole2 = TextInput(label='Поле 2', placeholder='Длинное поле', style=discord.TextStyle.long)
        self.add_item(self.pole1)
        self.add_item(self.pole2)

    
    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"{self.pole1.value}, {self.pole2.value}")


class AddBetView(View):
    def __init__(self, client):
        super().__init__(timeout=30)
        self.client = client

    @discord.ui.button(label='Открыть', style=discord.ButtonStyle.blurple)
    async def open_modal(self, interaction: discord.Interaction, button: Button):
        try:
            if interaction.user != self.member:
                    return
            
            self.stop()
            embed = discord.Embed(title='Открытие формы :white_check_mark:', description=' ')
            await interaction.response.edit_message(embed=embed, view=None)

            modal = AddBetModal(self.client)
            await interaction.response.send_modal(modal)
        except Exception as e:
             print(f'error: {e}')
             

    @discord.ui.button(label='Отмена', style=discord.ButtonStyle.red)
    async def close_command(self, interaction: discord.Interaction, button: Button):
        try:
            if interaction.user != self.member:
                    return
            
            self.stop()
            embed = discord.Embed(title='Отменено', description=' ')
            await interaction.response.edit_message(embed=embed, view=None)
        except Exception as e:
             print(f'error: {e}')


    async def on_timeout(self):
        embed = discord.Embed(
            title='Время вышло!',
            description='Команда отменена из-за бездействия',
            color=discord.Color.dark_grey()
        )
        await self.message.edit(embed=embed, view=None)