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
    "PROMOCODENAMEHERE":{"country": "COLLECTIBLENAMEHERE", 
                         "expires": datetime(Y, M, D),
                         "special": "SPECIALNAMEHERE",
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
        Redeem a promo code to claim the collectible
        """
        await interaction.response.defer(ephemeral=True, thinking=True)

        code_data = promo_codes.get(code.upper())
        if not code_data:
            await interaction.followup.send(
                "Invalid Promo Code. Please check if it's valid and try again.", ephemeral=True
            )
            return

        if datetime.now() > code_data["expires"]:
            await interaction.followup.send(
                "This promo code has expired.", ephemeral=True
            )
            return

        country = code_data["country"]
        try:
            promo_ball = next(ball for ball in balls.values() if ball.country.lower() == country.lower())
        except StopIteration:
            await interaction.followup.send(
                "The promo code is valid, but the collectible is unavailable at the moment.", ephemeral=True
            )
            return

        user_redeemed = redeemed_users.get(interaction.user.id, [])
        if code.upper() in user_redeemed:
            await interaction.followup.send(
                "You have already redeemed this promo code.", ephemeral=True
            )
            return

        player, _ = await Player.get_or_create(discord_id=interaction.user.id)

        special_name = code_data.get("special")  # This could be any name, e.g., "GoldenBall", "MysticBall", etc.

        special_instance = None
        if special_name:
            special_instance = next((x for x in specials.values() if x.name == special_name), None)

            if not special_instance:
                await interaction.followup.send(
                    f"Promo code is special, but no Special found with the name '{special_name}'. Please contact support.",
                    ephemeral=True,
                )
                return

        promo_ball_instance = await BallInstance.create(
            ball=promo_ball,
            player=player,
            server_id=interaction.guild_id,
            attack_health=random.randint(-20, 20),
            bonus_health=random.randint(-20, 20),
            special=special_instance  # Pass the Special instance or None
        )

        if interaction.user.id not in redeemed_users:
            redeemed_users[interaction.user.id] = []
        redeemed_users[interaction.user.id].append(code.upper())

        await interaction.followup.send(
            f"Promo Code redeemed. {promo_ball.country} now awaits in your inventory.",
            ephemeral=True,
        )

    @app_commands.command()
    @app_commands.checks.has_any_role(*settings.root_role_ids, *settings.admin_role_ids)
    async def list(self, interaction: discord.Interaction):
        """
        List all promo codes
        """
        await interaction.response.defer(ephemeral=True, thinking=True)

        active_codes = []
        expired_codes = []

        now = datetime.now()

        for code, data in promo_codes.items():
            expiration = data["expires"]
            status = f"**{code}** -> {data['country']} (Expires: {expiration.strftime('%Y-%m-%d')})"

            if now <= expiration:
                active_codes.append(status) 
            else:
                expired_codes.append(status)
            
        active_text = "\n".join(active_codes) if active_codes else "No active promo codes"
        expired_text = "\n".join(expired_codes) if expired_codes else "No expired promo codes"

        embed = discord.Embed(title="Promo Code List", color=discord.Colour.from_rgb(168, 199, 247))
        embed.add_field(name="✅ Active Promo Codes", value=active_text, inline=False)
        embed.add_field(name="❌ Expired Promo Codes", value=expired_text, inline=False)

        await interaction.followup.send(embed=embed, ephemeral=True)
