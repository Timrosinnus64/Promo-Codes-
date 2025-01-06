import discord
from discord import app_commands
from discord.ext import commands
import random
from datetime import datetime
from ballsdex.core.models import BallInstance, Player, balls
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ballsdex.core.bot import BallsDexBot

promo_codes = {
    "PROMOCODENAME":{"country": "COLLECTIBLENAMEHERE", 
             "expires": datetime(Y, M, D),
             }
}
redeemed_users = {}

class Promocode(commands.GroupCog, group_name="promocode"):
    """
    Promo Code command
    """
    def __init__(self, bot: "BallsDexBot"):
        self.bot = bot

    @app_commands.command()
    async def redeem(self, interaction: discord.Interaction, code: str):
        """
        Redeeem a promo code to claim the collectible
        """
        await interaction.response.defer(ephemeral=True, thinking=True)

        code_data = promo_codes.get(code.upper())
        if not code_data:
            await interaction.followup.send(
                "Invalid Promo Code. Please check if its valid and try again", ephemeral=True
            )
            return
    
        if datetime.now() > code_data["expires"]:
            await interaction.followup.send(
                "This promo code has expired", ephemeral=True
            )
            return
    
        country = code_data["country"]
        try:
            promo_ball = next(ball for ball in balls.values() if ball.country.lower() == country.lower())

        except StopIteration:
            await interaction.followup.send(
                "The promo code is valid, but the collectible is unavailable at the moment", ephemeral=True
            )
            return
    
        user_redeemed = redeemed_users.get(interaction.user.id, [])
        if code.upper() in user_redeemed:
            await interaction.followup.send(
                "You have Arleady redeemed it", ephemeral=True
            )
            return
    
        player, _ = await Player.get_or_create(discord_id=interaction.user.id)

        await BallInstance.create(
            ball=promo_ball, player=player, server_id=interaction.guild_id
        )

        if interaction.user.id not in redeemed_users:
            redeemed_users[interaction.user.id] = []
        redeemed_users[interaction.user.id].append(code.upper())

        await interaction.followup.send(
            f"Code Succesfully redeemed. {promo_ball.country} now awaits in your inventory.",
            ephemeral=True,
        )
