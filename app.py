import json, random, datetime
import io
import nextcord
from nextcord import Interaction, File, ButtonStyle, Embed, Color, SlashOption, ChannelType, User, SelectOption
from nextcord.abc import GuildChannel
from nextcord.ext import commands
from nextcord.ui import Button, View, Select
import textwrap
import os

# aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa

false = "false"
true = "ttue"
val = "both"
myview = None

intents = nextcord.Intents.default()
intents.guilds = True
intents.members = True

helpGuide = json.load(open("help.json"))
links = json.load(open("images.json"))
bot = commands.Bot(command_prefix='')
serverID = 1209545708068409405

blacklist_words = ["nig", "ngger", "niger", "nger", "nigr", "nga"]

sent_msg = None

def createHelpEmbed(pageNum=0, inline=False):
    pageNum = (pageNum) % len(list(helpGuide))
    pageTitle = list(helpGuide)[pageNum]
    embed=Embed(color=0x0080ff, title=pageTitle)
    for key, val in helpGuide[pageTitle].items():
        embed.add_field(name=bot.command_prefix+key, value=val, inline=inline)
    embed.set_footer(text=f"Page {pageNum+1} of {len(list(helpGuide))}")
    return embed
    
@bot.slash_command(name='serverinfo', description='display information about this server', guild_ids=[serverID])
async def serverinfo(ctx):
    guild = ctx.guild
    embed = nextcord.Embed(title="Server Information", color=0x00ff00)
    embed.add_field(name="Server Name", value=guild.name, inline=False)
    embed.add_field(name="Server ID", value=guild.id, inline=False)
    embed.add_field(name="Owner", value=guild.owner, inline=False)
    embed.add_field(name="Region", value=guild.region, inline=False)
    embed.add_field(name="Total Members", value=guild.member_count, inline=False)
    
    if guild.icon:
        embed.set_thumbnail(url=guild.icon.url)
    
    await ctx.send(embed=embed)

@bot.slash_command(name='cat', description='cat', guild_ids=[serverID])
async def cat(interaction: Interaction):
    await interaction.send(random.choice(links[val]))
    
@bot.slash_command(name='help', description='Shows some list commands', guild_ids=[serverID])
async def Help(ctx):
    global sent_msg, myview

    currentPage = 0

    async def next_callback(interaction):
        nonlocal currentPage
        currentPage += 1
        await sent_msg.edit(embed=createHelpEmbed(pageNum=currentPage), view=myview)

    async def previous_callback(interaction):
        nonlocal currentPage
        currentPage -= 1
        await sent_msg.edit(embed=createHelpEmbed(pageNum=currentPage), view=myview)

    if myview is None:
        myview = View()
        myview.add_item(Button(label="Next", custom_id="next_button", style=ButtonStyle.green))
        myview.add_item(Button(label="Previous", custom_id="previous_button", style=ButtonStyle.red))

    sent_msg = await ctx.send(embed=createHelpEmbed(), view=myview)

@bot.slash_command(name='selectcat', description='Selects a cat on the menu', guild_ids=[serverID])
async def selectcat(interaction: Interaction):
    
    async def dropdown_callback(interaction):
        for value in dropdown.values:
            await interaction.send(f"Selected {value} as a random cat image")
            val = value
            print(val)
    
    option1 = SelectOption(label="Maxwell", value="maxwell", description="Maxwell Da Cat")
    option2 = SelectOption(label="Soggy Cat", value="soggycat", description="Soggy da cat (not wet!!!1111)")
    option3 = SelectOption(label="Both", value="both", description="picks both of the cat")
    dropdown = Select(placeholder="What cat will you pick as a random cat image?", options=[option1, option2, option3], max_values=3)
    
    dropdown.callback = dropdown_callback
    myview = View(timeout=180)
    myview.add_item(dropdown)
    
    await interaction.send("Pick da cat", view=myview)

@bot.slash_command(name='exec', description='Executes code.')
async def exec_code(ctx: commands.Context, *, code: str):
    try:
        eval = exec(code)
        await ctx.send(f"Code executed successfully:\n```{eval}```")
    except Exception as e:
        await ctx.send(f"Error occurred: {e}")
        
@bot.slash_command(name='info', description='displays information about me', guild_ids=[serverID])
async def aboutme(ctx):
    embed = nextcord.Embed(title="Bot Info", color=0x00ff00)
    embed.add_field(name="Owner", value="voix (npxcd#0000)", inline=False)
    embed.add_field(name="Version", value="beta", inline=False)
    embed.add_field(name="ID", value="1224244381364781178", inline=False)
    embed.add_field(name="Name", value="slog v2", inline=False)
    embed.add_field(name="Programmed on", value="Python", inline=False)
    
    embed.set_thumbnail(url="https://npcldtt.github.io/1.jpg")
    
    await ctx.send(embed=embed)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    
    send_bot_start_message = false
    
    if send_bot_start_message == true:
    	channel_id = 1201054631967596584
    	channel = bot.get_channel(channel_id)
    	if channel:
            await channel.send("")
            
async def on_message(message):
    if message.author == bot.user:
        return

    for word in blacklist_words:
        if word in message.content.lower():
            await message.delete()
            try:
                await message.channel.send(f"{message.author.name}, your message contained a blacklisted word and has been deleted.")
            except discord.HTTPException as e:
                print(f"Error sending message: {e}")
            return

    await bot.process_commands(message)

if __name__ == "__main__":
    bot.run(os.environ["DISCORD_TOKEN"])