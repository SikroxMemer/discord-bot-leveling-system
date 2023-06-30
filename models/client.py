from discord import app_commands
from datetime import datetime
from discord import Embed
from discord import Client
from discord import Object
from discord import Intents


import json

guild_id = Object(id=1120025228232359976)


class client(Client):
    intents = Intents.default()
    intents.message_content = True

    def __init__(self, *, intents=intents, **options) -> None:
        super().__init__(intents=intents, **options)

    async def on_message(self, message):
        user_id = str(message.author.id)
        with open("data/users.json", "r") as data:
            users = json.load(data)
            exists = any(user['user']['id'] == user_id for user in users)
            if not exists:
                new_object = {"user": {"id": user_id,
                                       "level": 0, "exp": 0, "credit": 0}}
                users.append(new_object)
            else:
                for user in users:
                    if user['user']['id'] == user_id:
                        if user['user']['exp'] == 10:
                            user['user']['level'] += 1
                            user['user']['exp'] = 0
                        else:
                            user['user']['exp'] += 0.5
                            user['user']['credit'] += 100
                        break

            with open("data/users.json", "w") as f:
                json.dump(users, f, indent=2)


client = client()
Tree = app_commands.CommandTree(client=client)


@Tree.command(name="info", description="show user's info", guild=guild_id)
async def info(interaction):
    user = str(interaction.user.id)
    with open("data/users.json", "r") as user_info:
        file = json.load(user_info)
        for users in file:
            if users['user']['id'] == user:

                embed = Embed(
                    title=f"__Avatar Link__\n{interaction.user.display_avatar.url}", color=0x7600ec, description="")
                embed.set_author(
                    name=interaction.user.name,
                    icon_url=interaction.user.display_avatar.url
                )
                embed.add_field(
                    name="**Level:**", value=f"```yaml\n{users['user']['level']}\n```", inline=True)
                embed.add_field(
                    name="**Xp:**", value=f"```yaml\n{users['user']['exp']}\n```", inline=True)
                embed.add_field(
                    name="**Credit:**", value=f"```yaml\n{users['user']['credit']}\n```", inline=True)
                embed.set_image(
                    url="https://media.giphy.com/media/3oEjHECc1GftirnHZm/giphy.gif")
                embed.set_footer(
                    text=f"Command Timeline : {datetime.now().date()}")

                await interaction.response.send_message(embed=embed)

@client.event
async def on_ready():
    await Tree.sync(guild=guild_id)
    print("Commands Synced !")


def run(token):
    client.run(token=token)