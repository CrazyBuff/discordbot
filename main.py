import json
import random

import discord
import requests
from pycoingecko import CoinGeckoAPI

TOKEN = 'ODUwMDA5NDg0MDk2NDM4MzQy.GZPJp1.Zbkbot-WxyYnIN92wrUigGASjFfjtKT8K8b9oQ'

client = discord.Client()

cg = CoinGeckoAPI()

USER_WATCHLIST = {}


def get_crypto(coin_id: str):
    return cg.get_coins_markets(ids=coin_id, vs_currency='aud')


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    username = str(message.author).split('#')[0]
    user_message = str(message.content)
    channel = str(message.channel.name)
    print(f'{username}: {user_message} ({channel})')

    if message.author == client.user:
        return

    args = message.content.split(" ")

    if args[0] == "!nft":
        url = "https://testnets-api.opensea.io/api/v1/asset/0x381748c76f2b8871afbbe4578781cd24df34ae0d/0/"

        response = requests.get(url)

        print(response.text)
        response = response.json()
        embed = discord.Embed(
                            title=response["name"],
                            url=response["external_link"],
                            description=response["description"],
                            color=0xFF5733
        )
        embed.set_thumbnail(url=response["image_url"])
        embed.add_field(name="ETH price:", value=response["collection"]["payment_tokens"]["eth_price"], inline=True)
        embed.add_field(name="USD price:", value=response["collection"]["payment_tokens"]["usd_price"], inline=True)
        await message.channel.send(embed=embed)
    elif args[0] == "!crypto":
        if args[1]:
            crypto_data = get_crypto(args[1].lower())
            if len(crypto_data):
                crypto_data = crypto_data[0]
                embed = discord.Embed(
                    title=crypto_data["name"],
                    color=0xFF5733
                )
                embed.set_thumbnail(url=crypto_data["image"])
                embed.add_field(name="Market cap rank:", value=str(crypto_data["market_cap_rank"]),inline=False)
                embed.add_field(name="Current price:", value="$" + str(crypto_data["current_price"]), inline=False)
                embed.add_field(name="Price change (24h):", value=str(crypto_data["price_change_percentage_24h"]) + "%", inline=False)
            else:
                embed = discord.Embed(
                    title=args[1] + " is not a valid option!",
                )
                embed.set_thumbnail(url="https://i.pinimg.com/originals/d5/20/b2/d520b2a1aee3d944fc2c5bbfb1737ed5.jpg")

            await message.channel.send(embed=embed)
    elif args[0] == "!cryptowatchlist":
        if args[1] and args[1] == "add":
            if args[2]:
                crypto_data = get_crypto(args[2].lower())
                if len(crypto_data):
                    if message.author not in USER_WATCHLIST:
                        USER_WATCHLIST[message.author] = []
                    elif len(USER_WATCHLIST[message.author]) == 5:
                        await message.channel.send("You've reached the limit for your watchlist @" + username)
                        return
                    elif args[2].lower() in USER_WATCHLIST[message.author]:
                        await message.channel.send("You've already added this to your watchlist @" + username)
                        return
                    USER_WATCHLIST[message.author].append(args[2].lower())
                    await message.channel.send(crypto_data[0]["name"] + " added to your watchlist @" + username)

        elif args[1] and args[1] == "view":
            if message.author in USER_WATCHLIST:
                embed = discord.Embed(
                    title=username + "'s Crypto Watchlist :money_mouth:",
                    color=0xFF5733
                )
                watchlist = USER_WATCHLIST[message.author]
                for coin in watchlist:
                    crypto_data = get_crypto(coin)[0]
                    embed.add_field(name=crypto_data["name"], value="Price: $" + str(crypto_data["current_price"]) + "\nPrice change (24h): " + str(crypto_data["price_change_percentage_24h"]) + "%", inline=False)

                await message.channel.send(embed=embed)
            else:
                await message.channel.send("You don't have a watchlist @" + username + "!")

        elif args[1] and args[1] == "remove":
            if message.author in USER_WATCHLIST:
                if args[2] and args[2].lower() in USER_WATCHLIST[message.author]:
                    USER_WATCHLIST[message.author].remove(args[2].lower())
                    if not len(USER_WATCHLIST[message.author]):
                        del USER_WATCHLIST[message.author]

                    await message.channel.send(args[2] + " was removed from your watchlist @" + username)
                    return
                else:
                    await message.channel.send("That was not a valid input @" + username)
                    return

        return

    if user_message.lower() == 'hello':
        await message.channel.send(f'Hello {username}')
    elif user_message.lower() == 'bye':
        await message.channel.send(f'See you later {username}!')
    elif user_message.lower() == '!random':
        response = f'This is your random number: {random.randrange(100000)}'
        await message.channel.send(response)

    if user_message.lower() == '!anywhere':
        await message.channel.send('This can be used anywhere!')

    return


client.run(TOKEN)

