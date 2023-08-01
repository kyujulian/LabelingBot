import discord
import os
from discord.ext import commands
from oauth2client.service_account import ServiceAccountCredentials

from functools import partial


#local files
import api
import constants
import settings
# This example requires the 'message_content' intent.


logger = settings.logging.getLogger("bot")

import discord



def run(sheet):
    intents = discord.Intents.default()
    intents.message_content = True

    sheet = sheet

    client = commands.Bot(command_prefix='$',intents=intents)

    @client.event
    async def on_ready():
        logger.info(f"Logged in as {client.user}, ID : {client.user.id}")
        logger.info(f"Guild id : {client.guilds[0].id}")
        client.tree.copy_global_to(guild=settings.GUILDS_ID)
        await client.tree.sync(guild=settings.GUILDS_ID)

    @client.tree.command(description="Welcomes user" , name="greetings")
    async def ciao(interaction: discord.Interaction, url: str):
        message = 'ciao' + url
        await interaction.response.send_message(message)

    @client.tree.command(description="Sorts the original table" , name="sort")
    async def sorting(interaction: discord.Interaction, url: str):
        message = "Sheets sorted!"
        sheet.sort()
        await interaction.response.send_message(message)

    @client.tree.command(description="update sheets with classified data" , name="update_with_class")
    async def sorting(interaction: discord.Interaction):
        message = "updated sheets with classified data"
        sheet.update_with_class()
        await interaction.response.send_message(message)

        
    @client.command(description="button test", name="button")
    async def button(ctx):

        tweet = sheet.get_unclassified()
        if(tweet == None):
            await ctx.send("Todos os tweets foram classificados!")
            return
        view = ButtonView(tweet=tweet, sheets=sheet)
        await ctx.send(f"Classifique o tweet: \n {tweet} \n ", view=view)
        # await ctx.send(view=view)

    client.run(os.getenv('DISCORD_API_TOKEN'))




class ButtonView(discord.ui.View):

    def __init__(self, sheets = None, tweet = None):
        super().__init__() 
        self.tweet = tweet
        self.classes = constants.CLASSES
        self.buttons = [
            discord.ui.Button(label=c, style=discord.ButtonStyle.gray)\
            for c in self.classes
        ]

        self.sheets=sheets

        self.button_count = { c : 0 for c in self.classes }
            

        self.users = []
        for button in self.buttons:
            button.callback = partial(self.click_button,chosen_class=button.label)
            self.add_item(button)
        
    async def disable_all_items(self, chosen_class):
        self.sheets.add_and_write(self.tweet,chosen_class)

        for item in self.buttons:
            item.disable = True
    
    async def click_button(self,interaction: discord.Interaction,chosen_class: str):

        for button_value in self.button_count.values():
            if button_value >= constants.MAXVOTES:
                await interaction.response.send_message("Limite de votos alcançado!", ephemeral=True)
                await self.disable_all_items(chosen_class)
                return

        if interaction.user.id in self.users:
            await interaction.response.send_message("Você já votou!", ephemeral=True)
            return

        self.button_count[chosen_class] += 1
        self.users.append(interaction.user.id)

                

        logger.info(self.button_count)
        await interaction.response.send_message("Seu voto foi contado!", ephemeral=True)
