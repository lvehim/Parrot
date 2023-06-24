from __future__ import annotations

import os
from io import BytesIO
from typing import Callable, List, Optional, Tuple
from urllib.parse import urlencode

import arrow  # type: ignore
from discord.ext.commands import BucketType, check, group  # type: ignore

import discord
from core import Cog, Context, Parrot
from discord import Embed
from discord.ext import commands
from utilities.paginator import PaginationView

APPID = os.environ["WOLFRAM_APP"]
DEFAULT_OUTPUT_FORMAT = "JSON"
QUERY = "http://api.wolframalpha.com/v2/{request}"
WOLF_IMAGE = "https://www.symbols.com/gi.php?type=1&id=2886&i=1"

MAX_PODS = 20
STAFF_ROLES = {
    771025632184369152,
}  # I am poor
# The role is of Server Moderator of the support server

# Allows for 10 wolfram calls pr user pr day
usercd = commands.CooldownMapping.from_cooldown(10, 60 * 60 * 24, BucketType.user)

# Allows for max api requests / days in month per day for the entire guild (Temporary)
guildcd = commands.CooldownMapping.from_cooldown(67, 60 * 60 * 24, BucketType.guild)


async def send_embed(
    ctx: Context,
    message_txt: str,
    colour: int = 0x0279FD,
    footer: str = None,
    img_url: str = None,
    f: discord.File = None,
) -> None:
    """Generate & send a response embed with Wolfram as the author."""
    embed = Embed(colour=colour)
    embed.description = f"{message_txt}"  # well, fuck you pycord
    embed.set_author(name="Wolfram Alpha", icon_url=WOLF_IMAGE, url="https://www.wolframalpha.com/")
    if footer:
        embed.set_footer(text=footer)

    if img_url:
        embed.set_image(url=img_url)

    await ctx.send(embed=embed, file=f)


def custom_cooldown(*ignore: int) -> Callable:
    """
    Implement per-user and per-guild cooldowns for requests to the Wolfram API.
    A list of roles may be provided to ignore the per-user cooldown.
    """

    async def predicate(ctx: Context) -> bool:
        if ctx.invoked_with == "help":
            # if the invoked command is help we don't want to increase the ratelimits since it's not actually
            # invoking the command/making a request, so instead just check if the user/guild are on cooldown.
            guild_cooldown = guildcd.get_bucket(ctx.message).get_tokens() != 0
            # check the message is in a guild, and check user bucket if user is not ignored
            if ctx.guild and all(r.id not in ignore for r in ctx.author.roles):
                return guild_cooldown and usercd.get_bucket(ctx.message).get_tokens() != 0
            return guild_cooldown

        user_bucket = usercd.get_bucket(ctx.message)

        if all(role.id not in ignore for role in ctx.author.roles):
            user_rate = user_bucket.update_rate_limit()

            if user_rate:
                # Can't use api; cause: member limit
                cooldown = arrow.utcnow().shift(seconds=int(user_rate)).humanize(only_distance=True)
                message = "You've used up your limit for Wolfram|Alpha requests.\n" f"Cooldown: {cooldown}"
                await send_embed(ctx, message)
                return False

        guild_bucket = guildcd.get_bucket(ctx.message)
        guild_rate = guild_bucket.update_rate_limit()

        # Repr has a token attribute to read requests left

        if guild_rate:
            # Can't use api; cause: guild limit
            message = "The max limit of requests for the server has been reached for today.\n" f"Cooldown: {int(guild_rate)}"
            await send_embed(ctx, message)
            return False

        return True

    return check(predicate)


async def get_pod_pages(ctx: Context, bot: Parrot, query: str) -> Optional[List[Tuple[str, str]]]:
    """Get the Wolfram API pod pages for the provided query."""
    async with ctx.typing():
        params = {
            "input": query,
            "appid": APPID,
            "output": DEFAULT_OUTPUT_FORMAT,
            "format": "image,plaintext",
            "location": "the moon",
            "latlong": "0.0,0.0",
            "ip": "1.1.1.1",
        }
        request_url = QUERY.format(request="query")

        async with bot.http_session.get(url=request_url, params=params) as response:
            json = await response.json(content_type="text/plain")

        result = json["queryresult"]
        _ = f"{request_url}?{urlencode(params)}"
        if result.get("error"):
            # API key not set up correctly
            if result["error"]["msg"] == "Invalid appid":
                message = "Wolfram API key is invalid or missing."
                await send_embed(ctx, message)
                return None

            message = "Something went wrong internally with your request, please notify staff!"
            await send_embed(ctx, message)
            return None

        if not result["success"]:
            message = f"I couldn't find anything for {query}."
            await send_embed(ctx, message)
            return None

        if not result["numpods"]:
            message = "Could not find any results."
            await send_embed(ctx, message)
            return None

        pods = result["pods"]
        pages = []
        for pod in pods[:MAX_PODS]:
            subs = pod.get("subpods")

            for sub in subs:
                title = sub.get("title") or sub.get("plaintext") or sub.get("id", "")
                img = sub["img"]["src"]
                pages.append((title, img))
        return pages


class Wolfram(Cog):  # type: ignore
    """Commands for interacting with the Wolfram|Alpha API."""

    def __init__(self, bot: Parrot) -> None:
        self.bot = bot
        self.ON_TESTING = False

    @property
    def display_emoji(self) -> discord.PartialEmoji:
        return discord.PartialEmoji(name="\N{RIBBON}")

    @group(name="wolfram", aliases=("wolf", "wa"), invoke_without_command=True)
    @custom_cooldown(*STAFF_ROLES)
    async def wolfram_command(self, ctx: Context, *, query: str) -> None:
        """Requests all answers on a single image, sends an image of all related pods."""
        params = {
            "i": query,
            "appid": APPID,
            "location": "the moon",
            "latlong": "0.0,0.0",
            "ip": "1.1.1.1",
        }
        request_url = QUERY.format(request="simple")

        # Give feedback that the bot is working.
        async with ctx.typing():
            async with self.bot.http_session.get(url=request_url, params=params) as response:
                status = response.status
                image_bytes = await response.read()

            f = discord.File(BytesIO(image_bytes), filename="image.png")
            image_url = "attachment://image.png"

            if status == 501:
                message = "Failed to get response."
                footer = ""
            elif status == 400:
                message = "No input found."
                footer = ""
            elif status == 403:
                message = "Wolfram API key is invalid or missing."
                footer = ""
            else:
                message = ""
                footer = "View original for a bigger picture."
            color = 0x0279FD
            # Sends a "blank" embed if no request is received, unsure how to fix
            await send_embed(ctx, message, color, footer=footer, img_url=image_url, f=f)

    @wolfram_command.command(name="page", aliases=("pa", "p"))
    @custom_cooldown(*STAFF_ROLES)
    async def wolfram_page_command(self, ctx: Context, *, query: str) -> None:
        """
        Requests a drawn image of given query.
        Keywords worth noting are, "like curve", "curve", "graph", "pokemon", etc.
        """
        pages = await get_pod_pages(ctx, self.bot, query)

        if not pages:
            return
        em_list = []
        for page in pages:
            embed = Embed(title=page[0])
            embed.set_author(
                name="Wolfram Alpha",
                icon_url=WOLF_IMAGE,
                url="https://www.wolframalpha.com/",
            )
            embed.set_image(url=page[1])
            em_list.append(embed)

        await PaginationView(em_list).start(ctx=ctx)

    @wolfram_command.command(name="cut", aliases=("c",))
    @custom_cooldown(*STAFF_ROLES)
    async def wolfram_cut_command(self, ctx: Context, *, query: str) -> None:
        """
        Requests a drawn image of given query.
        Keywords worth noting are, "like curve", "curve", "graph", "pokemon", etc.
        """
        pages = await get_pod_pages(ctx, self.bot, query)

        if not pages:
            return

        page = pages[1] if len(pages) >= 2 else pages[0]
        await send_embed(ctx, page[0], colour=0x0279FD, img_url=page[1])

    @wolfram_command.command(name="short", aliases=("sh", "s"))
    @custom_cooldown(*STAFF_ROLES)
    async def wolfram_short_command(self, ctx: Context, *, query: str) -> None:
        """Requests an answer to a simple question."""
        params = {
            "i": query,
            "appid": APPID,
            "location": "the moon",
            "latlong": "0.0,0.0",
            "ip": "1.1.1.1",
        }
        request_url = QUERY.format(request="result")

        # Give feedback that the bot is working.
        async with ctx.typing():
            async with self.bot.http_session.get(url=request_url, params=params) as response:
                status = response.status
                response_text = await response.text()

            if status == 501:
                message = "Failed to get response."
            elif status == 400:
                message = "No input found."
            elif response_text == "Error 1: Invalid appid.":
                message = "Wolfram API key is invalid or missing."
            else:
                message = response_text
            color = 0x0279FD
            await send_embed(ctx, message, color)
