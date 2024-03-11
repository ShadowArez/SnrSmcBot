from includes.modules import types, FSMContext,json
from includes.keyboards import Keyboards
from includes.affilate import*
from includes.states import*
from includes.sqlite import Database
import re
db=Database("your_database.db")
keb = Keyboards()
with open('config.json', 'r', encoding='utf8') as config:
    config = json.load(config)
class paymentmethod:
    def __init__(self, dp,bot):
        self.dp = dp
        self.bot = bot
    def handle_payment(self):
        @self.dp.message_handler(lambda message: message.text == "جۆری پارەدان 💳")
        async def payment_method(message: types.Message):
            reply_markup = keb.get_payment_method_buttons()
            await message.answer("فەرموو ئەمە سەرجەم جۆرەكانی شێوازی پارەدانە :",reply_markup=reply_markup)
        @self.dp.callback_query_handler(lambda c:c.data.startswith(('add_pay_buttonk',"deletebuttons_")))
        async def payment_select(call: types.CallbackQuery,state:FSMContext):
            if call.data == "add_pay_buttonk":
                await call.message.answer("ئایا دڵنیایی لە زیادكردنی جۆری پارەدان",reply_markup=keb.get_start_button())
                await payment_method_state.CONFIRM_CREATE.set()
            else:
                title1 = call.data.split("_")[1]
                payment = db.get_payment_methods(title=title1)
                if payment[3]:
                    await self.bot.send_photo(chat_id=call.from_user.id,photo=payment[3],caption=f"{payment[1]}\n{payment[2]}",reply_markup=keb.get_confrim_delete_dis(button=title1,ne=True))
                else:
                    await call.message.answer(f"""
{payment[1]}
{payment[2]}

ئایا دڵنیایی لە ڕەشكردنەوەی ؟
                    """,reply_markup=keb.get_confrim_delete_dis(button=title1,ne=True))
        @self.dp.message_handler(lambda message: message.text in ["بەڵێ","نەخێر"],state=payment_method_state.CONFIRM_CREATE)
        async def confirm_payment(message: types.Message,state:FSMContext):
            if message.text == "بەڵێ":
                await message.answer("نكایە ناوی جۆری پارەدان بنووسە :")
                await payment_method_state.TITLE.set()
            elif message.text == "نەخێر":
                await message.answer("هەڵوەشایەوە",reply_markup=keb.get_owner_keyboards(message.from_user.id))
                await state.finish()
            else:
                await message.answer("ببوورە هەلبژاردنەكەت هەڵەیە",reply_markup=keb.get_user_keyboards())

        @self.dp.message_handler(state=payment_method_state.TITLE)
        async def process_title(message: types.Message,state:FSMContext):
            await state.update_data(title=message.text)
            await message.answer("زۆر باشە ، تكایە زانیاری بنێرە :")
            await payment_method_state.DESCRAPTION.set()
        @self.dp.message_handler(state=payment_method_state.DESCRAPTION)
        async def process_descraption(message: types.Message,state:FSMContext):
            await state.update_data(descraption=message.text)
            data = await state.get_data()
            await message.answer(f"""
زۆر باشە ، ئەمانە زانیارییەكانن

{data.get("title")}
{data.get("descraption")}

""",reply_markup=keb.add_payment_method(),parse_mode=types.ParseMode.MARKDOWN)
            await payment_method_state.PHOTO_CONFIRM.set()
        @self.dp.message_handler(lambda message: message.text in ["زیادكردنی وێنە","دووپاتكردنەوە","گەڕانەوە"],state=payment_method_state.PHOTO_CONFIRM)
        async def process_check(message: types.Message,state:FSMContext):
            if message.text == "زیادكردنی وێنە":
                await message.answer("زۆر باشە ، وێنەكە بنێرە")
                await payment_method_state.PHOTO.set()
            elif message.text == "دووپاتكردنەوە":
                data = await state.get_data()
                try:
                    db.add_payment_methods(data)
                    await message.answer("بەسەركەوتووی زیادكرا",reply_markup=keb.get_owner_keyboards(message.from_user.id))
                except Exception as e:
                    await message.answer(e)
            else:
                await message.answer("هەڵوەشایەوە",reply_markup=keb.get_user_keyboards())
                await state.finish()
        @self.dp.message_handler(content_types=types.ContentTypes.PHOTO,state=payment_method_state.PHOTO)
        async def process_photo(message: types.Message,state:FSMContext):
            photo_id = message.photo[-1].file_id
            await state.update_data(photo = photo_id)
            data = await state.get_data()
            await self.bot.send_photo(chat_id = message.from_user.id,
                                    photo=photo_id,
                                    caption=f'{data.get("title")}\n{data.get("descraption")}',
                                    reply_markup=keb.add_payment_method(photo=True)
                                    )
            await payment_method_state.CONFIRM.set()
        @self.dp.message_handler(lambda message:message.text,state=payment_method_state.PHOTO)
        async def process_broker(message: types.Message,state:FSMContext):
            await message.answer("ببورە ئەوەی ناردووتە هەڵەیە ، بەڕێزەكەم تكایە ڕەسم بنێرە ")

        @self.dp.message_handler(lambda message: message.text in ["دووپاتكردنەوە","گەڕانەوە"],state=payment_method_state.CONFIRM)
        async def process_confirm(message: types.Message,state:FSMContext):
            if message.text == "دووپاتكردنەوە":
                data = await state.get_data()
                try:
                    db.add_payment_methods(data,photo=True)
                    await message.answer("بەسەركەوتووی زیادكرا")
                except Exception as e:
                    await message.answer(e)
                await state.finish()
            if message.text == "گەڕانەوە":
                await message.answer("ڕەتكرایەوە",reply_markup=keb.get_owner_keyboards(message.from_user.id))
                await state.finish()
        @self.dp.callback_query_handler(lambda c:c.data.startswith("yesy_deletess__"))
        async def delet_disc_confirm(call : types.CallbackQuery):
            button_title = call.data.split("__")[1]
            try:
                db.delete_column(name_table="payment_method",where="title",where_equal=button_title)
                await call.message.answer("بەسەركەوتووی ڕەشكرایەوە",reply=keb.get_owner_keyboards(call.from_user.id))
            except Exception as e:
                print(e)
                await call.message.answer(f"ببورە كێشەیەك هەیە {e}")