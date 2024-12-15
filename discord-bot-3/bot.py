# pylint: disable=C0301,C0114,W0718,W1514,W0106

import asyncio
import logging
import os
from random import choice, randint
from typing import Final
from discord import Activity, ActivityType, Client, File, Intents, Interaction, Message, Object
from discord.ext import commands
from dotenv import load_dotenv

from bedrock import BedrockCursor, LLMmodel


load_dotenv()

GUILD_ID: Final[Object] = Object(id=os.getenv("DISCORD_ID"))
INTENTS: Final[Intents] = Intents.default()
INTENTS.message_content = True # NOQA
RESP_FILE: Final[str] = "response.md"
VERSION: Final[str] = "0.0.1"

client: Final[Client] = commands.Bot(command_prefix="/", intents=INTENTS) # pylint: disable=C0103


async def send_hello(message: Message, user_message: str) -> None:
    """
    Send a greeting message if a message contains 'hello'
    :param message:
    :param user_message:
    :return:
    """
    greetings: Final[list[str]] = [
        "Hello",
        "Hey",
        "Hi",
        "Hola",
        "How's it going",
        "Howdy",
        "Kumusta",
        "Sup",
        "What's up",
    ]

    if not user_message:
        logging.info("Message was empty")
        return

    if is_private := user_message[0] == "?":
        user_message = user_message[1:]

    try:
        if "hello" in user_message.lower():
            hello_msg = f"{choice(greetings)} {message.author.name.title()}!"
            await message.author.send(hello_msg) if is_private else await message.channel.send(hello_msg)
    except Exception as e:
        logging.error(e)


@client.event
async def on_ready() -> None:
    """
    Bot/client setup. On startup these settings are configured
    :return:
    """
    logging.info("%s is now online!", client.user)

    try:
        synced = await client.tree.sync(guild=GUILD_ID) # syncs slash commands with server
        logging.info("synced %d commands to guild %s", len(synced), GUILD_ID.id)
        await client.change_presence(activity=Activity(type=ActivityType.watching, name="you..."))
    except Exception as e:
        logging.error(e)


@client.event
async def on_message(message: Message) -> None:
    """
    monitors messages being sent on a server
    :param message:
    :return:
    """
    if message.author == client.user: # prevents infinite loop
        return

    logging.info("[%s] %s: %s", str(message.channel), str(message.author), message.content)

    if "hello" in message.content.lower():
        await send_hello(message, message.content)


@client.tree.command(name="roll", description="Roll a dice, default sides: 6", guild=GUILD_ID)
async def roll_dice(interaction: Interaction, sides: int = 6) -> None:
    """
    Roll a dice, default sides: 6
    :param interaction:
    :param sides:
    :return:
    """
    if sides < 1:
        await interaction.response.send_message("please set sides to 1 or greater")
        return

    await interaction.response.send_message(f"rolled {randint(1, sides)}")


@client.tree.command(name="ask", description="Ask a question to an LLM, default is titan", guild=GUILD_ID)
async def ask_question(
        interaction: Interaction,
        question: str,
        model: str = "titan"
    ) -> None:
    """
    Ask a question to an LLM, default is titan
    :param model:
    :param interaction:
    :param question:
    :return:
    """
    match model:
        case "claude":
            llm_id: str = LLMmodel.CLAUDE_3_5_SONNET.id
        case "claude2":
            llm_id: str = LLMmodel.CLAUDE_3_5_SONNET_V2.id
        case "llama":
            llm_id: str = LLMmodel.LLAMA_3_2_90B_INSTRUCT_V1.id
        case "titan":
            llm_id: str = LLMmodel.TITAN_TEXT_LITE.id
        case "titang1":
            llm_id: str = LLMmodel.TITAN_TEXT_G1_EXPRESS.id

    bedrock_cursor: BedrockCursor = BedrockCursor(llm_id)

    logging.info(
        "[%s] [cmd: %s | model: %s] %s: %s",
        str(interaction.channel),
        interaction.data["name"],
        model,
        str(interaction.user.name),
        question
    )

    try:
        # Defer the interaction if processing might take time
        # this is necessary because retrieving a response from bedrock/llm may take some time
        await interaction.response.defer()

        response: str = await asyncio.to_thread(bedrock_cursor.get_message, question)
        logging.info("llm response: %s", response)

        # if response is greater than 2000 characters
        # send response as a text file
        if len(response) > 2000:
            try:
                with open(RESP_FILE, "w+", encoding="utf-8") as file:
                    file.write(response)

                # Respond after deferring with followup
                await interaction.followup.send(file=File(RESP_FILE))
            finally:
                os.remove(RESP_FILE)  # delete file when complete
        else:
            await interaction.followup.send(response)
    except Exception as e:
        logging.error(e)
        await interaction.followup.send(e)


@client.tree.command(name="models", description="shows available llm models that can be passed into /ask", guild=GUILD_ID)
async def show_models(interaction: Interaction) -> None:
    """
    Shows available llm models
    :param interaction:
    :return:
    """
    models = """
        claude  = Claude 3.5 Sonnet
        claude2 = Claude 3.5 Sonnet v2
        llama   = Llama 3.2 90b instruct v1
        titan   = Titan Text G1 - Lite
        titang1 = Titan Text G1 - Express
    """
    await interaction.response.send_message(f"available llm models that can be passed into /ask: {models}")

@client.tree.command(name="version", description="shows version of bot", guild=GUILD_ID)
async def show_version(interaction: Interaction) -> None:
    """
    Shows version of bot
    :param interaction:
    :return:
    """
    await interaction.response.send_message(f"discord-bot-3 version: {VERSION}")
