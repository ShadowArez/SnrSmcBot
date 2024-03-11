from includes.modules import types, FSMContext,json
from includes.keyboards import Keyboards
from includes.affilate import*
from includes.states import*
from includes.sqlite import Database
db=Database("your_database.db")
keb = Keyboards()
with open('config.json', 'r', encoding='utf8') as config:
    config = json.load(config)
class Affiliate:
    def __init__(self, dp ):
        self.dp = dp

    def handle(self):
        @self.dp.message_handler(lambda message: message.text == "هەژمار")
        async def profile_cmd(message: types.Message):
            get_user = db.get_detail_of_affiliate(message.from_user.id)
            global keyboard
            if get_user and get_user[0]:
                keyboard = keb.get_affiliate_exists_button(message.from_user.id)
            else:
                keyboard = keb.get_profile_buttons()
            await message.answer("""
        سڵاو بەڕێز تكایە یەكێك لە هەڵبژاردەكان دیاری بكە :
        """, reply_markup=keyboard)
        @self.dp.message_handler(lambda message: message.text == "پشتگیری")
        async def profile_cmd(message: types.Message):
            await message.answer("""
            تاقیكردنەوە
            """, reply_markup=keb.get_affiliate())
        @self.dp.message_handler(lambda message: message.text == "زانیاری پشتگیری")
        async def profile_cmd(message: types.Message):
            await message.answer(config.get('affiliate_about'),reply_markup=keb.get_affiliate())
        @self.dp.message_handler(lambda message: message.text == "دەستپێكردن")
        async def profile_cmd(message: types.Message):
            await message.answer("یەڕێز ئایا دڵنیایت لە بەشداری كردن ؟",reply_markup=keb.get_start_button())
            await Affiliate_State.next()
        @self.dp.message_handler(lambda message: message.text in ["بەڵی","نەخێر"],state=Affiliate_State.CONFIRM)
        async def profile_cmd(message: types.Message,state:FSMContext):
            if message.text == "نەخێر":
                await message.answer("هەڵوەشایەوە")
                await state.finish()
            elif message.text == "بەڵی":
                try:
                    await message.answer("سووپاس بۆ بەشداری كردنت \nتكایە گرتە بكە لە پشتگیری بۆ دەسكەوتنی زانیارییەكانت",reply_markup=keb.get_affiliate_and_back())
                    db.add_user_to_affiliate(message.from_user.id)
                except Exception as e:
                    await message.answer(f"ببورە هەڵەیەك هەیە {e}")
                await state.finish()
            else:
                message.answer("ببورە هەڵبژاردنەكەت هەڵەیە")
        @self.dp.callback_query_handler(lambda c: c.data.startswith(("points", "speciallink")))
        async def profile_cmd(call: types.CallbackQuery):
            user_id = call.data.split('_')[1]

            if user_id:
                get_user = db.get_detail_of_affiliate(user_id)

                if call.data.startswith("points"):
                    await call.message.answer(f"{get_user[2]} : كۆی گشتی كۆینەكانت")
                elif call.data.startswith("speciallink"):
                    await call.message.answer("لینكی تایبەت")
                    await call.message.answer(f"https://t.me/snrsupportbot?start={get_user[1]}")
            else:
                # Handle the case where user_id is not found
                await call.message.answer("Invalid data format.")