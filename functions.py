from includes.sqlite import Database
from includes.keyboards import Keyboards
from includes.modules import types
from datetime import date,timedelta,datetime
db = Database("your_database.db")
keb = Keyboards()
class Functions:
    def __init__(self, dp,bot):
        self.dp = dp
        self.bot = bot
    @staticmethod
    async def schudele_vip_signals_date(bot):
        users = db.get_vip_signals()
        for user in users:
            if user[3] != "Unlimit":
                if str(user[3]) < str(date.today()):
                    if not expire:
                        try:
                            time_difference = datetime.strptime(user[3], '%Y-%m-%d') + timedelta(days=3)
                            formatted_date = time_difference.strftime('%Y-%m-%d')
                            db.add_expired_vip_signals(user_id=user[8],start_date=user[2],end_date=user[3],expired_date=formatted_date,status="expired")
                            user_detail = await bot.get_chat(user[1])
                            for admin in db.get_admins():
                                await bot.send_message(admin[3],f"""
سڵاو بەڕێز

ئەم بەشدار بووە ماوەی بەشداری كردنی بەسەرچووە

ناو : {user_detail.full_name}
ویزەر : @{user_detail.username}
بەرواری بەشداری كردن : {user[2]}
بەرواری بەسەرچوون: {user[3]}
نرخ : {user[6]}
جۆری پارەدان : {user[7]}

ماوەی بەشداری كردنی بەسەرچووە ❗

""")
    # تكایە دووبارە بەشداری بكەوە یاخوود لە ماوەی 48 كاتژمێر دەرئەكرێیت لە گرووپی سیگناڵ ✔
                        except Exception as e:
                            print(e)
    def handle_function(self):
        @self.dp.callback_query_handler(lambda c: c.data.startswith(("cancel_again_pay__", "again_pay")))
        async def again_pay(call:types.CallbackQuery):
            hash_id = call.data.split("__")[1]
            detail = db.get_vip_signals(hash_id=hash_id)
            if call.data.startswith("again_pay__"):
                reply_markup = keb.get_payment_method_buttons()
                await call.message.answer("فەرموو ئەمە سەرجەم جۆرەكانی شێوازی پارەدانە :",reply_markup=reply_markup)
                await payment_method_state.SELECT.set()
                try:
                    db.update_column(name_table="expired_vipsignals",column_to_change="status",change_text="expired",where="user_id",where_equal=hash_id)
                    await self.bot.kick_chat_member(chat_id=-1001554682977, user_id=detail[1])
                except Exception as e:
                        await call.message.answer(f"{e}")
            else:
                try:
                    db.update_column(name_table="expired_vipsignals",column_to_change="status",change_text="expired",where="user_id",where_equal=hash_id)
                    await self.bot.kick_chat_member(chat_id=-1001554682977, user_id=detail[1])
                    await call.message.answer("داواكاری وازهێنانت دووپاتكرایەوە")
                except Exception as e:
                        await call.message.answer(f"{e}")
#     @staticmethod
#     async def buy_vipsignal_affilate(bot,user_id,point):
#         user = db.userdata(user_id)
#         if user[6]:
#             affilate_code = user[6]
#             user_affiliate = db.get_detail_of_affiliate(code=affilate_code)
#             await bot.send_message(user_affiliate[0],f"""

# بابەت: 🎉 پیرۆزە بە بەدەستهێنانی {point} خاڵ! 🚀

# بەڕێز

# پیرۆزە بە دەستەبەرکردنی {point} خاڵ لە پرۆگرامی پشتگیری بە هاوبەشکردنی لینکی تایبەتت! 🌟، و ئێمە زۆر خۆشحاڵین بۆ پاداشتی هەوڵەکانتان.

# سوپاس بۆ ئێوە کە بەشێکی سەرەکی بوون لە SNR.
# ئەگەر هەر پرسیارێکتان هەیە یان پێویستتان بە یارمەتی هەیە،نامە بنێرن.


# [SNR].
# """)
#         try:
#             db.add_point(user_id=affilate_code,point=point)
#         except Exception() as e:
#             await bot.send_message(message.from_user.id,e)