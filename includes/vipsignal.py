from datetime import date,timedelta
from includes.modules import types, FSMContext,json,requests,BeautifulSoup
from includes.keyboards import Keyboards
from includes.affilate import*
from includes.states import*
from includes.sqlite import Database
from includes.functions import Functions
import re,random
db=Database("your_database.db")
keb = Keyboards()
with open('config.json', 'r', encoding='utf8') as config:
    config = json.load(config)
class vip_signal:
    def __init__(self, dp,bot):
        self.dp = dp
        self.bot = bot
        self.fun = Functions(self.dp, self.bot)
    def handle_signal(self):
        @self.dp.message_handler(lambda message: message.text == "گرووپی سیگناڵ 📡")
        async def group_signal(message: types.Message):
            with open('config.json', 'r', encoding='utf8') as config:
                config = json.load(config)
            output = ""
            if "type_of_payment" in config:
                for payment in config["type_of_payment"]:
                    if "payment" in payment:
                        output += f"بۆ ماوەی {payment['payment']['days']} ڕۆژ : {payment['payment']['price']} دۆلار💵\n"


            await message.answer('''سڵاو بەڕێزەکەم 🤍

بۆ بەشداری کردن لە گرووپی سیگناڵی VIP دوو ڕێگا هەیە :📈

ڕێگای یەکەم لە ڕێی پارەدان 💰

''' + output + '''

ڕێگای دووەم  لەڕێی برۆکەرەوە 🏦

پێویستە ئەکاونت لە ڕێگەی ئێمەوە بکەیتەوە لە برۆکەری INGOT یان MULTIEBANK و 500$ بۆ داخڵ بکەیت پاشان داخڵ دەکرێت لە گروپەکە بە خۆڕایی وە ئەگەر هەژمارت هەیە لەو دوو برۆکەرەی باس مان کرد ئەوە ئەتوانی بیتە سەر لینکی ئێمە بۆ ئەوەی داخیل گروپی سیگناڵی VIP بیت

~~~~~~~~~~~~~~~~~
بۆ بەشداری کردن لە ڕێی پارەدان گرتە بکە لە (پارەدان)

بۆ بەشداری کردن لەڕێی بڕۆکەر گرتە لە (برۆکەر)

زۆر سپاس🤍''', reply_markup=keb.get_sigal_group(), parse_mode=types.ParseMode.MARKDOWN)
            await vip_signal_state.SELECT.set()
        @self.dp.message_handler(state=vip_signal_state.SELECT)
        async def select_signal(message: types.Message,state:FSMContext):
            if message.text == "پارەدان":
                await message.answer("""
                زۆر سپاس بۆ داواكارییەكەت ، تكایە جۆری پارەدان دیاری بكە :
                """, reply_markup=keb.get_payment_method(back=True))
                await vip_signal_state.SELECT_PAYMENT.set()
            elif message.text == "بڕۆكەر":
                await message.answer("زۆر باشە ، ئایا پێشتر هەژمارت هەبووە ؟",reply_markup=keb.get_broker_account())
                await vip_signal_state.PAYMENT_OR_BROKER.set()
            else:
                await message.answer("چۆن بتوانم هاوکاریت بکەم ؟🌹", reply_markup=keb.get_user_keyboards())
                await state.finish()
        @self.dp.message_handler(state=vip_signal_state.PAYMENT_OR_BROKER)
        async def broker_or_create(message: types.Message,state:FSMContext):
            if message.text == "بەڵێ":
                await message.answer("""
                زۆر سپاس ، تكایە جۆری بڕۆكەر دیاری بكە :
                """, reply_markup=keb.get_brokers_name())
                await vip_signal_state.ACCOUNT_BROKER.set()

            elif message.text == "درووستكردنی هەژمار":
                await message.answer("بۆ درووستكردنی هەژماری فۆرێكس لە بڕۆكەری INGOT , MULTI BANK بە باشترین شێواز نامە بنێرە",reply_markup=keb.get_user_keyboards())
                await message.answer("ئەدمینەكان : ",reply_markup=keb.get_admins())

                await state.finish()
            else:
                await message.answer(config.get("welcomeMessage"),reply_markup=keb.get_sigal_group())
                await vip_signal_state.SELECT.set()
        @self.dp.message_handler(state=vip_signal_state.SELECT_PAYMENT)
        async def select_payment(message: types.Message,state:FSMContext):
            if message.text == "گەڕانەوە":
                await message.answer(config.get("welcomeMessage"),reply_markup=keb.get_user_keyboards())
                await state.finish()
            else:
                await state.update_data(method = message.text)
                await message.answer("زۆر باشە ،تكایە ماوەی بەشداری كردن دیاری بكە :",reply_markup=keb.get_pay_price_date())
                await vip_signal_state.SELECT_DATE.set()
        @self.dp.message_handler(state=vip_signal_state.SELECT_DATE)
        async def select_date(message: types.Message,state:FSMContext):
            await state.update_data(muda = message.text)
            data = await state.get_data()
            await message.answer(f"""

زۆر باشە ، ئایا دڵنیایی لە كڕین و پارەدان ؟.

جۆری پارەدان : {data.get("method")}
ماوەی بەشداری كردن : {data.get("muda")}

""",parse_mode=types.ParseMode.MARKDOWN,reply_markup=keb.get_confirm_account_creation())
            await vip_signal_state.SELECT_CONFIRM.set()
        @self.dp.message_handler(state=vip_signal_state.SELECT_CONFIRM)
        async def select_confirm(message: types.Message,state:FSMContext):
            if message.text == "بەڵێ":
                data = await state.get_data()
                url = 'https://qamaralfajr.com/production/exchange_rates.php?fbclid=PAAaaer3uyz3H8RVeoSoPxQv2UAsW_oRj3lK4RGEhJP04FGSb9PW1wpP0PYdg'
                headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
                'Accept-Language': 'en-US,en;q=0.5',
                }
                response = requests.get(url, headers=headers, timeout=5)
                if response.ok:
                    price_get = BeautifulSoup(response.text, 'html.parser')
                    button_text_get = price_get.button.get_text()
                    price_amount = price_get.find('button')
                    # Get payment method and date
                    payment_method = data.get("method")
                    parts = data.get("muda").split(':')
                    price_string = parts[1]
                    price_numeric = re.sub(r'\D', '', price_string)
                    price = int(price_numeric)
                    if price_amount:
                        match = re.search(r'\b\d+\b', button_text_get)
                        prmulti = int(match.group()) * int(price)
                        # Update state with price in dollars and formatted total price
                        await state.update_data(dolar=price)
                        # Format total price with commas
                        number2 = str(prmulti)[:-4] + '00'
                        formatted_number = "{:,.0f}".format(int(number2))
                        await state.update_data(price=formatted_number)
                        # payment detail
                        paymen_detail = db.get_payment_methods(title=payment_method)
                        if paymen_detail[3]:
                            await self.bot.send_photo(chat_id=message.from_user.id,caption=f"""
تكایە وێنەی پارەی مامەڵەی پارە ناردنەكە بنێرە یاخوود پاشگەزبوونەوە دابگرە

كۆی گشتی نرخ : {formatted_number}

زانیاری پارەدان:

{paymen_detail[2]}
""",photo=paymen_detail[3],parse_mode=types.ParseMode.MARKDOWN,reply_markup=keb.back_confirm())
                        else:
                            await message.answer(f"""
تكایە وێنەی پارەی مامەڵەی پارە ناردنەكە بنێرە یاخوود پاشگەزبوونەوە دابگرە

كۆی گشتی نرخ : {formatted_number} , ${price}

زانیاری پارەدان:

{paymen_detail[2]}
""",parse_mode=types.ParseMode.MARKDOWN,reply_markup=keb.back_confirm())
                        await vip_signal_state.CONFIRM_SEND_NUMBER.set()
                else:
                    await message.answer("ببورە هەڵەیەك هەیە تكایە پەیوەمدیمان پێوە بكە",reply_markup=keb.get_user_keyboards())
                    await state.finish()
            else:
                await message.answer(config.get("welcomeMessage"),reply_markup=keb.get_user_keyboards())
                await state.finish()
        @self.dp.message_handler(content_types=types.ContentTypes.PHOTO,state=vip_signal_state.CONFIRM_SEND_NUMBER)
        async def send_number_pay(message: types.Message,state:FSMContext):
            data = await state.get_data()
            try:
                hash_id = random.randint(100000000,99999999999)
                db.add_user_to_vipsignals(message.from_user.id,start_date=date.today(),end_date="Not yet",type_offer="pay",status="pedding_payment",price=data.get("price"),payment_method=data.get("method"),hash_id=hash_id,dolar=data.get('dolar'))
            except Exception as e:
                await message.answer(e)
            for admin in db.get_admins():
                await self.bot.send_photo(admin[3],photo=message.photo[-1].file_id,caption=f"""
سڵاو

ئەم بەڕێزە دەیەوێت بەشداری گرووپی سیگناڵ بكات لە ڕێێ پارەدان

جۆری پارەدان : {data.get("method")}
ماوەی بەشداری كردن : {data.get("muda")} , ${data.get("dolar")}
ویزەر : @{message.from_user.username}
{data.get("price")} : كۆی گشتی نرخ

""",reply_markup=keb.send_message_to_admins_confirm_account_creation(hash_id,type="pay",username=message.from_user.username),parse_mode=types.ParseMode.MARKDOWN)
            await message.answer(f"""
داواكارییەكەت بە سەركەوتووی تۆماركرا ، پاش كەمێكی دیكە جوابت ئەدرێتەوە

جۆری پارەدان : {data.get("method")}
ماوەی بەشداری كردن : {data.get("muda")}
كۆی گشتی نرخ : {data.get("price")} , ${data.get("dolar")}
""",reply_markup=keb.get_user_keyboards())
            await state.finish()
        @self.dp.message_handler(state=vip_signal_state.CONFIRM_SEND_NUMBER)
        async def send_number_pay(message: types.Message,state:FSMContext):
            if message.text == "پاشگەزبوونەوە":
                await message.answer("سەرەتا",reply_markup=keb.get_user_keyboards())
                await state.finish()
            else:
                await message.answer("ببورە ئەوەی ناردووتە وێنە نیە ، تكایە وێنەی پێویست بنێرە",reply_markup=keb.back_confirm())
        @self.dp.message_handler(state=vip_signal_state.ACCOUNT_BROKER)
        async def broker_Account(message: types.Message,state:FSMContext):
            if message.text in ['INGOT',"Multi Bank"]:
                await state.update_data(broker_name=message.text)
                await message.answer("زۆر باشە ، تكایە UID هەژمارەكەت بنێرە :")
                await vip_signal_state.ACCOUNT_EXISTS.set()
            else:
                await message.answer("ببوورە هەلبژاردنەكەت هەڵەیە")
                await message.answer(config.get("welcomeMessage"),reply_markup=keb.get_sigal_group())
                await state.finish()
        # uid exists
        @self.dp.message_handler(state=vip_signal_state.ACCOUNT_EXISTS)
        async def send_uid(message:types.Message,state:FSMContext):
            await state.update_data(uid=message.text)
            await message.answer("زۆر باشە ، ئایا دڵنیایی لە بەشداری كردن ؟",reply_markup=keb.get_confirm_of_create_account())
            await vip_signal_state.ACCOUNT_EXISTS_CONFIRM.set()
        @self.dp.message_handler(lambda message:message.text in ["بەڵێ","نەخێر"],state=vip_signal_state.ACCOUNT_EXISTS_CONFIRM)
        async def confirm_uid(message:types.Message,state:FSMContext):
            if message.text == "بەڵێ":
                await message.answer("زۆر باشە ، زانیارییەكانت تۆمار كرا ، پاش كەمێكی دیكە وەڵامت پێ ئەگات.",reply_markup=keb.get_user_keyboards())
                data = await state.get_data()
                hash_id = random.randint(100000000,99999999999)
                db.add_user_to_vipsignals(message.from_user.id,start_date=date.today(),end_date="Unlimit",type_offer="broker",status="pedding_accept",price="None",payment_method="None",hash_id=hash_id,dolar="None")
                for admin in db.get_admins():
                    await self.bot.send_message(admin[3],text=f"""
سڵاو

ئەم بەڕێزە دەیەوێت بەشداری گرووپی سیگناڵ بكات لە ڕێێ بڕۆكەرەوە

ناوی تەواو : {message.from_user.full_name}
ویزەر : @{message.from_user.username}
ناوی بڕۆكەر : {data.get('broker_name')}
UID : {data.get('uid')}

""",reply_markup=keb.send_message_to_admins_confirm_account_creation(hash_id,type="broker",username=message.from_user.id),parse_mode=types.ParseMode.MARKDOWN)
            else:
                await message.answer("بەسەركەوتووی هەڵوەشاەوە",reply_markup=keb.get_user_keyboards())
            await state.finish()
        @self.dp.callback_query_handler(lambda c: c.data.startswith(("accept_", "reject_")))
        async def call_start(call: types.CallbackQuery, state: FSMContext):
            hash_id = call.data.split('_')[1]
            type = call.data.split('__')[1]
            price = db.get_vip_signals(hash_id=hash_id)
            user_id = price[1]
            if call.data.startswith("accept_"):
                if type == "broker":
                    if price[5] != "done":
                        await call.message.answer("داواكارییەكەت قبووڵ كرا لینكی تایبەت ناردرا بۆ بەشداربوو.")
                        try:
                            db.update_column(name_table="vip_signals", column_to_change="status", change_text="done",
                                        where='hash_id', where_equal=price[8])
                            invite_link = await self.bot.create_chat_invite_link(-1001554682977, member_limit=1)
                            await self.bot.send_message(user_id, f"""
سڵاو بەڕێز

{invite_link.invite_link} : ئەمە لینكی تایبەتی تۆیە

ڕۆژی بەشداری كردن : {date.today()}
ڕۆژی بەسەرچوون : ماوەی نیە

تكایە یاساكان بپارێزە بۆوەی دەرنەكرێیت!

زۆر سپاس
                            """, parse_mode=types.ParseMode.MARKDOWN, reply_markup=keb.get_user_keyboards())
                        except Exception as e:
                            await call.message.answer(f"Error: {e}")

                elif type == "pay" and price[5] != "done":
                    try:
                        price = db.get_vip_signals(hash_id=hash_id)
                        multipliers = {'35': 30, '90': 90, '180': 180, '280': 365}
                        default_multiplier = 1
                        multiplier = next((value for key, value in multipliers.items() if key in price[9]), default_multiplier)

                        db.update_column(name_table="vip_signals", column_to_change="start_date", change_text=date.today(),
                                        where='hash_id', where_equal=hash_id)
                        db.update_column(name_table="vip_signals", column_to_change="end_date",
                                        change_text=date.today() + timedelta(days=multiplier), where='hash_id',
                                        where_equal=hash_id)
                        db.update_column(name_table="vip_signals", column_to_change="status", change_text="done",
                                        where='hash_id', where_equal=hash_id)

                        invite_link = await self.bot.create_chat_invite_link(-1001554682977, member_limit=1)

                        await self.bot.send_message(price[1], f"""
سڵاو بەڕێز

بەسەركەوتووی داواكارییەكەت قبووڵ كرا

ڕۆژی بەشداری كردن : {price[2]}
ڕۆژی بەسەرچوون: {date.today() + timedelta(days=multiplier)}
نرخی بەشداری كردن : {price[6]}
جۆری پارەدان : {price[7]}

لینكی بەشداری كردن:
{invite_link.invite_link}
""")

                        await call.message.answer("بەسەركەوتووی ناردرا")
                        # await self.fun.buy_vipsignal_affilate(user_id=user_id,point=5,bot=self.bot)
                    except Exception as e:
                        await call.message.answer(str(e))

            elif call.data.startswith("reject_"):
                if price[5] != "done":
                    await call.message.answer("تكایە هۆكاری ڕەتكردنەوە بنووسە", reply_markup=keb.back_confirm())
                    await state.update_data(user_id=price[1])
                    await state.update_data(hash_id=price[8])
                    await vip_signal_state.REJECT.set()

        @self.dp.message_handler(state=vip_signal_state.REJECT)
        async def confamrion_account(message: types.Message, state: FSMContext):
            if message.text == "پاشگەزبوونەوە":
                await message.answer("هەڵوەشایەوە", reply_markup=keb.get_owner_keyboards())
            else:
                data = await state.get_data()
                user_id = data.get("user_id")
                hash_id = data.get("hash_id")
                msg = message.text
                await self.bot.send_message(user_id, f"""
سڵاو بەڕێز

ببورە نەمان توانی داواكارییەكەت قبووڵ بكەین بە هۆكاری :
{msg}

زۆر سپاس🤍
                """)
                await message.answer("سەركەوتووبوو",reply_markup=keb.get_owner_keyboards())
                db.update_column(name_table="vip_signals", column_to_change="status", change_text="reject", where='hash_id',
                                where_equal=hash_id)
            await state.finish()