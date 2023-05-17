import requests



token = "1084883803706769539" #You should put your Discord token here
response = requests.get("https://discordapp.com/api/v6/guilds/1084877131760283658",
        headers = {"authorization" : token})

print(response.content)