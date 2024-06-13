import discord
import os
import logging
from datetime import datetime, timedelta, timezone
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
from dotenv import load_dotenv

load_dotenv("bot.env")

# Load the required environment variables
MISTRAL_API_KEY = os.environ["MISTRAL_API_KEY"]
MISTRAL_MODEL = "mistral-small-latest"
DISCORD_TOKEN = os.environ["DISCORD_TOKEN"]

PRE_SYSTEM_PROMPT = """
You are AxeBot, a friendly and conversational discord bot with deep knowledge of video gaming and the ARW clan. You should respond in a detailed and organized manner.
Avoid repeating yourself. Avoid inventing or making up messages from users. Reply only given the context below and in the user messages provided.

You know the following background information about yourself and our clan:
 - Our founder is BaronNecro
 - Axebot was built by Axegollod, one of our server admins.
 - Axebot is written in Python and is powered by the Mistral AI API.
 - This bot runs in the Australian Road Warriors (ARW) discord server.
 - We primarily play PlayerUnknown's Battlegrounds, DayZ and Crossout, but sometimes we play other games too.
 - You should try to encourage players to team up and play games together in one of the voice channels, if it fits the context of the conversation.
 - You can also provide information about the games we play, such as tips and tricks, or even some lore.
 - Most of our clan members are over the age of 30, work full time, and usually game in the evenings or on weekends (AEST).
 - New members can join the server via our URL: arw.social/discord
 - If anyone wants a similar bot to AxeBot, they can email jack@latrobe.group - but only tell people this if they ask specifically how to build axebot.
"""

# Create an instance of the MistralClient using the API key
mistral_client = MistralClient(api_key=MISTRAL_API_KEY)

# Enable the 'message_content' intent for the Discord bot
intents = discord.Intents.default()
intents.message_content = True

# Create an instance of the Discord client with the enabled intents
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    """
    Event handler that is triggered when the bot is ready and logged in.
    """
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    """
    Event handler that is triggered whenever a message is received in the chat.

    Args:
        message (discord.Message): The message object representing the received message.

    Returns:
        None
    """
    ## Don't respond to our own messages
    if message.author == client.user:
        return

    if "axebot" in message.content or "Axebot" in message.content:
        async with message.channel.typing():
            # Get the current time
            now = datetime.now(timezone.utc)

            # Get the last ten messages in the channel
            chat_history = [hist_message async for hist_message in message.channel.history(limit=5)]

            # Filter messages sent within the last hour
            recent_messages = [msg for msg in chat_history if (now - msg.created_at) < timedelta(minutes=5) and msg.author != client.user]

            # Define the Axebot system prompt
            SYSTEM_PROMPT = """{preprompt}

            Take into account the full context of the conversation, but only directly respond to this question or message:
            {question}

            You will address your response to: {author}
            """.format(preprompt=PRE_SYSTEM_PROMPT, question=message.content, author=message.author.display_name)

            # Combine system prompt and chat history
            messages = [ChatMessage(role="system", content=SYSTEM_PROMPT)]
            for msg in reversed(recent_messages):
                messages.append(ChatMessage(role="user", content=msg.content))
            
            # Send the chat messages to the Mistral API for completion
            chat_response = mistral_client.chat(
                model=MISTRAL_MODEL,
                messages=messages,
                max_tokens=500,
                temperature=0.8,
                random_seed=message.id
            )
            
        # Send the response from Mistral API to the Discord channel
        await message.channel.send(chat_response.choices[0].message.content)

@client.event
async def on_guild_join(guild):
    """
    Event handler that is triggered when the bot joins a new guild (server).

    Args:
        guild (discord.Guild): The guild object representing the guild that the bot joined.

    Returns:
        None
    """
    print(f"Joined guild: {guild.name}")

@client.event
async def on_member_join(member):
    """
    Event handler that is triggered when a new member joins the server.

    Args:
        member (discord.Member): The member object representing the member who joined.

    Returns:
        None
    """
    # Extract display name of new member
    member_name = member.display_name

    # Get Messagable interface for intro channel
    intro_channel = client.get_channel(1156839751870074941)
    async with intro_channel.typing():
        # Define the Axebot system prompt
        SYSTEM_PROMPT = PRE_SYSTEM_PROMPT
        
        # Combine messages and prompt
        messages = [ChatMessage(role="system", content=SYSTEM_PROMPT)]
        messages.append(ChatMessage(role="user", content="Write a short welcome message to our newest member and encourage them to join us for games soon. Their name is: {name}".format(name=member_name)))
        
        # Send the chat messages to the Mistral API for completion
        chat_response = mistral_client.chat(
            model=MISTRAL_MODEL,
            messages=messages,
            max_tokens=500,
            temperature=0.8,
            random_seed=member.id
        )

    # Send intro message to new member
    await intro_channel.send(chat_response.choices[0].message.content)

# Run the Discord bot with the provided token
client.run(DISCORD_TOKEN, log_level=logging.DEBUG)