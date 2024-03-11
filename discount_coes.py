from includes.keyboards import Keyboards
from includes.sqlite import Database
from includes.modules import types
from includes.states import add_discount_code
from includes.modules import types, FSMContext
import time
dis = add_discount_code()
db=Database("your_database.db")
keb = Keyboards()
class discount_code:
    def __init__(self, dp,bot):
        self.dp = dp
        self.bot = bot
    def handle(self):
        @self.dp.message_handler(lambda message: message.text == "كۆدی داشكان 🔑")
        async def group_challenges(message: types.Message):
            if db.get_admins(user_id=message.from_user.id):
                await message.answer("سەرجەم كۆدی داشكانەكان TFT تكایە یەكێك دیاری بكە :",reply_markup=keb.get_discount_code_button(admin=True))
            else:
                await message.answer("سەرجەم كۆدی داشكانەكان TFT تكایە یەكێك دیاری بكە :",reply_markup=keb.get_discount_code_button())
        @self.dp.message_handler(lambda m:m.text == "زيادكردنی كۆدی داشكان")
        async def add_disc(message: types.Message):
            await message.answer("زۆر باشە ، كۆدی كۆدی داشكان بنووسە",reply_markup=keb.back_confirm())
            await dis.entering_title.set()
        @self.dp.message_handler(state=dis.entering_title)
        async def add_disc(message: types.Message,state=FSMContext):
            if message.text == "پاشگەزبوونەوە":
                await message.answer("دووپاتكرایەوە ، چۆن هاوكاریت بكەم ؟",reply_markup=keb.get_owner_keyboards())
                await state.finish()
            else:
                async with state.proxy() as data:
                    data['title'] = message.text
                from aiogram.types import ReplyKeyboardRemove
                await message.answer("زۆر باشە ، دەقی كۆدی داشكان بنووسە",reply_markup=ReplyKeyboardRemove())
                await dis.entering_message.set()
        @self.dp.callback_query_handler(lambda c: c.data == 'add_photo_dis', state='*')
        async def add_photo(callback_query: types.CallbackQuery, state: FSMContext):
            await dis.entering_photo.set()
            await callback_query.message.answer("زۆر باشە ، تكایە وێنە بنێرە :")
        @self.dp.message_handler(content_types=['photo'], state=dis.entering_photo)
        async def process_photo(message: types.Message, state: FSMContext):
            current_state = await state.get_state()
            if current_state != state.finish:
                photo_id = message.photo[-1].file_id
                async with state.proxy() as data:
                    if 'photos_data' not in data:
                        data['photos_data'] = []
                    data['photos_data'].append(photo_id)
                keyboard = types.InlineKeyboardMarkup()
                keyboard.add(types.InlineKeyboardButton(text="زیادكردنی وێنە", callback_data="photos_dis"),
                                types.InlineKeyboardButton(text="دووپاتكردنەوە", callback_data="confirm_dis"),
                                types.InlineKeyboardButton(text="ڕەتكردنەوە", callback_data="decline_dis"))
                await self.bot.send_photo(chat_id=message.chat.id, photo=photo_id, caption=data.get('message', ""), reply_markup=keyboard)
        @self.dp.message_handler(state=dis.entering_message)
        async def group_challenges(message: types.Message,state:FSMContext):
            current_state = await state.get_state()
            if current_state != state.finish:

                if message.text == "پاشگەزبوونەوە":
                    pass
                else:
                    async with state.proxy() as data:
                        data['message'] = message.text
                    await dis.next()
                    keyboard = types.InlineKeyboardMarkup()
                    keyboard.add(types.InlineKeyboardButton(text="زیادكردنی وێنە", callback_data="photos_dis"),
                                types.InlineKeyboardButton(text="دووپاتكردنەوە", callback_data="confirm_dis"),
                                types.InlineKeyboardButton(text="ڕەتكردنەوە", callback_data="decline_dis"))
                    await message.answer("تكایە یەكێك لە هەڵبژاردنەكان دیاری بكە :", reply_markup=keyboard)
        @self.dp.callback_query_handler(lambda c: c.data in ['photos_dis','confirm_dis', 'decline_dis', 'back', 'add_button','confirm_yes_dis','confirm_dic_dis'], state='*')
        async def process_callback(callback_query: types.CallbackQuery, state: FSMContext):
            await self.bot.answer_callback_query(callback_query.id)
            choice = callback_query.data
            current_state = await state.get_state()
            if current_state != state.finish:
                async with state.proxy() as data:
                    if choice == "photos_dis":
                        if 'photos_data' in data and len(data['photos_data']) > 0:
                            media_group = types.MediaGroup()
                            for photo in data['photos_data']:
                                media_group.attach_photo(photo)
                            await callback_query.message.answer_media_group(media=media_group)
                            keyboard = types.InlineKeyboardMarkup()
                            keyboard.add(types.InlineKeyboardButton(text="زیادكردنی وێنە", callback_data="add_photo_dis"),
                                        types.InlineKeyboardButton(text="گەڕانەوە بۆ بەشەكان", callback_data="back"))
                            await callback_query.message.answer("هەڵبژاردن دیاری بكە :", reply_markup=keyboard)
                        else:
                            keyboard = types.InlineKeyboardMarkup()
                            keyboard.add(types.InlineKeyboardButton(text="زیادكردنی وێنە", callback_data="add_photo_dis"),
                                        types.InlineKeyboardButton(text="گەڕانەوە بۆ بەشەكان", callback_data="back"))
                            await callback_query.message.answer("هیچ وێنەیەك نیە ، تكایە هەڵبژاردن دیاری بكە :", reply_markup=keyboard)
                    elif choice == "confirm_dis":
                        keyboard = types.InlineKeyboardMarkup()
                        keyboard.add(types.InlineKeyboardButton(text="دووپاتكردنەوە", callback_data="confirm_yes_dis"),
                                    types.InlineKeyboardButton(text="ڕەتكردنەوە", callback_data="decline_dis"))
                        await callback_query.message.answer("ئایا دڵنایی لە ناردنی ئەم نامەیە?", reply_markup=keyboard)
                    elif choice == "confirm_yes_dis":
                        if 'photos_data' in data and data['photos_data']:
                            db.add_discount_code(data,photo=data['photos_data'][0])
                        else:
                            db.add_discount_code(data)
                        await callback_query.message.answer(text="بەسەركەوتووی زیادكرا",reply_markup=keb.get_owner_keyboards())
                        await state.finish()
        @self.dp.callback_query_handler(lambda c:c.data.startswith("delete_dis_code__"))
        async def delet_disc(call : types.CallbackQuery):
            button_title = call.data.split("__")[1]
            await call.message.answer("ئایا دڵنایی لە ڕەشكردنەوەی ؟",reply_markup=keb.get_confrim_delete_dis(button_title))
        @self.dp.callback_query_handler(lambda c:c.data.startswith("yesy_delete__"))
        async def delet_disc_confirm(call : types.CallbackQuery):
            button_title = call.data.split("__")[1]
            try:
                db.delete_column(name_table="discount",where="title",where_equal=button_title)
                await call.message.answer("بەسەركەوتووی ڕەشكرایەوە",reply=keb.get_discount_code_button(admin=True))
            except Exception as e:
                print(e)
                await call.message.answer(f"ببورە كێشەیەك هەیە {e}")