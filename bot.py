import discord
from discord.ext import commands
import random
import os
import openai
from dotenv import load_dotenv

load_dotenv()
D_TOKEN = os.getenv('DISCORD_CLIENT_TOKEN')
O_TOKEN = os.getenv('OPEN_AI_API_KEY')

client = openai.OpenAI(api_key=O_TOKEN)

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)


def massage_text(text):
    replacements = {
        ',': '',
        'frick': 'fuck',
        'friggin': 'fuckin',
        'frig': 'fuck',
        'goofball': 'dumbass',
        'goofballs': 'dumbasses',
        'little turd': 'shit head',
        'Frick': 'Fuck',
        'Friggin': 'Fuckin',
        'Frig': 'Fuck',
        'Goofball': 'Dumbass',
        'Goofballs': 'Dumbasses',
        'little turd': 'shit head'
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text

def describe_image(image, voice):
    response = client.chat.completions.create(
        model="gpt-4-vision-preview",
        max_tokens=100,
        messages=[
            {
                "role": "system",
                "content": voice['system'],
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": voice['user'],
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": image,
                        },
                    },
                ],
            },
        ]
    )
    print("Chat Completion")
    print(response.choices[0])

    return response.choices[0].message.content

prompts = {
    'deadpool': {
        'name': 'Deadpool',
        'id': '5pOjOeJ82iGHKnqIMFHV',
        'system': 'You are Deadpool from the marvel universe. You poke fun at the person in this photo. Make it short.',
        'user': 'Describe this photo of a person. Go into detail about 3 features and exaggerate. Be snarky and funny. Use "goof ball", "Frickin", "little turd" and "Frig off" a lot."',
    },
}

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.command(name='roast', help='Torchin\' your a$$ mfer 😈😈😈')
async def roast(ctx):
    attachment=ctx.message.attachments[0]
    image_url = str(attachment.url)
    voice_prompt = prompts['deadpool']
    description = describe_image(image_url, voice_prompt)
    print('Description\n')
    print(str(description))
    if not description:
        raise Exception('No description')

    massaged_text = massage_text(description)
    await ctx.send(massaged_text, tts=True)

bot.run(D_TOKEN)