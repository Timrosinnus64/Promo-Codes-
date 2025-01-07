import discord
from discord import app_commands
from discord.ext import commands
from ballsdex.settings import settings
import random
from ballsdex.core.models import BallInstance, Player
from ballsdex.core.utils.transformers import BallEnabledTransform

promo_codes = [] # <- List of promo codes << DO NOT CHANGE THIS LINE >>
claimed = [] # <- List of claimed promo codes << DO NOT CHANGE THIS LINE >>

def is_owner():
    async def predicate(interaction: discord.Interaction) -> bool:
        return interaction.user.id == interaction.client.application.owner.id # <- Checks if youre the bot owner, change "interaction.client.application.owner.id" to your Discord ID if youre using a alt account.
    return app_commands.check(predicate)

class Promocode(commands.GroupCog, group_name="promos"):
    """
    Promo Code command
    """
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.promo_codes = promo_codes
        self.claimed = claimed

    # <> Creates a promo code for a ball
    @app_commands.command()
    @app_commands.describe(ball="Select a ball to create a promo code for")
    @is_owner()
    async def create(self, interaction: discord.Interaction, ball: BallEnabledTransform):
        """Create a promo code for a ball"""
        code = 'PROMO-' + ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=8)) # <- Generates a random code, with 8 letters and numbers
        self.promo_codes.append({"code": code, "ball": ball})
        await interaction.response.send_message(f"Promo code `{code}` created for {ball.country}.", ephemeral=True)

    # <> Claims a ball using a promo code
    @app_commands.command()
    async def claim(self, interaction: discord.Interaction, code: str):
        """Claim a ball using a promo code"""
        await interaction.response.defer()
        for promo in self.promo_codes:
            if promo["code"] == code:
                if code in self.claimed:
                    await interaction.followup.send("This promo code has already been claimed.", ephemeral=False) # <- Checks if the code has already been claimed
                    return
                player, _ = await Player.get_or_create(discord_id=interaction.user.id)
                ball_instance = await BallInstance.create(
                    ball=promo["ball"],
                    player=player,
                    attack_bonus=random.randint(-settings.max_attack_bonus, settings.max_attack_bonus),
                    health_bonus=random.randint(-settings.max_health_bonus, settings.max_health_bonus),
                ) # <- Creates a ball instance with random attack and health bonuses
                self.claimed.append(code)
                await interaction.followup.send(f"You have claimed {ball_instance.ball.country}!")
                return
        await interaction.followup.send("Invalid promo code.", ephemeral=False)

    # <> Lists all available promo codes
    @app_commands.command()
    @is_owner()
    async def list(self, interaction: discord.Interaction):
        """List all available promo codes"""
        await interaction.response.defer(ephemeral=True)
        if not self.promo_codes:
            await interaction.followup.send("No promo codes available.")
            return
        codes = "\n".join([promo["code"] for promo in self.promo_codes if promo["code"] not in self.claimed])
        await interaction.followup.send(f"Available promo codes:\n{codes}", ephemeral=True)

    # <> Deletes a promo code
    @app_commands.command()
    @app_commands.describe(code="Select a promo code to delete")
    @is_owner()
    async def delete(self, interaction: discord.Interaction, code: str):
        """Delete a promo code"""
        await interaction.response.defer(ephemeral=True)
        for promo in self.promo_codes:
            if promo["code"] == code:
                self.promo_codes.remove(promo)
                await interaction.followup.send(f"Promo code `{code}` deleted.")
                return
        await interaction.followup.send("Promo code not found.", ephemeral=True)
