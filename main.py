import os
import discord
from discord.ext import commands
from groq import Groq
from collections import defaultdict, deque
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL = os.getenv("MODEL", "llama-3.3-70b-versatile")

if not DISCORD_TOKEN:
    raise RuntimeError("DISCORD_TOKEN is missing. Copy .env.example to .env and fill it in.")
if not GROQ_API_KEY:
    raise RuntimeError("GROQ_API_KEY is missing. Copy .env.example to .env and fill it in.")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)
groq = Groq(api_key=GROQ_API_KEY)

history = defaultdict(lambda: deque(maxlen=10))

SYSTEM_PROMPT = (
    "You are Mira AI, a friendly, witty assistant running inside a Discord bot. "
    "Reply in the same language the user uses. Be concise, helpful, and natural. "
    "Use a conversational tone. If a question is unclear, ask a short follow-up."
)


def is_private_or_mentioned(message):
    if isinstance(message.channel, discord.DMChannel):
        return True
    if bot.user and bot.user in message.mentions:
        return True
    return False


def strip_mention(content, bot_user):
    if bot_user is None:
        return content
    for u in content.split():
        if u.startswith(f"<@{bot_user.id}>") or u.startswith(f"<@!{bot_user.id}>"):
            content = content.replace(u, "")
    return content.strip()


@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user} (id={bot.user.id})")
    print(f"Model: {MODEL}")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="!help | AI chat"))


@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if is_private_or_mentioned(message):
        user_id = str(message.author.id)
        prompt = strip_mention(message.content, bot.user)
        if not prompt:
            await message.reply("هلا فيك! اسألني أي شي تبيه 🤖")
            return

        async with message.channel.typing():
            try:
                msgs = [{"role": "system", "content": SYSTEM_PROMPT}]
                for turn in history[user_id]:
                    msgs.append({
                        "role": "user" if turn["role"] == "user" else "assistant",
                        "content": turn["content"],
                    })
                msgs.append({"role": "user", "content": prompt})

                resp = groq.chat.completions.create(
                    model=MODEL,
                    messages=msgs,
                    max_tokens=800,
                    temperature=0.7,
                )
                reply = resp.choices[0].message.content.strip()

                history[user_id].append({"role": "user", "content": prompt})
                history[user_id].append({"role": "assistant", "content": reply})

                if len(reply) > 2000:
                    reply = reply[:1997] + "..."
                await message.reply(reply)
            except Exception as e:
                await message.reply(f"❌ Error: `{e}`")

    await bot.process_commands(message)


@bot.command(name="help")
async def help_cmd(ctx):
    await ctx.send(
        "🤖 **Mira AI — Commands**\n"
        "`!ping` — check latency\n"
        "`!model` — show current model\n"
        "`!forget` — clear your chat history\n"
        "Just DM me or mention me to chat!"
    )


@bot.command(name="ping")
async def ping(ctx):
    await ctx.send(f"🏓 Pong! {round(bot.latency * 1000)}ms")


@bot.command(name="model")
async def model_cmd(ctx):
    await ctx.send(f"🧠 Current model: **{MODEL}** (open source via Groq)")


@bot.command(name="forget")
async def forget(ctx):
    history.pop(str(ctx.author.id), None)
    await ctx.send("🧹 Your memory was cleared.")


if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)
