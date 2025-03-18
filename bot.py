import discord
from discord import app_commands
from discord.ext import commands
import json
import os
from datetime import datetime


with open("config.json", "r") as config_file:
    config = json.load(config_file)

TOKEN = config["bot_token"]
REQUIRED_ROLE_ID = config["required_role_id"]
RESTORE_ALLOWED_USERS = config["restore_allowed_users"]
ALLOWED_CHANNEL_ID = config["allowed_channel_id"] 
product_embeds_file = "product-embeds.json"
EMBED_REQUIRED_ROLE_ID = config["embed_required_role_id"]
CUSTOMER_ROLE_ID = config["customer_role_id"] 
CREATE_EMBED_ALLOWED_USERS = config["create_embed_allowed_users"]



intents = discord.Intents.default()
intents.members = True
intents.messages = True
bot = commands.Bot(command_prefix="!", intents=intents)
vouches_file = "vouches.json"


if not os.path.exists(vouches_file):
    with open(vouches_file, "w") as f:
        json.dump([], f)

def load_vouches():
    try:
        with open(vouches_file, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

def save_vouches(vouches):
    with open(vouches_file, "w") as f:
        json.dump(vouches, f, indent=4)

@bot.event
async def on_ready():
    print(f'✅ Logged in as {bot.user}')
    try:
        synced = await bot.tree.sync()
        print(f'✅ Synced {len(synced)} commands.')
    except Exception as e:
        print(f'❌ Error syncing commands: {e}')


@bot.tree.command(name="vouch", description="Create a Vouch")
@app_commands.describe(
    message="Your rating",
    stars="Choose a star rating",
    proof="Image as proof"
)
@app_commands.choices(
    stars=[
        app_commands.Choice(name="⭐", value="⭐"),
        app_commands.Choice(name="⭐⭐", value="⭐⭐"),
        app_commands.Choice(name="⭐⭐⭐", value="⭐⭐⭐"),
        app_commands.Choice(name="⭐⭐⭐⭐", value="⭐⭐⭐⭐"),
        app_commands.Choice(name="⭐⭐⭐⭐⭐", value="⭐⭐⭐⭐⭐")
    ]
)
async def vouch(interaction: discord.Interaction, message: str, stars: str, proof: discord.Attachment = None):
    
    if interaction.channel.id != ALLOWED_CHANNEL_ID:
        await interaction.response.send_message("❌ You can only use this command in the allowed channel.", ephemeral=True)
        return

    
    if REQUIRED_ROLE_ID not in [role.id for role in interaction.user.roles]:
        await interaction.response.send_message("❌ You don't have the required customer role to use this command.", ephemeral=True)
        return

    vouches = load_vouches()
    vouch_number = len(vouches) + 1
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

    vouch_info = {
        "vouch_number": vouch_number,
        "vouched_by": interaction.user.mention,
        "message": message,
        "stars": stars,
        "proof": proof.url if proof else None,
        "timestamp": timestamp
    }
    vouches.append(vouch_info)
    save_vouches(vouches)

    embed = discord.Embed(title="New vouch created!", color=discord.Color.green())
    embed.add_field(name="Bewertung:", value=stars, inline=False)
    embed.add_field(name="Vouch:", value=message, inline=False)
    embed.add_field(name="Vouch N°:", value=str(vouch_number), inline=True)
    embed.add_field(name="Vouched by:", value=interaction.user.mention, inline=True)
    embed.add_field(name="Vouched at:", value=timestamp, inline=True)
    embed.set_footer(text="© 2025 LTXX — All Rights Reserved.")
    if proof:
        embed.set_thumbnail(url=proof.url)

    await interaction.response.send_message("✅ Your Vouch has been successfully created! Thanks for vouching.", ephemeral=True)
    await interaction.channel.send(embed=embed)


@bot.tree.command(name="vouch-restore", description="Restores all vouches")
async def vouch_restore(interaction: discord.Interaction):
    
    if interaction.user.id not in RESTORE_ALLOWED_USERS:
        await interaction.response.send_message("❌ You don't have permissions to use this command!", ephemeral=True)
        return

    vouches = load_vouches()
    if not vouches:
        await interaction.response.send_message("❌ There are no stored vouches.", ephemeral=True)
        return
    
    restored_vouches_count = 0
    for vouch in vouches:
        embed = discord.Embed(title="Restored Vouch", color=discord.Color.green())
        embed.add_field(name="Bewertung:", value=vouch["stars"], inline=False)
        embed.add_field(name="Vouch:", value=vouch["message"], inline=False)
        embed.add_field(name="Vouch N°:", value=str(vouch["vouch_number"]), inline=True)
        embed.add_field(name="Vouched by:", value=vouch["vouched_by"], inline=True)
        embed.add_field(name="Vouched at:", value=vouch["timestamp"], inline=True)
        embed.set_footer(text="© 2025 LTXX — All Rights Reserved.")
        if vouch["proof"]:
            embed.set_thumbnail(url=vouch["proof"])
        
        await interaction.channel.send(embed=embed)
        restored_vouches_count += 1

    
    print(f"{interaction.user} successfully restored all {restored_vouches_count} vouches!")

    await interaction.response.send_message(f"✅ {interaction.user.mention} successfully restored all {restored_vouches_count} vouches!", ephemeral=True)


product_embeds_file = "product-embeds.json"

def load_product_embeds():
    try:
        with open(product_embeds_file, "r", encoding="utf-8") as f:  
            return json.load(f)
    except json.JSONDecodeError:
        return {}

def save_product_embeds(embeds):
    with open(product_embeds_file, "w", encoding="utf-8") as f: 
        json.dump(embeds, f, indent=4, ensure_ascii=False)  


@bot.tree.command(name="embed", description="Create and send product embed")
@app_commands.describe(product="Choose a product to create an embed")
@app_commands.choices(
    product=[
        app_commands.Choice(name="Spotify Premium", value="spotify-premium"),
        app_commands.Choice(name="Netflix", value="netflix"),
        app_commands.Choice(name="Prime Video", value="prime-video"),
        app_commands.Choice(name="Crunchyroll", value="crunchyroll"),
        app_commands.Choice(name="Disney+", value="disney+"),
        app_commands.Choice(name="YouTube Premium", value="youtube-premium"),
        app_commands.Choice(name="Minecraft", value="minecraft"),
        app_commands.Choice(name="Social Panel", value="social-panel"),
        app_commands.Choice(name="Exchange", value="exchange")
    ]
)
async def embed(interaction: discord.Interaction, product: str):
    
    if EMBED_REQUIRED_ROLE_ID not in [role.id for role in interaction.user.roles]:
        await interaction.response.send_message("❌ You don't have the required role to use this command.", ephemeral=True)
        return

    
    embeds = load_product_embeds()

    
    if product not in embeds:
        await interaction.response.send_message(f"❌ The product `{product}` does not exist!", ephemeral=True)
        return

    
    product_info = embeds[product]
    title = product_info.get("title", "No title")
    description = product_info.get("description", "No description available")
    details = product_info.get("details", "No details available")
    banner_url = product_info.get("banner", None)

  
    embed = discord.Embed(title=title, description=description, color=discord.Color.green())
    embed.add_field(name="Details", value=details, inline=False)

    
    if banner_url:
        embed.set_image(url=banner_url)

    embed.set_footer(text="© 2025 LTXX — All Rights Reserved.")
    
    
    await interaction.response.send_message(embed=embed)


@bot.tree.command(name="give-customer", description="Assign a customer role to a user.")
@app_commands.describe(user="The user to assign the customer role to")
async def give_customer(interaction: discord.Interaction, user: discord.User):
    
    if not interaction.user.guild_permissions.manage_roles:
       
        embed = discord.Embed(
            title="❌ Permission Denied",
            description="You don't have permission to manage roles!",
            color=discord.Color.red()
        )
        embed.set_footer(text="© 2025 LTXX — All Rights Reserved.")
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return

    
    guild = interaction.guild

    
    role = guild.get_role(CUSTOMER_ROLE_ID)

    if not role:
       
        embed = discord.Embed(
            title="❌ Role Not Found",
            description="The specified customer role does not exist.",
            color=discord.Color.red()
        )
        embed.set_footer(text="© 2025 LTXX — All Rights Reserved.")
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return

    
    member = await guild.fetch_member(user.id)  

    if not member:
        
        embed = discord.Embed(
            title="❌ User Not Found",
            description=f"Could not find the member {user.name}.",
            color=discord.Color.red()
        )
        embed.set_footer(text="© 2025 LTXX — All Rights Reserved.")
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return

    try:
       
        await member.add_roles(role)
        
        
        embed = discord.Embed(
            title="Role successfully assigned",
            description=f"The user <@{user.id}> has received the Customer role.",
            color=discord.Color.green()
        )
        embed.set_footer(text="© 2025 LTXX — All Rights Reserved.")
        
       
        await interaction.response.send_message(embed=embed)

    except discord.Forbidden:
       
        embed = discord.Embed(
            title="❌ Permission Denied",
            description="I don't have permission to assign roles!",
            color=discord.Color.red()
        )
        embed.set_footer(text="© 2025 LTXX — All Rights Reserved.")
        await interaction.response.send_message(embed=embed, ephemeral=True)
    except discord.HTTPException as e:
       
        embed = discord.Embed(
            title="❌ Error",
            description=f"An error occurred: {e}",
            color=discord.Color.red()
        )
        embed.set_footer(text="© 2025 LTXX — All Rights Reserved.")
        await interaction.response.send_message(embed=embed, ephemeral=True)


VALID_COLORS = {
    "green": discord.Color.green(),
    "blue": discord.Color.blue(),
    "red": discord.Color.red(),
    "orange": discord.Color.orange(),
}


@bot.tree.command(name="create-embed", description="Create a custom embed with multiple fields and options.")
@app_commands.describe(
    title="The title of the embed",
    description="The description of the embed (use \\n for new lines)",
)
@app_commands.choices(
    color=[
        app_commands.Choice(name="Green", value="green"),
        app_commands.Choice(name="Blue", value="blue"),
        app_commands.Choice(name="Red", value="red"),
        app_commands.Choice(name="Orange", value="orange"),
    ]
)
async def create_embed(
    interaction: discord.Interaction,
    title: str,
    description: str,
    color: str,
    thumbnail: discord.Attachment = None,
    img: discord.Attachment = None
):
    
    if str(interaction.user.id) not in CREATE_EMBED_ALLOWED_USERS:
        await interaction.response.send_message("❌ You do not have permission to use this command.", ephemeral=True)
        return

    
    if color.lower() not in VALID_COLORS:
        await interaction.response.send_message("❌ Invalid color! Please choose from green, blue, red, or orange.", ephemeral=True)
        return

    embed_color = VALID_COLORS[color.lower()]

    
    description = description.replace("\\n", "\n")

   
    embed = discord.Embed(title=title, description=description, color=embed_color)

   
    if thumbnail:
        embed.set_thumbnail(url=thumbnail.url)

   
    if img:
        embed.set_image(url=img.url)

    
    embed.set_footer(text="© 2025 LTXX — All Rights Reserved.")

   
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="clear", description="Clear a specified number of messages.")
@app_commands.describe(amount="The number of messages to delete.")
async def clear(interaction: discord.Interaction, amount: int):
    
    if not interaction.user.guild_permissions.manage_messages:
        await interaction.response.send_message("❌ You do not have permission to manage messages.", ephemeral=True)
        return

    
    if amount < 1 or amount > 100:
        await interaction.response.send_message("❌ Please enter a number between 1 and 100.", ephemeral=True)
        return

   
    await interaction.channel.purge(limit=amount)

   
    embed = discord.Embed(
        title="✅ Successfully deleted messages",
        description=f"Successfully deleted {amount} messages.",
        color=discord.Color.green()
    )
    embed.set_footer(text="© 2025 LTXX — All Rights Reserved.")

   
    await interaction.response.send_message(embed=embed, ephemeral=True)


bot.run(TOKEN)
