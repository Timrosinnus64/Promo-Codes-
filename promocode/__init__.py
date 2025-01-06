from typing import TYPE_CHECKING

from ballsdex.packages.promocode.cog import Promocode

if TYPE_CHECKING:
    from ballsdex.core.bot import BallsDexBot

async def setup(bot: "BallsDexBot"):
    await bot.add_cog(Promocode(bot))
