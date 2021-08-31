from discordwebhook import Discord

discord = Discord(url="https://discord.com/api/webhooks/882222704877527070/dHukunzFLC1gcq9W8EMEEe7YqonAJulrVEDFp_vX9miuxHN1xmXK8mJ6tm88Hjw73wlE")



def send_discord(text):
    discord.post(content=text)