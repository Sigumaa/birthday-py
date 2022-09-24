import discord
import re
import datetime

intents=discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print("起動しました！")

# Writes to a text file associating the user's ID with birthday
def register_birthday(user_id, birthday):
    if (check_birthday(birthday) == None):
        return "Invalid birthday format"
    with open("birthdays.txt", "a") as f:
        f.write("{}{}{}\n".format(user_id, ":", birthday))
    return "Birthday registered! : {}".format(birthday)

# Regular expression to check if it is the correct birthday
def check_birthday(birthday):
    return re.match(r"^(0[1-9]|1[0-2])(/)(0[1-9]|[12][0-9]|3[01])$", birthday)

# Reads the text file and returns the birthday of the user
async def today_birthday(message):
    is_today = False
    with open("birthdays.txt", "r") as f:
        for line in f:
            if (line.split(":")[1] == today()):
                is_today = True
                await message.channel.send("<@" +line.split(":")[0] + "> お誕生日おめでとう！")
    if (is_today == False):
        await message.channel.send("今日誕生日の人はいません。")

# Returns today's date
def today():
    return datetime.datetime.now().strftime("%m/%d") + "\n"

@client.event
async def on_message(message):
    if message.author.bot:
        return
    if message.content.startswith("登録"):
        print("登録コマンドを受け付けました")
        await message.channel.send(register_birthday(message.author.id, message.content[3:]))
    if message.content == "誕生日":
        await today_birthday(message)

client.run("token")
