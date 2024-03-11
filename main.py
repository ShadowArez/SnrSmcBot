from includes.modules import *
from includes.states import *
from includes.sqlite import *
from includes.classes import *
import asyncio
from keep_alive import keep_alive

keep_alive()
from aiogram import executor

API_TOKEN = '7130499850:AAG4bzYojdxUyhjqjaDZFdUgDRDgZ23Hduc'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
affiliate = Affiliate(dp)
VIP = vip_signal(dp, bot=bot)
payment_method = paymentmethod(dp, bot=bot)
FAQ = faq(dp, bot=bot)
FUNCTION = Functions(dp, bot=bot)
CHALLENGE = challnges(dp, bot=bot)
CHANNEL = channel(dp, bot=bot)
analy = analytics(dp, bot=bot)
send_message = send_message(dp, bot=bot)
discount_code = discount_code(dp, bot=bot)
admins = admins(dp, bot=bot)
about = about(dp, bot=bot)
type_of_payment = type_payment(dp, bot=bot)
keb = Keyboards()
db = Database("your_database.db")
db.create_tables()
db.get_discount_codes()
with open('config.json', 'r', encoding='utf8') as config:
  config = json.load(config)


@dp.message_handler(lambda message: message.text == "گەڕانەوە" or message.text
                    == "/start" or message.text.startswith('/'))
async def start(message: types.Message):
  with open('config.json', 'r', encoding='utf8') as config:
    config = json.load(config)
  user_data = db.userdata(message.from_user.id)
  if message.text.startswith("/start "):
    affiliate_code = message.text.split(" ")[1]
    await db.add_affilite_coin(affiliate_code,
                               bot=bot,
                               user_id=message.from_user.id)
  if user_data is None:
    db.add_user(message.from_user.full_name, message.from_user.username,
                message.from_user.id, 'user', datetime.now())
  if await db.check_user_channels(message.from_user.id, bot=bot):
    if user_data and user_data[4] == 'owner' or user_data and user_data[
        4] == "admin":
      await message.answer(config.get('welcomeMessage'),
                           reply_markup=keb.get_owner_keyboards(
                               message.from_user.id))
    elif user_data and user_data[4] == 'user':
      await message.answer(config.get("welcomeMessage"),
                           reply_markup=keb.get_user_keyboards())
  else:
    keyboard_inline = InlineKeyboardMarkup()
    for channel in db.get_channels():
      keyboard_inline.add(
          InlineKeyboardButton("جۆینی ئەم كەناڵە بكە",
                               url=f"https://t.me/{channel[1]}"))
    initial_message = await message.answer(
        "تكایە چاوەڕێ بكە ...", reply_markup=types.ReplyKeyboardRemove())
    await initial_message.delete()
    await message.answer("تكایە سەرەتا جۆینی كەناڵ بكە پاشان /start دابگرە",
                         reply_markup=keyboard_inline)


affiliate.handle()
VIP.handle_signal()
payment_method.handle_payment()
FAQ.handle_faq()
CHALLENGE.handle_challenges()
FUNCTION.handle_function()
CHANNEL.handle()
analy.handle()
send_message.handle()
discount_code.handle()
admins.handle()
about.handle()
type_of_payment.handle()


@dp.message_handler(
    lambda message: message.text == "درووستكردنی هەژماری فۆڕێكس 📊")
async def forex(message: types.Message, state: FSMContext):
  await message.answer("""
بۆ درووستكردنی هەژماری فۆرێكس لە بڕۆكەری INGOT , MULTI BANK بە باشترین شێواز نامە بنێرە بۆ ئەدمین
""",
                       reply_markup=keb.get_admins())


@dp.message_handler(lambda message: message.text == "فۆڕێكس 💱")
async def forex(message: types.Message, state: FSMContext):
  await message.answer("""
فۆڕێکس کورتکراوەی ئاڵوگۆڕی بیانییە، ئاماژەیە بۆ بازاڕی جیهانی بۆ کڕین و فرۆشتنی دراوەکان. گەورەترین و شلترین بازاڕی دارایی جیهانە، کە ٢٤ کاتژمێر لە هەفتەیەکدا پێنج ڕۆژ مامەڵەی پێوەدەکرێت. بەشداربووانی بازاڕی فۆڕێکس بریتین لە بانکەکان، دامەزراوە داراییەکان، کۆمپانیاکان، حکومەتەکان، و بازرگانانی تاکەکەسی. ئامانجی سەرەکی بازرگانی فۆڕێکس ئاسانکاری بازرگانی نێودەوڵەتی و وەبەرهێنانە لە ڕێگەی توانای گۆڕینی بازرگانەکان بۆ گۆڕینی دراوێک بۆ دراوێکی تر. بازرگانانی بازاڕی فۆڕێکس ئامانجیان قازانجکردنە لە هەڵاوسانی نرخی ئاڵوگۆڕکردن بە کڕینی دراوەکان بە نرخێکی کەم و فرۆشتنیان بە نرخێکی زیاتر، یان بە پێچەوانەوە.
""")


@dp.message_handler(lambda message: message.text == "هەژماری فەند 💰")
async def fund_inline(message: types.Message, state: FSMContext):
  await message.answer("فەرموو چۆن هاوكاریت بكەین ؟",
                       reply_markup=keb.fund_inline())


@dp.message_handler(lambda message: message.text == "هەژماری فەند چیە 💸")
async def forex(message: types.Message, state: FSMContext):
  await message.answer("""
بازرگانێکی پارەدار ئەو کەسەیە کە بازرگانی بە ئامرازە داراییەکانەوە دەکات بە بەکارهێنانی سەرمایەی دابینکراو لەلایەن کۆمپانیایەکی بازرگانی خاوەندارێتی یان بەرنامەیەکی پارەدارکردنەوە. زۆرجار ئەم بەرنامانە بە کۆمپانیای بازرگانی پرۆپ یان خانووی بازرگانی پرۆپ ناودەبرێن. ئەو بازرگانەی کە پارەی بۆ دابین دەکرێت سەرمایەی خۆی بۆ بازرگانی بەکارناهێنێت بەڵکو لەبری ئەوە بە پارەی کۆمپانیاکە مامەڵە دەکات.

لە بەرامبەر دەستڕاگەیشتن بە سەرمایەی کۆمپانیاکە، بازرگانانی پارەدار بە شێوەیەکی گشتی ڕازی دەبن بە ڕێکخستنی هاوبەشکردنی قازانج کە تێیدا ڕێژەیەک لەو قازانجانەی کە لە کاتی بازرگانیکردندا بەدەستی دەهێنن دەهێڵنەوە. بەڵام لەوانەیە ناچاربن پابەندبن بە هەندێک یاسا و ڕێنمایی بەڕێوەبردنی مەترسی کە لەلایەن کۆمپانیاکە دانراوە.

ئامانج لە بەرنامە بازرگانییە داراییەکان ئەوەیە کە دەرفەتێک بۆ بازرگانان دابین بکات کە دەستیان بە سەرمایەی بازرگانی گەورەتر بگات لەوەی کە ڕەنگە بە تەنیا هەیانبێت. ئەمەش دەتوانێت ڕێگە بە بازرگانان بدات کە سوود لە دەرفەتی بازرگانی بەرچاوتر وەربگرن و بە ئەگەرێکی زۆرەوە قازانجەکانیان زیاد بکەن. هەروەها ڕێگەیەک بۆ کۆمپانیا بازرگانییەکان دابین دەکات بۆ ئەوەی چالاکییە بازرگانییەکانیان هەمەچەشن بکەن و بە ئەگەرێکی زۆرەوە قازانج لە لێهاتوویی بازرگانی کەسانی بەتوانا بکەن.
""")


buttons = db.get_discount_codes()


@dp.message_handler(
    lambda message: any(message.text == button[1] for button in buttons))
async def answer_buttons(message: types.Message):
  for button in buttons:
    if message.text == button[1]:
      if db.get_admins(user_id=message.from_user.id):
        if button[3]:
          await self.bot.send_photo(chat_id=message.from_user.id,
                                    photo=button[3],
                                    caption=f"{button[1]}\n{button[2]}",
                                    reply_markup=keb.buttons_discount_delete(
                                        button[1]))
        else:
          await message.answer(f"{button[1]}\n{button[2]}",
                               reply_markup=keb.buttons_discount_delete(
                                   button[1]))
      else:
        if button[3]:
          await self.bot.send_photo(chat_id=message.from_user.id,
                                    photo=button[3],
                                    caption=f"{button[1]}\n{button[2]}")
        else:
          await message.answer(f"{button[1]}\n{button[2]}")


async def scheduled_task():
  while True:
    await FUNCTION.schudele_vip_signals_date(bot=bot)
    await asyncio.sleep(24 * 3600)


async def handle_buttons():
  while True:
    buttons = db.get_discount_codes()
    for user in db.userdata():
      user_detail = await bot.get_chat(user[3])
      if user[2] != user_detail.username:
        db.update_column(name_table="users",
                         column_to_change="username",
                         change_text=user_detail.username,
                         where='id',
                         where_equal=user[0])
      if user[1] != user_detail.full_name:
        db.update_column(name_table="users",
                         column_to_change="full_name",
                         change_text=user_detail.full_name,
                         where='id',
                         where_equal=user[0])
    await asyncio.sleep(5)


if __name__ == '__main__':
  loop = asyncio.get_event_loop()
  loop.create_task(scheduled_task())
  loop.create_task(handle_buttons())
  executor.start_polling(dp, skip_updates=True)
  loop.run_forever()
