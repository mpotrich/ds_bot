import os
import hikari
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.environ["DS_API_KEY"], base_url="https://api.deepseek.com")

bot = hikari.GatewayBot(token=os.environ["TOKEN"])
@bot.listen()
async def ping(event: hikari.GuildMessageCreateEvent) -> None:
    """If a non-bot user mentions your bot, respond with 'Pong!'."""

    # Do not respond to bots nor webhooks pinging us, only user accounts
    if not event.is_human:
        return

    me = bot.get_me()

    if me.id in event.message.user_mentions_ids:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "You are a helpful assistant"},
                {"role": "user", "content": event.message.content[22:]},
            ],
            stream=False
        )
        await event.message.respond(response.choices[0].message.content)

if __name__ == "__main__":
    bot.run()

