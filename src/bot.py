import discord
import os
from discord.ext import commands
from oauth2client.service_account import ServiceAccountCredentials

from utils import get_sheet_id

from functools import partial


#local files
import api
import constants
import settings
# This example requires the 'message_content' intent.


logger = settings.logging.getLogger("bot")
import discord


class UserPos:
    def __init__(self):
        self.user_position = {}
        
    def get_pos(self, user_id) :
        if not (user_id in self.user_position.keys()):
            self.user_position[user_id] = 0
        
        return self.user_position[user_id]
        
    def increment_pos(self, user_id) :
        self.user_position[user_id] += 1


def run(sheet):
    intents = discord.Intents.default()
    intents.message_content = True
    sheet = sheet
    client = commands.Bot(command_prefix='$',intents=intents)
    users_position = UserPos()

    @client.event
    async def on_ready():
        logger.info(f"Logged in as {client.user}, ID : {client.user.id}")
        logger.info(f"Guild id : {client.guilds[0].id}")
        client.tree.copy_global_to(guild=settings.GUILDS_ID)
        await client.tree.sync(guild=settings.GUILDS_ID)

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


    @client.tree.command(description="changes the spreadsheet id", name="set_sheet")
    async def set_sheet(interaction: discord.Interaction, url: str):
        message = "changed spreadsheet id"
        id = get_sheet_id(url) 
        sheet.set_spreadsheet_id(id)
        await interaction.response.send_message(message)

        
    @client.command(description="button test", name="vote")
    async def vote(ctx):
        tweet = sheet.get_unclassified(users_position.get_pos(ctx.author.id))

        if(tweet == None):
            await ctx.send("Todos os tweets foram classificados!")
            return

        view = ButtonView(tweet=tweet, sheets=sheet, users_position=users_position, user_id = ctx.author.id)
        await ctx.send(f"Classifique o tweet: \n\n {tweet} \n\n ", view=view)

    @client.tree.command(description="reload the spreadsheet", name="reload")
    async def reload(interaction: discord.Interaction):
        message = "reloaded spreadsheet"
        sheet.reload()
        await interaction.response.send_message(message)

    client.run(os.getenv('DISCORD_API_TOKEN'))




class ButtonView(discord.ui.View):

    def __init__(self, sheets = None, tweet = None, users_position=None, user_id = None):
        super().__init__() 
        self.tweet = tweet
        self.user_id = user_id
        self.classes = constants.CLASSES
        self.users_position = users_position
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
        # for button_value in self.button_count.values():
        #     if button_value >= constants.MAXVOTES:
        #         self.sheets.check_votes(self.tweet)
        #         await self.disable_all_items(chosen_class)
        #         return

        if interaction.user.id in self.users:
            await interaction.response.send_message("Você já votou!", ephemeral=True)
            return

        self.sheets.vote(self.tweet, chosen_class)
        self.users_position.increment_pos(self.user_id)
        updated = self.sheets.check_votes(self.tweet)

        self.users.append(interaction.user.id)
        if updated:
            default_message = "Votos contados \n"; 
            vote_message = f"Classe do tweet definida com {constants.MAXVOTES} votos: \n` {self.tweet} ` : `{chosen_class}` \n\n"
            await interaction.response.send_message(default_message + vote_message)
            return
                
        await interaction.response.send_message("Seu voto foi contado!", ephemeral=True)

