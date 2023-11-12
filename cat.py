# Imports
import discord
from discord.ext import commands
import httpx

# Intents + Prefix
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='c!', intents=intents)

# When bot is ready
@bot.event
async def on_ready():
    print(f'Cat command is now ready!')

# Cat command
@bot.command(name='cat')
async def get_cat_picture(ctx):
    """Get a random cat picture."""
    cat_api_url = 'https://api.thecatapi.com/v1/images/search'

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(cat_api_url)
            cat_data = response.json()

        cat_picture_url = cat_data[0]['url']
        await ctx.send(f"Found a funny cat picture!\n{cat_picture_url}")
    except Exception as e:
        print(f'Error fetching cat picture: {e}')
        await ctx.send('An error occurred while fetching the cat picture. Please try again later.')

# Error handler
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Command not found. Use `c!help` for a list of available commands.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Missing required argument. Check the command usage with `c!help`.")
    elif isinstance(error, commands.CommandInvokeError):
        await ctx.send(f"Error executing the command: {error.original}")
    else:
        await ctx.send(f"An error occurred: {error}")

# Bot token
bot.run('your_token')
