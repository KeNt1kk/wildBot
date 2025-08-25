import discord
from discord.ui import Button, View, TextInput, Modal
from utils.config import Variable


class AddBetModal(Modal, title='Информация о ставке'):
    def __init__(self, client):
        try:
            super().__init__(timeout=300)
            self.client = client
            self.title_input = TextInput(label='Название ставки', placeholder='введите название ставки', max_length=50)
            self.description_input = TextInput(label='Описание ставки', placeholder='введите краткое описание ставки', style=discord.TextStyle.long, max_length=300)
            self.first_event_name_input = TextInput(label='Событие 1', placeholder='имя участника / исход', max_length=50)
            self.event_chance_input = TextInput(label='Шанс на успех', placeholder='10 / 23.3 / 90.11')
            self.second_event_name_input = TextInput(label='Событие 2', placeholder='имя участника / исход', max_length=50)

            self.add_item(self.title_input)
            self.add_item(self.description_input)
            self.add_item(self.first_event_name_input)
            self.add_item(self.event_chance_input)
            self.add_item(self.second_event_name_input)
        except Exception as e:
            print(f'AddBetModal init error: {e}')

    
    async def on_submit(self, interaction: discord.Interaction):
        try:
            chance = float(self.event_chance_input.value)
            if (chance >= 100) or (chance <= 0):
                await interaction.response.send_message('В поле *шанс на успех* необходимо указать значение от 0.01 до 99.99')
                return
            
            second_event_chance = 100 - chance
            self.client.db.insert_rate(self.title_input.value, self.description_input.value, self.first_event_name_input.value, chance, self.second_event_name_input.value, second_event_chance)

            embed = discord.Embed(title=Variable.succes_title,
                                  description='Ставка успешно создана и добавлена в лист ставок',
                                  color=Variable.green_color)
            
            await interaction.response.send_message(embed=embed)
        except ValueError as e:
            print(f'AddBetModal on_submit value_error: {e}')
            await interaction.response.send_message('В поле *шанс на успех* необходимо указать цифру')
        except Exception as e:
            print(f'AddBetModal on_submit error: {e}')



class AddBetView(View):
    def __init__(self, client, member):
        super().__init__(timeout=30)
        self.client = client
        self.member = member

    @discord.ui.button(label='Создать', style=discord.ButtonStyle.blurple)
    async def open_modal(self, interaction: discord.Interaction, button: Button):
        try:
            if interaction.user != self.member:
                    return
            
            self.stop()
            modal = AddBetModal(self.client)
            await interaction.response.send_modal(modal)

            embed = discord.Embed(title='Открытие формы :white_check_mark:', description=' ', color=Variable.green_color)
            await interaction.edit_original_response(embed=embed, view=None)

        except Exception as e:
            print(f'AddBetView error: {e}')
             

    @discord.ui.button(label='Отмена', style=discord.ButtonStyle.red)
    async def close_command(self, interaction: discord.Interaction, button: Button):
        try:
            if interaction.user != self.member:
                    return
            
            self.stop()
            embed = discord.Embed(title='Отменено', description=' ', color=Variable.red_color)
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