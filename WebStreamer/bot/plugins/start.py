from WebStreamer.bot import StreamBot
from WebStreamer.vars import Var
from WebStreamer.utils.human_readable import humanbytes
from WebStreamer.utils.database import Database
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import UserNotParticipant
db = Database(Var.DATABASE_URL, Var.SESSION_NAME)


@StreamBot.on_message(filters.command('start') & filters.private & ~filters.edited)
async def start(b, m):
    if not await db.is_user_exist(m.from_user.id):
        await db.add_user(m.from_user.id)
        await b.send_message(
            Var.BIN_CHANNEL,
            f"#NEW_USER: \n\nNew User [{m.from_user.first_name}](tg://user?id={m.from_user.id}) Started !!"
        )
    usr_cmd = m.text.split("_")[-1]
    if usr_cmd == "/start":
        if Var.UPDATES_CHANNEL is not None:
            try:
                user = await b.get_chat_member(Var.UPDATES_CHANNEL, m.chat.id)
                if user.status == "kicked":
                    await b.send_message(
                        chat_id=m.chat.id,
                        text="⛔️ اکانت شما به علت ارسال محتوای خلاف قوانین سرویس مسدود شده است.",
                        parse_mode="markdown",
                        disable_web_page_preview=True
                    )
                    return
            except UserNotParticipant:
                await b.send_message(
                    chat_id=m.chat.id,
                    text="🔹 برای استفاده از ربات ابتدا باید عضو کانال شوید، تنها اعضای کانال می توانند از ربات استفاده کنند.",
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton("📢 کانال ربات", url=f"https://t.me/{Var.UPDATES_CHANNEL}")
                            ]
                        ]
                    ),
                    parse_mode="markdown"
                )
                return
            except Exception:
                await b.send_message(
                    chat_id=m.chat.id,
                    text="🔸 خطای نامعلوم!",
                    parse_mode="markdown",
                    disable_web_page_preview=True)
                return
        await m.reply_text(
            text='📤 برای دریافت لینک دانلود مستقیم فایل مورد نظر خودتون رو ارسال یا فوروارد کنید.\n⚠️ در صورت شلوغ بودن سرور از ربات اول یا دوم استفاده کنید.',
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton('📦 ربات اول', url='https://t.me/TelFiles_bot'), InlineKeyboardButton('👨🏻‍💻 پشتیبانی', url='https://t.me/Morning3tar_Bot')],
                    [InlineKeyboardButton("📦 ربات دوم", url='https://t.me/TelFiles_bot3')],
                    [InlineKeyboardButton("📢 کانال ربات", url='https://t.me/Telefiles_official')]
                ]
            ),
            disable_web_page_preview=True
        )
    else:
        if Var.UPDATES_CHANNEL is not None:
            try:
                user = await b.get_chat_member(Var.UPDATES_CHANNEL, m.chat.id)
                if user.status == "kicked":
                    await b.send_message(
                        chat_id=m.chat.id,
                        text="⛔️ اکانت شما به علت ارسال محتوای خلاف قوانین سرویس مسدود شده است.",
                        parse_mode="markdown",
                        disable_web_page_preview=True
                    )
                    return
            except UserNotParticipant:
                await b.send_message(
                    chat_id=m.chat.id,
                    text="🔹 برای استفاده از ربات ابتدا باید عضو کانال شوید، تنها اعضای کانال می توانند از ربات استفاده کنند.",
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton("📢 کانال ربات", url=f"https://t.me/{Var.UPDATES_CHANNEL}")
                            ],
                            [
                                InlineKeyboardButton("🔄 Refresh / Try Again",
                                                     url=f"https://t.me/TelFiles_Bot?start=Morning3tar_{usr_cmd}")
                            ]
                        ]
                    ),
                    parse_mode="markdown"
                )
                return
            except Exception:
                await b.send_message(
                    chat_id=m.chat.id,
                    text="🔸 خطای نامعلوم!",
                    parse_mode="markdown",
                    disable_web_page_preview=True)
                return

        get_msg = await b.get_messages(chat_id=Var.BIN_CHANNEL, message_ids=int(usr_cmd))

        file_size = None
        if get_msg.video:
            file_size = f"{humanbytes(get_msg.video.file_size)}"
        elif get_msg.document:
            file_size = f"{humanbytes(get_msg.document.file_size)}"
        elif get_msg.audio:
            file_size = f"{humanbytes(get_msg.audio.file_size)}"

        file_name = None
        if get_msg.video:
            file_name = f"{get_msg.video.file_name}"
        elif get_msg.document:
            file_name = f"{get_msg.document.file_name}"
        elif get_msg.audio:
            file_name = f"{get_msg.audio.file_name}"

        stream_link = "https://{}/{}".format(Var.FQDN, get_msg.message_id) if Var.ON_HEROKU or Var.NO_PORT else \
            "http://{}:{}/{}".format(Var.FQDN,
                                     Var.PORT,
                                     get_msg.message_id)

        msg_text = "**🗂 نام فایل :**\n`{}`\n\n**📥 لینک دانلود فایل :**\n`{}`\n\n⚠️ لینک دانلود پس از 72 ساعت منقضی میشود.\n💳 برای حمایت و آنلاین نگه داشتن بیشتر ربات میتونید از طریق لینک زیر دونیت کنید :\nhttps://idpay.ir/morning3tar"
        await m.reply_text(
            text=msg_text.format(file_name, stream_link),
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("📥 دانلود فایل", url=stream_link)],
                    [InlineKeyboardButton('👨🏻‍💻 پشتیبانی', url='https://t.me/Morning3tar_Bot'), InlineKeyboardButton('💳 دونیت', url='https://idpay.ir/morning3tar')]
                ]    
            ),
        )


@StreamBot.on_message(filters.command('help') & filters.private & ~filters.edited)
async def help_handler(bot, message):
    if not await db.is_user_exist(message.from_user.id):
        await db.add_user(message.from_user.id)
        await bot.send_message(
            Var.BIN_CHANNEL,
            f"#NEW_USER: \n\nNew User [{message.from_user.first_name}](tg://user?id={message.from_user.id}) Started !!"
        )
    if Var.UPDATES_CHANNEL is not None:
        try:
            user = await bot.get_chat_member(Var.UPDATES_CHANNEL, message.chat.id)
            if user.status == "kicked":
                await bot.send_message(
                    chat_id=message.chat.id,
                    text="⛔️ اکانت شما به علت ارسال محتوای خلاف قوانین سرویس مسدود شده است.",
                    parse_mode="markdown",
                    disable_web_page_preview=True
                )
                return
        except UserNotParticipant:
            await bot.send_message(
                chat_id=message.chat.id,
                text="🔹 برای استفاده از ربات ابتدا باید عضو کانال شوید، تنها اعضای کانال می توانند از ربات استفاده کنند.",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("📢 کانال ربات", url=f"https://t.me/{Var.UPDATES_CHANNEL}")
                        ]
                    ]
                ),
                parse_mode="markdown"
            )
            return
        except Exception:
            await bot.send_message(
                chat_id=message.chat.id,
                text="🔸 خطای نامعلوم!",
                parse_mode="markdown",
                disable_web_page_preview=True)
            return
    await message.reply_text(
        text="📤 برای دریافت لینک دانلود مستقیم فایل مورد نظر خودتون رو ارسال یا فوروارد کنید.",
        parse_mode="Markdown",
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton('📢 کانال ربات', url='https://t.me/Telefiles_official'), InlineKeyboardButton('👨🏻‍💻 پشتیبانی', url='https://t.me/Morning3tar_Bot')],
                [InlineKeyboardButton('💳 دونیت', url='https://idpay.ir/morning3tar')]
            ]
        )
    )
