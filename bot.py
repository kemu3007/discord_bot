import os
from datetime import datetime, timedelta, timezone

import requests
from dotenv import load_dotenv

import discord
from discord.ext import tasks

load_dotenv()

base_url = os.getenv("BASE_URL")
JST = timezone(timedelta(hours=+9), "JST")


class MyClient(discord.Client):
    async def on_ready(self):
        print("waiting message...")

    async def on_message(self, message):
        try:
            message_list = message.content.split()
            if message.author.bot or len(message_list) == 0:
                return
            if message_list[0] == "$ohayou_list":
                response = requests.get(
                    url=f"{base_url}/ohayou/",
                    headers={"content-type": "application/json"},
                )
                reply = ""
                if response.status_code == 200:
                    for ohayo in response.json():
                        reply += f"{ohayo['id']} {ohayo['text']} \n"
                    return await message.channel.send(reply)
                else:
                    raise SyntaxError
            elif message_list[0] == "$ohayou_add":
                response = requests.post(
                    url=f"{base_url}/ohayou/",
                    data={"text": message.content.strip("$ohayou_add")},
                )
                if response.status_code == 200:
                    return await message.channel.send(f"{message.content.strip('$ohayou_add')} をあいさつに追加しました")
                else:
                    raise SyntaxError
            elif message_list[0] == "$ohayou_delete":
                if len(message_list) >= 2:
                    response = requests.delete(url=f"{base_url}/ohayou/{message_list[1]}/")
                    if response.status_code == 204:
                        return await message.channel.send(f"pk: {message_list[1]} のあいさつを削除しました")
                    elif response.status_code == 404:
                        return await message.channel.send(f"pk: {message_list[1]} のあいさつは存在しません")
                else:
                    return await message.channel.send(f"IDを指定してください")
            elif message_list[0] == "$holodule":
                response = requests.get(url=f"{base_url}/holodule/")
                if response.status_code == 200:
                    embed = discord.Embed(title="ほろじゅーる", description=response.json()["message"])
                    return await message.channel.send(embed=embed)
                raise SyntaxError
            elif message_list[0] == "$holodule_reminder":
                try:
                    if message_list[1] == "on":
                        response = requests.post(
                            url=f"{base_url}/holodule_reminder/",
                            data={"channel_code": message.channel.id, "channel_name": message.channel.name},
                        )
                        if response.status_code == 200:
                            return await message.channel.send(response.json()["message"])
                        else:
                            return await message.channel.send("このチャンネルには既にリマインダーが設定されています")
                    elif message_list[1] == "off":
                        response = requests.delete(url=f"{base_url}/holodule_reminder/{message.channel.id}/")
                        return await message.channel.send("リマインダーを解除しました")
                    else:
                        raise SyntaxError
                except (IndexError, SyntaxError):
                    return await message.channel.send("on, offのどちらかを入力してください")
            elif "おはよう" in message.content:
                response = requests.get(
                    url=f"{base_url}/ohayou/generate/",
                    headers={"content-type": "application/json"},
                )
                if response.status_code == 200:
                    return await message.channel.send(response.json()["message"])
                raise SyntaxError
            elif "すいちゃんは" in message.content:
                return await message.channel.send("今日もかわいい～～～")
            elif "猫やんけ" in message.content:
                return await message.channel.send("狐じゃい！！！！")
        except Exception as e:
            return await message.channel.send(f"エラーが発生しました、管理者に問い合わせてください \n detail: {e}")


@tasks.loop(minutes=60)
async def remind_holodule():
    if datetime.now(JST).hour == 16:
        response = requests.get(url=f"{base_url}/holodule_reminder/")
        if response.status_code == 200:
            channels = [channel_info["channel_code"] for channel_info in response.json()]
            holodule = requests.get(url=f"{base_url}/holodule/")
            if holodule.status_code == 200:
                embed = discord.Embed(title="ほろじゅーる", description=holodule.json()["message"])
                for channel in channels:
                    channel = client.get_channel(int(channel))
                    if channel:
                        return await channel.send(embed=embed)


client = MyClient()
remind_holodule.start()
client.run(os.getenv("TOKEN"))
